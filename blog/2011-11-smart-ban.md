---
title: "smart-ban"
date: "2011-11"
source: "https://blog.libtorrent.org/2011/11/smart-ban/"
---

Bittorrent lets you verify data you receive from the swarm against the SHA-1 hashes in the .torrent file. This enable clients to ban peers that sends data that fails the hash check, and thus cannot be trusted. However, the integrity checking can only be done at piece level. A piece may be several megabytes, and downloaded from multiple peers. If a piece fails, how do you know which peer sent the bad block?

The straight forward solution is to, for each peer, keep track of how many pieces it has participated in that succeeded, and how many pieces it has participated in that has failed. If the success/failure ratio drops below some threshold (and we have at least some number of samples), the peer is considered untrustworthy, and is dropped.

This works pretty well, at least against naïve poisoners.

It apparently worked against Media Defender’s poison attacks back in 2007, as revealed by their internal emails that leaked:

> After more in-depth analysis…we’ve determined that the new version DOES affect our interdiction in a negative way. They’ve added a new “bt.ban\_ratio” field that takes into consideration how many good pieces a client has uploaded. On the older version, they would just kick any peer that uploaded bad data 5+ times.
>
> This post gives some more explanation about the bad ratio field:  
> [http://forum.utorrent.com/viewtopic.php … 90#p249190](http://forum.utorrent.com/viewtopic.php?pid=249190#p249190)
>
> We still see a lot of hash\_check fails…but now the only peers getting banned are ours. This also affects MediaSentry’s interdicted torrents. They are no longer effective on the newest version either.

([source](http://www.utorrent.com/forum/viewtopic.php?id=29551 "source"))

However, it is still a fairly blunt tool.

The smart ban, as implemented in uTorrent and libtorrent, is a clever technique to take the banning of corrupt peers even further. It was developed by Greg Hazel while at BitTorrent Inc.

For every piece that fails, record the hash of each individual blocks that makes up the piece, together with a reference to the peer we got each specific block from. The next time we download the piece, if any one peer happened to send us the same block, but different data (i.e. the second block we received did not match the hash of the first one), ban that peer immediately.

Keep doing this until we finally succeed in downloading the piece, from someone. At that point, hash all the blocks that we now know are correct and compare them against all blocks we received previously and ban all peers whose blocks do not match the correct ones.

In order to immediately identify a bad block from a peer, and potentially save ourselves from downloading more corrupt data, one could use hash trees, to hash check every 16 kiB block. There is an [existing hash tree extension](http://www.bittorrent.org/beps/bep_0030.html) (supported only by libtorrent and Tribler as far as I know).

The main problem with this extension is that it was mainly designed to make the .torrent files smaller (which it is very successful at), so the leaves in the hash tree are still pieces (not blocks). It might be tempting to simply make the pieces 16 kiB, but that would cause serious problems:

1. bitfield messages would inflate to be very large
2. a lot more protocol overhead would go to sending have messages
3. disk I/O performance would drop since the contiguous blocks read and written to disks would become a lot smaller

Number 3 is the most important one. A revised hash tree extension should define the leafs to always be 16 kiB, regardless of the piece size. While we’re at it, there could be one hash tree per file, and make all pieces aligned to file boundaries, but that’s a pretty radical change to the protocol.

---
