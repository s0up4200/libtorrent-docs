---
title: "Session"
source: "https://libtorrent.org/reference-Session.html"
---

# session\_proxy

Declared in "[libtorrent/session.hpp](include/libtorrent/session.hpp)"

this is a holder for the internal [session](reference-Session.md#session) implementation object. Once the
[session](reference-Session.md#session) destruction is explicitly initiated, this holder is used to
synchronize the completion of the shutdown. The lifetime of this object
may outlive [session](reference-Session.md#session), causing the [session](reference-Session.md#session) destructor to not block. The
[session\_proxy](reference-Session.md#session_proxy) destructor will block however, until the underlying [session](reference-Session.md#session)
is done shutting down.

```cpp
struct session_proxy
{
   session_proxy& operator= (session_proxy const&) &;
   session_proxy ();
   ~session_proxy ();
   session_proxy (session_proxy const&);
   session_proxy& operator= (session_proxy&&) & noexcept;
   session_proxy (session_proxy&&) noexcept;
};
```

## ~session\_proxy() operator=() session\_proxy()

```cpp
session_proxy& operator= (session_proxy const&) &;
session_proxy ();
~session_proxy ();
session_proxy (session_proxy const&);
session_proxy& operator= (session_proxy&&) & noexcept;
session_proxy (session_proxy&&) noexcept;
```

default constructor, does not refer to any [session](reference-Session.md#session)
implementation object.

# session

Declared in "[libtorrent/session.hpp](include/libtorrent/session.hpp)"

The [session](reference-Session.md#session) holds all state that spans multiple torrents. Among other
things it runs the network loop and manages all torrents. Once it's
created, the [session](reference-Session.md#session) object will spawn the main thread that will do all
the work. The main thread will be idle as long it doesn't have any
torrents to participate in.

You have some control over [session](reference-Session.md#session) configuration through the
session\_handle::apply\_settings() member function. To change one or more
configuration options, create a [settings\_pack](reference-Settings.md#settings_pack). object and fill it with
the settings to be set and pass it in to session::apply\_settings().

see [apply\_settings()](reference-Session.md#apply_settings()).

```cpp
struct session : session_handle
{
   session (session_params&& params, session_flags_t flags);
   session ();
   session (session_params const& params, session_flags_t flags);
   explicit session (session_params&& params);
   explicit session (session_params const& params);
   session (session_params const& params, io_context& ios, session_flags_t);
   session (session_params&& params, io_context& ios);
   session (session_params const& params, io_context& ios);
   session (session_params&& params, io_context& ios, session_flags_t);
   ~session ();
   session_proxy abort ();
};
```

## session()

```cpp
session (session_params&& params, session_flags_t flags);
session ();
session (session_params const& params, session_flags_t flags);
explicit session (session_params&& params);
explicit session (session_params const& params);
```

Constructs the [session](reference-Session.md#session) objects which acts as the container of torrents.
In order to avoid a race condition between starting the [session](reference-Session.md#session) and
configuring it, you can pass in a [session\_params](reference-Session.md#session_params) object. Its settings
will take effect before the [session](reference-Session.md#session) starts up.

The overloads taking flags can be used to start a [session](reference-Session.md#session) in
paused mode (by passing in session::paused). Note that
add\_default\_plugins do not have an affect on constructors that
take a [session\_params](reference-Session.md#session_params) object. It already contains the plugins to use.

## session()

```cpp
session (session_params const& params, io_context& ios, session_flags_t);
session (session_params&& params, io_context& ios);
session (session_params const& params, io_context& ios);
session (session_params&& params, io_context& ios, session_flags_t);
```

Overload of the constructor that takes an external io\_context to run
the [session](reference-Session.md#session) object on. This is primarily useful for tests that may want
to run multiple sessions on a single io\_context, or low resource
systems where additional threads are expensive and sharing an
io\_context with other events is fine.

Warning

The [session](reference-Session.md#session) object does not cleanly terminate with an external
io\_context. The io\_context::run() call *must* have returned
before it's safe to destruct the [session](reference-Session.md#session). Which means you *MUST*
call [session::abort()](reference-Session.md#abort()) and save the [session\_proxy](reference-Session.md#session_proxy) first, then
destruct the [session](reference-Session.md#session) object, then sync with the io\_context, then
destruct the [session\_proxy](reference-Session.md#session_proxy) object.

## ~session()

```cpp
~session ();
```

The destructor of [session](reference-Session.md#session) will notify all trackers that our torrents
have been shut down. If some trackers are down, they will time out.
All this before the destructor of [session](reference-Session.md#session) returns. So, it's advised
that any kind of interface (such as windows) are closed before
destructing the [session](reference-Session.md#session) object. Because it can take a few second for
it to finish. The timeout can be set with [apply\_settings()](reference-Session.md#apply_settings()).

## abort()

```cpp
session_proxy abort ();
```

In case you want to destruct the [session](reference-Session.md#session) asynchronously, you can
request a [session](reference-Session.md#session) destruction proxy. If you don't do this, the
destructor of the [session](reference-Session.md#session) object will block while the trackers are
contacted. If you keep one session\_proxy to the [session](reference-Session.md#session) when
destructing it, the destructor will not block, but start to close down
the [session](reference-Session.md#session), the destructor of the proxy will then synchronize the
threads. So, the destruction of the [session](reference-Session.md#session) is performed from the
session destructor call until the session\_proxy destructor
call. The session\_proxy does not have any operations on it (since
the [session](reference-Session.md#session) is being closed down, no operations are allowed on it).
The only valid operation is calling the destructor:

```cpp
struct session_proxy {};
```

# session\_params

Declared in "[libtorrent/session\_params.hpp](include/libtorrent/session_params.hpp)"

The [session\_params](reference-Session.md#session_params) is a parameters pack for configuring the [session](reference-Session.md#session)
before it's started.

```cpp
struct session_params
{
   session_params (settings_pack&& sp);
   session_params (settings_pack const& sp);
   session_params ();
   session_params (settings_pack const& sp
      , std::vector<std::shared_ptr<plugin>> exts);
   session_params (settings_pack&& sp
      , std::vector<std::shared_ptr<plugin>> exts);

   settings_pack settings;
   std::vector<std::shared_ptr<plugin>> extensions;
   dht::dht_state dht_state;
   dht::dht_storage_constructor_type dht_storage_constructor;
   disk_io_constructor_type disk_io_constructor;
   std::map<std::string, std::string> ext_state;
   libtorrent::ip_filter ip_filter;
};
```

## session\_params()

```cpp
session_params (settings_pack&& sp);
session_params (settings_pack const& sp);
session_params ();
```

This constructor can be used to start with the default plugins
(ut\_metadata, ut\_pex and smart\_ban). Pass a [settings\_pack](reference-Settings.md#settings_pack) to set the
initial settings when the [session](reference-Session.md#session) starts.

## session\_params()

```cpp
session_params (settings_pack const& sp
      , std::vector<std::shared_ptr<plugin>> exts);
session_params (settings_pack&& sp
      , std::vector<std::shared_ptr<plugin>> exts);
```

This constructor helps to configure the set of initial plugins
to be added to the [session](reference-Session.md#session) before it's started.

settings
:   The settings to configure the [session](reference-Session.md#session) with

extensions
:   the plugins to add to the [session](reference-Session.md#session) as it is constructed

dht\_state
:   DHT node ID and node addresses to bootstrap the DHT with.

dht\_storage\_constructor
:   function object to construct the storage object for DHT items.

disk\_io\_constructor
:   function object to create the disk I/O subsystem. Defaults to
    default\_disk\_io\_constructor.

ext\_state
:   this container can be used by extensions/plugins to store settings. It's
    primarily here to make it convenient to save and restore state across
    sessions, using [read\_session\_params()](reference-Session.md#read_session_params()) and [write\_session\_params()](reference-Session.md#write_session_params()).

ip\_filter
:   the IP filter to use for the [session](reference-Session.md#session). This restricts which peers are allowed
    to connect. As if passed to [set\_ip\_filter()](reference-Session.md#set_ip_filter()).

# session\_handle

Declared in "[libtorrent/session\_handle.hpp](include/libtorrent/session_handle.hpp)"

this class provides a non-owning handle to a [session](reference-Session.md#session) and a subset of the
interface of the [session](reference-Session.md#session) class. If the underlying [session](reference-Session.md#session) is destructed
any handle to it will no longer be valid. [is\_valid()](reference-Torrent_Info.md#is_valid()) will return false and
any operation on it will throw a system\_error exception, with error code
invalid\_session\_handle.

```cpp
struct session_handle
{
   bool is_valid () const;
   session_params session_state (save_state_flags_t flags = save_state_flags_t::all()) const;
   std::vector<torrent_status> get_torrent_status (
      std::function<bool(torrent_status const&)> const& pred
      , status_flags_t flags = {}) const;
   void refresh_torrent_status (std::vector<torrent_status>* ret
      , status_flags_t flags = {}) const;
   void post_torrent_updates (status_flags_t flags = status_flags_t::all());
   void post_session_stats ();
   void post_dht_stats ();
   void set_dht_state (dht::dht_state const& st);
   void set_dht_state (dht::dht_state&& st);
   std::vector<torrent_handle> get_torrents () const;
   torrent_handle find_torrent (sha1_hash const& info_hash) const;
   void async_add_torrent (add_torrent_params const& params);
   void async_add_torrent (add_torrent_params&& params);
   torrent_handle add_torrent (add_torrent_params&& params, error_code& ec);
   torrent_handle add_torrent (add_torrent_params const& params);
   torrent_handle add_torrent (add_torrent_params const& params, error_code& ec);
   torrent_handle add_torrent (add_torrent_params&& params);
   void pause ();
   bool is_paused () const;
   void resume ();
   bool is_dht_running () const;
   void set_dht_storage (dht::dht_storage_constructor_type sc);
   void add_dht_node (std::pair<std::string, int> const& node);
   void dht_get_item (sha1_hash const& target);
   void dht_get_item (std::array<char, 32> key
      , std::string salt = std::string());
   sha1_hash dht_put_item (entry data);
   void dht_put_item (std::array<char, 32> key
      , std::function<void(entry&, std::array<char, 64>&
      , std::int64_t&, std::string const&)> cb
      , std::string salt = std::string());
   void dht_get_peers (sha1_hash const& info_hash);
   void dht_announce (sha1_hash const& info_hash, int port = 0, dht::announce_flags_t flags = {});
   void dht_live_nodes (sha1_hash const& nid);
   void dht_sample_infohashes (udp::endpoint const& ep, sha1_hash const& target);
   void dht_direct_request (udp::endpoint const& ep, entry const& e, client_data_t userdata = {});
   void add_extension (std::shared_ptr<plugin> ext);
   void add_extension (std::function<std::shared_ptr<torrent_plugin>(
      torrent_handle const&, client_data_t)> ext);
   void set_ip_filter (ip_filter f);
   ip_filter get_ip_filter () const;
   void set_port_filter (port_filter const& f);
   bool is_listening () const;
   unsigned short listen_port () const;
   unsigned short ssl_listen_port () const;
   ip_filter get_peer_class_filter () const;
   void set_peer_class_filter (ip_filter const& f);
   peer_class_type_filter get_peer_class_type_filter () const;
   void set_peer_class_type_filter (peer_class_type_filter const& f);
   peer_class_t create_peer_class (char const* name);
   void delete_peer_class (peer_class_t cid);
   void set_peer_class (peer_class_t cid, peer_class_info const& pci);
   peer_class_info get_peer_class (peer_class_t cid) const;
   void remove_torrent (const torrent_handle&, remove_flags_t = {});
   void apply_settings (settings_pack const&);
   settings_pack get_settings () const;
   void apply_settings (settings_pack&&);
   void set_alert_notify (std::function<void()> const& fun);
   alert* wait_for_alert (time_duration max_wait);
   void pop_alerts (std::vector<alert*>* alerts);
   void delete_port_mapping (port_mapping_t handle);
   std::vector<port_mapping_t> add_port_mapping (portmap_protocol t, int external_port, int local_port);
   void reopen_network_sockets (reopen_network_flags_t options = reopen_map_ports);
   std::shared_ptr<aux::session_impl> native_handle () const;

   static constexpr save_state_flags_t save_settings  = 0_bit;
   static constexpr save_state_flags_t save_dht_state  = 2_bit;
   static constexpr save_state_flags_t save_extension_state  = 11_bit;
   static constexpr save_state_flags_t save_ip_filter  = 12_bit;
   static constexpr peer_class_t global_peer_class_id {0};
   static constexpr peer_class_t tcp_peer_class_id {1};
   static constexpr peer_class_t local_peer_class_id {2};
   static constexpr remove_flags_t delete_files  = 0_bit;
   static constexpr remove_flags_t delete_partfile  = 1_bit;
   static constexpr session_flags_t paused  = 2_bit;
   static constexpr portmap_protocol udp  = portmap_protocol::udp;
   static constexpr portmap_protocol tcp  = portmap_protocol::tcp;
   static constexpr reopen_network_flags_t reopen_map_ports  = 0_bit;
};
```

## is\_valid()

```cpp
bool is_valid () const;
```

returns true if this handle refers to a valid [session](reference-Session.md#session) object. If the
[session](reference-Session.md#session) has been destroyed, all [session\_handle](reference-Session.md#session_handle) objects will expire and
not be valid.

## session\_state()

```cpp
session_params session_state (save_state_flags_t flags = save_state_flags_t::all()) const;
```

returns the current [session](reference-Session.md#session) state. This can be passed to
[write\_session\_params()](reference-Session.md#write_session_params()) to save the state to disk and restored using
[read\_session\_params()](reference-Session.md#read_session_params()) when constructing a new [session](reference-Session.md#session). The kind of
state that's included is all settings, the DHT routing table, possibly
plugin-specific state.
the flags parameter can be used to only save certain parts of the
[session](reference-Session.md#session) state

## refresh\_torrent\_status() get\_torrent\_status()

```cpp
std::vector<torrent_status> get_torrent_status (
      std::function<bool(torrent_status const&)> const& pred
      , status_flags_t flags = {}) const;
void refresh_torrent_status (std::vector<torrent_status>* ret
      , status_flags_t flags = {}) const;
```

Note

these calls are potentially expensive and won't scale well with
lots of torrents. If you're concerned about performance, consider
using post\_torrent\_updates() instead.

get\_torrent\_status returns a vector of the [torrent\_status](reference-Torrent_Status.md#torrent_status) for
every torrent which satisfies pred, which is a predicate function
which determines if a torrent should be included in the returned set
or not. Returning true means it should be included and false means
excluded. The flags argument is the same as to
[torrent\_handle::status()](reference-Torrent_Handle.md#status()). Since pred is guaranteed to be
called for every torrent, it may be used to count the number of
torrents of different categories as well.

refresh\_torrent\_status takes a vector of [torrent\_status](reference-Torrent_Status.md#torrent_status) structs
(for instance the same vector that was returned by
[get\_torrent\_status()](reference-Session.md#get_torrent_status()) ) and refreshes the status based on the
handle member. It is possible to use this function by first
setting up a vector of default constructed torrent\_status objects,
only initializing the handle member, in order to request the
torrent status for multiple torrents in a single call. This can save a
significant amount of time if you have a lot of torrents.

Any [torrent\_status](reference-Torrent_Status.md#torrent_status) object whose handle member is not referring to
a valid torrent are ignored.

The intended use of these functions is to start off by calling
get\_torrent\_status() to get a list of all torrents that match your
criteria. Then call refresh\_torrent\_status() on that list. This
will only refresh the status for the torrents in your list, and thus
ignore all other torrents you might be running. This may save a
significant amount of time, especially if the number of torrents you're
interested in is small. In order to keep your list of interested
torrents up to date, you can either call get\_torrent\_status() from
time to time, to include torrents you might have become interested in
since the last time. In order to stop refreshing a certain torrent,
simply remove it from the list.

## post\_torrent\_updates()

```cpp
void post_torrent_updates (status_flags_t flags = status_flags_t::all());
```

This functions instructs the [session](reference-Session.md#session) to post the [state\_update\_alert](reference-Alerts.md#state_update_alert),
containing the status of all torrents whose state changed since the
last time this function was called.

Only torrents who has the state subscription flag set will be
included. This flag is on by default. See [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params).
the flags argument is the same as for [torrent\_handle::status()](reference-Torrent_Handle.md#status()).
see status\_flags\_t in [torrent\_handle](reference-Torrent_Handle.md#torrent_handle).

## post\_session\_stats()

```cpp
void post_session_stats ();
```

This function will post a [session\_stats\_alert](reference-Alerts.md#session_stats_alert) object, containing a
snapshot of the performance [counters](reference-Stats.md#counters) from the internals of libtorrent.
To interpret these [counters](reference-Stats.md#counters), query the [session](reference-Session.md#session) via
[session\_stats\_metrics()](reference-Stats.md#session_stats_metrics()).

For more information, see the [session statistics](manual-ref.md#session-statistics) section.

## post\_dht\_stats()

```cpp
void post_dht_stats ();
```

This will cause a [dht\_stats\_alert](reference-Alerts.md#dht_stats_alert) to be posted.

## set\_dht\_state()

```cpp
void set_dht_state (dht::dht_state const& st);
void set_dht_state (dht::dht_state&& st);
```

set the DHT state for the [session](reference-Session.md#session). This will be taken into account the
next time the DHT is started, as if it had been passed in via the
[session\_params](reference-Session.md#session_params) on startup.

## get\_torrents() find\_torrent()

```cpp
std::vector<torrent_handle> get_torrents () const;
torrent_handle find_torrent (sha1_hash const& info_hash) const;
```

find\_torrent() looks for a torrent with the given info-hash. In
case there is such a torrent in the [session](reference-Session.md#session), a [torrent\_handle](reference-Torrent_Handle.md#torrent_handle) to that
torrent is returned. In case the torrent cannot be found, an invalid
[torrent\_handle](reference-Torrent_Handle.md#torrent_handle) is returned.

See torrent\_handle::is\_valid() to know if the torrent was found or
not.

get\_torrents() returns a vector of torrent\_handles to all the
torrents currently in the [session](reference-Session.md#session).

## add\_torrent() async\_add\_torrent()

```cpp
void async_add_torrent (add_torrent_params const& params);
void async_add_torrent (add_torrent_params&& params);
torrent_handle add_torrent (add_torrent_params&& params, error_code& ec);
torrent_handle add_torrent (add_torrent_params const& params);
torrent_handle add_torrent (add_torrent_params const& params, error_code& ec);
torrent_handle add_torrent (add_torrent_params&& params);
```

You add torrents through the [add\_torrent()](reference-Session.md#add_torrent()) function where you give an
object with all the parameters. The [add\_torrent()](reference-Session.md#add_torrent()) overloads will block
until the torrent has been added (or failed to be added) and returns
an error code and a [torrent\_handle](reference-Torrent_Handle.md#torrent_handle). In order to add torrents more
efficiently, consider using [async\_add\_torrent()](reference-Session.md#async_add_torrent()) which returns
immediately, without waiting for the torrent to add. Notification of
the torrent being added is sent as [add\_torrent\_alert](reference-Alerts.md#add_torrent_alert).

The save\_path field in [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params) must be set to a valid
path where the files for the torrent will be saved. Even when using a
custom storage, this needs to be set to something. If the save\_path
is empty, the call to [add\_torrent()](reference-Session.md#add_torrent()) will throw a system\_error
exception.

The overload that does not take an error\_code throws an exception on
error and is not available when building without exception support.
The [torrent\_handle](reference-Torrent_Handle.md#torrent_handle) returned by [add\_torrent()](reference-Session.md#add_torrent()) can be used to retrieve
information about the torrent's progress, its peers etc. It is also
used to abort a torrent.

If the torrent you are trying to add already exists in the [session](reference-Session.md#session) (is
either queued for checking, being checked or downloading)
add\_torrent() will throw system\_error which derives from
std::exception unless duplicate\_is\_error is set to false. In that
case, [add\_torrent()](reference-Session.md#add_torrent()) will return the handle to the existing torrent.

The [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params) class has a flags field. It can be used to
control what state the new torrent will be added in. Common flags to
want to control are torrent\_flags::paused and
torrent\_flags::auto\_managed. In order to add a magnet link that will
just download the metadata, but no payload, set the
torrent\_flags::upload\_mode flag.

Special consideration has to be taken when adding hybrid torrents
(i.e. torrents that are BitTorrent v2 torrents that are backwards
compatible with v1). For more details, see [BitTorrent v2 torrents](manual-ref.md#bittorrent-v2-torrents).

## resume() pause() is\_paused()

```cpp
void pause ();
bool is_paused () const;
void resume ();
```

Pausing the [session](reference-Session.md#session) has the same effect as pausing every torrent in
it, except that torrents will not be resumed by the auto-manage
mechanism. Resuming will restore the torrents to their previous paused
state. i.e. the [session](reference-Session.md#session) pause state is separate from the torrent pause
state. A torrent is inactive if it is paused or if the [session](reference-Session.md#session) is
paused.

## is\_dht\_running()

```cpp
bool is_dht_running () const;
```

is\_dht\_running() returns true if the DHT support has been started
and false otherwise.

## set\_dht\_storage()

```cpp
void set_dht_storage (dht::dht_storage_constructor_type sc);
```

set\_dht\_storage set a dht custom storage constructor function
to be used internally when the dht is created.

Since the dht storage is a critical component for the dht behavior,
this function will only be effective the next time the dht is started.
If you never touch this feature, a default map-memory based storage
is used.

If you want to make sure the dht is initially created with your
custom storage, create a [session](reference-Session.md#session) with the setting
settings\_pack::enable\_dht to false, set your constructor function
and call apply\_settings with settings\_pack::enable\_dht to true.

## add\_dht\_node()

```cpp
void add_dht_node (std::pair<std::string, int> const& node);
```

add\_dht\_node takes a host name and port pair. That endpoint will be
pinged, and if a valid DHT reply is received, the node will be added to
the routing table.

## dht\_get\_item()

```cpp
void dht_get_item (sha1_hash const& target);
```

query the DHT for an immutable item at the target hash.
the result is posted as a [dht\_immutable\_item\_alert](reference-Alerts.md#dht_immutable_item_alert).

## dht\_get\_item()

```cpp
void dht_get_item (std::array<char, 32> key
      , std::string salt = std::string());
```

query the DHT for a mutable item under the public key key.
this is an ed25519 key. salt is optional and may be left
as an empty string if no salt is to be used.
if the item is found in the DHT, a [dht\_mutable\_item\_alert](reference-Alerts.md#dht_mutable_item_alert) is
posted.

## dht\_put\_item()

```cpp
sha1_hash dht_put_item (entry data);
```

store the given bencoded data as an immutable item in the DHT.
the returned hash is the key that is to be used to look the item
up again. It's just the SHA-1 hash of the bencoded form of the
structure.

## dht\_put\_item()

```cpp
void dht_put_item (std::array<char, 32> key
      , std::function<void(entry&, std::array<char, 64>&
      , std::int64_t&, std::string const&)> cb
      , std::string salt = std::string());
```

store a mutable item. The key is the public key the blob is
to be stored under. The optional salt argument is a string that
is to be mixed in with the key when determining where in the DHT
the value is to be stored. The callback function is called from within
the libtorrent network thread once we've found where to store the blob,
possibly with the current value stored under the key.
The values passed to the callback functions are:

entry& value
:   the current value stored under the key (may be empty). Also expected
    to be set to the value to be stored by the function.

std::array<char,64>& signature
:   the signature authenticating the current value. This may be zeros
    if there is currently no value stored. The function is expected to
    fill in this buffer with the signature of the new value to store.
    To generate the signature, you may want to use the
    sign\_mutable\_item function.

std::int64\_t& seq
:   current sequence number. May be zero if there is no current value.
    The function is expected to set this to the new sequence number of
    the value that is to be stored. Sequence numbers must be monotonically
    increasing. Attempting to overwrite a value with a lower or equal
    sequence number will fail, even if the signature is correct.

std::string const& salt
:   this is the salt that was used for this put call.

Since the callback function cb is called from within libtorrent,
it is critical to not perform any blocking operations. Ideally not
even locking a mutex. Pass any data required for this function along
with the function object's context and make the function entirely
self-contained. The only reason data blob's value is computed
via a function instead of just passing in the new value is to avoid
race conditions. If you want to *update* the value in the DHT, you
must first retrieve it, then modify it, then write it back. The way
the DHT works, it is natural to always do a lookup before storing and
calling the callback in between is convenient.

## dht\_get\_peers() dht\_announce()

```cpp
void dht_get_peers (sha1_hash const& info_hash);
void dht_announce (sha1_hash const& info_hash, int port = 0, dht::announce_flags_t flags = {});
```

dht\_get\_peers() will issue a DHT get\_peer request to the DHT for the
specified info-hash. The response (the peers) will be posted back in a
[dht\_get\_peers\_reply\_alert](reference-Alerts.md#dht_get_peers_reply_alert).

dht\_announce() will issue a DHT announce request to the DHT to the
specified info-hash, advertising the specified port. If the port is
left at its default, 0, the port will be implied by the DHT message's
source port (which may improve connectivity through a NAT).
dht\_announce() is not affected by the announce\_port override setting.

Both these functions are exposed for advanced custom use of the DHT.
All torrents eligible to be announce to the DHT will be automatically,
by libtorrent.

For possible flags, see [announce\_flags\_t](reference-DHT.md#announce_flags_t).

## dht\_live\_nodes()

```cpp
void dht_live_nodes (sha1_hash const& nid);
```

Retrieve all the live DHT (identified by nid) nodes. All the
nodes id and endpoint will be returned in the list of nodes in the
[alert](reference-Alerts.md#alert) dht\_live\_nodes\_alert.
Since this [alert](reference-Alerts.md#alert) is a response to an explicit call, it will always be
posted, regardless of the [alert](reference-Alerts.md#alert) mask.

## dht\_sample\_infohashes()

```cpp
void dht_sample_infohashes (udp::endpoint const& ep, sha1_hash const& target);
```

Query the DHT node specified by ep to retrieve a sample of the
info-hashes that the node currently have in their storage.
The target is included for iterative lookups so that indexing nodes
can perform a key space traversal with a single RPC per node by adjusting
the target value for each RPC. It has no effect on the returned sample value.
The result is posted as a dht\_sample\_infohashes\_alert.

## dht\_direct\_request()

```cpp
void dht_direct_request (udp::endpoint const& ep, entry const& e, client_data_t userdata = {});
```

Send an arbitrary DHT request directly to the specified endpoint. This
function is intended for use by plugins. When a response is received
or the request times out, a [dht\_direct\_response\_alert](reference-Alerts.md#dht_direct_response_alert) will be posted
with the response (if any) and the userdata pointer passed in here.
Since this [alert](reference-Alerts.md#alert) is a response to an explicit call, it will always be
posted, regardless of the [alert](reference-Alerts.md#alert) mask.

## add\_extension()

```cpp
void add_extension (std::shared_ptr<plugin> ext);
void add_extension (std::function<std::shared_ptr<torrent_plugin>(
      torrent_handle const&, client_data_t)> ext);
```

This function adds an extension to this [session](reference-Session.md#session). The argument is a
function object that is called with a torrent\_handle and which should
return a std::shared\_ptr<torrent\_plugin>. To write custom
plugins, see [libtorrent plugins](reference-Plugins.md). For the typical bittorrent client
all of these extensions should be added. The main plugins implemented
in libtorrent are:

uTorrent metadata
:   Allows peers to download the metadata (.torrent files) from the swarm
    directly. Makes it possible to join a swarm with just a tracker and
    info-hash.

```cpp
#include <libtorrent/extensions/ut_metadata.hpp>
ses.add_extension(&lt::create_ut_metadata_plugin);
```

uTorrent peer exchange
:   Exchanges peers between clients.

```cpp
#include <libtorrent/extensions/ut_pex.hpp>
ses.add_extension(&lt::create_ut_pex_plugin);
```

smart ban [plugin](reference-Plugins.md#plugin)
:   A [plugin](reference-Plugins.md#plugin) that, with a small overhead, can ban peers
    that sends bad data with very high accuracy. Should
    eliminate most problems on poisoned torrents.

```cpp
#include <libtorrent/extensions/smart_ban.hpp>
ses.add_extension(&lt::create_smart_ban_plugin);
```

## get\_ip\_filter() set\_ip\_filter()

```cpp
void set_ip_filter (ip_filter f);
ip_filter get_ip_filter () const;
```

Sets a filter that will be used to reject and accept incoming as well
as outgoing connections based on their originating ip address. The
default filter will allow connections to any ip address. To build a
set of rules for which addresses are accepted and not, see [ip\_filter](reference-Filter.md#ip_filter).

Each time a peer is blocked because of the IP filter, a
[peer\_blocked\_alert](reference-Alerts.md#peer_blocked_alert) is generated. get\_ip\_filter() Returns the
[ip\_filter](reference-Filter.md#ip_filter) currently in the [session](reference-Session.md#session). See [ip\_filter](reference-Filter.md#ip_filter).

## set\_port\_filter()

```cpp
void set_port_filter (port_filter const& f);
```

apply [port\_filter](reference-Filter.md#port_filter) f to incoming and outgoing peers. a port filter
will reject making outgoing peer connections to certain remote ports.
The main intention is to be able to avoid triggering certain
anti-virus software by connecting to SMTP, FTP ports.

## ssl\_listen\_port() is\_listening() listen\_port()

```cpp
bool is_listening () const;
unsigned short listen_port () const;
unsigned short ssl_listen_port () const;
```

is\_listening() will tell you whether or not the [session](reference-Session.md#session) has
successfully opened a listening port. If it hasn't, this function will
return false, and then you can set a new
[settings\_pack::listen\_interfaces](reference-Settings.md#listen_interfaces) to try another interface and port to
bind to.

listen\_port() returns the port we ended up listening on.

## set\_peer\_class\_filter() get\_peer\_class\_filter()

```cpp
ip_filter get_peer_class_filter () const;
void set_peer_class_filter (ip_filter const& f);
```

Sets the peer class filter for this [session](reference-Session.md#session). All new peer connections
will take this into account and be added to the peer classes specified
by this filter, based on the peer's IP address.

The ip-filter essentially maps an IP -> uint32. Each bit in that 32
bit integer represents a peer class. The least significant bit
represents class 0, the next bit class 1 and so on.

For more info, see [ip\_filter](reference-Filter.md#ip_filter).

For example, to make all peers in the range 200.1.1.0 - 200.1.255.255
belong to their own peer class, apply the following filter:

```cpp
ip_filter f = ses.get_peer_class_filter();
peer_class_t my_class = ses.create_peer_class("200.1.x.x IP range");
f.add_rule(make_address("200.1.1.0"), make_address("200.1.255.255")
        , 1 << static_cast<std::uint32_t>(my_class));
ses.set_peer_class_filter(f);
```

This setting only applies to new connections, it won't affect existing
peer connections.

This function is limited to only peer class 0-31, since there are only
32 bits in the IP range mapping. Only the set bits matter; no peer
class will be removed from a peer as a result of this call, peer
classes are only added.

The peer\_class argument cannot be greater than 31. The bitmasks
representing peer classes in the peer\_class\_filter are 32 bits.

The get\_peer\_class\_filter() function returns the current filter.

For more information, see [peer classes](manual-ref.md#peer-classes).

## set\_peer\_class\_type\_filter() get\_peer\_class\_type\_filter()

```cpp
peer_class_type_filter get_peer_class_type_filter () const;
void set_peer_class_type_filter (peer_class_type_filter const& f);
```

Sets and gets the *peer class type filter*. This is controls automatic
peer class assignments to peers based on what kind of socket it is.

It does not only support assigning peer classes, it also supports
removing peer classes based on socket type.

The order of these rules being applied are:

1. peer-class IP filter
2. peer-class type filter, removing classes
3. peer-class type filter, adding classes

For more information, see [peer classes](manual-ref.md#peer-classes).

## create\_peer\_class()

```cpp
peer_class_t create_peer_class (char const* name);
```

Creates a new peer class (see [peer classes](manual-ref.md#peer-classes)) with the given name. The
returned integer is the new peer class identifier. Peer classes may
have the same name, so each invocation of this function creates a new
class and returns a unique identifier.

Identifiers are assigned from low numbers to higher. So if you plan on
using certain peer classes in a call to [set\_peer\_class\_filter()](reference-Session.md#set_peer_class_filter()),
make sure to create those early on, to get low identifiers.

For more information on peer classes, see [peer classes](manual-ref.md#peer-classes).

## delete\_peer\_class()

```cpp
void delete_peer_class (peer_class_t cid);
```

This call dereferences the reference count of the specified peer
class. When creating a peer class it's automatically referenced by 1.
If you want to recycle a peer class, you may call this function. You
may only call this function **once** per peer class you create.
Calling it more than once for the same class will lead to memory
corruption.

Since peer classes are reference counted, this function will not
remove the peer class if it's still assigned to torrents or peers. It
will however remove it once the last peer and torrent drops their
references to it.

There is no need to call this function for custom peer classes. All
peer classes will be properly destructed when the [session](reference-Session.md#session) object
destructs.

For more information on peer classes, see [peer classes](manual-ref.md#peer-classes).

## set\_peer\_class() get\_peer\_class()

```cpp
void set_peer_class (peer_class_t cid, peer_class_info const& pci);
peer_class_info get_peer_class (peer_class_t cid) const;
```

These functions queries information from a peer class and updates the
configuration of a peer class, respectively.

cid must refer to an existing peer class. If it does not, the
return value of get\_peer\_class() is undefined.

set\_peer\_class() sets all the information in the
[peer\_class\_info](reference-PeerClass.md#peer_class_info) object in the specified peer class. There is no
option to only update a single property.

A peer or torrent belonging to more than one class, the highest
priority among any of its classes is the one that is taken into
account.

For more information, see [peer classes](manual-ref.md#peer-classes).

## remove\_torrent()

```cpp
void remove_torrent (const torrent_handle&, remove_flags_t = {});
```

remove\_torrent() will close all peer connections associated with
the torrent and tell the tracker that we've stopped participating in
the swarm. This operation cannot fail. When it completes, you will
receive a [torrent\_removed\_alert](reference-Alerts.md#torrent_removed_alert).

[remove\_torrent()](reference-Custom_Storage.md#remove_torrent()) is non-blocking, but will remove the torrent from the
[session](reference-Session.md#session) synchronously. Calling [session\_handle::add\_torrent()](reference-Session.md#add_torrent()) immediately
afterward with the same torrent will succeed. Note that this creates a
new handle which is not equal to the removed one.

The optional second argument options can be used to delete all the
files downloaded by this torrent. To do so, pass in the value
session\_handle::delete\_files. Once the torrent is deleted, a
[torrent\_deleted\_alert](reference-Alerts.md#torrent_deleted_alert) is posted.

The [torrent\_handle](reference-Torrent_Handle.md#torrent_handle) remains valid for some time after [remove\_torrent()](reference-Custom_Storage.md#remove_torrent()) is
called. It will become invalid only after all libtorrent tasks (such as
I/O tasks) release their references to the torrent. Until this happens,
[torrent\_handle::is\_valid()](reference-Torrent_Handle.md#is_valid()) will return true, and other calls such
as [torrent\_handle::status()](reference-Torrent_Handle.md#status()) will succeed. Because of this, and because
[remove\_torrent()](reference-Custom_Storage.md#remove_torrent()) is non-blocking, the following sequence usually
succeeds (does not throw system\_error):
.. code:: c++

> session.remove\_handle(handle);
> handle.save\_resume\_data();

Note that when a queued or downloading torrent is removed, its position
in the download queue is vacated and every subsequent torrent in the
queue has their queue positions updated. This can potentially cause a
large state\_update to be posted. When removing all torrents, it is
advised to remove them from the back of the queue, to minimize the
shifting.

## get\_settings() apply\_settings()

```cpp
void apply_settings (settings_pack const&);
settings_pack get_settings () const;
void apply_settings (settings_pack&&);
```

Applies the settings specified by the [settings\_pack](reference-Settings.md#settings_pack) s. This is an
asynchronous operation that will return immediately and actually apply
the settings to the main thread of libtorrent some time later.

## set\_alert\_notify() wait\_for\_alert() pop\_alerts()

```cpp
void set_alert_notify (std::function<void()> const& fun);
alert* wait_for_alert (time_duration max_wait);
void pop_alerts (std::vector<alert*>* alerts);
```

Alerts is the main mechanism for libtorrent to report errors and
events. pop\_alerts fills in the vector passed to it with pointers
to new alerts. The [session](reference-Session.md#session) still owns these alerts and they will stay
valid until the next time pop\_alerts is called. You may not delete
the [alert](reference-Alerts.md#alert) objects.

It is safe to call pop\_alerts from multiple different threads, as
long as the alerts themselves are not accessed once another thread
calls pop\_alerts. Doing this requires manual synchronization
between the popping threads.

wait\_for\_alert will block the current thread for max\_wait time
duration, or until another [alert](reference-Alerts.md#alert) is posted. If an [alert](reference-Alerts.md#alert) is available
at the time of the call, it returns immediately. The returned [alert](reference-Alerts.md#alert)
pointer is the head of the [alert](reference-Alerts.md#alert) queue. wait\_for\_alert does not
pop alerts from the queue, it merely peeks at it. The returned [alert](reference-Alerts.md#alert)
will stay valid until pop\_alerts is called twice. The first time
will pop it and the second will free it.

If there is no [alert](reference-Alerts.md#alert) in the queue and no [alert](reference-Alerts.md#alert) arrives within the
specified timeout, wait\_for\_alert returns nullptr.

In the python binding, wait\_for\_alert takes the number of
milliseconds to wait as an integer.

The [alert](reference-Alerts.md#alert) queue in the [session](reference-Session.md#session) will not grow indefinitely. Make sure
to pop periodically to not miss notifications. To control the max
number of alerts that's queued by the [session](reference-Session.md#session), see
settings\_pack::alert\_queue\_size.

Some alerts are considered so important that they are posted even when
the [alert](reference-Alerts.md#alert) queue is full. Some alerts are considered mandatory and cannot
be disabled by the alert\_mask. For instance,
[save\_resume\_data\_alert](reference-Alerts.md#save_resume_data_alert) and [save\_resume\_data\_failed\_alert](reference-Alerts.md#save_resume_data_failed_alert) are always
posted, regardless of the [alert](reference-Alerts.md#alert) mask.

To control which alerts are posted, set the alert\_mask
([settings\_pack::alert\_mask](reference-Settings.md#alert_mask)).

If the [alert](reference-Alerts.md#alert) queue fills up to the point where alerts are dropped, this
will be indicated by a [alerts\_dropped\_alert](reference-Alerts.md#alerts_dropped_alert), which contains a bitmask
of which types of alerts were dropped. Generally it is a good idea to
make sure the [alert](reference-Alerts.md#alert) queue is large enough, the alert\_mask doesn't have
unnecessary categories enabled and to call pop\_alert() frequently, to
avoid alerts being dropped.

the set\_alert\_notify function lets the client set a function object
to be invoked every time the [alert](reference-Alerts.md#alert) queue goes from having 0 alerts to
1 [alert](reference-Alerts.md#alert). This function is called from within libtorrent, it may be the
main thread, or it may be from within a user call. The intention of
of the function is that the client wakes up its main thread, to poll
for more alerts using pop\_alerts(). If the notify function fails
to do so, it won't be called again, until pop\_alerts is called for
some other reason. For instance, it could signal an eventfd, post a
message to an HWND or some other main message pump. The actual
retrieval of alerts should not be done in the callback. In fact, the
callback should not block. It should not perform any expensive work.
It really should just notify the main application thread.

The type of an [alert](reference-Alerts.md#alert) is returned by the polymorphic function
alert::type() but can also be queries from a concrete type via
T::alert\_type, as a static constant.

## delete\_port\_mapping() add\_port\_mapping()

```cpp
void delete_port_mapping (port_mapping_t handle);
std::vector<port_mapping_t> add_port_mapping (portmap_protocol t, int external_port, int local_port);
```

add\_port\_mapping adds one or more port forwards on UPnP and/or NAT-PMP,
whichever is enabled. A mapping is created for each listen socket
in the [session](reference-Session.md#session). The return values are all handles referring to the
port mappings that were just created. Pass them to [delete\_port\_mapping()](reference-Session.md#delete_port_mapping())
to remove them.

## reopen\_network\_sockets()

```cpp
void reopen_network_sockets (reopen_network_flags_t options = reopen_map_ports);
```

Instructs the [session](reference-Session.md#session) to reopen all listen and outgoing sockets.

It's useful in the case your platform doesn't support the built in
IP notifier mechanism, or if you have a better more reliable way to
detect changes in the IP routing table.

## native\_handle()

```cpp
std::shared_ptr<aux::session_impl> native_handle () const;
```

This function is intended only for use by plugins. This type does
not have a stable API and should be relied on as little as possible.

save\_settings
:   saves settings (i.e. the [settings\_pack](reference-Settings.md#settings_pack))

save\_dht\_state
:   saves dht state such as nodes and node-id, possibly accelerating
    joining the DHT if provided at next [session](reference-Session.md#session) startup.

save\_extension\_state
:   load or save state from plugins

save\_ip\_filter
:   load or save the IP filter set on the [session](reference-Session.md#session)

global\_peer\_class\_id tcp\_peer\_class\_id local\_peer\_class\_id
:   built-in peer classes

delete\_files
:   delete the files belonging to the torrent from disk.
    including the part-file, if there is one

delete\_partfile
:   delete just the part-file associated with this torrent

paused
:   when set, the [session](reference-Session.md#session) will start paused. Call
    [session\_handle::resume()](reference-Session.md#resume()) to start

udp tcp
:   protocols used by [add\_port\_mapping()](reference-Session.md#add_port_mapping())

reopen\_map\_ports
:   This option indicates if the ports are mapped using natpmp
    and upnp. If mapping was already made, they are deleted and added
    again. This only works if natpmp and/or upnp are configured to be
    enable.

# write\_session\_params() read\_session\_params() write\_session\_params\_buf()

Declared in "[libtorrent/session\_params.hpp](include/libtorrent/session_params.hpp)"

```cpp
entry write_session_params (session_params const& sp
   , save_state_flags_t flags = save_state_flags_t::all());
session_params read_session_params (bdecode_node const& e
   , save_state_flags_t flags = save_state_flags_t::all());
session_params read_session_params (span<char const> buf
   , save_state_flags_t flags = save_state_flags_t::all());
std::vector<char> write_session_params_buf (session_params const& sp
   , save_state_flags_t flags = save_state_flags_t::all());
```

These functions serialize and de-serialize a session\_params object to and
from bencoded form. The [session\_params](reference-Session.md#session_params) object is used to initialize a new
[session](reference-Session.md#session) using the state from a previous one (or by programmatically configure
the [session](reference-Session.md#session) up-front).
The flags parameter can be used to only save and load certain aspects of the
session's state.
The \_buf suffix indicates the function operates on buffer rather than the
bencoded structure.
The torrents in a [session](reference-Session.md#session) are not part of the [session\_params](reference-Session.md#session_params) state, they have
to be restored separately.
