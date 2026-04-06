---
title: "a word of caution"
source: "https://libtorrent.org/reference-Plugins.html"
---

[home](reference.md)

libtorrent has a [plugin](reference-Plugins.md#plugin) interface for implementing extensions to the protocol.
These can be general extensions for transferring metadata or peer exchange
extensions, or it could be used to provide a way to customize the protocol
to fit a particular (closed) network.

In short, the [plugin](reference-Plugins.md#plugin) interface makes it possible to:

* register extension messages (sent in the extension handshake), see
  [extensions](manual-ref.md#extensions).
* add data and parse data from the extension handshake.
* send extension messages and standard bittorrent messages.
* override or block the handling of standard bittorrent messages.
* save and restore state via the [session](reference-Session.md#session) state
* see all alerts that are posted

# a word of caution

Writing your own [plugin](reference-Plugins.md#plugin) is a very easy way to introduce serious bugs such as
dead locks and race conditions. Since a [plugin](reference-Plugins.md#plugin) has access to internal
structures it is also quite easy to sabotage libtorrent's operation.

All the callbacks are always called from the libtorrent network thread. In
case portions of your [plugin](reference-Plugins.md#plugin) are called from other threads, typically the main
thread, you cannot use any of the member functions on the internal structures
in libtorrent, since those require being called from the libtorrent network
thread . Furthermore, you also need to synchronize your own shared data
within the [plugin](reference-Plugins.md#plugin), to make sure it is not accessed at the same time from the
libtorrent thread (through a callback). If you need to send out a message
from another thread, it is advised to use an internal queue, and do the
actual sending in tick().

Since the [plugin](reference-Plugins.md#plugin) interface gives you easy access to internal structures, it
is not supported as a stable API. Plugins should be considered specific to a
specific version of libtorrent. Although, in practice the internals mostly
don't change that dramatically.

# plugin-interface

The [plugin](reference-Plugins.md#plugin) interface consists of three base classes that the [plugin](reference-Plugins.md#plugin) may
implement. These are called [plugin](reference-Plugins.md#plugin), [torrent\_plugin](reference-Plugins.md#torrent_plugin) and [peer\_plugin](reference-Plugins.md#peer_plugin).
They are found in the <libtorrent/extensions.hpp> header.

These plugins are instantiated for each [session](reference-Session.md#session), torrent and possibly each peer,
respectively.

For plugins that only need per torrent state, it is enough to only implement
torrent\_plugin and pass a constructor function or function object to
session::add\_extension() or torrent\_handle::add\_extension() (if the
torrent has already been started and you want to hook in the extension at
run-time).

The signature of the function is:

```cpp
std::shared_ptr<torrent_plugin> (*)(torrent_handle const&, client_data_t);
```

The second argument is the userdata passed to session::add\_torrent() or
torrent\_handle::add\_extension().

The function should return a std::shared\_ptr<torrent\_plugin> which
may or may not be 0. If it is a nullptr, the extension is simply ignored
for this torrent. If it is a valid pointer (to a class inheriting
torrent\_plugin), it will be associated with this torrent and callbacks
will be made on torrent events.

For more elaborate plugins which require [session](reference-Session.md#session) wide state, you would
implement plugin, construct an object (in a std::shared\_ptr) and pass
it in to session::add\_extension().

# custom alerts

Since plugins are running within internal libtorrent threads, one convenient
way to communicate with the client is to post custom alerts.

The expected interface of any [alert](reference-Alerts.md#alert), apart from deriving from the [alert](reference-Alerts.md#alert)
base class, looks like this:

```cpp
static const int alert_type = <unique alert ID>;
virtual int type() const { return alert_type; }

virtual std::string message() const;

static const alert_category_t static_category = <bitmask of alert::category_t flags>;
virtual alert_category_t category() const { return static_category; }

virtual char const* what() const { return <string literal of the name of this alert>; }
```

The alert\_type is used for the type-checking in alert\_cast. It must
not collide with any other [alert](reference-Alerts.md#alert). The built-in alerts in libtorrent will
not use [alert](reference-Alerts.md#alert) type IDs greater than user\_alert\_id. When defining your
own [alert](reference-Alerts.md#alert), make sure it's greater than this constant.

type() is the run-time equivalence of the alert\_type.

The message() virtual function is expected to construct a useful
string representation of the [alert](reference-Alerts.md#alert) and the event or data it represents.
Something convenient to put in a log file for instance.

clone() is used internally to copy alerts. The suggested implementation
of simply allocating a new instance as a copy of \*this is all that's
expected.

The static category is required for checking whether or not the category
for a specific [alert](reference-Alerts.md#alert) is enabled or not, without instantiating the [alert](reference-Alerts.md#alert).
The category virtual function is the run-time equivalence.

The what() virtual function may simply be a string literal of the class
name of your [alert](reference-Alerts.md#alert).

For more information, see the [alert section](reference-Alerts.md).

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:class+peer_connection_handle&labels=documentation&body=Documentation+under+heading+%22class+peer_connection_handle%22+could+be+improved)]

# peer\_connection\_handle

Declared in "[libtorrent/peer\_connection\_handle.hpp](include/libtorrent/peer_connection_handle.hpp)"

the [peer\_connection\_handle](reference-Plugins.md#peer_connection_handle) class provides a handle to the internal peer
connection object, to be used by plugins. This is a low level interface that
may not be stable across libtorrent versions

```cpp
struct peer_connection_handle
{
   explicit peer_connection_handle (std::weak_ptr<peer_connection> impl);
   connection_type type () const;
   void add_extension (std::shared_ptr<peer_plugin>);
   peer_plugin const* find_plugin (string_view type) const;
   bool is_seed () const;
   bool upload_only () const;
   peer_id const& pid () const;
   bool has_piece (piece_index_t i) const;
   bool is_interesting () const;
   bool is_choked () const;
   bool is_peer_interested () const;
   bool has_peer_choked () const;
   void choke_this_peer ();
   void maybe_unchoke_this_peer ();
   void get_peer_info (peer_info& p) const;
   torrent_handle associated_torrent () const;
   tcp::endpoint const& remote () const;
   tcp::endpoint local_endpoint () const;
   bool is_disconnecting () const;
   void disconnect (error_code const& ec, operation_t op
      , disconnect_severity_t = peer_connection_interface::normal);
   bool is_connecting () const;
   bool is_outgoing () const;
   bool on_local_network () const;
   bool ignore_unchoke_slots () const;
   bool failed () const;
   bool should_log (peer_log_alert::direction_t direction) const;
   void peer_log (peer_log_alert::direction_t direction
      , char const* event, char const* fmt = "", ...) const TORRENT_FORMAT(4,5);
   bool can_disconnect (error_code const& ec) const;
   bool has_metadata () const;
   bool in_handshake () const;
   void send_buffer (char const* begin, int size);
   time_point time_of_last_unchoke () const;
   std::time_t last_seen_complete () const;
   bool operator< (peer_connection_handle const& o) const;
   bool operator!= (peer_connection_handle const& o) const;
   bool operator== (peer_connection_handle const& o) const;
   std::shared_ptr<peer_connection> native_handle () const;
};
```

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:class+bt_peer_connection_handle&labels=documentation&body=Documentation+under+heading+%22class+bt_peer_connection_handle%22+could+be+improved)]

# bt\_peer\_connection\_handle

Declared in "[libtorrent/peer\_connection\_handle.hpp](include/libtorrent/peer_connection_handle.hpp)"

The [bt\_peer\_connection\_handle](reference-Plugins.md#bt_peer_connection_handle) provides a handle to the internal bittorrent
peer connection object to plugins. It's low level and may not be a stable API
across libtorrent versions.

```cpp
struct bt_peer_connection_handle : peer_connection_handle
{
   explicit bt_peer_connection_handle (peer_connection_handle pc);
   bool packet_finished () const;
   bool support_extensions () const;
   bool supports_encryption () const;
   void switch_send_crypto (std::shared_ptr<crypto_plugin> crypto);
   void switch_recv_crypto (std::shared_ptr<crypto_plugin> crypto);
   std::shared_ptr<bt_peer_connection> native_handle () const;
};
```

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:class+plugin&labels=documentation&body=Documentation+under+heading+%22class+plugin%22+could+be+improved)]

# plugin

Declared in "[libtorrent/extensions.hpp](include/libtorrent/extensions.hpp)"

this is the base class for a [session](reference-Session.md#session) [plugin](reference-Plugins.md#plugin). One primary feature
is that it is notified of all torrents that are added to the [session](reference-Session.md#session),
and can add its own torrent\_plugins.

```cpp
struct plugin
{
   virtual feature_flags_t implemented_features ();
   virtual std::shared_ptr<torrent_plugin> new_torrent (torrent_handle const&, client_data_t);
   virtual void added (session_handle const&);
   virtual void abort ();
   virtual bool on_dht_request (string_view /* query */
      , udp::endpoint const& /* source */, bdecode_node const& /* message */
      , entry& /* response */);
   virtual void on_alert (alert const*);
   virtual bool on_unknown_torrent (info_hash_t const& /* info_hash */
      , peer_connection_handle const& /* pc */, add_torrent_params& /* p */);
   virtual void on_tick ();
   virtual uint64_t get_unchoke_priority (peer_connection_handle const& /* peer */);
   virtual std::map<std::string, std::string> save_state () const;
   virtual void load_state (std::map<std::string, std::string> const&);

   static constexpr feature_flags_t optimistic_unchoke_feature  = 1_bit;
   static constexpr feature_flags_t tick_feature  = 2_bit;
   static constexpr feature_flags_t dht_request_feature  = 3_bit;
   static constexpr feature_flags_t alert_feature  = 4_bit;
   static constexpr feature_flags_t unknown_torrent_feature  = 5_bit;
};
```

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:plugin%3A%3A%5Bimplemented_features%28%29%5D&labels=documentation&body=Documentation+under+heading+%22plugin%3A%3A%5Bimplemented_features%28%29%5D%22+could+be+improved)]

## implemented\_features()

```cpp
virtual feature_flags_t implemented_features ();
```

This function is expected to return a bitmask indicating which features
this [plugin](reference-Plugins.md#plugin) implements. Some callbacks on this object may not be called
unless the corresponding feature flag is returned here. Note that
callbacks may still be called even if the corresponding feature is not
specified in the return value here. See feature\_flags\_t for possible
flags to return.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:plugin%3A%3A%5Bnew_torrent%28%29%5D&labels=documentation&body=Documentation+under+heading+%22plugin%3A%3A%5Bnew_torrent%28%29%5D%22+could+be+improved)]

## new\_torrent()

```cpp
virtual std::shared_ptr<torrent_plugin> new_torrent (torrent_handle const&, client_data_t);
```

this is called by the [session](reference-Session.md#session) every time a new torrent is added.
The torrent\* points to the internal torrent object created
for the new torrent. The [client\_data\_t](reference-Add_Torrent.md#client_data_t) is the userdata pointer as
passed in via [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params).

If the [plugin](reference-Plugins.md#plugin) returns a [torrent\_plugin](reference-Plugins.md#torrent_plugin) instance, it will be added
to the new torrent. Otherwise, return an empty shared\_ptr to a
[torrent\_plugin](reference-Plugins.md#torrent_plugin) (the default).

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:plugin%3A%3A%5Badded%28%29%5D&labels=documentation&body=Documentation+under+heading+%22plugin%3A%3A%5Badded%28%29%5D%22+could+be+improved)]

## added()

```cpp
virtual void added (session_handle const&);
```

called when [plugin](reference-Plugins.md#plugin) is added to a [session](reference-Session.md#session)

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:plugin%3A%3A%5Babort%28%29%5D&labels=documentation&body=Documentation+under+heading+%22plugin%3A%3A%5Babort%28%29%5D%22+could+be+improved)]

## abort()

```cpp
virtual void abort ();
```

called when the [session](reference-Session.md#session) is aborted
the [plugin](reference-Plugins.md#plugin) should perform any cleanup necessary to allow the session's
destruction (e.g. cancel outstanding async operations)

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:plugin%3A%3A%5Bon_dht_request%28%29%5D&labels=documentation&body=Documentation+under+heading+%22plugin%3A%3A%5Bon_dht_request%28%29%5D%22+could+be+improved)]

## on\_dht\_request()

```cpp
virtual bool on_dht_request (string_view /* query */
      , udp::endpoint const& /* source */, bdecode_node const& /* message */
      , entry& /* response */);
```

called when a dht request is received.
If your [plugin](reference-Plugins.md#plugin) expects this to be called, make sure to include the flag
dht\_request\_feature in the return value from [implemented\_features()](reference-Plugins.md#implemented_features()).

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:plugin%3A%3A%5Bon_alert%28%29%5D&labels=documentation&body=Documentation+under+heading+%22plugin%3A%3A%5Bon_alert%28%29%5D%22+could+be+improved)]

## on\_alert()

```cpp
virtual void on_alert (alert const*);
```

called when an [alert](reference-Alerts.md#alert) is posted alerts that are filtered are not posted.
If your [plugin](reference-Plugins.md#plugin) expects this to be called, make sure to include the flag
alert\_feature in the return value from [implemented\_features()](reference-Plugins.md#implemented_features()).

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:plugin%3A%3A%5Bon_unknown_torrent%28%29%5D&labels=documentation&body=Documentation+under+heading+%22plugin%3A%3A%5Bon_unknown_torrent%28%29%5D%22+could+be+improved)]

## on\_unknown\_torrent()

```cpp
virtual bool on_unknown_torrent (info_hash_t const& /* info_hash */
      , peer_connection_handle const& /* pc */, add_torrent_params& /* p */);
```

return true if the [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params) should be added

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:plugin%3A%3A%5Bon_tick%28%29%5D&labels=documentation&body=Documentation+under+heading+%22plugin%3A%3A%5Bon_tick%28%29%5D%22+could+be+improved)]

## on\_tick()

```cpp
virtual void on_tick ();
```

called once per second.
If your [plugin](reference-Plugins.md#plugin) expects this to be called, make sure to include the flag
tick\_feature in the return value from [implemented\_features()](reference-Plugins.md#implemented_features()).

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:plugin%3A%3A%5Bget_unchoke_priority%28%29%5D&labels=documentation&body=Documentation+under+heading+%22plugin%3A%3A%5Bget_unchoke_priority%28%29%5D%22+could+be+improved)]

## get\_unchoke\_priority()

```cpp
virtual uint64_t get_unchoke_priority (peer_connection_handle const& /* peer */);
```

called when choosing peers to optimistically unchoke. The return value
indicates the peer's priority for unchoking. Lower return values
correspond to higher priority. Priorities above 2^63-1 are reserved.
If your [plugin](reference-Plugins.md#plugin) has no priority to assign a peer it should return 2^64-1.
If your [plugin](reference-Plugins.md#plugin) expects this to be called, make sure to include the flag
optimistic\_unchoke\_feature in the return value from [implemented\_features()](reference-Plugins.md#implemented_features()).
If multiple plugins implement this function the lowest return value
(i.e. the highest priority) is used.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:plugin%3A%3A%5Bload_state%28%29%5D&labels=documentation&body=Documentation+under+heading+%22plugin%3A%3A%5Bload_state%28%29%5D%22+could+be+improved)]

## load\_state()

```cpp
virtual void load_state (std::map<std::string, std::string> const&);
```

called on startup while loading settings state from the [session\_params](reference-Session.md#session_params)

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:plugin%3A%3A%5Boptimistic_unchoke_feature%5D&labels=documentation&body=Documentation+under+heading+%22plugin%3A%3A%5Boptimistic_unchoke_feature%5D%22+could+be+improved)]

optimistic\_unchoke\_feature
:   include this bit if your [plugin](reference-Plugins.md#plugin) needs to alter the order of the
    optimistic unchoke of peers. i.e. have the on\_optimistic\_unchoke()
    callback be called.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:plugin%3A%3A%5Btick_feature%5D&labels=documentation&body=Documentation+under+heading+%22plugin%3A%3A%5Btick_feature%5D%22+could+be+improved)]

tick\_feature
:   include this bit if your [plugin](reference-Plugins.md#plugin) needs to have [on\_tick()](reference-Plugins.md#on_tick()) called

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:plugin%3A%3A%5Bdht_request_feature%5D&labels=documentation&body=Documentation+under+heading+%22plugin%3A%3A%5Bdht_request_feature%5D%22+could+be+improved)]

dht\_request\_feature
:   include this bit if your [plugin](reference-Plugins.md#plugin) needs to have [on\_dht\_request()](reference-Plugins.md#on_dht_request())
    called

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:plugin%3A%3A%5Balert_feature%5D&labels=documentation&body=Documentation+under+heading+%22plugin%3A%3A%5Balert_feature%5D%22+could+be+improved)]

alert\_feature
:   include this bit if your [plugin](reference-Plugins.md#plugin) needs to have [on\_alert()](reference-Plugins.md#on_alert())
    called

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:plugin%3A%3A%5Bunknown_torrent_feature%5D&labels=documentation&body=Documentation+under+heading+%22plugin%3A%3A%5Bunknown_torrent_feature%5D%22+could+be+improved)]

unknown\_torrent\_feature
:   include this bit if your [plugin](reference-Plugins.md#plugin) needs to have [on\_unknown\_torrent()](reference-Plugins.md#on_unknown_torrent())
    called even if there is no active torrent in the [session](reference-Session.md#session)

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:class+torrent_plugin&labels=documentation&body=Documentation+under+heading+%22class+torrent_plugin%22+could+be+improved)]

# torrent\_plugin

Declared in "[libtorrent/extensions.hpp](include/libtorrent/extensions.hpp)"

Torrent plugins are associated with a single torrent and have a number
of functions called at certain events. Many of its functions have the
ability to change or override the default libtorrent behavior.

```cpp
struct torrent_plugin
{
   virtual std::shared_ptr<peer_plugin> new_connection (peer_connection_handle const&);
   virtual void on_piece_failed (piece_index_t);
   virtual void on_piece_pass (piece_index_t);
   virtual void tick ();
   virtual bool on_pause ();
   virtual bool on_resume ();
   virtual void on_files_checked ();
   virtual void on_state (torrent_status::state_t);
   virtual void on_add_peer (tcp::endpoint const&,
      peer_source_flags_t, add_peer_flags_t);

   static constexpr add_peer_flags_t first_time  = 1_bit;
   static constexpr add_peer_flags_t filtered  = 2_bit;
};
```

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_plugin%3A%3A%5Bnew_connection%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_plugin%3A%3A%5Bnew_connection%28%29%5D%22+could+be+improved)]

## new\_connection()

```cpp
virtual std::shared_ptr<peer_plugin> new_connection (peer_connection_handle const&);
```

This function is called each time a new peer is connected to the torrent. You
may choose to ignore this by just returning a default constructed
shared\_ptr (in which case you don't need to override this member
function).

If you need an extension to the peer connection (which most plugins do) you
are supposed to return an instance of your [peer\_plugin](reference-Plugins.md#peer_plugin) class. Which in
turn will have its hook functions called on event specific to that peer.

The peer\_connection\_handle will be valid as long as the shared\_ptr
is being held by the torrent object. So, it is generally a good idea to not
keep a shared\_ptr to your own [peer\_plugin](reference-Plugins.md#peer_plugin). If you want to keep references
to it, use weak\_ptr.

If this function throws an exception, the connection will be closed.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_plugin%3A%3A%5Bon_piece_pass%28%29+on_piece_failed%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_plugin%3A%3A%5Bon_piece_pass%28%29+on_piece_failed%28%29%5D%22+could+be+improved)]

## on\_piece\_pass() on\_piece\_failed()

```cpp
virtual void on_piece_failed (piece_index_t);
virtual void on_piece_pass (piece_index_t);
```

These hooks are called when a piece passes the hash check or fails the hash
check, respectively. The index is the piece index that was downloaded.
It is possible to access the list of peers that participated in sending the
piece through the torrent and the piece\_picker.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_plugin%3A%3A%5Btick%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_plugin%3A%3A%5Btick%28%29%5D%22+could+be+improved)]

## tick()

```cpp
virtual void tick ();
```

This hook is called approximately once per second. It is a way of making it
easy for plugins to do timed events, for sending messages or whatever.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_plugin%3A%3A%5Bon_pause%28%29+on_resume%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_plugin%3A%3A%5Bon_pause%28%29+on_resume%28%29%5D%22+could+be+improved)]

## on\_pause() on\_resume()

```cpp
virtual bool on_pause ();
virtual bool on_resume ();
```

These hooks are called when the torrent is paused and resumed respectively.
The return value indicates if the event was handled. A return value of
true indicates that it was handled, and no other [plugin](reference-Plugins.md#plugin) after this one
will have this hook function called, and the standard handler will also not be
invoked. So, returning true effectively overrides the standard behavior of
pause or resume.

Note that if you call pause() or resume() on the torrent from your
handler it will recurse back into your handler, so in order to invoke the
standard handler, you have to keep your own state on whether you want standard
behavior or overridden behavior.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_plugin%3A%3A%5Bon_files_checked%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_plugin%3A%3A%5Bon_files_checked%28%29%5D%22+could+be+improved)]

## on\_files\_checked()

```cpp
virtual void on_files_checked ();
```

This function is called when the initial files of the torrent have been
checked. If there are no files to check, this function is called immediately.

i.e. This function is always called when the torrent is in a state where it
can start downloading.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_plugin%3A%3A%5Bon_state%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_plugin%3A%3A%5Bon_state%28%29%5D%22+could+be+improved)]

## on\_state()

```cpp
virtual void on_state (torrent_status::state_t);
```

called when the torrent changes state
the state is one of [torrent\_status::state\_t](reference-Torrent_Status.md#state_t)
enum members

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_plugin%3A%3A%5Bon_add_peer%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_plugin%3A%3A%5Bon_add_peer%28%29%5D%22+could+be+improved)]

## on\_add\_peer()

```cpp
virtual void on_add_peer (tcp::endpoint const&,
      peer_source_flags_t, add_peer_flags_t);
```

called every time a new peer is added to the peer list.
This is before the peer is connected to. For flags, see
torrent\_plugin::flags\_t. The source argument refers to
the source where we learned about this peer from. It's a
bitmask, because many sources may have told us about the same
peer. For peer source flags, see peer\_info::peer\_source\_flags.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_plugin%3A%3A%5Bfirst_time%5D&labels=documentation&body=Documentation+under+heading+%22torrent_plugin%3A%3A%5Bfirst_time%5D%22+could+be+improved)]

