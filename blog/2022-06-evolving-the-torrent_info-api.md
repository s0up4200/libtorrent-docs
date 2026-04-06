---
title: "evolving the torrent_info API"
date: "2022-06"
source: "https://blog.libtorrent.org/2022/06/evolving-the-torrent_info-api/"
---

Sunday, June 12th, 2022 by arvid

Currently, torrent files are loaded by the [`torrent_info`](https://libtorrent.org/reference-Torrent_Info.html#torrent_info()) constructor. The `torrent_info` object essentially holds all state from the .torrent file.  
This post is arguing in favor of moving towards torrent\_info only representing the *immutable* portion of torrent files. i.e. what’s in the info-section.

This is primarily motivated by the v2 piece-layers that are currently part of torrent\_info. The piece layers, when parsed into merkle trees, have a non-trivial size. So once a torrent is added to a session, they need to be removed from the torrent\_info object and stored in their internal representation in the session. Because of this, a `torrent_info` object you get by calling [`torrent_handle::torrent_file()`](http://libtorrent.org/reference-Torrent_Handle.html#torrent-file-torrent-file-with-hashes) is now a “crippled” version of what you get when loading the same torrent file from disk. i.e. the piece layers are stripped when added to the session. For v2 torrents, it’s no longer possible to save a copy of the .torrent file from a `torrent_handle` by just asking for the torrent\_info object, you have to call [`torrent_file_with_hashes()`](http://libtorrent.org/reference-Torrent_Handle.html#torrent-file-torrent-file-with-hashes). This new function is more expensive because it needs to make a copy of the `torrent_info` object and also copy the piece layers into it.

I believe a cleaner and clearer future API to move towards would be to make torrent\_info represent the immutable info-section, and `add_torrent_params` represent the whole torrent (as well as resume data). It already holds most necessary states. A few new fields would have to be added:

* comment
* created by
* creation date
* similar torrents
* collections

It would mean `torrent_info` would not hold trackers or web seeds, since those are mutable.

Similar torrent lists and collections lists can be found both inside the info-dictionary, and outside of it. So these need to live in both `torrent_info` and `add_torrent_params`.  
The benefits I anticipate with this design are:

## Simplifying adding torrents

Currently the `torrent_info` and `add_torrent_params` duplicate some fields like trackers and web seeds. There are flags to indicate whether they should be merged or whether the resume data should take precedence. (see `override_trackers` and `override_web_seeds` [here](http://libtorrent.org/reference-Core.html#torrent_flags_t)).

A new `load_torrent_file()` function can load the torrent into an `add_torrent_params` object. Thus, trackers, web seeds and piece layers (or any other mutable metadata) can be loaded *just* into the (mutable) `add_torrent_params`, and `torrent_info` won’t overlap with any of those fields.

## Simplifying saving .torrent files

Saving a torrent file from a `torrent_handle` would just be a matter of asking to save resume data (which posts an `add_torrent_params` object in an alert. This can then be passed to `write_torrent_file()`to write it to disk. Since the resume data already contains trackers, web seeds and the piece layer hashes, it has all it needs to write a complete .torrent file.

This also has the added benefit of being able to request the resume data asynchronously, without blocking the calling thread.

## Simplifying making magnet links

Just like writing a torrent file, making a magnet URI is a matter of first requesting the resume data (`add_torrent_params`) and pass that to `make_magnet_uri()`.

## new API

This new API would be made up by the following functions (some of which are new and have already landed in RC\_2\_0):

```
void torrent_handle::save_resume_data(); // post add_torrent_params  
add_torrent_params load_torrent_file(std::string file);  
add_torrent_params parse_magnet_uri(string_view uri);  
  
std::string make_magnet_uri(add_torrent_params const&);  
entry write_torrent_file(add_torrent_params const&);  
void session::async_add_torrent(add_torrent_params);
```

## deprecations

Along with the new API, the following functions would be deprecated at some point in the future:

`torrent_info::add_tracker()`  
`torrent_info::clear_trackers()`  
`torrent_info::trackers()`

`torrent_info::add_url_seed()`  
`torrent_info::add_http_seed()`  
`torrent_info::web_seeds()`  
`torrent_info::set_web_seeds()`

`torrent_info::nodes()`  
`torrent_info::add_node()`

`torrent_info::comment()`  
`torrent_info::creator()`  
`torrent_info::creation_date()`

`make_magnet_uri(torrent_handle const&)`

Posted in [API](https://blog.libtorrent.org/category/api/)
**|**
 [No Comments](https://blog.libtorrent.org/2022/06/evolving-the-torrent_info-api/#respond)

---

### Leave a Reply [Cancel reply](/2022/06/evolving-the-torrent_info-api/#respond)

You must be [logged in](https://blog.libtorrent.org/wp-login.php?redirect_to=https%3A%2F%2Fblog.libtorrent.org%2F2022%2F06%2Fevolving-the-torrent_info-api%2F) to post a comment.
