---
title: "disk_observer"
source: "https://libtorrent.org/reference-Custom_Storage.html"
---

[home](reference.md)

The disk I/O can be customized in libtorrent. In previous versions, the
customization was at the level of each torrent. Now, the customization point
is at the [session](reference-Session.md#session) level. All torrents added to a [session](reference-Session.md#session) will use the same
disk I/O subsystem, as determined by the disk\_io\_constructor (in
[session\_params](reference-Session.md#session_params)).

This allows the disk subsystem to also customize threading and disk job
management.

To customize the disk subsystem, implement [disk\_interface](reference-Custom_Storage.md#disk_interface) and provide a
factory function to the [session](reference-Session.md#session) constructor (via [session\_params](reference-Session.md#session_params)).

Example use:

```cpp
struct temp_storage
{
  explicit temp_storage(lt::file_storage const& fs) : m_files(fs) {}

  lt::span<char const> readv(lt::peer_request const r, lt::storage_error& ec) const
  {
    auto const i = m_file_data.find(r.piece);
    if (i == m_file_data.end())
    {
      ec.operation = lt::operation_t::file_read;
      ec.ec = boost::asio::error::eof;
      return {};
    }
    if (int(i->second.size()) <= r.start)
    {
      ec.operation = lt::operation_t::file_read;
      ec.ec = boost::asio::error::eof;
      return {};
    }
    return { i->second.data() + r.start, std::min(r.length, int(i->second.size()) - r.start) };
  }
  void writev(lt::span<char const> const b, lt::piece_index_t const piece, int const offset)
  {
    auto& data = m_file_data[piece];
    if (data.empty())
    {
      // allocate the whole piece, otherwise we'll invalidate the pointers
      // we have returned back to libtorrent
      int const size = piece_size(piece);
      data.resize(std::size_t(size));
    }
    TORRENT_ASSERT(offset + b.size() <= int(data.size()));
    std::memcpy(data.data() + offset, b.data(), std::size_t(b.size()));
  }
  lt::sha1_hash hash(lt::piece_index_t const piece
    , lt::span<lt::sha256_hash> const block_hashes, lt::storage_error& ec) const
  {
    auto const i = m_file_data.find(piece);
    if (i == m_file_data.end())
    {
      ec.operation = lt::operation_t::file_read;
      ec.ec = boost::asio::error::eof;
      return {};
    }
    if (!block_hashes.empty())
    {
      int const piece_size2 = m_files.piece_size2(piece);
      int const blocks_in_piece2 = m_files.blocks_in_piece2(piece);
      char const* buf = i->second.data();
      std::int64_t offset = 0;
      for (int k = 0; k < blocks_in_piece2; ++k)
      {
        lt::hasher256 h2;
        std::ptrdiff_t const len2 = std::min(lt::default_block_size, int(piece_size2 - offset));
        h2.update({ buf, len2 });
        buf += len2;
        offset += len2;
        block_hashes[k] = h2.final();
      }
    }
    return lt::hasher(i->second).final();
  }
  lt::sha256_hash hash2(lt::piece_index_t const piece, int const offset, lt::storage_error& ec)
  {
    auto const i = m_file_data.find(piece);
    if (i == m_file_data.end())
    {
      ec.operation = lt::operation_t::file_read;
      ec.ec = boost::asio::error::eof;
      return {};
    }

    int const piece_size = m_files.piece_size2(piece);

    std::ptrdiff_t const len = std::min(lt::default_block_size, piece_size - offset);

    lt::span<char const> b = {i->second.data() + offset, len};
    return lt::hasher256(b).final();
  }

private:
  int piece_size(lt::piece_index_t piece) const
  {
    int const num_pieces = static_cast<int>((m_files.total_size() + m_files.piece_length() - 1) / m_files.piece_length());
    return static_cast<int>(piece) < num_pieces - 1
      ? m_files.piece_length() : static_cast<int>(m_files.total_size() - std::int64_t(num_pieces - 1) * m_files.piece_length());
  }

  lt::file_storage const& m_files;
  std::map<lt::piece_index_t, std::vector<char>> m_file_data;
};

lt::storage_index_t pop(std::vector<lt::storage_index_t>& q)
{
  TORRENT_ASSERT(!q.empty());
  lt::storage_index_t const ret = q.back();
  q.pop_back();
  return ret;
}

struct temp_disk_io final : lt::disk_interface
  , lt::buffer_allocator_interface
{
  explicit temp_disk_io(lt::io_context& ioc): m_ioc(ioc) {}

  void settings_updated() override {}

  lt::storage_holder new_torrent(lt::storage_params const& params
    , std::shared_ptr<void> const&) override
  {
    lt::storage_index_t const idx = m_free_slots.empty()
      ? m_torrents.end_index()
      : pop(m_free_slots);
    auto storage = std::make_unique<temp_storage>(params.files);
    if (idx == m_torrents.end_index()) m_torrents.emplace_back(std::move(storage));
    else m_torrents[idx] = std::move(storage);
    return lt::storage_holder(idx, *this);
  }

  void remove_torrent(lt::storage_index_t const idx) override
  {
    m_torrents[idx].reset();
    m_free_slots.push_back(idx);
  }

  void abort(bool) override {}

  void async_read(lt::storage_index_t storage, lt::peer_request const& r
    , std::function<void(lt::disk_buffer_holder block, lt::storage_error const& se)> handler
    , lt::disk_job_flags_t) override
  {
    // this buffer is owned by the storage. It will remain valid for as
    // long as the torrent remains in the session. We don't need any lifetime
    // management of it.
    lt::storage_error error;
    lt::span<char const> b = m_torrents[storage]->readv(r, error);

    post(m_ioc, [handler, error, b, this]
      { handler(lt::disk_buffer_holder(*this, const_cast<char*>(b.data()), int(b.size())), error); });
  }

  bool async_write(lt::storage_index_t storage, lt::peer_request const& r
    , char const* buf, std::shared_ptr<lt::disk_observer>
    , std::function<void(lt::storage_error const&)> handler
    , lt::disk_job_flags_t) override
  {
    lt::span<char const> const b = { buf, r.length };

    m_torrents[storage]->writev(b, r.piece, r.start);

    post(m_ioc, [=]{ handler(lt::storage_error()); });
    return false;
  }

  void async_hash(lt::storage_index_t storage, lt::piece_index_t const piece
    , lt::span<lt::sha256_hash> block_hashes, lt::disk_job_flags_t
    , std::function<void(lt::piece_index_t, lt::sha1_hash const&, lt::storage_error const&)> handler) override
  {
    lt::storage_error error;
    lt::sha1_hash const hash = m_torrents[storage]->hash(piece, block_hashes, error);
    post(m_ioc, [=]{ handler(piece, hash, error); });
  }

  void async_hash2(lt::storage_index_t storage, lt::piece_index_t const piece
    , int const offset, lt::disk_job_flags_t
    , std::function<void(lt::piece_index_t, lt::sha256_hash const&, lt::storage_error const&)> handler) override
  {
    lt::storage_error error;
    lt::sha256_hash const hash = m_torrents[storage]->hash2(piece, offset, error);
    post(m_ioc, [=]{ handler(piece, hash, error); });
  }

  void async_move_storage(lt::storage_index_t, std::string p, lt::move_flags_t
    , std::function<void(lt::status_t, std::string const&, lt::storage_error const&)> handler) override
  {
    post(m_ioc, [=]{
      handler(lt::status_t::fatal_disk_error, p
        , lt::storage_error(lt::error_code(boost::system::errc::operation_not_supported, lt::system_category())));
    });
  }

  void async_release_files(lt::storage_index_t, std::function<void()>) override {}

  void async_delete_files(lt::storage_index_t, lt::remove_flags_t
    , std::function<void(lt::storage_error const&)> handler) override
  {
    post(m_ioc, [=]{ handler(lt::storage_error()); });
  }

  void async_check_files(lt::storage_index_t
    , lt::add_torrent_params const*
    , lt::aux::vector<std::string, lt::file_index_t>
    , std::function<void(lt::status_t, lt::storage_error const&)> handler) override
  {
    post(m_ioc, [=]{ handler(lt::status_t::no_error, lt::storage_error()); });
  }

  void async_rename_file(lt::storage_index_t
    , lt::file_index_t const idx
    , std::string const name
    , std::function<void(std::string const&, lt::file_index_t, lt::storage_error const&)> handler) override
  {
    post(m_ioc, [=]{ handler(name, idx, lt::storage_error()); });
  }

  void async_stop_torrent(lt::storage_index_t, std::function<void()> handler) override
  {
    post(m_ioc, handler);
  }

  void async_set_file_priority(lt::storage_index_t
    , lt::aux::vector<lt::download_priority_t, lt::file_index_t> prio
    , std::function<void(lt::storage_error const&
      , lt::aux::vector<lt::download_priority_t, lt::file_index_t>)> handler) override
  {
    post(m_ioc, [=]{
      handler(lt::storage_error(lt::error_code(
        boost::system::errc::operation_not_supported, lt::system_category())), std::move(prio));
    });
  }

  void async_clear_piece(lt::storage_index_t, lt::piece_index_t index
    , std::function<void(lt::piece_index_t)> handler) override
  {
    post(m_ioc, [=]{ handler(index); });
  }

  // implements buffer_allocator_interface
  void free_disk_buffer(char*) override
  {
    // never free any buffer. We only return buffers owned by the storage
    // object
  }

  void update_stats_counters(lt::counters&) const override {}

  std::vector<lt::open_file_state> get_status(lt::storage_index_t) const override
  { return {}; }

  void submit_jobs() override {}

private:

  lt::aux::vector<std::shared_ptr<temp_storage>, lt::storage_index_t> m_torrents;

  // slots that are unused in the m_torrents vector
  std::vector<lt::storage_index_t> m_free_slots;

  // callbacks are posted on this
  lt::io_context& m_ioc;
};

std::unique_ptr<lt::disk_interface> temp_disk_constructor(
  lt::io_context& ioc, lt::settings_interface const&, lt::counters&)
{
  return std::make_unique<temp_disk_io>(ioc);
}
```

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:class+disk_observer&labels=documentation&body=Documentation+under+heading+%22class+disk_observer%22+could+be+improved)]

# disk\_observer

Declared in "[libtorrent/disk\_observer.hpp](include/libtorrent/disk_observer.hpp)"

```cpp
struct disk_observer
{
   virtual void on_disk () = 0;
};
```

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disk_observer%3A%3A%5Bon_disk%28%29%5D&labels=documentation&body=Documentation+under+heading+%22disk_observer%3A%3A%5Bon_disk%28%29%5D%22+could+be+improved)]

## on\_disk()

```cpp
virtual void on_disk () = 0;
```

called when the disk cache size has dropped
below the low watermark again and we can
resume downloading from peers

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:class+buffer_allocator_interface&labels=documentation&body=Documentation+under+heading+%22class+buffer_allocator_interface%22+could+be+improved)]

