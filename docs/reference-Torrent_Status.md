---
title: "Torrent Status"
source: "https://libtorrent.org/reference-Torrent_Status.html"
---

# torrent\_status

Declared in "[libtorrent/torrent\_status.hpp](include/libtorrent/torrent_status.hpp)"

holds a snapshot of the status of a torrent, as queried by
[torrent\_handle::status()](reference-Torrent_Handle.md#status()).

```cpp
struct torrent_status
{
   bool operator== (torrent_status const& st) const;

   enum state_t
   {
      checking_files,
      downloading_metadata,
      downloading,
      finished,
      seeding,
      unused_enum_for_backwards_compatibility_allocating,
      checking_resume_data,
   };

   torrent_handle handle;
   error_code errc;
   file_index_t error_file  = torrent_status::error_file_none;
   static constexpr file_index_t error_file_none {-1};
   static constexpr file_index_t error_file_ssl_ctx {-3};
   static constexpr file_index_t error_file_metadata {-4};
   static constexpr file_index_t error_file_exception {-5};
   static constexpr file_index_t error_file_partfile {-6};
   std::string save_path;
   std::string name;
   std::weak_ptr<const torrent_info> torrent_file;
   time_duration next_announce  = seconds{0};
   std::string current_tracker;
   std::int64_t total_download  = 0;
   std::int64_t total_upload  = 0;
   std::int64_t total_payload_download  = 0;
   std::int64_t total_payload_upload  = 0;
   std::int64_t total_failed_bytes  = 0;
   std::int64_t total_redundant_bytes  = 0;
   typed_bitfield<piece_index_t> pieces;
   typed_bitfield<piece_index_t> verified_pieces;
   std::int64_t total_done  = 0;
   std::int64_t total  = 0;
   std::int64_t total_wanted_done  = 0;
   std::int64_t total_wanted  = 0;
   std::int64_t all_time_upload  = 0;
   std::int64_t all_time_download  = 0;
   std::time_t added_time  = 0;
   std::time_t completed_time  = 0;
   std::time_t last_seen_complete  = 0;
   storage_mode_t storage_mode  = storage_mode_sparse;
   float progress  = 0.f;
   int progress_ppm  = 0;
   queue_position_t queue_position {};
   int download_rate  = 0;
   int upload_rate  = 0;
   int download_payload_rate  = 0;
   int upload_payload_rate  = 0;
   int num_seeds  = 0;
   int num_peers  = 0;
   int num_complete  = -1;
   int num_incomplete  = -1;
   int list_seeds  = 0;
   int list_peers  = 0;
   int connect_candidates  = 0;
   int num_pieces  = 0;
   int distributed_full_copies  = 0;
   int distributed_fraction  = 0;
   float distributed_copies  = 0.f;
   int block_size  = 0;
   int num_uploads  = 0;
   int num_connections  = 0;
   int uploads_limit  = 0;
   int connections_limit  = 0;
   int up_bandwidth_queue  = 0;
   int down_bandwidth_queue  = 0;
   int seed_rank  = 0;
   state_t state  = checking_resume_data;
   bool need_save_resume  = false;
   bool is_seeding  = false;
   bool is_finished  = false;
   bool has_metadata  = false;
   bool has_incoming  = false;
   bool moving_storage  = false;
   bool announcing_to_trackers  = false;
   bool announcing_to_lsd  = false;
   bool announcing_to_dht  = false;
   info_hash_t info_hashes;
   time_point last_upload;
   time_point last_download;
   seconds active_duration;
   seconds finished_duration;
   seconds seeding_duration;
   torrent_flags_t flags {};
};
```

## operator==()

```cpp
bool operator== (torrent_status const& st) const;
```

compares if the torrent status objects come from the same torrent. i.e.
only the [torrent\_handle](reference-Torrent_Handle.md#torrent_handle) field is compared.

## enum state\_t

Declared in "[libtorrent/torrent\_status.hpp](include/libtorrent/torrent_status.hpp)"

| name | value | description |
| --- | --- | --- |
| checking\_files | 1 | The torrent has not started its download yet, and is currently checking existing files. |
| downloading\_metadata | 2 | The torrent is trying to download metadata from peers. This implies the ut\_metadata extension is in use. |
| downloading | 3 | The torrent is being downloaded. This is the state most torrents will be in most of the time. The progress meter will tell how much of the files that has been downloaded. |
| finished | 4 | In this state the torrent has finished downloading but still doesn't have the entire torrent. i.e. some pieces are filtered and won't get downloaded. |
| seeding | 5 | In this state the torrent has finished downloading and is a pure seeder. |
| unused\_enum\_for\_backwards\_compatibility\_allocating | 6 | If the torrent was started in full allocation mode, this indicates that the (disk) storage for the torrent is allocated. |
| checking\_resume\_data | 7 | The torrent is currently checking the fast resume data and comparing it to the files on disk. This is typically completed in a fraction of a second, but if you add a large number of torrents at once, they will queue up. |

handle
:   a handle to the torrent whose status the object represents.

errc
:   may be set to an error code describing why the torrent was paused, in
    case it was paused by an error. If the torrent is not paused or if it's
    paused but not because of an error, this error\_code is not set.
    if the error is attributed specifically to a file, error\_file is set to
    the index of that file in the .torrent file.

error\_file
:   if the torrent is stopped because of an disk I/O error, this field
    contains the index of the file in the torrent that encountered the
    error. If the error did not originate in a file in the torrent, there
    are a few special values this can be set to: error\_file\_none,
    error\_file\_ssl\_ctx, error\_file\_exception, error\_file\_partfile or
    error\_file\_metadata;

error\_file\_none
:   special values for error\_file to describe which file or component
    encountered the error (errc).
    the error did not occur on a file

error\_file\_ssl\_ctx
:   the error occurred setting up the SSL context

error\_file\_metadata
:   the error occurred while loading the metadata for the torrent

error\_file\_exception
:   there was a serious error reported in this torrent. The error code
    or a torrent log [alert](reference-Alerts.md#alert) may provide more information.

error\_file\_partfile
:   the error occurred with the partfile

save\_path
:   the path to the directory where this torrent's files are stored.
    It's typically the path as was given to [async\_add\_torrent()](reference-Session.md#async_add_torrent()) or
    [add\_torrent()](reference-Session.md#add_torrent()) when this torrent was started. This field is only
    included if the torrent status is queried with
    torrent\_handle::query\_save\_path.

name
:   the name of the torrent. Typically this is derived from the
    .torrent file. In case the torrent was started without metadata,
    and hasn't completely received it yet, it returns the name given
    to it when added to the [session](reference-Session.md#session). See session::add\_torrent.
    This field is only included if the torrent status is queried
    with torrent\_handle::query\_name.

torrent\_file
:   set to point to the torrent\_info object for this torrent. It's
    only included if the torrent status is queried with
    torrent\_handle::query\_torrent\_file.

next\_announce
:   the time until the torrent will announce itself to the tracker.

current\_tracker
:   the URL of the last working tracker. If no tracker request has
    been successful yet, it's set to an empty string.

total\_download total\_upload
:   the number of bytes downloaded and uploaded to all peers, accumulated,
    *this session* only. The [session](reference-Session.md#session) is considered to restart when a
    torrent is paused and restarted again. When a torrent is paused, these
    [counters](reference-Stats.md#counters) are reset to 0. If you want complete, persistent, stats, see
    all\_time\_upload and all\_time\_download.

total\_payload\_download total\_payload\_upload
:   counts the amount of bytes send and received this [session](reference-Session.md#session), but only
    the actual payload data (i.e the interesting data), these [counters](reference-Stats.md#counters)
    ignore any protocol overhead. The [session](reference-Session.md#session) is considered to restart
    when a torrent is paused and restarted again. When a torrent is
    paused, these [counters](reference-Stats.md#counters) are reset to 0.

total\_failed\_bytes
:   the number of bytes that has been downloaded and that has failed the
    piece hash test. In other words, this is just how much crap that has
    been downloaded since the torrent was last started. If a torrent is
    paused and then restarted again, this counter will be reset.

total\_redundant\_bytes
:   the number of bytes that has been downloaded even though that data
    already was downloaded. The reason for this is that in some situations
    the same data can be downloaded by mistake. When libtorrent sends
    requests to a peer, and the peer doesn't send a response within a
    certain timeout, libtorrent will re-request that block. Another
    situation when libtorrent may re-request blocks is when the requests
    it sends out are not replied in FIFO-order (it will re-request blocks
    that are skipped by an out of order block). This is supposed to be as
    low as possible. This only counts bytes since the torrent was last
    started. If a torrent is paused and then restarted again, this counter
    will be reset.

pieces
:   a bitmask that represents which pieces we have (set to true) and the
    pieces we don't have. It's a pointer and may be set to 0 if the
    torrent isn't downloading or seeding.

verified\_pieces
:   a bitmask representing which pieces has had their hash checked. This
    only applies to torrents in *seed mode*. If the torrent is not in seed
    mode, this bitmask may be empty.

total\_done
:   the total number of bytes of the file(s) that we have. All this does
    not necessarily has to be downloaded during this [session](reference-Session.md#session) (that's
    total\_payload\_download).

total
:   the total number of bytes to download for this torrent. This
    may be less than the size of the torrent in case there are
    pad files. This number only counts bytes that will actually
    be requested from peers.

total\_wanted\_done
:   the number of bytes we have downloaded, only counting the pieces that
    we actually want to download. i.e. excluding any pieces that we have
    but have priority 0 (i.e. not wanted).
    Once a torrent becomes seed, any piece- and file priorities are
    forgotten and all bytes are considered "wanted".

total\_wanted
:   The total number of bytes we want to download. This may be smaller
    than the total torrent size in case any pieces are prioritized to 0,
    i.e. not wanted.
    Once a torrent becomes seed, any piece- and file priorities are
    forgotten and all bytes are considered "wanted".

all\_time\_upload all\_time\_download
:   are accumulated upload and download payload byte [counters](reference-Stats.md#counters). They are
    saved in and restored from resume data to keep totals across sessions.

added\_time
:   the posix-time when this torrent was added. i.e. what time(nullptr)
    returned at the time.

completed\_time
:   the posix-time when this torrent was finished. If the torrent is not
    yet finished, this is 0.

last\_seen\_complete
:   the time when we, or one of our peers, last saw a complete copy of
    this torrent.

storage\_mode
:   The allocation mode for the torrent. See [storage\_mode\_t](reference-Storage.md#storage_mode_t) for the
    options. For more information, see [storage allocation](manual-ref.md#storage-allocation).

progress
:   a value in the range [0, 1], that represents the progress of the
    torrent's current task. It may be checking files or downloading.

progress\_ppm
:   progress parts per million (progress \* 1000000) when disabling
    floating point operations, this is the only option to query progress

    reflects the same value as progress, but instead in a range [0,
    1000000] (ppm = parts per million). When floating point operations are
    disabled, this is the only alternative to the floating point value in
    progress.

queue\_position
:   the position this torrent has in the download
    queue. If the torrent is a seed or finished, this is -1.

download\_rate upload\_rate
:   the total rates for all peers for this torrent. These will usually
    have better precision than summing the rates from all peers. The rates
    are given as the number of bytes per second.

download\_payload\_rate upload\_payload\_rate
:   the total transfer rate of payload only, not counting protocol
    chatter. This might be slightly smaller than the other rates, but if
    projected over a long time (e.g. when calculating ETA:s) the
    difference may be noticeable.

num\_seeds
:   the number of peers that are seeding that this client is
    currently connected to.

num\_peers
:   the number of peers this torrent currently is connected to. Peer
    connections that are in the half-open state (is attempting to connect)
    or are queued for later connection attempt do not count. Although they
    are visible in the peer list when you call [get\_peer\_info()](reference-Torrent_Handle.md#get_peer_info()).

num\_complete num\_incomplete
:   if the tracker sends scrape info in its announce reply, these fields
    will be set to the total number of peers that have the whole file and
    the total number of peers that are still downloading. set to -1 if the
    tracker did not send any scrape data in its announce reply.

list\_seeds list\_peers
:   the number of seeds in our peer list and the total number of peers
    (including seeds). We are not necessarily connected to all the peers
    in our peer list. This is the number of peers we know of in total,
    including banned peers and peers that we have failed to connect to.

connect\_candidates
:   the number of peers in this torrent's peer list that is a candidate to
    be connected to. i.e. It has fewer connect attempts than the max fail
    count, it is not a seed if we are a seed, it is not banned etc. If
    this is 0, it means we don't know of any more peers that we can try.

num\_pieces
:   the number of pieces that has been downloaded. It is equivalent to:
    std::accumulate(pieces->begin(), pieces->end()). So you don't have
    to count yourself. This can be used to see if anything has updated
    since last time if you want to keep a graph of the pieces up to date.
    Note that these pieces have not necessarily been written to disk yet,
    and there is a risk the write to disk will fail.

distributed\_full\_copies
:   the number of distributed copies of the torrent. Note that one copy
    may be spread out among many peers. It tells how many copies there are
    currently of the rarest piece(s) among the peers this client is
    connected to.

distributed\_fraction
:   tells the share of pieces that have more copies than the rarest
    piece(s). Divide this number by 1000 to get the fraction.

    For example, if distributed\_full\_copies is 2 and
    distributed\_fraction is 500, it means that the rarest pieces have
    only 2 copies among the peers this torrent is connected to, and that
    50% of all the pieces have more than two copies.

    If we are a seed, the piece picker is deallocated as an optimization,
    and piece availability is no longer tracked. In this case the
    distributed copies members are set to -1.

distributed\_copies
:   the number of distributed copies of the file. note that one copy may
    be spread out among many peers. This is a floating point
    representation of the distributed copies.

    the integer part tells how many copies
    :   there are of the rarest piece(s)

    the fractional part tells the fraction of pieces that
    :   have more copies than the rarest piece(s).

block\_size
:   the size of a block, in bytes. A block is a sub piece, it is the
    number of bytes that each piece request asks for and the number of
    bytes that each bit in the partial\_piece\_info's bitset represents,
    see [get\_download\_queue()](reference-Torrent_Handle.md#get_download_queue()). This is typically 16 kB, but it may be
    smaller, if the pieces are smaller.

num\_uploads
:   the number of unchoked peers in this torrent.

num\_connections
:   the number of peer connections this torrent has, including half-open
    connections that hasn't completed the bittorrent handshake yet. This
    is always >= num\_peers.

uploads\_limit
:   the set limit of upload slots (unchoked peers) for this torrent.

connections\_limit
:   the set limit of number of connections for this torrent.

up\_bandwidth\_queue down\_bandwidth\_queue
:   the number of peers in this torrent that are waiting for more
    bandwidth quota from the torrent rate limiter. This can determine if
    the rate you get from this torrent is bound by the torrents limit or
    not. If there is no limit set on this torrent, the peers might still
    be waiting for bandwidth quota from the global limiter, but then they
    are counted in the session\_status object.

seed\_rank
:   A rank of how important it is to seed the torrent, it is used to
    determine which torrents to seed and which to queue. It is based on
    the peer to seed ratio from the tracker scrape. For more information,
    see [queuing](manual-ref.md#queuing). Higher value means more important to seed

state
:   the main state the torrent is in. See [torrent\_status::state\_t](reference-Torrent_Status.md#state_t).

need\_save\_resume
:   true if this torrent has unsaved changes
    to its download state and statistics since the last resume data
    was saved.

is\_seeding
:   true if all pieces have been downloaded.

is\_finished
:   true if all pieces that have a priority > 0 are downloaded. There is
    only a distinction between finished and seeding if some pieces or
    files have been set to priority 0, i.e. are not downloaded.

has\_metadata
:   true if this torrent has metadata (either it was started from a
    .torrent file or the metadata has been downloaded). The only scenario
    where this can be false is when the torrent was started torrent-less
    (i.e. with just an info-hash and tracker ip, a magnet link for
    instance).

has\_incoming
:   true if there has ever been an incoming connection attempt to this
    torrent.

moving\_storage
:   this is true if this torrent's storage is currently being moved from
    one location to another. This may potentially be a long operation
    if a large file ends up being copied from one drive to another.

announcing\_to\_trackers announcing\_to\_lsd announcing\_to\_dht
:   these are set to true if this torrent is allowed to announce to the
    respective peer source. Whether they are true or false is determined by
    the queue logic/auto manager. Torrents that are not auto managed will
    always be allowed to announce to all peer sources.

info\_hashes
:   the info-hash for this torrent

last\_upload last\_download
:   the timestamps of the last time this torrent uploaded or downloaded
    payload to any peer.

active\_duration finished\_duration seeding\_duration
:   these are cumulative [counters](reference-Stats.md#counters) of for how long the torrent has been in
    different states. active means not paused and added to [session](reference-Session.md#session). Whether
    it has found any peers or not is not relevant.
    finished means all selected files/pieces were downloaded and available
    to other peers (this is always a subset of active time).
    seeding means all files/pieces were downloaded and available to
    peers. Being available to peers does not imply there are other peers
    asking for the payload.

flags
:   reflects several of the torrent's flags. For more
    information, see torrent\_handle::flags().
