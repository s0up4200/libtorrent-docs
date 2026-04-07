---
title: "Torrent Handle"
source: "https://libtorrent.org/reference-Torrent_Handle.html"
---

# block\_info

Declared in "[libtorrent/torrent\_handle.hpp](include/libtorrent/torrent_handle.hpp)"

holds the state of a block in a piece. Who we requested
it from and how far along we are at downloading it.

```cpp
struct block_info
{
   tcp::endpoint peer () const;
   void set_peer (tcp::endpoint const& ep);

   enum block_state_t
   {
      none,
      requested,
      writing,
      finished,
   };

   unsigned bytes_progress:15;
   unsigned block_size:15;
   unsigned state:2;
   unsigned num_peers:14;
};
```

## set\_peer() peer()

```cpp
tcp::endpoint peer () const;
void set_peer (tcp::endpoint const& ep);
```

The peer is the ip address of the peer this block was downloaded from.

## enum block\_state\_t

Declared in "[libtorrent/torrent\_handle.hpp](include/libtorrent/torrent_handle.hpp)"

| name | value | description |
| --- | --- | --- |
| none | 0 | This block has not been downloaded or requested form any peer. |
| requested | 1 | The block has been requested, but not completely downloaded yet. |
| writing | 2 | The block has been downloaded and is currently queued for being written to disk. |
| finished | 3 | The block has been written to disk. |

bytes\_progress
:   the number of bytes that have been received for this block

block\_size
:   the total number of bytes in this block.