# buffer\_allocator\_interface

Declared in "[libtorrent/disk\_buffer\_holder.hpp](include/libtorrent/disk_buffer_holder.hpp)"

the interface for freeing disk buffers, used by the [disk\_buffer\_holder](reference-Custom_Storage.md#disk_buffer_holder).
when implementing [disk\_interface](reference-Custom_Storage.md#disk_interface), this must also be implemented in order
to return disk buffers back to libtorrent

```cpp
struct buffer_allocator_interface
{
   virtual void free_disk_buffer (char* b) = 0;
};
```

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:class+disk_buffer_holder&labels=documentation&body=Documentation+under+heading+%22class+disk_buffer_holder%22+could+be+improved)]

# disk\_buffer\_holder

Declared in "[libtorrent/disk\_buffer\_holder.hpp](include/libtorrent/disk_buffer_holder.hpp)"

The disk buffer holder acts like a unique\_ptr that frees a disk buffer
when it's destructed

If this buffer holder is moved-from, default constructed or reset,
data() will return nullptr.

```cpp
struct disk_buffer_holder
{
   disk_buffer_holder& operator= (disk_buffer_holder&&) & noexcept;
   disk_buffer_holder (disk_buffer_holder&&) noexcept;
   disk_buffer_holder (disk_buffer_holder const&) = delete;
   disk_buffer_holder& operator= (disk_buffer_holder const&) = delete;
   disk_buffer_holder (buffer_allocator_interface& alloc
      , char* buf, int sz) noexcept;
   disk_buffer_holder () noexcept = default;
   ~disk_buffer_holder ();
   char* data () const noexcept;
   void reset ();
   void swap (disk_buffer_holder& h) noexcept;
   bool is_mutable () const noexcept;
   explicit operator bool () const noexcept;
   std::ptrdiff_t size () const;
};
```

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disk_buffer_holder%3A%3A%5Bdisk_buffer_holder%28%29%5D&labels=documentation&body=Documentation+under+heading+%22disk_buffer_holder%3A%3A%5Bdisk_buffer_holder%28%29%5D%22+could+be+improved)]

