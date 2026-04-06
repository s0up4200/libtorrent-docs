---
title: "web_seed_entry"
source: "https://libtorrent.org/reference-Torrent_Info.html"
---

[home](reference.md)

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:class+web_seed_entry&labels=documentation&body=Documentation+under+heading+%22class+web_seed_entry%22+could+be+improved)]

# web\_seed\_entry

Declared in "[libtorrent/torrent\_info.hpp](include/libtorrent/torrent_info.hpp)"

the [web\_seed\_entry](reference-Torrent_Info.md#web_seed_entry) holds information about a web seed (also known
as URL seed or HTTP seed). It is essentially a URL with some state
associated with it. For more information, see [BEP 17](https://www.bittorrent.org/beps/bep_0017.html) and [BEP 19](https://www.bittorrent.org/beps/bep_0019.html).

```cpp
struct web_seed_entry
{
   bool operator== (web_seed_entry const& e) const;
   bool operator< (web_seed_entry const& e) const;

   enum type_t
   {
      url_seed,
      http_seed,
   };

   std::string url;
   std::string auth;
   headers_t extra_headers;
   std::uint8_t type;
};
```

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:web_seed_entry%3A%3A%5Boperator%3D%3D%28%29%5D&labels=documentation&body=Documentation+under+heading+%22web_seed_entry%3A%3A%5Boperator%3D%3D%28%29%5D%22+could+be+improved)]

## operator==()

```cpp
bool operator== (web_seed_entry const& e) const;
```

URL and type comparison

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:web_seed_entry%3A%3A%5Boperator%3C%28%29%5D&labels=documentation&body=Documentation+under+heading+%22web_seed_entry%3A%3A%5Boperator%3C%28%29%5D%22+could+be+improved)]

## operator<()

```cpp
bool operator< (web_seed_entry const& e) const;
```

URL and type less-than comparison

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:enum+type_t&labels=documentation&body=Documentation+under+heading+%22enum+type_t%22+could+be+improved)]

## enum type\_t

Declared in "[libtorrent/torrent\_info.hpp](include/libtorrent/torrent_info.hpp)"

| name | value | description |
| --- | --- | --- |
| url\_seed | 0 |  |
| http\_seed | 1 |  |

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:web_seed_entry%3A%3A%5Burl%5D&labels=documentation&body=Documentation+under+heading+%22web_seed_entry%3A%3A%5Burl%5D%22+could+be+improved)]

url
:   The URL of the web seed

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:web_seed_entry%3A%3A%5Bauth%5D&labels=documentation&body=Documentation+under+heading+%22web_seed_entry%3A%3A%5Bauth%5D%22+could+be+improved)]

auth
:   Optional authentication. If this is set, it's passed
    in as HTTP basic auth to the web seed. The format is:
    username:password.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:web_seed_entry%3A%3A%5Bextra_headers%5D&labels=documentation&body=Documentation+under+heading+%22web_seed_entry%3A%3A%5Bextra_headers%5D%22+could+be+improved)]

extra\_headers
:   Any extra HTTP headers that need to be passed to the web seed

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:web_seed_entry%3A%3A%5Btype%5D&labels=documentation&body=Documentation+under+heading+%22web_seed_entry%3A%3A%5Btype%5D%22+could+be+improved)]

type
:   The type of web seed (see [type\_t](reference-Torrent_Info.md#type_t))

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:class+load_torrent_limits&labels=documentation&body=Documentation+under+heading+%22class+load_torrent_limits%22+could+be+improved)]

# load\_torrent\_limits

Declared in "[libtorrent/torrent\_info.hpp](include/libtorrent/torrent_info.hpp)"

this object holds configuration options for limits to use when loading
torrents. They are meant to prevent loading potentially malicious torrents
that cause excessive memory allocations.

```cpp
struct load_torrent_limits
{
   int max_buffer_size  = 10000000;
   int max_pieces  = 0x200000;
   int max_decode_depth  = 100;
   int max_decode_tokens  = 3000000;
};
```

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:load_torrent_limits%3A%3A%5Bmax_buffer_size%5D&labels=documentation&body=Documentation+under+heading+%22load_torrent_limits%3A%3A%5Bmax_buffer_size%5D%22+could+be+improved)]

