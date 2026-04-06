---
title: "peer_class_info"
source: "https://libtorrent.org/reference-PeerClass.html"
---

[home](reference.md)

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:class+peer_class_info&labels=documentation&body=Documentation+under+heading+%22class+peer_class_info%22+could+be+improved)]

# peer\_class\_info

Declared in "[libtorrent/peer\_class.hpp](include/libtorrent/peer_class.hpp)"

holds settings for a peer class. Used in [set\_peer\_class()](reference-Session.md#set_peer_class()) and
[get\_peer\_class()](reference-Session.md#get_peer_class()) calls.

```cpp
struct peer_class_info
{
   bool ignore_unchoke_slots;
   int connection_limit_factor;
   std::string label;
   int upload_limit;
   int download_limit;
   int upload_priority;
   int download_priority;
};
```

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:peer_class_info%3A%3A%5Bignore_unchoke_slots%5D&labels=documentation&body=Documentation+under+heading+%22peer_class_info%3A%3A%5Bignore_unchoke_slots%5D%22+could+be+improved)]

ignore\_unchoke\_slots
:   ignore\_unchoke\_slots determines whether peers should always
    unchoke a peer, regardless of the choking algorithm, or if it should
    honor the unchoke slot limits. It's used for local peers by default.
    If *any* of the peer classes a peer belongs to has this set to true,
    that peer will be unchoked at all times.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:peer_class_info%3A%3A%5Bconnection_limit_factor%5D&labels=documentation&body=Documentation+under+heading+%22peer_class_info%3A%3A%5Bconnection_limit_factor%5D%22+could+be+improved)]

connection\_limit\_factor
:   adjusts the connection limit (global and per torrent) that applies to
    this peer class. By default, local peers are allowed to exceed the
    normal connection limit for instance. This is specified as a percent
    factor. 100 makes the peer class apply normally to the limit. 200
    means as long as there are fewer connections than twice the limit, we
    accept this peer. This factor applies both to the global connection
    limit and the per-torrent limit. Note that if not used carefully one
    peer class can potentially completely starve out all other over time.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:peer_class_info%3A%3A%5Blabel%5D&labels=documentation&body=Documentation+under+heading+%22peer_class_info%3A%3A%5Blabel%5D%22+could+be+improved)]

label
:   not used by libtorrent. It's intended as a potentially user-facing
    identifier of this peer class.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:peer_class_info%3A%3A%5Bupload_limit+download_limit%5D&labels=documentation&body=Documentation+under+heading+%22peer_class_info%3A%3A%5Bupload_limit+download_limit%5D%22+could+be+improved)]

upload\_limit download\_limit
:   transfer rates limits for the whole peer class. They are specified in
    bytes per second and apply to the sum of all peers that are members of
    this class.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:peer_class_info%3A%3A%5Bupload_priority+download_priority%5D&labels=documentation&body=Documentation+under+heading+%22peer_class_info%3A%3A%5Bupload_priority+download_priority%5D%22+could+be+improved)]

upload\_priority download\_priority
:   relative priorities used by the bandwidth allocator in the rate
    limiter. If no rate limits are in use, the priority is not used
    either. Priorities start at 1 (0 is not a valid priority) and may not
    exceed 255.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:class+peer_class_type_filter&labels=documentation&body=Documentation+under+heading+%22class+peer_class_type_filter%22+could+be+improved)]

# peer\_class\_type\_filter

Declared in "[libtorrent/peer\_class\_type\_filter.hpp](include/libtorrent/peer_class_type_filter.hpp)"

peer\_class\_type\_filter is a simple container for rules for adding and subtracting
peer-classes from peers. It is applied *after* the peer class filter is applied (which
is based on the peer's IP address).

```cpp
struct peer_class_type_filter
{
   void remove (socket_type_t const st, peer_class_t const peer_class);
   void add (socket_type_t const st, peer_class_t const peer_class);
   void allow (socket_type_t const st, peer_class_t const peer_class);
   void disallow (socket_type_t const st, peer_class_t const peer_class);
   std::uint32_t apply (socket_type_t const st, std::uint32_t peer_class_mask);
   friend bool operator== (peer_class_type_filter const& lhs
      , peer_class_type_filter const& rhs);

   enum socket_type_t
   {
      tcp_socket,
      utp_socket,
      ssl_tcp_socket,
      ssl_utp_socket,
      i2p_socket,
      num_socket_types,
   };
};
```

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:peer_class_type_filter%3A%3A%5Bremove%28%29+add%28%29%5D&labels=documentation&body=Documentation+under+heading+%22peer_class_type_filter%3A%3A%5Bremove%28%29+add%28%29%5D%22+could+be+improved)]

## remove() add()

```cpp
void remove (socket_type_t const st, peer_class_t const peer_class);
void add (socket_type_t const st, peer_class_t const peer_class);
```

add() and remove() adds and removes a peer class to be added
to new peers based on socket type.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:peer_class_type_filter%3A%3A%5Ballow%28%29+disallow%28%29%5D&labels=documentation&body=Documentation+under+heading+%22peer_class_type_filter%3A%3A%5Ballow%28%29+disallow%28%29%5D%22+could+be+improved)]

## allow() disallow()

```cpp
void allow (socket_type_t const st, peer_class_t const peer_class);
void disallow (socket_type_t const st, peer_class_t const peer_class);
```

disallow() and allow() adds and removes a peer class to be
removed from new peers based on socket type.

The peer\_class argument cannot be greater than 31. The bitmasks representing
peer classes in the peer\_class\_type\_filter are 32 bits.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:peer_class_type_filter%3A%3A%5Bapply%28%29%5D&labels=documentation&body=Documentation+under+heading+%22peer_class_type_filter%3A%3A%5Bapply%28%29%5D%22+could+be+improved)]

## apply()

```cpp
std::uint32_t apply (socket_type_t const st, std::uint32_t peer_class_mask);
```

takes a bitmask of peer classes and returns a new bitmask of
peer classes after the rules have been applied, based on the socket type argument
(st).

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:enum+socket_type_t&labels=documentation&body=Documentation+under+heading+%22enum+socket_type_t%22+could+be+improved)]

## enum socket\_type\_t

Declared in "[libtorrent/peer\_class\_type\_filter.hpp](include/libtorrent/peer_class_type_filter.hpp)"

| name | value | description |
| --- | --- | --- |
| tcp\_socket | 0 | these match the socket types from socket\_type.hpp shifted one down |
| utp\_socket | 1 |  |
| ssl\_tcp\_socket | 2 |  |
| ssl\_utp\_socket | 3 |  |
| i2p\_socket | 4 |  |
| num\_socket\_types | 5 |  |
