---
title: "asynchronous disk I/O"
date: "2012-10"
source: "https://blog.libtorrent.org/2012/10/asynchronous-disk-io/"
---

Since 2010, I’ve been working, on and off, on a branch off of libtorrent which use asynchronous disk I/O, instead of the synchronous disk calls in the disk thread in 0.16.x versions.

The aio branch has several performance improvements apart from allowing multiple disk operations outstanding at any given time. For instance:

1. the disk cache allows multiple threads accessing it (cache hits are served immediately, even as other threads are flushing and reading data into blocks).
2. pieces no longer need to be flushed to disk before they can be uploaded to other peers.
3. socket operations can be performed in a thread pool. This is useful for expensive operations like SSL sockets.
4. the disk cache uses ARC instead of LRU and has O(1) complexity instead of O(log n).
5. the disk cache supports multiple cache layers, where an SSD drive can be inserted as a second level cache.
6. the piece picker has been optimized
7. the torrent list has been optimized to support hundreds of thousands of torrents loaded simultaneously.
8. hashing pieces is done in parallel, to improve download speed.

The first attempt at doing disk I/O asynchronous used various system specific operations for truly async. operations. The idea was that the more operations the kernel knows about, the better scheduling it can perform. 2 years later, I decided to switch over to using a thread pool where disk operations instead would use regular blocking calls.

Here are the reasons to use a thread pool instead of the various async. disk I/O APIs:

1. code complexity
2. poor APIs
3. poor quality of implementations
4. weak support

There are primarily 3 kinds of asynchronous disk APIs.

1. linux AIO (supported in the kernel)
2. posix AIO (supported by linux, Mac OS X, BSD, solaris, AIX etc.)
3. Windows’ overlapped I/O

Supporting 3 distinct APIs as well as a thread pool for systems not supporting any of them introduces a lot of code and a lot of conditionals when testing. To make things worse, the plain posix AIO API is not very rich, and to make decent use of it, one is required to use system specific extensions. In short, even the posix API ends up having many special cases for different platforms. More on this later.

When using linux kernel AIO, files are required to be opened in O\_DIRECT mode. This introduces further requirements of all read and write operations to have their file offset, memory buffer and size be aligned to 512 bytes. This introduces significant complexity for multi-file torrents, where the piece blocks no longer will be aligned with the file boundaries. Unaligned write operations need to first cause one or two read operations for the edges, and the write back the buffer. Doing so also introduces extra considerations when writing two adjacent unaligned blocks. Since all operations would be asynchronous, special care need to be taken to serialize them correctly, to not overwrite the edges.

This applies primarily to posix AIO and linux AIO. I/O completion ports on windows is surprisingly well throught through. The only odd thing about iocp is that it is tricky to mix async. operations and synchronous ones on the same file (the synchronous ones still trigger an event when they complete).

The posix AIO API has two major flaws.

1. The only (reasonable) event callback mechanism is via a signal.
2. the number of operations you can issue in a single call is sometimes very limited

## notifications

The posix API specifies two kinds of callbacks, a signal and callback from an unspecified thread. The problem with having some threads call your callback is partly a performance degradation and partly that you can’t do much in the callback. Also, some operating systems don’t implement the thread notification (like Mac OS X). We’re left with the signal handler (which, granted, also suffers from the problem of not being able to do much in it, even less).

Some systems support \*real time signals\* which means you can associate user data with the signal, delivered to the signal handler. This way you can know in your signal handler which job completed. Other operating systems don’t support real time signals (Mac OS X) and you’re left with scanning through all outstanding jobs to find out which one completed (does not scale well).

The third mechanism to be notified of completed jobs, is to explicitly call *aio\_suspend*and pass in the currently outstanding jobs. This has the same scaling issues as select() does. You pass in an array of jobs, you then wake up when one of them completes and you scan the array for which one completed. It does not scale with many jobs, but more importantly, you cannot interrupt this call in order to issue another job.