max\_buffer\_size
:   the max size of a .torrent file to load into RAM

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:load_torrent_limits%3A%3A%5Bmax_pieces%5D&labels=documentation&body=Documentation+under+heading+%22load_torrent_limits%3A%3A%5Bmax_pieces%5D%22+could+be+improved)]

max\_pieces
:   the max number of pieces allowed in the torrent

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:load_torrent_limits%3A%3A%5Bmax_decode_depth%5D&labels=documentation&body=Documentation+under+heading+%22load_torrent_limits%3A%3A%5Bmax_decode_depth%5D%22+could+be+improved)]

max\_decode\_depth
:   the max recursion depth in the bdecoded structure

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:load_torrent_limits%3A%3A%5Bmax_decode_tokens%5D&labels=documentation&body=Documentation+under+heading+%22load_torrent_limits%3A%3A%5Bmax_decode_tokens%5D%22+could+be+improved)]

max\_decode\_tokens
:   the max number of bdecode tokens

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:class+torrent_info&labels=documentation&body=Documentation+under+heading+%22class+torrent_info%22+could+be+improved)]

# torrent\_info

Declared in "[libtorrent/torrent\_info.hpp](include/libtorrent/torrent_info.hpp)"

the [torrent\_info](reference-Torrent_Info.md#torrent_info) class holds the information found in a .torrent file.

```cpp
class torrent_info
{
   torrent_info (span<char const> buffer, load_torrent_limits const& cfg, from_span_t);
   explicit torrent_info (info_hash_t const& info_hash);
   explicit torrent_info (std::string const& filename);
   explicit torrent_info (span<char const> buffer, from_span_t);
   torrent_info (char const* buffer, int size, error_code& ec);
   torrent_info (bdecode_node const& torrent_file, load_torrent_limits const& cfg);
   torrent_info (torrent_info const& t);
   torrent_info (char const* buffer, int size);
   torrent_info (span<char const> buffer, error_code& ec, from_span_t);
   explicit torrent_info (bdecode_node const& torrent_file);
   torrent_info (bdecode_node const& torrent_file, error_code& ec);
   torrent_info (std::string const& filename, error_code& ec);
   torrent_info (std::string const& filename, load_torrent_limits const& cfg);
   ~torrent_info ();
   file_storage const& orig_files () const;
   file_storage const& files () const;
   void rename_file (file_index_t index, std::string const& new_filename);
   void remap_files (file_storage const& f);
   void clear_trackers ();
   void add_tracker (std::string const& url, int tier
      , announce_entry::tracker_source source);
   std::vector<announce_entry> const& trackers () const;
   void add_tracker (std::string const& url, int tier = 0);
   std::vector<sha1_hash> similar_torrents () const;
   std::vector<std::string> collections () const;
   void set_web_seeds (std::vector<web_seed_entry> seeds);
   void add_http_seed (std::string const& url
      , std::string const& extern_auth = std::string()
      , web_seed_entry::headers_t const& extra_headers = web_seed_entry::headers_t());
   std::vector<web_seed_entry> const& web_seeds () const;
   void add_url_seed (std::string const& url
      , std::string const& ext_auth = std::string()
      , web_seed_entry::headers_t const& ext_headers = web_seed_entry::headers_t());
   std::int64_t total_size () const;
   int num_pieces () const;
   int piece_length () const;
   int blocks_per_piece () const;
   index_range<piece_index_t> piece_range () const;
   piece_index_t end_piece () const;
   piece_index_t last_piece () const;
   info_hash_t const& info_hashes () const;
   sha1_hash info_hash () const noexcept;
   bool v2 () const;
   bool v1 () const;
   int num_files () const;
   std::vector<file_slice> map_block (piece_index_t const piece
      , std::int64_t offset, int size) const;
   peer_request map_file (file_index_t const file, std::int64_t offset, int size) const;
   string_view ssl_cert () const;
   bool is_valid () const;
   bool priv () const;
   bool is_i2p () const;
   int piece_size (piece_index_t index) const;
   sha1_hash hash_for_piece (piece_index_t index) const;
   char const* hash_for_piece_ptr (piece_index_t const index) const;
   bool is_loaded () const;
   const std::string& name () const;
   std::time_t creation_date () const;
   const std::string& creator () const;
   const std::string& comment () const;
   std::vector<std::pair<std::string, int>> const& nodes () const;
   void add_node (std::pair<std::string, int> const& node);
   bool parse_info_section (bdecode_node const& info, error_code& ec, int max_pieces);
   bdecode_node info (char const* key) const;
   span<char const> info_section () const;
   span<char const> piece_layer (file_index_t) const;
   void free_piece_layers ();
};
```

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Btorrent_info%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Btorrent_info%28%29%5D%22+could+be+improved)]

