---
title: "storage_params"
source: "https://libtorrent.org/reference-Storage.html"
---

[home](reference.md)

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:class+storage_params&labels=documentation&body=Documentation+under+heading+%22class+storage_params%22+could+be+improved)]

# storage\_params

Declared in "[libtorrent/storage\_defs.hpp](include/libtorrent/storage_defs.hpp)"

a parameter pack used to construct the storage for a torrent, used in
[disk\_interface](reference-Custom_Storage.md#disk_interface)

```cpp
struct storage_params
{
   storage_params (file_storage const& f, file_storage const* mf
      , std::string const& sp, storage_mode_t const sm
      , aux::vector<download_priority_t, file_index_t> const& prio
      , sha1_hash const& ih);

   file_storage const& files;
   file_storage const* mapped_files  = nullptr;
   std::string const& path;
   storage_mode_t mode {storage_mode_sparse};
   aux::vector<download_priority_t, file_index_t> const& priorities;
   sha1_hash info_hash;
};
```

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:class+file_slice&labels=documentation&body=Documentation+under+heading+%22class+file_slice%22+could+be+improved)]

# file\_slice

Declared in "[libtorrent/file\_storage.hpp](include/libtorrent/file_storage.hpp)"

represents a window of a file in a torrent.

The file\_index refers to the index of the file (in the [torrent\_info](reference-Torrent_Info.md#torrent_info)).
To get the path and filename, use file\_path() and give the file\_index
as argument. The offset is the byte offset in the file where the range
starts, and size is the number of bytes this range is. The size + offset
will never be greater than the file size.

```cpp
struct file_slice
{
   file_index_t file_index;
   std::int64_t offset;
   std::int64_t size;
};
```

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_slice%3A%3A%5Bfile_index%5D&labels=documentation&body=Documentation+under+heading+%22file_slice%3A%3A%5Bfile_index%5D%22+could+be+improved)]

file\_index
:   the index of the file

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_slice%3A%3A%5Boffset%5D&labels=documentation&body=Documentation+under+heading+%22file_slice%3A%3A%5Boffset%5D%22+could+be+improved)]

offset
:   the offset from the start of the file, in bytes

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_slice%3A%3A%5Bsize%5D&labels=documentation&body=Documentation+under+heading+%22file_slice%3A%3A%5Bsize%5D%22+could+be+improved)]

size
:   the size of the window, in bytes

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:class+file_storage&labels=documentation&body=Documentation+under+heading+%22class+file_storage%22+could+be+improved)]

# file\_storage

Declared in "[libtorrent/file\_storage.hpp](include/libtorrent/file_storage.hpp)"

The file\_storage class represents a file list and the piece
size. Everything necessary to interpret a regular bittorrent storage
file structure.

