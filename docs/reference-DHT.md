---
title: "DHT"
source: "https://libtorrent.org/reference-DHT.html"
---

# dht\_state

Declared in "[libtorrent/kademlia/dht\_state.hpp](include/libtorrent/kademlia/dht_state.hpp)"

This structure helps to store and load the state
of the dht\_tracker.
At this moment the library is only a dual stack
implementation of the DHT. See [BEP 32](https://www.bittorrent.org/beps/bep_0032.html)

```cpp
struct dht_state
{
   void clear ();

   node_ids_t nids;
   std::vector<udp::endpoint> nodes;
   std::vector<udp::endpoint> nodes6;
};
```

nodes
:   the bootstrap nodes saved from the buckets node

nodes6
:   the bootstrap nodes saved from the IPv6 buckets node

# dht\_storage\_counters

Declared in "[libtorrent/kademlia/dht\_storage.hpp](include/libtorrent/kademlia/dht_storage.hpp)"

This structure hold the relevant [counters](reference-Stats.md#counters) for the storage

```cpp
struct dht_storage_counters
{
   void reset ();

   std::int32_t torrents  = 0;
   std::int32_t peers  = 0;
   std::int32_t immutable_data  = 0;
   std::int32_t mutable_data  = 0;
};
```

## reset()

```cpp
void reset ();
```

This member function set the [counters](reference-Stats.md#counters) to zero.

# dht\_storage\_interface

Declared in "[libtorrent/kademlia/dht\_storage.hpp](include/libtorrent/kademlia/dht_storage.hpp)"

The DHT storage interface is a pure virtual class that can
be implemented to customize how the data for the DHT is stored.

The default storage implementation uses three maps in RAM to save
the peers, mutable and immutable items and it's designed to
provide a fast and fully compliant behavior of the BEPs.

libtorrent comes with one built-in storage implementation:
dht\_default\_storage (private non-accessible class). Its
constructor function is called [dht\_default\_storage\_constructor()](reference-DHT.md#dht_default_storage_constructor()).
You should know that if this storage becomes full of DHT items,
the current implementation could degrade in performance.

```cpp
struct dht_storage_interface
{
   virtual void update_node_ids (std::vector<node_id> const& ids) = 0;
   virtual bool get_peers (sha1_hash const& info_hash
      , bool noseed, bool scrape, address const& requester
      , entry& peers) const = 0;
   virtual void announce_peer (sha1_hash const& info_hash
      , tcp::endpoint const& endp
      , string_view name, bool seed) = 0;
   virtual bool get_immutable_item (sha1_hash const& target
      , entry& item) const = 0;
   virtual void put_immutable_item (sha1_hash const& target
      , span<char const> buf
      , address const& addr) = 0;
   virtual bool get_mutable_item_seq (sha1_hash const& target
      , sequence_number& seq) const = 0;
   virtual bool get_mutable_item (sha1_hash const& target
      , sequence_number seq, bool force_fill
      , entry& item) const = 0;
   virtual void put_mutable_item (sha1_hash const& target
      , span<char const> buf
      , signature const& sig
      , sequence_number seq
      , public_key const& pk
      , span<char const> salt
      , address const& addr) = 0;
   virtual int get_infohashes_sample (entry& item) = 0;
   virtual void tick () = 0;
   virtual dht_storage_counters counters () const = 0;
};
```

## update\_node\_ids()

```cpp
virtual void update_node_ids (std::vector<node_id> const& ids) = 0;
```

This member function notifies the list of all node's ids
of each DHT running inside libtorrent. It's advisable
that the concrete implementation keeps a copy of this list
for an eventual prioritization when deleting an element
to make room for a new one.

## get\_peers()

```cpp
virtual bool get_peers (sha1_hash const& info_hash
      , bool noseed, bool scrape, address const& requester
      , entry& peers) const = 0;
```

This function retrieve the peers tracked by the DHT
corresponding to the given info\_hash. You can specify if
you want only seeds and/or you are scraping the data.

For future implementers:
If the torrent tracked contains a name, such a name
must be stored as a string in peers["n"]

If the scrape parameter is true, you should fill these keys:

> peers["BFpe"]
> :   with the standard bit representation of a
>     256 bloom filter containing the downloaders
>
> peers["BFsd"]
> :   with the standard bit representation of a
>     256 bloom filter containing the seeders

If the scrape parameter is false, you should fill the
key peers["values"] with a list containing a subset of
peers tracked by the given info\_hash. Such a list should
consider the value of [settings\_pack::dht\_max\_peers\_reply](reference-Settings.md#dht_max_peers_reply).
If noseed is true only peers marked as no seed should be included.

returns true if the maximum number of peers are stored
for this info\_hash.

## announce\_peer()

```cpp
virtual void announce_peer (sha1_hash const& info_hash
      , tcp::endpoint const& endp
      , string_view name, bool seed) = 0;
```

This function is named announce\_peer for consistency with the
upper layers, but has nothing to do with networking. Its only
responsibility is store the peer in such a way that it's returned
in the [entry](reference-Bencoding.md#entry) with the lookup\_peers.

The name parameter is the name of the torrent if provided in
the announce\_peer DHT message. The length of this value should
have a maximum length in the final storage. The default
implementation truncate the value for a maximum of 50 characters.

## get\_immutable\_item()

```cpp
virtual bool get_immutable_item (sha1_hash const& target
      , entry& item) const = 0;
```

This function retrieves the immutable item given its target hash.

For future implementers:
The value should be returned as an [entry](reference-Bencoding.md#entry) in the key item["v"].

returns true if the item is found and the data is returned
inside the ([entry](reference-Bencoding.md#entry)) out parameter item.

## put\_immutable\_item()

```cpp
virtual void put_immutable_item (sha1_hash const& target
      , span<char const> buf
      , address const& addr) = 0;
```

Store the item's data. This layer is only for storage.
The authentication of the item is performed by the upper layer.

For implementers:
This data can be stored only if the target is not already
present. The implementation should consider the value of
[settings\_pack::dht\_max\_dht\_items](reference-Settings.md#dht_max_dht_items).

## get\_mutable\_item\_seq()

```cpp
virtual bool get_mutable_item_seq (sha1_hash const& target
      , sequence_number& seq) const = 0;
```

This function retrieves the sequence number of a mutable item.

returns true if the item is found and the data is returned
inside the out parameter seq.

## get\_mutable\_item()

```cpp
virtual bool get_mutable_item (sha1_hash const& target
      , sequence_number seq, bool force_fill
      , entry& item) const = 0;
```

This function retrieves the mutable stored in the DHT.

For implementers:
The item sequence should be stored in the key item["seq"].
if force\_fill is true or (0 <= seq and seq < item["seq"])
the following keys should be filled
item["v"] - with the value no encoded.
item["sig"] - with a string representation of the signature.
item["k"] - with a string representation of the public key.

returns true if the item is found and the data is returned
inside the ([entry](reference-Bencoding.md#entry)) out parameter item.

## put\_mutable\_item()

```cpp
virtual void put_mutable_item (sha1_hash const& target
      , span<char const> buf
      , signature const& sig
      , sequence_number seq
      , public_key const& pk
      , span<char const> salt
      , address const& addr) = 0;
```

Store the item's data. This layer is only for storage.
The authentication of the item is performed by the upper layer.

For implementers:
The sequence number should be checked if the item is already
present. The implementation should consider the value of
[settings\_pack::dht\_max\_dht\_items](reference-Settings.md#dht_max_dht_items).

## get\_infohashes\_sample()

```cpp
virtual int get_infohashes_sample (entry& item) = 0;
```

This function retrieves a sample info-hashes

For implementers:
The info-hashes should be stored in ["samples"] (N x 20 bytes).
the following keys should be filled
item["interval"] - the subset refresh interval in seconds.
item["num"] - number of info-hashes in storage.

Internally, this function is allowed to lazily evaluate, cache
and modify the actual sample to put in item

returns the number of info-hashes in the sample.

## tick()

```cpp
virtual void tick () = 0;
```

This function is called periodically (non-constant frequency).

For implementers:
Use this functions for expire peers or items or any other
storage cleanup.

## counters()

```cpp
virtual dht_storage_counters counters () const = 0;
```

return stats [counters](reference-Stats.md#counters) for the store

# dht\_default\_storage\_constructor()

Declared in "[libtorrent/kademlia/dht\_storage.hpp](include/libtorrent/kademlia/dht_storage.hpp)"

```cpp
std::unique_ptr<dht_storage_interface> dht_default_storage_constructor (
   settings_interface const& settings);
```

constructor for the default DHT storage. The DHT storage is responsible
for maintaining peers and mutable and immutable items announced and
stored/put to the DHT node.

# sign\_mutable\_item()

Declared in "[libtorrent/kademlia/item.hpp](include/libtorrent/kademlia/item.hpp)"

```cpp
signature sign_mutable_item (
   span<char const> v
   , span<char const> salt
   , sequence_number seq
   , public_key const& pk
   , secret_key const& sk);
```

given a byte range v and an optional byte range salt, a
sequence number, public key pk (must be 32 bytes) and a secret key
sk (must be 64 bytes), this function produces a signature which
is written into a 64 byte buffer pointed to by sig. The caller
is responsible for allocating the destination buffer that's passed in
as the sig argument. Typically it would be allocated on the stack.

# announce\_flags\_t

Declared in "[libtorrent/kademlia/announce\_flags.hpp](include/libtorrent/kademlia/announce_flags.hpp)"

seed
:   announce to DHT as a seed

implied\_port
:   announce to DHT with the implied-port flag set. This tells the network to use
    your source UDP port as your listen port, rather than the one specified in
    the message. This may improve the chances of traversing NATs when using uTP.

ssl\_torrent
:   Specify the port number for the SSL listen socket in the DHT announce.
