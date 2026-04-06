---
title: "scalable interfaces"
date: "2011-11"
source: "https://blog.libtorrent.org/2011/11/scalable-interfaces/"
---

Tuesday, November 15th, 2011 by arvid

The typical bittorrent client user interface shows you a list of all torrents loaded in the client. Some of these torrents may be stopped and inactive, some of them may be seeding, but not having any peers interested in the torrent, and some (obviously) downloading.

The simple (and probably most common) way to update the user interface of such a client would be to:

1. acquire the mutex protecting the network thread and all torrent objects
2. loop over all torrents and copy all relevant properties for the torrents into a data structured owned by the gui thread
3. release mutex

Clearly this is a bit simplified, for instance, there may be a second pass where extra information is collected for some specific torrent, say its peer list for instance.

What happens if we have 50’000 torrents in the client?

In order to scale with a lot of torrents, where presumably a lot of the information stays the same between updates, for most torrents. For instance, the torrent name, number of peers, number of seeds are fairly static. Even upload and download rates will be static overall. For most torrents, at this scale, these rates will stay at 0 for the most part.

For the uTorrent 3.1 release, I revamped the way we render the UI. Profiling uTorrent 3.0, once every second, we would spike the CPU and spend by far most of the time in free() and strdup(), when copying data from torrents into the GUI thread’s data structure, and freeing the previous value.

My first attempt at optimizing this (which was a little bit heroic) was to simply identify the case where the string we’re about to copy is identical to the one we already have, and skip the free()/strdup() in that case. This was then simplified into something performing better and being simpler.

While we’re copying all this data, and looping over all the torrents, keep in mind we’re holding the network thread’s lock. We’re essentially preventing any network activity to happen during this time. Simply looping over 50000 torrents once a second is enough to get a noticeable hick-up in the GUI.

The final solution was to have a clear ownership of the data structures. The gui thread should not snoop around in the network thread’s data structures. Instead, the network thread collects all torrents when their state changes on a separate queue. Every second (or gui update rate), the network thread takes this list of torrents and sends them in a message to the gui thread, which then updates the respective torrents in its data structure.

If a torrent changes states 10 times during one second, it will still just be a single update to the GUI thread, and if there are 49990 torrents that didn’t change any state at all, they won’t be mentioned and be entirely free (CPU wise).

As a heritage from the first attempt at a fix, each update even keeps a bitmask of which fields were updated, so that not every string for a torrent has to be copied, just the ones that changed. For the most part, strings don’t change, just transfer rates and peer counters.

This allows uTorrent to have a huge number of torrents loaded at once, without dragging down the snappiness of the UI.

The current API of libtorrent (as of 0.15.x) prevents blocking the network thread, at the expense of the GUI thread. Each call to a libtorrent API function is actually a message posted to the network thread, put in the queue and handled. Once it’s done, a condition variable fires to notify the calling thread the result is there. Clearly, for calls that don’t have a return value, it can be posted without blocking the calling thread.

This means each call with a return value, that requires blocking, will be potentially expensive. Especially if the network thread is busy. The positive side of this is the network thread will have plenty of CPU time and will not likely be slowed down by the GUI. Hence, function calls with return values should be avoided in order to have good performance.

One common function call in libtorrent’s API is **pop\_alert()**. This function asks libtorrent if there’s an alert (a generic notification message coming from the bittorrent engine). If there is, one alert is returned. This function is called repeatedly until there are no more queued alerts. There are two problems with this API:

1. if libtorrent produces alerts faster then the GUI thread can pop them, you have an infinite loop
2. each alert requires a separate API call, which is potentially expensive

In libtorrent 0.16 there’s a new function call to pop the entire queue of alerts. **pop\_alerts()**, (note the plural-S). This solves the infinite loop problem and improves performance to loop through the alerts.

Another example is adding a torrent. Typically it’s not critical that this is a very efficient call, but when starting up a client, all torrents from the previous session are typically added. In the case where you have 50000 torrents in your client, having a slow **add\_torrent()** call can significantly delay startup.

In libtorrent 0.15.x, add\_torrent() is one of those API calls that has a return value. This means the call blocks the calling thread until the message has been processed and the torrent has been added to the internal list in libtorrent. Calling this repeatedly 50000 times, you’ll find that the GUI thread and libtorrent network thread are very poorly utilized. They end up waiting for each other in a ping-pong-fashion. The network thread waits for messages, the GUI thread sends an add-torrent message and waits for a response, the network thread processes the message and goes back to waiting, the gui thread then goes to load the next .torrent file from disk while the network thread is waiting.

To improve this, libtorrent 0.16 introduces **async\_add\_torrent()**. This function does not return a value, and hence returns immediately. The torrent handle for the new torrent is returned later via an **add\_torrent\_alert**. Using this function, the network thread and torrent loading thread can both be fully utilized while loading the torrents.

torrent\_handle::status() is a similar bottleneck. Each call is potentially expensive. In order to perform better, use session::get\_torrent\_status(), which retrieves status for all torrents in a single call (introduced in 0.16). There’s also session::refresh\_torrent\_status(), where you can send in the same vector, and instead of reallocating all state, the states are updated. However, this still doesn’t scale well with many torrents.

Now, going back to the original topic, status updates for a GUI. The new libtorrent API to allow for this has been modeled after the uTorrent way of updating the UI.

Each torrent has a *subscribe* flag indicating whether or not we’re subscribed to state changes or not. All torrents that has the subscription flag set, will have references to them stored in an update list whenever their state changes. The user can request updates, which is an asynchronous call that triggers an alert with update list in it, resetting the update list.

To receive a delta update of only the torrents that changed some of their state, call **session::post\_torrent\_updates()** and handle the **state\_update\_alert**. The alert contains a vector of the torrent\_status  of all updated torrents. Use the handle field from the torrent\_status to map it to which torrent it refers to.

Posted in [algorithms](https://blog.libtorrent.org/category/algorithms/), [user interface](https://blog.libtorrent.org/category/user_interface/)
**|**
 [No Comments](https://blog.libtorrent.org/2011/11/scalable-interfaces/#respond)

---