```cpp
class file_storage
{
   bool is_valid () const;
   void reserve (int num_files);
   void add_file (std::string const& path, std::int64_t file_size
      , file_flags_t file_flags = {}
      , std::time_t mtime = 0, string_view symlink_path = string_view()
      , char const* root_hash = nullptr);
   void add_file_borrow (string_view filename
      , std::string const& path, std::int64_t file_size
      , file_flags_t file_flags = {}, char const* filehash = nullptr
      , std::int64_t mtime = 0, string_view symlink_path = string_view()
      , char const* root_hash = nullptr);
   void add_file (error_code& ec, std::string const& path, std::int64_t file_size
      , file_flags_t file_flags = {}
      , std::time_t mtime = 0, string_view symlink_path = string_view()
      , char const* root_hash = nullptr);
   void add_file_borrow (error_code& ec, string_view filename
      , std::string const& path, std::int64_t file_size
      , file_flags_t file_flags = {}, char const* filehash = nullptr
      , std::int64_t mtime = 0, string_view symlink_path = string_view()
      , char const* root_hash = nullptr);
   void rename_file (file_index_t index, std::string const& new_filename);
   std::vector<file_slice> map_block (piece_index_t piece, std::int64_t offset
      , std::int64_t size) const;
   peer_request map_file (file_index_t file, std::int64_t offset, int size) const;
   int num_files () const noexcept;
   file_index_t end_file () const noexcept;
   index_range<file_index_t> file_range () const noexcept;
   std::int64_t total_size () const;
   int num_pieces () const;
   void set_num_pieces (int n);
   piece_index_t end_piece () const;
   piece_index_t last_piece () const;
   index_range<piece_index_t> piece_range () const noexcept;
   void set_piece_length (int l);
   int piece_length () const;
   int piece_size (piece_index_t index) const;
   int piece_size2 (piece_index_t index) const;
   int blocks_in_piece2 (piece_index_t index) const;
   int blocks_per_piece () const;
   void set_name (std::string const& n);
   std::string const& name () const;
   void swap (file_storage& ti) noexcept;
   void canonicalize ();
   sha256_hash root (file_index_t index) const;
   std::int64_t file_size (file_index_t index) const;
   char const* root_ptr (file_index_t const index) const;
   sha1_hash hash (file_index_t index) const;
   string_view file_name (file_index_t index) const;
   std::int64_t file_offset (file_index_t index) const;
   std::time_t mtime (file_index_t index) const;
   bool pad_file_at (file_index_t index) const;
   std::string symlink (file_index_t index) const;
   std::string file_path (file_index_t index, std::string const& save_path = "") const;
   index_range<piece_index_t::diff_type> file_piece_range (file_index_t) const;
   int file_num_pieces (file_index_t index) const;
   int file_num_blocks (file_index_t index) const;
   int file_first_piece_node (file_index_t index) const;
   int file_first_block_node (file_index_t index) const;
   std::uint32_t file_path_hash (file_index_t index, std::string const& save_path) const;
   void all_path_hashes (std::unordered_set<std::uint32_t>& table) const;
   file_flags_t file_flags (file_index_t index) const;
   bool file_absolute_path (file_index_t index) const;
   file_index_t file_index_at_piece (piece_index_t piece) const;
   file_index_t file_index_at_offset (std::int64_t offset) const;
   file_index_t file_index_for_root (sha256_hash const& root_hash) const;
   piece_index_t piece_index_at_file (file_index_t f) const;
   void sanitize_symlinks ();
   bool v2 () const;

   static constexpr file_flags_t flag_pad_file  = 0_bit;
   static constexpr file_flags_t flag_hidden  = 1_bit;
   static constexpr file_flags_t flag_executable  = 2_bit;
   static constexpr file_flags_t flag_symlink  = 3_bit;
};
```

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Bis_valid%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Bis_valid%28%29%5D%22+could+be+improved)]

## is\_valid()

```cpp
bool is_valid () const;
```

returns true if the piece length has been initialized
on the [file\_storage](reference-Storage.md#file_storage). This is typically taken as a proxy
of whether the [file\_storage](reference-Storage.md#file_storage) as a whole is initialized or
not.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Breserve%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Breserve%28%29%5D%22+could+be+improved)]

## reserve()

```cpp
void reserve (int num_files);
```

allocates space for num\_files in the internal file list. This can
be used to avoid reallocating the internal file list when the number
of files to be added is known up-front.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Badd_file%28%29+add_file_borrow%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Badd_file%28%29+add_file_borrow%28%29%5D%22+could+be+improved)]

## add\_file() add\_file\_borrow()

```cpp
void add_file (std::string const& path, std::int64_t file_size
      , file_flags_t file_flags = {}
      , std::time_t mtime = 0, string_view symlink_path = string_view()
      , char const* root_hash = nullptr);
void add_file_borrow (string_view filename
      , std::string const& path, std::int64_t file_size
      , file_flags_t file_flags = {}, char const* filehash = nullptr
      , std::int64_t mtime = 0, string_view symlink_path = string_view()
      , char const* root_hash = nullptr);
void add_file (error_code& ec, std::string const& path, std::int64_t file_size
      , file_flags_t file_flags = {}
      , std::time_t mtime = 0, string_view symlink_path = string_view()
      , char const* root_hash = nullptr);
void add_file_borrow (error_code& ec, string_view filename
      , std::string const& path, std::int64_t file_size
      , file_flags_t file_flags = {}, char const* filehash = nullptr
      , std::int64_t mtime = 0, string_view symlink_path = string_view()
      , char const* root_hash = nullptr);
```

