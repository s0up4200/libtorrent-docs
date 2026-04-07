---
title: "Utility"
source: "https://libtorrent.org/reference-Utility.html"
---

# hasher

Declared in "[libtorrent/hasher.hpp](include/libtorrent/hasher.hpp)"

this is a SHA-1 hash class.

You use it by first instantiating it, then call update() to feed it
with data. i.e. you don't have to keep the entire buffer of which you want to
create the hash in memory. You can feed the [hasher](reference-Utility.md#hasher) parts of it at a time. When
You have fed the [hasher](reference-Utility.md#hasher) with all the data, you call final() and it
will return the sha1-hash of the data.

The constructor that takes a char const\* and an integer will construct the
sha1 context and feed it the data passed in.

If you want to reuse the [hasher](reference-Utility.md#hasher) object once you have created a hash, you have to
call reset() to reinitialize it.

The built-in software version of sha1-algorithm was implemented
by Steve Reid and released as public domain.
For more info, see src/sha1.cpp.

```cpp
class hasher
{
   hasher ();
   hasher (char const* data, int len);
   explicit hasher (span<char const> data);
   hasher (hasher const&);
   hasher& operator= (hasher const&) &;
   hasher& update (char const* data, int len);
   hasher& update (span<char const> data);
   sha1_hash final ();
   void reset ();
};
```

## operator=() hasher()

```cpp
hasher (char const* data, int len);
explicit hasher (span<char const> data);
hasher (hasher const&);
hasher& operator= (hasher const&) &;
```

this is the same as default constructing followed by a call to
update(data, len).

## update()

```cpp
hasher& update (char const* data, int len);
hasher& update (span<char const> data);
```

append the following bytes to what is being hashed

## final()

```cpp
sha1_hash final ();
```

returns the SHA-1 digest of the buffers previously passed to
[update()](reference-Utility.md#update()) and the [hasher](reference-Utility.md#hasher) constructor.

## reset()

```cpp
void reset ();
```

restore the [hasher](reference-Utility.md#hasher) state to be as if the [hasher](reference-Utility.md#hasher) has just been
default constructed.

# hasher256

Declared in "[libtorrent/hasher.hpp](include/libtorrent/hasher.hpp)"

```cpp
class hasher256
{
   hasher256 ();
   hasher256 (hasher256 const&);
   explicit hasher256 (span<char const> data);
   hasher256 (char const* data, int len);
   hasher256& operator= (hasher256 const&) &;
   hasher256& update (char const* data, int len);
   hasher256& update (span<char const> data);
   sha256_hash final ();
   void reset ();
   ~hasher256 ();
};
```

## hasher256() operator=()

```cpp
hasher256 (hasher256 const&);
explicit hasher256 (span<char const> data);
hasher256 (char const* data, int len);
hasher256& operator= (hasher256 const&) &;
```

this is the same as default constructing followed by a call to
update(data, len).

## update()

```cpp
hasher256& update (char const* data, int len);
hasher256& update (span<char const> data);
```

append the following bytes to what is being hashed

## final()

```cpp
sha256_hash final ();
```

returns the SHA-1 digest of the buffers previously passed to
[update()](reference-Utility.md#update()) and the [hasher](reference-Utility.md#hasher) constructor.

## reset()

```cpp
void reset ();
```

restore the [hasher](reference-Utility.md#hasher) state to be as if the [hasher](reference-Utility.md#hasher) has just been
default constructed.

# bitfield

Declared in "[libtorrent/bitfield.hpp](include/libtorrent/bitfield.hpp)"

The [bitfield](reference-Utility.md#bitfield) type stores any number of bits as a [bitfield](reference-Utility.md#bitfield)
in a heap allocated array.

```cpp
struct bitfield
{
   explicit bitfield (int bits);
   bitfield () noexcept = default;
   bitfield (int bits, bool val);
   bitfield (bitfield&& rhs) noexcept = default;
   bitfield (bitfield const& rhs);
   bitfield (char const* b, int bits);
   void assign (char const* b, int const bits);
   bool operator[] (int index) const noexcept;
   bool get_bit (int index) const noexcept;
   void set_bit (int index) noexcept;
   void clear_bit (int index) noexcept;
   bool all_set () const noexcept;
   bool none_set () const noexcept;
   int size () const noexcept;
   int num_words () const noexcept;
   int num_bytes () const noexcept;
   bool empty () const noexcept;
   char const* data () const noexcept;
   char* data () noexcept;
   void swap (bitfield& rhs) noexcept;
   int count () const noexcept;
   int find_first_set () const noexcept;
   int find_last_clear () const noexcept;
   bool operator== (lt::bitfield const& rhs) const;
};
```

## bitfield()

```cpp
explicit bitfield (int bits);
bitfield () noexcept = default;
bitfield (int bits, bool val);
bitfield (bitfield&& rhs) noexcept = default;
bitfield (bitfield const& rhs);
bitfield (char const* b, int bits);
```

constructs a new [bitfield](reference-Utility.md#bitfield). The default constructor creates an empty
[bitfield](reference-Utility.md#bitfield). bits is the size of the [bitfield](reference-Utility.md#bitfield) (specified in bits).
val is the value to initialize the bits to. If not specified
all bits are initialized to 0.

The constructor taking a pointer b and bits copies a [bitfield](reference-Utility.md#bitfield)
from the specified buffer, and bits number of bits (rounded up to
the nearest byte boundary).

## assign()

```cpp
void assign (char const* b, int const bits);
```

copy [bitfield](reference-Utility.md#bitfield) from buffer b of bits number of bits, rounded up to
the nearest byte boundary.

## operator[]() get\_bit()

```cpp
bool operator[] (int index) const noexcept;
bool get_bit (int index) const noexcept;
```

query bit at index. Returns true if bit is 1, otherwise false.

## set\_bit() clear\_bit()

```cpp
void set_bit (int index) noexcept;
void clear_bit (int index) noexcept;
```

set bit at index to 0 (clear\_bit) or 1 (set\_bit).

## all\_set()

```cpp
bool all_set () const noexcept;
```

returns true if all bits in the [bitfield](reference-Utility.md#bitfield) are set

## none\_set()

```cpp
bool none_set () const noexcept;
```

returns true if no bit in the [bitfield](reference-Utility.md#bitfield) is set

## size()

```cpp
int size () const noexcept;
```

returns the size of the [bitfield](reference-Utility.md#bitfield) in bits.

## num\_words()

```cpp
int num_words () const noexcept;
```

returns the number of 32 bit words are needed to represent all bits in
this [bitfield](reference-Utility.md#bitfield).

## num\_bytes()

```cpp
int num_bytes () const noexcept;
```

returns the number of bytes needed to represent all bits in this
[bitfield](reference-Utility.md#bitfield)

## empty()

```cpp
bool empty () const noexcept;
```

returns true if the [bitfield](reference-Utility.md#bitfield) has zero size.

## data()

```cpp
char const* data () const noexcept;
char* data () noexcept;
```

returns a pointer to the internal buffer of the [bitfield](reference-Utility.md#bitfield), or
nullptr if it's empty.

## swap()

```cpp
void swap (bitfield& rhs) noexcept;
```

swaps the bit-fields two variables refer to

## count()

```cpp
int count () const noexcept;
```

count the number of bits in the [bitfield](reference-Utility.md#bitfield) that are set to 1.

## find\_first\_set()

```cpp
int find_first_set () const noexcept;
```

returns the index of the first set bit in the [bitfield](reference-Utility.md#bitfield), i.e. 1 bit.

## find\_last\_clear()

```cpp
int find_last_clear () const noexcept;
```

returns the index to the last cleared bit in the [bitfield](reference-Utility.md#bitfield), i.e. 0 bit.