first\_time
:   this is the first time we see this peer

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_plugin%3A%3A%5Bfiltered%5D&labels=documentation&body=Documentation+under+heading+%22torrent_plugin%3A%3A%5Bfiltered%5D%22+could+be+improved)]

filtered
:   this peer was not added because it was
    filtered by the IP filter

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:class+peer_plugin&labels=documentation&body=Documentation+under+heading+%22class+peer_plugin%22+could+be+improved)]

# peer\_plugin

Declared in "[libtorrent/extensions.hpp](include/libtorrent/extensions.hpp)"

peer plugins are associated with a specific peer. A peer could be
both a regular bittorrent peer (bt\_peer\_connection) or one of the
web seed connections (web\_peer\_connection or http\_seed\_connection).
In order to only attach to certain peers, make your
torrent\_plugin::new\_connection only return a [plugin](reference-Plugins.md#plugin) for certain peer
connection types

```cpp
struct peer_plugin
{
   virtual string_view type () const;
   virtual void add_handshake (entry&);
   virtual void on_disconnect (error_code const&);
   virtual void on_connected ();
   virtual bool on_handshake (span<char const>);
   virtual bool on_extension_handshake (bdecode_node const&);
   virtual bool on_dont_have (piece_index_t);
   virtual bool on_choke ();
   virtual bool on_have (piece_index_t);
   virtual bool on_bitfield (bitfield const& /*bitfield*/);
   virtual bool on_have_none ();
   virtual bool on_request (peer_request const&);
   virtual bool on_interested ();
   virtual bool on_have_all ();
   virtual bool on_allowed_fast (piece_index_t);
   virtual bool on_not_interested ();
   virtual bool on_unchoke ();
   virtual bool on_piece (peer_request const& /*piece*/
      , span<char const> /*buf*/);
   virtual bool on_reject (peer_request const&);
   virtual bool on_suggest (piece_index_t);
   virtual bool on_cancel (peer_request const&);
   virtual void sent_have_all ();
   virtual void sent_cancel (peer_request const&);
   virtual void sent_reject_request (peer_request const&);
   virtual void sent_suggest (piece_index_t);
   virtual void sent_allow_fast (piece_index_t);
   virtual void sent_have_none ();
   virtual void sent_request (peer_request const&);
   virtual void sent_choke ();
   virtual void sent_unchoke ();
   virtual void sent_piece (peer_request const&);
   virtual void sent_have (piece_index_t);
   virtual void sent_interested ();
   virtual void sent_not_interested ();
   virtual void sent_payload (int /* bytes */);
   virtual bool can_disconnect (error_code const& /*ec*/);
   virtual bool on_extended (int /*length*/, int /*msg*/,
      span<char const> /*body*/);
   virtual bool on_unknown_message (int /*length*/, int /*msg*/,
      span<char const> /*body*/);
   virtual void on_piece_failed (piece_index_t);
   virtual void on_piece_pass (piece_index_t);
   virtual void tick ();
   virtual bool write_request (peer_request const&);
};
```

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:peer_plugin%3A%3A%5Btype%28%29%5D&labels=documentation&body=Documentation+under+heading+%22peer_plugin%3A%3A%5Btype%28%29%5D%22+could+be+improved)]

