---
title: "settings_pack"
source: "https://libtorrent.org/reference-Settings.html"
---

[home](reference.md)

You have some control over [session](reference-Session.md#session) configuration through the session::apply\_settings()
member function. To change one or more configuration options, create a [settings\_pack](reference-Settings.md#settings_pack)
object and fill it with the settings to be set and pass it in to session::apply\_settings().

The [settings\_pack](reference-Settings.md#settings_pack) object is a collection of settings updates that are applied
to the [session](reference-Session.md#session) when passed to session::apply\_settings(). It's empty when
constructed.

You have control over proxy and authorization settings and also the user-agent
that will be sent to the tracker. The user-agent will also be used to identify the
client with other peers.

Each configuration option is named with an enum value inside the
[settings\_pack](reference-Settings.md#settings_pack) class. These are the available settings:

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:class+settings_pack&labels=documentation&body=Documentation+under+heading+%22class+settings_pack%22+could+be+improved)]

# settings\_pack

Declared in "[libtorrent/settings\_pack.hpp](include/libtorrent/settings_pack.hpp)"

The settings\_pack struct, contains the names of all settings as
enum values. These values are passed in to the set\_str(),
set\_int(), set\_bool() functions, to specify the setting to
change.

The settings\_pack only stores values for settings that have been
explicitly set on this object. However, it can still be queried for
settings that have not been set and returns the default value for those
settings.

| name | type | default |
| --- | --- | --- |
| user\_agent | string | libtorrent/ |

this is the client identification to the tracker. The recommended
format of this string is: "client-name/client-version
libtorrent/libtorrent-version". This name will not only be used when
making HTTP requests, but also when sending extended headers to
peers that support that extension. It may not contain r or n

| name | type | default |
| --- | --- | --- |
| announce\_ip | string | nullptr |

announce\_ip is the ip address passed along to trackers as the
&ip= parameter. If left as the default, that parameter is
omitted.

Note

This setting is only meant for very special cases where a seed is
running on the same host as the tracker, and the tracker accepts
the IP parameter (which normal trackers don't). Do not set this
option unless you also control the tracker.

| name | type | default |
| --- | --- | --- |
| handshake\_client\_version | string | nullptr |

this is the client name and version identifier sent to peers in the
handshake message. If this is an empty string, the user\_agent is
used instead. This string must be a UTF-8 encoded unicode string.

| name | type | default |
| --- | --- | --- |
| outgoing\_interfaces | string |  |

This controls which IP address outgoing TCP peer connections are bound
to, in addition to controlling whether such connections are also
bound to a specific network interface/adapter (*bind-to-device*).

This string is a comma-separated list of IP addresses and
interface names. An empty string will not bind TCP sockets to a
device, and let the network stack assign the local address.

A list of names will be used to bind outgoing TCP sockets in a
round-robin fashion. An IP address will simply be used to bind()
the socket. An interface name will attempt to bind the socket to
that interface. If that fails, or is unsupported, one of the IP
addresses configured for that interface is used to bind() the
socket to. If the interface or adapter doesn't exist, the
outgoing peer connection will fail with an error message suggesting
the device cannot be found. Adapter names on Unix systems are of
the form "eth0", "eth1", "tun0", etc. This may be useful for
clients that are multi-homed. Binding an outgoing connection to a
local IP does not necessarily make the connection via the
associated NIC/Adapter.

When outgoing interfaces are specified, incoming connections or
packets sent to a local interface or IP that's *not* in this list
will be rejected with a [peer\_blocked\_alert](reference-Alerts.md#peer_blocked_alert) with
invalid\_local\_interface as the reason.

Note that these are just interface/adapter names or IP addresses.
There are no ports specified in this list. IPv6 addresses without
port should be specified without enclosing [, ].

| name | type | default |
| --- | --- | --- |
| listen\_interfaces | string | 0.0.0.0:6881,[::]:6881 |

a comma-separated list of (IP or device name, port) pairs. These are
the listen ports that will be opened for accepting incoming uTP and
TCP peer connections. These are also used for *outgoing* uTP and UDP
tracker connections and DHT nodes.

It is possible to listen on multiple interfaces and
multiple ports. Binding to port 0 will make the operating system
pick the port.

Note

There are reasons to stick to the same port across sessions,
which would mean only using port 0 on the first start, and
recording the port that was picked for subsequent startups.
Trackers, the DHT and other peers will remember the port they see
you use and hand that port out to other peers trying to connect
to you, as well as trying to connect to you themselves.

A port that has an "s" suffix will accept SSL peer connections. (note
that SSL sockets are only available in builds with SSL support)

A port that has an "l" suffix will be considered a local network.
i.e. it's assumed to only be able to reach hosts in the same local
network as the IP address (based on the netmask associated with the
IP, queried from the operating system).

if binding fails, the [listen\_failed\_alert](reference-Alerts.md#listen_failed_alert) is posted. Once a
socket binding succeeds (if it does), the [listen\_succeeded\_alert](reference-Alerts.md#listen_succeeded_alert)
is posted. There may be multiple failures before a success.

If a device name that does not exist is configured, no listen
socket will be opened for that interface. If this is the only
interface configured, it will be as if no listen ports are
configured.

If no listen ports are configured (e.g. listen\_interfaces is an
empty string), networking will be disabled. No DHT will start, no
outgoing uTP or tracker connections will be made. No incoming TCP
or uTP connections will be accepted. (outgoing TCP connections
will still be possible, depending on
[settings\_pack::outgoing\_interfaces](reference-Settings.md#outgoing_interfaces)).

For example:
[::1]:8888 - will only accept connections on the IPv6 loopback
address on port 8888.

eth0:4444,eth1:4444 - will accept connections on port 4444 on
any IP address bound to device eth0 or eth1.

[::]:0s - will accept SSL connections on a port chosen by the
OS. And not accept non-SSL connections at all.

0.0.0.0:6881,[::]:6881 - binds to all interfaces on port 6881.

10.0.1.13:6881l - binds to the local IP address, port 6881, but
only allow talking to peers on the same local network. The netmask
is queried from the operating system. Interfaces marked l are
not announced to trackers, unless the tracker is also on the same
local network.

Windows OS network adapter device name must be specified with GUID.
It can be obtained from "netsh lan show interfaces" command output.
GUID must be uppercased string embraced in curly brackets.
{E4F0B674-0DFC-48BB-98A5-2AA730BDB6D6}:7777 - will accept
connections on port 7777 on adapter with this GUID.

For more information, see the [Multi-homed hosts](manual-ref.md#multi-homed-hosts) section.

| name | type | default |
| --- | --- | --- |
| proxy\_hostname | string |  |

when using a proxy, this is the hostname where the proxy is running
see proxy\_type. Note that when using a proxy, the
[settings\_pack::listen\_interfaces](reference-Settings.md#listen_interfaces) setting is overridden and only a
single interface is created, just to contact the proxy. This
means a proxy cannot be combined with SSL torrents or multiple
listen interfaces. This proxy listen interface will not accept
incoming TCP connections, will not map ports with any gateway and
will not enable local service discovery. All traffic is supposed
to be channeled through the proxy.

| name | type | default |
| --- | --- | --- |
| proxy\_username | string |  |
| proxy\_password | string |  |

when using a proxy, these are the credentials (if any) to use when
connecting to it. see proxy\_type

| name | type | default |
| --- | --- | --- |
| i2p\_hostname | string |  |

sets the [i2p](http://www.i2p2.de) SAM bridge to connect to. set the port with the
i2p\_port setting. Unless this is set, i2p torrents are not
supported. This setting is separate from the other proxy settings
since i2p torrents and their peers are orthogonal. You can have
i2p peers as well as regular peers via a proxy.

| name | type | default |
| --- | --- | --- |
| peer\_fingerprint | string | -LT20B0- |

this is the fingerprint for the client. It will be used as the
prefix to the peer\_id. If this is 20 bytes (or longer) it will be
truncated to 20 bytes and used as the entire peer-id

There is a utility function, [generate\_fingerprint()](reference-Settings.md#generate_fingerprint()) that can be used
to generate a standard client peer ID fingerprint prefix.

| name | type | default |
| --- | --- | --- |
| dht\_bootstrap\_nodes | string | dht.libtorrent.org:25401 |

This is a comma-separated list of IP port-pairs. They will be added
to the DHT node (if it's enabled) as back-up nodes in case we don't
know of any.

Changing these after the DHT has been started may not have any
effect until the DHT is restarted.
Here are some other bootstrap nodes that may work:
router.bittorrent.com:6881,
dht.transmissionbt.com:6881
router.bt.ouinet.work:6881,

| name | type | default |
| --- | --- | --- |
| allow\_multiple\_connections\_per\_ip | bool | false |

determines if connections from the same IP address as existing
connections should be rejected or not. Rejecting multiple connections
from the same IP address will prevent abusive
behavior by peers. The logic for determining whether connections are
to the same peer is more complicated with this enabled, and more
likely to fail in some edge cases. It is not recommended to enable
this feature.

| name | type | default |
| --- | --- | --- |
| send\_redundant\_have | bool | true |

send\_redundant\_have controls if have messages will be sent to
peers that already have the piece. This is typically not necessary,
but it might be necessary for collecting statistics in some cases.

| name | type | default |
| --- | --- | --- |
| use\_dht\_as\_fallback | bool | false |

use\_dht\_as\_fallback determines how the DHT is used. If this is
true, the DHT will only be used for torrents where all trackers in
its tracker list has failed. Either by an explicit error message or
a time out. If this is false, the DHT is used regardless of if the
trackers fail or not.

| name | type | default |
| --- | --- | --- |
| upnp\_ignore\_nonrouters | bool | false |

upnp\_ignore\_nonrouters indicates whether or not the UPnP
implementation should ignore any broadcast response from a device
whose address is not on our subnet. i.e.
it's a way to not talk to other people's routers by mistake.

| name | type | default |
| --- | --- | --- |
| use\_parole\_mode | bool | true |

use\_parole\_mode specifies if parole mode should be used. Parole
mode means that peers that participate in pieces that fail the hash
check are put in a mode where they are only allowed to download
whole pieces. If the whole piece a peer in parole mode fails the
hash check, it is banned. If a peer participates in a piece that
passes the hash check, it is taken out of parole mode.

| name | type | default |
| --- | --- | --- |
| auto\_manage\_prefer\_seeds | bool | false |

if true, prefer seeding torrents when determining which torrents to give
active slots to. If false, give preference to downloading torrents

| name | type | default |
| --- | --- | --- |
| dont\_count\_slow\_torrents | bool | true |

if dont\_count\_slow\_torrents is true, torrents without any
payload transfers are not subject to the active\_seeds and
active\_downloads limits. This is intended to make it more
likely to utilize all available bandwidth, and avoid having
torrents that don't transfer anything block the active slots.

| name | type | default |
| --- | --- | --- |
| close\_redundant\_connections | bool | true |

close\_redundant\_connections specifies whether libtorrent should
close connections where both ends have no utility in keeping the
connection open. For instance if both ends have completed their
downloads, there's no point in keeping it open.

| name | type | default |
| --- | --- | --- |
| prioritize\_partial\_pieces | bool | false |

If prioritize\_partial\_pieces is true, partial pieces are picked
before pieces that are more rare. If false, rare pieces are always
prioritized, unless the number of partial pieces is growing out of
proportion.

| name | type | default |
| --- | --- | --- |
| rate\_limit\_ip\_overhead | bool | true |

if set to true, the estimated TCP/IP overhead is drained from the
rate limiters, to avoid exceeding the limits with the total traffic

| name | type | default |
| --- | --- | --- |
| announce\_to\_all\_tiers | bool | false |
| announce\_to\_all\_trackers | bool | false |

announce\_to\_all\_trackers controls how multi tracker torrents
are treated. If this is set to true, all trackers in the same tier
are announced to in parallel. If all trackers in tier 0 fails, all
trackers in tier 1 are announced as well. If it's set to false, the
behavior is as defined by the multi tracker specification.

announce\_to\_all\_tiers also controls how multi tracker torrents
are treated. When this is set to true, one tracker from each tier
is announced to. This is the uTorrent behavior. To be compliant
with the Multi-tracker specification, set it to false.

| name | type | default |
| --- | --- | --- |
| prefer\_udp\_trackers | bool | true |

prefer\_udp\_trackers: true means that trackers
may be rearranged in a way that udp trackers are always tried
before http trackers for the same hostname. Setting this to false
means that the tracker's tier is respected and there's no
preference of one protocol over another.

| name | type | default |
| --- | --- | --- |
| disable\_hash\_checks | bool | false |

when set to true, all data downloaded from peers will be assumed to
be correct, and not tested to match the hashes in the torrent this
is only useful for simulation and testing purposes (typically
combined with disabled\_storage)

| name | type | default |
| --- | --- | --- |
| allow\_i2p\_mixed | bool | false |

if this is true, i2p torrents are allowed to also get peers from
other sources than the tracker, and connect to regular IPs, not
providing any anonymization. This may be useful if the user is not
interested in the anonymization of i2p, but still wants to be able
to connect to i2p peers.

| name | type | default |
| --- | --- | --- |
| no\_atime\_storage | bool | true |

no\_atime\_storage this is a Linux-only option and passes in the
O\_NOATIME to open() when opening files. This may lead to
some disk performance improvements.

| name | type | default |
| --- | --- | --- |
| incoming\_starts\_queued\_torrents | bool | false |

incoming\_starts\_queued\_torrents. If a torrent
has been paused by the auto managed feature in libtorrent, i.e. the
torrent is paused and auto managed, this feature affects whether or
not it is automatically started on an incoming connection. The main
reason to queue torrents, is not to make them unavailable, but to
save on the overhead of announcing to the trackers, the DHT and to
avoid spreading one's unchoke slots too thin. If a peer managed to
find us, even though we're no in the torrent anymore, this setting
can make us start the torrent and serve it.

| name | type | default |
| --- | --- | --- |
| report\_true\_downloaded | bool | false |

when set to true, the downloaded counter sent to trackers will
include the actual number of payload bytes downloaded including
redundant bytes. If set to false, it will not include any redundancy
bytes

| name | type | default |
| --- | --- | --- |
| strict\_end\_game\_mode | bool | true |

strict\_end\_game\_mode controls when a
block may be requested twice. If this is true, a block may only
be requested twice when there's at least one request to every piece
that's left to download in the torrent. This may slow down progress
on some pieces sometimes, but it may also avoid downloading a lot
of redundant bytes. If this is false, libtorrent attempts to
use each peer connection to its max, by always requesting
something, even if it means requesting something that has been
requested from another peer already.

| name | type | default |
| --- | --- | --- |
| enable\_outgoing\_utp | bool | true |
| enable\_incoming\_utp | bool | true |
| enable\_outgoing\_tcp | bool | true |
| enable\_incoming\_tcp | bool | true |

Enables incoming and outgoing, TCP and uTP peer connections.
false is disabled and true is enabled. When outgoing
connections are disabled, libtorrent will simply not make
outgoing peer connections with the specific transport protocol.
Disabled incoming peer connections will simply be rejected.
These options only apply to peer connections, not tracker- or any
other kinds of connections.

| name | type | default |
| --- | --- | --- |
| no\_recheck\_incomplete\_resume | bool | false |

no\_recheck\_incomplete\_resume determines if the storage should
check the whole files when resume data is incomplete or missing or
whether it should simply assume we don't have any of the data. If
false, any existing files will be checked.
By setting this setting to true, the files won't be checked, but
will go straight to download mode.

| name | type | default |
| --- | --- | --- |
| anonymous\_mode | bool | false |

anonymous\_mode: When set to true, the client tries to hide
its identity to a certain degree.

* A generic user-agent will be
  used for trackers (except for private torrents).
* Your local IPv4 and IPv6 address won't be sent as query string
  parameters to private trackers.
* If announce\_ip is configured, it will not be sent to trackers
* The client version will not be sent to peers in the extension
  handshake.

| name | type | default |
| --- | --- | --- |
| report\_web\_seed\_downloads | bool | true |

specifies whether downloads from web seeds is reported to the
tracker or not. Turning it off also excludes web
seed traffic from other stats and download rate reporting via the
libtorrent API.

| name | type | default |
| --- | --- | --- |
| seeding\_outgoing\_connections | bool | true |

seeding\_outgoing\_connections determines if seeding (and
finished) torrents should attempt to make outgoing connections or
not. It may be set to false in very
specific applications where the cost of making outgoing connections
is high, and there are no or small benefits of doing so. For
instance, if no nodes are behind a firewall or a NAT, seeds don't
need to make outgoing connections.

| name | type | default |
| --- | --- | --- |
| no\_connect\_privileged\_ports | bool | false |

when this is true, libtorrent will not attempt to make outgoing
connections to peers whose port is < 1024. This is a safety
precaution to avoid being part of a DDoS attack

| name | type | default |
| --- | --- | --- |
| smooth\_connects | bool | true |

smooth\_connects means the number of
connection attempts per second may be limited to below the
connection\_speed, in case we're close to bump up against the
limit of number of connections. The intention of this setting is to
more evenly distribute our connection attempts over time, instead
of attempting to connect in batches, and timing them out in
batches.

| name | type | default |
| --- | --- | --- |
| always\_send\_user\_agent | bool | false |

always send user-agent in every web seed request. If false, only
the first request per http connection will include the user agent

| name | type | default |
| --- | --- | --- |
| apply\_ip\_filter\_to\_trackers | bool | true |

apply\_ip\_filter\_to\_trackers determines
whether the IP filter applies to trackers as well as peers. If this
is set to false, trackers are exempt from the IP filter (if there
is one). If no IP filter is set, this setting is irrelevant.

| name | type | default |
| --- | --- | --- |
| ban\_web\_seeds | bool | true |

when true, web seeds sending bad data will be banned

| name | type | default |
| --- | --- | --- |
| support\_share\_mode | bool | true |

if false, prevents libtorrent to advertise share-mode support

| name | type | default |
| --- | --- | --- |
| report\_redundant\_bytes | bool | true |

if this is true, the number of redundant bytes is sent to the
tracker

| name | type | default |
| --- | --- | --- |
| listen\_system\_port\_fallback | bool | true |

if this is true, libtorrent will fall back to listening on a port
chosen by the operating system (i.e. binding to port 0). If a
failure is preferred, set this to false.

| name | type | default |
| --- | --- | --- |
| announce\_crypto\_support | bool | true |

when this is true, and incoming encrypted connections are enabled,
&supportcrypt=1 is included in http tracker announces

| name | type | default |
| --- | --- | --- |
| enable\_upnp | bool | true |

Starts and stops the UPnP service. When started, the listen port
and the DHT port are attempted to be forwarded on local UPnP router
devices.

The upnp object returned by start\_upnp() can be used to add and
remove arbitrary port mappings. Mapping status is returned through
the [portmap\_alert](reference-Alerts.md#portmap_alert) and the [portmap\_error\_alert](reference-Alerts.md#portmap_error_alert). The object will be
valid until stop\_upnp() is called. See [upnp and nat pmp](manual-ref.md#upnp-and-nat-pmp).

| name | type | default |
| --- | --- | --- |
| enable\_natpmp | bool | true |

Starts and stops the NAT-PMP service. When started, the listen port
and the DHT port are attempted to be forwarded on the router
through NAT-PMP.

The natpmp object returned by start\_natpmp() can be used to add
and remove arbitrary port mappings. Mapping status is returned
through the [portmap\_alert](reference-Alerts.md#portmap_alert) and the [portmap\_error\_alert](reference-Alerts.md#portmap_error_alert). The object
will be valid until stop\_natpmp() is called. See
[upnp and nat pmp](manual-ref.md#upnp-and-nat-pmp).

| name | type | default |
| --- | --- | --- |
| enable\_lsd | bool | true |

Starts and stops Local Service Discovery. This service will
broadcast the info-hashes of all the non-private torrents on the
local network to look for peers on the same swarm within multicast
reach.

| name | type | default |
| --- | --- | --- |
| enable\_dht | bool | true |

starts the dht node and makes the trackerless service available to
torrents.

| name | type | default |
| --- | --- | --- |
| prefer\_rc4 | bool | false |

if the allowed encryption level is both, setting this to true will
prefer RC4 if both methods are offered, plain text otherwise

| name | type | default |
| --- | --- | --- |
| proxy\_hostnames | bool | true |

if true, hostname lookups are done via the configured proxy (if
any). This is only supported by SOCKS5 and HTTP.

| name | type | default |
| --- | --- | --- |
| proxy\_peer\_connections | bool | true |

if true, peer connections are made (and accepted) over the
configured proxy, if any. Web seeds as well as regular bittorrent
peer connections are considered "peer connections". Anything
transporting actual torrent payload (trackers and DHT traffic are
not considered peer connections).

| name | type | default |
| --- | --- | --- |
| auto\_sequential | bool | true |

if this setting is true, torrents with a very high availability of
pieces (and seeds) are downloaded sequentially. This is more
efficient for the disk I/O. With many seeds, the download order is
unlikely to matter anyway

| name | type | default |
| --- | --- | --- |
| proxy\_tracker\_connections | bool | true |

if true, tracker connections are made over the configured proxy, if
any.

| name | type | default |
| --- | --- | --- |
| enable\_ip\_notifier | bool | true |

Starts and stops the internal IP table route changes notifier.

The current implementation supports multiple platforms, and it is
recommended to have it enable, but you may want to disable it if
it's supported but unreliable, or if you have a better way to
detect the changes. In the later case, you should manually call
session\_handle::reopen\_network\_sockets to ensure network
changes are taken in consideration.

| name | type | default |
| --- | --- | --- |
| dht\_prefer\_verified\_node\_ids | bool | true |

when this is true, nodes whose IDs are derived from their source
IP according to [BEP 42](https://www.bittorrent.org/beps/bep_0042.html) are preferred in the routing table.

| name | type | default |
| --- | --- | --- |
| dht\_restrict\_routing\_ips | bool | true |

determines if the routing table entries should restrict entries to one
per IP. This defaults to true, which helps mitigate some attacks on
the DHT. It prevents adding multiple nodes with IPs with a very close
CIDR distance.

when set, nodes whose IP address that's in the same /24 (or /64 for
IPv6) range in the same routing table bucket. This is an attempt to
mitigate node ID spoofing attacks also restrict any IP to only have a
single [entry](reference-Bencoding.md#entry) in the whole routing table

| name | type | default |
| --- | --- | --- |
| dht\_restrict\_search\_ips | bool | true |

determines if DHT searches should prevent adding nodes with IPs with
very close CIDR distance. This also defaults to true and helps
mitigate certain attacks on the DHT.

| name | type | default |
| --- | --- | --- |
| dht\_extended\_routing\_table | bool | true |

makes the first buckets in the DHT routing table fit 128, 64, 32 and
16 nodes respectively, as opposed to the standard size of 8. All other
buckets have size 8 still.

| name | type | default |
| --- | --- | --- |
| dht\_aggressive\_lookups | bool | true |

slightly changes the lookup behavior in terms of how many outstanding
requests we keep. Instead of having branch factor be a hard limit, we
always keep *branch factor* outstanding requests to the closest nodes.
i.e. every time we get results back with closer nodes, we query them
right away. It lowers the lookup times at the cost of more outstanding
queries.

| name | type | default |
| --- | --- | --- |
| dht\_privacy\_lookups | bool | false |

when set, perform lookups in a way that is slightly more expensive,
but which minimizes the amount of information leaked about you.

| name | type | default |
| --- | --- | --- |
| dht\_enforce\_node\_id | bool | false |

when set, node's whose IDs that are not correctly generated based on
its external IP are ignored. When a query arrives from such node, an
error message is returned with a message saying "invalid node ID".

| name | type | default |
| --- | --- | --- |
| dht\_ignore\_dark\_internet | bool | true |

ignore DHT messages from parts of the internet we wouldn't expect to
see any traffic from

| name | type | default |
| --- | --- | --- |
| dht\_read\_only | bool | false |

when set, the other nodes won't keep this node in their routing
tables, it's meant for low-power and/or ephemeral devices that
cannot support the DHT, it is also useful for mobile devices which
are sensitive to network traffic and battery life.
this node no longer responds to 'query' messages, and will place a
'ro' key (value = 1) in the top-level message dictionary of outgoing
query messages.

| name | type | default |
| --- | --- | --- |
| piece\_extent\_affinity | bool | false |

when this is true, create an affinity for downloading 4 MiB extents
of adjacent pieces. This is an attempt to achieve better disk I/O
throughput by downloading larger extents of bytes, for torrents with
small piece sizes

| name | type | default |
| --- | --- | --- |
| validate\_https\_trackers | bool | true |

when set to true, the certificate of HTTPS trackers and HTTPS web
seeds will be validated against the system's certificate store
(as defined by OpenSSL). If the system does not have a
certificate store, this option may have to be disabled in order
to get trackers and web seeds to work).

| name | type | default |
| --- | --- | --- |
| ssrf\_mitigation | bool | true |

when enabled, tracker and web seed requests are subject to
certain restrictions.

An HTTP(s) tracker requests to localhost (loopback)
must have the request path start with "/announce". This is the
conventional bittorrent tracker request. Any other HTTP(S)
tracker request to loopback will be rejected. This applies to
trackers that redirect to loopback as well.

Web seeds that end up on the client's local network (i.e. in a
private IP address range) may not include query string arguments.
This applies to web seeds redirecting to the local network as
well.

Web seeds on global IPs (i.e. not local network) may not redirect
to a local network address

| name | type | default |
| --- | --- | --- |
| allow\_idna | bool | false |

when disabled, any tracker or web seed with an IDNA hostname
(internationalized domain name) is ignored. This is a security
precaution to avoid various unicode encoding attacks that might
happen at the application level.

| name | type | default |
| --- | --- | --- |
| enable\_set\_file\_valid\_data | bool | false |

when set to true, enables the attempt to use SetFileValidData()
to pre-allocate disk space. This system call will only work when
running with Administrator privileges on Windows, and so this
setting is only relevant in that scenario. Using
SetFileValidData() poses a security risk, as it may reveal
previously deleted information from the disk.

| name | type | default |
| --- | --- | --- |
| socks5\_udp\_send\_local\_ep | bool | false |

When using a SOCKS5 proxy, UDP traffic is routed through the
proxy by sending a UDP ASSOCIATE command. If this option is true,
the UDP ASSOCIATE command will include the IP address and
listen port to the local UDP socket. This indicates to the proxy
which source endpoint to expect our packets from. The benefit is
that incoming packets can be forwarded correctly, before any
outgoing packets are sent. The risk is that if there's a NAT
between the client and the proxy, the IP address specified in the
protocol may not be valid from the proxy's point of view.

| name | type | default |
| --- | --- | --- |
| tracker\_completion\_timeout | int | 30 |

tracker\_completion\_timeout is the number of seconds the tracker
connection will wait from when it sent the request until it
considers the tracker to have timed-out.

| name | type | default |
| --- | --- | --- |
| tracker\_receive\_timeout | int | 10 |

tracker\_receive\_timeout is the number of seconds to wait to
receive any data from the tracker. If no data is received for this
number of seconds, the tracker will be considered as having timed
out. If a tracker is down, this is the kind of timeout that will
occur.

| name | type | default |
| --- | --- | --- |
| stop\_tracker\_timeout | int | 5 |

stop\_tracker\_timeout is the number of seconds to wait when
sending a stopped message before considering a tracker to have
timed out. This is usually shorter, to make the client quit faster.
If the value is set to 0, the connections to trackers with the
stopped event are suppressed.

| name | type | default |
| --- | --- | --- |
| tracker\_maximum\_response\_length | int | 1024\*1024 |

this is the maximum number of bytes in a tracker response. If a
response size passes this number of bytes it will be rejected and
the connection will be closed. On gzipped responses this size is
measured on the uncompressed data. So, if you get 20 bytes of gzip
response that'll expand to 2 megabytes, it will be interrupted
before the entire response has been uncompressed (assuming the
limit is lower than 2 MiB).

| name | type | default |
| --- | --- | --- |
| piece\_timeout | int | 20 |

the number of seconds from a request is sent until it times out if
no piece response is returned.

| name | type | default |
| --- | --- | --- |
| request\_timeout | int | 60 |

the number of seconds one block (16 kiB) is expected to be received
within. If it's not, the block is requested from a different peer

| name | type | default |
| --- | --- | --- |
| request\_queue\_time | int | 3 |

the length of the request queue given in the number of seconds it
should take for the other end to send all the pieces. i.e. the
actual number of requests depends on the download rate and this
number.

| name | type | default |
| --- | --- | --- |
| max\_allowed\_in\_request\_queue | int | 2000 |

the number of outstanding block requests a peer is allowed to queue
up in the client. If a peer sends more requests than this (before
the first one has been sent) the last request will be dropped. the
higher this is, the faster upload speeds the client can get to a
single peer.

| name | type | default |
| --- | --- | --- |
| max\_out\_request\_queue | int | 500 |

max\_out\_request\_queue is the maximum number of outstanding
requests to send to a peer. This limit takes precedence over
request\_queue\_time. i.e. no matter the download speed, the
number of outstanding requests will never exceed this limit.

| name | type | default |
| --- | --- | --- |
| whole\_pieces\_threshold | int | 20 |

if a whole piece can be downloaded in this number of seconds, or
less, the peer\_connection will prefer to request whole pieces at a
time from this peer. The benefit of this is to better utilize disk
caches by doing localized accesses and also to make it easier to
identify bad peers if a piece fails the hash check.

| name | type | default |
| --- | --- | --- |
| peer\_timeout | int | 120 |

peer\_timeout is the number of seconds the peer connection
should wait (for any activity on the peer connection) before
closing it due to time out. 120 seconds is
specified in the protocol specification. After half
the time out, a keep alive message is sent.

| name | type | default |
| --- | --- | --- |
| urlseed\_timeout | int | 20 |

same as peer\_timeout, but only applies to url-seeds. this is
usually set lower, because web servers are expected to be more
reliable.

| name | type | default |
| --- | --- | --- |
| urlseed\_pipeline\_size | int | 5 |

controls the pipelining size of url and http seeds. i.e. the number of HTTP
request to keep outstanding before waiting for the first one to
complete. It's common for web servers to limit this to a relatively
low number, like 5

| name | type | default |
| --- | --- | --- |
| urlseed\_wait\_retry | int | 30 |

number of seconds until a new retry of a url-seed takes place.
Default retry value for http-seeds that don't provide
a valid retry-after header.

| name | type | default |
| --- | --- | --- |
| file\_pool\_size | int | 40 |

sets the upper limit on the total number of files this [session](reference-Session.md#session) will
keep open. The reason why files are left open at all is that some
anti virus software hooks on every file close, and scans the file
for viruses. deferring the closing of the files will be the
difference between a usable system and a completely hogged down
system. Most operating systems also has a limit on the total number
of file descriptors a process may have open.

| name | type | default |
| --- | --- | --- |
| max\_failcount | int | 3 |

max\_failcount is the maximum times we try to
connect to a peer before stop connecting again. If a
peer succeeds, the failure counter is reset. If a
peer is retrieved from a peer source (other than DHT)
the failcount is decremented by one, allowing another
try.

| name | type | default |
| --- | --- | --- |
| min\_reconnect\_time | int | 60 |

the number of seconds to wait to reconnect to a peer. this time is
multiplied with the failcount.

| name | type | default |
| --- | --- | --- |
| peer\_connect\_timeout | int | 15 |

peer\_connect\_timeout the number of seconds to wait after a
connection attempt is initiated to a peer until it is considered as
having timed out. This setting is especially important in case the
number of half-open connections are limited, since stale half-open
connection may delay the connection of other peers considerably.

| name | type | default |
| --- | --- | --- |
| connection\_speed | int | 30 |

connection\_speed is the number of connection attempts that are
made per second. If a number < 0 is specified, it will default to
200 connections per second. If 0 is specified, it means don't make
outgoing connections at all.

| name | type | default |
| --- | --- | --- |
| inactivity\_timeout | int | 600 |

if a peer is uninteresting and uninterested for longer than this
number of seconds, it will be disconnected.

| name | type | default |
| --- | --- | --- |
| unchoke\_interval | int | 15 |

unchoke\_interval is the number of seconds between
chokes/unchokes. On this interval, peers are re-evaluated for being
choked/unchoked. This is defined as 30 seconds in the protocol, and
it should be significantly longer than what it takes for TCP to
ramp up to it's max rate.

| name | type | default |
| --- | --- | --- |
| optimistic\_unchoke\_interval | int | 30 |

optimistic\_unchoke\_interval is the number of seconds between
each *optimistic* unchoke. On this timer, the currently
optimistically unchoked peer will change.

| name | type | default |
| --- | --- | --- |
| num\_want | int | 200 |

num\_want is the number of peers we want from each tracker
request. It defines what is sent as the &num\_want= parameter to
the tracker.

| name | type | default |
| --- | --- | --- |
| initial\_picker\_threshold | int | 4 |

initial\_picker\_threshold specifies the number of pieces we need
before we switch to rarest first picking. The first
initial\_picker\_threshold pieces in any torrent are picked at random
, the following pieces are picked in rarest first order.

| name | type | default |
| --- | --- | --- |
| allowed\_fast\_set\_size | int | 5 |

the number of allowed pieces to send to peers that supports the
fast extensions

| name | type | default |
| --- | --- | --- |
| suggest\_mode | int | settings\_pack::no\_piece\_suggestions |

suggest\_mode controls whether or not libtorrent will send out
suggest messages to create a bias of its peers to request certain
pieces. The modes are:

* no\_piece\_suggestions which will not send out suggest messages.
* suggest\_read\_cache which will send out suggest messages for
  the most recent pieces that are in the read cache.

| name | type | default |
| --- | --- | --- |
| max\_queued\_disk\_bytes | int | 1024 \* 1024 |

max\_queued\_disk\_bytes is the maximum number of bytes, to
be written to disk, that can wait in the disk I/O thread queue.
This queue is only for waiting for the disk I/O thread to receive
the job and either write it to disk or insert it in the write
cache. When this limit is reached, the peer connections will stop
reading data from their sockets, until the disk thread catches up.
Setting this too low will severely limit your download rate.

| name | type | default |
| --- | --- | --- |
| handshake\_timeout | int | 10 |

the number of seconds to wait for a handshake response from a peer.
If no response is received within this time, the peer is
disconnected.

| name | type | default |
| --- | --- | --- |
| send\_buffer\_low\_watermark | int | 10 \* 1024 |
| send\_buffer\_watermark | int | 500 \* 1024 |
| send\_buffer\_watermark\_factor | int | 50 |

send\_buffer\_low\_watermark the minimum send buffer target size
(send buffer includes bytes pending being read from disk). For good
and snappy seeding performance, set this fairly high, to at least
fit a few blocks. This is essentially the initial window size which
will determine how fast we can ramp up the send rate

if the send buffer has fewer bytes than send\_buffer\_watermark,
we'll read another 16 kiB block onto it. If set too small, upload
rate capacity will suffer. If set too high, memory will be wasted.
The actual watermark may be lower than this in case the upload rate
is low, this is the upper limit.

the current upload rate to a peer is multiplied by this factor to
get the send buffer watermark. The factor is specified as a
percentage. i.e. 50 -> 0.5 This product is clamped to the
send\_buffer\_watermark setting to not exceed the max. For high
speed upload, this should be set to a greater value than 100. For
high capacity connections, setting this higher can improve upload
performance and disk throughput. Setting it too high may waste RAM
and create a bias towards read jobs over write jobs.

| name | type | default |
| --- | --- | --- |
| choking\_algorithm | int | settings\_pack::fixed\_slots\_choker |
| seed\_choking\_algorithm | int | settings\_pack::round\_robin |

choking\_algorithm specifies which algorithm to use to determine
how many peers to unchoke. The unchoking algorithm for
downloading torrents is always "tit-for-tat", i.e. the peers we
download the fastest from are unchoked.

The options for choking algorithms are defined in the
[choking\_algorithm\_t](reference-Settings.md#choking_algorithm_t) enum.

seed\_choking\_algorithm controls the seeding unchoke behavior.
i.e. How we select which peers to unchoke for seeding torrents.
Since a seeding torrent isn't downloading anything, the
tit-for-tat mechanism cannot be used. The available options are
defined in the [seed\_choking\_algorithm\_t](reference-Settings.md#seed_choking_algorithm_t) enum.

| name | type | default |
| --- | --- | --- |
| disk\_io\_write\_mode | int | DISK\_WRITE\_MODE |
| disk\_io\_read\_mode | int | settings\_pack::enable\_os\_cache |

determines how files are opened when they're in read only mode
versus read and write mode. The options are:

enable\_os\_cache
:   Files are opened normally, with the OS caching reads and writes.

disable\_os\_cache
:   This opens all files in no-cache mode. This corresponds to the
    OS not letting blocks for the files linger in the cache. This
    makes sense in order to avoid the bittorrent client to
    potentially evict all other processes' cache by simply handling
    high throughput and large files. If libtorrent's read cache is
    disabled, enabling this may reduce performance.

write\_through
:   flush pieces to disk as they complete validation.

One reason to disable caching is that it may help the operating
system from growing its file cache indefinitely.

| name | type | default |
| --- | --- | --- |
| outgoing\_port | int | 0 |
| num\_outgoing\_ports | int | 0 |

this is the first port to use for binding outgoing connections to.
This is useful for users that have routers that allow QoS settings
based on local port. when binding outgoing connections to specific
ports, num\_outgoing\_ports is the size of the range. It should
be more than a few

Warning

setting outgoing ports will limit the ability to keep
multiple connections to the same client, even for different
torrents. It is not recommended to change this setting. Its main
purpose is to use as an escape hatch for cheap routers with QoS
capability but can only classify flows based on port numbers.

It is a range instead of a single port because of the problems with
failing to reconnect to peers if a previous socket to that peer and
port is in TIME\_WAIT state.

| name | type | default |
| --- | --- | --- |
| peer\_dscp | int | 0x04 |

peer\_dscp determines the DSCP field in the IP header of every
packet sent to peers (including web seeds). 0x0 means no marking,
0x04 represents Lower Effort. For more details see [RFC 8622](http://www.faqs.org/rfcs/rfc8622.html).

peer\_tos is the backwards compatible name for this setting.

| name | type | default |
| --- | --- | --- |
| active\_downloads | int | 3 |
| active\_seeds | int | 5 |
| active\_checking | int | 1 |
| active\_dht\_limit | int | 88 |
| active\_tracker\_limit | int | 1600 |
| active\_lsd\_limit | int | 60 |
| active\_limit | int | 500 |

for auto managed torrents, these are the limits they are subject
to. If there are too many torrents some of the auto managed ones
will be paused until some slots free up. active\_downloads and
active\_seeds controls how many active seeding and downloading
torrents the queuing mechanism allows. The target number of active
torrents is min(active\_downloads + active\_seeds, active\_limit).
active\_downloads and active\_seeds are upper limits on the
number of downloading torrents and seeding torrents respectively.
Setting the value to -1 means unlimited.

For example if there are 10 seeding torrents and 10 downloading
torrents, and active\_downloads is 4 and active\_seeds is 4,
there will be 4 seeds active and 4 downloading torrents. If the
settings are active\_downloads = 2 and active\_seeds = 4,
then there will be 2 downloading torrents and 4 seeding torrents
active. Torrents that are not auto managed are not counted against
these limits.

active\_checking is the limit of number of simultaneous checking
torrents.

active\_limit is a hard limit on the number of active (auto
managed) torrents. This limit also applies to slow torrents.

active\_dht\_limit is the max number of torrents to announce to
the DHT.

active\_tracker\_limit is the max number of torrents to announce
to their trackers.

active\_lsd\_limit is the max number of torrents to announce to
the local network over the local service discovery protocol.

You can have more torrents *active*, even though they are not
announced to the DHT, lsd or their tracker. If some peer knows
about you for any reason and tries to connect, it will still be
accepted, unless the torrent is paused, which means it won't accept
any connections.

| name | type | default |
| --- | --- | --- |
| auto\_manage\_interval | int | 30 |

auto\_manage\_interval is the number of seconds between the
torrent queue is updated, and rotated.

| name | type | default |
| --- | --- | --- |
| seed\_time\_limit | int | 24 \* 60 \* 60 |

this is the limit on the time a torrent has been an active seed
(specified in seconds) before it is considered having met the seed
limit criteria. See [queuing](manual-ref.md#queuing).

| name | type | default |
| --- | --- | --- |
| auto\_scrape\_interval | int | 1800 |
| auto\_scrape\_min\_interval | int | 300 |

auto\_scrape\_interval is the number of seconds between scrapes
of queued torrents (auto managed and paused torrents). Auto managed
torrents that are paused, are scraped regularly in order to keep
track of their downloader/seed ratio. This ratio is used to
determine which torrents to seed and which to pause.

auto\_scrape\_min\_interval is the minimum number of seconds
between any automatic scrape (regardless of torrent). In case there
are a large number of paused auto managed torrents, this puts a
limit on how often a scrape request is sent.

| name | type | default |
| --- | --- | --- |
| max\_peerlist\_size | int | 3000 |
| max\_paused\_peerlist\_size | int | 1000 |

max\_peerlist\_size is the maximum number of peers in the list of
known peers. These peers are not necessarily connected, so this
number should be much greater than the maximum number of connected
peers. Peers are evicted from the cache when the list grows passed
90% of this limit, and once the size hits the limit, peers are no
longer added to the list. If this limit is set to 0, there is no
limit on how many peers we'll keep in the peer list.

max\_paused\_peerlist\_size is the max peer list size used for
torrents that are paused. This can be used to save memory for paused
torrents, since it's not as important for them to keep a large peer
list.

| name | type | default |
| --- | --- | --- |
| min\_announce\_interval | int | 5 \* 60 |

this is the minimum allowed announce interval for a tracker. This
is specified in seconds and is used as a sanity check on what is
returned from a tracker. It mitigates hammering mis-configured
trackers.

| name | type | default |
| --- | --- | --- |
| auto\_manage\_startup | int | 60 |

this is the number of seconds a torrent is considered active after
it was started, regardless of upload and download speed. This is so
that newly started torrents are not considered inactive until they
have a fair chance to start downloading.

| name | type | default |
| --- | --- | --- |
| seeding\_piece\_quota | int | 20 |

seeding\_piece\_quota is the number of pieces to send to a peer,
when seeding, before rotating in another peer to the unchoke set.

| name | type | default |
| --- | --- | --- |
| max\_rejects | int | 50 |

max\_rejects is the number of piece requests we will reject in a
row while a peer is choked before the peer is considered abusive
and is disconnected.

| name | type | default |
| --- | --- | --- |
| recv\_socket\_buffer\_size | int | 0 |
| send\_socket\_buffer\_size | int | 0 |

specifies the buffer sizes set on peer sockets. 0 means the OS
default (i.e. don't change the buffer sizes).
The socket buffer sizes are changed using setsockopt() with
SOL\_SOCKET/SO\_RCVBUF and SO\_SNDBUFFER.

Note that uTP peers share a single UDP socket buffer for each of the
listen\_interfaces, along with DHT and UDP tracker traffic.
If the buffer size is too small for the combined traffic through the
socket, packets may be dropped.

| name | type | default |
| --- | --- | --- |
| max\_peer\_recv\_buffer\_size | int | 2 \* 1024 \* 1024 |

the max number of bytes a single peer connection's receive buffer is
allowed to grow to.

| name | type | default |
| --- | --- | --- |
| optimistic\_disk\_retry | int | 10 \* 60 |

optimistic\_disk\_retry is the number of seconds from a disk
write errors occur on a torrent until libtorrent will take it out
of the upload mode, to test if the error condition has been fixed.

libtorrent will only do this automatically for auto managed
torrents.

You can explicitly take a torrent out of upload only mode using
set\_upload\_mode().

| name | type | default |
| --- | --- | --- |
| max\_suggest\_pieces | int | 16 |

max\_suggest\_pieces is the max number of suggested piece indices
received from a peer that's remembered. If a peer floods suggest
messages, this limit prevents libtorrent from using too much RAM.

| name | type | default |
| --- | --- | --- |
| local\_service\_announce\_interval | int | 5 \* 60 |

local\_service\_announce\_interval is the time between local
network announces for a torrent.
This interval is specified in seconds.

| name | type | default |
| --- | --- | --- |
| dht\_announce\_interval | int | 15 \* 60 |

dht\_announce\_interval is the number of seconds between
announcing torrents to the distributed hash table (DHT).

| name | type | default |
| --- | --- | --- |
| udp\_tracker\_token\_expiry | int | 60 |

udp\_tracker\_token\_expiry is the number of seconds libtorrent
will keep UDP tracker connection tokens around for. This is
specified to be 60 seconds. The higher this
value is, the fewer packets have to be sent to the UDP tracker. In
order for higher values to work, the tracker needs to be configured
to match the expiration time for tokens.

| name | type | default |
| --- | --- | --- |
| num\_optimistic\_unchoke\_slots | int | 0 |

num\_optimistic\_unchoke\_slots is the number of optimistic
unchoke slots to use.
Having a higher number of optimistic unchoke slots mean you will
find the good peers faster but with the trade-off to use up more
bandwidth. 0 means automatic, where libtorrent opens up 20% of your
allowed upload slots as optimistic unchoke slots.

| name | type | default |
| --- | --- | --- |
| max\_pex\_peers | int | 50 |

the max number of peers we accept from pex messages from a single
peer. this limits the number of concurrent peers any of our peers
claims to be connected to. If they claim to be connected to more
than this, we'll ignore any peer that exceeds this limit

| name | type | default |
| --- | --- | --- |
| tick\_interval | int | 500 |

tick\_interval specifies the number of milliseconds between
internal ticks. This is the frequency with which bandwidth quota is
distributed to peers. It should not be more than one second (i.e.
1000 ms). Setting this to a low value (around 100) means higher
resolution bandwidth quota distribution, setting it to a higher
value saves CPU cycles.

| name | type | default |
| --- | --- | --- |
| share\_mode\_target | int | 3 |

share\_mode\_target specifies the target share ratio for share
mode torrents. If set to 3, we'll try to upload 3
times as much as we download. Setting this very high, will make it
very conservative and you might end up not downloading anything
ever (and not affecting your share ratio). It does not make any
sense to set this any lower than 2. For instance, if only 3 peers
need to download the rarest piece, it's impossible to download a
single piece and upload it more than 3 times. If the
share\_mode\_target is set to more than 3, nothing is downloaded.

| name | type | default |
| --- | --- | --- |
| upload\_rate\_limit | int | 0 |
| download\_rate\_limit | int | 0 |

upload\_rate\_limit and download\_rate\_limit sets
the session-global limits of upload and download rate limits, in
bytes per second. By default peers on the local network are not rate
limited.

A value of 0 means unlimited.

For fine grained control over rate limits, including making them apply
to local peers, see [peer classes](manual-ref.md#peer-classes).

| name | type | default |
| --- | --- | --- |
| dht\_upload\_rate\_limit | int | 8000 |

the number of bytes per second (on average) the DHT is allowed to send.
If the incoming requests causes to many bytes to be sent in responses,
incoming requests will be dropped until the quota has been replenished.

| name | type | default |
| --- | --- | --- |
| unchoke\_slots\_limit | int | 8 |

unchoke\_slots\_limit is the max number of unchoked peers in the
[session](reference-Session.md#session). The number of unchoke slots may be ignored depending on
what choking\_algorithm is set to. Setting this limit to -1
means unlimited, i.e. all peers will always be unchoked.

| name | type | default |
| --- | --- | --- |
| connections\_limit | int | 200 |

connections\_limit sets a global limit on the number of
connections opened. The number of connections is set to a hard
minimum of at least two per torrent, so if you set a too low
connections limit, and open too many torrents, the limit will not
be met.

| name | type | default |
| --- | --- | --- |
| connections\_slack | int | 10 |

connections\_slack is the number of incoming connections
exceeding the connection limit to accept in order to potentially
replace existing ones.

| name | type | default |
| --- | --- | --- |
| utp\_target\_delay | int | 100 |
| utp\_gain\_factor | int | 3000 |
| utp\_min\_timeout | int | 500 |
| utp\_syn\_resends | int | 2 |
| utp\_fin\_resends | int | 2 |
| utp\_num\_resends | int | 3 |
| utp\_connect\_timeout | int | 3000 |
| utp\_loss\_multiplier | int | 50 |

utp\_target\_delay is the target delay for uTP sockets in
milliseconds. A high value will make uTP connections more
aggressive and cause longer queues in the upload bottleneck. It
cannot be too low, since the noise in the measurements would cause
it to send too slow.
utp\_gain\_factor is the number of bytes the uTP congestion
window can increase at the most in one RTT.
If this is set too high, the congestion controller reacts
too hard to noise and will not be stable, if it's set too low, it
will react slow to congestion and not back off as fast.

utp\_min\_timeout is the shortest allowed uTP socket timeout,
specified in milliseconds. The
timeout depends on the RTT of the connection, but is never smaller
than this value. A connection times out when every packet in a
window is lost, or when a packet is lost twice in a row (i.e. the
resent packet is lost as well).

The shorter the timeout is, the faster the connection will recover
from this situation, assuming the RTT is low enough.
utp\_syn\_resends is the number of SYN packets that are sent (and
timed out) before giving up and closing the socket.
utp\_num\_resends is the number of times a packet is sent (and
lost or timed out) before giving up and closing the connection.
utp\_connect\_timeout is the number of milliseconds of timeout
for the initial SYN packet for uTP connections. For each timed out
packet (in a row), the timeout is doubled. utp\_loss\_multiplier
controls how the congestion window is changed when a packet loss is
experienced. It's specified as a percentage multiplier for
cwnd. Do not change this value unless you know what you're doing.
Never set it higher than 100.

| name | type | default |
| --- | --- | --- |
| mixed\_mode\_algorithm | int | settings\_pack::peer\_proportional |

The mixed\_mode\_algorithm determines how to treat TCP
connections when there are uTP connections. Since uTP is designed
to yield to TCP, there's an inherent problem when using swarms that
have both TCP and uTP connections. If nothing is done, uTP
connections would often be starved out for bandwidth by the TCP
connections. This mode is prefer\_tcp. The peer\_proportional
mode simply looks at the current throughput and rate limits all TCP
connections to their proportional share based on how many of the
connections are TCP. This works best if uTP connections are not
rate limited by the global rate limiter (which they aren't by
default).

| name | type | default |
| --- | --- | --- |
| listen\_queue\_size | int | 5 |

listen\_queue\_size is the value passed in to listen() for the
listen socket. It is the number of outstanding incoming connections
to queue up while we're not actively waiting for a connection to be
accepted. 5 should be sufficient for any
normal client. If this is a high performance server which expects
to receive a lot of connections, or used in a simulator or test, it
might make sense to raise this number. It will not take affect
until the listen\_interfaces settings is updated.

| name | type | default |
| --- | --- | --- |
| torrent\_connect\_boost | int | 30 |

torrent\_connect\_boost is the number of peers to try to connect
to immediately when the first tracker response is received for a
torrent. This is a boost to given to new torrents to accelerate
them starting up. The normal connect scheduler is run once every
second, this allows peers to be connected immediately instead of
waiting for the [session](reference-Session.md#session) tick to trigger connections.
This may not be set higher than 255.

| name | type | default |
| --- | --- | --- |
| alert\_queue\_size | int | 2000 |

alert\_queue\_size is the maximum number of alerts queued up
internally. If alerts are not popped, the queue will eventually
fill up to this level. Once the [alert](reference-Alerts.md#alert) queue is full, additional
alerts will be dropped, and not delivered to the client. Once the
client drains the queue, new alerts may be delivered again. In order
to know that alerts have been dropped, see
session\_handle::dropped\_alerts().

| name | type | default |
| --- | --- | --- |
| max\_metadata\_size | int | 3 \* 1024 \* 10240 |

max\_metadata\_size is the maximum allowed size (in bytes) to be
received by the metadata extension, i.e. magnet links.

| name | type | default |
| --- | --- | --- |
| hashing\_threads | int | 1 |

hashing\_threads is the number of disk I/O threads to use for
piece hash verification. These threads are *in addition* to the
regular disk I/O threads specified by [settings\_pack::aio\_threads](reference-Settings.md#aio_threads).
These threads are only used for full checking of torrents. The
hash checking done while downloading are done by the regular disk
I/O threads.
The [hasher](reference-Utility.md#hasher) threads do not only compute hashes, but also perform
the read from disk. On storage optimal for sequential access,
such as hard drives, this setting should be set to 1, which is
also the default.

| name | type | default |
| --- | --- | --- |
| checking\_mem\_usage | int | 256 |

the number of blocks to keep outstanding at any given time when
checking torrents. Higher numbers give faster re-checks but uses
more memory. Specified in number of 16 kiB blocks

| name | type | default |
| --- | --- | --- |
| predictive\_piece\_announce | int | 0 |

if set to > 0, pieces will be announced to other peers before they
are fully downloaded (and before they are hash checked). The
intention is to gain 1.5 potential round trip times per downloaded
piece. When non-zero, this indicates how many milliseconds in
advance pieces should be announced, before they are expected to be
completed.

| name | type | default |
| --- | --- | --- |
| aio\_threads | int | 10 |

for some aio back-ends, aio\_threads specifies the number of
io-threads to use.

| name | type | default |
| --- | --- | --- |
| tracker\_backoff | int | 250 |

tracker\_backoff determines how aggressively to back off from
retrying failing trackers. This value determines *x* in the
following formula, determining the number of seconds to wait until
the next retry:

> delay = 5 + 5 \* x / 100 \* fails^2

This setting may be useful to make libtorrent more or less
aggressive in hitting trackers.

| name | type | default |
| --- | --- | --- |
| share\_ratio\_limit | int | 200 |
| seed\_time\_ratio\_limit | int | 700 |

when a seeding torrent reaches either the share ratio (bytes up /
bytes down) or the seed time ratio (seconds as seed / seconds as
downloader) or the seed time limit (seconds as seed) it is
considered done, and it will leave room for other torrents. These
are specified as percentages. Torrents that are considered done will
still be allowed to be seeded, they just won't have priority anymore.
For more, see [queuing](manual-ref.md#queuing).

| name | type | default |
| --- | --- | --- |
| peer\_turnover | int | 4 |
| peer\_turnover\_cutoff | int | 90 |
| peer\_turnover\_interval | int | 300 |

peer\_turnover is the percentage of peers to disconnect every
turnover peer\_turnover\_interval (if we're at the peer limit), this
is specified in percent when we are connected to more than limit \*
peer\_turnover\_cutoff peers disconnect peer\_turnover fraction of the
peers. It is specified in percent peer\_turnover\_interval is the
interval (in seconds) between optimistic disconnects if the
disconnects happen and how many peers are disconnected is
controlled by peer\_turnover and peer\_turnover\_cutoff

| name | type | default |
| --- | --- | --- |
| connect\_seed\_every\_n\_download | int | 10 |

this setting controls the priority of downloading torrents over
seeding or finished torrents when it comes to making peer
connections. Peer connections are throttled by the connection\_speed
and the half-open connection limit. This makes peer connections a
limited resource. Torrents that still have pieces to download are
prioritized by default, to avoid having many seeding torrents use
most of the connection attempts and only give one peer every now
and then to the downloading torrent. libtorrent will loop over the
downloading torrents to connect a peer each, and every n:th
connection attempt, a finished torrent is picked to be allowed to
connect to a peer. This setting controls n.

| name | type | default |
| --- | --- | --- |
| max\_http\_recv\_buffer\_size | int | 4\*1024\*204 |

the max number of bytes to allow an HTTP response to be when
announcing to trackers or downloading .torrent files via the
url provided in add\_torrent\_params.

| name | type | default |
| --- | --- | --- |
| max\_retry\_port\_bind | int | 10 |

if binding to a specific port fails, should the port be incremented
by one and tried again? This setting specifies how many times to
retry a failed port bind

| name | type | default |
| --- | --- | --- |
| alert\_mask | int | int |

a bitmask combining flags from [alert\_category\_t](reference-Alerts.md#alert_category_t) defining which
kinds of alerts to receive

| name | type | default |
| --- | --- | --- |
| out\_enc\_policy | int | settings\_pack::pe\_enabled |
| in\_enc\_policy | int | settings\_pack::pe\_enabled |

control the settings for incoming and outgoing connections
respectively. see [enc\_policy](reference-Settings.md#enc_policy) enum for the available options.
Keep in mind that protocol encryption degrades performance in
several respects:

1. It prevents "zero copy" disk buffers being sent to peers, since
   each peer needs to mutate the data (i.e. encrypt it) the data
   must be copied per peer connection rather than sending the same
   buffer to multiple peers.
2. The encryption itself requires more CPU than plain bittorrent
   protocol. The highest cost is the Diffie Hellman exchange on
   connection setup.
3. The encryption handshake adds several round-trips to the
   connection setup, and delays transferring data.

| name | type | default |
| --- | --- | --- |
| allowed\_enc\_level | int | settings\_pack::pe\_both |

determines the encryption level of the connections. This setting
will adjust which encryption scheme is offered to the other peer,
as well as which encryption scheme is selected by the client. See
[enc\_level](reference-Settings.md#enc_level) enum for options.

| name | type | default |
| --- | --- | --- |
| inactive\_down\_rate | int | 2048 |
| inactive\_up\_rate | int | 2048 |

the download and upload rate limits for a torrent to be considered
active by the queuing mechanism. A torrent whose download rate is
less than inactive\_down\_rate and whose upload rate is less than
inactive\_up\_rate for auto\_manage\_startup seconds, is
considered inactive, and another queued torrent may be started.
This logic is disabled if dont\_count\_slow\_torrents is false.

| name | type | default |
| --- | --- | --- |
| proxy\_type | int | settings\_pack::none |

proxy to use. see [proxy\_type\_t](reference-Settings.md#proxy_type_t).

| name | type | default |
| --- | --- | --- |
| proxy\_port | int | 0 |

the port of the proxy server

| name | type | default |
| --- | --- | --- |
| i2p\_port | int | 0 |

sets the [i2p](http://www.i2p2.de) SAM bridge port to connect to. set the hostname with
the i2p\_hostname setting.

| name | type | default |
| --- | --- | --- |
| urlseed\_max\_request\_bytes | int | 16 \* 1024 \* 1024 |

The maximum request range of an url seed in bytes. This value
defines the largest possible sequential web seed request. Lower values
are possible but will be ignored if they are lower then piece size.
This value should be related to your download speed to prevent
libtorrent from creating too many expensive http requests per
second. You can select a value as high as you want but keep in mind
that libtorrent can't create parallel requests if the first request
did already select the whole file.
If you combine bittorrent seeds with web seeds and pick strategies
like rarest first you may find your web seed requests split into
smaller parts because we don't download already picked pieces
twice.

| name | type | default |
| --- | --- | --- |
| web\_seed\_name\_lookup\_retry | int | 1800 |

time to wait until a new retry of a web seed name lookup

| name | type | default |
| --- | --- | --- |
| close\_file\_interval | int | CLOSE\_FILE\_INTERVAL |

the number of seconds between closing the file opened the longest
ago. 0 means to disable the feature. The purpose of this is to
periodically close files to trigger the operating system flushing
disk cache. Specifically it has been observed to be required on
windows to not have the disk cache grow indefinitely.
This defaults to 240 seconds on windows, and disabled on other
systems.

| name | type | default |
| --- | --- | --- |
| utp\_cwnd\_reduce\_timer | int | 100 |

When uTP experiences packet loss, it will reduce the congestion
window, and not reduce it again for this many milliseconds, even if
experiencing another lost packet.

| name | type | default |
| --- | --- | --- |
| max\_web\_seed\_connections | int | 3 |

the max number of web seeds to have connected per torrent at any
given time.

| name | type | default |
| --- | --- | --- |
| resolver\_cache\_timeout | int | 1200 |

the number of seconds before the internal host name resolver
considers a cache value timed out, negative values are interpreted
as zero.

| name | type | default |
| --- | --- | --- |
| send\_not\_sent\_low\_watermark | int | 16384 |

specify the not-sent low watermark for socket send buffers. This
corresponds to the, Linux-specific, TCP\_NOTSENT\_LOWAT TCP socket
option.

| name | type | default |
| --- | --- | --- |
| rate\_choker\_initial\_threshold | int | 1024 |

the rate based choker compares the upload rate to peers against a
threshold that increases proportionally by its size for every
peer it visits, visiting peers in decreasing upload rate. The
number of upload slots is determined by the number of peers whose
upload rate exceeds the threshold. This option sets the start
value for this threshold. A higher value leads to fewer unchoke
slots, a lower value leads to more.

| name | type | default |
| --- | --- | --- |
| upnp\_lease\_duration | int | 3600 |

The expiration time of UPnP port-mappings, specified in seconds. 0
means permanent lease. Some routers do not support expiration times
on port-maps (nor correctly returning an error indicating lack of
support). In those cases, set this to 0. Otherwise, don't set it any
lower than 5 minutes.

| name | type | default |
| --- | --- | --- |
| max\_concurrent\_http\_announces | int | 50 |

limits the number of concurrent HTTP tracker announces. Once the
limit is hit, tracker requests are queued and issued when an
outstanding announce completes.

| name | type | default |
| --- | --- | --- |
| dht\_max\_peers\_reply | int | 100 |

the maximum number of peers to send in a reply to get\_peers

| name | type | default |
| --- | --- | --- |
| dht\_search\_branching | int | 5 |

the number of concurrent search request the node will send when
announcing and refreshing the routing table. This parameter is called
alpha in the kademlia paper

| name | type | default |
| --- | --- | --- |
| dht\_max\_fail\_count | int | 20 |

the maximum number of failed tries to contact a node before it is
removed from the routing table. If there are known working nodes that
are ready to replace a failing node, it will be replaced immediately,
this limit is only used to clear out nodes that don't have any node
that can replace them.

| name | type | default |
| --- | --- | --- |
| dht\_max\_torrents | int | 2000 |

the total number of torrents to track from the DHT. This is simply an
upper limit to make sure malicious DHT nodes cannot make us allocate
an unbounded amount of memory.

| name | type | default |
| --- | --- | --- |
| dht\_max\_dht\_items | int | 700 |

max number of items the DHT will store

| name | type | default |
| --- | --- | --- |
| dht\_max\_peers | int | 500 |

the max number of peers to store per torrent (for the DHT)

| name | type | default |
| --- | --- | --- |
| dht\_max\_torrent\_search\_reply | int | 20 |

the max number of torrents to return in a torrent search query to the
DHT

| name | type | default |
| --- | --- | --- |
| dht\_block\_timeout | int | 5 \* 60 |

the number of seconds a DHT node is banned if it exceeds the rate
limit. The rate limit is averaged over 10 seconds to allow for bursts
above the limit.

| name | type | default |
| --- | --- | --- |
| dht\_block\_ratelimit | int | 5 |

the max number of packets per second a DHT node is allowed to send
without getting banned.

| name | type | default |
| --- | --- | --- |
| dht\_item\_lifetime | int | 0 |

the number of seconds a immutable/mutable item will be expired.
default is 0, means never expires.

| name | type | default |
| --- | --- | --- |
| dht\_sample\_infohashes\_interval | int | 21600 |

the info-hashes sample recomputation interval (in seconds).
The node will precompute a subset of the tracked info-hashes and return
that instead of calculating it upon each request. The permissible range
is between 0 and 21600 seconds (inclusive).

| name | type | default |
| --- | --- | --- |
| dht\_max\_infohashes\_sample\_count | int | 20 |

the maximum number of elements in the sampled subset of info-hashes.
If this number is too big, expect the DHT storage implementations
to clamp it in order to allow UDP packets go through

| name | type | default |
| --- | --- | --- |
| max\_piece\_count | int | 0x200000 |

max\_piece\_count is the maximum allowed number of pieces in
metadata received via magnet links. Loading large torrents (with
more pieces than the default limit) may also require passing in
a higher limit to [read\_resume\_data()](reference-Resume_Data.md#read_resume_data()) and
[torrent\_info::parse\_info\_section()](reference-Torrent_Info.md#parse_info_section()), if those are used.

| name | type | default |
| --- | --- | --- |
| metadata\_token\_limit | int | 2500000 |

when receiving metadata (torrent file) from peers, this is the
max number of bencoded tokens we're willing to parse. This limit
is meant to prevent DoS attacks on peers. For very large
torrents, this limit may have to be raised.

| name | type | default |
| --- | --- | --- |
| disk\_write\_mode | int | settings\_pack::mmap\_write\_mode\_t::auto\_mmap\_write |

controls whether disk writes will be made through a memory mapped
file or via normal write calls. This only affects the
mmap\_disk\_io. When saving to a non-local drive (network share,
NFS or NAS) using memory mapped files is most likely inferior.
When writing to a local SSD (especially in DAX mode) using memory
mapped files likely gives the best performance.
The values for this setting are specified as [mmap\_write\_mode\_t](reference-Settings.md#mmap_write_mode_t).

| name | type | default |
| --- | --- | --- |
| mmap\_file\_size\_cutoff | int | 40 |

when using mmap\_disk\_io, files smaller than this number of blocks
will not be memory mapped, but will use normal pread/pwrite
operations. This file size limit is specified in 16 kiB blocks.

| name | type | default |
| --- | --- | --- |
| i2p\_inbound\_quantity | int | 3 |
| i2p\_outbound\_quantity | int | 3 |
| i2p\_inbound\_length | int | 3 |
| i2p\_outbound\_length | int | 3 |

Configures the SAM [session](reference-Session.md#session)
quantity of I2P inbound and outbound tunnels [1..16].
number of hops for I2P inbound and outbound tunnels [0..7]
Changing these will not trigger a reconnect to the SAM bridge,
they will take effect the next time the SAM connection is
re-established (by restarting or changing i2p\_hostname or
i2p\_port).

| name | type | default |
| --- | --- | --- |
| announce\_port | int | 0 |

announce\_port is the port passed along as the port parameter
to remote trackers such as HTTP or DHT. This setting does not affect
the effective listening port nor local service discovery announcements.
If left as zero (default), the listening port value is used.

Note

This setting is only meant for very special cases where a
seed's listening port differs from the external port. As an
example, if a local proxy is used and that the proxy supports
reverse tunnels through NAT-PMP, the tracker must connect to
the external NAT-PMP port (configured using announce\_port)
instead of the actual local listening port.

```cpp
struct settings_pack final : settings_interface
{
   friend  void apply_pack_impl (settings_pack const*
      , aux::session_settings_single_thread&
      , std::vector<void(aux::session_impl::*)()>*);
   void set_bool (int name, bool val) override;
   void set_int (int name, int val) override;
   void set_str (int name, std::string val) override;
   void set_int (int name, flags::bitfield_flag<Type, Tag> const val);
   bool has_val (int name) const override;
   void clear ();
   void clear (int name);
   int get_int (int name) const override;
   bool get_bool (int name) const override;
   std::string const& get_str (int name) const override;
   void for_each (Fun&& f) const;

   enum type_bases
   {
      string_type_base,
      int_type_base,
      bool_type_base,
      type_mask,
      index_mask,
   };

   enum mmap_write_mode_t
   {
      always_pwrite,
      always_mmap_write,
      auto_mmap_write,
   };

   enum suggest_mode_t
   {
      no_piece_suggestions,
      suggest_read_cache,
   };

   enum choking_algorithm_t
   {
      fixed_slots_choker,
      rate_based_choker,
      deprecated_bittyrant_choker,
   };

   enum seed_choking_algorithm_t
   {
      round_robin,
      fastest_upload,
      anti_leech,
   };

   enum io_buffer_mode_t
   {
      enable_os_cache,
      deprecated_disable_os_cache_for_aligned_files,
      disable_os_cache,
      write_through,
   };

   enum bandwidth_mixed_algo_t
   {
      prefer_tcp,
      peer_proportional,
   };

   enum enc_policy
   {
      pe_forced,
      pe_enabled,
      pe_disabled,
   };

   enum enc_level
   {
      pe_plaintext,
      pe_rc4,
      pe_both,
   };

   enum proxy_type_t
   {
      none,
      socks4,
      socks5,
      socks5_pw,
      http,
      http_pw,
   };
};
```

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:settings_pack%3A%3A%5Bset_int%28%29+set_bool%28%29+set_str%28%29%5D&labels=documentation&body=Documentation+under+heading+%22settings_pack%3A%3A%5Bset_int%28%29+set_bool%28%29+set_str%28%29%5D%22+could+be+improved)]

## set\_int() set\_bool() set\_str()

```cpp
void set_bool (int name, bool val) override;
void set_int (int name, int val) override;
void set_str (int name, std::string val) override;
void set_int (int name, flags::bitfield_flag<Type, Tag> const val);
```

set a configuration option in the [settings\_pack](reference-Settings.md#settings_pack). name is one of
the enum values from string\_types, int\_types or bool\_types. They must
match the respective type of the set\_\* function.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:settings_pack%3A%3A%5Bhas_val%28%29%5D&labels=documentation&body=Documentation+under+heading+%22settings_pack%3A%3A%5Bhas_val%28%29%5D%22+could+be+improved)]

## has\_val()

```cpp
bool has_val (int name) const override;
```

queries whether the specified configuration option has a value set in
this pack. name can be any enumeration value from string\_types,
int\_types or bool\_types.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:settings_pack%3A%3A%5Bclear%28%29%5D&labels=documentation&body=Documentation+under+heading+%22settings_pack%3A%3A%5Bclear%28%29%5D%22+could+be+improved)]

## clear()

```cpp
void clear ();
```

clear the settings pack from all settings

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:settings_pack%3A%3A%5Bclear%28%29%5D&labels=documentation&body=Documentation+under+heading+%22settings_pack%3A%3A%5Bclear%28%29%5D%22+could+be+improved)]

## clear()

```cpp
void clear (int name);
```

clear a specific setting from the pack

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:settings_pack%3A%3A%5Bget_str%28%29+get_int%28%29+get_bool%28%29%5D&labels=documentation&body=Documentation+under+heading+%22settings_pack%3A%3A%5Bget_str%28%29+get_int%28%29+get_bool%28%29%5D%22+could+be+improved)]

## get\_str() get\_int() get\_bool()

```cpp
int get_int (int name) const override;
bool get_bool (int name) const override;
std::string const& get_str (int name) const override;
```

queries the current configuration option from the [settings\_pack](reference-Settings.md#settings_pack).
name is one of the enumeration values from string\_types, int\_types
or bool\_types. The enum value must match the type of the get\_\*
function. If the specified setting field has not been set, the default
value is returned.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:enum+type_bases&labels=documentation&body=Documentation+under+heading+%22enum+type_bases%22+could+be+improved)]

## enum type\_bases

Declared in "[libtorrent/settings\_pack.hpp](include/libtorrent/settings_pack.hpp)"

| name | value | description |
| --- | --- | --- |
| string\_type\_base | 0 |  |
| int\_type\_base | 16384 |  |
| bool\_type\_base | 32768 |  |
| type\_mask | 49152 |  |
| index\_mask | 16383 |  |

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:enum+mmap_write_mode_t&labels=documentation&body=Documentation+under+heading+%22enum+mmap_write_mode_t%22+could+be+improved)]

## enum mmap\_write\_mode\_t

Declared in "[libtorrent/settings\_pack.hpp](include/libtorrent/settings_pack.hpp)"

| name | value | description |
| --- | --- | --- |
| always\_pwrite | 0 | disable writing to disk via mmap, always use normal write calls |
| always\_mmap\_write | 1 | prefer using memory mapped files for disk writes (at least for large files where it might make sense) |
| auto\_mmap\_write | 2 | determine whether to use pwrite or memory mapped files for disk writes depending on the kind of storage behind the save path |

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:enum+suggest_mode_t&labels=documentation&body=Documentation+under+heading+%22enum+suggest_mode_t%22+could+be+improved)]

## enum suggest\_mode\_t

Declared in "[libtorrent/settings\_pack.hpp](include/libtorrent/settings_pack.hpp)"

| name | value | description |
| --- | --- | --- |
| no\_piece\_suggestions | 0 |  |
| suggest\_read\_cache | 1 |  |

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:enum+choking_algorithm_t&labels=documentation&body=Documentation+under+heading+%22enum+choking_algorithm_t%22+could+be+improved)]

## enum choking\_algorithm\_t

Declared in "[libtorrent/settings\_pack.hpp](include/libtorrent/settings_pack.hpp)"

| name | value | description |
| --- | --- | --- |
| fixed\_slots\_choker | 0 | This is the traditional choker with a fixed number of unchoke slots (as specified by [settings\_pack::unchoke\_slots\_limit](reference-Settings.md#unchoke_slots_limit)). |
| rate\_based\_choker | 2 | This opens up unchoke slots based on the upload rate achieved to peers. The more slots that are opened, the marginal upload rate required to open up another slot increases. Configure the initial threshold with [settings\_pack::rate\_choker\_initial\_threshold](reference-Settings.md#rate_choker_initial_threshold).  For more information, see [rate based choking](manual-ref.md#rate-based-choking). |
| deprecated\_bittyrant\_choker | 3 |  |

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:enum+seed_choking_algorithm_t&labels=documentation&body=Documentation+under+heading+%22enum+seed_choking_algorithm_t%22+could+be+improved)]

## enum seed\_choking\_algorithm\_t

Declared in "[libtorrent/settings\_pack.hpp](include/libtorrent/settings_pack.hpp)"

| name | value | description |
| --- | --- | --- |
| round\_robin | 0 | which round-robins the peers that are unchoked when seeding. This distributes the upload bandwidth uniformly and fairly. It minimizes the ability for a peer to download everything without redistributing it. |
| fastest\_upload | 1 | unchokes the peers we can send to the fastest. This might be a bit more reliable in utilizing all available capacity. |
| anti\_leech | 2 | prioritizes peers who have just started or are just about to finish the download. The intention is to force peers in the middle of the download to trade with each other. This does not just take into account the pieces a peer is reporting having downloaded, but also the pieces we have sent to it. |

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:enum+io_buffer_mode_t&labels=documentation&body=Documentation+under+heading+%22enum+io_buffer_mode_t%22+could+be+improved)]

## enum io\_buffer\_mode\_t

Declared in "[libtorrent/settings\_pack.hpp](include/libtorrent/settings_pack.hpp)"

| name | value | description |
| --- | --- | --- |
| enable\_os\_cache | 0 |  |
| deprecated\_disable\_os\_cache\_for\_aligned\_files | 1 |  |
| disable\_os\_cache | 2 |  |
| write\_through | 3 |  |

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:enum+bandwidth_mixed_algo_t&labels=documentation&body=Documentation+under+heading+%22enum+bandwidth_mixed_algo_t%22+could+be+improved)]

## enum bandwidth\_mixed\_algo\_t

Declared in "[libtorrent/settings\_pack.hpp](include/libtorrent/settings_pack.hpp)"

| name | value | description |
| --- | --- | --- |
| prefer\_tcp | 0 | disables the mixed mode bandwidth balancing |
| peer\_proportional | 1 | does not throttle uTP, throttles TCP to the same proportion of throughput as there are TCP connections |

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:enum+enc_policy&labels=documentation&body=Documentation+under+heading+%22enum+enc_policy%22+could+be+improved)]

## enum enc\_policy

Declared in "[libtorrent/settings\_pack.hpp](include/libtorrent/settings_pack.hpp)"

| name | value | description |
| --- | --- | --- |
| pe\_forced | 0 | Only encrypted connections are allowed. Incoming connections that are not encrypted are closed and if the encrypted outgoing connection fails, a non-encrypted retry will not be made. |
| pe\_enabled | 1 | encrypted connections are enabled, but non-encrypted connections are allowed. An incoming non-encrypted connection will be accepted, and if an outgoing encrypted connection fails, a non- encrypted connection will be tried. |
| pe\_disabled | 2 | only non-encrypted connections are allowed. |

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:enum+enc_level&labels=documentation&body=Documentation+under+heading+%22enum+enc_level%22+could+be+improved)]

## enum enc\_level

Declared in "[libtorrent/settings\_pack.hpp](include/libtorrent/settings_pack.hpp)"

| name | value | description |
| --- | --- | --- |
| pe\_plaintext | 1 | use only plain text encryption |
| pe\_rc4 | 2 | use only RC4 encryption |
| pe\_both | 3 | allow both |

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:enum+proxy_type_t&labels=documentation&body=Documentation+under+heading+%22enum+proxy_type_t%22+could+be+improved)]

## enum proxy\_type\_t

Declared in "[libtorrent/settings\_pack.hpp](include/libtorrent/settings_pack.hpp)"

| name | value | description |
| --- | --- | --- |
| none | 0 | No proxy server is used and all other fields are ignored. |
| socks4 | 1 | The server is assumed to be a [SOCKS4 server](http://www.ufasoft.com/doc/socks4_protocol.htm) that requires a username. |
| socks5 | 2 | The server is assumed to be a SOCKS5 server ([RFC 1928](http://www.faqs.org/rfcs/rfc1928.html)) that does not require any authentication. The username and password are ignored. |
| socks5\_pw | 3 | The server is assumed to be a SOCKS5 server that supports plain text username and password authentication ([RFC 1929](http://www.faqs.org/rfcs/rfc1929.html)). The username and password specified may be sent to the proxy if it requires. |
| http | 4 | The server is assumed to be an HTTP proxy. If the transport used for the connection is non-HTTP, the server is assumed to support the [CONNECT](http://tools.ietf.org/html/draft-luotonen-web-proxy-tunneling-01) method. i.e. for web seeds and HTTP trackers, a plain proxy will suffice. The proxy is assumed to not require authorization. The username and password will not be used. |
| http\_pw | 5 | The server is assumed to be an HTTP proxy that requires user authorization. The username and password will be sent to the proxy. |

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:min_memory_usage%28%29+high_performance_seed%28%29&labels=documentation&body=Documentation+under+heading+%22min_memory_usage%28%29+high_performance_seed%28%29%22+could+be+improved)]

# min\_memory\_usage() high\_performance\_seed()

Declared in "[libtorrent/session.hpp](include/libtorrent/session.hpp)"

```cpp
settings_pack min_memory_usage ();
settings_pack high_performance_seed ();
```

The default values of the [session](reference-Session.md#session) settings are set for a regular
bittorrent client running on a desktop system. There are functions that
can set the [session](reference-Session.md#session) settings to pre set settings for other environments.
These can be used for the basis, and should be tweaked to fit your needs
better.

min\_memory\_usage returns settings that will use the minimal amount of
RAM, at the potential expense of upload and download performance. It
adjusts the socket buffer sizes, disables the disk cache, lowers the send
buffer watermarks so that each connection only has at most one block in
use at any one time. It lowers the outstanding blocks send to the disk
I/O thread so that connections only have one block waiting to be flushed
to disk at any given time. It lowers the max number of peers in the peer
list for torrents. It performs multiple smaller reads when it hashes
pieces, instead of reading it all into memory before hashing.

This configuration is intended to be the starting point for embedded
devices. It will significantly reduce memory usage.

high\_performance\_seed returns settings optimized for a seed box,
serving many peers and that doesn't do any downloading. It has a 128 MB
disk cache and has a limit of 400 files in its file pool. It support fast
upload rates by allowing large send buffers.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:name_for_setting%28%29+setting_by_name%28%29&labels=documentation&body=Documentation+under+heading+%22name_for_setting%28%29+setting_by_name%28%29%22+could+be+improved)]

# name\_for\_setting() setting\_by\_name()

Declared in "[libtorrent/settings\_pack.hpp](include/libtorrent/settings_pack.hpp)"

```cpp
char const* name_for_setting (int s);
int setting_by_name (string_view name);
```

converts a setting integer (from the enums string\_types, int\_types or
bool\_types) to a string, and vice versa.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:default_settings%28%29&labels=documentation&body=Documentation+under+heading+%22default_settings%28%29%22+could+be+improved)]

# default\_settings()

Declared in "[libtorrent/settings\_pack.hpp](include/libtorrent/settings_pack.hpp)"

```cpp
settings_pack default_settings ();
```

returns a [settings\_pack](reference-Settings.md#settings_pack) with every setting set to its default value

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:generate_fingerprint%28%29&labels=documentation&body=Documentation+under+heading+%22generate_fingerprint%28%29%22+could+be+improved)]

# generate\_fingerprint()

Declared in "[libtorrent/fingerprint.hpp](include/libtorrent/fingerprint.hpp)"

```cpp
std::string generate_fingerprint (std::string name
   , int major, int minor = 0, int revision = 0, int tag = 0);
```

This is a utility function to produce a client ID fingerprint formatted to
the most common convention. The fingerprint can be set via the
peer\_fingerprint setting, in [settings\_pack](reference-Settings.md#settings_pack).

The name string should contain exactly two characters. These are the
characters unique to your client, used to identify it. Make sure not to
clash with anybody else. Here are some taken id's:

| id chars | client |
| --- | --- |
| LT | libtorrent (default) |
| UT | uTorrent |
| UM | uTorrent Mac |
| qB | qBittorrent |
| BP | BitTorrent Pro |
| BT | BitTorrent |
| DE | Deluge |
| AZ | Azureus |
| TL | Tribler |

There's an informal directory of client id's [here](http://wiki.theory.org/BitTorrentSpecification#peer_id).

The major, minor, revision and tag parameters are used to
identify the version of your client.