Adds a file to the file storage. The add\_file\_borrow version
expects that filename is the file name (without a path) of
the file that's being added.
This memory is *borrowed*, i.e. it is the caller's
responsibility to make sure it stays valid throughout the lifetime
of this [file\_storage](reference-Storage.md#file_storage) object or any copy of it. The same thing applies
to filehash, which is an optional pointer to a 20 byte binary
SHA-1 hash of the file.

if filename is empty, the filename from path is used and not
borrowed.

The path argument is the full path (in the torrent file) to
the file to add. Note that this is not supposed to be an absolute
path, but it is expected to include the name of the torrent as the
first path element.

file\_size is the size of the file in bytes.

The file\_flags argument sets attributes on the file. The file
attributes is an extension and may not work in all bittorrent clients.

For possible file attributes, see file\_storage::flags\_t.

The mtime argument is optional and can be set to 0. If non-zero,
it is the posix time of the last modification time of this file.

symlink\_path is the path the file is a symlink to. To make this a
symlink you also need to set the [file\_storage::flag\_symlink](reference-Storage.md#flag_symlink) file flag.

root\_hash is an optional pointer to a 32 byte SHA-256 hash, being
the merkle tree root hash for this file. This is only used for v2
torrents. If the root hash is specified for one file, it has to
be specified for all, otherwise this function will fail.
Note that the buffer root\_hash points to must out-live the
[file\_storage](reference-Storage.md#file_storage) object, it will not be copied. This parameter is only
used when *loading* torrents, that already have their file hashes
computed. When creating torrents, the file hashes will be computed by
the piece hashes.

If more files than one are added, certain restrictions to their paths
apply. In a multi-file file storage (torrent), all files must share
the same root directory.

That is, the first path element of all files must be the same.
This shared path element is also set to the name of the torrent. It
can be changed by calling set\_name.

The overloads that take an error\_code reference will report failures
via that variable, otherwise system\_error is thrown.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Brename_file%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Brename_file%28%29%5D%22+could+be+improved)]

## rename\_file()

```cpp
void rename_file (file_index_t index, std::string const& new_filename);
```

renames the file at index to new\_filename. Keep in mind
that filenames are expected to be UTF-8 encoded.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Bmap_block%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Bmap_block%28%29%5D%22+could+be+improved)]

## map\_block()

```cpp
std::vector<file_slice> map_block (piece_index_t piece, std::int64_t offset
      , std::int64_t size) const;
```

returns a list of [file\_slice](reference-Storage.md#file_slice) objects representing the portions of
files the specified piece index, byte offset and size range overlaps.
this is the inverse mapping of [map\_file()](reference-Torrent_Info.md#map_file()).

Preconditions of this function is that the input range is within the
torrents address space. piece may not be negative and

> piece \* piece\_size + offset + size

may not exceed the total size of the torrent.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Bmap_file%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Bmap_file%28%29%5D%22+could+be+improved)]

## map\_file()

```cpp
peer_request map_file (file_index_t file, std::int64_t offset, int size) const;
```

returns a [peer\_request](reference-Core.md#peer_request) representing the piece index, byte offset
and size the specified file range overlaps. This is the inverse
mapping over [map\_block()](reference-Torrent_Info.md#map_block()). Note that the peer\_request return type
is meant to hold bittorrent block requests, which may not be larger
than 16 kiB. Mapping a range larger than that may return an overflown
integer.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Bnum_files%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Bnum_files%28%29%5D%22+could+be+improved)]

## num\_files()

```cpp
int num_files () const noexcept;
```

