---
title: "seeding a million torrents"
date: "2012-01"
source: "https://blog.libtorrent.org/2012/01/seeding-a-million-torrents/"
---

There are two main architectures of peer-to-peer networks. There’s the peer-centric (limewire style) and content-centric (bittorrent style). In a peer-centric network each participant announces its existence to the network, and other peers looking for content go around asking peers if they have the content. This makes the peer-centric networks scale well with pieces of content. There’s (essentially) no extra cost for a peer to share more pieces of content. However, finding rare content becomes increasingly hard the more participants in the network.

In a content-centric network, each participant announces its existence to each piece of content. i.e. announcing to a tracker for each torrent. This makes the network scale poorly with pieces of content. However, it makes it very reliable finding the one peer that has a rare piece of content. This post explores the possibilities to make bittorrent scale better with pieces of content, to promote content longevity and accessibility.

What would happen if you would seed a million torrents? First you would run into bottlenecks of the bittorrent implementation, where it assumes the list of torrents will be fairly short. Fixing these may involve:

* eliminating all (or near all) loops over all torrents. For instance, when connecting to peers, instead of looping over all torrents, loop over a list of a subset of the torrents which have advertised interest in connecting to peers.
* optimizing data structures to use less memory, since loading a lot of torrents may explode the sizes of some data structures.
* change red-black tree data structures to hash tables.
* optimize UI refreshes to only mention changes (i.e. **post\_torrent\_updates()**), since polling a million torrents is very slow.

Once you fix all of those, you’ll get down to the more fundamental bottlenecks. Sending an announce request to a tracker will cost you about 350 bytes of upstream payload bytes. Let’s assume the vast majority of these torrents don’t have any peers, so the response payload would be around 150 bytes, just for the HTTP header. On the lower layer, there would be 3 round trips (syn, syn-ack, payload, payload-ack, fin, fin-ack), each packet is 40 bytes. All in all, about 470 bytes up and 270 bytes down, per announce. With one million torrents, announcing once every hour, you need to announce to 1000000 / 60 / 60 = 277.8 torrents per second, resulting in a constant **130 kB/s upload** and **75 kB/s download**. That’s a significant portion, or all of, of most people’s internet connections.

Let’s instead assume all torrents are using UDP trackers. Then you get away with two round trips per announce (or maybe less if many torrents use the same tracker). The announce packet for UDP trackers is 100 bytes, the response is 20 bytes (assuming no peers), the connect packet and its response are both 16 bytes. Each packet has the IP and UDP header, which together are 28 bytes. This yields 172 bytes up and 92 bytes down per announce, i.e. **47.8 kB/s** upload and **25.6 kB/s download**. This is more manageable, but still not negligible.

These estimates are conservative, the default announce interval for trackers is 30 minutes, not 1 hour, so in most normal cases the required bandwidth would **double**.

There are additional costs associated with announcing torrents to the DHT and the local network as well. The DHT is especially expensive since you’re expected to reannounce **every 15 minutes**. Local peer discovery is supposed to send out multicast messages **every 5 minutes** per torrent, on the local network.

Simply loading a million .torrent files into RAM will use in the order of 4 GiB of RAM. When the file lists and tracker URLs are parsed out and stored in more expanded forms, a significant amount of RAM is added to that. This is enough to run out of RAM on many laptops.

If one assumption is that most torrents will have very little and rare activity, torrents could be loaded on demand, rather than up-front. It would first be loaded just to calculate its info-hash and to get its announce URLs. All torrent meta data could then be removed from RAM and loaded again the first time an incoming peer references the info-hash. This feature is referred to as *ghost torrents* in libtorrent, and require a user callback to pull the actual .torrent file back into memory when accessed.

The traditional solution to this problem is to have the bittorrent client scrape all torrents, slowly, and only seed the ones that have the lowest seed/peer ratio (i.e. the ones with the most need of more seeds). In libtorrent this is called auto-managed, because libtorrent determines which torrents are started and which are stopped, based on its scrape results. A stopped torrent does not announce to anything and does not allow any incoming peer connections and does not attempt to make outgoing connections.

The auto managed features of bittorrent clients are typically configured by setting the allowed number of downloading torrents and seeding torrents. The torrents are then sorted by their rank (determined by its queue order if we need to download the torrent or its peers/seeds ratio) and then *x* downloading torrents are started and *y* seeding torrents are started and all others are stopped.

What if we would never stop torrents, just stop announcing to them, or announce more infrequently? Always accept incoming connections for torrents (as long as the connection limit isn’t reached of course).

libtorrent supports setting separate limits for different announce methods. That is, making the *x* top torrents announce to trackers, the *y* top torrents announce to the DHT, the *z* top torrents announce to local peer discovery. Using this feature, all torrents could always be running, just not necessarily announce.

Instead of scraping torrents to find their rank, just announce to them instead.

This would mean all torrents always allows peer connections. All torrents are not necessarily announcing to their trackers every 30 minutes, but do announce every now and then, round-robin with all the other torrents that aren’t announcing regularly.

Never stopping a torrent might significantly improve availability and longevity of content in bittorrent networks.

---
