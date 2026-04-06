---
title: "announce_infohash"
source: "https://libtorrent.org/reference-Trackers.html"
---

[home](reference.md)

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:class+announce_infohash&labels=documentation&body=Documentation+under+heading+%22class+announce_infohash%22+could+be+improved)]

# announce\_infohash

Declared in "[libtorrent/announce\_entry.hpp](include/libtorrent/announce_entry.hpp)"

```cpp
struct announce_infohash
{
   std::string message;
   error_code last_error;
   int scrape_incomplete  = -1;
   int scrape_complete  = -1;
   int scrape_downloaded  = -1;
   std::uint8_t fails : 7;
   bool updating : 1;
   bool start_sent : 1;
   bool complete_sent : 1;
};
```

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:announce_infohash%3A%3A%5Bmessage%5D&labels=documentation&body=Documentation+under+heading+%22announce_infohash%3A%3A%5Bmessage%5D%22+could+be+improved)]

message
:   if this tracker has returned an error or warning message
    that message is stored here

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:announce_infohash%3A%3A%5Blast_error%5D&labels=documentation&body=Documentation+under+heading+%22announce_infohash%3A%3A%5Blast_error%5D%22+could+be+improved)]

last\_error
:   if this tracker failed the last time it was contacted
    this error code specifies what error occurred

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:announce_infohash%3A%3A%5Bscrape_incomplete+scrape_complete+scrape_downloaded%5D&labels=documentation&body=Documentation+under+heading+%22announce_infohash%3A%3A%5Bscrape_incomplete+scrape_complete+scrape_downloaded%5D%22+could+be+improved)]

scrape\_incomplete scrape\_complete scrape\_downloaded
:   if this tracker has returned scrape data, these fields are filled in
    with valid numbers. Otherwise they are set to -1. incomplete counts
    the number of current downloaders. complete counts the number of
    current peers completed the download, or "seeds". downloaded is the
    cumulative number of completed downloads.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:announce_infohash%3A%3A%5Bfails%5D&labels=documentation&body=Documentation+under+heading+%22announce_infohash%3A%3A%5Bfails%5D%22+could+be+improved)]

fails
:   the number of times in a row we have failed to announce to this
    tracker.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:announce_infohash%3A%3A%5Bupdating%5D&labels=documentation&body=Documentation+under+heading+%22announce_infohash%3A%3A%5Bupdating%5D%22+could+be+improved)]

updating
:   true while we're waiting for a response from the tracker.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:announce_infohash%3A%3A%5Bstart_sent%5D&labels=documentation&body=Documentation+under+heading+%22announce_infohash%3A%3A%5Bstart_sent%5D%22+could+be+improved)]

start\_sent
:   set to true when we get a valid response from an announce
    with event=started. If it is set, we won't send start in the subsequent
    announces.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:announce_infohash%3A%3A%5Bcomplete_sent%5D&labels=documentation&body=Documentation+under+heading+%22announce_infohash%3A%3A%5Bcomplete_sent%5D%22+could+be+improved)]

complete\_sent
:   set to true when we send a event=completed.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:class+announce_endpoint&labels=documentation&body=Documentation+under+heading+%22class+announce_endpoint%22+could+be+improved)]

# announce\_endpoint

Declared in "[libtorrent/announce\_entry.hpp](include/libtorrent/announce_entry.hpp)"

announces are sent to each tracker using every listen socket
this class holds information about one listen socket for one tracker

```cpp
struct announce_endpoint
{
   announce_endpoint ();

   tcp::endpoint local_endpoint;
   aux::array<announce_infohash, num_protocols, protocol_version> info_hashes;
   bool enabled  = true;
};
```

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:announce_endpoint%3A%3A%5Blocal_endpoint%5D&labels=documentation&body=Documentation+under+heading+%22announce_endpoint%3A%3A%5Blocal_endpoint%5D%22+could+be+improved)]

local\_endpoint
:   the local endpoint of the listen interface associated with this endpoint

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:announce_endpoint%3A%3A%5Binfo_hashes%5D&labels=documentation&body=Documentation+under+heading+%22announce_endpoint%3A%3A%5Binfo_hashes%5D%22+could+be+improved)]

info\_hashes
:   info\_hashes[0] is the v1 info hash (SHA1)
    info\_hashes[1] is the v2 info hash (truncated SHA-256)

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:announce_endpoint%3A%3A%5Benabled%5D&labels=documentation&body=Documentation+under+heading+%22announce_endpoint%3A%3A%5Benabled%5D%22+could+be+improved)]

