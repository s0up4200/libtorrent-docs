---
title: "Upgrading to libtorrent 2.0"
source: "https://libtorrent.org/upgrade_to_2.0-ref.html"
---

# Upgrading to libtorrent 2.0

In libtorrent 2.0, some parts of the API has changed and some deprecated parts
have been removed.
This document summarizes the changes affecting library clients.

# C++11 no longer supported

libtorrent 2.0 requires at least C++-14. To build with boost build, specify the
C++ version using the cxxstd=14 build feature (14 is the default).

# boost version

The oldest boost version supported is 1.67

# BitTorrent v2 support

Supporting bittorrent v2 come with some changes to the API. Specifically to
support *hybrid* torrents. i.e. torrents that are compatible with v1-only
bittorrent clients as well as supporting v2 features among the peers that
support them.

## Example torrents

* [bittorrent-v2-hybrid-test.torrent](https://libtorrent.org/bittorrent-v2-hybrid-test.torrent)
* [bittorrent-v2-test.torrent](https://libtorrent.org/bittorrent-v2-test.torrent)

## info-hashes

With bittorrent v2 support, each torrent may now have two separate info hashes,
one SHA-1 hash and one SHA-256 hash. These are bundled in a new type called
[info\_hash\_t](reference-Core.md#info_hash_t). Many places that previously took an info-hash as sha1\_hash now
takes an [info\_hash\_t](reference-Core.md#info_hash_t). For backwards compatibility, [info\_hash\_t](reference-Core.md#info_hash_t) is implicitly
convertible to and from sha1\_hash and is interpreted as the v1 info-hash.
The implicit conversion is deprecated though.

Perhaps most noteworthy is that add\_torrent\_params::info\_hash is now
deprecated in favor of add\_torrent\_params::info\_hashes which is an
[info\_hash\_t](reference-Core.md#info_hash_t).

The alerts [torrent\_removed\_alert](reference-Alerts.md#torrent_removed_alert), [torrent\_deleted\_alert](reference-Alerts.md#torrent_deleted_alert),
[torrent\_delete\_failed\_alert](reference-Alerts.md#torrent_delete_failed_alert) all have info\_hash members. Those members are
now deprecated in favor of an info\_hashes member, which is of type
[info\_hash\_t](reference-Core.md#info_hash_t).

An [info\_hash\_t](reference-Core.md#info_hash_t) object for a hybrid torrent will have both the v1 and v2 hashes
set, it will compare false to a sha1\_hash of *just* the v1 hash.

Calls to [torrent\_handle::info\_hash()](reference-Torrent_Handle.md#info_hash()) may need to be replaced by
[torrent\_handle::info\_hashes()](reference-Torrent_Handle.md#info_hashes()), in order to get both v1 and v2 hashes.

## announce\_entry/tracker changes

On major change in the API is reporting of trackers. Since hybrid torrents
announce once per info-hash (once for v1 and once for v2), the tracker results
are also reported per *bittorrent version*.

Each tracker ([announce\_entry](reference-Trackers.md#announce_entry)) has a list of endpoints. Each corresponding to
a local listen socket. Each listen socket is announced independently. The
[announce\_endpoint](reference-Trackers.md#announce_endpoint) in turn has an array info\_hashes, containing objects of
type [announce\_infohash](reference-Trackers.md#announce_infohash), for each bittorrent version. The array is indexed by
the enum [protocol\_version](reference-Core.md#protocol_version). There are two members, V1 and V2.

Example:

```cpp
std::vector<lt::announce_entry> tr = h.trackers();
for (lt::announce_entry const& ae : h.trackers()) {
    for (lt::announce_endpoint const& aep : ae.endpoints) {
        int version = 1;
        for (lt::announce_infohash const& ai : aep.info_hashes) {
            std::cout << "[V" << version << "] " << ae.tier << " " << ae.url
                << " " << (ih.updating ? "updating" : "")
                << " " << (ih.start_sent ? "start-sent" : "")
                << " fails: " << ih.fails
                << " msg: " << ih.message
                << "\n";
            ++version;
        }
    }
}
```

## Merkle tree support removed

The old merkle tree torrent support has been removed, as BitTorrent v2 has
better support for merkle trees, where each file has its own merkle tree.

This means [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params) no longer has the merkle\_tree member. Instead
it has the new verified\_leaf\_hashes and merkle\_trees members.

It also means the merkle flag for [create\_torrent](reference-Create_Torrents.md#create_torrent) has been removed.
[torrent\_info](reference-Torrent_Info.md#torrent_info) no longer has set\_merkle\_tree() and merkle\_tree() member
functions.

## create\_torrent changes

The [create\_torrent](reference-Create_Torrents.md#create_torrent) class creates *hybrid* torrents by default. i.e. torrents
compatible with both v1 and v2 bittorrent clients.

To create v1-only torrents use the v1\_only flag. To create v2-only torrents,
use the v2\_only flag.

Perhaps the most important addition for v2 torrents is the new member function
[set\_hash2()](reference-Create_Torrents.md#set_hash2()), which is similar to [set\_hash()](reference-Create_Torrents.md#set_hash()), but for the v2-part of a torrent.
One important difference is that v2 hashes are SHA-256 hashes, and they are set
*per file*. In v2 torrents, each file forms a merkle tree and each v2 piece hash
is the SHA-256 merkle root hash of the 16 kiB blocks in that piece.

All v2 torrents have pieces aligned to files, so the optimize\_alignment flag
is no longer relevant (as it's effectively always on). Similarly, the
mutable\_torrent\_support flag is also always on.

pad\_file\_limit and alignment parameters to the [create\_torrent](reference-Create_Torrents.md#create_torrent) constructor
have also been removed. The rules for padding and alignment is well defined for
v2 torrents.

set\_file\_hash() and file\_hash() functions are obsolete, as v2 torrents have
a file\_root() for each file.

## on\_unknown\_torrent() plugin API

Since hybrid torrents have two info-hashes, the [on\_unknown\_torrent()](reference-Plugins.md#on_unknown_torrent()) function
on the [plugin](reference-Plugins.md#plugin) class now takes an [info\_hash\_t](reference-Core.md#info_hash_t) instead of a sha1\_hash.

## socket\_type\_t

There is a new enum class called socket\_type\_t used to identify different
kinds of sockets. In previous versions of libtorrent this was exposed as plain
int with subtly different sets of meanings.

Previously there was an enum value udp, which has been deprecated in favor of utp.

The socket type is exposed in the following alerts, which now use the socket\_type\_t
enum instead of int:

* peer\_connect\_alert
* peer\_disconnected\_alert
* incoming\_connection\_alert
* listen\_failed\_alert
* listen\_succeeded\_alert

# DHT settings

DHT configuration options have previously been set separately from the main client settings.
In libtorrent 2.0 they have been unified into the main [settings\_pack](reference-Settings.md#settings_pack).

Hence, lt::dht::dht\_settings is now deprecated, in favor of the new dht\_\*
settings in [settings\_pack](reference-Settings.md#settings_pack).

Deprecating dht\_settings also causes an API change to the dht custom storage
constructor (see [session\_params](reference-Session.md#session_params)). Instead of taking a dht\_settings object, it
is now passed the full settings\_pack. This is considered a niche interface,
so there is no backward compatibility option provided.

# stats\_alert

The stats\_alert is deprecated. Instead, call session::post\_torrent\_updates().
This will post a [state\_update\_alert](reference-Alerts.md#state_update_alert) containing [torrent\_status](reference-Torrent_Status.md#torrent_status) of all torrents
that have any updates since last time this function was called.

The new mechanism scales a lot better.

# saving and restoring session state

The functions save\_state() and load\_state() on the [session](reference-Session.md#session) object have
been deprecated in favor loading the [session](reference-Session.md#session) state up-front using
[read\_session\_params()](reference-Session.md#read_session_params()) and construct the [session](reference-Session.md#session) from it.

The [session](reference-Session.md#session) state can be acquired, in the form of a [session\_params](reference-Session.md#session_params) object, by
calling session::session\_state().

The [session\_params](reference-Session.md#session_params) object is passed to the [session](reference-Session.md#session) constructor, and will restore
the state from a previous [session](reference-Session.md#session).

Use [read\_session\_params()](reference-Session.md#read_session_params()) and [write\_session\_params()](reference-Session.md#write_session_params()) to serialize and de-serialize
the [session\_params](reference-Session.md#session_params) object.

As a result of this, plugins that wish to save and restore state or settings
must now use the new overload of [load\_state()](reference-Plugins.md#load_state()), that takes a
std::map<std::string, std::string>. Similarly, for saving state, it now has
to be saved to a std::map<std::string, std::string> via the new overload of
[save\_state()](reference-Plugins.md#save_state()).

A lot of [session](reference-Session.md#session) constructors have been deprecated in favor of the ones that take
a [session\_params](reference-Session.md#session_params) object. The [session\_params](reference-Session.md#session_params) object can be implicitly constructed
from a [settings\_pack](reference-Settings.md#settings_pack), to cover one of the now-deprecated constructors. However,
to access this conversion libtorrent/session\_params.hpp must be included.

# userdata is no longer a void\*

The userdata field in [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params) is no longer a raw void pointer.
Instead it is a type-safe [client\_data\_t](reference-Add_Torrent.md#client_data_t) object. [client\_data\_t](reference-Add_Torrent.md#client_data_t) is similar to
std::any, it can hold a pointer of any type by assignment and can be cast
back to that pointer via static\_cast (explicit conversion). However, if the
pointer type it is cast to is not identical to what was assigned, a nullptr
is returned. Note that the type has to be identical in CV-qualifiers as well.

This userdata field affects the [plugin](reference-Plugins.md#plugin) APIs that has this field passed into it.

Additionally, there's now a way to ask a [torrent\_handle](reference-Torrent_Handle.md#torrent_handle) for the userdata, so it is
associated with the torrent itself.

# Adding torrents by URL no longer supported

The URL covers 3 separate features, all deprecated in the previous version and
removed in 2.0.

## downloading over HTTP

One used to be able to add a torrent by specifying an HTTP URL in the
add\_torrent\_params::url member. Libtorrent would download the file and attempt
to load the file as a .torrent file. The [torrent\_handle](reference-Torrent_Handle.md#torrent_handle) in this mode would
not represent a torrent, but a *potential* torrent. Its info-hash was the hash of
the URL until the torrent file could be loaded, at which point the info hash *changed*.
The corresponding torrent\_update\_alert has also been removed. In libtorrent 2.0
info-hashes cannot change. (Although they can be amended with bittorrent v1 or v2
info-hashes).

Instead of using this feature, clients should download the .torrent files
themselves, possibly spawn their own threads, before adding them to the [session](reference-Session.md#session).

## magnet links

The add\_torrent\_params::url could also be used to add torrents by magnet link.
This was also deprecated in the previous version and has been removed in
libtorrent 2.0. Instead, use [parse\_magnet\_uri()](reference-Core.md#parse_magnet_uri()) to construct an [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params)
object to add to the [session](reference-Session.md#session). This also allows the client to alter settings,
such as save\_path, before adding the magnet link.

## async loading of .torrent files

The add\_torrent\_params::url field also supported file:// URLs. This would
use a libtorrent thread to load the file from disk, asynchronously (in the case
of [async\_add\_torrent()](reference-Session.md#async_add_torrent())). This feature has been removed. Clients should instead
load their torrents from disk themselves, before adding them to the [session](reference-Session.md#session).
Possibly spawning their own threads.

# Disk I/O overhaul

In libtorrent 2.0, the disk I/O subsystem underwent a significant update. In
previous versions of libtorrent, each torrent has had its own, isolated,
disk storage object. This was a customization point. In order to share things
like a pool of open file handles across torrents (to have a global limit on
open file descriptors) all storage objects would share a file\_pool object
passed in to them.

In libtorrent 2.0, the default disk I/O uses memory mapped files, which means
a lot more of what used to belong in the disk caching subsystem is now handled
by the kernel. This greatly simplifies the disk code and also has the potential
of making a lot more efficient use of modern disks as well as physical memory.

In this new system, the customization point is the whole disk I/O subsystem.
Instead of configuring a custom storage (implementing storage\_interface) when
adding a torrent, you can now configure a disk subsystem (implementing
[disk\_interface](reference-Custom_Storage.md#disk_interface)) when creating a [session](reference-Session.md#session).

Systems that don't support memory mapped files can still be used with a simple
fopen()/fclose() family of functions. This disk subsystem is also not threaded
and generally more primitive than the memory mapped file one.

Clients that need to customize storage should implement the [disk\_interface](reference-Custom_Storage.md#disk_interface) and
configure it at [session](reference-Session.md#session) creation time instead of storage\_interface configured
in [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params). [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params) no longer has a storage\_constructor
member.

As a consequence of this, get\_storage\_impl() has been removed from [torrent\_handle](reference-Torrent_Handle.md#torrent_handle).

## aio\_threads and hashing\_threads

In previous versions of libtorrent, the number of disk threads to use were
configured by [settings\_pack::aio\_threads](reference-Settings.md#aio_threads). Every fourth thread was dedicated to
run hash jobs, i.e. computing SHA-1 piece hashes to compare them against the
expected hash.

This setting has now been split up to allow controlling the number of dedicated
hash threads independently from the number of generic disk I/O threads.
[settings\_pack::hashing\_threads](reference-Settings.md#hashing_threads) is now used to control the number of threads
dedicated to computing hashes.

## cache\_size

The cache\_size setting is no longer used. The caching of disk I/O is handled
by the operating system.

## get\_cache\_info() get\_cache\_status()

Since libtorrent no longer manages the disk cache (except for a store-buffer),
get\_cache\_info() and get\_cache\_status() on the [session](reference-Session.md#session) object has also
been removed. They cannot return anything useful.

# last remnants of RSS support removed

The rss\_notification [alert](reference-Alerts.md#alert) category flag has been removed, which has been unused
and deprecated since libtorrent 1.2.

The uuid member of [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params) has been removed. Torrents can no longer
be added under a specific UUID. This feature was specifically meant for RSS feeds,
which was removed in the previous version of libtorrent.
