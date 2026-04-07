---
title: "Core"
source: "https://libtorrent.org/reference-Core.html"
---

# peer\_request

Declared in "[libtorrent/peer\_request.hpp](include/libtorrent/peer_request.hpp)"

represents a byte range within a piece. Internally this is is used for
incoming piece requests.

```cpp
struct peer_request
{
   bool operator== (peer_request const& r) const;

   piece_index_t piece;
   int start;
   int length;
};
```

## operator==()

```cpp
bool operator== (peer_request const& r) const;
```

returns true if the right hand side [peer\_request](reference-Core.md#peer_request) refers to the same
range as this does.

piece
:   The index of the piece in which the range starts.

start
:   The byte offset within that piece where the range starts.

length
:   The size of the range, in bytes.

# peer\_info

Declared in "[libtorrent/peer\_info.hpp](include/libtorrent/peer_info.hpp)"

holds information and statistics about one peer
that libtorrent is connected to

```cpp
struct peer_info
{
   sha256_hash i2p_destination () const;

   std::string client;
   typed_bitfield<piece_index_t> pieces;
   std::int64_t total_download;
   std::int64_t total_upload;
   time_duration last_request;
   time_duration last_active;
   time_duration download_queue_time;
   static constexpr peer_flags_t interesting  = 0_bit;
   static constexpr peer_flags_t choked  = 1_bit;
   static constexpr peer_flags_t remote_interested  = 2_bit;
   static constexpr peer_flags_t remote_choked  = 3_bit;
   static constexpr peer_flags_t supports_extensions  = 4_bit;
   static constexpr peer_flags_t outgoing_connection  = 5_bit;
   static constexpr peer_flags_t local_connection  = 5_bit;
   static constexpr peer_flags_t handshake  = 6_bit;
   static constexpr peer_flags_t connecting  = 7_bit;
   static constexpr peer_flags_t on_parole  = 9_bit;
   static constexpr peer_flags_t seed  = 10_bit;
   static constexpr peer_flags_t optimistic_unchoke  = 11_bit;
   static constexpr peer_flags_t snubbed  = 12_bit;
   static constexpr peer_flags_t upload_only  = 13_bit;
   static constexpr peer_flags_t endgame_mode  = 14_bit;
   static constexpr peer_flags_t holepunched  = 15_bit;
   static constexpr peer_flags_t i2p_socket  = 16_bit;
   static constexpr peer_flags_t utp_socket  = 17_bit;
   static constexpr peer_flags_t ssl_socket  = 18_bit;
   static constexpr peer_flags_t rc4_encrypted  = 19_bit;
   static constexpr peer_flags_t plaintext_encrypted  = 20_bit;
   peer_flags_t flags;
   static constexpr peer_source_flags_t tracker  = 0_bit;
   static constexpr peer_source_flags_t dht  = 1_bit;
   static constexpr peer_source_flags_t pex  = 2_bit;
   static constexpr peer_source_flags_t lsd  = 3_bit;
   static constexpr peer_source_flags_t resume_data  = 4_bit;
   static constexpr peer_source_flags_t incoming  = 5_bit;
   peer_source_flags_t source;
   int up_speed;
   int down_speed;
   int payload_up_speed;
   int payload_down_speed;
   peer_id pid;
   int queue_bytes;
   int request_timeout;
   int send_buffer_size;
   int used_send_buffer;
   int receive_buffer_size;
   int used_receive_buffer;
   int receive_buffer_watermark;
   int num_hashfails;
   int download_queue_length;
   int timed_out_requests;
   int busy_requests;
   int requests_in_buffer;
   int target_dl_queue_length;
   int upload_queue_length;
   int failcount;
   piece_index_t downloading_piece_index;
   int downloading_block_index;
   int downloading_progress;
   int downloading_total;
   static constexpr connection_type_t standard_bittorrent  = 0_bit;
   static constexpr connection_type_t web_seed  = 1_bit;
   static constexpr connection_type_t http_seed  = 2_bit;
   connection_type_t connection_type;
   int pending_disk_bytes;
   int pending_disk_read_bytes;
   int send_quota;
   int receive_quota;
   int rtt;
   int num_pieces;
   int download_rate_peak;
   int upload_rate_peak;
   float progress;
   int progress_ppm;
   tcp::endpoint ip;
   tcp::endpoint local_endpoint;
   static constexpr bandwidth_state_flags_t bw_idle  = 0_bit;
   static constexpr bandwidth_state_flags_t bw_limit  = 1_bit;
   static constexpr bandwidth_state_flags_t bw_network  = 2_bit;
   static constexpr bandwidth_state_flags_t bw_disk  = 4_bit;
   bandwidth_state_flags_t read_state;
   bandwidth_state_flags_t write_state;
};
```

## i2p\_destination()

```cpp
sha256_hash i2p_destination () const;
```

If this peer is an i2p peer, this function returns the destination
address of the peer

client
:   A human readable string describing the software at the other end of
    the connection. In some cases this information is not available, then
    it will contain a string that may give away something about which
    software is running in the other end. In the case of a web seed, the
    server type and version will be a part of this string. This is UTF-8
    encoded.

pieces
:   a [bitfield](reference-Utility.md#bitfield), with one bit per piece in the torrent. Each bit tells you
    if the peer has that piece (if it's set to 1) or if the peer miss that
    piece (set to 0).

total\_download total\_upload
:   the total number of bytes downloaded from and uploaded to this peer.
    These numbers do not include the protocol chatter, but only the
    payload data.

last\_request last\_active
:   the time since we last sent a request to this peer and since any
    transfer occurred with this peer

download\_queue\_time
:   the time until all blocks in the request queue will be downloaded

interesting
:   **we** are interested in pieces from this peer.

choked
:   **we** have choked this peer.

remote\_interested
:   the peer is interested in **us**

remote\_choked
:   the peer has choked **us**.

supports\_extensions
:   means that this peer supports the
    [extension protocol](extension_protocol.md).

outgoing\_connection
:   The connection was initiated by us, the peer has a
    listen port open, and that port is the same as in the
    address of this peer. If this flag is not set, this
    peer connection was opened by this peer connecting to
    us.

local\_connection
:   deprecated synonym for outgoing\_connection

handshake
:   The connection is opened, and waiting for the
    handshake. Until the handshake is done, the peer
    cannot be identified.

connecting
:   The connection is in a half-open state (i.e. it is
    being connected).

on\_parole
:   The peer has participated in a piece that failed the
    hash check, and is now "on parole", which means we're
    only requesting whole pieces from this peer until
    it either fails that piece or proves that it doesn't
    send bad data.

seed
:   This peer is a seed (it has all the pieces).

optimistic\_unchoke
:   This peer is subject to an optimistic unchoke. It has
    been unchoked for a while to see if it might unchoke
    us in return an earn an upload/unchoke slot. If it
    doesn't within some period of time, it will be choked
    and another peer will be optimistically unchoked.

snubbed
:   This peer has recently failed to send a block within
    the request timeout from when the request was sent.
    We're currently picking one block at a time from this
    peer.

upload\_only
:   This peer has either explicitly (with an extension)
    or implicitly (by becoming a seed) told us that it
    will not downloading anything more, regardless of
    which pieces we have.

endgame\_mode
:   This means the last time this peer picket a piece,
    it could not pick as many as it wanted because there
    were not enough free ones. i.e. all pieces this peer
    has were already requested from other peers.

holepunched
:   This flag is set if the peer was in holepunch mode
    when the connection succeeded. This typically only
    happens if both peers are behind a NAT and the peers
    connect via the NAT holepunch mechanism.

i2p\_socket
:   indicates that this socket is running on top of the
    I2P transport.

utp\_socket
:   indicates that this socket is a uTP socket

ssl\_socket
:   indicates that this socket is running on top of an SSL
    (TLS) channel

rc4\_encrypted
:   this connection is obfuscated with RC4

plaintext\_encrypted
:   the handshake of this connection was obfuscated
    with a Diffie-Hellman exchange

flags
:   tells you in which state the peer is in. It is set to
    any combination of the peer\_flags\_t flags above.

tracker
:   The peer was received from the tracker.

dht
:   The peer was received from the kademlia DHT.

pex
:   The peer was received from the peer exchange
    extension.

lsd
:   The peer was received from the local service
    discovery (The peer is on the local network).

resume\_data
:   The peer was added from the fast resume data.

incoming
:   we received an incoming connection from this peer

source
:   a combination of flags describing from which sources this peer
    was received. A combination of the peer\_source\_flags\_t above.

up\_speed down\_speed
:   the current upload and download speed we have to and from this peer
    (including any protocol messages). updated about once per second

payload\_up\_speed payload\_down\_speed
:   The transfer rates of payload data only updated about once per second

pid
:   the peer's id as used in the bittorrent protocol. This id can be used
    to extract 'fingerprints' from the peer. Sometimes it can tell you
    which client the peer is using. See identify\_client()\_

queue\_bytes
:   the number of bytes we have requested from this peer, but not yet
    received.

request\_timeout
:   the number of seconds until the current front piece request will time
    out. This timeout can be adjusted through
    settings\_pack::request\_timeout.
    -1 means that there is not outstanding request.

send\_buffer\_size used\_send\_buffer
:   the number of bytes allocated
    and used for the peer's send buffer, respectively.

receive\_buffer\_size used\_receive\_buffer receive\_buffer\_watermark
:   the number of bytes
    allocated and used as receive buffer, respectively.

num\_hashfails
:   the number of pieces this peer has participated in sending us that
    turned out to fail the hash check.

download\_queue\_length
:   this is the number of requests we have sent to this peer that we
    haven't got a response for yet

timed\_out\_requests
:   the number of block requests that have timed out, and are still in the
    download queue

busy\_requests
:   the number of busy requests in the download queue. A busy request is a
    request for a block we've also requested from a different peer

requests\_in\_buffer
:   the number of requests messages that are currently in the send buffer
    waiting to be sent.

target\_dl\_queue\_length
:   the number of requests that is tried to be maintained (this is
    typically a function of download speed)

upload\_queue\_length
:   the number of piece-requests we have received from this peer
    that we haven't answered with a piece yet.

failcount
:   the number of times this peer has "failed". i.e. failed to connect or
    disconnected us. The failcount is decremented when we see this peer in
    a tracker response or peer exchange message.

downloading\_piece\_index downloading\_block\_index downloading\_progress downloading\_total
:   You can know which piece, and which part of that piece, that is
    currently being downloaded from a specific peer by looking at these
    four members. downloading\_piece\_index is the index of the piece
    that is currently being downloaded. This may be set to -1 if there's
    currently no piece downloading from this peer. If it is >= 0, the
    other three members are valid. downloading\_block\_index is the
    index of the block (or sub-piece) that is being downloaded.
    downloading\_progress is the number of bytes of this block we have
    received from the peer, and downloading\_total is the total number
    of bytes in this block.

standard\_bittorrent
:   Regular bittorrent connection

web\_seed
:   HTTP connection using the [BEP 19](https://www.bittorrent.org/beps/bep_0019.html) protocol

http\_seed
:   HTTP connection using the [BEP 17](https://www.bittorrent.org/beps/bep_0017.html) protocol

connection\_type
:   the kind of connection this peer uses. See connection\_type\_t.

pending\_disk\_bytes
:   the number of bytes this peer has pending in the disk-io thread.
    Downloaded and waiting to be written to disk. This is what is capped
    by settings\_pack::max\_queued\_disk\_bytes.

pending\_disk\_read\_bytes
:   number of outstanding bytes to read
    from disk

send\_quota receive\_quota
:   the number of bytes this peer has been assigned to be allowed to send
    and receive until it has to request more quota from the bandwidth
    manager.

rtt
:   an estimated round trip time to this peer, in milliseconds. It is
    estimated by timing the TCP connect(). It may be 0 for
    incoming connections.

num\_pieces
:   the number of pieces this peer has.

download\_rate\_peak upload\_rate\_peak
:   the highest download and upload rates seen on this connection. They
    are given in bytes per second. This number is reset to 0 on reconnect.

progress
:   the progress of the peer in the range [0, 1]. This is always 0 when
    floating point operations are disabled, instead use progress\_ppm.

progress\_ppm
:   indicates the download progress of the peer in the range [0, 1000000]
    (parts per million).

ip
:   the IP-address to this peer. The type is an asio endpoint. For
    more info, see the [asio](http://asio.sourceforge.net/asio-0.3.8/doc/asio/reference.html) documentation. This field is not valid for
    i2p peers. Instead use the [i2p\_destination()](reference-Core.md#i2p_destination()) function.

local\_endpoint
:   the IP and port pair the socket is bound to locally. i.e. the IP
    address of the interface it's going out over. This may be useful for
    multi-homed clients with multiple interfaces to the internet.
    This field is not valid for i2p peers.

bw\_idle
:   The peer is not waiting for any external events to
    send or receive data.

bw\_limit
:   The peer is waiting for the rate limiter.

bw\_network
:   The peer has quota and is currently waiting for a
    network read or write operation to complete. This is
    the state all peers are in if there are no bandwidth
    limits.

bw\_disk
:   The peer is waiting for the disk I/O thread to catch
    up writing buffers to disk before downloading more.

read\_state write\_state
:   bitmasks indicating what state this peer
    is in with regards to sending and receiving data. The states are
    defined as independent flags of type bandwidth\_state\_flags\_t, in this
    class.

# info\_hash\_t

Declared in "[libtorrent/info\_hash.hpp](include/libtorrent/info_hash.hpp)"

class holding the info-hash of a torrent. It can hold a v1 info-hash
(SHA-1) or a v2 info-hash (SHA-256) or both.

Note

If has\_v2() is false then the v1 hash might actually be a truncated
v2 hash

```cpp
struct info_hash_t
{
   info_hash_t () noexcept = default;
   explicit info_hash_t (sha256_hash h2) noexcept;
   explicit info_hash_t (sha1_hash h1) noexcept;
   info_hash_t (sha1_hash h1, sha256_hash h2) noexcept;
   bool has_v1 () const;
   bool has_v2 () const;
   bool has (protocol_version v) const;
   sha1_hash get (protocol_version v) const;
   sha1_hash get_best () const;
   friend bool operator!= (info_hash_t const& lhs, info_hash_t const& rhs);
   friend bool operator== (info_hash_t const& lhs, info_hash_t const& rhs) noexcept;
   template <typename F> void for_each (F f) const;
   bool operator< (info_hash_t const& o) const;
   friend std::ostream& operator<< (std::ostream& os, info_hash_t const& ih);

   sha1_hash v1;
   sha256_hash v2;
};
```

## info\_hash\_t()

```cpp
info_hash_t () noexcept = default;
explicit info_hash_t (sha256_hash h2) noexcept;
explicit info_hash_t (sha1_hash h1) noexcept;
info_hash_t (sha1_hash h1, sha256_hash h2) noexcept;
```

The default constructor creates an object that has neither a v1 or v2
hash.

For backwards compatibility, make it possible to construct directly
from a v1 hash. This constructor allows *implicit* conversion from a
v1 hash, but the implicitness is deprecated.

## has\_v1() has() has\_v2()

```cpp
bool has_v1 () const;
bool has_v2 () const;
bool has (protocol_version v) const;
```

returns true if the corresponding info hash is present in this
object.

## get()

```cpp
sha1_hash get (protocol_version v) const;
```

returns the has for the specified protocol version

## get\_best()

```cpp
sha1_hash get_best () const;
```

returns the v2 (truncated) info-hash, if there is one, otherwise
returns the v1 info-hash

## for\_each()

```cpp
template <typename F> void for_each (F f) const;
```

calls the function object f for each hash that is available.
starting with v1. The signature of F is:

```cpp
void(sha1_hash const&, protocol_version);
```

# piece\_block

Declared in "[libtorrent/piece\_block.hpp](include/libtorrent/piece_block.hpp)"

```cpp
struct piece_block
{
   piece_block () = default;
   piece_block (piece_index_t p_index, int b_index);
   bool operator< (piece_block const& b) const;
   bool operator== (piece_block const& b) const;
   bool operator!= (piece_block const& b) const;

   static const piece_block invalid;
   piece_index_t piece_index {0};
   int block_index  = 0;
};
```

# load\_torrent\_file() load\_torrent\_buffer() load\_torrent\_parsed()

Declared in "[libtorrent/load\_torrent.hpp](include/libtorrent/load_torrent.hpp)"

```cpp
add_torrent_params load_torrent_parsed (
   bdecode_node const& torrent_file, load_torrent_limits const& cfg);
add_torrent_params load_torrent_buffer (
   span<char const> buffer);
add_torrent_params load_torrent_buffer (
   span<char const> buffer, load_torrent_limits const& cfg);
add_torrent_params load_torrent_parsed (
   bdecode_node const& torrent_file);
add_torrent_params load_torrent_file (
   std::string const& filename, load_torrent_limits const& cfg);
add_torrent_params load_torrent_file (
   std::string const& filename);
```

These functions load the content of a .torrent file into an
[add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params) object.
The immutable part of a torrent file (the info-dictionary) is stored in
the ti field in the [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params) object (as a [torrent\_info](reference-Torrent_Info.md#torrent_info)
object).
The returned object is suitable to be:

> * added to a [session](reference-Session.md#session) via [add\_torrent()](reference-Session.md#add_torrent()) or [async\_add\_torrent()](reference-Session.md#async_add_torrent())
> * saved as a .torrent\_file via [write\_torrent\_file()](reference-Resume_Data.md#write_torrent_file())
> * turned into a magnet link via [make\_magnet\_uri()](reference-Core.md#make_magnet_uri())

# torrent\_peer\_equal()

Declared in "[libtorrent/torrent\_peer.hpp](include/libtorrent/torrent_peer.hpp)"

```cpp
inline bool torrent_peer_equal (torrent_peer const* lhs, torrent_peer const* rhs);
```

# make\_magnet\_uri()

Declared in "[libtorrent/magnet\_uri.hpp](include/libtorrent/magnet_uri.hpp)"

```cpp
std::string make_magnet_uri (torrent_handle const& handle);
std::string make_magnet_uri (torrent_info const& info);
std::string make_magnet_uri (add_torrent_params const& atp);
```

Generates a magnet URI from the specified torrent.

Several fields from the [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params) objects are recorded in the
magnet link. In order to not include them, they have to be cleared before
calling [make\_magnet\_uri()](reference-Core.md#make_magnet_uri()). These fields are used:

> ti, info\_hashes, url\_seeds, dht\_nodes,
> file\_priorities, trackers, name, peers.

Depending on what the use case for the resulting magnet link is, clearing
peers and dht\_nodes is probably a good idea if the [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params)
came from a running torrent. Those lists may be long and be ephemeral.

If none of the info\_hashes or ti fields are set, there is not
info-hash available, and a magnet link cannot be created. In this case
[make\_magnet\_uri()](reference-Core.md#make_magnet_uri()) returns an empty string.

The recommended way to generate a magnet link from a [torrent\_handle](reference-Torrent_Handle.md#torrent_handle) is to
call [save\_resume\_data()](reference-Torrent_Handle.md#save_resume_data()), which will post a [save\_resume\_data\_alert](reference-Alerts.md#save_resume_data_alert)
containing an [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params) object. This can then be passed to
[make\_magnet\_uri()](reference-Core.md#make_magnet_uri()).

The overload that takes a [torrent\_handle](reference-Torrent_Handle.md#torrent_handle) will make blocking calls to
query information about the torrent. If the torrent handle is invalid,
an empty string is returned.

For more information about magnet links, see [magnet links](manual-ref.md#magnet-links).

# parse\_magnet\_uri()

Declared in "[libtorrent/magnet\_uri.hpp](include/libtorrent/magnet_uri.hpp)"

```cpp
void parse_magnet_uri (string_view uri, add_torrent_params& p, error_code& ec);
add_torrent_params parse_magnet_uri (string_view uri, error_code& ec);
add_torrent_params parse_magnet_uri (string_view uri);
```

This function parses out information from the magnet link and populates the
[add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params) object. The overload that does not take an
error\_code reference will throw a system\_error on error
The overload taking an add\_torrent\_params reference will fill in the
fields specified in the magnet URI.

# version()

Declared in "[libtorrent/version.hpp](include/libtorrent/version.hpp)"

```cpp
char const* version ();
```

returns the libtorrent version as string form in this format:
"<major>.<minor>.<tiny>.<tag>"

# truncate\_files()

Declared in "[libtorrent/truncate.hpp](include/libtorrent/truncate.hpp)"

```cpp
void truncate_files (file_storage const& fs, std::string const& save_path, storage_error& ec);
```

Truncates files larger than specified in the [file\_storage](reference-Storage.md#file_storage), saved under
the specified save\_path.

# enum event\_t

Declared in "[libtorrent/tracker\_manager.hpp](include/libtorrent/tracker_manager.hpp)"

| name | value | description |
| --- | --- | --- |
| none | 0 |  |
| completed | 1 |  |
| started | 2 |  |
| stopped | 3 |  |
| paused | 4 |  |

# enum socket\_type\_t

Declared in "[libtorrent/socket\_type.hpp](include/libtorrent/socket_type.hpp)"

| name | value | description |
| --- | --- | --- |
| tcp | 0 |  |
| socks5 | 1 |  |
| http | 2 |  |
| utp | 3 |  |
| i2p | 4 |  |
| tcp\_ssl | 5 |  |
| socks5\_ssl | 6 |  |
| http\_ssl | 7 |  |
| utp\_ssl | 8 |  |

# enum connection\_type

Declared in "[libtorrent/peer\_connection.hpp](include/libtorrent/peer_connection.hpp)"

| name | value | description |
| --- | --- | --- |
| bittorrent | 0 |  |
| url\_seed | 1 |  |
| http\_seed | 2 |  |

# enum portmap\_transport

Declared in "[libtorrent/portmap.hpp](include/libtorrent/portmap.hpp)"

| name | value | description |
| --- | --- | --- |
| natpmp | 0 | natpmp can be NAT-PMP or PCP |
| upnp | 1 |  |

# enum portmap\_protocol

Declared in "[libtorrent/portmap.hpp](include/libtorrent/portmap.hpp)"

| name | value | description |
| --- | --- | --- |
| none | 0 |  |
| tcp | 1 |  |
| udp | 2 |  |

# enum protocol\_version

Declared in "[libtorrent/info\_hash.hpp](include/libtorrent/info_hash.hpp)"

| name | value | description |
| --- | --- | --- |
| V1 | 0 | The original BitTorrent version, using SHA-1 hashes |
| V2 | 1 | Version 2 of the BitTorrent protocol, using SHA-256 hashes |
| NUM | 2 |  |

# int

Declared in "[libtorrent/version.hpp](include/libtorrent/version.hpp)"

version\_major
:   the major, minor and tiny versions of libtorrent

version\_minor
:   the major, minor and tiny versions of libtorrent

version\_tiny
:   the major, minor and tiny versions of libtorrent

# download\_priority\_t

Declared in "[libtorrent/download\_priority.hpp](include/libtorrent/download_priority.hpp)"

dont\_download
:   Don't download the file or piece. Partial pieces may still be downloaded when
    setting file priorities.

default\_priority
:   The default priority for files and pieces.

low\_priority
:   The lowest priority for files and pieces.

top\_priority
:   The highest priority for files and pieces.

# char const\*

Declared in "[libtorrent/version.hpp](include/libtorrent/version.hpp)"

version\_str
:   the libtorrent version in string form

# std::uint64\_t

Declared in "[libtorrent/version.hpp](include/libtorrent/version.hpp)"

version\_revision
:   the git commit of this libtorrent version

# pex\_flags\_t

Declared in "[libtorrent/pex\_flags.hpp](include/libtorrent/pex_flags.hpp)"

pex\_encryption
:   the peer supports protocol encryption

pex\_seed
:   the peer is a seed

pex\_utp
:   the peer supports the uTP, transport protocol over UDP.

pex\_holepunch
:   the peer supports the holepunch extension If this flag is received from a
    peer, it can be used as a rendezvous point in case direct connections to
    the peer fail

pex\_lt\_v2
:   protocol v2
    this is not a standard flag, it is only used internally

# torrent\_flags\_t

Declared in "[libtorrent/torrent\_flags.hpp](include/libtorrent/torrent_flags.hpp)"

seed\_mode
:   If seed\_mode is set, libtorrent will assume that all files
    are present for this torrent and that they all match the hashes in
    the torrent file. Each time a peer requests to download a block,
    the piece is verified against the hash, unless it has been verified
    already. If a hash fails, the torrent will automatically leave the
    seed mode and recheck all the files. The use case for this mode is
    if a torrent is created and seeded, or if the user already know
    that the files are complete, this is a way to avoid the initial
    file checks, and significantly reduce the startup time.

    Setting seed\_mode on a torrent without metadata (a
    .torrent file) is a no-op and will be ignored.

    It is not possible to *set* the seed\_mode flag on a torrent after it has
    been added to a [session](reference-Session.md#session). It is possible to *clear* it though.

upload\_mode
:   If upload\_mode is set, the torrent will be initialized in
    upload-mode, which means it will not make any piece requests. This
    state is typically entered on disk I/O errors, and if the torrent
    is also auto managed, it will be taken out of this state
    periodically (see settings\_pack::optimistic\_disk\_retry).

    This mode can be used to avoid race conditions when
    adjusting priorities of pieces before allowing the torrent to start
    downloading.

    If the torrent is auto-managed (auto\_managed), the torrent
    will eventually be taken out of upload-mode, regardless of how it
    got there. If it's important to manually control when the torrent
    leaves upload mode, don't make it auto managed.

share\_mode
:   determines if the torrent should be added in *share mode* or not.
    Share mode indicates that we are not interested in downloading the
    torrent, but merely want to improve our share ratio (i.e. increase
    it). A torrent started in share mode will do its best to never
    download more than it uploads to the swarm. If the swarm does not
    have enough demand for upload capacity, the torrent will not
    download anything. This mode is intended to be safe to add any
    number of torrents to, without manual screening, without the risk
    of downloading more than is uploaded.

    A torrent in share mode sets the priority to all pieces to 0,
    except for the pieces that are downloaded, when pieces are decided
    to be downloaded. This affects the progress bar, which might be set
    to "100% finished" most of the time. Do not change file or piece
    priorities for torrents in share mode, it will make it not work.

    The share mode has one setting, the share ratio target, see
    settings\_pack::share\_mode\_target for more info.

apply\_ip\_filter
:   determines if the IP filter should apply to this torrent or not. By
    default all torrents are subject to filtering by the IP filter
    (i.e. this flag is set by default). This is useful if certain
    torrents needs to be exempt for some reason, being an auto-update
    torrent for instance.

paused
:   specifies whether or not the torrent is paused. i.e. it won't connect to the tracker or any of the peers
    until it's resumed. Note that a paused torrent that also has the
    auto\_managed flag set can be started at any time by libtorrent's queuing
    logic. See [queuing](manual-ref.md#queuing).

auto\_managed
:   If the torrent is auto-managed (auto\_managed), the torrent
    may be resumed at any point, regardless of how it paused. If it's
    important to manually control when the torrent is paused and
    resumed, don't make it auto managed.

    If auto\_managed is set, the torrent will be queued,
    started and seeded automatically by libtorrent. When this is set,
    the torrent should also be started as paused. The default queue
    order is the order the torrents were added. They are all downloaded
    in that order. For more details, see [queuing](manual-ref.md#queuing).

duplicate\_is\_error
:   used in [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params) to indicate that it's an error to attempt
    to add a torrent that's already in the [session](reference-Session.md#session). If it's not considered an
    error, a handle to the existing torrent is returned.
    This flag is not saved by [write\_resume\_data()](reference-Resume_Data.md#write_resume_data()), since it is only meant for
    adding torrents.

update\_subscribe
:   on by default and means that this torrent will be part of state
    updates when calling [post\_torrent\_updates()](reference-Session.md#post_torrent_updates()).
    This flag is not saved by [write\_resume\_data()](reference-Resume_Data.md#write_resume_data()).

super\_seeding
:   sets the torrent into super seeding/initial seeding mode. If the torrent
    is not a seed, this flag has no effect.

sequential\_download
:   sets the sequential download state for the torrent. In this mode the
    piece picker will pick pieces with low index numbers before pieces with
    high indices. The actual pieces that are picked depend on other factors
    still, such as which pieces a peer has and whether it is in parole mode
    or "prefer whole pieces"-mode. Sequential mode is not ideal for streaming
    media. For that, see [set\_piece\_deadline()](reference-Torrent_Handle.md#set_piece_deadline()) instead.

stop\_when\_ready
:   When this flag is set, the torrent will *force stop* whenever it
    transitions from a non-data-transferring state into a data-transferring
    state (referred to as being ready to download or seed). This is useful
    for torrents that should not start downloading or seeding yet, but want
    to be made ready to do so. A torrent may need to have its files checked
    for instance, so it needs to be started and possibly queued for checking
    (auto-managed and started) but as soon as it's done, it should be
    stopped.

    *Force stopped* means auto-managed is set to false and it's paused. As
    if the auto\_manages flag is cleared and the paused flag is set on the torrent.

    Note that the torrent may transition into a downloading state while
    setting this flag, and since the logic is edge triggered you may
    miss the edge. To avoid this race, if the torrent already is in a
    downloading state when this call is made, it will trigger the
    stop-when-ready immediately.

    When the stop-when-ready logic fires, the flag is cleared. Any
    subsequent transitions between downloading and non-downloading states
    will not be affected, until this flag is set again.

    The behavior is more robust when setting this flag as part of adding
    the torrent. See [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params).

    The stop-when-ready flag fixes the inherent race condition of waiting
    for the [state\_changed\_alert](reference-Alerts.md#state_changed_alert) and then call [pause()](reference-Session.md#pause()). The download/seeding
    will most likely start in between posting the [alert](reference-Alerts.md#alert) and receiving the
    call to pause.

    A downloading state is one where peers are being connected. Which means
    just downloading the metadata via the ut\_metadata extension counts
    as a downloading state. In order to stop a torrent once the metadata
    has been downloaded, instead set all file priorities to dont\_download

override\_trackers
:   when this flag is set, the tracker list in the [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params)
    object override any trackers from the torrent file. If the flag is
    not set, the trackers from the [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params) object will be
    added to the list of trackers used by the torrent.
    This flag is set by [read\_resume\_data()](reference-Resume_Data.md#read_resume_data()) if there are trackers present in
    the resume data file. This effectively makes the trackers saved in the
    resume data take precedence over the original trackers. This includes if
    there's an empty list of trackers, to support the case where they were
    explicitly removed in the previous [session](reference-Session.md#session).
    This flag is not saved by [write\_resume\_data()](reference-Resume_Data.md#write_resume_data())

override\_web\_seeds
:   If this flag is set, the web seeds from the [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params)
    object will override any web seeds in the torrent file. If it's not
    set, web seeds in the [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params) object will be added to the
    list of web seeds used by the torrent.
    This flag is set by [read\_resume\_data()](reference-Resume_Data.md#read_resume_data()) if there are web seeds present in
    the resume data file. This effectively makes the web seeds saved in the
    resume data take precedence over the original ones. This includes if
    there's an empty list of web seeds, to support the case where they were
    explicitly removed in the previous [session](reference-Session.md#session).
    This flag is not saved by [write\_resume\_data()](reference-Resume_Data.md#write_resume_data())

need\_save\_resume
:   if this flag is set (which it is by default) the torrent will be
    considered needing to save its resume data immediately, in the
    category if\_metadata\_changed. See resume\_data\_flags\_t and
    [save\_resume\_data()](reference-Torrent_Handle.md#save_resume_data()) for details.

    This flag is cleared by a successful call to [save\_resume\_data()](reference-Torrent_Handle.md#save_resume_data())
    This flag is not saved by [write\_resume\_data()](reference-Resume_Data.md#write_resume_data()), since it represents an
    ephemeral state of a running torrent.

disable\_dht
:   set this flag to disable DHT for this torrent. This lets you have the DHT
    enabled for the whole client, and still have specific torrents not
    participating in it. i.e. not announcing to the DHT nor picking up peers
    from it.

disable\_lsd
:   set this flag to disable local service discovery for this torrent.

disable\_pex
:   set this flag to disable peer exchange for this torrent.

no\_verify\_files
:   if this flag is set, the resume data will be assumed to be correct
    without validating it against any files on disk. This may be used when
    restoring a [session](reference-Session.md#session) by loading resume data from disk. It will save time
    and also delay any hard disk errors until files are actually needed. If
    the resume data cannot be trusted, or if a torrent is added for the first
    time to some save path that may already have some of the files, this flag
    should not be set.

default\_dont\_download
:   default all file priorities to dont\_download. This is useful for adding
    magnet links where the number of files is unknown, but the
    file\_priorities is still set for some files. Any file not covered by
    the file\_priorities list will be set to normal download priority,
    unless this flag is set, in which case they will be set to 0
    (dont\_download).

i2p\_torrent
:   this flag makes the torrent be considered an "i2p torrent" for purposes
    of the allow\_i2p\_mixed setting. When mixing regular peers and i2p peers
    is disabled, i2p torrents won't add normal peers to its peer list.
    Note that non i2p torrents may still allow i2p peers (on the off-chance
    that a tracker return them and the [session](reference-Session.md#session) is configured with a SAM
    connection).
    This flag is set automatically when adding a torrent that has at least
    one tracker whose hostname ends with .i2p.
    It's also set by [parse\_magnet\_uri()](reference-Core.md#parse_magnet_uri()) if the tracker list contains such
    URL.

all
:   all torrent flags combined. Can conveniently be used when creating masks
    for flags