## type()

```cpp
virtual string_view type () const;
```

This function is expected to return the name of
the [plugin](reference-Plugins.md#plugin).

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:peer_plugin%3A%3A%5Badd_handshake%28%29%5D&labels=documentation&body=Documentation+under+heading+%22peer_plugin%3A%3A%5Badd_handshake%28%29%5D%22+could+be+improved)]

## add\_handshake()

```cpp
virtual void add_handshake (entry&);
```

can add entries to the extension handshake
this is not called for web seeds

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:peer_plugin%3A%3A%5Bon_disconnect%28%29%5D&labels=documentation&body=Documentation+under+heading+%22peer_plugin%3A%3A%5Bon_disconnect%28%29%5D%22+could+be+improved)]

## on\_disconnect()

```cpp
virtual void on_disconnect (error_code const&);
```

called when the peer is being disconnected.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:peer_plugin%3A%3A%5Bon_connected%28%29%5D&labels=documentation&body=Documentation+under+heading+%22peer_plugin%3A%3A%5Bon_connected%28%29%5D%22+could+be+improved)]

## on\_connected()

```cpp
virtual void on_connected ();
```

called when the peer is successfully connected. Note that
incoming connections will have been connected by the time
the peer [plugin](reference-Plugins.md#plugin) is attached to it, and won't have this hook
called.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:peer_plugin%3A%3A%5Bon_handshake%28%29%5D&labels=documentation&body=Documentation+under+heading+%22peer_plugin%3A%3A%5Bon_handshake%28%29%5D%22+could+be+improved)]

