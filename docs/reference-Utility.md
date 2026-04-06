---
title: "hasher"
source: "https://libtorrent.org/reference-Utility.html"
---

[home](reference.md)

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:class+hasher&labels=documentation&body=Documentation+under+heading+%22class+hasher%22+could+be+improved)]

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

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:hasher%3A%3A%5Boperator%3D%28%29+hasher%28%29%5D&labels=documentation&body=Documentation+under+heading+%22hasher%3A%3A%5Boperator%3D%28%29+hasher%28%29%5D%22+could+be+improved)]

## operator=() hasher()

```cpp
hasher (char const* data, int len);
explicit hasher (span<char const> data);
hasher (hasher const&);
hasher& operator= (hasher const&) &;
```

this is the same as default constructing followed by a call to
update(data, len).

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:hasher%3A%3A%5Bupdate%28%29%5D&labels=documentation&body=Documentation+under+heading+%22hasher%3A%3A%5Bupdate%28%29%5D%22+could+be+improved)]

## update()

```cpp
hasher& update (char const* data, int len);
hasher& update (span<char const> data);
```

append the following bytes to what is being hashed

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:hasher%3A%3A%5Bfinal%28%29%5D&labels=documentation&body=Documentation+under+heading+%22hasher%3A%3A%5Bfinal%28%29%5D%22+could+be+improved)]

## final()

```cpp
sha1_hash final ();
```

returns the SHA-1 digest of the buffers previously passed to
[update()](reference-Utility.md#update()) and the [hasher](reference-Utility.md#hasher) constructor.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:hasher%3A%3A%5Breset%28%29%5D&labels=documentation&body=Documentation+under+heading+%22hasher%3A%3A%5Breset%28%29%5D%22+could+be+improved)]

## reset()

```cpp
void reset ();
```

restore the [hasher](reference-Utility.md#hasher) state to be as if the [hasher](reference-Utility.md#hasher) has just been
default constructed.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:class+hasher256&labels=documentation&body=Documentation+under+heading+%22class+hasher256%22+could+be+improved)]

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

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:hasher256%3A%3A%5Bhasher256%28%29+operator%3D%28%29%5D&labels=documentation&body=Documentation+under+heading+%22hasher256%3A%3A%5Bhasher256%28%29+operator%3D%28%29%5D%22+could+be+improved)]

## hasher256() operator=()

```cpp
hasher256 (hasher256 const&);
explicit hasher256 (span<char const> data);
hasher256 (char const* data, int len);
hasher256& operator= (hasher256 const&) &;
```

this is the same as default constructing followed by a call to
update(data, len).

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:hasher256%3A%3A%5Bupdate%28%29%5D&labels=documentation&body=Documentation+under+heading+%22hasher256%3A%3A%5Bupdate%28%29%5D%22+could+be+improved)]

## update()

```cpp
hasher256& update (char const* data, int len);
hasher256& update (span<char const> data);
```

append the following bytes to what is being hashed

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:hasher256%3A%3A%5Bfinal%28%29%5D&labels=documentation&body=Documentation+under+heading+%22hasher256%3A%3A%5Bfinal%28%29%5D%22+could+be+improved)]

## final()

```cpp
sha256_hash final ();
```

returns the SHA-1 digest of the buffers previously passed to
[update()](reference-Utility.md#update()) and the [hasher](reference-Utility.md#hasher) constructor.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:hasher256%3A%3A%5Breset%28%29%5D&labels=documentation&body=Documentation+under+heading+%22hasher256%3A%3A%5Breset%28%29%5D%22+could+be+improved)]

## reset()

```cpp
void reset ();
```

restore the [hasher](reference-Utility.md#hasher) state to be as if the [hasher](reference-Utility.md#hasher) has just been
default constructed.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:class+bitfield&labels=documentation&body=Documentation+under+heading+%22class+bitfield%22+could+be+improved)]

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

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:bitfield%3A%3A%5Bbitfield%28%29%5D&labels=documentation&body=Documentation+under+heading+%22bitfield%3A%3A%5Bbitfield%28%29%5D%22+could+be+improved)]

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

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:bitfield%3A%3A%5Bassign%28%29%5D&labels=documentation&body=Documentation+under+heading+%22bitfield%3A%3A%5Bassign%28%29%5D%22+could+be+improved)]

## assign()

```cpp
void assign (char const* b, int const bits);
```

copy [bitfield](reference-Utility.md#bitfield) from buffer b of bits number of bits, rounded up to
the nearest byte boundary.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:bitfield%3A%3A%5Boperator%5B%5D%28%29+get_bit%28%29%5D&labels=documentation&body=Documentation+under+heading+%22bitfield%3A%3A%5Boperator%5B%5D%28%29+get_bit%28%29%5D%22+could+be+improved)]

