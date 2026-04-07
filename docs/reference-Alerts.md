---
title: "Alerts"
source: "https://libtorrent.org/reference-Alerts.html"
---

The [pop\_alerts()](reference-Session.md#pop_alerts()) function on [session](reference-Session.md#session) is the main interface for retrieving
alerts (warnings, messages and errors from libtorrent). If no alerts have
been posted by libtorrent [pop\_alerts()](reference-Session.md#pop_alerts()) will return an empty list.

By default, only errors are reported. [settings\_pack::alert\_mask](reference-Settings.md#alert_mask) can be
used to specify which kinds of events should be reported. The [alert](reference-Alerts.md#alert) mask is
a combination of the [alert\_category\_t](reference-Alerts.md#alert_category_t) flags in the [alert](reference-Alerts.md#alert) class.

Every [alert](reference-Alerts.md#alert) belongs to one or more category. There is a cost associated with
posting alerts. Only alerts that belong to an enabled category are
posted. Setting the [alert](reference-Alerts.md#alert) bitmask to 0 will disable all alerts (except those
that are non-discardable). Alerts that are responses to API calls such as
[save\_resume\_data()](reference-Torrent_Handle.md#save_resume_data()) and [post\_session\_stats()](reference-Session.md#post_session_stats()) are non-discardable and will be
posted even if their category is disabled.

There are other [alert](reference-Alerts.md#alert) base classes that some alerts derive from, all the
alerts that are generated for a specific torrent are derived from
[torrent\_alert](reference-Alerts.md#torrent_alert), and tracker events derive from [tracker\_alert](reference-Alerts.md#tracker_alert).

Alerts returned by [pop\_alerts()](reference-Session.md#pop_alerts()) are only valid until the next call to
[pop\_alerts()](reference-Session.md#pop_alerts()). You may not copy an [alert](reference-Alerts.md#alert) object to access it after the next
call to [pop\_alerts()](reference-Session.md#pop_alerts()). Internal members of alerts also become invalid once
[pop\_alerts()](reference-Session.md#pop_alerts()) is called again.

# dht\_routing\_bucket

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

struct to hold information about a single DHT routing table bucket

```cpp
struct dht_routing_bucket
{
   int num_nodes;
   int num_replacements;
   int last_active;
};
```

num\_nodes num\_replacements
:   the total number of nodes and replacement nodes
    in the routing table

last\_active
:   number of seconds since last activity

# torrent\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This is a base class for alerts that are associated with a
specific torrent. It contains a handle to the torrent.

Note that by the time the client receives a [torrent\_alert](reference-Alerts.md#torrent_alert), its
handle member may be invalid.

```cpp
struct torrent_alert : alert
{
   std::string message () const override;
   char const* torrent_name () const;

   torrent_handle handle;
};
```

## message()

```cpp
std::string message () const override;
```

returns the message associated with this [alert](reference-Alerts.md#alert)

handle
:   The [torrent\_handle](reference-Torrent_Handle.md#torrent_handle) pointing to the torrent this
    [alert](reference-Alerts.md#alert) is associated with.

# peer\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

The peer [alert](reference-Alerts.md#alert) is a base class for alerts that refer to a specific peer. It includes all
the information to identify the peer. i.e. ip and peer-id.

```cpp
struct peer_alert : torrent_alert
{
   std::string message () const override;

   aux::noexcept_movable<tcp::endpoint> endpoint;
   peer_id pid;
};
```

endpoint
:   The peer's IP address and port.

pid
:   the peer ID, if known.

# tracker\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This is a base class used for alerts that are associated with a
specific tracker. It derives from [torrent\_alert](reference-Alerts.md#torrent_alert) since a tracker
is also associated with a specific torrent.

```cpp
struct tracker_alert : torrent_alert
{
   std::string message () const override;
   char const* tracker_url () const;

   aux::noexcept_movable<tcp::endpoint> local_endpoint;
};
```

## tracker\_url()

```cpp
char const* tracker_url () const;
```

returns a 0-terminated string of the tracker's URL

local\_endpoint
:   endpoint of the listen interface being announced

# torrent\_removed\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

The torrent\_removed\_alert is posted whenever a torrent is removed. Since
the torrent handle in its base class will usually be invalid (since the torrent
is already removed) it has the info hash as a member, to identify it.
It's posted when the alert\_category::status bit is set in the alert\_mask.

Note that the handle remains valid for some time after
[torrent\_removed\_alert](reference-Alerts.md#torrent_removed_alert) is posted, as long as some internal libtorrent
task (such as an I/O task) refers to it. Additionally, other alerts like
[save\_resume\_data\_alert](reference-Alerts.md#save_resume_data_alert) may be posted after [torrent\_removed\_alert](reference-Alerts.md#torrent_removed_alert).
To synchronize on whether the torrent has been removed or not, call
[torrent\_handle::in\_session()](reference-Torrent_Handle.md#in_session()). This will return true before
[torrent\_removed\_alert](reference-Alerts.md#torrent_removed_alert) is posted, and false afterward.

Even though the handle member doesn't point to an existing torrent anymore,
it is still useful for comparing to other handles, which may also no
longer point to existing torrents, but to the same non-existing torrents.

The torrent\_handle acts as a weak\_ptr, even though its object no
longer exists, it can still compare equal to another weak pointer which
points to the same non-existent object.

```cpp
struct torrent_removed_alert final : torrent_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::status;
   info_hash_t info_hashes;
   client_data_t userdata;
};
```

userdata
:   'userdata` as set in [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params) at torrent creation.
    This can be used to associate this torrent with related data
    in the client application more efficiently than info\_hashes.

# read\_piece\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is posted when the asynchronous read operation initiated by
a call to [torrent\_handle::read\_piece()](reference-Torrent_Handle.md#read_piece()) is completed. If the read failed, the torrent
is paused and an error state is set and the buffer member of the [alert](reference-Alerts.md#alert)
is 0. If successful, buffer points to a buffer containing all the data
of the piece. piece is the piece index that was read. size is the
number of bytes that was read.

If the operation fails, error will indicate what went wrong.

```cpp
struct read_piece_alert final : torrent_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::storage;
   error_code const error;
   boost::shared_array<char> const buffer;
   piece_index_t const piece;
   int const size;
};
```

# file\_completed\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This is posted whenever an individual file completes its download. i.e.
All pieces overlapping this file have passed their hash check.

```cpp
struct file_completed_alert final : torrent_alert
{
   std::string message () const override;

   file_index_t const index;
};
```

index
:   refers to the index of the file that completed.

# file\_renamed\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This is posted as a response to a [torrent\_handle::rename\_file()](reference-Torrent_Handle.md#rename_file()) call, if the rename
operation succeeds.

```cpp
struct file_renamed_alert final : torrent_alert
{
   std::string message () const override;
   char const* old_name () const;
   char const* new_name () const;

   static constexpr alert_category_t static_category  = alert_category::storage;
   file_index_t const index;
};
```

## new\_name() old\_name()

```cpp
char const* old_name () const;
char const* new_name () const;
```

returns the new and previous file name, respectively.

index
:   refers to the index of the file that was renamed,

# file\_rename\_failed\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This is posted as a response to a [torrent\_handle::rename\_file()](reference-Torrent_Handle.md#rename_file()) call, if the rename
operation failed.

```cpp
struct file_rename_failed_alert final : torrent_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::storage;
   file_index_t const index;
   error_code const error;
};
```

index error
:   refers to the index of the file that was supposed to be renamed,
    error is the error code returned from the filesystem.

# performance\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated when a limit is reached that might have a negative impact on
upload or download rate performance.

```cpp
struct performance_alert final : torrent_alert
{
   std::string message () const override;

   enum performance_warning_t
   {
      outstanding_disk_buffer_limit_reached,
      outstanding_request_limit_reached,
      upload_limit_too_low,
      download_limit_too_low,
      send_buffer_watermark_too_low,
      too_many_optimistic_unchoke_slots,
      too_high_disk_queue_limit,
      aio_limit_reached,
      deprecated_bittyrant_with_no_uplimit,
      too_few_outgoing_ports,
      too_few_file_descriptors,
      num_warnings,
   };

   static constexpr alert_category_t static_category  = alert_category::performance_warning;
   performance_warning_t const warning_code;
};
```

## enum performance\_warning\_t

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

| name | value | description |
| --- | --- | --- |
| outstanding\_disk\_buffer\_limit\_reached | 0 | This warning means that the number of bytes queued to be written to disk exceeds the max disk byte queue setting (settings\_pack::max\_queued\_disk\_bytes). This might restrict the download rate, by not queuing up enough write jobs to the disk I/O thread. When this [alert](reference-Alerts.md#alert) is posted, peer connections are temporarily stopped from downloading, until the queued disk bytes have fallen below the limit again. Unless your max\_queued\_disk\_bytes setting is already high, you might want to increase it to get better performance. |
| outstanding\_request\_limit\_reached | 1 | This is posted when libtorrent would like to send more requests to a peer, but it's limited by settings\_pack::max\_out\_request\_queue. The queue length libtorrent is trying to achieve is determined by the download rate and the assumed round-trip-time (settings\_pack::request\_queue\_time). The assumed round-trip-time is not limited to just the network RTT, but also the remote disk access time and message handling time. It defaults to 3 seconds. The target number of outstanding requests is set to fill the bandwidth-delay product (assumed RTT times download rate divided by number of bytes per request). When this [alert](reference-Alerts.md#alert) is posted, there is a risk that the number of outstanding requests is too low and limits the download rate. You might want to increase the max\_out\_request\_queue setting. |
| upload\_limit\_too\_low | 2 | This warning is posted when the amount of TCP/IP overhead is greater than the upload rate limit. When this happens, the TCP/IP overhead is caused by a much faster download rate, triggering TCP ACK packets. These packets eat into the rate limit specified to libtorrent. When the overhead traffic is greater than the rate limit, libtorrent will not be able to send any actual payload, such as piece requests. This means the download rate will suffer, and new requests can be sent again. There will be an equilibrium where the download rate, on average, is about 20 times the upload rate limit. If you want to maximize the download rate, increase the upload rate limit above 5% of your download capacity. |
| download\_limit\_too\_low | 3 | This is the same warning as upload\_limit\_too\_low but referring to the download limit instead of upload. This suggests that your download rate limit is much lower than your upload capacity. Your upload rate will suffer. To maximize upload rate, make sure your download rate limit is above 5% of your upload capacity. |
| send\_buffer\_watermark\_too\_low | 4 | We're stalled on the disk. We want to write to the socket, and we can write but our send buffer is empty, waiting to be refilled from the disk. This either means the disk is slower than the network connection or that our send buffer watermark is too small, because we can send it all before the disk gets back to us. The number of bytes that we keep outstanding, requested from the disk, is calculated as follows:   ```cpp min(512, max(upload_rate * send_buffer_watermark_factor / 100, send_buffer_watermark)) ```   If you receive this [alert](reference-Alerts.md#alert), you might want to either increase your send\_buffer\_watermark or send\_buffer\_watermark\_factor. |
| too\_many\_optimistic\_unchoke\_slots | 5 | If the half (or more) of all upload slots are set as optimistic unchoke slots, this warning is issued. You probably want more regular (rate based) unchoke slots. |
| too\_high\_disk\_queue\_limit | 6 | If the disk write queue ever grows larger than half of the cache size, this warning is posted. The disk write queue eats into the total disk cache and leaves very little left for the actual cache. This causes the disk cache to oscillate in evicting large portions of the cache before allowing peers to download any more, onto the disk write queue. Either lower max\_queued\_disk\_bytes or increase cache\_size. |
| aio\_limit\_reached | 7 |  |
| deprecated\_bittyrant\_with\_no\_uplimit | 8 |  |
| too\_few\_outgoing\_ports | 9 | This is generated if outgoing peer connections are failing because of *address in use* errors, indicating that settings\_pack::outgoing\_ports is set and is too small of a range. Consider not using the outgoing\_ports setting at all, or widen the range to include more ports. |
| too\_few\_file\_descriptors | 10 |  |
| num\_warnings | 11 |  |

# state\_changed\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

Generated whenever a torrent changes its state.

```cpp
struct state_changed_alert final : torrent_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::status;
   torrent_status::state_t const state;
   torrent_status::state_t const prev_state;
};
```

state
:   the new state of the torrent.

prev\_state
:   the previous state.

# tracker\_error\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated on tracker time outs, premature disconnects,
invalid response or a HTTP response other than "200 OK". From the [alert](reference-Alerts.md#alert)
you can get the handle to the torrent the tracker belongs to.

```cpp
struct tracker_error_alert final : tracker_alert
{
   std::string message () const override;
   char const* failure_reason () const;

   static constexpr alert_category_t static_category  = alert_category::tracker | alert_category::error;
   int const times_in_row;
   error_code const error;
   operation_t op;
   protocol_version version;
};
```

## failure\_reason()

```cpp
char const* failure_reason () const;
```

if the tracker sent a "failure reason" string, it will be returned
here.

times\_in\_row
:   This member says how many times in a row this tracker has failed.

error
:   the error code indicating why the tracker announce failed. If it is
    is lt::errors::tracker\_failure the [failure\_reason()](reference-Alerts.md#failure_reason()) might contain
    a more detailed description of why the tracker rejected the request.
    HTTP status codes indicating errors are also set in this field.

version
:   the bittorrent protocol version that was announced

# tracker\_warning\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is triggered if the tracker reply contains a warning field.
Usually this means that the tracker announce was successful, but the
tracker has a message to the client.

```cpp
struct tracker_warning_alert final : tracker_alert
{
   std::string message () const override;
   char const* warning_message () const;

   static constexpr alert_category_t static_category  = alert_category::tracker | alert_category::error;
   protocol_version version;
};
```

## warning\_message()

```cpp
char const* warning_message () const;
```

the message associated with this warning

version
:   the bittorrent protocol version that was announced

# scrape\_reply\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated when a scrape request succeeds.

```cpp
struct scrape_reply_alert final : tracker_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::tracker;
   int const incomplete;
   int const complete;
   protocol_version version;
};
```

incomplete complete
:   the data returned in the scrape response. These numbers
    may be -1 if the response was malformed.

version
:   the bittorrent protocol version that was scraped

# scrape\_failed\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

If a scrape request fails, this [alert](reference-Alerts.md#alert) is generated. This might be due
to the tracker timing out, refusing connection or returning an http response
code indicating an error.

```cpp
struct scrape_failed_alert final : tracker_alert
{
   std::string message () const override;
   char const* error_message () const;

   static constexpr alert_category_t static_category  = alert_category::tracker | alert_category::error;
   error_code const error;
   protocol_version version;
};
```

## error\_message()

```cpp
char const* error_message () const;
```

if the error indicates there is an associated message, this returns
that message. Otherwise and empty string.

error
:   the error itself. This may indicate that the tracker sent an error
    message (error::tracker\_failure), in which case it can be
    retrieved by calling error\_message().

version
:   the bittorrent protocol version that was scraped

# tracker\_reply\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is only for informational purpose. It is generated when a tracker announce
succeeds. It is generated regardless what kind of tracker was used, be it UDP, HTTP or
the DHT.

```cpp
struct tracker_reply_alert final : tracker_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::tracker;
   int const num_peers;
   protocol_version version;
};
```

num\_peers
:   tells how many peers the tracker returned in this response. This is
    not expected to be greater than the num\_want settings. These are not necessarily
    all new peers, some of them may already be connected.

version
:   the bittorrent protocol version that was announced

# dht\_reply\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated each time the DHT receives peers from a node. num\_peers
is the number of peers we received in this packet. Typically these packets are
received from multiple DHT nodes, and so the alerts are typically generated
a few at a time.

```cpp
struct dht_reply_alert final : tracker_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::dht | alert_category::tracker;
   int const num_peers;
};
```

# tracker\_announce\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated each time a tracker announce is sent (or attempted to be sent).
There are no extra data members in this [alert](reference-Alerts.md#alert). The url can be found in the base class
however.

```cpp
struct tracker_announce_alert final : tracker_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::tracker;
   event_t const event;
   protocol_version version;
};
```

event
:   specifies what event was sent to the tracker. See [event\_t](reference-Core.md#event_t).

version
:   the bittorrent protocol version that is announced

# hash\_failed\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated when a finished piece fails its hash check. You can get the handle
to the torrent which got the failed piece and the index of the piece itself from the [alert](reference-Alerts.md#alert).

```cpp
struct hash_failed_alert final : torrent_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::status;
   piece_index_t const piece_index;
};
```

# peer\_ban\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated when a peer is banned because it has sent too many corrupt pieces
to us. ip is the endpoint to the peer that was banned.

```cpp
struct peer_ban_alert final : peer_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::peer;
};
```

# peer\_unsnubbed\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated when a peer is un-snubbed. Essentially when it was snubbed for stalling
sending data, and now it started sending data again.

```cpp
struct peer_unsnubbed_alert final : peer_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::peer;
};
```

# peer\_snubbed\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated when a peer is snubbed, when it stops sending data when we request
it.

```cpp
struct peer_snubbed_alert final : peer_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::peer;
};
```

# peer\_error\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated when a peer sends invalid data over the peer-peer protocol. The peer
will be disconnected, but you get its ip address from the [alert](reference-Alerts.md#alert), to identify it.

```cpp
struct peer_error_alert final : peer_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::peer;
   operation_t op;
   error_code const error;
};
```

op
:   a 0-terminated string of the low-level operation that failed, or nullptr if
    there was no low level disk operation.

error
:   tells you what error caused this [alert](reference-Alerts.md#alert).

# peer\_connect\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is posted every time an incoming peer connection both
successfully passes the protocol handshake and is associated with a
torrent, or an outgoing peer connection attempt succeeds. For arbitrary
incoming connections, see [incoming\_connection\_alert](reference-Alerts.md#incoming_connection_alert).

```cpp
struct peer_connect_alert final : peer_alert
{
   std::string message () const override;

   enum direction_t
   {
      in,
      out,
   };

   static constexpr alert_category_t static_category  = alert_category::connect;
   direction_t direction;
   socket_type_t socket_type;
};
```

## enum direction\_t

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

| name | value | description |
| --- | --- | --- |
| in | 0 |  |
| out | 1 |  |

direction
:   Tells you if the peer was incoming or outgoing

# peer\_disconnected\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated when a peer is disconnected for any reason (other than the ones
covered by [peer\_error\_alert](reference-Alerts.md#peer_error_alert) ).

```cpp
struct peer_disconnected_alert final : peer_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::connect;
   socket_type_t const socket_type;
   operation_t const op;
   error_code const error;
   close_reason_t const reason;
};
```

socket\_type
:   the kind of socket this peer was connected over

op
:   the operation or level where the error occurred. Specified as an
    value from the [operation\_t](reference-Alerts.md#operation_t) enum. Defined in operations.hpp.

error
:   tells you what error caused peer to disconnect.

reason
:   the reason the peer disconnected (if specified)

# invalid\_request\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This is a debug [alert](reference-Alerts.md#alert) that is generated by an incoming invalid piece request.
ip is the address of the peer and the request is the actual incoming
request from the peer. See [peer\_request](reference-Core.md#peer_request) for more info.

```cpp
struct invalid_request_alert final : peer_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::peer;
   peer_request const request;
   bool const we_have;
   bool const peer_interested;
   bool const withheld;
};
```

request
:   the request we received from the peer

we\_have
:   true if we have this piece

peer\_interested
:   true if the peer indicated that it was interested to download before
    sending the request

withheld
:   if this is true, the peer is not allowed to download this piece because
    of super-seeding rules.

# torrent\_finished\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated when a torrent switches from being a downloader to a seed.
It will only be generated once per torrent. It contains a [torrent\_handle](reference-Torrent_Handle.md#torrent_handle) to the
torrent in question.

```cpp
struct torrent_finished_alert final : torrent_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::status;
};
```

# piece\_finished\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

this [alert](reference-Alerts.md#alert) is posted every time a piece completes downloading
and passes the hash check. This [alert](reference-Alerts.md#alert) derives from [torrent\_alert](reference-Alerts.md#torrent_alert)
which contains the [torrent\_handle](reference-Torrent_Handle.md#torrent_handle) to the torrent the piece belongs to.
Note that being downloaded and passing the hash check may happen before
the piece is also fully flushed to disk. So [torrent\_handle::have\_piece()](reference-Torrent_Handle.md#have_piece())
may still return false

```cpp
struct piece_finished_alert final : torrent_alert
{
   std::string message () const override;

   piece_index_t const piece_index;
};
```

piece\_index
:   the index of the piece that finished

# request\_dropped\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated when a peer rejects or ignores a piece request.

```cpp
struct request_dropped_alert final : peer_alert
{
   std::string message () const override;

   int const block_index;
   piece_index_t const piece_index;
};
```

# block\_timeout\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated when a block request times out.

```cpp
struct block_timeout_alert final : peer_alert
{
   std::string message () const override;

   int const block_index;
   piece_index_t const piece_index;
};
```

# block\_finished\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated when a block request receives a response.

```cpp
struct block_finished_alert final : peer_alert
{
   std::string message () const override;

   int const block_index;
   piece_index_t const piece_index;
};
```

# block\_downloading\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated when a block request is sent to a peer.

```cpp
struct block_downloading_alert final : peer_alert
{
   std::string message () const override;

   int const block_index;
   piece_index_t const piece_index;
};
```

# unwanted\_block\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated when a block is received that was not requested or
whose request timed out.

```cpp
struct unwanted_block_alert final : peer_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::peer;
   int const block_index;
   piece_index_t const piece_index;
};
```

# storage\_moved\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

The storage\_moved\_alert is generated when all the disk IO has
completed and the files have been moved, as an effect of a call to
torrent\_handle::move\_storage. This is useful to synchronize with the
actual disk. The storage\_path() member return the new path of the
storage.

```cpp
struct storage_moved_alert final : torrent_alert
{
   std::string message () const override;
   char const* storage_path () const;
   char const* old_path () const;

   static constexpr alert_category_t static_category  = alert_category::storage;
};
```

## storage\_path() old\_path()

```cpp
char const* storage_path () const;
char const* old_path () const;
```

the path the torrent was moved to and from, respectively.

# storage\_moved\_failed\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

The storage\_moved\_failed\_alert is generated when an attempt to move the storage,
via [torrent\_handle::move\_storage()](reference-Torrent_Handle.md#move_storage()), fails.

```cpp
struct storage_moved_failed_alert final : torrent_alert
{
   std::string message () const override;
   char const* file_path () const;

   static constexpr alert_category_t static_category  = alert_category::storage;
   error_code const error;
   operation_t op;
};
```

## file\_path()

```cpp
char const* file_path () const;
```

If the error happened for a specific file, this returns its path.

op
:   this indicates what underlying operation caused the error

# torrent\_deleted\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated when a request to delete the files of a torrent complete.

This [alert](reference-Alerts.md#alert) is posted in the alert\_category::storage category, and that bit
needs to be set in the alert\_mask.

```cpp
struct torrent_deleted_alert final : torrent_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::storage;
   info_hash_t info_hashes;
};
```

info\_hashes
:   The info-hash of the torrent that was just deleted. Most of
    the time the [torrent\_handle](reference-Torrent_Handle.md#torrent_handle) in the torrent\_alert will be invalid by the time
    this [alert](reference-Alerts.md#alert) arrives, since the torrent is being deleted. The info\_hashes member
    is hence the main way of identifying which torrent just completed the delete.

# torrent\_delete\_failed\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated when a request to delete the files of a torrent fails.
Just removing a torrent from the [session](reference-Session.md#session) cannot fail

```cpp
struct torrent_delete_failed_alert final : torrent_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::storage
   | alert_category::error;
   error_code const error;
   info_hash_t info_hashes;
};
```

error
:   tells you why it failed.

info\_hashes
:   the info hash of the torrent whose files failed to be deleted

# save\_resume\_data\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated as a response to a torrent\_handle::save\_resume\_data request.
It is generated once the disk IO thread is done writing the state for this torrent.

```cpp
struct save_resume_data_alert final : torrent_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::storage;
   add_torrent_params params;
};
```

params
:   the params object is populated with the torrent file whose resume
    data was saved. It is suitable to be:

    * added to a [session](reference-Session.md#session) with [add\_torrent()](reference-Session.md#add_torrent()) or [async\_add\_torrent()](reference-Session.md#async_add_torrent())
    * saved to disk with [write\_resume\_data()](reference-Resume_Data.md#write_resume_data())
    * turned into a magnet link with [make\_magnet\_uri()](reference-Core.md#make_magnet_uri())
    * saved as a .torrent file with [write\_torrent\_file()](reference-Resume_Data.md#write_torrent_file())

# save\_resume\_data\_failed\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated instead of save\_resume\_data\_alert if there was an error
generating the resume data. error describes what went wrong.

```cpp
struct save_resume_data_failed_alert final : torrent_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::storage
   | alert_category::error;
   error_code const error;
};
```

error
:   the error code from the resume\_data failure

# torrent\_paused\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated as a response to a torrent\_handle::pause request. It is
generated once all disk IO is complete and the files in the torrent have been closed.
This is useful for synchronizing with the disk.

```cpp
struct torrent_paused_alert final : torrent_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::status;
};
```

# torrent\_resumed\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated as a response to a [torrent\_handle::resume()](reference-Torrent_Handle.md#resume()) request. It is
generated when a torrent goes from a paused state to an active state.

```cpp
struct torrent_resumed_alert final : torrent_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::status;
};
```

# torrent\_checked\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is posted when a torrent completes checking. i.e. when it transitions
out of the checking files state into a state where it is ready to start downloading

```cpp
struct torrent_checked_alert final : torrent_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::status;
};
```

# url\_seed\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated when a HTTP seed name lookup fails.

```cpp
struct url_seed_alert final : torrent_alert
{
   std::string message () const override;
   char const* server_url () const;
   char const* error_message () const;

   static constexpr alert_category_t static_category  = alert_category::peer | alert_category::error;
   error_code const error;
};
```

## server\_url()

```cpp
char const* server_url () const;
```

the URL the error is associated with

## error\_message()

```cpp
char const* error_message () const;
```

in case the web server sent an error message, this function returns
it.

error
:   the error the web seed encountered. If this is not set, the server
    sent an error message, call error\_message().

# file\_error\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

If the storage fails to read or write files that it needs access to, this [alert](reference-Alerts.md#alert) is
generated and the torrent is paused.

```cpp
struct file_error_alert final : torrent_alert
{
   std::string message () const override;
   char const* filename () const;

   static constexpr alert_category_t static_category  = alert_category::status
   | alert_category::storage;
   error_code const error;
   operation_t op;
};
```

## filename()

```cpp
char const* filename () const;
```

the file that experienced the error

error
:   the error code describing the error.

op
:   indicates which underlying operation caused the error

# metadata\_failed\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated when the metadata has been completely received and the info-hash
failed to match it. i.e. the metadata that was received was corrupt. libtorrent will
automatically retry to fetch it in this case. This is only relevant when running a
torrent-less download, with the metadata extension provided by libtorrent.

```cpp
struct metadata_failed_alert final : torrent_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::error;
   error_code const error;
};
```

error
:   indicates what failed when parsing the metadata. This error is
    what's returned from lazy\_bdecode().

# metadata\_received\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated when the metadata has been completely received and the torrent
can start downloading. It is not generated on torrents that are started with metadata, but
only those that needs to download it from peers (when utilizing the libtorrent extension).

There are no additional data members in this [alert](reference-Alerts.md#alert).

Typically, when receiving this [alert](reference-Alerts.md#alert), you would want to save the torrent file in order
to load it back up again when the [session](reference-Session.md#session) is restarted. Here's an example snippet of
code to do that:

```cpp
torrent_handle h = alert->handle;
std::shared_ptr<torrent_info const> ti = h.torrent_file();
create_torrent ct(*ti);
entry te = ct.generate();
std::vector<char> buffer;
bencode(std::back_inserter(buffer), te);
FILE* f = fopen((to_hex(ti->info_hashes().get_best().to_string()) + ".torrent").c_str(), "wb+");
if (f) {
        fwrite(&buffer[0], 1, buffer.size(), f);
        fclose(f);
}
```

```cpp
struct metadata_received_alert final : torrent_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::status;
};
```

# udp\_error\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is posted when there is an error on a UDP socket. The
UDP sockets are used for all uTP, DHT and UDP tracker traffic. They are
global to the [session](reference-Session.md#session).

```cpp
struct udp_error_alert final : alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::error;
   aux::noexcept_movable<udp::endpoint> endpoint;
   operation_t operation;
   error_code const error;
};
```

endpoint
:   the source address associated with the error (if any)

operation
:   the operation that failed

error
:   the error code describing the error

# external\_ip\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

Whenever libtorrent learns about the machines external IP, this [alert](reference-Alerts.md#alert) is
generated. The external IP address can be acquired from the tracker (if it
supports that) or from peers that supports the extension protocol.
The address can be accessed through the external\_address member.

```cpp
struct external_ip_alert final : alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::status;
   aux::noexcept_movable<address> external_address;
};
```

external\_address
:   the IP address that is believed to be our external IP

# listen\_failed\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated when none of the ports, given in the port range, to
[session](reference-Session.md#session) can be opened for listening. The listen\_interface member is the
interface that failed, error is the error code describing the failure.

In the case an endpoint was created before generating the [alert](reference-Alerts.md#alert), it is
represented by address and port. The combinations of socket type
and operation in which such address and port are not valid are:
accept - i2p
accept - socks5
enum\_if - tcp

libtorrent may sometimes try to listen on port 0, if all other ports failed.
Port 0 asks the operating system to pick a port that's free). If that fails
you may see a [listen\_failed\_alert](reference-Alerts.md#listen_failed_alert) with port 0 even if you didn't ask to
listen on it.

```cpp
struct listen_failed_alert final : alert
{
   std::string message () const override;
   char const* listen_interface () const;

   static constexpr alert_category_t static_category  = alert_category::status | alert_category::error;
   error_code const error;
   operation_t op;
   lt::socket_type_t const socket_type;
   aux::noexcept_movable<lt::address> address;
   int const port;
};
```

## listen\_interface()

```cpp
char const* listen_interface () const;
```

the network device libtorrent attempted to listen on, or the IP address

error
:   the error the system returned

op
:   the underlying operation that failed

socket\_type
:   the type of listen socket this [alert](reference-Alerts.md#alert) refers to.

address
:   the address libtorrent attempted to listen on
    see [alert](reference-Alerts.md#alert) documentation for validity of this value

port
:   the port libtorrent attempted to listen on
    see [alert](reference-Alerts.md#alert) documentation for validity of this value

# listen\_succeeded\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is posted when the listen port succeeds to be opened on a
particular interface. address and port is the endpoint that
successfully was opened for listening.

```cpp
struct listen_succeeded_alert final : alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::status;
   aux::noexcept_movable<lt::address> address;
   int const port;
   lt::socket_type_t const socket_type;
};
```

address
:   the address libtorrent ended up listening on. This address
    refers to the local interface.

port
:   the port libtorrent ended up listening on.

socket\_type
:   the type of listen socket this [alert](reference-Alerts.md#alert) refers to.

# portmap\_error\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated when a NAT router was successfully found but some
part of the port mapping request failed. It contains a text message that
may help the user figure out what is wrong. This [alert](reference-Alerts.md#alert) is not generated in
case it appears the client is not running on a NAT:ed network or if it
appears there is no NAT router that can be remote controlled to add port
mappings.

```cpp
struct portmap_error_alert final : alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::port_mapping
   | alert_category::error;
   port_mapping_t const mapping;
   portmap_transport map_transport;
   aux::noexcept_movable<address> local_address;
   error_code const error;
};
```

mapping
:   refers to the mapping index of the port map that failed, i.e.
    the index returned from add\_mapping().

map\_transport
:   UPnP or NAT-PMP

local\_address
:   the local network the port mapper is running on

error
:   tells you what failed.

# portmap\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated when a NAT router was successfully found and
a port was successfully mapped on it. On a NAT:ed network with a NAT-PMP
capable router, this is typically generated once when mapping the TCP
port and, if DHT is enabled, when the UDP port is mapped.

```cpp
struct portmap_alert final : alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::port_mapping;
   port_mapping_t const mapping;
   int const external_port;
   portmap_protocol const map_protocol;
   portmap_transport const map_transport;
   aux::noexcept_movable<address> local_address;
};
```

mapping
:   refers to the mapping index of the port map that failed, i.e.
    the index returned from add\_mapping().

external\_port
:   the external port allocated for the mapping.

local\_address
:   the local network the port mapper is running on

# portmap\_log\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated to log informational events related to either
UPnP or NAT-PMP. They contain a log line and the type (0 = NAT-PMP
and 1 = UPnP). Displaying these messages to an end user is only useful
for debugging the UPnP or NAT-PMP implementation. This [alert](reference-Alerts.md#alert) is only
posted if the alert\_category::port\_mapping\_log flag is enabled in
the [alert](reference-Alerts.md#alert) mask.

```cpp
struct portmap_log_alert final : alert
{
   std::string message () const override;
   char const* log_message () const;

   static constexpr alert_category_t static_category  = alert_category::port_mapping_log;
   portmap_transport const map_transport;
   aux::noexcept_movable<address> local_address;
};
```

## log\_message()

```cpp
char const* log_message () const;
```

the message associated with this log line

local\_address
:   the local network the port mapper is running on

# fastresume\_rejected\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated when a fast resume file has been passed to
[add\_torrent()](reference-Session.md#add_torrent()) but the files on disk did not match the fast resume file.
The error\_code explains the reason why the resume file was rejected.

```cpp
struct fastresume_rejected_alert final : torrent_alert
{
   std::string message () const override;
   char const* file_path () const;

   static constexpr alert_category_t static_category  = alert_category::status
   | alert_category::error;
   error_code error;
   operation_t op;
};
```

## file\_path()

```cpp
char const* file_path () const;
```

If the error happened to a specific file, this returns the path to it.

op
:   the underlying operation that failed

# peer\_blocked\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is posted when an incoming peer connection, or a peer that's about to be added
to our peer list, is blocked for some reason. This could be any of:

* the IP filter
* i2p mixed mode restrictions (a normal peer is not allowed on an i2p swarm)
* the port filter
* the peer has a low port and no\_connect\_privileged\_ports is enabled
* the protocol of the peer is blocked (uTP/TCP blocking)

```cpp
struct peer_blocked_alert final : peer_alert
{
   std::string message () const override;

   enum reason_t
   {
      ip_filter,
      port_filter,
      i2p_mixed,
      privileged_ports,
      utp_disabled,
      tcp_disabled,
      invalid_local_interface,
      ssrf_mitigation,
   };

   static constexpr alert_category_t static_category  = alert_category::ip_block;
   int const reason;
};
```

## enum reason\_t

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

| name | value | description |
| --- | --- | --- |
| ip\_filter | 0 |  |
| port\_filter | 1 |  |
| i2p\_mixed | 2 |  |
| privileged\_ports | 3 |  |
| utp\_disabled | 4 |  |
| tcp\_disabled | 5 |  |
| invalid\_local\_interface | 6 |  |
| ssrf\_mitigation | 7 |  |

reason
:   the reason for the peer being blocked. Is one of the values from the
    [reason\_t](reference-Alerts.md#reason_t) enum.

# dht\_announce\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated when a DHT node announces to an info-hash on our
DHT node. It belongs to the alert\_category::dht category.

```cpp
struct dht_announce_alert final : alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::dht;
   aux::noexcept_movable<address> ip;
   int port;
   sha1_hash info_hash;
};
```

# dht\_get\_peers\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated when a DHT node sends a get\_peers message to
our DHT node. It belongs to the alert\_category::dht category.

```cpp
struct dht_get_peers_alert final : alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::dht;
   sha1_hash info_hash;
};
```

# cache\_flushed\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is posted when the disk cache has been flushed for a specific
torrent as a result of a call to [torrent\_handle::flush\_cache()](reference-Torrent_Handle.md#flush_cache()). This
[alert](reference-Alerts.md#alert) belongs to the alert\_category::storage category, which must be
enabled to let this [alert](reference-Alerts.md#alert) through. The [alert](reference-Alerts.md#alert) is also posted when removing
a torrent from the [session](reference-Session.md#session), once the outstanding cache flush is complete
and the torrent does no longer have any files open.

```cpp
struct cache_flushed_alert final : torrent_alert
{
   static constexpr alert_category_t static_category  = alert_category::storage;
};
```

# lsd\_peer\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated when we receive a local service discovery message
from a peer for a torrent we're currently participating in.

```cpp
struct lsd_peer_alert final : peer_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::peer;
};
```

# trackerid\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is posted whenever a tracker responds with a trackerid.
The tracker ID is like a cookie. libtorrent will store the tracker ID
for this tracker and repeat it in subsequent announces.

```cpp
struct trackerid_alert final : tracker_alert
{
   std::string message () const override;
   char const* tracker_id () const;

   static constexpr alert_category_t static_category  = alert_category::status;
};
```

## tracker\_id()

```cpp
char const* tracker_id () const;
```

The tracker ID returned by the tracker

# dht\_bootstrap\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is posted when the initial DHT bootstrap is done.

```cpp
struct dht_bootstrap_alert final : alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::dht;
};
```

# torrent\_error\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This is posted whenever a torrent is transitioned into the error state.
If the error code is duplicate\_torrent ([error\_code\_enum](reference-Error_Codes.md#error_code_enum)) error, it suggests two magnet
links ended up resolving to the same hybrid torrent. For more details,
see [BitTorrent v2 torrents](manual-ref.md#bittorrent-v2-torrents).

```cpp
struct torrent_error_alert final : torrent_alert
{
   std::string message () const override;
   char const* filename () const;

   static constexpr alert_category_t static_category  = alert_category::error | alert_category::status;
   error_code const error;
};
```

## filename()

```cpp
char const* filename () const;
```

the filename (or object) the error occurred on.

error
:   specifies which error the torrent encountered.

# torrent\_need\_cert\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This is always posted for SSL torrents. This is a reminder to the client that
the torrent won't work unless [torrent\_handle::set\_ssl\_certificate()](reference-Torrent_Handle.md#set_ssl_certificate()) is called with
a valid certificate. Valid certificates MUST be signed by the SSL certificate
in the .torrent file.

```cpp
struct torrent_need_cert_alert final : torrent_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::status;
};
```

# incoming\_connection\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

The incoming connection [alert](reference-Alerts.md#alert) is posted every time we successfully accept
an incoming connection, through any mean. The most straight-forward ways
of accepting incoming connections are through the TCP listen socket and
the UDP listen socket for uTP sockets. However, connections may also be
accepted through a Socks5 or i2p listen socket, or via an SSL listen
socket.

```cpp
struct incoming_connection_alert final : alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::peer;
   socket_type_t socket_type;
   aux::noexcept_movable<tcp::endpoint> endpoint;
};
```

socket\_type
:   tells you what kind of socket the connection was accepted

endpoint
:   is the IP address and port the connection came from.

# add\_torrent\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is always posted when a torrent was attempted to be added
and contains the return status of the add operation. The torrent handle of the new
torrent can be found as the handle member in the base class. If adding
the torrent failed, error contains the error code.

```cpp
struct add_torrent_alert final : torrent_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::status;
   add_torrent_params params;
   error_code error;
};
```

params
:   This contains copies of the most important fields from the original
    [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params) object, passed to [add\_torrent()](reference-Session.md#add_torrent()) or
    [async\_add\_torrent()](reference-Session.md#async_add_torrent()). Specifically, these fields are copied:

    * version
    * ti
    * name
    * save\_path
    * userdata
    * tracker\_id
    * flags
    * info\_hash

    the info\_hash field will be updated with the info-hash of the torrent
    specified by ti.

error
:   set to the error, if one occurred while adding the torrent.

# state\_update\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is only posted when requested by the user, by calling
session::post\_torrent\_updates() on the [session](reference-Session.md#session). It contains the torrent
status of all torrents that changed since last time this message was
posted. Its category is alert\_category::status, but it's not subject to
filtering, since it's only manually posted anyway.

```cpp
struct state_update_alert final : alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::status;
   std::vector<torrent_status> status;
};
```

status
:   contains the torrent status of all torrents that changed since last
    time this message was posted. Note that you can map a torrent status
    to a specific torrent via its handle member. The receiving end is
    suggested to have all torrents sorted by the [torrent\_handle](reference-Torrent_Handle.md#torrent_handle) or hashed
    by it, for efficient updates.

# session\_stats\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

The [session\_stats\_alert](reference-Alerts.md#session_stats_alert) is posted when the user requests [session](reference-Session.md#session) statistics by
calling [post\_session\_stats()](reference-Session.md#post_session_stats()) on the [session](reference-Session.md#session) object. This [alert](reference-Alerts.md#alert) does not
have a category, since it's only posted in response to an API call. It
is not subject to the alert\_mask filter.

the message() member function returns a string representation of the values that
properly match the line returned in session\_stats\_header\_alert::message().

this specific output is parsed by tools/parse\_session\_stats.py
if this is changed, that parser should also be changed

```cpp
struct session_stats_alert final : alert
{
   std::string message () const override;
   span<std::int64_t const> counters () const;

   static constexpr alert_category_t static_category  = {};
};
```

## counters()

```cpp
span<std::int64_t const> counters () const;
```

An array are a mix of *counters* and *gauges*, which meanings can be
queries via the [session\_stats\_metrics()](reference-Stats.md#session_stats_metrics()) function on the [session](reference-Session.md#session). The
mapping from a specific metric to an index into this array is constant
for a specific version of libtorrent, but may differ for other
versions. The intended usage is to request the mapping, i.e. call
[session\_stats\_metrics()](reference-Stats.md#session_stats_metrics()), once on startup, and then use that mapping to
interpret these values throughout the process' runtime.

For more information, see the [session statistics](manual-ref.md#session-statistics) section.

# dht\_error\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

posted when something fails in the DHT. This is not necessarily a fatal
error, but it could prevent proper operation

```cpp
struct dht_error_alert final : alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::error | alert_category::dht;
   error_code error;
   operation_t op;
};
```

error
:   the error code

op
:   the operation that failed

# dht\_immutable\_item\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

this [alert](reference-Alerts.md#alert) is posted as a response to a call to session::get\_item(),
specifically the overload for looking up immutable items in the DHT.

```cpp
struct dht_immutable_item_alert final : alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::dht;
   sha1_hash target;
   entry item;
};
```

target
:   the target hash of the immutable item. This must
    match the SHA-1 hash of the bencoded form of item.

item
:   the data for this item

# dht\_mutable\_item\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

this [alert](reference-Alerts.md#alert) is posted as a response to a call to session::get\_item(),
specifically the overload for looking up mutable items in the DHT.

```cpp
struct dht_mutable_item_alert final : alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::dht;
   std::array<char, 32> key;
   std::array<char, 64> signature;
   std::int64_t seq;
   std::string salt;
   entry item;
   bool authoritative;
};
```

key
:   the public key that was looked up

signature
:   the signature of the data. This is not the signature of the
    plain encoded form of the item, but it includes the sequence number
    and possibly the hash as well. See the dht\_store document for more
    information. This is primarily useful for echoing back in a store
    request.

seq
:   the sequence number of this item

salt
:   the salt, if any, used to lookup and store this item. If no
    salt was used, this is an empty string

item
:   the data for this item

authoritative
:   the last response for mutable data is authoritative.

# dht\_put\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

this is posted when a DHT put operation completes. This is useful if the
client is waiting for a put to complete before shutting down for instance.

```cpp
struct dht_put_alert final : alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::dht;
   sha1_hash target;
   std::array<char, 32> public_key;
   std::array<char, 64> signature;
   std::string salt;
   std::int64_t seq;
   int num_success;
};
```

target
:   the target hash the item was stored under if this was an *immutable*
    item.

public\_key signature salt seq
:   if a mutable item was stored, these are the public key, signature,
    salt and sequence number the item was stored under.

num\_success
:   DHT put operation usually writes item to k nodes, maybe the node
    is stale so no response, or the node doesn't support 'put', or the
    token for write is out of date, etc. num\_success is the number of
    successful responses we got from the puts.

# i2p\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

this [alert](reference-Alerts.md#alert) is used to report errors in the i2p SAM connection

```cpp
struct i2p_alert final : alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::error;
   error_code error;
};
```

error
:   the error that occurred in the i2p SAM connection

# dht\_outgoing\_get\_peers\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is generated when we send a get\_peers request
It belongs to the alert\_category::dht category.

```cpp
struct dht_outgoing_get_peers_alert final : alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::dht;
   sha1_hash info_hash;
   sha1_hash obfuscated_info_hash;
   aux::noexcept_movable<udp::endpoint> endpoint;
};
```

info\_hash
:   the info\_hash of the torrent we're looking for peers for.

obfuscated\_info\_hash
:   if this was an obfuscated lookup, this is the info-hash target
    actually sent to the node.

endpoint
:   the endpoint we're sending this query to

# log\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is posted by some [session](reference-Session.md#session) wide event. Its main purpose is
trouble shooting and debugging. It's not enabled by the default [alert](reference-Alerts.md#alert)
mask and is enabled by the alert\_category::session\_log bit.
Furthermore, it's by default disabled as a build configuration.

```cpp
struct log_alert final : alert
{
   std::string message () const override;
   char const* log_message () const;

   static constexpr alert_category_t static_category  = alert_category::session_log;
};
```

## log\_message()

```cpp
char const* log_message () const;
```

returns the log message

# torrent\_log\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is posted by torrent wide events. It's meant to be used for
trouble shooting and debugging. It's not enabled by the default [alert](reference-Alerts.md#alert)
mask and is enabled by the alert\_category::torrent\_log bit. By
default it is disabled as a build configuration.

```cpp
struct torrent_log_alert final : torrent_alert
{
   std::string message () const override;
   char const* log_message () const;

   static constexpr alert_category_t static_category  = alert_category::torrent_log;
};
```

## log\_message()

```cpp
char const* log_message () const;
```

returns the log message

# peer\_log\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is posted by events specific to a peer. It's meant to be used
for trouble shooting and debugging. It's not enabled by the default [alert](reference-Alerts.md#alert)
mask and is enabled by the alert\_category::peer\_log bit. By
default it is disabled as a build configuration.

```cpp
struct peer_log_alert final : peer_alert
{
   std::string message () const override;
   char const* log_message () const;

   enum direction_t
   {
      incoming_message,
      outgoing_message,
      incoming,
      outgoing,
      info,
   };

   static constexpr alert_category_t static_category  = alert_category::peer_log;
   char const* event_type;
   direction_t direction;
};
```

## log\_message()

```cpp
char const* log_message () const;
```

returns the log message

## enum direction\_t

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

| name | value | description |
| --- | --- | --- |
| incoming\_message | 0 |  |
| outgoing\_message | 1 |  |
| incoming | 2 |  |
| outgoing | 3 |  |
| info | 4 |  |

event\_type
:   string literal indicating the kind of event. For messages, this is the
    message name.

# lsd\_error\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

posted if the local service discovery socket fails to start properly.
it's categorized as alert\_category::error.

```cpp
struct lsd_error_alert final : alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::error;
   aux::noexcept_movable<address> local_address;
   error_code error;
};
```

local\_address
:   the local network the corresponding local service discovery is running
    on

error
:   The error code

# dht\_lookup

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

holds statistics about a current [dht\_lookup](reference-Alerts.md#dht_lookup) operation.
a DHT lookup is the traversal of nodes, looking up a
set of target nodes in the DHT for retrieving and possibly
storing information in the DHT

```cpp
struct dht_lookup
{
   char const* type;
   int outstanding_requests;
   int timeouts;
   int responses;
   int branch_factor;
   int nodes_left;
   int last_sent;
   int first_timeout;
   sha1_hash target;
};
```

type
:   string literal indicating which kind of lookup this is

outstanding\_requests
:   the number of outstanding request to individual nodes
    this lookup has right now

timeouts
:   the total number of requests that have timed out so far
    for this lookup

responses
:   the total number of responses we have received for this
    lookup so far for this lookup

branch\_factor
:   the branch factor for this lookup. This is the number of
    nodes we keep outstanding requests to in parallel by default.
    when nodes time out we may increase this.

nodes\_left
:   the number of nodes left that could be queries for this
    lookup. Many of these are likely to be part of the trail
    while performing the lookup and would never end up actually
    being queried.

last\_sent
:   the number of seconds ago the
    last message was sent that's still
    outstanding

first\_timeout
:   the number of outstanding requests
    that have exceeded the short timeout
    and are considered timed out in the
    sense that they increased the branch
    factor

target
:   the node-id or info-hash target for this lookup

# dht\_stats\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

contains current DHT state. Posted in response to session::post\_dht\_stats().

```cpp
struct dht_stats_alert final : alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = {};
   std::vector<dht_lookup> active_requests;
   std::vector<dht_routing_bucket> routing_table;
   sha1_hash nid;
   aux::noexcept_movable<udp::endpoint> local_endpoint;
};
```

active\_requests
:   a vector of the currently running DHT lookups.

routing\_table
:   contains information about every bucket in the DHT routing
    table.

nid
:   the node ID of the DHT node instance

local\_endpoint
:   the local socket this DHT node is running on

# incoming\_request\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

posted every time an incoming request from a peer is accepted and queued
up for being serviced. This [alert](reference-Alerts.md#alert) is only posted if
the alert\_category::incoming\_request flag is enabled in the [alert](reference-Alerts.md#alert)
mask.

```cpp
struct incoming_request_alert final : peer_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::incoming_request;
   peer_request req;
};
```

req
:   the request this peer sent to us

# dht\_log\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

debug logging of the DHT when alert\_category::dht\_log is set in the [alert](reference-Alerts.md#alert)
mask.

```cpp
struct dht_log_alert final : alert
{
   std::string message () const override;
   char const* log_message () const;

   enum dht_module_t
   {
      tracker,
      node,
      routing_table,
      rpc_manager,
      traversal,
   };

   static constexpr alert_category_t static_category  = alert_category::dht_log;
   dht_module_t module;
};
```

## log\_message()

```cpp
char const* log_message () const;
```

the log message

## enum dht\_module\_t

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

| name | value | description |
| --- | --- | --- |
| tracker | 0 |  |
| node | 1 |  |
| routing\_table | 2 |  |
| rpc\_manager | 3 |  |
| traversal | 4 |  |

module
:   the module, or part, of the DHT that produced this log message.

# dht\_pkt\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is posted every time a DHT message is sent or received. It is
only posted if the alert\_category::dht\_log [alert](reference-Alerts.md#alert) category is
enabled. It contains a verbatim copy of the message.

```cpp
struct dht_pkt_alert final : alert
{
   std::string message () const override;
   span<char const> pkt_buf () const;

   enum direction_t
   {
      incoming,
      outgoing,
   };

   static constexpr alert_category_t static_category  = alert_category::dht_log;
   direction_t direction;
   aux::noexcept_movable<udp::endpoint> node;
};
```

## pkt\_buf()

```cpp
span<char const> pkt_buf () const;
```

returns a pointer to the packet buffer and size of the packet,
respectively. This buffer is only valid for as long as the [alert](reference-Alerts.md#alert) itself
is valid, which is owned by libtorrent and reclaimed whenever
[pop\_alerts()](reference-Session.md#pop_alerts()) is called on the [session](reference-Session.md#session).

## enum direction\_t

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

| name | value | description |
| --- | --- | --- |
| incoming | 0 |  |
| outgoing | 1 |  |

direction
:   whether this is an incoming or outgoing packet.

node
:   the DHT node we received this packet from, or sent this packet to
    (depending on direction).

# dht\_get\_peers\_reply\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

Posted when we receive a response to a DHT get\_peers request.

```cpp
struct dht_get_peers_reply_alert final : alert
{
   std::string message () const override;
   int num_peers () const;
   std::vector<tcp::endpoint> peers () const;

   static constexpr alert_category_t static_category  = alert_category::dht_operation;
   sha1_hash info_hash;
};
```

# dht\_direct\_response\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This is posted exactly once for every call to session\_handle::dht\_direct\_request.
If the request failed, [response()](reference-Alerts.md#response()) will return a default constructed [bdecode\_node](reference-Bdecoding.md#bdecode_node).

```cpp
struct dht_direct_response_alert final : alert
{
   std::string message () const override;
   bdecode_node response () const;

   static constexpr alert_category_t static_category  = alert_category::dht;
   client_data_t userdata;
   aux::noexcept_movable<udp::endpoint> endpoint;
};
```

# picker\_log\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

this is posted when one or more blocks are picked by the piece picker,
assuming the verbose piece picker logging is enabled (see
alert\_category::picker\_log).

```cpp
struct picker_log_alert final : peer_alert
{
   std::string message () const override;
   std::vector<piece_block> blocks () const;

   static constexpr alert_category_t static_category  = alert_category::picker_log;
   static constexpr picker_flags_t partial_ratio  = 0_bit;
   static constexpr picker_flags_t prioritize_partials  = 1_bit;
   static constexpr picker_flags_t rarest_first_partials  = 2_bit;
   static constexpr picker_flags_t rarest_first  = 3_bit;
   static constexpr picker_flags_t reverse_rarest_first  = 4_bit;
   static constexpr picker_flags_t suggested_pieces  = 5_bit;
   static constexpr picker_flags_t prio_sequential_pieces  = 6_bit;
   static constexpr picker_flags_t sequential_pieces  = 7_bit;
   static constexpr picker_flags_t reverse_pieces  = 8_bit;
   static constexpr picker_flags_t time_critical  = 9_bit;
   static constexpr picker_flags_t random_pieces  = 10_bit;
   static constexpr picker_flags_t prefer_contiguous  = 11_bit;
   static constexpr picker_flags_t reverse_sequential  = 12_bit;
   static constexpr picker_flags_t backup1  = 13_bit;
   static constexpr picker_flags_t backup2  = 14_bit;
   static constexpr picker_flags_t end_game  = 15_bit;
   static constexpr picker_flags_t extent_affinity  = 16_bit;
   picker_flags_t const picker_flags;
};
```

picker\_flags
:   this is a bitmask of which features were enabled for this particular
    pick. The bits are defined in the picker\_flags\_t enum.

# session\_error\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

this [alert](reference-Alerts.md#alert) is posted when the [session](reference-Session.md#session) encounters a serious error,
potentially fatal

```cpp
struct session_error_alert final : alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::error;
   error_code const error;
};
```

error
:   The error code, if one is associated with this error

# dht\_live\_nodes\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

posted in response to a call to session::dht\_live\_nodes(). It contains the
live nodes from the DHT routing table of one of the DHT nodes running
locally.

```cpp
struct dht_live_nodes_alert final : alert
{
   std::string message () const override;
   std::vector<std::pair<sha1_hash, udp::endpoint>> nodes () const;
   int num_nodes () const;

   static constexpr alert_category_t static_category  = alert_category::dht;
   sha1_hash node_id;
};
```

## num\_nodes() nodes()

```cpp
std::vector<std::pair<sha1_hash, udp::endpoint>> nodes () const;
int num_nodes () const;
```

the number of nodes in the routing table and the actual nodes.

node\_id
:   the local DHT node's node-ID this routing table belongs to

# session\_stats\_header\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

The session\_stats\_header [alert](reference-Alerts.md#alert) is posted the first time
[post\_session\_stats()](reference-Session.md#post_session_stats()) is called

the message() member function returns a string representation of the
header that properly match the stats values string returned in
session\_stats\_alert::message().

this specific output is parsed by tools/parse\_session\_stats.py
if this is changed, that parser should also be changed

```cpp
struct session_stats_header_alert final : alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = {};
};
```

# dht\_sample\_infohashes\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

posted as a response to a call to session::dht\_sample\_infohashes() with
the information from the DHT response message.

```cpp
struct dht_sample_infohashes_alert final : alert
{
   std::string message () const override;
   int num_samples () const;
   std::vector<sha1_hash> samples () const;
   int num_nodes () const;
   std::vector<std::pair<sha1_hash, udp::endpoint>> nodes () const;

   static constexpr alert_category_t static_category  = alert_category::dht_operation;
   sha1_hash node_id;
   aux::noexcept_movable<udp::endpoint> endpoint;
   time_duration const interval;
   int const num_infohashes;
};
```

## num\_samples() samples()

```cpp
int num_samples () const;
std::vector<sha1_hash> samples () const;
```

returns the number of info-hashes returned by the node, as well as the
actual info-hashes. num\_samples() is more efficient than
samples().size().

## num\_nodes()

```cpp
int num_nodes () const;
```

The total number of nodes returned by nodes().

## nodes()

```cpp
std::vector<std::pair<sha1_hash, udp::endpoint>> nodes () const;
```

This is the set of more DHT nodes returned by the request.

The information is included so that indexing nodes can perform a key
space traversal with a single RPC per node by adjusting the target
value for each RPC.

node\_id
:   id of the node the request was sent to (and this response was received from)

endpoint
:   the node the request was sent to (and this response was received from)

interval
:   the interval to wait before making another request to this node

num\_infohashes
:   This field indicates how many info-hash keys are currently in the node's storage.
    If the value is larger than the number of returned samples it indicates that the
    indexer may obtain additional samples after waiting out the interval.

# block\_uploaded\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

This [alert](reference-Alerts.md#alert) is posted when a block intended to be sent to a peer is placed in the
send buffer. Note that if the connection is closed before the send buffer is sent,
the [alert](reference-Alerts.md#alert) may be posted without the bytes having been sent to the peer.
It belongs to the alert\_category::upload category.

```cpp
struct block_uploaded_alert final : peer_alert
{
   std::string message () const override;

   int const block_index;
   piece_index_t const piece_index;
};
```

# alerts\_dropped\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

this [alert](reference-Alerts.md#alert) is posted to indicate to the client that some alerts were
dropped. Dropped meaning that the [alert](reference-Alerts.md#alert) failed to be delivered to the
client. The most common cause of such failure is that the internal [alert](reference-Alerts.md#alert)
queue grew too big (controlled by alert\_queue\_size).

```cpp
struct alerts_dropped_alert final : alert
{
   static_assert (num_alert_types <= abi_alert_count, "need to increase bitset. This is an ABI break");
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::error;
   std::bitset<abi_alert_count> dropped_alerts;
};
```

dropped\_alerts
:   a bitmask indicating which alerts were dropped. Each bit represents the
    [alert](reference-Alerts.md#alert) type ID, where bit 0 represents whether any [alert](reference-Alerts.md#alert) of type 0 has
    been dropped, and so on.

# socks5\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

this [alert](reference-Alerts.md#alert) is posted with SOCKS5 related errors, when a SOCKS5 proxy is
configured. It's enabled with the alert\_category::error [alert](reference-Alerts.md#alert) category.

```cpp
struct socks5_alert final : alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::error;
   error_code error;
   operation_t op;
   aux::noexcept_movable<tcp::endpoint> ip;
};
```

error
:   the error

op
:   the operation that failed

ip
:   the endpoint configured as the proxy

# file\_prio\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

posted when a [prioritize\_files()](reference-Torrent_Handle.md#prioritize_files()) or [file\_priority()](reference-Torrent_Handle.md#file_priority()) update of the file
priorities complete, which requires a round-trip to the disk thread.

If the disk operation fails this [alert](reference-Alerts.md#alert) won't be posted, but a
[file\_error\_alert](reference-Alerts.md#file_error_alert) is posted instead, and the torrent is stopped.

```cpp
struct file_prio_alert final : torrent_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::storage;
   error_code error;
   operation_t op;
};
```

error
:   the error

op
:   the operation that failed

# oversized\_file\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

this [alert](reference-Alerts.md#alert) may be posted when the initial checking of resume data and files
on disk (just existence, not piece hashes) completes. If a file belonging
to the torrent is found on disk, but is larger than the file in the
torrent, that's when this [alert](reference-Alerts.md#alert) is posted.
the client may want to call [truncate\_files()](reference-Core.md#truncate_files()) in that case, or perhaps
interpret it as a sign that some other file is in the way, that shouldn't
be overwritten.

```cpp
struct oversized_file_alert final : torrent_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::storage;
};
```

# torrent\_conflict\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

this [alert](reference-Alerts.md#alert) is posted when two separate torrents (magnet links) resolve to
the same torrent, thus causing the same torrent being added twice. In
that case, both torrents enter an error state with duplicate\_torrent
as the error code. This [alert](reference-Alerts.md#alert) is posted containing the metadata. For more
information, see [BitTorrent v2 torrents](manual-ref.md#bittorrent-v2-torrents).
The torrent this [alert](reference-Alerts.md#alert) originated from was the one that downloaded the

metadata (i.e. the handle member from the [torrent\_alert](reference-Alerts.md#torrent_alert) base class).

```cpp
struct torrent_conflict_alert final : torrent_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::error;
   torrent_handle conflicting_torrent;
   std::shared_ptr<torrent_info> metadata;
};
```

conflicting\_torrent
:   the handle to the torrent in conflict. The swarm associated with this
    torrent handle did not download the metadata, but the downloaded
    metadata collided with this swarm's info-hash.

metadata
:   the metadata that was received by one of the torrents in conflict.
    One way to resolve the conflict is to remove both failing torrents
    and re-add it using this metadata

# peer\_info\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

posted when [torrent\_handle::post\_peer\_info()](reference-Torrent_Handle.md#post_peer_info()) is called

```cpp
struct peer_info_alert final : torrent_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::status;
   std::vector<lt::peer_info> peer_info;
};
```

peer\_info
:   the list of the currently connected peers

# file\_progress\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

posted when [torrent\_handle::post\_file\_progress()](reference-Torrent_Handle.md#post_file_progress()) is called

```cpp
struct file_progress_alert final : torrent_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::file_progress;
   aux::vector<std::int64_t, file_index_t> files;
};
```

files
:   the list of the files in the torrent

# piece\_info\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

posted when [torrent\_handle::post\_download\_queue()](reference-Torrent_Handle.md#post_download_queue()) is called

```cpp
struct piece_info_alert final : torrent_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::piece_progress;
   std::vector<partial_piece_info> piece_info;
   std::vector<block_info> block_data;
};
```

piece\_info
:   info about pieces being downloaded for the torrent

block\_data
:   storage for [block\_info](reference-Torrent_Handle.md#block_info) pointers in [partial\_piece\_info](reference-Torrent_Handle.md#partial_piece_info) objects

# piece\_availability\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

posted when [torrent\_handle::post\_piece\_availability()](reference-Torrent_Handle.md#post_piece_availability()) is called

```cpp
struct piece_availability_alert final : torrent_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::status;
   std::vector<int> piece_availability;
};
```

piece\_availability
:   info about pieces being downloaded for the torrent

# tracker\_list\_alert

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

posted when [torrent\_handle::post\_trackers()](reference-Torrent_Handle.md#post_trackers()) is called

```cpp
struct tracker_list_alert final : torrent_alert
{
   std::string message () const override;

   static constexpr alert_category_t static_category  = alert_category::status;
   std::vector<announce_entry> trackers;
};
```

trackers
:   list of trackers and their status for the torrent

# alert

Declared in "[libtorrent/alert.hpp](include/libtorrent/alert.hpp)"

The alert class is the base class that specific messages are derived from.
[alert](reference-Alerts.md#alert) types are not copyable, and cannot be constructed by the client. The
pointers returned by libtorrent are short lived (the details are described
under [session\_handle::pop\_alerts()](reference-Session.md#pop_alerts()))

```cpp
struct alert
{
   time_point timestamp () const;
   virtual int type () const noexcept = 0;
   virtual char const* what () const noexcept = 0;
   virtual std::string message () const = 0;
   virtual alert_category_t category () const noexcept = 0;

   static constexpr alert_category_t error_notification  = 0_bit;
   static constexpr alert_category_t peer_notification  = 1_bit;
   static constexpr alert_category_t port_mapping_notification  = 2_bit;
   static constexpr alert_category_t storage_notification  = 3_bit;
   static constexpr alert_category_t tracker_notification  = 4_bit;
   static constexpr alert_category_t connect_notification  = 5_bit;
   static constexpr alert_category_t status_notification  = 6_bit;
   static constexpr alert_category_t ip_block_notification  = 8_bit;
   static constexpr alert_category_t performance_warning  = 9_bit;
   static constexpr alert_category_t dht_notification  = 10_bit;
   static constexpr alert_category_t session_log_notification  = 13_bit;
   static constexpr alert_category_t torrent_log_notification  = 14_bit;
   static constexpr alert_category_t peer_log_notification  = 15_bit;
   static constexpr alert_category_t incoming_request_notification  = 16_bit;
   static constexpr alert_category_t dht_log_notification  = 17_bit;
   static constexpr alert_category_t dht_operation_notification  = 18_bit;
   static constexpr alert_category_t port_mapping_log_notification  = 19_bit;
   static constexpr alert_category_t picker_log_notification  = 20_bit;
   static constexpr alert_category_t file_progress_notification  = 21_bit;
   static constexpr alert_category_t piece_progress_notification  = 22_bit;
   static constexpr alert_category_t upload_notification  = 23_bit;
   static constexpr alert_category_t block_progress_notification  = 24_bit;
   static constexpr alert_category_t all_categories  = alert_category_t::all();
};
```

## timestamp()

```cpp
time_point timestamp () const;
```

a timestamp is automatically created in the constructor

## type()

```cpp
virtual int type () const noexcept = 0;
```

returns an integer that is unique to this [alert](reference-Alerts.md#alert) type. It can be
compared against a specific [alert](reference-Alerts.md#alert) by querying a static constant called alert\_type
in the [alert](reference-Alerts.md#alert). It can be used to determine the run-time type of an alert\* in
order to cast to that [alert](reference-Alerts.md#alert) type and access specific members.

e.g:

```cpp
std::vector<alert*> alerts;
ses.pop_alerts(&alerts);
for (alert* a : alerts) {
        switch (a->type()) {

                case read_piece_alert::alert_type:
                {
                        auto* p = static_cast<read_piece_alert*>(a);
                        if (p->ec) {
                                // read_piece failed
                                break;
                        }
                        // use p
                        break;
                }
                case file_renamed_alert::alert_type:
                {
                        // etc...
                }
        }
}
```

## what()

```cpp
virtual char const* what () const noexcept = 0;
```

returns a string literal describing the type of the [alert](reference-Alerts.md#alert). It does
not include any information that might be bundled with the [alert](reference-Alerts.md#alert).

## message()

```cpp
virtual std::string message () const = 0;
```

generate a string describing the [alert](reference-Alerts.md#alert) and the information bundled
with it. This is mainly intended for debug and development use. It is not suitable
to use this for applications that may be localized. Instead, handle each [alert](reference-Alerts.md#alert)
type individually and extract and render the information from the [alert](reference-Alerts.md#alert) depending
on the locale.

## category()

```cpp
virtual alert_category_t category () const noexcept = 0;
```

returns a bitmask specifying which categories this [alert](reference-Alerts.md#alert) belong to.

# alert\_cast()

Declared in "[libtorrent/alert.hpp](include/libtorrent/alert.hpp)"

```cpp
template <typename T> T* alert_cast (alert* a);
template <typename T> T const* alert_cast (alert const* a);
```

When you get an [alert](reference-Alerts.md#alert), you can use alert\_cast<> to attempt to cast the
pointer to a specific [alert](reference-Alerts.md#alert) type, in order to query it for more
information.

Note

alert\_cast<> can only cast to an exact [alert](reference-Alerts.md#alert) type, not a base class

# operation\_name()

Declared in "[libtorrent/operations.hpp](include/libtorrent/operations.hpp)"

```cpp
char const* operation_name (operation_t op);
```

maps an operation id (from [peer\_error\_alert](reference-Alerts.md#peer_error_alert) and [peer\_disconnected\_alert](reference-Alerts.md#peer_disconnected_alert))
to its name. See [operation\_t](reference-Alerts.md#operation_t) for the constants

# enum operation\_t

Declared in "[libtorrent/operations.hpp](include/libtorrent/operations.hpp)"

| name | value | description |
| --- | --- | --- |
| unknown | 0 | the error was unexpected and it is unknown which operation caused it |
| bittorrent | 1 | this is used when the bittorrent logic determines to disconnect |
| iocontrol | 2 | a call to iocontrol failed |
| getpeername | 3 | a call to getpeername() failed (querying the remote IP of a connection) |
| getname | 4 | a call to getname failed (querying the local IP of a connection) |
| alloc\_recvbuf | 5 | an attempt to allocate a receive buffer failed |
| alloc\_sndbuf | 6 | an attempt to allocate a send buffer failed |
| file\_write | 7 | writing to a file failed |
| file\_read | 8 | reading from a file failed |
| file | 9 | a non-read and non-write file operation failed |
| sock\_write | 10 | a socket write operation failed |
| sock\_read | 11 | a socket read operation failed |
| sock\_open | 12 | a call to open(), to create a socket socket failed |
| sock\_bind | 13 | a call to bind() on a socket failed |
| available | 14 | an attempt to query the number of bytes available to read from a socket failed |
| encryption | 15 | a call related to bittorrent protocol encryption failed |
| connect | 16 | an attempt to connect a socket failed |
| ssl\_handshake | 17 | establishing an SSL connection failed |
| get\_interface | 18 | a connection failed to satisfy the bind interface setting |
| sock\_listen | 19 | a call to listen() on a socket |
| sock\_bind\_to\_device | 20 | a call to the ioctl to bind a socket to a specific network device or adapter |
| sock\_accept | 21 | a call to accept() on a socket |
| parse\_address | 22 | convert a string into a valid network address |
| enum\_if | 23 | enumeration network devices or adapters |
| file\_stat | 24 | invoking stat() on a file |
| file\_copy | 25 | copying a file |
| file\_fallocate | 26 | allocating storage for a file |
| file\_hard\_link | 27 | creating a hard link |
| file\_remove | 28 | removing a file |
| file\_rename | 29 | renaming a file |
| file\_open | 30 | opening a file |
| mkdir | 31 | creating a directory |
| check\_resume | 32 | check fast resume data against files on disk |
| exception | 33 | an unknown exception |
| alloc\_cache\_piece | 34 | allocate space for a piece in the cache |
| partfile\_move | 35 | move a part-file |
| partfile\_read | 36 | read from a part file |
| partfile\_write | 37 | write to a part-file |
| hostname\_lookup | 38 | a hostname lookup |
| symlink | 39 | create or read a symlink |
| handshake | 40 | handshake with a peer or server |
| sock\_option | 41 | set socket option |
| enum\_route | 42 | enumeration of network routes |
| file\_seek | 43 | moving read/write position in a file, [operation\_t::hostname\_lookup](reference-Alerts.md#hostname_lookup) |
| timer | 44 | an async wait operation on a timer |
| file\_mmap | 45 | call to mmap() (or windows counterpart) |
| file\_truncate | 46 | call to ftruncate() (or SetEndOfFile() on windows) |

# int

Declared in "[libtorrent/alert\_types.hpp](include/libtorrent/alert_types.hpp)"

user\_alert\_id
:   user defined alerts should use IDs greater than this

num\_alert\_types
:   this constant represents "max\_alert\_index" + 1

# alert\_category\_t

Declared in "[libtorrent/alert.hpp](include/libtorrent/alert.hpp)"

error
:   Enables alerts that report an error. This includes:

    * tracker errors
    * tracker warnings
    * file errors
    * resume data failures
    * web seed errors
    * .torrent files errors
    * listen socket errors
    * port mapping errors

peer
:   Enables alerts when peers send invalid requests, get banned or
    snubbed.

port\_mapping
:   Enables alerts for port mapping events. For NAT-PMP and UPnP.

storage
:   Enables alerts for events related to the storage. File errors and
    synchronization events for moving the storage, renaming files etc.

tracker
:   Enables all tracker events. Includes announcing to trackers,
    receiving responses, warnings and errors.

connect
:   Low level alerts for when peers are connected and disconnected.

status
:   Enables alerts for when a torrent or the [session](reference-Session.md#session) changes state.

ip\_block
:   Alerts when a peer is blocked by the ip blocker or port blocker.

performance\_warning
:   Alerts when some limit is reached that might limit the download
    or upload rate.

dht
:   Alerts on events in the DHT node. For incoming searches or
    bootstrapping being done etc.

stats
:   If you enable these alerts, you will receive a stats\_alert
    approximately once every second, for every active torrent.
    These alerts contain all statistics [counters](reference-Stats.md#counters) for the interval since
    the lasts stats [alert](reference-Alerts.md#alert).

session\_log
:   Enables debug logging alerts. These are available unless libtorrent
    was built with logging disabled (TORRENT\_DISABLE\_LOGGING). The
    alerts being posted are [log\_alert](reference-Alerts.md#log_alert) and are [session](reference-Session.md#session) wide.

torrent\_log
:   Enables debug logging alerts for torrents. These are available
    unless libtorrent was built with logging disabled
    (TORRENT\_DISABLE\_LOGGING). The alerts being posted are
    [torrent\_log\_alert](reference-Alerts.md#torrent_log_alert) and are torrent wide debug events.

peer\_log
:   Enables debug logging alerts for peers. These are available unless
    libtorrent was built with logging disabled
    (TORRENT\_DISABLE\_LOGGING). The alerts being posted are
    [peer\_log\_alert](reference-Alerts.md#peer_log_alert) and low-level peer events and messages.

incoming\_request
:   enables the [incoming\_request\_alert](reference-Alerts.md#incoming_request_alert).

dht\_log
:   enables [dht\_log\_alert](reference-Alerts.md#dht_log_alert), debug logging for the DHT

dht\_operation
:   enable events from pure dht operations not related to torrents

port\_mapping\_log
:   enables port mapping log events. This log is useful
    for debugging the UPnP or NAT-PMP implementation

picker\_log
:   enables verbose logging from the piece picker.

file\_progress
:   alerts when files complete downloading

piece\_progress
:   alerts when pieces complete downloading or fail hash check

upload
:   alerts when we upload blocks to other peers

block\_progress
:   alerts on individual blocks being requested, downloading, finished,
    rejected, time-out and cancelled. This is likely to post alerts at a
    high rate.

all
:   The full bitmask, representing all available categories.

    since the enum is signed, make sure this isn't
    interpreted as -1. For instance, boost.python
    does that and fails when assigning it to an
    unsigned parameter.