## on\_handshake()

```cpp
virtual bool on_handshake (span<char const>);
```

this is called when the initial bittorrent handshake is received.
Returning false means that the other end doesn't support this extension
and will remove it from the list of plugins. this is not called for web
seeds

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:peer_plugin%3A%3A%5Bon_extension_handshake%28%29%5D&labels=documentation&body=Documentation+under+heading+%22peer_plugin%3A%3A%5Bon_extension_handshake%28%29%5D%22+could+be+improved)]

## on\_extension\_handshake()

```cpp
virtual bool on_extension_handshake (bdecode_node const&);
```

called when the extension handshake from the other end is received
if this returns false, it means that this extension isn't
supported by this peer. It will result in this [peer\_plugin](reference-Plugins.md#peer_plugin)
being removed from the peer\_connection and destructed.
this is not called for web seeds

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:peer_plugin%3A%3A%5Bon_have_all%28%29+on_interested%28%29+on_choke%28%29+on_dont_have%28%29+on_bitfield%28%29+on_have%28%29+on_request%28%29+on_have_none%28%29+on_allowed_fast%28%29+on_unchoke%28%29+on_not_interested%28%29%5D&labels=documentation&body=Documentation+under+heading+%22peer_plugin%3A%3A%5Bon_have_all%28%29+on_interested%28%29+on_choke%28%29+on_dont_have%28%29+on_bitfield%28%29+on_have%28%29+on_request%28%29+on_have_none%28%29+on_allowed_fast%28%29+on_unchoke%28%29+on_not_interested%28%29%5D%22+could+be+improved)]