returns the number of files in the [file\_storage](reference-Storage.md#file_storage)

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Bend_file%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Bend_file%28%29%5D%22+could+be+improved)]

## end\_file()

```cpp
file_index_t end_file () const noexcept;
```

returns the index of the one-past-end file in the file storage

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Bfile_range%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Bfile_range%28%29%5D%22+could+be+improved)]

## file\_range()

```cpp
index_range<file_index_t> file_range () const noexcept;
```

returns an implementation-defined type that can be used as the
container in a range-for loop. Where the values are the indices of all
files in the [file\_storage](reference-Storage.md#file_storage).

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Btotal_size%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Btotal_size%28%29%5D%22+could+be+improved)]

## total\_size()

```cpp
std::int64_t total_size () const;
```

returns the total number of bytes all the files in this torrent spans

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Bset_num_pieces%28%29+num_pieces%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Bset_num_pieces%28%29+num_pieces%28%29%5D%22+could+be+improved)]

## set\_num\_pieces() num\_pieces()

```cpp
int num_pieces () const;
void set_num_pieces (int n);
```

set and get the number of pieces in the torrent

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Bend_piece%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Bend_piece%28%29%5D%22+could+be+improved)]

## end\_piece()

```cpp
piece_index_t end_piece () const;
```

returns the index of the one-past-end piece in the file storage

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Blast_piece%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Blast_piece%28%29%5D%22+could+be+improved)]

## last\_piece()

```cpp
piece_index_t last_piece () const;
```

returns the index of the last piece in the torrent. The last piece is
special in that it may be smaller than the other pieces (and the other
pieces are all the same size).

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Bpiece_range%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Bpiece_range%28%29%5D%22+could+be+improved)]

## piece\_range()

```cpp
index_range<piece_index_t> piece_range () const noexcept;
```

returns an implementation-defined type that can be used as the
container in a range-for loop. Where the values are the indices of all
pieces in the [file\_storage](reference-Storage.md#file_storage).

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Bpiece_length%28%29+set_piece_length%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Bpiece_length%28%29+set_piece_length%28%29%5D%22+could+be+improved)]

## piece\_length() set\_piece\_length()

```cpp
void set_piece_length (int l);
int piece_length () const;
```

set and get the size of each piece in this torrent. It must be a power of two
and at least 16 kiB.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Bpiece_size%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Bpiece_size%28%29%5D%22+could+be+improved)]

## piece\_size()

```cpp
int piece_size (piece_index_t index) const;
```

returns the piece size of index. This will be the same as [piece\_length()](reference-Torrent_Info.md#piece_length()), except
for the last piece, which may be shorter.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Bpiece_size2%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Bpiece_size2%28%29%5D%22+could+be+improved)]

## piece\_size2()

```cpp
int piece_size2 (piece_index_t index) const;
```

Returns the size of the given piece. If the piece spans multiple files,
only the first file is considered part of the piece. This is used for
v2 torrents, where all files are piece aligned and padded. i.e. The pad
files are not considered part of the piece for this purpose.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Bblocks_in_piece2%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Bblocks_in_piece2%28%29%5D%22+could+be+improved)]

## blocks\_in\_piece2()

```cpp
int blocks_in_piece2 (piece_index_t index) const;
```

returns the number of blocks in the specified piece, for v2 torrents.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Bblocks_per_piece%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Bblocks_per_piece%28%29%5D%22+could+be+improved)]

## blocks\_per\_piece()

```cpp
int blocks_per_piece () const;
```

returns the number of blocks there are in the typical piece. There
may be fewer in the last piece)

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Bname%28%29+set_name%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Bname%28%29+set_name%28%29%5D%22+could+be+improved)]

## name() set\_name()

```cpp
void set_name (std::string const& n);
std::string const& name () const;
```

set and get the name of this torrent. For multi-file torrents, this is also
the name of the root directory all the files are stored in.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Bswap%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Bswap%28%29%5D%22+could+be+improved)]

## swap()

```cpp
void swap (file_storage& ti) noexcept;
```