## disk\_buffer\_holder()

```cpp
disk_buffer_holder (buffer_allocator_interface& alloc
      , char* buf, int sz) noexcept;
```

construct a buffer holder that will free the held buffer
using a disk buffer pool directly (there's only one
disk\_buffer\_pool per [session](reference-Session.md#session))

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disk_buffer_holder%3A%3A%5Bdisk_buffer_holder%28%29%5D&labels=documentation&body=Documentation+under+heading+%22disk_buffer_holder%3A%3A%5Bdisk_buffer_holder%28%29%5D%22+could+be+improved)]

## disk\_buffer\_holder()

```cpp
disk_buffer_holder () noexcept = default;
```

default construct a holder that does not own any buffer

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disk_buffer_holder%3A%3A%5B~disk_buffer_holder%28%29%5D&labels=documentation&body=Documentation+under+heading+%22disk_buffer_holder%3A%3A%5B~disk_buffer_holder%28%29%5D%22+could+be+improved)]

## ~disk\_buffer\_holder()

```cpp
~disk_buffer_holder ();
```

frees disk buffer held by this object

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disk_buffer_holder%3A%3A%5Bdata%28%29%5D&labels=documentation&body=Documentation+under+heading+%22disk_buffer_holder%3A%3A%5Bdata%28%29%5D%22+could+be+improved)]

## data()

```cpp
char* data () const noexcept;
```

return a pointer to the held buffer, if any. Otherwise returns nullptr.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disk_buffer_holder%3A%3A%5Breset%28%29%5D&labels=documentation&body=Documentation+under+heading+%22disk_buffer_holder%3A%3A%5Breset%28%29%5D%22+could+be+improved)]