enabled
:   set to false to not announce from this endpoint

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:class+announce_entry&labels=documentation&body=Documentation+under+heading+%22class+announce_entry%22+could+be+improved)]

# announce\_entry

Declared in "[libtorrent/announce\_entry.hpp](include/libtorrent/announce_entry.hpp)"

this class holds information about one bittorrent tracker, as it
relates to a specific torrent.

```cpp
struct announce_entry
{
   announce_entry (announce_entry const&);
   announce_entry& operator= (announce_entry const&) &;
   ~announce_entry ();
   announce_entry ();
   explicit announce_entry (string_view u);

   enum tracker_source
   {
      source_torrent,
      source_client,
      source_magnet_link,
      source_tex,
   };

   std::string url;
   std::string trackerid;
   std::vector<announce_endpoint> endpoints;
   std::uint8_t tier  = 0;
   std::uint8_t fail_limit  = 0;
   std::uint8_t source:4;
   bool verified:1;
};
```

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:announce_entry%3A%3A%5Bannounce_entry%28%29+operator%3D%28%29+~announce_entry%28%29%5D&labels=documentation&body=Documentation+under+heading+%22announce_entry%3A%3A%5Bannounce_entry%28%29+operator%3D%28%29+~announce_entry%28%29%5D%22+could+be+improved)]

## announce\_entry() operator=() ~announce\_entry()

```cpp
announce_entry (announce_entry const&);
announce_entry& operator= (announce_entry const&) &;
~announce_entry ();
announce_entry ();
explicit announce_entry (string_view u);
```

constructs a tracker announce [entry](reference-Bencoding.md#entry) with u as the URL.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:enum+tracker_source&labels=documentation&body=Documentation+under+heading+%22enum+tracker_source%22+could+be+improved)]

## enum tracker\_source

Declared in "[libtorrent/announce\_entry.hpp](include/libtorrent/announce_entry.hpp)"

| name | value | description |
| --- | --- | --- |
| source\_torrent | 1 | the tracker was part of the .torrent file |
| source\_client | 2 | the tracker was added programmatically via the [add\_tracker()](reference-Torrent_Info.md#add_tracker()) function |
| source\_magnet\_link | 4 | the tracker was part of a magnet link |
| source\_tex | 8 | the tracker was received from the swarm via tracker exchange |

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:announce_entry%3A%3A%5Burl%5D&labels=documentation&body=Documentation+under+heading+%22announce_entry%3A%3A%5Burl%5D%22+could+be+improved)]

url
:   tracker URL as it appeared in the torrent file

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:announce_entry%3A%3A%5Btrackerid%5D&labels=documentation&body=Documentation+under+heading+%22announce_entry%3A%3A%5Btrackerid%5D%22+could+be+improved)]

trackerid
:   the current &trackerid= argument passed to the tracker.
    this is optional and is normally empty (in which case no
    trackerid is sent).

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:announce_entry%3A%3A%5Bendpoints%5D&labels=documentation&body=Documentation+under+heading+%22announce_entry%3A%3A%5Bendpoints%5D%22+could+be+improved)]

endpoints
:   each local listen socket (endpoint) will announce to the tracker. This
    list contains state per endpoint.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:announce_entry%3A%3A%5Btier%5D&labels=documentation&body=Documentation+under+heading+%22announce_entry%3A%3A%5Btier%5D%22+could+be+improved)]

tier
:   the tier this tracker belongs to

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:announce_entry%3A%3A%5Bfail_limit%5D&labels=documentation&body=Documentation+under+heading+%22announce_entry%3A%3A%5Bfail_limit%5D%22+could+be+improved)]

fail\_limit
:   the max number of failures to announce to this tracker in
    a row, before this tracker is not used anymore. 0 means unlimited

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:announce_entry%3A%3A%5Bsource%5D&labels=documentation&body=Documentation+under+heading+%22announce_entry%3A%3A%5Bsource%5D%22+could+be+improved)]

source
:   a bitmask specifying which sources we got this tracker from.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:announce_entry%3A%3A%5Bverified%5D&labels=documentation&body=Documentation+under+heading+%22announce_entry%3A%3A%5Bverified%5D%22+could+be+improved)]

verified
:   set to true the first time we receive a valid response
    from this tracker.
