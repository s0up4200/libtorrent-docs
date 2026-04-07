---
title: "Add Torrent"
source: "https://libtorrent.org/reference-Add_Torrent.html"
---

# client\_data\_t

Declared in "[libtorrent/client\_data.hpp](include/libtorrent/client_data.hpp)"

A thin wrapper around a void pointer used as "user data". i.e. an opaque
cookie passed in to libtorrent and returned on demand. It adds type-safety by
requiring the same type be requested out of it as was assigned to it.

```cpp
struct client_data_t
{
   client_data_t () = default;
   explicit client_data_t (T* v);
   client_data_t& operator= (T* v);
   explicit operator T () const;
   T* get () const;
   client_data_t& operator= (void const*) = delete;
   operator void* () const = delete;
   client_data_t& operator= (void*) = delete;
   operator void const* () const = delete;

   template <typename T, typename U  = typename std::enable_if<std::is_pointer<T>::value>::type>
};
```

## client\_data\_t()

```cpp
client_data_t () = default;
```

construct a nullptr client data

## operator=() void\*() const\*()

```cpp
client_data_t& operator= (void const*) = delete;
operator void* () const = delete;
client_data_t& operator= (void*) = delete;
operator void const* () const = delete;
```

we don't allow type-unsafe operations

# add\_torrent\_params

Declared in "[libtorrent/add\_torrent\_params.hpp](include/libtorrent/add_torrent_params.hpp)"