## reset()

```cpp
void reset ();
```

free the held disk buffer, if any, and clear the holder. This sets the
holder object to a default-constructed state

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disk_buffer_holder%3A%3A%5Bswap%28%29%5D&labels=documentation&body=Documentation+under+heading+%22disk_buffer_holder%3A%3A%5Bswap%28%29%5D%22+could+be+improved)]

## swap()

```cpp
void swap (disk_buffer_holder& h) noexcept;
```

swap pointers of two disk buffer holders.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disk_buffer_holder%3A%3A%5Bis_mutable%28%29%5D&labels=documentation&body=Documentation+under+heading+%22disk_buffer_holder%3A%3A%5Bis_mutable%28%29%5D%22+could+be+improved)]

## is\_mutable()

```cpp
bool is_mutable () const noexcept;
```

if this returns true, the buffer may not be modified in place

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disk_buffer_holder%3A%3A%5Bbool%28%29%5D&labels=documentation&body=Documentation+under+heading+%22disk_buffer_holder%3A%3A%5Bbool%28%29%5D%22+could+be+improved)]

## bool()

```cpp
explicit operator bool () const noexcept;
```

implicitly convertible to true if the object is currently holding a
buffer

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:class+settings_interface&labels=documentation&body=Documentation+under+heading+%22class+settings_interface%22+could+be+improved)]

# settings\_interface

Declared in "[libtorrent/settings\_pack.hpp](include/libtorrent/settings_pack.hpp)"

the common interface to [settings\_pack](reference-Settings.md#settings_pack) and the internal representation of
settings.

```cpp
struct settings_interface
{
   virtual bool has_val (int name) const = 0;
   virtual void set_bool (int name, bool val) = 0;
   virtual void set_str (int name, std::string val) = 0;
   virtual void set_int (int name, int val) = 0;
   virtual int get_int (int name) const = 0;
   virtual bool get_bool (int name) const = 0;
   virtual std::string const& get_str (int name) const = 0;
};
```

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:class+open_file_state&labels=documentation&body=Documentation+under+heading+%22class+open_file_state%22+could+be+improved)]

# open\_file\_state

Declared in "[libtorrent/disk\_interface.hpp](include/libtorrent/disk_interface.hpp)"

this contains information about a file that's currently open by the
libtorrent disk I/O subsystem. It's associated with a single torrent.

```cpp
struct open_file_state
{
   file_index_t file_index;
   file_open_mode_t open_mode;
   time_point last_use;
};
```

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:open_file_state%3A%3A%5Bfile_index%5D&labels=documentation&body=Documentation+under+heading+%22open_file_state%3A%3A%5Bfile_index%5D%22+could+be+improved)]

file\_index
:   the index of the file this [entry](reference-Bencoding.md#entry) refers to into the file\_storage
    file list of this torrent. This starts indexing at 0.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:open_file_state%3A%3A%5Bopen_mode%5D&labels=documentation&body=Documentation+under+heading+%22open_file_state%3A%3A%5Bopen_mode%5D%22+could+be+improved)]

open\_mode
:   open\_mode is a bitmask of the file flags this file is currently
    opened with. For possible flags, see [file\_open\_mode\_t](reference-Custom_Storage.md#file_open_mode_t).

    Note that the read/write mode is not a bitmask. The two least significant bits are used
    to represent the read/write mode. Those bits can be masked out using the rw\_mask constant.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:open_file_state%3A%3A%5Blast_use%5D&labels=documentation&body=Documentation+under+heading+%22open_file_state%3A%3A%5Blast_use%5D%22+could+be+improved)]

last\_use
:   a (high precision) timestamp of when the file was last used.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:class+disk_interface&labels=documentation&body=Documentation+under+heading+%22class+disk_interface%22+could+be+improved)]

# disk\_interface

Declared in "[libtorrent/disk\_interface.hpp](include/libtorrent/disk_interface.hpp)"