## torrent\_info()

```cpp
torrent_info (span<char const> buffer, load_torrent_limits const& cfg, from_span_t);
explicit torrent_info (info_hash_t const& info_hash);
explicit torrent_info (std::string const& filename);
explicit torrent_info (span<char const> buffer, from_span_t);
torrent_info (char const* buffer, int size, error_code& ec);
torrent_info (bdecode_node const& torrent_file, load_torrent_limits const& cfg);
torrent_info (torrent_info const& t);
torrent_info (char const* buffer, int size);
torrent_info (span<char const> buffer, error_code& ec, from_span_t);
explicit torrent_info (bdecode_node const& torrent_file);
torrent_info (bdecode_node const& torrent_file, error_code& ec);
torrent_info (std::string const& filename, error_code& ec);
torrent_info (std::string const& filename, load_torrent_limits const& cfg);
```

The constructor that takes an info-hash will initialize the info-hash
to the given value, but leave all other fields empty. This is used
internally when downloading torrents without the metadata. The
metadata will be created by libtorrent as soon as it has been
downloaded from the swarm.

The constructor that takes a [bdecode\_node](reference-Bdecoding.md#bdecode_node) will create a [torrent\_info](reference-Torrent_Info.md#torrent_info)
object from the information found in the given torrent\_file. The
[bdecode\_node](reference-Bdecoding.md#bdecode_node) represents a tree node in an bencoded file. To load an
ordinary .torrent file into a [bdecode\_node](reference-Bdecoding.md#bdecode_node), use [bdecode()](reference-Bdecoding.md#bdecode()).

The version that takes a buffer pointer and a size will decode it as a
.torrent file and initialize the [torrent\_info](reference-Torrent_Info.md#torrent_info) object for you.

The version that takes a filename will simply load the torrent file
and decode it inside the constructor, for convenience. This might not
be the most suitable for applications that want to be able to report
detailed errors on what might go wrong.

There is an upper limit on the size of the torrent file that will be
loaded by the overload taking a filename. If it's important that even
very large torrent files are loaded, use one of the other overloads.

The overloads that takes an error\_code const& never throws if an
error occur, they will simply set the error code to describe what went
wrong and not fully initialize the [torrent\_info](reference-Torrent_Info.md#torrent_info) object. The overloads
that do not take the extra error\_code parameter will always throw if
an error occurs. These overloads are not available when building
without exception support.

The overload that takes a span also needs an extra parameter of
type from\_span\_t to disambiguate the std::string overload for
string literals. There is an object in the libtorrent namespace of this
type called from\_span.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5B~torrent_info%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5B~torrent_info%28%29%5D%22+could+be+improved)]

## ~torrent\_info()

```cpp
~torrent_info ();
```

frees all storage associated with this [torrent\_info](reference-Torrent_Info.md#torrent_info) object

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Borig_files%28%29+files%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Borig_files%28%29+files%28%29%5D%22+could+be+improved)]

## orig\_files() files()

```cpp
file_storage const& orig_files () const;
file_storage const& files () const;
```

The [file\_storage](reference-Storage.md#file_storage) object contains the information on how to map the
pieces to files. It is separated from the [torrent\_info](reference-Torrent_Info.md#torrent_info) object because
when creating torrents a storage object needs to be created without
having a torrent file. When renaming files in a storage, the storage
needs to make its own copy of the [file\_storage](reference-Storage.md#file_storage) in order to make its
mapping differ from the one in the torrent file.

orig\_files() returns the original (unmodified) file storage for
this torrent. This is used by the web server connection, which needs
to request files with the original names. Filename may be changed using
torrent\_info::rename\_file().

For more information on the [file\_storage](reference-Storage.md#file_storage) object, see the separate
document on how to create torrents.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Brename_file%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Brename_file%28%29%5D%22+could+be+improved)]

## rename\_file()

```cpp
void rename_file (file_index_t index, std::string const& new_filename);
```

Renames the file with the specified index to the new name. The new
filename is reflected by the file\_storage returned by files()
but not by the one returned by orig\_files().

If you want to rename the base name of the torrent (for a multi file
torrent), you can copy the file\_storage (see [files()](reference-Torrent_Info.md#files()) and
[orig\_files()](reference-Torrent_Info.md#orig_files()) ), change the name, and then use [remap\_files()](#remap-files).

The new\_filename can both be a relative path, in which case the
file name is relative to the save\_path of the torrent. If the
new\_filename is an absolute path (i.e. is\_complete(new\_filename)
== true), then the file is detached from the save\_path of the
torrent. In this case the file is not moved when [move\_storage()](reference-Torrent_Handle.md#move_storage()) is
invoked.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Bremap_files%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Bremap_files%28%29%5D%22+could+be+improved)]

## remap\_files()

```cpp
void remap_files (file_storage const& f);
```

Warning

Using remap\_files() is discouraged as it's incompatible with v2
torrents. This is because the piece boundaries and piece hashes in
v2 torrents are intimately tied to the file boundaries. Instead,
just rename individual files, or implement a custom [disk\_interface](reference-Custom_Storage.md#disk_interface)
to customize how to store files.

Remaps the file storage to a new file layout. This can be used to, for
instance, download all data in a torrent to a single file, or to a
number of fixed size sector aligned files, regardless of the number
and sizes of the files in the torrent.

The new specified file\_storage must have the exact same size as
the current one.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Badd_tracker%28%29+clear_trackers%28%29+trackers%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Badd_tracker%28%29+clear_trackers%28%29+trackers%28%29%5D%22+could+be+improved)]

## add\_tracker() clear\_trackers() trackers()

```cpp
void clear_trackers ();
void add_tracker (std::string const& url, int tier
      , announce_entry::tracker_source source);
std::vector<announce_entry> const& trackers () const;
void add_tracker (std::string const& url, int tier = 0);
```

add\_tracker() adds a tracker to the announce-list. The tier
determines the order in which the trackers are to be tried.
The trackers() function will return a sorted vector of
[announce\_entry](reference-Trackers.md#announce_entry). Each announce [entry](reference-Bencoding.md#entry) contains a string, which is
the tracker url, and a tier index. The tier index is the high-level
priority. No matter which trackers that works or not, the ones with
lower tier will always be tried before the one with higher tier
number. For more information, see [announce\_entry](reference-Trackers.md#announce_entry).

trackers() returns all entries from announce-list.

clear\_trackers() removes all trackers from announce-list.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Bsimilar_torrents%28%29+collections%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Bsimilar_torrents%28%29+collections%28%29%5D%22+could+be+improved)]

## similar\_torrents() collections()

```cpp
std::vector<sha1_hash> similar_torrents () const;
std::vector<std::string> collections () const;
```

These two functions are related to [BEP 38](https://www.bittorrent.org/beps/bep_0038.html) (mutable torrents). The
vectors returned from these correspond to the "similar" and
"collections" keys in the .torrent file. Both info-hashes and
collections from within the info-dict and from outside of it are
included.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Badd_http_seed%28%29+add_url_seed%28%29+set_web_seeds%28%29+web_seeds%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Badd_http_seed%28%29+add_url_seed%28%29+set_web_seeds%28%29+web_seeds%28%29%5D%22+could+be+improved)]

## add\_http\_seed() add\_url\_seed() set\_web\_seeds() web\_seeds()

```cpp
void set_web_seeds (std::vector<web_seed_entry> seeds);
void add_http_seed (std::string const& url
      , std::string const& extern_auth = std::string()
      , web_seed_entry::headers_t const& extra_headers = web_seed_entry::headers_t());
std::vector<web_seed_entry> const& web_seeds () const;
void add_url_seed (std::string const& url
      , std::string const& ext_auth = std::string()
      , web_seed_entry::headers_t const& ext_headers = web_seed_entry::headers_t());
```

web\_seeds() returns all url seeds and http seeds in the torrent.
Each [entry](reference-Bencoding.md#entry) is a web\_seed\_entry and may refer to either a url seed
or http seed.

add\_url\_seed() and add\_http\_seed() adds one url to the list of
url/http seeds.

set\_web\_seeds() replaces all web seeds with the ones specified in
the seeds vector.

The extern\_auth argument can be used for other authorization
schemes than basic HTTP authorization. If set, it will override any
username and password found in the URL itself. The string will be sent
as the HTTP authorization header's value (without specifying "Basic").

The extra\_headers argument defaults to an empty list, but can be
used to insert custom HTTP headers in the requests to a specific web
seed.

See [http seeding](manual-ref.md#http-seeding) for more information.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Btotal_size%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Btotal_size%28%29%5D%22+could+be+improved)]

## total\_size()

```cpp
std::int64_t total_size () const;
```

total\_size() returns the total number of bytes the torrent-file
represents. Note that this is the number of pieces times the piece
size (modulo the last piece possibly being smaller). With pad files,
the total size will be larger than the sum of all (regular) file
sizes.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Bpiece_length%28%29+num_pieces%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Bpiece_length%28%29+num_pieces%28%29%5D%22+could+be+improved)]

## piece\_length() num\_pieces()

```cpp
int num_pieces () const;
int piece_length () const;
```

piece\_length() and num\_pieces() returns the number of byte
for each piece and the total number of pieces, respectively. The
difference between piece\_size() and piece\_length() is that
piece\_size() takes the piece index as argument and gives you the
exact size of that piece. It will always be the same as
piece\_length() except in the case of the last piece, which may be
smaller.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Bblocks_per_piece%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Bblocks_per_piece%28%29%5D%22+could+be+improved)]

## blocks\_per\_piece()

```cpp
int blocks_per_piece () const;
```

returns the number of blocks there are in the typical piece. There
may be fewer in the last piece)

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Blast_piece%28%29+piece_range%28%29+end_piece%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Blast_piece%28%29+piece_range%28%29+end_piece%28%29%5D%22+could+be+improved)]

