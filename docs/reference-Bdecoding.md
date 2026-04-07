---
title: "Bdecoding"
source: "https://libtorrent.org/reference-Bdecoding.html"
---

# bdecode\_node

Declared in "[libtorrent/bdecode.hpp](include/libtorrent/bdecode.hpp)"

Sometimes it's important to get a non-owning reference to the root node (
to be able to copy it as a reference for instance). For that, use the
[non\_owning()](reference-Bdecoding.md#non_owning()) member function.

There are 5 different types of nodes, see [type\_t](reference-Torrent_Info.md#type_t).

```cpp
struct bdecode_node
{
   bdecode_node () = default;
   bdecode_node (bdecode_node&&) noexcept;
   bdecode_node& operator= (bdecode_node const&) &;
   bdecode_node (bdecode_node const&);
   bdecode_node& operator= (bdecode_node&&) & = default;
   type_t type () const noexcept;
   explicit operator bool () const noexcept;
   bdecode_node non_owning () const;
   span<char const> data_section () const noexcept;
   std::ptrdiff_t data_offset () const noexcept;
   bdecode_node list_at (int i) const;
   int list_size () const;
   std::int64_t list_int_value_at (int i
      , std::int64_t default_val = 0) const;
   string_view list_string_value_at (int i
      , string_view default_val = string_view()) const;
   bdecode_node dict_find_list (string_view key) const;
   int dict_size () const;
   std::pair<string_view, bdecode_node> dict_at (int i) const;
   bdecode_node dict_find (string_view key) const;
   bdecode_node dict_find_int (string_view key) const;
   std::int64_t dict_find_int_value (string_view key
      , std::int64_t default_val = 0) const;
   std::pair<bdecode_node, bdecode_node> dict_at_node (int i) const;
   string_view dict_find_string_value (string_view key
      , string_view default_value = string_view()) const;
   bdecode_node dict_find_dict (string_view key) const;
   bdecode_node dict_find_string (string_view key) const;
   std::int64_t int_value () const;
   char const* string_ptr () const;
   int string_length () const;
   string_view string_value () const;
   std::ptrdiff_t string_offset () const;
   void clear ();
   void swap (bdecode_node& n);
   void reserve (int tokens);
   void switch_underlying_buffer (char const* buf) noexcept;
   bool has_soft_error (span<char> error) const;

   enum type_t
   {
      none_t,
      dict_t,
      list_t,
      string_t,
      int_t,
   };
};
```

## bdecode\_node()

```cpp
bdecode_node () = default;
```

creates a default constructed node, it will have the type none\_t.

## operator=() bdecode\_node()

```cpp
bdecode_node (bdecode_node&&) noexcept;
bdecode_node& operator= (bdecode_node const&) &;
bdecode_node (bdecode_node const&);
bdecode_node& operator= (bdecode_node&&) & = default;
```

For owning nodes, the copy will create a copy of the tree, but the
underlying buffer remains the same.

## type()

```cpp
type_t type () const noexcept;
```

the type of this node. See [type\_t](reference-Torrent_Info.md#type_t).

## bool()

```cpp
explicit operator bool () const noexcept;
```

returns true if [type()](reference-Plugins.md#type()) != none\_t.

## non\_owning()

```cpp
bdecode_node non_owning () const;
```

return a non-owning reference to this node. This is useful to refer to
the root node without copying it in assignments.

## data\_section() data\_offset()

```cpp
span<char const> data_section () const noexcept;
std::ptrdiff_t data_offset () const noexcept;
```

returns the buffer and length of the section in the original bencoded
buffer where this node is defined. For a dictionary for instance, this
starts with d and ends with e, and has all the content of the
dictionary in between.
the data\_offset() function returns the byte-offset to this node in,
starting from the beginning of the buffer that was parsed.

## list\_string\_value\_at() list\_at() list\_size() list\_int\_value\_at()

```cpp
bdecode_node list_at (int i) const;
int list_size () const;
std::int64_t list_int_value_at (int i
      , std::int64_t default_val = 0) const;
string_view list_string_value_at (int i
      , string_view default_val = string_view()) const;
```

functions with the list\_ prefix operate on lists. These functions are
only valid if type() == list\_t. list\_at() returns the item
in the list at index i. i may not be greater than or equal to the
size of the list. size() returns the size of the list.

## dict\_find\_int\_value() dict\_find\_string() dict\_find() dict\_find\_dict() dict\_at() dict\_size() dict\_find\_list() dict\_find\_string\_value() dict\_at\_node() dict\_find\_int()

```cpp
bdecode_node dict_find_list (string_view key) const;
int dict_size () const;
std::pair<string_view, bdecode_node> dict_at (int i) const;
bdecode_node dict_find (string_view key) const;
bdecode_node dict_find_int (string_view key) const;
std::int64_t dict_find_int_value (string_view key
      , std::int64_t default_val = 0) const;
std::pair<bdecode_node, bdecode_node> dict_at_node (int i) const;
string_view dict_find_string_value (string_view key
      , string_view default_value = string_view()) const;
bdecode_node dict_find_dict (string_view key) const;
bdecode_node dict_find_string (string_view key) const;
```

Functions with the dict\_ prefix operates on dictionaries. They are
only valid if type() == dict\_t. In case a key you're looking up
contains a 0 byte, you cannot use the 0-terminated string overloads,
but have to use string\_view instead. dict\_find\_list will return a
valid bdecode\_node if the key is found \_and\_ it is a list. Otherwise
it will return a default-constructed [bdecode\_node](reference-Bdecoding.md#bdecode_node).

Functions with the \_value suffix return the value of the node
directly, rather than the nodes. In case the node is not found, or it has
a different type, a default value is returned (which can be specified).

dict\_at() returns the (key, value)-pair at the specified index in a
dictionary. Keys are only allowed to be strings. dict\_at\_node() also
returns the (key, value)-pair, but the key is returned as a
bdecode\_node (and it will always be a string).

## int\_value()

```cpp
std::int64_t int_value () const;
```

this function is only valid if type() == int\_t. It returns the
value of the integer.

## string\_value() string\_offset() string\_length() string\_ptr()

```cpp
char const* string_ptr () const;
int string_length () const;
string_view string_value () const;
std::ptrdiff_t string_offset () const;
```

these functions are only valid if type() == string\_t. They return
the string values. Note that string\_ptr() is *not* 0-terminated.
string\_length() returns the number of bytes in the string.
string\_offset() returns the byte offset from the start of the parsed
bencoded buffer this string can be found.

## clear()

```cpp
void clear ();
```

resets the bdecoded\_node to a default constructed state. If this is
an owning node, the tree is freed and all child nodes are invalidated.

## swap()

```cpp
void swap (bdecode_node& n);
```

Swap contents.

## reserve()

```cpp
void reserve (int tokens);
```

preallocate memory for the specified numbers of tokens. This is
useful if you know approximately how many tokens are in the file
you are about to parse. Doing so will save realloc operations
while parsing. You should only call this on the root node, before
passing it in to [bdecode()](reference-Bdecoding.md#bdecode()).

## switch\_underlying\_buffer()

```cpp
void switch_underlying_buffer (char const* buf) noexcept;
```

this buffer *MUST* be identical to the one originally parsed. This
operation is only defined on owning root nodes, i.e. the one passed in to
decode().

## has\_soft\_error()

```cpp
bool has_soft_error (span<char> error) const;
```

returns true if there is a non-fatal error in the bencoding of this node
or its children

## enum type\_t

Declared in "[libtorrent/bdecode.hpp](include/libtorrent/bdecode.hpp)"

| name | value | description |
| --- | --- | --- |
| none\_t | 0 | uninitialized or default constructed. This is also used to indicate that a node was not found in some cases. |
| dict\_t | 1 | a dictionary node. The dict\_find\_ functions are valid. |
| list\_t | 2 | a list node. The list\_ functions are valid. |
| string\_t | 3 | a string node, the string\_ functions are valid. |
| int\_t | 4 | an integer node. The int\_ functions are valid. |

# print\_entry()

Declared in "[libtorrent/bdecode.hpp](include/libtorrent/bdecode.hpp)"

```cpp
std::string print_entry (bdecode_node const& e
   , bool single_line = false, int indent = 0);
```

print the bencoded structure in a human-readable format to a string
that's returned.

# bdecode()

Declared in "[libtorrent/bdecode.hpp](include/libtorrent/bdecode.hpp)"

```cpp
bdecode_node bdecode (span<char const> buffer
   , int depth_limit = 100, int token_limit = 2000000);
int bdecode (char const* start, char const* end, bdecode_node& ret
   , error_code& ec, int* error_pos = nullptr, int depth_limit = 100
   , int token_limit = 2000000);
bdecode_node bdecode (span<char const> buffer
   , error_code& ec, int* error_pos = nullptr, int depth_limit = 100
   , int token_limit = 2000000);
```

This function decodes/parses bdecoded data (for example a .torrent file).
The data structure is returned in the ret argument. the buffer to parse
is specified by the start of the buffer as well as the end, i.e. one
byte past the end. If the buffer fails to parse, the function returns a
non-zero value and fills in ec with the error code. The optional
argument error\_pos, if set to non-nullptr, will be set to the byte offset
into the buffer where the parse failure occurred.

depth\_limit specifies the max number of nested lists or dictionaries are
allowed in the data structure. (This affects the stack usage of the
function, be careful not to set it too high).

token\_limit is the max number of tokens allowed to be parsed from the
buffer. This is simply a sanity check to not have unbounded memory usage.

The resulting bdecode\_node is an *owning* node. That means it will
be holding the whole parsed tree. When iterating lists and dictionaries,
those bdecode\_node objects will simply have references to the root or
owning bdecode\_node. If the root node is destructed, all other nodes
that refer to anything in that tree become invalid.

However, the underlying buffer passed in to this function (start, end)
must also remain valid while the bdecoded tree is used. The parsed tree
produced by this function does not copy any data out of the buffer, but
simply produces references back into it.