The [disk\_interface](reference-Custom_Storage.md#disk_interface) is the customization point for disk I/O in libtorrent.
implement this interface and provide a factory function to the [session](reference-Session.md#session) constructor
use custom disk I/O. All functions on the disk subsystem (implementing
[disk\_interface](reference-Custom_Storage.md#disk_interface)) are called from within libtorrent's network thread. For
disk I/O to be performed in a separate thread, the disk subsystem has to
manage that itself.

Although the functions are called async\_\*, they do not technically
*have* to be asynchronous, but they support being asynchronous, by
expecting the result passed back into a callback. The callbacks must be
posted back onto the network thread via the io\_context object passed into
the constructor. The callbacks will be run in the network thread.

```cpp
struct disk_interface
{
   virtual storage_holder new_torrent (storage_params const& p
      , std::shared_ptr<void> const& torrent) = 0;
   virtual void remove_torrent (storage_index_t) = 0;
   virtual bool async_write (storage_index_t storage, peer_request const& r
      , char const* buf, std::shared_ptr<disk_observer> o
      , std::function<void(storage_error const&)> handler
      , disk_job_flags_t flags = {}) = 0;
   virtual void async_read (storage_index_t storage, peer_request const& r
      , std::function<void(disk_buffer_holder, storage_error const&)> handler
      , disk_job_flags_t flags = {}) = 0;
   virtual void async_hash (storage_index_t storage, piece_index_t piece, span<sha256_hash> v2
      , disk_job_flags_t flags
      , std::function<void(piece_index_t, sha1_hash const&, storage_error const&)> handler) = 0;
   virtual void async_hash2 (storage_index_t storage, piece_index_t piece, int offset, disk_job_flags_t flags
      , std::function<void(piece_index_t, sha256_hash const&, storage_error const&)> handler) = 0;
   virtual void async_move_storage (storage_index_t storage, std::string p, move_flags_t flags
      , std::function<void(status_t, std::string const&, storage_error const&)> handler) = 0;
   virtual void async_release_files (storage_index_t storage
      , std::function<void()> handler = std::function<void()>()) = 0;
   virtual void async_check_files (storage_index_t storage
      , add_torrent_params const* resume_data
      , aux::vector<std::string, file_index_t> links
      , std::function<void(status_t, storage_error const&)> handler) = 0;
   virtual void async_stop_torrent (storage_index_t storage
      , std::function<void()> handler = std::function<void()>()) = 0;
   virtual void async_rename_file (storage_index_t storage
      , file_index_t index, std::string name
      , std::function<void(std::string const&, file_index_t, storage_error const&)> handler) = 0;
   virtual void async_delete_files (storage_index_t storage, remove_flags_t options
      , std::function<void(storage_error const&)> handler) = 0;
   virtual void async_set_file_priority (storage_index_t storage
      , aux::vector<download_priority_t, file_index_t> prio
      , std::function<void(storage_error const&
      , aux::vector<download_priority_t, file_index_t>)> handler) = 0;
   virtual void async_clear_piece (storage_index_t storage, piece_index_t index
      , std::function<void(piece_index_t)> handler) = 0;
   virtual void update_stats_counters (counters& c) const = 0;
   virtual std::vector<open_file_state> get_status (storage_index_t) const = 0;
   virtual void abort (bool wait) = 0;
   virtual void submit_jobs () = 0;
   virtual void settings_updated () = 0;

   static constexpr disk_job_flags_t force_copy  = 0_bit;
   static constexpr disk_job_flags_t sequential_access  = 3_bit;
   static constexpr disk_job_flags_t volatile_read  = 4_bit;
   static constexpr disk_job_flags_t v1_hash  = 5_bit;
   static constexpr disk_job_flags_t flush_piece  = 7_bit;
};
```

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disk_interface%3A%3A%5Bnew_torrent%28%29%5D&labels=documentation&body=Documentation+under+heading+%22disk_interface%3A%3A%5Bnew_torrent%28%29%5D%22+could+be+improved)]

## new\_torrent()

```cpp
virtual storage_holder new_torrent (storage_params const& p
      , std::shared_ptr<void> const& torrent) = 0;
```

this is called when a new torrent is added. The shared\_ptr can be
used to hold the internal torrent object alive as long as there are
outstanding disk operations on the storage.
The returned [storage\_holder](reference-Custom_Storage.md#storage_holder) is an owning reference to the underlying
storage that was just created. It is fundamentally a storage\_index\_t

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disk_interface%3A%3A%5Bremove_torrent%28%29%5D&labels=documentation&body=Documentation+under+heading+%22disk_interface%3A%3A%5Bremove_torrent%28%29%5D%22+could+be+improved)]

## remove\_torrent()

```cpp
virtual void remove_torrent (storage_index_t) = 0;
```

remove the storage with the specified index. This is not expected to
delete any files from disk, just to clean up any resources associated
with the specified storage.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disk_interface%3A%3A%5Basync_write%28%29+async_read%28%29%5D&labels=documentation&body=Documentation+under+heading+%22disk_interface%3A%3A%5Basync_write%28%29+async_read%28%29%5D%22+could+be+improved)]

## async\_write() async\_read()

```cpp
virtual bool async_write (storage_index_t storage, peer_request const& r
      , char const* buf, std::shared_ptr<disk_observer> o
      , std::function<void(storage_error const&)> handler
      , disk_job_flags_t flags = {}) = 0;
virtual void async_read (storage_index_t storage, peer_request const& r
      , std::function<void(disk_buffer_holder, storage_error const&)> handler
      , disk_job_flags_t flags = {}) = 0;
```