swap all content of *this* with *ti*.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Bcanonicalize%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Bcanonicalize%28%29%5D%22+could+be+improved)]

## canonicalize()

```cpp
void canonicalize ();
```

arrange files and padding to match the canonical form required
by BEP 52

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Broot_ptr%28%29+symlink%28%29+hash%28%29+root%28%29+file_offset%28%29+file_name%28%29+pad_file_at%28%29+file_path%28%29+file_size%28%29+mtime%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Broot_ptr%28%29+symlink%28%29+hash%28%29+root%28%29+file_offset%28%29+file_name%28%29+pad_file_at%28%29+file_path%28%29+file_size%28%29+mtime%28%29%5D%22+could+be+improved)]

## root\_ptr() symlink() hash() root() file\_offset() file\_name() pad\_file\_at() file\_path() file\_size() mtime()

```cpp
sha256_hash root (file_index_t index) const;
std::int64_t file_size (file_index_t index) const;
char const* root_ptr (file_index_t const index) const;
sha1_hash hash (file_index_t index) const;
string_view file_name (file_index_t index) const;
std::int64_t file_offset (file_index_t index) const;
std::time_t mtime (file_index_t index) const;
bool pad_file_at (file_index_t index) const;
std::string symlink (file_index_t index) const;
std::string file_path (file_index_t index, std::string const& save_path = "") const;
```

These functions are used to query attributes of files at
a given index.

The hash() is a SHA-1 hash of the file, or 0 if none was
provided in the torrent file. This can potentially be used to
join a bittorrent network with other file sharing networks.

root() returns the SHA-256 merkle tree root of the specified file,
in case this is a v2 torrent. Otherwise returns zeros.
root\_ptr() returns a pointer to the SHA-256 merkle tree root hash
for the specified file. The pointer points into storage referred to
when the file was added, it is not owned by this object. Torrents
that are not v2 torrents return nullptr.

The mtime() is the modification time is the posix
time when a file was last modified when the torrent
was created, or 0 if it was not included in the torrent file.

file\_path() returns the full path to a file.

file\_size() returns the size of a file.

pad\_file\_at() returns true if the file at the given
index is a pad-file.

file\_name() returns *just* the name of the file, whereas
file\_path() returns the path (inside the torrent file) with
the filename appended.

file\_offset() returns the byte offset within the torrent file
where this file starts. It can be used to map the file to a piece
index (given the piece size).

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Bfile_num_blocks%28%29+file_num_pieces%28%29+file_piece_range%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Bfile_num_blocks%28%29+file_num_pieces%28%29+file_piece_range%28%29%5D%22+could+be+improved)]

## file\_num\_blocks() file\_num\_pieces() file\_piece\_range()

```cpp
index_range<piece_index_t::diff_type> file_piece_range (file_index_t) const;
int file_num_pieces (file_index_t index) const;
int file_num_blocks (file_index_t index) const;
```

Returns the number of pieces or blocks the file at index spans,
under the assumption that the file is aligned to the start of a piece.
This is only meaningful for v2 torrents, where files are guaranteed
such alignment.
These numbers are used to size and navigate the merkle hash tree for
each file.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Bfile_first_block_node%28%29+file_first_piece_node%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Bfile_first_block_node%28%29+file_first_piece_node%28%29%5D%22+could+be+improved)]

## file\_first\_block\_node() file\_first\_piece\_node()

```cpp
int file_first_piece_node (file_index_t index) const;
int file_first_block_node (file_index_t index) const;
```

index of first piece node in the merkle tree

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Bfile_path_hash%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Bfile_path_hash%28%29%5D%22+could+be+improved)]

## file\_path\_hash()

```cpp
std::uint32_t file_path_hash (file_index_t index, std::string const& save_path) const;
```

returns the crc32 hash of file\_path(index)

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Ball_path_hashes%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Ball_path_hashes%28%29%5D%22+could+be+improved)]

## all\_path\_hashes()

```cpp
void all_path_hashes (std::unordered_set<std::uint32_t>& table) const;
```