## on\_have\_all() on\_interested() on\_choke() on\_dont\_have() on\_bitfield() on\_have() on\_request() on\_have\_none() on\_allowed\_fast() on\_unchoke() on\_not\_interested()

```cpp
virtual bool on_dont_have (piece_index_t);
virtual bool on_choke ();
virtual bool on_have (piece_index_t);
virtual bool on_bitfield (bitfield const& /*bitfield*/);
virtual bool on_have_none ();
virtual bool on_request (peer_request const&);
virtual bool on_interested ();
virtual bool on_have_all ();
virtual bool on_allowed_fast (piece_index_t);
virtual bool on_not_interested ();
virtual bool on_unchoke ();
```

returning true from any of the message handlers
indicates that the [plugin](reference-Plugins.md#plugin) has handled the message.
it will break the [plugin](reference-Plugins.md#plugin) chain traversing and not let
anyone else handle the message, including the default
handler.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:peer_plugin%3A%3A%5Bon_piece%28%29%5D&labels=documentation&body=Documentation+under+heading+%22peer_plugin%3A%3A%5Bon_piece%28%29%5D%22+could+be+improved)]

## on\_piece()

```cpp
virtual bool on_piece (peer_request const& /*piece*/
      , span<char const> /*buf*/);
```

This function is called when the peer connection is receiving
a piece. buf points (non-owning pointer) to the data in an
internal immutable disk buffer. The length of the data is specified
in the length member of the piece parameter.
returns true to indicate that the piece is handled and the
rest of the logic should be ignored.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:peer_plugin%3A%3A%5Bsent_unchoke%28%29+sent_not_interested%28%29+sent_have%28%29+sent_interested%28%29+sent_piece%28%29%5D&labels=documentation&body=Documentation+under+heading+%22peer_plugin%3A%3A%5Bsent_unchoke%28%29+sent_not_interested%28%29+sent_have%28%29+sent_interested%28%29+sent_piece%28%29%5D%22+could+be+improved)]

