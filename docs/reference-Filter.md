---
title: "Filter"
source: "https://libtorrent.org/reference-Filter.html"
---

# ip\_filter

Declared in "[libtorrent/ip\_filter.hpp](include/libtorrent/ip_filter.hpp)"

The ip\_filter class is a set of rules that uniquely categorizes all
ip addresses as allowed or disallowed. The default constructor creates
a single rule that allows all addresses (0.0.0.0 - 255.255.255.255 for
the IPv4 range, and the equivalent range covering all addresses for the
IPv6 range).

A default constructed [ip\_filter](reference-Filter.md#ip_filter) does not filter any address.

```cpp
struct ip_filter
{
   ip_filter ();
   ip_filter& operator= (ip_filter const&);
   ~ip_filter ();
   ip_filter (ip_filter&&);
   ip_filter& operator= (ip_filter&&);
   ip_filter (ip_filter const&);
   bool empty () const;
   void add_rule (address const& first, address const& last, std::uint32_t flags);
   std::uint32_t access (address const& addr) const;
   filter_tuple_t export_filter () const;

   enum access_flags
   {
      blocked,
   };
};
```

## empty()

```cpp
bool empty () const;
```

returns true if the filter does not contain any rules

## add\_rule()

```cpp
void add_rule (address const& first, address const& last, std::uint32_t flags);
```

Adds a rule to the filter. first and last defines a range of
ip addresses that will be marked with the given flags. The flags
can currently be 0, which means allowed, or ip\_filter::blocked, which
means disallowed.

precondition:
first.is\_v4() == last.is\_v4() && first.is\_v6() == last.is\_v6()

postcondition:
access(x) == flags for every x in the range [first, last]

This means that in a case of overlapping ranges, the last one applied takes
precedence.

## access()

```cpp
std::uint32_t access (address const& addr) const;
```

Returns the access permissions for the given address (addr). The permission
can currently be 0 or ip\_filter::blocked. The complexity of this operation
is O(log n), where n is the minimum number of non-overlapping ranges to describe
the current filter.

## export\_filter()

```cpp
filter_tuple_t export_filter () const;
```

This function will return the current state of the filter in the minimum number of
ranges possible. They are sorted from ranges in low addresses to high addresses. Each
[entry](reference-Bencoding.md#entry) in the returned vector is a range with the access control specified in its
flags field.

The return value is a tuple containing two range-lists. One for IPv4 addresses
and one for IPv6 addresses.

## enum access\_flags

Declared in "[libtorrent/ip\_filter.hpp](include/libtorrent/ip_filter.hpp)"

| name | value | description |
| --- | --- | --- |
| blocked | 1 | indicates that IPs in this range should not be connected to nor accepted as incoming connections |

# port\_filter

Declared in "[libtorrent/ip\_filter.hpp](include/libtorrent/ip_filter.hpp)"

the port filter maps non-overlapping port ranges to flags. This
is primarily used to indicate whether a range of ports should
be connected to or not. The default is to have the full port
range (0-65535) set to flag 0.

```cpp
class port_filter
{
   port_filter (port_filter const&);
   port_filter (port_filter&&);
   port_filter ();
   ~port_filter ();
   port_filter& operator= (port_filter const&);
   port_filter& operator= (port_filter&&);
   void add_rule (std::uint16_t first, std::uint16_t last, std::uint32_t flags);
   std::uint32_t access (std::uint16_t port) const;

   enum access_flags
   {
      blocked,
   };
};
```

## add\_rule()

```cpp
void add_rule (std::uint16_t first, std::uint16_t last, std::uint32_t flags);
```

set the flags for the specified port range (first, last) to
flags overwriting any existing rule for those ports. The range
is inclusive, i.e. the port last also has the flag set on it.

## access()

```cpp
std::uint32_t access (std::uint16_t port) const;
```

test the specified port (port) for whether it is blocked
or not. The returned value is the flags set for this port.
see [access\_flags](reference-Filter.md#access_flags).

## enum access\_flags

Declared in "[libtorrent/ip\_filter.hpp](include/libtorrent/ip_filter.hpp)"

| name | value | description |
| --- | --- | --- |
| blocked | 1 | this flag indicates that destination ports in the range should not be connected to |