## last\_piece() piece\_range() end\_piece()

```cpp
index_range<piece_index_t> piece_range () const;
piece_index_t end_piece () const;
piece_index_t last_piece () const;
```

last\_piece() returns the index to the last piece in the torrent and
end\_piece() returns the index to the one-past-end piece in the
torrent
piece\_range() returns an implementation-defined type that can be
used as the container in a range-for loop. Where the values are the
indices of all pieces in the [file\_storage](reference-Storage.md#file_storage).

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Binfo_hashes%28%29+info_hash%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Binfo_hashes%28%29+info_hash%28%29%5D%22+could+be+improved)]

## info\_hashes() info\_hash()

```cpp
info_hash_t const& info_hashes () const;
sha1_hash info_hash () const noexcept;
```

returns the info-hash of the torrent. For BitTorrent v2 support, use
info\_hashes() to get an object that may hold both a v1 and v2
info-hash

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Bv2%28%29+v1%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Bv2%28%29+v1%28%29%5D%22+could+be+improved)]

## v2() v1()

```cpp
bool v2 () const;
bool v1 () const;
```

returns whether this torrent has v1 and/or v2 metadata, respectively.
Hybrid torrents have both. These are shortcuts for
info\_hashes().has\_v1() and info\_hashes().has\_v2() calls.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Bnum_files%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Bnum_files%28%29%5D%22+could+be+improved)]

