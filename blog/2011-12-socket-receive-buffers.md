---
title: "socket receive buffers"
date: "2011-12"
source: "https://blog.libtorrent.org/2011/12/socket-receive-buffers/"
---

Wednesday, December 14th, 2011 by arvid

In an attempt to save memory copying, libtorrent attempts to receive payload bytes directly into page aligned, pool allocated disk buffers. These buffers can then be used to DMA directly to disk (either with blocking O\_DIRECT files or via AIO operations, if run on a clever kernel).

To do this for the bittorrent protocol, the network loop needs to read 5 bytes (4 bytes length-prefix and 1 byte message code), if the message code is a piece packet, receive another 8 bytes (piece index and start offset) and 16 kiB into the disk buffer. This can be a single receive operation using vector read (or scatter/gather in windows terminology).

This means each 16 kiB payload block that’s received, requires two system calls to read (one for the message header and one for the data block itself). It also requires two system calls for every other bittorrent message that’s received, except for the ones that don’t have any arguments, and fit in 5 bytes (choke, unchoke, interested, not-interested, keep-alive). Those messages will still require one system call per message.

To illustrate this, a syscall log could look something like this:

```
read(5, buf) // length prefix + message code
readv({{buf, 12}, {disk_buf, 16384}}) // message header + payload
read(5, buf)
readv({{buf, 12}, {disk_buf, 16384}})
```

The assumption with this is that the saved memory copy will be worth the cost of the additional system calls.

This technique enables the possibility to receive from the socket directly into a memory mapped file buffer, which potentially can save even more copying (if the kernel is clever, but not clever enough to save that copy anyway).

However, testing this on a PowerMac, receiving into large contiguous (in virtual address space) buffers and then copy it into place, is faster than calling **recv()** twice for every message that’s received.

![](../images/recv_buffers-2fcbaab3.png)

Download rate over loopback when disk I/O and hashing is disabled

memcopy vs. syscalls

The main costs with the two techniques (receiving into the correct memory buffer vs. receiving into one large receive buffer) are the time it takes to copy memory and the time it takes to make a system call (and lock a socket object and unlink buffers from the kernel receive buffer chain etc.).

Which one is faster depends on how many 16 kiB blocks can we fit in a normal receive operation. In my benchmarks, almost all recv() calls resulted in having received about 128 kiB, which means 8 blocks. That would have resulted in 16 syscalls, instead of one, but 128 kiB less memory copying. In the case of my MacPro, it’s clearly faster to copy 128 kiB memory than to make 15 syscalls.

It would be interesting to know if receiving straight into memory mapped files then does give you any actual performance gains compared to the traditional method of receiving into a large buffer and copying it to where it needs to live.

When seeding, you definitely don’t want to make two syscalls per message you receive. Since you’re essentially guaranteed to not receive any payload messages, you’ll end up making 2 syscalls for almost all bittorrent messages received, with severe performance degradation. Most of the received messages will be requests, which are just 13 bytes each.

In libtorrent this setting can be controlled by session\_settings::contiguous\_recv\_buffers. It defaults to true, and even when set to false it will only have an affect for peers we’re downloading from.

Posted in [network](https://blog.libtorrent.org/category/network/), [optimization](https://blog.libtorrent.org/category/optimization/)
**|**
 [No Comments](https://blog.libtorrent.org/2011/12/socket-receive-buffers/#respond)

---

### Leave a Reply [Cancel reply](/2011/12/socket-receive-buffers/#respond)

You must be [logged in](https://blog.libtorrent.org/wp-login.php?redirect_to=https%3A%2F%2Fblog.libtorrent.org%2F2011%2F12%2Fsocket-receive-buffers%2F) to post a comment.