perform a read or write operation from/to the specified storage
index and the specified request. When the operation completes, call
handler possibly with a [disk\_buffer\_holder](reference-Custom_Storage.md#disk_buffer_holder), holding the buffer with
the result. Flags may be set to affect the read operation. See
disk\_job\_flags\_t.

The [disk\_observer](reference-Custom_Storage.md#disk_observer) is a callback to indicate that
the store buffer/disk write queue is below the watermark to let peers
start writing buffers to disk again. When async\_write() returns
true, indicating the write queue is full, the peer will stop
further writes and wait for the passed-in disk\_observer to be
notified before resuming.

Note that for async\_read, the [peer\_request](reference-Core.md#peer_request) (r) is not
necessarily aligned to blocks (but it is most of the time). However,
all writes (passed to async\_write) are guaranteed to be block
aligned.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disk_interface%3A%3A%5Basync_hash%28%29%5D&labels=documentation&body=Documentation+under+heading+%22disk_interface%3A%3A%5Basync_hash%28%29%5D%22+could+be+improved)]

## async\_hash()

```cpp
virtual void async_hash (storage_index_t storage, piece_index_t piece, span<sha256_hash> v2
      , disk_job_flags_t flags
      , std::function<void(piece_index_t, sha1_hash const&, storage_error const&)> handler) = 0;
```

Compute hash(es) for the specified piece. Unless the v1\_hash flag is
set (in flags), the SHA-1 hash of the whole piece does not need
to be computed.

The v2 span is optional and can be empty, which means v2 hashes
should not be computed. If v2 is non-empty it must be at least large
enough to hold all v2 blocks in the piece, and this function will
fill in the span with the SHA-256 block hashes of the piece.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disk_interface%3A%3A%5Basync_hash2%28%29%5D&labels=documentation&body=Documentation+under+heading+%22disk_interface%3A%3A%5Basync_hash2%28%29%5D%22+could+be+improved)]

## async\_hash2()

```cpp
virtual void async_hash2 (storage_index_t storage, piece_index_t piece, int offset, disk_job_flags_t flags
      , std::function<void(piece_index_t, sha256_hash const&, storage_error const&)> handler) = 0;
```

computes the v2 hash (SHA-256) of a single block. The block at
offset in piece piece.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disk_interface%3A%3A%5Basync_move_storage%28%29%5D&labels=documentation&body=Documentation+under+heading+%22disk_interface%3A%3A%5Basync_move_storage%28%29%5D%22+could+be+improved)]

## async\_move\_storage()

```cpp
virtual void async_move_storage (storage_index_t storage, std::string p, move_flags_t flags
      , std::function<void(status_t, std::string const&, storage_error const&)> handler) = 0;
```

called to request the files for the specified storage/torrent be
moved to a new location. It is the disk I/O object's responsibility
to synchronize this with any currently outstanding disk operations to
the storage. Whether files are replaced at the destination path or
not is controlled by flags (see [move\_flags\_t](reference-Storage.md#move_flags_t)).

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disk_interface%3A%3A%5Basync_release_files%28%29%5D&labels=documentation&body=Documentation+under+heading+%22disk_interface%3A%3A%5Basync_release_files%28%29%5D%22+could+be+improved)]

## async\_release\_files()

```cpp
virtual void async_release_files (storage_index_t storage
      , std::function<void()> handler = std::function<void()>()) = 0;
```

This is called on disk I/O objects to request they close all open
files for the specified storage/torrent. If file handles are not
pooled/cached, it can be a no-op. For truly asynchronous disk I/O,
this should provide at least one point in time when all files are
closed. It is possible that later asynchronous operations will
re-open some of the files, by the time this completion handler is
called, that's fine.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disk_interface%3A%3A%5Basync_check_files%28%29%5D&labels=documentation&body=Documentation+under+heading+%22disk_interface%3A%3A%5Basync_check_files%28%29%5D%22+could+be+improved)]

## async\_check\_files()

```cpp
virtual void async_check_files (storage_index_t storage
      , add_torrent_params const* resume_data
      , aux::vector<std::string, file_index_t> links
      , std::function<void(status_t, storage_error const&)> handler) = 0;
```

this is called when torrents are added to validate their resume data
against the files on disk. This function is expected to do a few things:

if links is non-empty, it contains a string for each file in the
torrent. The string being a path to an existing identical file. The
default behavior is to create hard links of those files into the
storage of the new torrent (specified by storage). An empty
string indicates that there is no known identical file. This is part
of the "mutable torrent" feature, where files can be reused from
other torrents.

The resume\_data points the resume data passed in by the client.

If the resume\_data->flags field has the seed\_mode flag set, all
files/pieces are expected to be on disk already. This should be
verified. Not just the existence of the file, but also that it has
the correct size.

Any file with a piece set in the resume\_data->have\_pieces bitmask
should exist on disk, this should be verified. Pad files and files
with zero priority may be skipped.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disk_interface%3A%3A%5Basync_stop_torrent%28%29%5D&labels=documentation&body=Documentation+under+heading+%22disk_interface%3A%3A%5Basync_stop_torrent%28%29%5D%22+could+be+improved)]

## async\_stop\_torrent()

```cpp
virtual void async_stop_torrent (storage_index_t storage
      , std::function<void()> handler = std::function<void()>()) = 0;
```