## num\_files()

```cpp
int num_files () const;
```

If you need index-access to files you can use the num\_files() along
with the file\_path(), file\_size()-family of functions to access
files using indices.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Bmap_block%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Bmap_block%28%29%5D%22+could+be+improved)]

## map\_block()

```cpp
std::vector<file_slice> map_block (piece_index_t const piece
      , std::int64_t offset, int size) const;
```

This function will map a piece index, a byte offset within that piece
and a size (in bytes) into the corresponding files with offsets where
that data for that piece is supposed to be stored. See [file\_slice](reference-Storage.md#file_slice).

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Bmap_file%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Bmap_file%28%29%5D%22+could+be+improved)]

## map\_file()

```cpp
peer_request map_file (file_index_t const file, std::int64_t offset, int size) const;
```

This function will map a range in a specific file into a range in the
torrent. The file\_offset parameter is the offset in the file,
given in bytes, where 0 is the start of the file. See [peer\_request](reference-Core.md#peer_request).

The input range is assumed to be valid within the torrent.
file\_offset + size is not allowed to be greater than the file
size. file\_index must refer to a valid file, i.e. it cannot be >=
num\_files().

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Bssl_cert%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Bssl_cert%28%29%5D%22+could+be+improved)]

## ssl\_cert()

```cpp
string_view ssl_cert () const;
```