In a bittorrent client, the disk thread often needs to wake up because there’s another job to be issued. Not being able to wake up the thread causes performance degradation and added complexity. AIO operations don’t work on pipes or eventfds (which could have been a way to wake up).

The main problem of using a signal handler for notification, however, is not that you may have to scan through all the jobs to find which one completed, or that the only reasonable thing to do in the handler is to write to a pipe to communicate with the main thread.

The main problem is that signal numbers is a limited process wide resource. To use a signal inside a library means intruding into the program using that library. The program may be using the signal for other things or it may be using another library registering the same signal number. This means instantiating two libtorrent instances in the same process will not work (well). In order to make it work, libtorrent needs to take special care, and it won’t be efficient. Each instance will see the other ones notifications.

The second problem of signals is that it’s often not well defined which thread they are delivered to. You may have to register your signal handler in every thread of your program in order to be guaranteed to receive it. This is certainly true on linux.

For this reason there is an extension to the posix API on linux, which lets you specify the thread ID you would like your signals delivered to. Solaris has an extension to post notifications to a port (which comes very close to be as useful as iocp on windows). BSD has an extension to get notifications via kqueue, which also circumvents the issues of using signals.

## issuing multiple jobs

The posix AIO API does not include the equivalent of pwritev() and preadv(), i.e. it does not have vector operations. This may seem perfectly fine, since it’s an async. API anyway, the readv and writev operations are just special cases of issuing multiple jobs that happen to be adjecent on disk.

However, the restriction on lio\_listio() (the function used to issue a batch of jobs) means that in practice, it has to be invoked several times for a relatively small vector. The specification only requires that 2 jobs can be submitted at a time.

It adds to code complexity to split up one contiguous write into multiple jobs as well. Their notifications need to be collected and the full operation’s notification can only be triggered once they are all complete.

## linux AIO

linux AIO has similar problems as posix AIO. The main fix, however, was to build a sane notification mechanism. On linux you have an aio\_context which acts as a queue for notifications, and you can wait for notification on it.

The issues that remain is that you cannot post custom messages to the queue (to wake the thread up to issue more jobs for instance). The work-around for this is to associate an eventfd with each job (io\_set\_eventfd()) and then use select() to wait on it along with a pipe that can be used to interrupt the thread.

On linux, io\_submit() blocks, which to some degree defeats the purpose of async. operations. The reason why it blocks is because most filesystems perform blocking disk operations internally, and as long as jobs are submitted to read and write files in a filesystem, they will spend a lot of time blocking during submit. This is not the case when submitting jobs to raw devices however, which indicates that the async disk I/O was primarily meant for applications that circumvent the filesystem as well. In order to make this work well when writing ordinary files, you need a thread pool to invoke io\_submit().

Mac OS X does not support notifications via kqueue nor realtime signals. This makes the Mac version extremely inefficient. On top of that, the default limits on Mac are 16 outstanding jobs per process. This is not enough to issue a single flush operation for a piece (most torrents have more than 16 blocks per piece).

Of all three asynchronous disk I/O APIs (linux, posix and iocp) the only operations that are asynchronous are reading and writing files. Those operations may be the ones typically associated with taking a long time, but on mac OS X, close() also blocks.

HFS+ doesn’t support sparse files. When closing a file that has been written to sparsely, the kernel will fill in the blanks with zeroes, while the program is blocked in the close() system call.

Other prominent operations that are not asynchronous are stat(), open(), fallocate() and rename() (as well as their windows counterparts).

Benefits of using a thread pool with blocking operations instead of asynchronous disk operations:

* The high level operations that break down into multiple disk operations become significantly simpler to understand and make correct.
* Every disk operation is asynchrounous, including rename and copy files.
* The disk code is entirely platform-independent (with the exception for systems not supporting pwritev()/preadv())
* The disk thread can use vector operations (readv and writev), and typically pass more buffers than Mac OS X would allow using AIO.

---

### 5 Comments
