---
title: "bittorrent over SSL"
date: "2012-01"
source: "https://blog.libtorrent.org/2012/01/bittorrent-over-ssl/"
---

Monday, January 30th, 2012 by arvid

Running bittorrent over SSL could make sense for several applications. Anything you want distributed to a closed group, but large enough to warrant bittorrent would do well being distributed over bittorrent/SSL. Currently closed group distributions either don’t use any peer-to-peer distribution at all, or they use poor-man’s privacy/security. I’m referring to the “private” flag of torrent files, which suggests to clients that they should not announce to any source other than the tracker (i.e. no DHT, no peer exchange, no local peer discovery).

The fundamental problem with the private flag is that there’s no enforcement of it. And even if there was, it’s not done on the peers themselves. This means that anyone can join a private swarm, simply by knowing a few peers on it (that’s knowing the IP and listen port of a few people that are in the swarm). When connecting to those peers, they have no way of knowing whether or not you’re allowed to join or not, so they have to assume that you are, since you know their IP and listen port.

With SSL, the publisher of a torrent can actually require peers to properly authenticate in the SSL handshake. Each peer can verify that all peers they’re connected to are allowed onto the swarm by the publisher, by making sure they can present a certificate signed by the publisher. SSL supports two-way authentication, although HTTPS servers normally just provide authentication of the server, not the client.

A typical response to running bittorrent over SSL is that you could just encrypt your files before distributing them, and send the keys only to the people who should have access to the data. There are several drawbacks of this approach though. Encrypting on the fly compared to distributing an encrypted file has the benefit that you don’t need to make a copy to decrypt it at the end-points. If you decrypt in place you can no longer seed the torrent, which would defeat the main purpose of using bittorrent in the first place.

Using SSL, specifically, also has the advantage that it can fit in to existing authentication schemes. For example, one can use an HTTPS tracker and use the same root certificate to authenticate the tracker as used for the peers. Same thing goes for web seeds.

Here’s how SSL support is implemented in libtorrent.

The .torrent file contains an X.509 certificate from the publisher. The private key part of the certificate can be used to sign peer certificates to grant them access to the torrent. This would typically only be possible to do by the original publisher.

If a peer find an X.509 certificate in the torrent file, it will require a signed certificate from the publisher, and it will require all peers connecting to that torrent presenting a valid and signed certificate in the SSL handshake. Signed by the holder of the certificate in the .torrent file, which acts as a root CA (the only root CA in fact) and all certificates only using a single hop to the root.

Since a published may want to be able to re-use the root certificate for multiple torrents, the CommonName field (or actually the SubjectAltName fields, same rules apply as in RFC 2818) which normally contains the hostname, must contain either the name of the torrent (the “name” field) or “\*”. Star indicating that any torrent is OK. Peers honors this by verifying this field to match when accepting connections. This allows the publisher to use a single key, with a single tracker, for multiple torrents, with different access control for each.

Since one peer may have multiple torrents, the *SNI* (server name indication) extension to TLS is used to indicate which torrent a peer is connecting to. Any outgoing SSL connection will set the SNI field to the hex encoded info-hash of the torrent. Since this is all happening during the SSL handshake, it happens before the bittorrent protocol has a chance to indicate which info-hash it’s talking to. In the case of SSL, it is required that the bittorrent level info-hash matches the one specified in the SNI field. If they don’t match, the connection is dropped. SNI support is required, if there is not SNI field in an incoming connection, it is dropped.

If the tracker of an SSL torrent uses HTTPS, the server is expected to present a certificate signed by the same root CA cert that’s in the .torrent file. This finally closes the loop of having properly authenticated trackers, verified by something in the .torrent file itself (which is controlled by the publisher). The same is expected from any web seed with an HTTPS URL.

More information is available [here](http://libtorrent.org/manual-ref.html#ssl-torrents).

One future possibility with SSL torrents is to use the unique and identifying keys each peer has to sign piece requests, or some sort of digital coin, to prove that something was uploaded to someone. With such a scheme, tracker would no longer have to rely on the client stats reporting being honest (and would no longer create an incentive to lie in those reports).

This is a scheme that was actually implemented in the bittorrent downloader at [headweb](http://www.headweb.se), where each peer would “buy” blocks from each other, and then cache them in for store credit. Creating a true incentive to keep seeding.

Posted in [network](https://blog.libtorrent.org/category/network/), [protocol](https://blog.libtorrent.org/category/protocol/)
**|**
 [No Comments](https://blog.libtorrent.org/2012/01/bittorrent-over-ssl/#respond)

---