## sent\_unchoke() sent\_not\_interested() sent\_have() sent\_interested() sent\_piece()

```cpp
virtual void sent_unchoke ();
virtual void sent_piece (peer_request const&);
virtual void sent_have (piece_index_t);
virtual void sent_interested ();
virtual void sent_not_interested ();
```

called after a choke message has been sent to the peer

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:peer_plugin%3A%3A%5Bsent_payload%28%29%5D&labels=documentation&body=Documentation+under+heading+%22peer_plugin%3A%3A%5Bsent_payload%28%29%5D%22+could+be+improved)]

## sent\_payload()

```cpp
virtual void sent_payload (int /* bytes */);
```

called after piece data has been sent to the peer
this can be used for stats book keeping

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:peer_plugin%3A%3A%5Bcan_disconnect%28%29%5D&labels=documentation&body=Documentation+under+heading+%22peer_plugin%3A%3A%5Bcan_disconnect%28%29%5D%22+could+be+improved)]

## can\_disconnect()

```cpp
virtual bool can_disconnect (error_code const& /*ec*/);
```

called when libtorrent think this peer should be disconnected.
if the [plugin](reference-Plugins.md#plugin) returns false, the peer will not be disconnected.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:peer_plugin%3A%3A%5Bon_extended%28%29%5D&labels=documentation&body=Documentation+under+heading+%22peer_plugin%3A%3A%5Bon_extended%28%29%5D%22+could+be+improved)]

## on\_extended()

```cpp
virtual bool on_extended (int /*length*/, int /*msg*/,
      span<char const> /*body*/);
```

called when an extended message is received. If returning true,
the message is not processed by any other [plugin](reference-Plugins.md#plugin) and if false
is returned the next [plugin](reference-Plugins.md#plugin) in the chain will receive it to
be able to handle it. This is not called for web seeds.
thus function may be called more than once per incoming message, but
only the last of the calls will the body size equal the length.
i.e. Every time another fragment of the message is received, this
function will be called, until finally the whole message has been
received. The purpose of this is to allow early disconnects for invalid
messages and for reporting progress of receiving large messages.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:peer_plugin%3A%3A%5Bon_unknown_message%28%29%5D&labels=documentation&body=Documentation+under+heading+%22peer_plugin%3A%3A%5Bon_unknown_message%28%29%5D%22+could+be+improved)]

## on\_unknown\_message()

```cpp
virtual bool on_unknown_message (int /*length*/, int /*msg*/,
      span<char const> /*body*/);
```

this is not called for web seeds

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:peer_plugin%3A%3A%5Bon_piece_pass%28%29+on_piece_failed%28%29%5D&labels=documentation&body=Documentation+under+heading+%22peer_plugin%3A%3A%5Bon_piece_pass%28%29+on_piece_failed%28%29%5D%22+could+be+improved)]