this will add the CRC32 hash of all directory entries to the table. No
filename will be included, just directories. Every depth of directories
are added separately to allow test for collisions with files at all
levels. i.e. if one path in the torrent is foo/bar/baz, the CRC32
hashes for foo, foo/bar and foo/bar/baz will be added to
the set.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Bfile_flags%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Bfile_flags%28%29%5D%22+could+be+improved)]

## file\_flags()

```cpp
file_flags_t file_flags (file_index_t index) const;
```

returns a bitmask of flags from file\_flags\_t that apply
to file at index.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Bfile_absolute_path%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Bfile_absolute_path%28%29%5D%22+could+be+improved)]

## file\_absolute\_path()

```cpp
bool file_absolute_path (file_index_t index) const;
```

returns true if the file at the specified index has been renamed to
have an absolute path, i.e. is not anchored in the save path of the
torrent.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Bfile_index_at_offset%28%29+file_index_at_piece%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Bfile_index_at_offset%28%29+file_index_at_piece%28%29%5D%22+could+be+improved)]

## file\_index\_at\_offset() file\_index\_at\_piece()

```cpp
file_index_t file_index_at_piece (piece_index_t piece) const;
file_index_t file_index_at_offset (std::int64_t offset) const;
```

returns the index of the file at the given offset in the torrent

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Bfile_index_for_root%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Bfile_index_for_root%28%29%5D%22+could+be+improved)]

## file\_index\_for\_root()

```cpp
file_index_t file_index_for_root (sha256_hash const& root_hash) const;
```

finds the file with the given root hash and returns its index
if there is no file with the root hash, file\_index\_t{-1} is returned

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Bpiece_index_at_file%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Bpiece_index_at_file%28%29%5D%22+could+be+improved)]

## piece\_index\_at\_file()

```cpp
piece_index_t piece_index_at_file (file_index_t f) const;
```

returns the piece index the given file starts at

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Bsanitize_symlinks%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Bsanitize_symlinks%28%29%5D%22+could+be+improved)]

## sanitize\_symlinks()

```cpp
void sanitize_symlinks ();
```

validate any symlinks, to ensure they all point to
other files or directories inside this storage. Any invalid symlinks
are updated to point to themselves.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Bv2%28%29%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Bv2%28%29%5D%22+could+be+improved)]

## v2()

```cpp
bool v2 () const;
```

returns true if this torrent contains v2 metadata.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Bflag_pad_file%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Bflag_pad_file%5D%22+could+be+improved)]

flag\_pad\_file
:   the file is a pad file. It's required to contain zeros
    at it will not be saved to disk. Its purpose is to make
    the following file start on a piece boundary.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Bflag_hidden%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Bflag_hidden%5D%22+could+be+improved)]

flag\_hidden
:   this file has the hidden attribute set. This is primarily
    a windows attribute

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Bflag_executable%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Bflag_executable%5D%22+could+be+improved)]

flag\_executable
:   this file has the executable attribute set.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:file_storage%3A%3A%5Bflag_symlink%5D&labels=documentation&body=Documentation+under+heading+%22file_storage%3A%3A%5Bflag_symlink%5D%22+could+be+improved)]

flag\_symlink
:   this file is a symbolic link. It should have a link
    target string associated with it.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:mmap_disk_io_constructor%28%29&labels=documentation&body=Documentation+under+heading+%22mmap_disk_io_constructor%28%29%22+could+be+improved)]

# mmap\_disk\_io\_constructor()

Declared in "[libtorrent/mmap\_disk\_io.hpp](include/libtorrent/mmap_disk_io.hpp)"

```cpp
std::unique_ptr<disk_interface> mmap_disk_io_constructor (
   io_context& ios, settings_interface const&, counters& cnt);
```

constructs a memory mapped file disk I/O object.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:default_disk_io_constructor%28%29&labels=documentation&body=Documentation+under+heading+%22default_disk_io_constructor%28%29%22+could+be+improved)]

# default\_disk\_io\_constructor()

