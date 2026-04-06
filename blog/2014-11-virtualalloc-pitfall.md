---
title: "VirtualAlloc pitfall"
date: "2014-11"
source: "https://blog.libtorrent.org/2014/11/virtualalloc-pitfall/"
---

Monday, November 24th, 2014 by arvid

When allocating blocks in the disk cache, libtorrent uses [valloc()](http://pubs.opengroup.org/onlinepubs/7908799/xsh/valloc.html), to allocate page-aligned 16kiB blocks. On windows, the natural couterpart to valloc() is [VirtualAlloc()](http://msdn.microsoft.com/en-us/library/windows/desktop/aa366887(v=vs.85).aspx). Having these blocks page aligned may provide performance improvements when reading and writing files that are aligned to the block boundaries.

The 16kiB allocation size is derived from the bittorrent protocol data transfer unit. Even if a piece is 1MiB, you can only ask to download 16kiB per request (and you need multiple pipelined requests to saturate the bandwidth delay product).

There used to be a bug in libtorrent where, on 32 bit systems, memory allocations would start failing even though only a quarter of the physical RAM was in use. The disk cache would grow to about 580 MiB and then stop, see [ticket 508](https://code.google.com/p/libtorrent/issues/detail?id=508).

It turned out to be caused by a little known (and poorly documented) “feature” of VirtualAlloc(). Every allocation it makes, allocates 64 kiB of virtual memory. In libtorrent’s case, every call allocated 16 kiB, but 64kB of virtual memory. This caused the process to run out of virtual address space long before the physical memory was exhausted, because each call to VirtualAlloc would waste 3/4 of the virtual address space it allocated.

This feature is called dwAllocationGranularity. It is actually documented on msdn, but not with VirtualAlloc, where one might expect. It’s in the documentation for the [SYSTEM\_INFO structure](http://msdn.microsoft.com/en-us/library/windows/desktop/ms724958(v=vs.85).aspx#dwAllocationGranularity).

Here’s another [post](http://cbloomrants.blogspot.com/2009/01/01-16-09-virtual-memory.html) diving into some more details of this topic.

now libtorrent uses [\_aligned\_malloc()](http://msdn.microsoft.com/en-us/library/8z34s9c6.aspx) instead.

Posted in [operating system](https://blog.libtorrent.org/category/operating-system/), [optimization](https://blog.libtorrent.org/category/optimization/)
**|**
 [No Comments](https://blog.libtorrent.org/2014/11/virtualalloc-pitfall/#respond)

---