## on\_piece\_pass() on\_piece\_failed()

```cpp
virtual void on_piece_failed (piece_index_t);
virtual void on_piece_pass (piece_index_t);
```

called when a piece that this peer participated in either
fails or passes the hash\_check

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:peer_plugin%3A%3A%5Btick%28%29%5D&labels=documentation&body=Documentation+under+heading+%22peer_plugin%3A%3A%5Btick%28%29%5D%22+could+be+improved)]

## tick()

```cpp
virtual void tick ();
```

called approximately once every second

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:peer_plugin%3A%3A%5Bwrite_request%28%29%5D&labels=documentation&body=Documentation+under+heading+%22peer_plugin%3A%3A%5Bwrite_request%28%29%5D%22+could+be+improved)]

## write\_request()

```cpp
virtual bool write_request (peer_request const&);
```

called each time a request message is to be sent. If true
is returned, the original request message won't be sent and
no other [plugin](reference-Plugins.md#plugin) will have this function called.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:class+crypto_plugin&labels=documentation&body=Documentation+under+heading+%22class+crypto_plugin%22+could+be+improved)]

# crypto\_plugin

Declared in "[libtorrent/extensions.hpp](include/libtorrent/extensions.hpp)"

```cpp
struct crypto_plugin
{
   virtual void set_outgoing_key (span<char const> key) = 0;
   virtual void set_incoming_key (span<char const> key) = 0;
   encrypt (span<span<char>> /*send_vec*/) = 0;
   virtual std::tuple<int, int, int> decrypt (span<span<char>> /*receive_vec*/) = 0;
};
```

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:crypto_plugin%3A%3A%5Bdecrypt%28%29%5D&labels=documentation&body=Documentation+under+heading+%22crypto_plugin%3A%3A%5Bdecrypt%28%29%5D%22+could+be+improved)]