state
:   the state this block is in (see [block\_state\_t](reference-Torrent_Handle.md#block_state_t))

num\_peers
:   the number of peers that is currently requesting this block. Typically
    this is 0 or 1, but at the end of the torrent blocks may be requested
    by more peers in parallel to speed things up.

# partial\_piece\_info

Declared in "[libtorrent/torrent\_handle.hpp](include/libtorrent/torrent_handle.hpp)"

This class holds information about pieces that have outstanding requests
or outstanding writes

```cpp
struct partial_piece_info
{
   piece_index_t piece_index;
   int blocks_in_piece;
   int finished;
   int writing;
   int requested;
   block_info const* blocks;
};
```

piece\_index
:   the index of the piece in question. blocks\_in\_piece is the number
    of blocks in this particular piece. This number will be the same for
    most pieces, but
    the last piece may have fewer blocks than the standard pieces.

blocks\_in\_piece
:   the number of blocks in this piece

finished
:   the number of blocks that are in the finished state

writing
:   the number of blocks that are in the writing state

requested
:   the number of blocks that are in the requested state

blocks
:   this is an array of blocks\_in\_piece number of
    items. One for each block in the piece.

    Warning

    This is a pointer that points to an array
    that's owned by the [session](reference-Session.md#session) object. The next time
    [get\_download\_queue()](reference-Torrent_Handle.md#get_download_queue()) is called, it will be invalidated.
    In the case of [piece\_info\_alert](reference-Alerts.md#piece_info_alert), these pointers point into the [alert](reference-Alerts.md#alert)
    object itself, and will be invalidated when the [alert](reference-Alerts.md#alert) destruct.

# torrent\_handle

Declared in "[libtorrent/torrent\_handle.hpp](include/libtorrent/torrent_handle.hpp)"

You will usually have to store your torrent handles somewhere, since it's
the object through which you retrieve information about the torrent and
aborts the torrent.

Warning

Any member function that returns a value or fills in a value has to be
made synchronously. This means it has to wait for the main thread to
complete the query before it can return. This might potentially be
expensive if done from within a GUI thread that needs to stay
responsive. Try to avoid querying for information you don't need, and
try to do it in as few calls as possible. You can get most of the
interesting information about a torrent from the
[torrent\_handle::status()](reference-Torrent_Handle.md#status()) call.

The default constructor will initialize the handle to an invalid state.
Which means you cannot perform any operation on it, unless you first
assign it a valid handle. If you try to perform any operation on an
uninitialized handle, it will throw invalid\_handle.

Warning

All operations on a [torrent\_handle](reference-Torrent_Handle.md#torrent_handle) may throw system\_error
exception, in case the handle is no longer referring to a torrent.
There is one exception [is\_valid()](reference-Torrent_Info.md#is_valid()) will never throw. Since the torrents
are processed by a background thread, there is no guarantee that a
handle will remain valid between two calls.

```cpp
struct torrent_handle
{
   friend std::size_t hash_value (torrent_handle const& th);
   torrent_handle () noexcept = default;
   void add_piece (piece_index_t piece, char const* data, add_piece_flags_t flags = {}) const;
   void add_piece (piece_index_t piece, std::vector<char> data, add_piece_flags_t flags = {}) const;
   void read_piece (piece_index_t piece) const;
   bool have_piece (piece_index_t piece) const;
   void get_peer_info (std::vector<peer_info>& v) const;
   void post_peer_info () const;
   void post_status (status_flags_t flags = status_flags_t::all()) const;
   torrent_status status (status_flags_t flags = status_flags_t::all()) const;
   void post_download_queue () const;
   void get_download_queue (std::vector<partial_piece_info>& queue) const;
   std::vector<partial_piece_info> get_download_queue () const;
   void set_piece_deadline (piece_index_t index, int deadline, deadline_flags_t flags = {}) const;
   void clear_piece_deadlines () const;
   void reset_piece_deadline (piece_index_t index) const;
   std::vector<std::int64_t> file_progress (file_progress_flags_t flags = {}) const;
   void post_file_progress (file_progress_flags_t flags) const;
   void file_progress (std::vector<std::int64_t>& progress, file_progress_flags_t flags = {}) const;
   std::vector<open_file_state> file_status () const;
   void clear_error () const;
   std::vector<announce_entry> trackers () const;
   void add_tracker (announce_entry const&) const;
   void replace_trackers (std::vector<announce_entry> const&) const;
   void post_trackers () const;
   void add_url_seed (std::string const& url) const;
   void remove_url_seed (std::string const& url) const;
   std::set<std::string> url_seeds () const;
   void remove_http_seed (std::string const& url) const;
   void add_http_seed (std::string const& url) const;
   std::set<std::string> http_seeds () const;
   void add_extension (
      std::function<std::shared_ptr<torrent_plugin>(torrent_handle const&, client_data_t)> const& ext
      , client_data_t userdata = client_data_t{});
   bool set_metadata (span<char const> metadata) const;
   bool is_valid () const;
   void resume () const;
   void pause (pause_flags_t flags = {}) const;
   void set_flags (torrent_flags_t flags) const;
   void unset_flags (torrent_flags_t flags) const;
   void set_flags (torrent_flags_t flags, torrent_flags_t mask) const;
   torrent_flags_t flags () const;
   void flush_cache () const;
   void force_recheck () const;
   void save_resume_data (resume_data_flags_t flags = {}) const;
   bool need_save_resume_data () const;
   bool need_save_resume_data (resume_data_flags_t flags) const;
   void queue_position_up () const;
   void queue_position_top () const;
   queue_position_t queue_position () const;
   void queue_position_down () const;
   void queue_position_bottom () const;
   void queue_position_set (queue_position_t p) const;
   void set_ssl_certificate_buffer (std::string const& certificate
      , std::string const& private_key
      , std::string const& dh_params);
   void set_ssl_certificate (std::string const& certificate
      , std::string const& private_key
      , std::string const& dh_params
      , std::string const& passphrase = "");
   std::shared_ptr<const torrent_info> torrent_file () const;
   std::shared_ptr<torrent_info> torrent_file_with_hashes () const;
   std::vector<std::vector<sha256_hash>> piece_layers () const;
   void piece_availability (std::vector<int>& avail) const;
   void post_piece_availability () const;
   void prioritize_pieces (std::vector<std::pair<piece_index_t, download_priority_t>> const& pieces) const;
   std::vector<download_priority_t> get_piece_priorities () const;
   void piece_priority (piece_index_t index, download_priority_t priority) const;
   download_priority_t piece_priority (piece_index_t index) const;
   void prioritize_pieces (std::vector<download_priority_t> const& pieces) const;
   void prioritize_files (std::vector<download_priority_t> const& files) const;
   void file_priority (file_index_t index, download_priority_t priority) const;
   std::vector<download_priority_t> get_file_priorities () const;
   download_priority_t file_priority (file_index_t index) const;
   void force_reannounce (int seconds = 0, int idx = -1, reannounce_flags_t = {}) const;
   void force_dht_announce () const;
   void force_lsd_announce () const;
   void scrape_tracker (int idx = -1) const;
   int download_limit () const;
   void set_download_limit (int limit) const;
   void set_upload_limit (int limit) const;
   int upload_limit () const;
   void connect_peer (tcp::endpoint const& adr, peer_source_flags_t source = {}
      , pex_flags_t flags = pex_encryption | pex_utp | pex_holepunch) const;
   void clear_peers ();
   int max_uploads () const;
   void set_max_uploads (int max_uploads) const;
   int max_connections () const;
   void set_max_connections (int max_connections) const;
   void move_storage (std::string const& save_path
      , move_flags_t flags = move_flags_t::always_replace_files
      ) const;
   void rename_file (file_index_t index, std::string const& new_name) const;
   sha1_hash info_hash () const;
   info_hash_t info_hashes () const;
   bool operator!= (const torrent_handle& h) const;
   bool operator< (const torrent_handle& h) const;
   bool operator== (const torrent_handle& h) const;
   std::uint32_t id () const;
   std::shared_ptr<torrent> native_handle () const;
   client_data_t userdata () const;
   bool in_session () const;

   static constexpr add_piece_flags_t overwrite_existing  = 0_bit;
   static constexpr status_flags_t query_distributed_copies  = 0_bit;
   static constexpr status_flags_t query_accurate_download_counters  = 1_bit;
   static constexpr status_flags_t query_last_seen_complete  = 2_bit;
   static constexpr status_flags_t query_pieces  = 3_bit;
   static constexpr status_flags_t query_verified_pieces  = 4_bit;
   static constexpr status_flags_t query_torrent_file  = 5_bit;
   static constexpr status_flags_t query_name  = 6_bit;
   static constexpr status_flags_t query_save_path  = 7_bit;
   static constexpr deadline_flags_t alert_when_available  = 0_bit;
   static constexpr file_progress_flags_t piece_granularity  = 0_bit;
   static constexpr pause_flags_t graceful_pause  = 0_bit;
   static constexpr resume_data_flags_t flush_disk_cache  = 0_bit;
   static constexpr resume_data_flags_t save_info_dict  = 1_bit;
   static constexpr resume_data_flags_t only_if_modified  = 2_bit;
   static constexpr resume_data_flags_t if_counters_changed  = 3_bit;
   static constexpr resume_data_flags_t if_download_progress  = 4_bit;
   static constexpr resume_data_flags_t if_config_changed  = 5_bit;
   static constexpr resume_data_flags_t if_state_changed  = 6_bit;
   static constexpr resume_data_flags_t if_metadata_changed  = 7_bit;
   static constexpr reannounce_flags_t ignore_min_interval  = 0_bit;
};
```

## torrent\_handle()

```cpp
torrent_handle () noexcept = default;
```

constructs a torrent handle that does not refer to a torrent.
i.e. [is\_valid()](reference-Torrent_Info.md#is_valid()) will return false.

## add\_piece()

```cpp
void add_piece (piece_index_t piece, char const* data, add_piece_flags_t flags = {}) const;
void add_piece (piece_index_t piece, std::vector<char> data, add_piece_flags_t flags = {}) const;
```

This function will write data to the storage as piece piece,
as if it had been downloaded from a peer.

By default, data that's already been downloaded is not overwritten by
this buffer. If you trust this data to be correct (and pass the piece
hash check) you may pass the overwrite\_existing flag. This will
instruct libtorrent to overwrite any data that may already have been
downloaded with this data.

Since the data is written asynchronously, you may know that is passed
or failed the hash check by waiting for [piece\_finished\_alert](reference-Alerts.md#piece_finished_alert) or
[hash\_failed\_alert](reference-Alerts.md#hash_failed_alert).

Adding pieces while the torrent is being checked (i.e. in
[torrent\_status::checking\_files](reference-Torrent_Status.md#checking_files) state) is not supported.

The overload taking a raw pointer to the data is a blocking call. It
won't return until the libtorrent thread has copied the data into its
disk write buffer. data is expected to point to a buffer of as
many bytes as the size of the specified piece. See
[file\_storage::piece\_size()](reference-Storage.md#piece_size()).

The data in the buffer is copied and passed on to the disk IO thread
to be written at a later point.

The overload taking a std::vector<char> is not blocking, it will
send the buffer to the main thread and return immediately.

## read\_piece()

```cpp
void read_piece (piece_index_t piece) const;
```

This function starts an asynchronous read operation of the specified
piece from this torrent. You must have completed the download of the
specified piece before calling this function.

When the read operation is completed, it is passed back through an
[alert](reference-Alerts.md#alert), [read\_piece\_alert](reference-Alerts.md#read_piece_alert). Since this [alert](reference-Alerts.md#alert) is a response to an explicit
call, it will always be posted, regardless of the [alert](reference-Alerts.md#alert) mask.

Note that if you read multiple pieces, the read operations are not
guaranteed to finish in the same order as you initiated them.

## have\_piece()

```cpp
bool have_piece (piece_index_t piece) const;
```

Returns true if this piece has been completely downloaded and written
to disk, and false otherwise.

## get\_peer\_info() post\_peer\_info()

```cpp
void get_peer_info (std::vector<peer_info>& v) const;
void post_peer_info () const;
```

Query information about connected peers for this torrent. If the
[torrent\_handle](reference-Torrent_Handle.md#torrent_handle) is invalid, it will throw a system\_error exception.

post\_peer\_info() is asynchronous and will trigger the posting of
a [peer\_info\_alert](reference-Alerts.md#peer_info_alert). The [alert](reference-Alerts.md#alert) contain a list of [peer\_info](reference-Core.md#peer_info) objects, one
for each connected peer.

get\_peer\_info() is synchronous and takes a reference to a vector
that will be cleared and filled with one [entry](reference-Bencoding.md#entry) for each peer
connected to this torrent, given the handle is valid. Each [entry](reference-Bencoding.md#entry) in
the vector contains information about that particular peer. See
[peer\_info](reference-Core.md#peer_info).

## status() post\_status()

```cpp
void post_status (status_flags_t flags = status_flags_t::all()) const;
torrent_status status (status_flags_t flags = status_flags_t::all()) const;
```

status() will return a structure with information about the status
of this torrent. If the [torrent\_handle](reference-Torrent_Handle.md#torrent_handle) is invalid, it will throw
system\_error exception. See [torrent\_status](reference-Torrent_Status.md#torrent_status). The flags
argument filters what information is returned in the [torrent\_status](reference-Torrent_Status.md#torrent_status).
Some information in there is relatively expensive to calculate, and if
you're not interested in it (and see performance issues), you can
filter them out.

The status() function will block until the internal libtorrent
thread responds with the [torrent\_status](reference-Torrent_Status.md#torrent_status) object. To avoid blocking,
instead call post\_status(). It will trigger posting of a
[state\_update\_alert](reference-Alerts.md#state_update_alert) with a single [torrent\_status](reference-Torrent_Status.md#torrent_status) object for this
torrent.

In order to get regular updates for torrents whose status changes,
consider calling session::post\_torrent\_updates()`` instead.

By default everything is included. The flags you can use to decide
what to *include* are defined in this class.

## post\_download\_queue() get\_download\_queue()

```cpp
void post_download_queue () const;
void get_download_queue (std::vector<partial_piece_info>& queue) const;
std::vector<partial_piece_info> get_download_queue () const;
```

post\_download\_queue() triggers a download\_queue\_alert to be
posted.
get\_download\_queue() is a synchronous call and returns a vector
with information about pieces that are partially downloaded or not
downloaded but partially requested. See [partial\_piece\_info](reference-Torrent_Handle.md#partial_piece_info) for the
fields in the returned vector.

## reset\_piece\_deadline() set\_piece\_deadline() clear\_piece\_deadlines()

```cpp
void set_piece_deadline (piece_index_t index, int deadline, deadline_flags_t flags = {}) const;
void clear_piece_deadlines () const;
void reset_piece_deadline (piece_index_t index) const;
```

This function sets or resets the deadline associated with a specific
piece index (index). libtorrent will attempt to download this
entire piece before the deadline expires. This is not necessarily
possible, but pieces with a more recent deadline will always be
prioritized over pieces with a deadline further ahead in time. The
deadline (and flags) of a piece can be changed by calling this
function again.

If the piece is already downloaded when this call is made, nothing
happens, unless the alert\_when\_available flag is set, in which case it
will have the same effect as calling [read\_piece()](reference-Torrent_Handle.md#read_piece()) for index.

deadline is the number of milliseconds until this piece should be
completed.

reset\_piece\_deadline removes the deadline from the piece. If it
hasn't already been downloaded, it will no longer be considered a
priority.

clear\_piece\_deadlines() removes deadlines on all pieces in
the torrent. As if [reset\_piece\_deadline()](reference-Torrent_Handle.md#reset_piece_deadline()) was called on all pieces.

## file\_progress() post\_file\_progress()

```cpp
std::vector<std::int64_t> file_progress (file_progress_flags_t flags = {}) const;
void post_file_progress (file_progress_flags_t flags) const;
void file_progress (std::vector<std::int64_t>& progress, file_progress_flags_t flags = {}) const;
```

This function fills in the supplied vector, or returns a vector, with
the number of bytes downloaded of each file in this torrent. The
progress values are ordered the same as the files in the
[torrent\_info](reference-Torrent_Info.md#torrent_info).

This operation is not very cheap. Its complexity is *O(n + mj)*.
Where *n* is the number of files, *m* is the number of currently
downloading pieces and *j* is the number of blocks in a piece.

The flags parameter can be used to specify the granularity of the
file progress. If left at the default value of 0, the progress will be
as accurate as possible, but also more expensive to calculate. If
torrent\_handle::piece\_granularity is specified, the progress will
be specified in piece granularity. i.e. only pieces that have been
fully downloaded and passed the hash check count. When specifying
piece granularity, the operation is a lot cheaper, since libtorrent
already keeps track of this internally and no calculation is required.

## file\_status()

```cpp
std::vector<open_file_state> file_status () const;
```

This function returns a vector with status about files
that are open for this torrent. Any file that is not open
will not be reported in the vector, i.e. it's possible that
the vector is empty when returning, if none of the files in the
torrent are currently open.

See [open\_file\_state](reference-Custom_Storage.md#open_file_state)

## clear\_error()

```cpp
void clear_error () const;
```

If the torrent is in an error state (i.e. torrent\_status::error is
non-empty), this will clear the error and start the torrent again.

## add\_tracker() post\_trackers() replace\_trackers() trackers()

```cpp
std::vector<announce_entry> trackers () const;
void add_tracker (announce_entry const&) const;
void replace_trackers (std::vector<announce_entry> const&) const;
void post_trackers () const;
```

trackers() returns the list of trackers for this torrent. The
announce [entry](reference-Bencoding.md#entry) contains both a string url which specify the
announce url for the tracker as well as an [int](reference-Core.md#int) tier, which is
specifies the order in which this tracker is tried. If you want
libtorrent to use another list of trackers for this torrent, you can
use replace\_trackers() which takes a list of the same form as the
one returned from trackers() and will replace it. If you want an
immediate effect, you have to call [force\_reannounce()](reference-Torrent_Handle.md#force_reannounce()). See
[announce\_entry](reference-Trackers.md#announce_entry).

post\_trackers() is the asynchronous version of trackers(). It
will trigger a [tracker\_list\_alert](reference-Alerts.md#tracker_list_alert) to be posted.

add\_tracker() will look if the specified tracker is already in the
set. If it is, it doesn't do anything. If it's not in the current set
of trackers, it will insert it in the tier specified in the
[announce\_entry](reference-Trackers.md#announce_entry).

The updated set of trackers will be saved in the resume data, and when
a torrent is started with resume data, the trackers from the resume
data will replace the original ones.

## url\_seeds() add\_url\_seed() remove\_url\_seed()

```cpp
void add_url_seed (std::string const& url) const;
void remove_url_seed (std::string const& url) const;
std::set<std::string> url_seeds () const;
```

add\_url\_seed() adds another url to the torrent's list of url
seeds. If the given url already exists in that list, the call has no
effect. The torrent will connect to the server and try to download
pieces from it, unless it's paused, queued, checking or seeding.
remove\_url\_seed() removes the given url if it exists already.
url\_seeds() return a set of the url seeds currently in this
torrent. Note that URLs that fails may be removed automatically from
the list.

See [http seeding](manual-ref.md#http-seeding) for more information.

## add\_http\_seed() http\_seeds() remove\_http\_seed()

```cpp
void remove_http_seed (std::string const& url) const;
void add_http_seed (std::string const& url) const;
std::set<std::string> http_seeds () const;
```

These functions are identical as the \*\_url\_seed() variants, but
they operate on [BEP 17](https://www.bittorrent.org/beps/bep_0017.html) web seeds instead of [BEP 19](https://www.bittorrent.org/beps/bep_0019.html).

See [http seeding](manual-ref.md#http-seeding) for more information.

## add\_extension()

```cpp
void add_extension (
      std::function<std::shared_ptr<torrent_plugin>(torrent_handle const&, client_data_t)> const& ext
      , client_data_t userdata = client_data_t{});
```

add the specified extension to this torrent. The ext argument is
a function that will be called from within libtorrent's context
passing in the internal torrent object and the specified userdata
pointer. The function is expected to return a shared pointer to
a [torrent\_plugin](reference-Plugins.md#torrent_plugin) instance.

## set\_metadata()

```cpp
bool set_metadata (span<char const> metadata) const;
```

set\_metadata expects the *info* section of metadata. i.e. The
buffer passed in will be hashed and verified against the info-hash. If
it fails, a metadata\_failed\_alert will be generated. If it passes,
a metadata\_received\_alert is generated. The function returns true
if the metadata is successfully set on the torrent, and false
otherwise. If the torrent already has metadata, this function will not
affect the torrent, and false will be returned.

## is\_valid()

```cpp
bool is_valid () const;
```

Returns true if this handle refers to a valid torrent and false if it
hasn't been initialized or if the torrent it refers to has been
removed from the [session](reference-Session.md#session) AND destructed.

To tell if the [torrent\_handle](reference-Torrent_Handle.md#torrent_handle) is in the [session](reference-Session.md#session), use
[torrent\_handle::in\_session()](reference-Torrent_Handle.md#in_session()). This will return true before
[session\_handle::remove\_torrent()](reference-Session.md#remove_torrent()) is called, and false
afterward.

Clients should only use [is\_valid()](reference-Torrent_Info.md#is_valid()) to determine if the result of
session::find\_torrent() was successful.

Unlike other member functions which return a value, [is\_valid()](reference-Torrent_Info.md#is_valid())
completes immediately, without blocking on a result from the
network thread. Also unlike other functions, it never throws
the system\_error exception.

## resume() pause()

```cpp
void resume () const;
void pause (pause_flags_t flags = {}) const;
```

pause(), and resume() will disconnect all peers and reconnect
all peers respectively. When a torrent is paused, it will however
remember all share ratios to all peers and remember all potential (not
connected) peers. Torrents may be paused automatically if there is a
file error (e.g. disk full) or something similar. See
[file\_error\_alert](reference-Alerts.md#file_error_alert).

For possible values of the flags parameter, see pause\_flags\_t.

To know if a torrent is paused or not, call
torrent\_handle::flags() and check for the
torrent\_status::paused flag.

Note

Torrents that are auto-managed may be automatically resumed again. It
does not make sense to pause an auto-managed torrent without making it
not auto-managed first. Torrents are auto-managed by default when added
to the [session](reference-Session.md#session). For more information, see [queuing](manual-ref.md#queuing).

## unset\_flags() set\_flags() flags()

```cpp
void set_flags (torrent_flags_t flags) const;
void unset_flags (torrent_flags_t flags) const;
void set_flags (torrent_flags_t flags, torrent_flags_t mask) const;
torrent_flags_t flags () const;
```

sets and gets the torrent state flags. See [torrent\_flags\_t](reference-Core.md#torrent_flags_t).
The set\_flags overload that take a mask will affect all
flags part of the mask, and set their values to what the
flags argument is set to. This allows clearing and
setting flags in a single function call.
The set\_flags overload that just takes flags, sets all
the specified flags and leave any other flags unchanged.
unset\_flags clears the specified flags, while leaving
any other flags unchanged.

The seed\_mode flag is special, it can only be cleared once the
torrent has been added, and it can only be set as part of the
[add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params) flags, when adding the torrent.

## flush\_cache()

```cpp
void flush_cache () const;
```

Instructs libtorrent to flush all the disk caches for this torrent and
close all file handles. This is done asynchronously and you will be
notified that it's complete through [cache\_flushed\_alert](reference-Alerts.md#cache_flushed_alert).

Note that by the time you get the [alert](reference-Alerts.md#alert), libtorrent may have cached
more data for the torrent, but you are guaranteed that whatever cached
data libtorrent had by the time you called
torrent\_handle::flush\_cache() has been written to disk.

## force\_recheck()

```cpp
void force_recheck () const;
```

force\_recheck puts the torrent back in a state where it assumes to
have no resume data. All peers will be disconnected and the torrent
will stop announcing to the tracker. The torrent will be added to the
checking queue, and will be checked (all the files will be read and
compared to the piece hashes). Once the check is complete, the torrent
will start connecting to peers again, as normal.
The torrent will be placed last in queue, i.e. its queue position
will be the highest of all torrents in the [session](reference-Session.md#session).

## save\_resume\_data()

```cpp
void save_resume_data (resume_data_flags_t flags = {}) const;
```

save\_resume\_data() asks libtorrent to generate fast-resume data for
this torrent. The fast resume data (stored in an [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params)
object) can be used to resume a torrent in the next [session](reference-Session.md#session) without
having to check all files for which pieces have been downloaded. It
can also be used to save a .torrent file for a [torrent\_handle](reference-Torrent_Handle.md#torrent_handle).

This operation is asynchronous, save\_resume\_data will return
immediately. The resume data is delivered when it's done through a
[save\_resume\_data\_alert](reference-Alerts.md#save_resume_data_alert).

The operation will fail, and post a [save\_resume\_data\_failed\_alert](reference-Alerts.md#save_resume_data_failed_alert)
instead, in the following cases:

> 1. The torrent is in the process of being removed.
> 2. No torrent state has changed since the last saving of resume
>    data, and the only\_if\_modified flag is set.
>    metadata (see libtorrent's [metadata from peers](manual-ref.md#metadata-from-peers) extension)

Note that some [counters](reference-Stats.md#counters) may be outdated by the time you receive the fast resume data

When saving resume data because of shutting down, make sure not to
[remove\_torrent()](reference-Custom_Storage.md#remove_torrent()) before you receive the [save\_resume\_data\_alert](reference-Alerts.md#save_resume_data_alert).
There's no need to pause the [session](reference-Session.md#session) or torrent when saving resume
data.

The paused state of a torrent is saved in the resume data, so pausing
all torrents before saving resume data will all torrents be restored
in a paused state.

Note

It is typically a good idea to save resume data whenever a torrent
is completed or paused. If you save resume data for torrents when they are
paused, you can accelerate the shutdown process by not saving resume
data again for those torrents. Completed torrents should have their
resume data saved when they complete and on exit, since their
statistics might be updated.

Example code to pause and save resume data for all torrents and wait
for the alerts:

```cpp
extern int outstanding_resume_data; // global counter of outstanding resume data
std::vector<torrent_handle> handles = ses.get_torrents();
for (torrent_handle const& h : handles) try
{
        h.save_resume_data(torrent_handle::only_if_modified);
        ++outstanding_resume_data;
}
catch (lt::system_error const& e)
{
        // the handle was invalid, ignore this one and move to the next
}

while (outstanding_resume_data > 0)
{
        alert const* a = ses.wait_for_alert(seconds(30));

        // if we don't get an alert within 30 seconds, abort
        if (a == nullptr) break;

        std::vector<alert*> alerts;
        ses.pop_alerts(&alerts);

        for (alert* i : alerts)
        {
                if (alert_cast<save_resume_data_failed_alert>(i))
                {
                        process_alert(i);
                        --outstanding_resume_data;
                        continue;
                }

                save_resume_data_alert const* rd = alert_cast<save_resume_data_alert>(i);
                if (rd == nullptr)
                {
                        process_alert(i);
                        continue;
                }

                std::ofstream out((rd->params.save_path
                        + "/" + rd->params.name + ".fastresume").c_str()
                        , std::ios_base::binary);
                std::vector<char> buf = write_resume_data_buf(rd->params);
                out.write(buf.data(), buf.size());
                --outstanding_resume_data;
        }
}
```

Note

Note how outstanding\_resume\_data is a global counter in this
example. This is deliberate, otherwise there is a race condition for
torrents that was just asked to save their resume data, they posted
the [alert](reference-Alerts.md#alert), but it has not been received yet. Those torrents would
report that they don't need to save resume data again, and skipped by
the initial loop, and thwart the counter otherwise.

## need\_save\_resume\_data()

```cpp
bool need_save_resume_data () const;
bool need_save_resume_data (resume_data_flags_t flags) const;
```

This function returns true if anything that is stored in the resume
data has changed since the last time resume data was saved.
The overload that takes flags let you ask if specific categories
of properties have changed. These flags have the same behavior as in
the [save\_resume\_data()](reference-Torrent_Handle.md#save_resume_data()) call.

This is a *blocking* call. It will wait for a response from
libtorrent's main thread. A way to avoid blocking is to instead
call [save\_resume\_data()](reference-Torrent_Handle.md#save_resume_data()) directly, specifying the conditions under
which resume data should be saved.

Note

A torrent's resume data is considered saved as soon as the
[save\_resume\_data\_alert](reference-Alerts.md#save_resume_data_alert) is posted. It is important to make sure this
[alert](reference-Alerts.md#alert) is received and handled in order for this function to be
meaningful.

## queue\_position\_top() queue\_position\_up() queue\_position() queue\_position\_bottom() queue\_position\_down()

```cpp
void queue_position_up () const;
void queue_position_top () const;
queue_position_t queue_position () const;
void queue_position_down () const;
void queue_position_bottom () const;
```

Every torrent that is added is assigned a queue position exactly one
greater than the greatest queue position of all existing torrents.
Torrents that are being seeded have -1 as their queue position, since
they're no longer in line to be downloaded.

When a torrent is removed or turns into a seed, all torrents with
greater queue positions have their positions decreased to fill in the
space in the sequence.

queue\_position() returns the torrent's position in the download
queue. The torrents with the smallest numbers are the ones that are
being downloaded. The smaller number, the closer the torrent is to the
front of the line to be started.

The queue position is also available in the [torrent\_status](reference-Torrent_Status.md#torrent_status).

The queue\_position\_\*() functions adjust the torrents position in
the queue. Up means closer to the front and down means closer to the
back of the queue. Top and bottom refers to the front and the back of
the queue respectively.

## queue\_position\_set()

```cpp
void queue_position_set (queue_position_t p) const;
```

updates the position in the queue for this torrent. The relative order
of all other torrents remain intact but their numerical queue position
shifts to make space for this torrent's new position

## set\_ssl\_certificate\_buffer() set\_ssl\_certificate()

```cpp
void set_ssl_certificate_buffer (std::string const& certificate
      , std::string const& private_key
      , std::string const& dh_params);
void set_ssl_certificate (std::string const& certificate
      , std::string const& private_key
      , std::string const& dh_params
      , std::string const& passphrase = "");
```

For SSL torrents, use this to specify a path to a .pem file to use as
this client's certificate. The certificate must be signed by the
certificate in the .torrent file to be valid.

The [set\_ssl\_certificate\_buffer()](reference-Torrent_Handle.md#set_ssl_certificate_buffer()) overload takes the actual certificate,
private key and DH params as strings, rather than paths to files.

cert is a path to the (signed) certificate in .pem format
corresponding to this torrent.

private\_key is a path to the private key for the specified
certificate. This must be in .pem format.

dh\_params is a path to the Diffie-Hellman parameter file, which
needs to be in .pem format. You can generate this file using the
openssl command like this: openssl dhparam -outform PEM -out
dhparams.pem 512.

passphrase may be specified if the private key is encrypted and
requires a passphrase to be decrypted.

Note that when a torrent first starts up, and it needs a certificate,
it will suspend connecting to any peers until it has one. It's
typically desirable to resume the torrent after setting the SSL
certificate.

If you receive a [torrent\_need\_cert\_alert](reference-Alerts.md#torrent_need_cert_alert), you need to call this to
provide a valid cert. If you don't have a cert you won't be allowed to
connect to any peers.

## torrent\_file() torrent\_file\_with\_hashes()

```cpp
std::shared_ptr<const torrent_info> torrent_file () const;
std::shared_ptr<torrent_info> torrent_file_with_hashes () const;
```

[torrent\_file()](reference-Torrent_Handle.md#torrent_file()) returns a pointer to the [torrent\_info](reference-Torrent_Info.md#torrent_info) object
associated with this torrent. The [torrent\_info](reference-Torrent_Info.md#torrent_info) object may be a copy
of the internal object. If the torrent doesn't have metadata, the
pointer will not be initialized (i.e. a nullptr). The torrent may be
in a state without metadata only if it was started without a .torrent
file, e.g. by being added by magnet link.

Note that the [torrent\_info](reference-Torrent_Info.md#torrent_info) object returned here may be a different
instance than the one added to the [session](reference-Session.md#session), with different attributes
like piece layers, dht nodes and trackers. A [torrent\_info](reference-Torrent_Info.md#torrent_info) object does
not round-trip cleanly when added to a [session](reference-Session.md#session).

If you want to save a .torrent file from the [torrent\_handle](reference-Torrent_Handle.md#torrent_handle), instead
call [save\_resume\_data()](reference-Torrent_Handle.md#save_resume_data()) and [write\_torrent\_file()](reference-Resume_Data.md#write_torrent_file()) the
[add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params) object passed back in the [alert](reference-Alerts.md#alert).

[torrent\_file\_with\_hashes()](reference-Torrent_Handle.md#torrent_file_with_hashes()) returns a *copy* of the internal
[torrent\_info](reference-Torrent_Info.md#torrent_info) and piece layer hashes (if it's a v2 torrent). The piece
layers will only be included if they are available. If this torrent
was added from a .torrent file with piece layers or if it's seeding,
the piece layers are available. This function is more expensive than
[torrent\_file()](reference-Torrent_Handle.md#torrent_file()) since it needs to make copies of this information.

The [torrent\_file\_with\_hashes()](reference-Torrent_Handle.md#torrent_file_with_hashes()) is here for backwards compatibility
when constructing a [create\_torrent](reference-Create_Torrents.md#create_torrent) object from a [torrent\_info](reference-Torrent_Info.md#torrent_info) that's
in a [session](reference-Session.md#session). Prefer [save\_resume\_data()](reference-Torrent_Handle.md#save_resume_data()) + [write\_torrent\_file()](reference-Resume_Data.md#write_torrent_file()).

Note that a torrent added from a magnet link may not have the full
merkle trees for all files, and hence not have the complete piece
layers. In that state, you cannot create a .torrent file even from
the [torrent\_info](reference-Torrent_Info.md#torrent_info) returned from [torrent\_file\_with\_hashes()](reference-Torrent_Handle.md#torrent_file_with_hashes()). Once the
torrent completes downloading all files, becoming a seed, you can
make a .torrent file from it.

## piece\_layers()

```cpp
std::vector<std::vector<sha256_hash>> piece_layers () const;
```

returns the piece layers for all files in the torrent. If this is a
v1 torrent (and doesn't have any piece layers) it returns an empty
vector. This is a blocking call that will synchronize with the
libtorrent network thread.

## post\_piece\_availability() piece\_availability()

```cpp
void piece_availability (std::vector<int>& avail) const;
void post_piece_availability () const;
```

The piece availability is the number of peers that we are connected
that has advertised having a particular piece. This is the information
that libtorrent uses in order to prefer picking rare pieces.

post\_piece\_availability() will trigger a [piece\_availability\_alert](reference-Alerts.md#piece_availability_alert)
to be posted.

piece\_availability() fills the specified std::vector<int>
with the availability for each piece in this torrent. libtorrent does
not keep track of availability for seeds, so if the torrent is
seeding the availability for all pieces is reported as 0.

## prioritize\_pieces() get\_piece\_priorities() piece\_priority()

```cpp
void prioritize_pieces (std::vector<std::pair<piece_index_t, download_priority_t>> const& pieces) const;
std::vector<download_priority_t> get_piece_priorities () const;
void piece_priority (piece_index_t index, download_priority_t priority) const;
download_priority_t piece_priority (piece_index_t index) const;
void prioritize_pieces (std::vector<download_priority_t> const& pieces) const;
```

These functions are used to set and get the priority of individual
pieces. By default all pieces have priority 4. That means that the
random rarest first algorithm is effectively active for all pieces.
You may however change the priority of individual pieces. There are 8
priority levels. 0 means not to download the piece at all. Otherwise,
lower priority values means less likely to be picked. Piece priority
takes precedence over piece availability. Every piece with priority 7
will be attempted to be picked before a priority 6 piece and so on.

The default priority of pieces is 4.

Piece priorities can not be changed for torrents that have not
downloaded the metadata yet. Magnet links won't have metadata
immediately. see the [metadata\_received\_alert](reference-Alerts.md#metadata_received_alert).

piece\_priority sets or gets the priority for an individual piece,
specified by index.

prioritize\_pieces takes a vector of integers, one integer per
piece in the torrent. All the piece priorities will be updated with
the priorities in the vector.
The second overload of prioritize\_pieces that takes a vector of pairs
will update the priorities of only select pieces, and leave all other
unaffected. Each pair is (piece, priority). That is, the first item is
the piece index and the second item is the priority of that piece.
Invalid entries, where the piece index or priority is out of range, are
not allowed.

get\_piece\_priorities returns a vector with one element for each piece
in the torrent. Each element is the current priority of that piece.

It's possible to cancel the effect of *file* priorities by setting the
priorities for the affected pieces. Care has to be taken when mixing
usage of file- and piece priorities.

## prioritize\_files() get\_file\_priorities() file\_priority()

```cpp
void prioritize_files (std::vector<download_priority_t> const& files) const;
void file_priority (file_index_t index, download_priority_t priority) const;
std::vector<download_priority_t> get_file_priorities () const;
download_priority_t file_priority (file_index_t index) const;
```

index must be in the range [0, number\_of\_files).

file\_priority() queries or sets the priority of file index.

prioritize\_files() takes a vector that has at as many elements as
there are files in the torrent. Each [entry](reference-Bencoding.md#entry) is the priority of that
file. The function sets the priorities of all the pieces in the
torrent based on the vector.

get\_file\_priorities() returns a vector with the priorities of all
files.

The priority values are the same as for [piece\_priority()](reference-Torrent_Handle.md#piece_priority()). See
[download\_priority\_t](reference-Core.md#download_priority_t).

Whenever a file priority is changed, all other piece priorities are
reset to match the file priorities. In order to maintain special
priorities for particular pieces, [piece\_priority()](reference-Torrent_Handle.md#piece_priority()) has to be called
again for those pieces.

You cannot set the file priorities on a torrent that does not yet have
metadata or a torrent that is a seed. file\_priority(int, int) and
[prioritize\_files()](reference-Torrent_Handle.md#prioritize_files()) are both no-ops for such torrents.

Since changing file priorities may involve disk operations (of moving
files in- and out of the part file), the internal accounting of file
priorities happen asynchronously. i.e. setting file priorities and then
immediately querying them may not yield the same priorities just set.
To synchronize with the priorities taking effect, wait for the
[file\_prio\_alert](reference-Alerts.md#file_prio_alert).

When combining file- and piece priorities, the resume file will record
both. When loading the resume data, the file priorities will be applied
first, then the piece priorities.

Moving data from a file into the part file is currently not
supported. If a file has its priority set to 0 *after* it has already
been created, it will not be moved into the partfile.

## force\_dht\_announce() force\_lsd\_announce() force\_reannounce()

```cpp
void force_reannounce (int seconds = 0, int idx = -1, reannounce_flags_t = {}) const;
void force_dht_announce () const;
void force_lsd_announce () const;
```

force\_reannounce() will force this torrent to do another tracker
request, to receive new peers. The seconds argument specifies how
many seconds from now to issue the tracker announces.

If the tracker's min\_interval has not passed since the last
announce, the forced announce will be scheduled to happen immediately
as the min\_interval expires. This is to honor trackers minimum
re-announce interval settings.

The tracker\_index argument specifies which tracker to re-announce.
If set to -1 (which is the default), all trackers are re-announce.

The flags argument can be used to affect the re-announce. See
ignore\_min\_interval.

force\_dht\_announce will announce the torrent to the DHT
immediately.

force\_lsd\_announce will announce the torrent on LSD
immediately.

## scrape\_tracker()

```cpp
void scrape_tracker (int idx = -1) const;
```

scrape\_tracker() will send a scrape request to a tracker. By
default (idx = -1) it will scrape the last working tracker. If
idx is >= 0, the tracker with the specified index will scraped.

A scrape request queries the tracker for statistics such as total
number of incomplete peers, complete peers, number of downloads etc.

This request will specifically update the num\_complete and
num\_incomplete fields in the [torrent\_status](reference-Torrent_Status.md#torrent_status) struct once it
completes. When it completes, it will generate a [scrape\_reply\_alert](reference-Alerts.md#scrape_reply_alert).
If it fails, it will generate a [scrape\_failed\_alert](reference-Alerts.md#scrape_failed_alert).

## set\_download\_limit() download\_limit() set\_upload\_limit() upload\_limit()

```cpp
int download_limit () const;
void set_download_limit (int limit) const;
void set_upload_limit (int limit) const;
int upload_limit () const;
```

set\_upload\_limit will limit the upload bandwidth used by this
particular torrent to the limit you set. It is given as the number of
bytes per second the torrent is allowed to upload.
set\_download\_limit works the same way but for download bandwidth
instead of upload bandwidth. Note that setting a higher limit on a
torrent then the global limit
(settings\_pack::upload\_rate\_limit) will not override the global
rate limit. The torrent can never upload more than the global rate
limit.

upload\_limit and download\_limit will return the current limit
setting, for upload and download, respectively.

Local peers are not rate limited by default. see [peer classes](manual-ref.md#peer-classes).

## connect\_peer()

```cpp
void connect_peer (tcp::endpoint const& adr, peer_source_flags_t source = {}
      , pex_flags_t flags = pex_encryption | pex_utp | pex_holepunch) const;
```

connect\_peer() is a way to manually connect to peers that one
believe is a part of the torrent. If the peer does not respond, or is
not a member of this torrent, it will simply be disconnected. No harm
can be done by using this other than an unnecessary connection attempt
is made. If the torrent is uninitialized or in queued or checking
mode, this will throw system\_error. The second (optional)
argument will be bitwise ORed into the source mask of this peer.
Typically this is one of the source flags in [peer\_info](reference-Core.md#peer_info). i.e.
tracker, pex, dht etc.

For possible values of flags, see [pex\_flags\_t](reference-Core.md#pex_flags_t).

## clear\_peers()

```cpp
void clear_peers ();
```

This will disconnect all peers and clear the peer list for this
torrent. New peers will have to be acquired before resuming, from
trackers, DHT or local service discovery, for example.

## set\_max\_uploads() max\_uploads()

```cpp
int max_uploads () const;
void set_max_uploads (int max_uploads) const;
```

set\_max\_uploads() sets the maximum number of peers that's unchoked
at the same time on this torrent. If you set this to -1, there will be
no limit. This defaults to infinite. The primary setting controlling
this is the global unchoke slots limit, set by unchoke\_slots\_limit in
[settings\_pack](reference-Settings.md#settings_pack).

max\_uploads() returns the current settings.

## set\_max\_connections() max\_connections()

```cpp
int max_connections () const;
void set_max_connections (int max_connections) const;
```

set\_max\_connections() sets the maximum number of connection this
torrent will open. If all connections are used up, incoming
connections may be refused or poor connections may be closed. This
must be at least 2. The default is unlimited number of connections. If
-1 is given to the function, it means unlimited. There is also a
global limit of the number of connections, set by
connections\_limit in [settings\_pack](reference-Settings.md#settings_pack).

max\_connections() returns the current settings.

## move\_storage()

```cpp
void move_storage (std::string const& save_path
      , move_flags_t flags = move_flags_t::always_replace_files
      ) const;
```

Moves the file(s) that this torrent are currently seeding from or
downloading to. If the given save\_path is not located on the same
drive as the original save path, the files will be copied to the new
drive and removed from their original location. This will block all
other disk IO, and other torrents download and upload rates may drop
while copying the file.

Since disk IO is performed in a separate thread, this operation is
also asynchronous. Once the operation completes, the
storage\_moved\_alert is generated, with the new path as the
message. If the move fails for some reason,
storage\_moved\_failed\_alert is generated instead, containing the
error message.

The flags argument determines the behavior of the copying/moving
of the files in the torrent. see [move\_flags\_t](reference-Storage.md#move_flags_t).

always\_replace\_files is the default and replaces any file that
exist in both the source directory and the target directory.

fail\_if\_exist first check to see that none of the copy operations
would cause an overwrite. If it would, it will fail. Otherwise it will
proceed as if it was in always\_replace\_files mode. Note that there
is an inherent race condition here. If the files in the target
directory appear after the check but before the copy or move
completes, they will be overwritten. When failing because of files
already existing in the target path, the error of
move\_storage\_failed\_alert is set to
boost::system::errc::file\_exists.

The intention is that a client may use this as a probe, and if it
fails, ask the user which mode to use. The client may then re-issue
the move\_storage call with one of the other modes.

dont\_replace always keeps the existing file in the target
directory, if there is one. The source files will still be removed in
that case. Note that it won't automatically re-check files. If an
incomplete torrent is moved into a directory with the complete files,
pause, move, force-recheck and resume. Without the re-checking, the
torrent will keep downloading and files in the new download directory
will be overwritten.

Files that have been renamed to have absolute paths are not moved by
this function. Keep in mind that files that don't belong to the
torrent but are stored in the torrent's directory may be moved as
well. This goes for files that have been renamed to absolute paths
that still end up inside the save path.

When copying files, sparse regions are not likely to be preserved.
This makes it proportionally more expensive to move a large torrent
when only few pieces have been downloaded, since the files are then
allocated with zeros in the destination directory.

## rename\_file()

```cpp
void rename_file (file_index_t index, std::string const& new_name) const;
```

Renames the file with the given index asynchronously. The rename
operation is complete when either a [file\_renamed\_alert](reference-Alerts.md#file_renamed_alert) or
[file\_rename\_failed\_alert](reference-Alerts.md#file_rename_failed_alert) is posted.

## info\_hashes() info\_hash()

```cpp
sha1_hash info_hash () const;
info_hash_t info_hashes () const;
```

returns the info-hash(es) of the torrent. If this handle is to a
torrent that hasn't loaded yet (for instance by being added) by a
URL, the returned value is undefined.
The info\_hash() returns the SHA-1 info-hash for v1 torrents and a
truncated hash for v2 torrents. For the full v2 info-hash, use
info\_hashes() instead.

## operator==() operator<() operator!=()

```cpp
bool operator!= (const torrent_handle& h) const;
bool operator< (const torrent_handle& h) const;
bool operator== (const torrent_handle& h) const;
```

comparison operators. The order of the torrents is unspecified
but stable.

## id()

```cpp
std::uint32_t id () const;
```

returns a unique identifier for this torrent. It's not a dense index.
It's not preserved across sessions.

## native\_handle()

```cpp
std::shared_ptr<torrent> native_handle () const;
```

This function is intended only for use by plugins and the [alert](reference-Alerts.md#alert)
dispatch function. This type does not have a stable ABI and should
be relied on as little as possible. Accessing the handle returned by
this function is not thread safe outside of libtorrent's internal
thread (which is used to invoke [plugin](reference-Plugins.md#plugin) callbacks).
The torrent class is not only eligible for changing ABI across
minor versions of libtorrent, its layout is also dependent on build
configuration. This adds additional requirements on a client to be
built with the exact same build configuration as libtorrent itself.
i.e. the TORRENT\_ macros must match between libtorrent and the
client builds.

## userdata()

```cpp
client_data_t userdata () const;
```

returns the userdata pointer as set in [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params)

## in\_session()

```cpp
bool in_session () const;
```

Returns true if the torrent is in the [session](reference-Session.md#session). It returns true before
session::remove\_torrent() is called, and false afterward.

Note that this is a blocking function, unlike [torrent\_handle::is\_valid()](reference-Torrent_Handle.md#is_valid())
which returns immediately.

overwrite\_existing
:   instruct libtorrent to overwrite any data that may already have been
    downloaded with the data of the new piece being added. Using this
    flag when adding a piece that is actively being downloaded from other
    peers may have some unexpected consequences, as blocks currently
    being downloaded from peers may not be replaced.

query\_distributed\_copies
:   calculates distributed\_copies, distributed\_full\_copies and
    distributed\_fraction.

query\_accurate\_download\_counters
:   includes partial downloaded blocks in total\_done and
    total\_wanted\_done.

query\_last\_seen\_complete
:   includes last\_seen\_complete.

query\_pieces
:   populate the pieces field in [torrent\_status](reference-Torrent_Status.md#torrent_status).

query\_verified\_pieces
:   includes verified\_pieces (only applies to torrents in *seed
    mode*).

query\_torrent\_file
:   includes torrent\_file, which is all the static information from
    the .torrent file.

query\_name
:   includes name, the name of the torrent. This is either derived
    from the .torrent file, or from the &dn= magnet link argument
    or possibly some other source. If the name of the torrent is not
    known, this is an empty string.

query\_save\_path
:   includes save\_path, the path to the directory the files of the
    torrent are saved to.

alert\_when\_available
:   used to ask libtorrent to send an [alert](reference-Alerts.md#alert) once the piece has been
    downloaded, by passing alert\_when\_available. When set, the
    [read\_piece\_alert](reference-Alerts.md#read_piece_alert) [alert](reference-Alerts.md#alert) will be delivered, with the piece data, when
    it's downloaded.

piece\_granularity
:   only calculate file progress at piece granularity. This makes
    the [file\_progress()](reference-Torrent_Handle.md#file_progress()) call cheaper and also only takes bytes that
    have passed the hash check into account, so progress cannot
    regress in this mode.

graceful\_pause
:   will delay the disconnect of peers that we're still downloading
    outstanding requests from. The torrent will not accept any more
    requests and will disconnect all idle peers. As soon as a peer is done
    transferring the blocks that were requested from it, it is
    disconnected. This is a graceful shut down of the torrent in the sense
    that no downloaded bytes are wasted.

flush\_disk\_cache
:   the disk cache will be flushed before creating the resume data.
    This avoids a problem with file timestamps in the resume data in
    case the cache hasn't been flushed yet.

save\_info\_dict
:   the resume data will contain the metadata from the torrent file as
    well. This is useful for clients that don't keep .torrent files
    around separately, or for torrents that were added via a magnet link.

only\_if\_modified
:   this flag has the same behavior as the combination of:
    if\_counters\_changed | if\_download\_progress | if\_config\_changed |
    if\_state\_changed | if\_metadata\_changed

if\_counters\_changed
:   save resume data if any [counters](reference-Stats.md#counters) has changed since the last time
    resume data was saved. This includes upload/download [counters](reference-Stats.md#counters), active
    time [counters](reference-Stats.md#counters) and scrape data. A torrent that is not paused will have
    its active time [counters](reference-Stats.md#counters) incremented continuously.

if\_download\_progress
:   save the resume data if any blocks have been downloaded since the
    last time resume data was saved. This includes:
    \* checking existing files on disk
    \* downloading a block from a peer

if\_config\_changed
:   save the resume data if configuration options changed since last time
    the resume data was saved. This includes:
    \* file- or piece priorities
    \* upload- and download rate limits
    \* change max-uploads (unchoke slots)
    \* change max connection limit
    \* enable/disable peer-exchange, local service discovery or DHT
    \* enable/disable apply IP-filter
    \* enable/disable auto-managed
    \* enable/disable share-mode
    \* enable/disable sequential-mode
    \* files renamed
    \* storage moved (save\_path changed)

if\_state\_changed
:   save the resume data if torrent state has changed since last time the
    resume data was saved. This includes:
    \* upload mode
    \* paused state
    \* super-seeding
    \* seed-mode

if\_metadata\_changed
:   save the resume data if any *metadata* changed since the last time
    resume data was saved. This includes:
    \* add/remove web seeds
    \* add/remove trackers
    \* receiving metadata for a magnet link

ignore\_min\_interval
:   by default, force-reannounce will still honor the min-interval
    published by the tracker. If this flag is set, it will be ignored
    and the tracker is announced immediately.

# hash\_value()

Declared in "[libtorrent/torrent\_handle.hpp](include/libtorrent/torrent_handle.hpp)"

```cpp
std::size_t hash_value (torrent_handle const& h);
```

for std::hash (and to support using this type in unordered\_map etc.)