This is called when a torrent is stopped. It gives the disk I/O
object an opportunity to flush any data to disk that's currently kept
cached. This function should at least do the same thing as
[async\_release\_files()](reference-Custom_Storage.md#async_release_files()).

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disk_interface%3A%3A%5Basync_rename_file%28%29%5D&labels=documentation&body=Documentation+under+heading+%22disk_interface%3A%3A%5Basync_rename_file%28%29%5D%22+could+be+improved)]

## async\_rename\_file()

```cpp
virtual void async_rename_file (storage_index_t storage
      , file_index_t index, std::string name
      , std::function<void(std::string const&, file_index_t, storage_error const&)> handler) = 0;
```

This function is called when the name of a file in the specified
storage has been requested to be renamed. The disk I/O object is
responsible for renaming the file without racing with other
potentially outstanding operations against the file (such as read,
write, move, etc.).

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disk_interface%3A%3A%5Basync_delete_files%28%29%5D&labels=documentation&body=Documentation+under+heading+%22disk_interface%3A%3A%5Basync_delete_files%28%29%5D%22+could+be+improved)]

## async\_delete\_files()

```cpp
virtual void async_delete_files (storage_index_t storage, remove_flags_t options
      , std::function<void(storage_error const&)> handler) = 0;
```

This function is called when some file(s) on disk have been requested
to be removed by the client. storage indicates which torrent is
referred to. See [session\_handle](reference-Session.md#session_handle) for remove\_flags\_t flags
indicating which files are to be removed.
e.g. [session\_handle::delete\_files](reference-Session.md#delete_files) - delete all files
[session\_handle::delete\_partfile](reference-Session.md#delete_partfile) - only delete part file.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disk_interface%3A%3A%5Basync_set_file_priority%28%29%5D&labels=documentation&body=Documentation+under+heading+%22disk_interface%3A%3A%5Basync_set_file_priority%28%29%5D%22+could+be+improved)]

## async\_set\_file\_priority()

```cpp
virtual void async_set_file_priority (storage_index_t storage
      , aux::vector<download_priority_t, file_index_t> prio
      , std::function<void(storage_error const&
      , aux::vector<download_priority_t, file_index_t>)> handler) = 0;
```

This is called to set the priority of some or all files. Changing the
priority from or to 0 may involve moving data to and from the
partfile. The disk I/O object is responsible for correctly
synchronizing this work to not race with any potentially outstanding
asynchronous operations affecting these files.

prio is a vector of the file priority for all files. If it's
shorter than the total number of files in the torrent, they are
assumed to be set to the default priority.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disk_interface%3A%3A%5Basync_clear_piece%28%29%5D&labels=documentation&body=Documentation+under+heading+%22disk_interface%3A%3A%5Basync_clear_piece%28%29%5D%22+could+be+improved)]

## async\_clear\_piece()

```cpp
virtual void async_clear_piece (storage_index_t storage, piece_index_t index
      , std::function<void(piece_index_t)> handler) = 0;
```

This is called when a piece fails the hash check, to ensure there are
no outstanding disk operations to the piece before blocks are
re-requested from peers to overwrite the existing blocks. The disk I/O
object does not need to perform any action other than synchronize
with all outstanding disk operations to the specified piece before
posting the result back.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disk_interface%3A%3A%5Bupdate_stats_counters%28%29%5D&labels=documentation&body=Documentation+under+heading+%22disk_interface%3A%3A%5Bupdate_stats_counters%28%29%5D%22+could+be+improved)]

## update\_stats\_counters()

```cpp
virtual void update_stats_counters (counters& c) const = 0;
```

[update\_stats\_counters()](reference-Custom_Storage.md#update_stats_counters()) is called to give the disk storage an
opportunity to update gauges in the c stats [counters](reference-Stats.md#counters), that aren't
updated continuously as operations are performed. This is called
before a snapshot of the [counters](reference-Stats.md#counters) are passed to the client.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disk_interface%3A%3A%5Bget_status%28%29%5D&labels=documentation&body=Documentation+under+heading+%22disk_interface%3A%3A%5Bget_status%28%29%5D%22+could+be+improved)]

## get\_status()

```cpp
virtual std::vector<open_file_state> get_status (storage_index_t) const = 0;
```

Return a list of all the files that are currently open for the
specified storage/torrent. This is is just used for the client to
query the currently open files, and which modes those files are open
in.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disk_interface%3A%3A%5Babort%28%29%5D&labels=documentation&body=Documentation+under+heading+%22disk_interface%3A%3A%5Babort%28%29%5D%22+could+be+improved)]

## abort()

```cpp
virtual void abort (bool wait) = 0;
```

this is called when the [session](reference-Session.md#session) is starting to shut down. The disk
I/O object is expected to flush any outstanding write jobs, cancel
hash jobs and initiate tearing down of any internal threads. If
wait is true, this should be asynchronous. i.e. this call should
not return until all threads have stopped and all jobs have either
been aborted or completed and the disk I/O object is ready to be
destructed.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disk_interface%3A%3A%5Bsubmit_jobs%28%29%5D&labels=documentation&body=Documentation+under+heading+%22disk_interface%3A%3A%5Bsubmit_jobs%28%29%5D%22+could+be+improved)]

