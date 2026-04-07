---
title: "ed25519"
source: "https://libtorrent.org/reference-ed25519.html"
---

# ed25519\_create\_seed()

Declared in "[libtorrent/kademlia/ed25519.hpp](include/libtorrent/kademlia/ed25519.hpp)"

```cpp
std::array<char, 32> ed25519_create_seed ();
```

See documentation of internal random\_bytes

# ed25519\_create\_keypair()

Declared in "[libtorrent/kademlia/ed25519.hpp](include/libtorrent/kademlia/ed25519.hpp)"

```cpp
std::tuple<public_key, secret_key> ed25519_create_keypair (
   std::array<char, 32> const& seed);
```

Creates a new key pair from the given seed.

It's important to clarify that the seed completely determines
the key pair. Then it's enough to save the seed and the
public key as the key-pair in a buffer of 64 bytes. The standard
is (32 bytes seed, 32 bytes public key).

This function does work with a given seed, giving you a pair of
(64 bytes private key, 32 bytes public key). It's a trade-off between
space and CPU, saving in one format or another.

The smaller format is not weaker by any means, in fact, it is only
the seed (32 bytes) that determines the point in the curve.

# ed25519\_sign()

Declared in "[libtorrent/kademlia/ed25519.hpp](include/libtorrent/kademlia/ed25519.hpp)"

```cpp
signature ed25519_sign (span<char const> msg
   , public_key const& pk, secret_key const& sk);
```

Creates a signature of the given message with the given key pair.

# ed25519\_verify()

Declared in "[libtorrent/kademlia/ed25519.hpp](include/libtorrent/kademlia/ed25519.hpp)"

```cpp
bool ed25519_verify (signature const& sig
   , span<char const> msg, public_key const& pk);
```

Verifies the signature on the given message using pk

# ed25519\_add\_scalar()

Declared in "[libtorrent/kademlia/ed25519.hpp](include/libtorrent/kademlia/ed25519.hpp)"

```cpp
secret_key ed25519_add_scalar (secret_key const& sk
   , std::array<char, 32> const& scalar);
public_key ed25519_add_scalar (public_key const& pk
   , std::array<char, 32> const& scalar);
```

Adds a scalar to the given key pair where scalar is a 32 byte buffer
(possibly generated with ed25519\_create\_seed), generating a new key pair.

You can calculate the public key sum without knowing the private key and
vice versa by passing in null for the key you don't know. This is useful
when a third party (an authoritative server for example) needs to enforce
randomness on a key pair while only knowing the public key of the other
side.

Warning: the last bit of the scalar is ignored - if comparing scalars make
sure to clear it with scalar[31] &= 127.

see <http://crypto.stackexchange.com/a/6215/4697>
see test\_ed25519 for a practical example

# ed25519\_key\_exchange()

Declared in "[libtorrent/kademlia/ed25519.hpp](include/libtorrent/kademlia/ed25519.hpp)"

```cpp
std::array<char, 32> ed25519_key_exchange (
   public_key const& pk, secret_key const& sk);
```

Performs a key exchange on the given public key and private key, producing a
shared secret. It is recommended to hash the shared secret before using it.

This is useful when two parties want to share a secret but both only knows
their respective public keys.
see test\_ed25519 for a practical example