## operator[]() get\_bit()

```cpp
bool operator[] (int index) const noexcept;
bool get_bit (int index) const noexcept;
```

query bit at index. Returns true if bit is 1, otherwise false.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:bitfield%3A%3A%5Bset_bit%28%29+clear_bit%28%29%5D&labels=documentation&body=Documentation+under+heading+%22bitfield%3A%3A%5Bset_bit%28%29+clear_bit%28%29%5D%22+could+be+improved)]

## set\_bit() clear\_bit()

```cpp
void set_bit (int index) noexcept;
void clear_bit (int index) noexcept;
```

set bit at index to 0 (clear\_bit) or 1 (set\_bit).

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:bitfield%3A%3A%5Ball_set%28%29%5D&labels=documentation&body=Documentation+under+heading+%22bitfield%3A%3A%5Ball_set%28%29%5D%22+could+be+improved)]

## all\_set()

```cpp
bool all_set () const noexcept;
```

returns true if all bits in the [bitfield](reference-Utility.md#bitfield) are set

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:bitfield%3A%3A%5Bnone_set%28%29%5D&labels=documentation&body=Documentation+under+heading+%22bitfield%3A%3A%5Bnone_set%28%29%5D%22+could+be+improved)]

## none\_set()

```cpp
bool none_set () const noexcept;
```

returns true if no bit in the [bitfield](reference-Utility.md#bitfield) is set

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:bitfield%3A%3A%5Bsize%28%29%5D&labels=documentation&body=Documentation+under+heading+%22bitfield%3A%3A%5Bsize%28%29%5D%22+could+be+improved)]

## size()

```cpp
int size () const noexcept;
```

returns the size of the [bitfield](reference-Utility.md#bitfield) in bits.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:bitfield%3A%3A%5Bnum_words%28%29%5D&labels=documentation&body=Documentation+under+heading+%22bitfield%3A%3A%5Bnum_words%28%29%5D%22+could+be+improved)]

## num\_words()

```cpp
int num_words () const noexcept;
```

returns the number of 32 bit words are needed to represent all bits in
this [bitfield](reference-Utility.md#bitfield).

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:bitfield%3A%3A%5Bnum_bytes%28%29%5D&labels=documentation&body=Documentation+under+heading+%22bitfield%3A%3A%5Bnum_bytes%28%29%5D%22+could+be+improved)]

## num\_bytes()

```cpp
int num_bytes () const noexcept;
```

returns the number of bytes needed to represent all bits in this
[bitfield](reference-Utility.md#bitfield)

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:bitfield%3A%3A%5Bempty%28%29%5D&labels=documentation&body=Documentation+under+heading+%22bitfield%3A%3A%5Bempty%28%29%5D%22+could+be+improved)]

## empty()

```cpp
bool empty () const noexcept;
```

returns true if the [bitfield](reference-Utility.md#bitfield) has zero size.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:bitfield%3A%3A%5Bdata%28%29%5D&labels=documentation&body=Documentation+under+heading+%22bitfield%3A%3A%5Bdata%28%29%5D%22+could+be+improved)]

## data()

```cpp
char const* data () const noexcept;
char* data () noexcept;
```

returns a pointer to the internal buffer of the [bitfield](reference-Utility.md#bitfield), or
nullptr if it's empty.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:bitfield%3A%3A%5Bswap%28%29%5D&labels=documentation&body=Documentation+under+heading+%22bitfield%3A%3A%5Bswap%28%29%5D%22+could+be+improved)]

## swap()

```cpp
void swap (bitfield& rhs) noexcept;
```

swaps the bit-fields two variables refer to

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:bitfield%3A%3A%5Bcount%28%29%5D&labels=documentation&body=Documentation+under+heading+%22bitfield%3A%3A%5Bcount%28%29%5D%22+could+be+improved)]

## count()

```cpp
int count () const noexcept;
```

count the number of bits in the [bitfield](reference-Utility.md#bitfield) that are set to 1.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:bitfield%3A%3A%5Bfind_first_set%28%29%5D&labels=documentation&body=Documentation+under+heading+%22bitfield%3A%3A%5Bfind_first_set%28%29%5D%22+could+be+improved)]

## find\_first\_set()

```cpp
int find_first_set () const noexcept;
```

returns the index of the first set bit in the [bitfield](reference-Utility.md#bitfield), i.e. 1 bit.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:bitfield%3A%3A%5Bfind_last_clear%28%29%5D&labels=documentation&body=Documentation+under+heading+%22bitfield%3A%3A%5Bfind_last_clear%28%29%5D%22+could+be+improved)]

## find\_last\_clear()

```cpp
int find_last_clear () const noexcept;
```

returns the index to the last cleared bit in the [bitfield](reference-Utility.md#bitfield), i.e. 0 bit.
