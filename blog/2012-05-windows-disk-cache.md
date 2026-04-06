---
title: "windows’ disk cache"
date: "2012-05"
source: "https://blog.libtorrent.org/2012/05/windows-disk-cache/"
---

Thursday, May 31st, 2012 by arvid

A long standing problem with bittorrent clients on windows is that if you’re seeding large files or downloading large files, windows may decide to essentially use all your physical RAM for disk cache. The disk cache grows to the point where running processes start having their working set swapped out, significantly slowing down the system as a whole. Both uTorrent and libtorrent based clients have this problem.

To mitigate this problem, uTorrent and libtorrent lets you disable the OS disk cache. That is, it let’s you tell the client to open all files in unbuffered mode (this is called FILE\_FLAG\_NO\_BUFFERING on windows). This successfully solves the problem of ever-growing disk cache. The cost however is significantly more complicated client code. This is because unbuffered I/O requires all reads and writes to be cluster aligned, and buffers to be page aligned in memory. Since pieces in torrents span files, they are not necessarily (in fact, quite unlikely to be) aligned with the clusters on the disk. In order for the client to write an unaligned block to disk, it first has to read the blocks at the edges, overlay the unaligned block and then write it back. This is not the only increase in complexity though. The length of writes also need to be cluster aligned, which means you can only write files whose size is evenly divisible by the cluster size (which typically is 512 bytes). In order to actually set the correct file size, one has to either close the file and re-open it in buffered mode and call SetEndOfFile() or dig out NtSetInformationFile from nt.dll and call that directly. A common problem that arises from this are a number of race conditions. For instance, when writing the last piece, the file has to be closed and re-opened in order to be truncated to the correct size, and then re-opened again in unbuffered mode. This opens up for an opportunity for other processes to open the file in exclusive mode, preventing the bittorrent client from opening the file again. This actually happens, probably mostly with media players scanning directories. In short, using unbuffered I/O is a real pain, introduces bugs and makes code a lot more complex.

It turns out that there is this innocent looking flag that one can pass to CreateFile() on windows to hint that you may not be reading and writing sequentially. This is what the msdn page on CreateFile() has to say about the FILE\_FLAG\_RANDOM\_ACCESS:

> Access is intended to be random. The system can use this as a hint to optimize file caching.

Since bittorrent file access is very random, it seems to make a lot of sense for clients to use this flag on all downloaded and seeded files it opens. And clients do, both uTorrent and libtorrent does this (as of this writing). However, at an entirely different place on msdn, there’s a knowledge base article explaining what FILE\_FLAG\_RANDOM\_ACCESS actually does:

> This flag disables intelligent read-aheads and **prevents automatic unmapping of views after pages are read** to minimize mapping/unmapping when the process revisits that part of the file. This keeps previously read views in the Cache Manager working set. However, if the cumulative size of the accessed files exceeds physical memory, keeping so many views in the Cache Manager working set may be detrimental to overall operating system performance because it can consume a large amount of physical RAM.

(highlight added). This explains the exact symptoms users have seen with uTorrent and libtorrent. It turns out that not using this flag allows clients to be restored to the simpler, more unified, less error prone use of normal, buffered, files.

Posted in [disk](https://blog.libtorrent.org/category/disk/)
**|**
 [No Comments](https://blog.libtorrent.org/2012/05/windows-disk-cache/#respond)

---

### Leave a Reply [Cancel reply](/2012/05/windows-disk-cache/#respond)

You must be [logged in](https://blog.libtorrent.org/wp-login.php?redirect_to=https%3A%2F%2Fblog.libtorrent.org%2F2012%2F05%2Fwindows-disk-cache%2F) to post a comment.
