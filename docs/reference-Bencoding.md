---
title: "entry"
source: "https://libtorrent.org/reference-Bencoding.html"
---

[home](reference.md)

Bencoding is a common representation in bittorrent used for dictionary,
list, [int](reference-Core.md#int) and string hierarchies. It's used to encode .torrent files and
some messages in the network protocol. libtorrent also uses it to store
settings, resume data and other [session](reference-Session.md#session) state.

Strings in bencoded structures do not necessarily represent text.
Strings are raw byte buffers of a certain length. If a string is meant to be
interpreted as text, it is required to be UTF-8 encoded. See [BEP 3](https://www.bittorrent.org/beps/bep_0003.html).

The function for decoding bencoded data [bdecode()](reference-Bdecoding.md#bdecode()), returning a [bdecode\_node](reference-Bdecoding.md#bdecode_node).
This function builds a tree that points back into the original buffer. The
returned [bdecode\_node](reference-Bdecoding.md#bdecode_node) will not be valid once the buffer it was parsed out of
is discarded.

It's possible to construct an [entry](reference-Bencoding.md#entry) from a [bdecode\_node](reference-Bdecoding.md#bdecode_node), if a structure needs
to be altered and re-encoded.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:class+entry&labels=documentation&body=Documentation+under+heading+%22class+entry%22+could+be+improved)]

# entry

Declared in "[libtorrent/entry.hpp](include/libtorrent/entry.hpp)"

The entry class represents one node in a bencoded hierarchy. It works as a
variant type, it can be either a list, a dictionary (std::map), an integer
or a string.

```cpp
class entry
{
   data_type type () const;
   entry (list_type);
   entry (preformatted_type);
   entry (integer_type);
   entry (dictionary_type);
   entry (span<char const>);
   entry (U v);
   entry (data_type t);
   entry (bdecode_node const& n);
   entry& operator= (dictionary_type) &;
   entry& operator= (entry const&) &;
   entry& operator= (bdecode_node const&) &;
   entry& operator= (integer_type) &;
   entry& operator= (preformatted_type) &;
   entry& operator= (entry&&) & noexcept;
   entry& operator= (list_type) &;
   entry& operator= (span<char const>) &;
   entry& operator= (U v) &;
   integer_type& integer ();
   list_type const& list () const;
   list_type& list ();
   string_type const& string () const;
   integer_type const& integer () const;
   string_type& string ();
   dictionary_type& dict ();
   preformatted_type const& preformatted () const;
   dictionary_type const& dict () const;
   preformatted_type& preformatted ();
   void swap (entry& e);
   entry const& operator[] (string_view key) const;
   entry& operator[] (string_view key);
   entry const* find_key (string_view key) const;
   entry* find_key (string_view key);
   std::string to_string (bool single_line = false) const;

   enum data_type
   {
      int_t,
      string_t,
      list_t,
      dictionary_t,
      undefined_t,
      preformatted_t,
   };
};
```

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:entry%3A%3A%5Btype%28%29%5D&labels=documentation&body=Documentation+under+heading+%22entry%3A%3A%5Btype%28%29%5D%22+could+be+improved)]

## type()

```cpp
data_type type () const;
```

returns the concrete type of the [entry](reference-Bencoding.md#entry)

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:entry%3A%3A%5Bentry%28%29%5D&labels=documentation&body=Documentation+under+heading+%22entry%3A%3A%5Bentry%28%29%5D%22+could+be+improved)]

## entry()

```cpp
entry (list_type);
entry (preformatted_type);
entry (integer_type);
entry (dictionary_type);
entry (span<char const>);
```

constructors directly from a specific type.
The content of the argument is copied into the
newly constructed [entry](reference-Bencoding.md#entry)

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:entry%3A%3A%5Bentry%28%29%5D&labels=documentation&body=Documentation+under+heading+%22entry%3A%3A%5Bentry%28%29%5D%22+could+be+improved)]

## entry()

```cpp
entry (data_type t);
```

construct an empty [entry](reference-Bencoding.md#entry) of the specified type.
see [data\_type](reference-Bencoding.md#data_type) enum.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:entry%3A%3A%5Bentry%28%29%5D&labels=documentation&body=Documentation+under+heading+%22entry%3A%3A%5Bentry%28%29%5D%22+could+be+improved)]

## entry()

```cpp
entry (bdecode_node const& n);
```

construct from [bdecode\_node](reference-Bdecoding.md#bdecode_node) parsed form (see [bdecode()](reference-Bdecoding.md#bdecode()))

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:entry%3A%3A%5Boperator%3D%28%29%5D&labels=documentation&body=Documentation+under+heading+%22entry%3A%3A%5Boperator%3D%28%29%5D%22+could+be+improved)]

## operator=()

```cpp
entry& operator= (dictionary_type) &;
entry& operator= (entry const&) &;
entry& operator= (bdecode_node const&) &;
entry& operator= (integer_type) &;
entry& operator= (preformatted_type) &;
entry& operator= (entry&&) & noexcept;
entry& operator= (list_type) &;
entry& operator= (span<char const>) &;
```

copies the structure of the right hand side into this
[entry](reference-Bencoding.md#entry).

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:entry%3A%3A%5Bstring%28%29+integer%28%29+dict%28%29+list%28%29+preformatted%28%29%5D&labels=documentation&body=Documentation+under+heading+%22entry%3A%3A%5Bstring%28%29+integer%28%29+dict%28%29+list%28%29+preformatted%28%29%5D%22+could+be+improved)]