Returns the SSL root certificate for the torrent, if it is an SSL
torrent. Otherwise returns an empty string. The certificate is
the public certificate in x509 format.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Bis_valid%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Bis_valid%28%29%5D%22+could+be+improved)]

## is\_valid()

```cpp
bool is_valid () const;
```

returns true if this [torrent\_info](reference-Torrent_Info.md#torrent_info) object has a torrent loaded.
This is primarily used to determine if a magnet link has had its
metadata resolved yet or not.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Bpriv%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Bpriv%28%29%5D%22+could+be+improved)]

## priv()

```cpp
bool priv () const;
```

returns true if this torrent is private. i.e., the client should not
advertise itself on the trackerless network (the Kademlia DHT) for this torrent.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Bis_i2p%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Bis_i2p%28%29%5D%22+could+be+improved)]

## is\_i2p()

```cpp
bool is_i2p () const;
```

returns true if this is an i2p torrent. This is determined by whether
or not it has a tracker whose URL domain name ends with ".i2p". i2p
torrents disable the DHT and local peer discovery as well as talking
to peers over anything other than the i2p network.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Bpiece_size%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Bpiece_size%28%29%5D%22+could+be+improved)]

## piece\_size()

```cpp
int piece_size (piece_index_t index) const;
```

returns the piece size of file with index. This will be the same as [piece\_length()](reference-Torrent_Info.md#piece_length()),
except for the last piece, which may be shorter.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Bhash_for_piece_ptr%28%29+hash_for_piece%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Bhash_for_piece_ptr%28%29+hash_for_piece%28%29%5D%22+could+be+improved)]

## hash\_for\_piece\_ptr() hash\_for\_piece()

```cpp
sha1_hash hash_for_piece (piece_index_t index) const;
char const* hash_for_piece_ptr (piece_index_t const index) const;
```

hash\_for\_piece() takes a piece-index and returns the 20-bytes
sha1-hash for that piece and info\_hash() returns the 20-bytes
sha1-hash for the info-section of the torrent file.
hash\_for\_piece\_ptr() returns a pointer to the 20 byte sha1 digest
for the piece. Note that the string is not 0-terminated.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Bname%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Bname%28%29%5D%22+could+be+improved)]

## name()

```cpp
const std::string& name () const;
```

name() returns the name of the torrent.
name contains UTF-8 encoded string.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Bcreation_date%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Bcreation_date%28%29%5D%22+could+be+improved)]