## decrypt()

```cpp
virtual std::tuple<int, int, int> decrypt (span<span<char>> /*receive_vec*/) = 0;
```

decrypt the provided buffers.
returns is a tuple representing the values
(consume, produce, packet\_size)

consume is set to the number of bytes which should be trimmed from the
head of the buffers, default is 0

produce is set to the number of bytes of payload which are now ready to
be sent to the upper layer. default is the number of bytes passed in receive\_vec

packet\_size is set to the minimum number of bytes which must be read to
advance the next step of decryption. default is 0

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:create_smart_ban_plugin%28%29&labels=documentation&body=Documentation+under+heading+%22create_smart_ban_plugin%28%29%22+could+be+improved)]

# create\_smart\_ban\_plugin()

Declared in "[libtorrent/extensions/smart\_ban.hpp](include/libtorrent/extensions/smart_ban.hpp)"

```cpp
std::shared_ptr<torrent_plugin> create_smart_ban_plugin (torrent_handle const&, client_data_t);
```

constructor function for the smart ban extension. The extension keeps
track of the data peers have sent us for failing pieces and once the
piece completes and passes the hash check bans the peers that turned
out to have sent corrupt data.
This function can either be passed in the add\_torrent\_params::extensions
field, or via [torrent\_handle::add\_extension()](reference-Torrent_Handle.md#add_extension()).

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:create_ut_pex_plugin%28%29&labels=documentation&body=Documentation+under+heading+%22create_ut_pex_plugin%28%29%22+could+be+improved)]

# create\_ut\_pex\_plugin()

Declared in "[libtorrent/extensions/ut\_pex.hpp](include/libtorrent/extensions/ut_pex.hpp)"

```cpp
std::shared_ptr<torrent_plugin> create_ut_pex_plugin (torrent_handle const&, client_data_t);
```

constructor function for the ut\_pex extension. The ut\_pex
extension allows peers to gossip about their connections, allowing
the swarm stay well connected and peers aware of more peers in the
swarm. This extension is enabled by default unless explicitly disabled in
the [session](reference-Session.md#session) constructor.

This can either be passed in the add\_torrent\_params::extensions field, or
via [torrent\_handle::add\_extension()](reference-Torrent_Handle.md#add_extension()).

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:create_ut_metadata_plugin%28%29&labels=documentation&body=Documentation+under+heading+%22create_ut_metadata_plugin%28%29%22+could+be+improved)]

# create\_ut\_metadata\_plugin()

Declared in "[libtorrent/extensions/ut\_metadata.hpp](include/libtorrent/extensions/ut_metadata.hpp)"

```cpp
std::shared_ptr<torrent_plugin> create_ut_metadata_plugin (torrent_handle const&, client_data_t);
```

constructor function for the ut\_metadata extension. The ut\_metadata
extension allows peers to request the .torrent file (or more
specifically the info-dictionary of the .torrent file) from each
other. This is the main building block in making magnet links work.
This extension is enabled by default unless explicitly disabled in
the [session](reference-Session.md#session) constructor.

This can either be passed in the add\_torrent\_params::extensions field, or
via [torrent\_handle::add\_extension()](reference-Torrent_Handle.md#add_extension()).