The [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params) contains all the information in a .torrent file
along with all information necessary to add that torrent to a [session](reference-Session.md#session).
The key fields when adding a torrent are:

* ti - the immutable info-dict part of the torrent
* info\_hash - when you don't have the metadata (.torrent file). This
  uniquely identifies the torrent and can validate the info-dict when
  received from the swarm.

In order to add a torrent to a [session](reference-Session.md#session), one of those fields must be set
in addition to save\_path. The [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params) object can then be
passed into one of the session::add\_torrent() overloads or
session::async\_add\_torrent().

If you only specify the info-hash, the torrent file will be downloaded
from peers, which requires them to support the metadata extension. For
the metadata extension to work, libtorrent must be built with extensions
enabled (TORRENT\_DISABLE\_EXTENSIONS must not be defined). It also
takes an optional name argument. This may be left empty in case no
name should be assigned to the torrent. In case it's not, the name is
used for the torrent as long as it doesn't have metadata. See
torrent\_handle::name.

The add\_torrent\_params is also used when requesting resume data for a
torrent. It can be saved to and restored from a file and added back to a
new [session](reference-Session.md#session). For serialization and de-serialization of
add\_torrent\_params objects, see [read\_resume\_data()](reference-Resume_Data.md#read_resume_data()) and
[write\_resume\_data()](reference-Resume_Data.md#write_resume_data()).

The add\_torrent\_params is also used to represent a parsed .torrent
file. It can be loaded via [load\_torrent\_file()](reference-Core.md#load_torrent_file()), [load\_torrent\_buffer()](reference-Core.md#load_torrent_buffer()) and
[load\_torrent\_parsed()](reference-Core.md#load_torrent_parsed()). It can be saved via [write\_torrent\_file()](reference-Resume_Data.md#write_torrent_file()).

```cpp
struct add_torrent_params
{
   int version  = LIBTORRENT_VERSION_NUM;
   std::shared_ptr<torrent_info> ti;
   aux::noexcept_movable<std::vector<std::string>> trackers;
   aux::noexcept_movable<std::vector<int>> tracker_tiers;
   aux::noexcept_movable<std::vector<std::pair<std::string, int>>> dht_nodes;
   std::string name;
   std::string save_path;
   storage_mode_t storage_mode  = storage_mode_sparse;
   client_data_t userdata;
   aux::noexcept_movable<std::vector<download_priority_t>> file_priorities;
   std::string trackerid;
   torrent_flags_t flags  = torrent_flags::default_flags;
   info_hash_t info_hashes;
   int max_uploads  = -1;
   int max_connections  = -1;
   int upload_limit  = -1;
   int download_limit  = -1;
   std::int64_t total_uploaded  = 0;
   std::int64_t total_downloaded  = 0;
   int active_time  = 0;
   int finished_time  = 0;
   int seeding_time  = 0;
   std::time_t added_time  = 0;
   std::time_t completed_time  = 0;
   std::time_t last_seen_complete  = 0;
   int num_complete  = -1;
   int num_incomplete  = -1;
   int num_downloaded  = -1;
   aux::noexcept_movable<std::vector<std::string>> http_seeds;
   aux::noexcept_movable<std::vector<std::string>> url_seeds;
   aux::noexcept_movable<std::vector<tcp::endpoint>> peers;
   aux::noexcept_movable<std::vector<tcp::endpoint>> banned_peers;
   aux::noexcept_movable<std::map<piece_index_t, bitfield>> unfinished_pieces;
   typed_bitfield<piece_index_t> have_pieces;
   typed_bitfield<piece_index_t> verified_pieces;
   aux::noexcept_movable<std::vector<download_priority_t>> piece_priorities;
   aux::vector<std::vector<sha256_hash>, file_index_t> merkle_trees;
   aux::vector<std::vector<bool>, file_index_t> merkle_tree_mask;
   aux::vector<std::vector<bool>, file_index_t> verified_leaf_hashes;
   aux::noexcept_movable<std::map<file_index_t, std::string>> renamed_files;
   std::time_t last_download  = 0;
   std::time_t last_upload  = 0;
};
```

version
:   filled in by the constructor and should be left untouched. It is used
    for forward binary compatibility.

ti
:   [torrent\_info](reference-Torrent_Info.md#torrent_info) object with the torrent to add. Unless the
    info\_hash is set, this is required to be initialized.

trackers
:   If the torrent doesn't have a tracker, but relies on the DHT to find
    peers, the trackers can specify tracker URLs for the torrent.

tracker\_tiers
:   the tiers the URLs in trackers belong to. Trackers belonging to
    different tiers may be treated differently, as defined by the multi
    tracker extension. This is optional, if not specified trackers are
    assumed to be part of tier 0, or whichever the last tier was as
    iterating over the trackers.

dht\_nodes
:   a list of hostname and port pairs, representing DHT nodes to be added
    to the [session](reference-Session.md#session) (if DHT is enabled). The hostname may be an IP address.

name
:   in case there's no other name in this torrent, this name will be used.
    The name out of the [torrent\_info](reference-Torrent_Info.md#torrent_info) object takes precedence if available.

save\_path
:   the path where the torrent is or will be stored.

    Note

    On windows this path (and other paths) are interpreted as UNC
    paths. This means they must use backslashes as directory separators
    and may not contain the special directories "." or "..".

    Setting this to an absolute path performs slightly better than a
    relative path.

storage\_mode
:   One of the values from [storage\_mode\_t](reference-Storage.md#storage_mode_t). For more information, see
    [storage allocation](manual-ref.md#storage-allocation).

userdata
:   The userdata parameter is optional and will be passed on to the
    extension constructor functions, if any
    (see [torrent\_handle::add\_extension()](reference-Torrent_Handle.md#add_extension())). It will also be stored in the
    torrent object and can be retrieved by calling [userdata()](reference-Torrent_Handle.md#userdata()).

file\_priorities
:   can be set to control the initial file priorities when adding a
    torrent. The semantics are the same as for
    torrent\_handle::prioritize\_files(). The file priorities specified
    in here take precedence over those specified in the resume data, if
    any.
    If this vector of file priorities is shorter than the number of files
    in the torrent, the remaining files (not covered by this) will still
    have the default download priority. This default can be changed by
    setting the default\_dont\_download torrent\_flag.

trackerid
:   the default tracker id to be used when announcing to trackers. By
    default this is empty, and no tracker ID is used, since this is an
    optional argument. If a tracker returns a tracker ID, that ID is used
    instead of this.

flags
:   flags controlling aspects of this torrent and how it's added. See
    [torrent\_flags\_t](reference-Core.md#torrent_flags_t) for details.

    Note

    The flags field is initialized with default flags by the
    constructor. In order to preserve default behavior when clearing or
    setting other flags, make sure to bitwise OR or in a flag or bitwise
    AND the inverse of a flag to clear it.

info\_hashes
:   set this to the info hash of the torrent to add in case the info-hash
    is the only known property of the torrent. i.e. you don't have a
    .torrent file nor a magnet link.
    To add a magnet link, use [parse\_magnet\_uri()](reference-Core.md#parse_magnet_uri()) to populate fields in the
    [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params) object.

max\_uploads max\_connections
:   max\_uploads, max\_connections, upload\_limit,
    download\_limit correspond to the set\_max\_uploads(),
    set\_max\_connections(), set\_upload\_limit() and
    set\_download\_limit() functions on [torrent\_handle](reference-Torrent_Handle.md#torrent_handle). These values let
    you initialize these settings when the torrent is added, instead of
    calling these functions immediately following adding it.

    -1 means unlimited on these settings just like their counterpart
    functions on [torrent\_handle](reference-Torrent_Handle.md#torrent_handle)

    For fine grained control over rate limits, including making them apply
    to local peers, see [peer classes](manual-ref.md#peer-classes).

upload\_limit download\_limit
:   the upload and download rate limits for this torrent, specified in
    bytes per second. -1 means unlimited.

total\_uploaded total\_downloaded
:   the total number of bytes uploaded and downloaded by this torrent so
    far.

active\_time finished\_time seeding\_time
:   the number of seconds this torrent has spent in started, finished and
    seeding state so far, respectively.

added\_time completed\_time
:   if set to a non-zero value, this is the posix time of when this torrent
    was first added, including previous runs/sessions. If set to zero, the
    internal added\_time will be set to the time of when [add\_torrent()](reference-Session.md#add_torrent()) is
    called.

last\_seen\_complete
:   if set to non-zero, initializes the time (expressed in posix time) when
    we last saw a seed or peers that together formed a complete copy of the
    torrent. If left set to zero, the internal counterpart to this field
    will be updated when we see a seed or a distributed copies >= 1.0.

num\_complete num\_incomplete num\_downloaded
:   these field can be used to initialize the torrent's cached scrape data.
    The scrape data is high level metadata about the current state of the
    swarm, as returned by the tracker (either when announcing to it or by
    sending a specific scrape request). num\_complete is the number of
    peers in the swarm that are seeds, or have every piece in the torrent.
    num\_incomplete is the number of peers in the swarm that do not have
    every piece. num\_downloaded is the number of times the torrent has
    been downloaded (not initiated, but the number of times a download has
    completed).

    Leaving any of these values set to -1 indicates we don't know, or we
    have not received any scrape data.

http\_seeds url\_seeds
:   URLs can be added to these two lists to specify additional web
    seeds to be used by the torrent. If the flag\_override\_web\_seeds
    is set, these will be the \_only\_ ones to be used. i.e. any web seeds
    found in the .torrent file will be overridden.

    http\_seeds expects URLs to web servers implementing the original HTTP
    seed specification [BEP 17](https://www.bittorrent.org/beps/bep_0017.html).

    url\_seeds expects URLs to regular web servers, aka "get right" style,
    specified in [BEP 19](https://www.bittorrent.org/beps/bep_0019.html).

peers
:   peers to add to the torrent, to be tried to be connected to as
    bittorrent peers.

banned\_peers
:   peers banned from this torrent. The will not be connected to

unfinished\_pieces
:   this is a map of partially downloaded piece. The key is the piece index
    and the value is a [bitfield](reference-Utility.md#bitfield) where each bit represents a 16 kiB block.
    A set bit means we have that block.

have\_pieces
:   this is a [bitfield](reference-Utility.md#bitfield) indicating which pieces we already have of this
    torrent.

verified\_pieces
:   when in seed\_mode, pieces with a set bit in this [bitfield](reference-Utility.md#bitfield) have been
    verified to be valid. Other pieces will be verified the first time a
    peer requests it.

piece\_priorities
:   this sets the priorities for each individual piece in the torrent. Each
    element in the vector represent the piece with the same index. If you
    set both file- and piece priorities, file priorities will take
    precedence.

merkle\_trees
:   v2 hashes, if known

merkle\_tree\_mask
:   if set, indicates which hashes are included in the corresponding
    vector of merkle\_trees. These bitmasks always cover the full
    tree, a cleared bit means the hash is all zeros (i.e. not set) and
    set bit means the next hash in the corresponding vector in
    merkle\_trees is the hash for that node. This is an optimization
    to avoid storing a lot of zeros.

verified\_leaf\_hashes
:   bit-fields indicating which v2 leaf hashes have been verified
    against the root hash. If this vector is empty and merkle\_trees is
    non-empty it implies that all hashes in merkle\_trees are verified.

renamed\_files
:   this is a map of file indices in the torrent and new filenames to be
    applied before the torrent is added.

last\_download last\_upload
:   the posix time of the last time payload was received or sent for this
    torrent, respectively. A value of 0 means we don't know when we last
    uploaded or downloaded, or we have never uploaded or downloaded any
    payload for this torrent.