## submit\_jobs()

```cpp
virtual void submit_jobs () = 0;
```

This will be called after a batch of disk jobs has been issues (via
the async\_\* ). It gives the disk I/O object an opportunity to
notify any potential condition variables to wake up the disk
thread(s). The async\_\* calls can of course also notify condition
variables, but doing it in this call allows for batching jobs, by
issuing the notification once for a collection of jobs.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disk_interface%3A%3A%5Bsettings_updated%28%29%5D&labels=documentation&body=Documentation+under+heading+%22disk_interface%3A%3A%5Bsettings_updated%28%29%5D%22+could+be+improved)]

## settings\_updated()

```cpp
virtual void settings_updated () = 0;
```

This is called to notify the disk I/O object that the settings have
been updated. In the disk io constructor, a [settings\_interface](reference-Custom_Storage.md#settings_interface)
reference is passed in. Whenever these settings are updated, this
function is called to allow the disk I/O object to react to any
changed settings relevant to its operations.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disk_interface%3A%3A%5Bforce_copy%5D&labels=documentation&body=Documentation+under+heading+%22disk_interface%3A%3A%5Bforce_copy%5D%22+could+be+improved)]

force\_copy
:   force making a copy of the cached block, rather than getting a
    reference to a block already in the cache. This is used the block is
    expected to be overwritten very soon, by async\_write()`, and we need
    access to the previous content.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disk_interface%3A%3A%5Bsequential_access%5D&labels=documentation&body=Documentation+under+heading+%22disk_interface%3A%3A%5Bsequential_access%5D%22+could+be+improved)]

sequential\_access
:   hint that there may be more disk operations with sequential access to
    the file

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disk_interface%3A%3A%5Bvolatile_read%5D&labels=documentation&body=Documentation+under+heading+%22disk_interface%3A%3A%5Bvolatile_read%5D%22+could+be+improved)]

volatile\_read
:   don't keep the read block in cache. This is a hint that this block is
    unlikely to be read again anytime soon, and caching it would be
    wasteful.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disk_interface%3A%3A%5Bv1_hash%5D&labels=documentation&body=Documentation+under+heading+%22disk_interface%3A%3A%5Bv1_hash%5D%22+could+be+improved)]

v1\_hash
:   compute a v1 piece hash. This is only used by the [async\_hash()](reference-Custom_Storage.md#async_hash()) call.
    If this flag is not set in the [async\_hash()](reference-Custom_Storage.md#async_hash()) call, the SHA-1 piece
    hash does not need to be computed.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disk_interface%3A%3A%5Bflush_piece%5D&labels=documentation&body=Documentation+under+heading+%22disk_interface%3A%3A%5Bflush_piece%5D%22+could+be+improved)]

flush\_piece
:   this flag instructs a hash job that we just completed this piece, and
    it should be flushed to disk

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:class+storage_holder&labels=documentation&body=Documentation+under+heading+%22class+storage_holder%22+could+be+improved)]

# storage\_holder

Declared in "[libtorrent/disk\_interface.hpp](include/libtorrent/disk_interface.hpp)"

a unique, owning, reference to the storage of a torrent in a disk io
subsystem (class that implements [disk\_interface](reference-Custom_Storage.md#disk_interface)). This is held by the
internal libtorrent torrent object to tie the storage object allocated
for a torrent to the lifetime of the internal torrent object. When a
torrent is removed from the [session](reference-Session.md#session), this holder is destructed and will
inform the disk object.

```cpp
struct storage_holder
{
   storage_holder () = default;
   ~storage_holder ();
   storage_holder (storage_index_t idx, disk_interface& disk_io);
   explicit operator bool () const;
   operator storage_index_t () const;
   void reset ();
   storage_holder (storage_holder const&) = delete;
   storage_holder& operator= (storage_holder const&) = delete;
   storage_holder (storage_holder&& rhs) noexcept;
   storage_holder& operator= (storage_holder&& rhs) noexcept;
};
```

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_open_mode_t&labels=documentation&body=Documentation+under+heading+%22file_open_mode_t%22+could+be+improved)]

# file\_open\_mode\_t

Declared in "[libtorrent/disk\_interface.hpp](include/libtorrent/disk_interface.hpp)"

read\_only
:   open the file for reading only

write\_only
:   open the file for writing only

read\_write
:   open the file for reading and writing

rw\_mask
:   the mask for the bits determining read or write mode

sparse
:   open the file in sparse mode (if supported by the
    filesystem).

no\_atime
:   don't update the access timestamps on the file (if
    supported by the operating system and filesystem).
    this generally improves disk performance.

random\_access
:   When this is not set, the kernel is hinted that access to this file will
    be made sequentially.

mmapped
:   the file is memory mapped