## creation\_date()

```cpp
std::time_t creation_date () const;
```

creation\_date() returns the creation date of the torrent as time\_t
([posix time](#posix-time)). If there's no time stamp in the torrent file, 0 is
returned.
.. posix time: <http://www.opengroup.org/onlinepubs/009695399/functions/time.html>

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Bcreator%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Bcreator%28%29%5D%22+could+be+improved)]

## creator()

```cpp
const std::string& creator () const;
```

creator() returns the creator string in the torrent. If there is
no creator string it will return an empty string.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Bcomment%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Bcomment%28%29%5D%22+could+be+improved)]

## comment()

```cpp
const std::string& comment () const;
```

comment() returns the comment associated with the torrent. If
there's no comment, it will return an empty string.
comment contains UTF-8 encoded string.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Bnodes%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Bnodes%28%29%5D%22+could+be+improved)]

## nodes()

```cpp
std::vector<std::pair<std::string, int>> const& nodes () const;
```

If this torrent contains any DHT nodes, they are put in this vector in
their original form (host name and port number).

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Badd_node%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Badd_node%28%29%5D%22+could+be+improved)]

## add\_node()

```cpp
void add_node (std::pair<std::string, int> const& node);
```

This is used when creating torrent. Use this to add a known DHT node.
It may be used, by the client, to bootstrap into the DHT network.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Bparse_info_section%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Bparse_info_section%28%29%5D%22+could+be+improved)]

## parse\_info\_section()

```cpp
bool parse_info_section (bdecode_node const& info, error_code& ec, int max_pieces);
```

populates the [torrent\_info](reference-Torrent_Info.md#torrent_info) by providing just the info-dict buffer.
This is used when loading a torrent from a magnet link for instance,
where we only have the info-dict. The [bdecode\_node](reference-Bdecoding.md#bdecode_node) e points to a
parsed info-dictionary. ec returns an error code if something
fails (typically if the info dictionary is malformed).
The max\_pieces parameter allows limiting the amount of memory
dedicated to loading the torrent, and fails for torrents that exceed
the limit. To load large torrents, this limit may also need to be
raised in [settings\_pack::max\_piece\_count](reference-Settings.md#max_piece_count) and in calls to
[read\_resume\_data()](reference-Resume_Data.md#read_resume_data()).

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Binfo%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Binfo%28%29%5D%22+could+be+improved)]

## info()

```cpp
bdecode_node info (char const* key) const;
```

This function looks up keys from the info-dictionary of the loaded
torrent file. It can be used to access extension values put in the
.torrent file. If the specified key cannot be found, it returns nullptr.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Binfo_section%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Binfo_section%28%29%5D%22+could+be+improved)]

## info\_section()

```cpp
span<char const> info_section () const;
```

returns a the raw info section of the torrent file.
The underlying buffer is still owned by the [torrent\_info](reference-Torrent_Info.md#torrent_info) object

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Bpiece_layer%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Bpiece_layer%28%29%5D%22+could+be+improved)]

## piece\_layer()

```cpp
span<char const> piece_layer (file_index_t) const;
```

return the bytes of the piece layer hashes for the specified file. If
the file doesn't have a piece layer, an empty span is returned.
The span size is divisible by 32, the size of a SHA-256 hash.
If the size of the file is smaller than or equal to the piece size,
the files "root hash" is the hash of the file and is not saved
separately in the "piece layers" field, but this function still
returns the root hash of the file in that case.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:torrent_info%3A%3A%5Bfree_piece_layers%28%29%5D&labels=documentation&body=Documentation+under+heading+%22torrent_info%3A%3A%5Bfree_piece_layers%28%29%5D%22+could+be+improved)]

## free\_piece\_layers()

```cpp
void free_piece_layers ();
```

clears the piece layers from the [torrent\_info](reference-Torrent_Info.md#torrent_info). This is done by the
[session](reference-Session.md#session) when a torrent is added, to avoid storing it twice. The piece
layer (or other hashes part of the merkle tree) are stored in the
internal torrent object.