Declared in "[libtorrent/session.hpp](include/libtorrent/session.hpp)"

```cpp
std::unique_ptr<disk_interface> default_disk_io_constructor (
   io_context& ios, settings_interface const&, counters& cnt);
```

the constructor function for the default storage. On systems that support
memory mapped files (and a 64 bit address space) the memory mapped storage
will be constructed, otherwise the portable posix storage.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:disabled_disk_io_constructor%28%29&labels=documentation&body=Documentation+under+heading+%22disabled_disk_io_constructor%28%29%22+could+be+improved)]

# disabled\_disk\_io\_constructor()

Declared in "[libtorrent/disabled\_disk\_io.hpp](include/libtorrent/disabled_disk_io.hpp)"

```cpp
std::unique_ptr<disk_interface> disabled_disk_io_constructor (
   io_context& ios, settings_interface const&, counters& cnt);
```

creates a disk io object that discards all data written to it, and only
returns zero-buffers when read from. May be useful for testing and
benchmarking.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:posix_disk_io_constructor%28%29&labels=documentation&body=Documentation+under+heading+%22posix_disk_io_constructor%28%29%22+could+be+improved)]

# posix\_disk\_io\_constructor()

Declared in "[libtorrent/posix\_disk\_io.hpp](include/libtorrent/posix_disk_io.hpp)"

```cpp
std::unique_ptr<disk_interface> posix_disk_io_constructor (
   io_context& ios, settings_interface const&, counters& cnt);
```

this is a simple posix disk I/O back-end, used for systems that don't
have a 64 bit virtual address space or don't support memory mapped files.
It's implemented using portable C file functions and is single-threaded.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:enum+storage_mode_t&labels=documentation&body=Documentation+under+heading+%22enum+storage_mode_t%22+could+be+improved)]

# enum storage\_mode\_t

Declared in "[libtorrent/storage\_defs.hpp](include/libtorrent/storage_defs.hpp)"

| name | value | description |
| --- | --- | --- |
| storage\_mode\_allocate | 0 | All pieces will be written to their final position, all files will be allocated in full when the torrent is first started. This mode minimizes fragmentation but could be a costly operation. |
| storage\_mode\_sparse | 1 | All pieces will be written to the place where they belong and sparse files will be used. This is the recommended, and default mode. |

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:enum+status_t&labels=documentation&body=Documentation+under+heading+%22enum+status_t%22+could+be+improved)]

# enum status\_t

Declared in "[libtorrent/storage\_defs.hpp](include/libtorrent/storage_defs.hpp)"

| name | value | description |
| --- | --- | --- |
| no\_error | 0 |  |
| fatal\_disk\_error | 1 |  |
| need\_full\_check | 2 |  |
| file\_exist | 3 |  |
| oversized\_file | 16 | this is not an enum value, but a flag that can be set in the return from async\_check\_files, in case an existing file was found larger than specified in the torrent. i.e. it has garbage at the end the [status\_t](reference-Storage.md#status_t) field is used for this to preserve ABI. |

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:enum+move_flags_t&labels=documentation&body=Documentation+under+heading+%22enum+move_flags_t%22+could+be+improved)]

# enum move\_flags\_t

Declared in "[libtorrent/storage\_defs.hpp](include/libtorrent/storage_defs.hpp)"

| name | value | description |
| --- | --- | --- |
| always\_replace\_files | 0 | replace any files in the destination when copying or moving the storage |
| fail\_if\_exist | 1 | if any files that we want to copy exist in the destination exist, fail the whole operation and don't perform any copy or move. There is an inherent race condition in this mode. The files are checked for existence before the operation starts. In between the check and performing the copy, the destination files may be created, in which case they are replaced. |
| dont\_replace | 2 | if any file exist in the target, take those files instead of the ones we may have in the source. |
| reset\_save\_path | 3 | don't move any source files, just forget about them and begin checking files at new save path |
| reset\_save\_path\_unchecked | 4 | don't move any source files, just change save path and continue working without any checks |