## string() integer() dict() list() preformatted()

```cpp
integer_type& integer ();
list_type const& list () const;
list_type& list ();
string_type const& string () const;
integer_type const& integer () const;
string_type& string ();
dictionary_type& dict ();
preformatted_type const& preformatted () const;
dictionary_type const& dict () const;
preformatted_type& preformatted ();
```

The integer(), string(), list() and dict() functions
are accessors that return the respective type. If the entry object
isn't of the type you request, the accessor will throw
system\_error. You can ask an entry for its type through the
type() function.

If you want to create an entry you give it the type you want it to
have in its constructor, and then use one of the non-const accessors
to get a reference which you then can assign the value you want it to
have.

The typical code to get info from a torrent file will then look like
this:

```cpp
entry torrent_file;
// ...

// throws if this is not a dictionary
entry::dictionary_type const& dict = torrent_file.dict();
entry::dictionary_type::const_iterator i;
i = dict.find("announce");
if (i != dict.end())
{
        std::string tracker_url = i->second.string();
        std::cout << tracker_url << "\n";
}
```

The following code is equivalent, but a little bit shorter:

```cpp
entry torrent_file;
// ...

// throws if this is not a dictionary
if (entry* i = torrent_file.find_key("announce"))
{
        std::string tracker_url = i->string();
        std::cout << tracker_url << "\n";
}
```

To make it easier to extract information from a torrent file, the
class [torrent\_info](reference-Torrent_Info.md#torrent_info) exists.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:entry%3A%3A%5Bswap%28%29%5D&labels=documentation&body=Documentation+under+heading+%22entry%3A%3A%5Bswap%28%29%5D%22+could+be+improved)]

## swap()

```cpp
void swap (entry& e);
```

swaps the content of *this* with e.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:entry%3A%3A%5Boperator%5B%5D%28%29%5D&labels=documentation&body=Documentation+under+heading+%22entry%3A%3A%5Boperator%5B%5D%28%29%5D%22+could+be+improved)]

## operator[]()

```cpp
entry const& operator[] (string_view key) const;
entry& operator[] (string_view key);
```

All of these functions requires the [entry](reference-Bencoding.md#entry) to be a dictionary, if it
isn't they will throw system\_error.

The non-const versions of the operator[] will return a reference
to either the existing element at the given key or, if there is no
element with the given key, a reference to a newly inserted element at
that key.

The const version of operator[] will only return a reference to an
existing element at the given key. If the key is not found, it will
throw system\_error.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:entry%3A%3A%5Bfind_key%28%29%5D&labels=documentation&body=Documentation+under+heading+%22entry%3A%3A%5Bfind_key%28%29%5D%22+could+be+improved)]

## find\_key()

```cpp
entry const* find_key (string_view key) const;
entry* find_key (string_view key);
```

These functions requires the [entry](reference-Bencoding.md#entry) to be a dictionary, if it isn't
they will throw system\_error.

They will look for an element at the given key in the dictionary, if
the element cannot be found, they will return nullptr. If an element
with the given key is found, the return a pointer to it.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:entry%3A%3A%5Bto_string%28%29%5D&labels=documentation&body=Documentation+under+heading+%22entry%3A%3A%5Bto_string%28%29%5D%22+could+be+improved)]

## to\_string()

```cpp
std::string to_string (bool single_line = false) const;
```

returns a pretty-printed string representation
of the bencoded structure, with JSON-style syntax

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:enum+data_type&labels=documentation&body=Documentation+under+heading+%22enum+data_type%22+could+be+improved)]

## enum data\_type

Declared in "[libtorrent/entry.hpp](include/libtorrent/entry.hpp)"

| name | value | description |
| --- | --- | --- |
| int\_t | 0 |  |
| string\_t | 1 |  |
| list\_t | 2 |  |
| dictionary\_t | 3 |  |
| undefined\_t | 4 |  |
| preformatted\_t | 5 |  |

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:operator%3C%3C%28%29&labels=documentation&body=Documentation+under+heading+%22operator%3C%3C%28%29%22+could+be+improved)]

# operator<<()

Declared in "[libtorrent/entry.hpp](include/libtorrent/entry.hpp)"

```cpp
inline std::ostream& operator<< (std::ostream& os, const entry& e);
```

prints the bencoded structure to the ostream as a JSON-style structure.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:bencode%28%29&labels=documentation&body=Documentation+under+heading+%22bencode%28%29%22+could+be+improved)]

# bencode()

Declared in "[libtorrent/bencode.hpp](include/libtorrent/bencode.hpp)"

```cpp
template<class OutIt> int bencode (OutIt out, const entry& e);
```

This function will encode data to bencoded form.

The [entry](#entry) class is the internal representation of the bencoded data
and it can be used to retrieve information, an [entry](#entry) can also be build by
the program and given to bencode() to encode it into the OutIt
iterator.

OutIt is an [OutputIterator](https://en.cppreference.com/w/cpp/named_req/OutputIterator). It's a template and usually
instantiated as [ostream\_iterator](https://en.cppreference.com/w/cpp/iterator/ostream_iterator) or [back\_insert\_iterator](https://en.cppreference.com/w/cpp/iterator/back_insert_iterator). This
function assumes the value\_type of the iterator is a char.
In order to encode [entry](reference-Bencoding.md#entry) e into a buffer, do:

```cpp
std::vector<char> buf;
bencode(std::back_inserter(buf), e);
```
