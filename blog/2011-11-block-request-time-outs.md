---
title: "block request time-outs"
date: "2011-11"
source: "https://blog.libtorrent.org/2011/11/block-request-time-outs/"
---

Tuesday, November 22nd, 2011 by arvid

timing out requests, and requesting blocks from other peers, may seem like a straight forward and trivial problem. However, there’s a balance to be struck between timing out a block too early, causing certain situation to systematically request every block multiple times, or never timing blocks out causing partially downloaded pieces to linger for a very long time, preventing uploading those.

In the early days of bittorrent, there was a client called BitComet, which received a lot of bad reputation. Some of it was FUD, and some of it was warranted. One thing BitComet did to prevent DoS attacks was to limit the number of outstanding requests it would allow any single peer to send to it to 50. If a peer would send more than 50 requests, they would just be silently dropped (keep in mind this was before the FAST extension’s reject message was introduced).

As you can imagine, a downloader encountering a BitComet client on a fast network (where the bandwidth delay product requires more than 50 outstanding requests) would be caught quite off guard, sending requests, some of which would never get a response. What would happen is that the outstanding requests would “gum up”, and the effective outstanding requests would be fewer than the downloader thought. You could time out requests after some time, but that would still reduce performance, since you’d get stuck for a minute, or whatever timeout you choose. Keep in mind that BitTorrent allows for block requests to be serviced out of order (this is an important feature to allow for cache hits to go before cache misses), and waiting for these requests just looked like they were being handled out of order.

In libtorrent I tried to be clever, by detecting that some requests would go through and some would not get responses at all. Essentially detecting *how much* out of order the requests were being handled. If one entire request window would go by (being requested and receiving responses), passed any request in the queue already, that would be considered too much out of order, and the block would be assumed to have been dropped.

Fast forward a few years, people have very fast internet connections. My out of order limit is not longer valid, in fact, it’s quite common for pieces to be that much out of order at those rates. libtorrent gets into a state where it constantly assumes that requests were dropped and re-requests them from the same peer, over and over. This is clearly very bad. People were seeing redundant data being downloaded at megabytes per second.

This logic was dropped, in favor of a special case for BitComet to simply never request more than 50 blocks at a time if the other end is detected to be BitComet.

While I was working on this issue initially, I introduced a field in the extension handshake header called, **reqq** (request queue) indicating what the limit is for this client. Combined with FAST extention’s reject message, it provides a robust solution for this problem.

Since blocks may be received out of order, a time out is not tied to a certain block. That is, you cannot assign an expected arrival time to each block and then time out a block if it hasn’t been received before that time. Since blocks are received out of order, there’s no way of knowing ahead of time in which order the blocks will be received, and hence no way of assigning timeouts. The blocks that will come first should have a shorter timeout than the last block.

One way of implementing time outs is to simply have a generic timeout for any block. Every time we receive any block, this timer is reset and starts counting down for the next block, whichever it is. If the timer expires without a block, we have a time out event.

Which block timed out?

There’s no way of knowing which order the other end intends to send the blocks, but for the most part they tend to come in FIFO order. Should we time out the oldest block we requested or the last one we requested?

Consider the following piece, there are 5 outstanding requests to a peer that just failed to meet one of the deadlines. The blocks were requested in the order specified.

[![](http://www.rasterbar.com/libtorrent_blog/wp-content/uploads/2011/11/timeout-multiple-blocking.png "timeout-multiple-blocking")](http://www.rasterbar.com/libtorrent_blog/wp-content/uploads/2011/11/timeout-multiple-blocking.png)

If we time out 1, and let another peer pick it, we’re increasing our chances of block 2 timing out, and 3 and so on, assuming the peer actually will send the blocks in order. And we would most definitely get redundant download for block 1.

The other end is also most likely to have started sending 1 already, in which case there’s no going back. If we try to cancel the piece, we’ll still receive it and just add it to the wasted download.

However, if we time out 5, and open it up for another peer to request, we minimize the risk of adding wasted download. This is because the other end is the least likely to have started sending it, and the most likely to react to a cancel message.

When a time out happens, something may need to be done. The two extremes of reactions are:

> Always clear one of the requested blocks, as if it was cancelled, to allow another peer to request it.

and:

> Never clear a requested block, rely on the end-game mode to re-pick any blocks, or rely on the peer dropping the connection, releasing the blocks that way.

Always clearing the block invites a lot of redundant downloaded bytes, since the peer will likely send us this block eventually (unless it drops or actually receives a cancel message first).

Never clearing the block causes issues when end-game mode is strict (i.e. it only triggers when we’re about to complete the torrent). In the case where a swarm is large, but rate limited on the source, every peer will essentially have the same pieces. In this scenario, it’s important to keep up with the swarm as a whole, in order to be able to contribute as much as possible. If one or a few slow peers can block the completion of a piece until the whole torrent is complete, that may block several peers for the whole download, and make the client not keep up.

The example below is a piece where every block is complete, except for the yellow one, which we requested from a peer that just timed out (as in it hasn’t sent us the block yet, and we thought it would have).

![](http://www.rasterbar.com/libtorrent_blog/wp-content/uploads/2011/11/timeout-blocking.png "timeout-blocking")

a block timed out in an otherwise complete piece

In this case it is clearly useful to let another peer finish this piece, so we can start uploading it. If there are no other open blocks in the piece, cancel the block from this peer, to open it up to be requested from other peers.

On the other hand, if there still are free blocks to pick, like in the next example below:

[![](http://www.rasterbar.com/libtorrent_blog/wp-content/uploads/2011/11/timeout-not-blocking1.png "timeout-not-blocking")](http://www.rasterbar.com/libtorrent_blog/wp-content/uploads/2011/11/timeout-not-blocking1.png)

a block timed out in a piece with unrequested blocks

In this case, it does not make sense to cancel the block. This peer may be the only one that has this piece, in which case we better give it all the time it needs to complete. In this case, it makes sense to postpone the timeout another block worth of time.

Posted in [protocol](https://blog.libtorrent.org/category/protocol/)
**|**
 [No Comments](https://blog.libtorrent.org/2011/11/block-request-time-outs/#respond)

---

### Leave a Reply [Cancel reply](/2011/11/block-request-time-outs/#respond)

You must be [logged in](https://blog.libtorrent.org/wp-login.php?redirect_to=https%3A%2F%2Fblog.libtorrent.org%2F2011%2F11%2Fblock-request-time-outs%2F) to post a comment.
