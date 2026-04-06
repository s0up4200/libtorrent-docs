---
title: "create_torrent"
source: "https://libtorrent.org/reference-Create_Torrents.html"
---

[home](reference.md)

This section describes the functions and classes that are used
to create torrent files. It is a layered API with low level classes
and higher level convenience functions. A torrent is created in 4
steps:

1. first the files that will be part of the torrent are determined.
2. the torrent properties are set, such as tracker url, web seeds,
   DHT nodes etc.
3. Read through all the files in the torrent, SHA-1 all the data
   and set the piece hashes.
4. The torrent is bencoded into a file or buffer.

If there are a lot of files and or deep directory hierarchies to
traverse, step one can be time consuming.

Typically step 3 is by far the most time consuming step, since it
requires to read all the bytes from all the files in the torrent.

All of these classes and functions are declared by including
libtorrent/create\_torrent.hpp.

example:

```cpp
file_storage fs;

// recursively adds files in directories
add_files(fs, "./my_torrent");

create_torrent t(fs);
t.add_tracker("http://my.tracker.com/announce");
t.set_creator("libtorrent example");

// reads the files and calculates the hashes
set_piece_hashes(t, ".");

ofstream out("my_torrent.torrent", std::ios_base::binary);
std::vector<char> buf = t.generate_buf();
out.write(buf.data(), buf.size());

// alternatively, generate an entry and encode it directly to an ostream
// iterator
bencode(std::ostream_iterator<char>(out), t.generate());
```

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:class+create_torrent&labels=documentation&body=Documentation+under+heading+%22class+create_torrent%22+could+be+improved)]

# create\_torrent

Declared in "[libtorrent/create\_torrent.hpp](include/libtorrent/create_torrent.hpp)"

This class holds state for creating a torrent. After having added
all information to it, call [create\_torrent::generate()](reference-Create_Torrents.md#generate()) to generate
the torrent. The [entry](reference-Bencoding.md#entry) that's returned can then be bencoded into a
.torrent file using [bencode()](reference-Bencoding.md#bencode()).

```cpp
struct create_torrent
{
   explicit create_torrent (file_storage& fs, int piece_size = 0
      , create_flags_t flags = {});
   explicit create_torrent (torrent_info const& ti);
   entry generate () const;
   std::vector<char> generate_buf () const;
   file_storage const& files () const;
   void set_comment (char const* str);
   void set_creator (char const* str);
   void set_creation_date (std::time_t timestamp);
   void set_hash (piece_index_t index, sha1_hash const& h);
   void set_hash2 (file_index_t file, piece_index_t::diff_type piece, sha256_hash const& h);
   void add_url_seed (string_view url);
   void add_http_seed (string_view url);
   void add_node (std::pair<std::string, int> node);
   void add_tracker (string_view url, int tier = 0);
   void set_root_cert (string_view cert);
   bool priv () const;
   void set_priv (bool p);
   bool is_v2_only () const;
   bool is_v1_only () const;
   int num_pieces () const;
   piece_index_t end_piece () const;
   index_range<piece_index_t> piece_range () const noexcept;
   file_index_t end_file () const;
   index_range<file_index_t> file_range () const noexcept;
   index_range<piece_index_t::diff_type> file_piece_range (file_index_t f);
   std::int64_t total_size () const;
   int piece_length () const;
   int piece_size (piece_index_t i) const;
   void add_similar_torrent (sha1_hash ih);
   void add_collection (string_view c);

   static constexpr create_flags_t modification_time  = 2_bit;
   static constexpr create_flags_t symlinks  = 3_bit;
   static constexpr create_flags_t v2_only  = 5_bit;
   static constexpr create_flags_t v1_only  = 6_bit;
   static constexpr create_flags_t canonical_files  = 7_bit;
   static constexpr create_flags_t no_attributes  = 8_bit;
   static constexpr create_flags_t canonical_files_no_tail_padding  = 9_bit;
};
```

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:create_torrent%3A%3A%5Bcreate_torrent%28%29%5D&labels=documentation&body=Documentation+under+heading+%22create_torrent%3A%3A%5Bcreate_torrent%28%29%5D%22+could+be+improved)]

## create\_torrent()

```cpp
explicit create_torrent (file_storage& fs, int piece_size = 0
      , create_flags_t flags = {});
explicit create_torrent (torrent_info const& ti);
```

The piece\_size is the size of each piece in bytes. It must be a
power of 2 and a minimum of 16 kiB. If a piece size of 0 is
specified, a piece\_size will be set automatically.
Piece sizes greater than 128 MiB are considered unreasonable and will
be rejected (with an lt::system\_error exception).

The flags arguments specifies options for the torrent creation. It can
be any combination of the flags defined by create\_flags\_t.

The [file\_storage](reference-Storage.md#file_storage) (fs) parameter defines the files, sizes and
their properties for the torrent to be created. Set this up first,
before passing it to the [create\_torrent](reference-Create_Torrents.md#create_torrent) constructor.

The overload that takes a torrent\_info object will make a verbatim
copy of its info dictionary (to preserve the info-hash). The copy of
the info dictionary will be used by [create\_torrent::generate()](reference-Create_Torrents.md#generate()). This means
that none of the member functions of [create\_torrent](reference-Create_Torrents.md#create_torrent) that affects
the content of the info dictionary (such as [set\_hash()](reference-Create_Torrents.md#set_hash())), will
have any affect. Instead of using this overload, consider using
[write\_torrent\_file()](reference-Resume_Data.md#write_torrent_file()) instead.

Warning

The [file\_storage](reference-Storage.md#file_storage) and [torrent\_info](reference-Torrent_Info.md#torrent_info) objects must stay alive for the
entire duration of the [create\_torrent](reference-Create_Torrents.md#create_torrent) object.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:create_torrent%3A%3A%5Bgenerate_buf%28%29+generate%28%29%5D&labels=documentation&body=Documentation+under+heading+%22create_torrent%3A%3A%5Bgenerate_buf%28%29+generate%28%29%5D%22+could+be+improved)]

## generate\_buf() generate()

```cpp
entry generate () const;
std::vector<char> generate_buf () const;
```

This function will generate the .torrent file as a bencode tree, or a
bencoded into a buffer.
In order to encode the [entry](reference-Bencoding.md#entry) into a flat file, use the [bencode()](reference-Bencoding.md#bencode()) function.

The function returning an [entry](reference-Bencoding.md#entry) may be useful to add custom entries
to the torrent file before bencoding it and saving it to disk.

Whether the resulting torrent object is v1, v2 or hybrid depends on
whether any of the v1\_only or v2\_only flags were set on the
constructor. If neither were set, the resulting torrent depends on
which hashes were set. If both v1 and v2 hashes were set, a hybrid
torrent is created.

Any failure will cause this function to throw system\_error, with an
appropriate error message. These are the reasons this call may throw:

* the file storage has 0 files
* the total size of the file storage is 0 bytes (i.e. it only has
  empty files)
* not all v1 hashes ([set\_hash()](reference-Create_Torrents.md#set_hash())) and not all v2 hashes ([set\_hash2()](reference-Create_Torrents.md#set_hash2()))
  were set
* for v2 torrents, you may not have a directory with the same name as
  a file. If that's encountered in the file storage, [generate()](reference-Create_Torrents.md#generate())
  fails.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:create_torrent%3A%3A%5Bfiles%28%29%5D&labels=documentation&body=Documentation+under+heading+%22create_torrent%3A%3A%5Bfiles%28%29%5D%22+could+be+improved)]

## files()

```cpp
file_storage const& files () const;
```

returns an immutable reference to the [file\_storage](reference-Storage.md#file_storage) used to create
the torrent from.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:create_torrent%3A%3A%5Bset_comment%28%29%5D&labels=documentation&body=Documentation+under+heading+%22create_torrent%3A%3A%5Bset_comment%28%29%5D%22+could+be+improved)]

## set\_comment()

```cpp
void set_comment (char const* str);
```

Sets the comment for the torrent. The string str should be utf-8 encoded.
The comment in a torrent file is optional.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:create_torrent%3A%3A%5Bset_creator%28%29%5D&labels=documentation&body=Documentation+under+heading+%22create_torrent%3A%3A%5Bset_creator%28%29%5D%22+could+be+improved)]

## set\_creator()

```cpp
void set_creator (char const* str);
```

Sets the creator of the torrent. The string str should be utf-8 encoded.
This is optional.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:create_torrent%3A%3A%5Bset_creation_date%28%29%5D&labels=documentation&body=Documentation+under+heading+%22create_torrent%3A%3A%5Bset_creation_date%28%29%5D%22+could+be+improved)]

## set\_creation\_date()

```cpp
void set_creation_date (std::time_t timestamp);
```

sets the "creation time" field. Defaults to the system clock at the
time of construction of the [create\_torrent](reference-Create_Torrents.md#create_torrent) object. The timestamp is
specified in seconds, posix time. If the creation date is set to 0,
the "creation date" field will be omitted from the generated torrent.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:create_torrent%3A%3A%5Bset_hash%28%29%5D&labels=documentation&body=Documentation+under+heading+%22create_torrent%3A%3A%5Bset_hash%28%29%5D%22+could+be+improved)]

## set\_hash()

```cpp
void set_hash (piece_index_t index, sha1_hash const& h);
```

This sets the SHA-1 hash for the specified piece (index). You are required
to set the hash for every piece in the torrent before generating it. If you have
the files on disk, you can use the high level convenience function to do this.
See [set\_piece\_hashes()](reference-Create_Torrents.md#set_piece_hashes()).
A SHA-1 hash of all zeros is internally used to indicate a hash that
has not been set. Setting such hash will not be considered set when
calling [generate()](reference-Create_Torrents.md#generate()).
This function will throw std::system\_error if it is called on an
object constructed with the v2\_only flag.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:create_torrent%3A%3A%5Bset_hash2%28%29%5D&labels=documentation&body=Documentation+under+heading+%22create_torrent%3A%3A%5Bset_hash2%28%29%5D%22+could+be+improved)]

## set\_hash2()

```cpp
void set_hash2 (file_index_t file, piece_index_t::diff_type piece, sha256_hash const& h);
```

sets the bittorrent v2 hash for file file of the piece piece.
piece is relative to the first piece of the file, starting at 0. The
first piece in the file can be computed with
[file\_storage::file\_index\_at\_piece()](reference-Storage.md#file_index_at_piece()).
The hash, h, is the root of the merkle tree formed by the piece's
16 kiB blocks. Note that piece sizes must be powers-of-2, so all
per-piece merkle trees are complete.
A SHA-256 hash of all zeros is internally used to indicate a hash
that has not been set. Setting such hash will not be considered set
when calling [generate()](reference-Create_Torrents.md#generate()).
This function will throw std::system\_error if it is called on an
object constructed with the v1\_only flag.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:create_torrent%3A%3A%5Badd_http_seed%28%29+add_url_seed%28%29%5D&labels=documentation&body=Documentation+under+heading+%22create_torrent%3A%3A%5Badd_http_seed%28%29+add_url_seed%28%29%5D%22+could+be+improved)]

## add\_http\_seed() add\_url\_seed()

```cpp
void add_url_seed (string_view url);
void add_http_seed (string_view url);
```

This adds a url seed to the torrent. You can have any number of url seeds. For a
single file torrent, this should be an HTTP url, pointing to a file with identical
content as the file of the torrent. For a multi-file torrent, it should point to
a directory containing a directory with the same name as this torrent, and all the
files of the torrent in it.

The second function, add\_http\_seed() adds an HTTP seed instead.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:create_torrent%3A%3A%5Badd_node%28%29%5D&labels=documentation&body=Documentation+under+heading+%22create_torrent%3A%3A%5Badd_node%28%29%5D%22+could+be+improved)]

## add\_node()

```cpp
void add_node (std::pair<std::string, int> node);
```

This adds a DHT node to the torrent. This especially useful if you're creating a
tracker less torrent. It can be used by clients to bootstrap their DHT node from.
The node is a hostname and a port number where there is a DHT node running.
You can have any number of DHT nodes in a torrent.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:create_torrent%3A%3A%5Badd_tracker%28%29%5D&labels=documentation&body=Documentation+under+heading+%22create_torrent%3A%3A%5Badd_tracker%28%29%5D%22+could+be+improved)]

## add\_tracker()

```cpp
void add_tracker (string_view url, int tier = 0);
```

Adds a tracker to the torrent. This is not strictly required, but most torrents
use a tracker as their main source of peers. The url should be an <http://> or udp://
url to a machine running a bittorrent tracker that accepts announces for this torrent's
info-hash. The tier is the fallback priority of the tracker. All trackers with tier 0 are
tried first (in any order). If all fail, trackers with tier 1 are tried. If all of those
fail, trackers with tier 2 are tried, and so on.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:create_torrent%3A%3A%5Bset_root_cert%28%29%5D&labels=documentation&body=Documentation+under+heading+%22create_torrent%3A%3A%5Bset_root_cert%28%29%5D%22+could+be+improved)]

## set\_root\_cert()

```cpp
void set_root_cert (string_view cert);
```

This function sets an X.509 certificate in PEM format to the torrent. This makes the
torrent an *SSL torrent*. An SSL torrent requires that each peer has a valid certificate
signed by this root certificate. For SSL torrents, all peers are connecting over SSL
connections. For more information, see the section on [ssl torrents](manual-ref.md#ssl-torrents).

The string is not the path to the cert, it's the actual content of the
certificate.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:create_torrent%3A%3A%5Bpriv%28%29+set_priv%28%29%5D&labels=documentation&body=Documentation+under+heading+%22create_torrent%3A%3A%5Bpriv%28%29+set_priv%28%29%5D%22+could+be+improved)]

## priv() set\_priv()

```cpp
bool priv () const;
void set_priv (bool p);
```

Sets and queries the private flag of the torrent.
Torrents with the private flag set ask the client to not use any other
sources than the tracker for peers, and to not use DHT to advertise itself publicly,
only the tracker.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:create_torrent%3A%3A%5Bnum_pieces%28%29%5D&labels=documentation&body=Documentation+under+heading+%22create_torrent%3A%3A%5Bnum_pieces%28%29%5D%22+could+be+improved)]

## num\_pieces()

```cpp
int num_pieces () const;
```

returns the number of pieces in the associated [file\_storage](reference-Storage.md#file_storage) object.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:create_torrent%3A%3A%5Bpiece_range%28%29%5D&labels=documentation&body=Documentation+under+heading+%22create_torrent%3A%3A%5Bpiece_range%28%29%5D%22+could+be+improved)]

## piece\_range()

```cpp
index_range<piece_index_t> piece_range () const noexcept;
```

all piece indices in the torrent to be created

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:create_torrent%3A%3A%5Bfile_range%28%29%5D&labels=documentation&body=Documentation+under+heading+%22create_torrent%3A%3A%5Bfile_range%28%29%5D%22+could+be+improved)]

## file\_range()

```cpp
index_range<file_index_t> file_range () const noexcept;
```

all file indices in the torrent to be created

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:create_torrent%3A%3A%5Bfile_piece_range%28%29%5D&labels=documentation&body=Documentation+under+heading+%22create_torrent%3A%3A%5Bfile_piece_range%28%29%5D%22+could+be+improved)]

## file\_piece\_range()

```cpp
index_range<piece_index_t::diff_type> file_piece_range (file_index_t f);
```

for v2 and hybrid torrents only, the pieces in the
specified file, specified as delta from the first piece in the file.
i.e. the first index is 0.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:create_torrent%3A%3A%5Btotal_size%28%29%5D&labels=documentation&body=Documentation+under+heading+%22create_torrent%3A%3A%5Btotal_size%28%29%5D%22+could+be+improved)]

## total\_size()

```cpp
std::int64_t total_size () const;
```

the total number of bytes of all files and pad files

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:create_torrent%3A%3A%5Bpiece_length%28%29+piece_size%28%29%5D&labels=documentation&body=Documentation+under+heading+%22create_torrent%3A%3A%5Bpiece_length%28%29+piece_size%28%29%5D%22+could+be+improved)]

## piece\_length() piece\_size()

```cpp
int piece_length () const;
int piece_size (piece_index_t i) const;
```

piece\_length() returns the piece size of all pieces but the
last one. piece\_size() returns the size of the specified piece.
these functions are just forwarding to the associated [file\_storage](reference-Storage.md#file_storage).

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:create_torrent%3A%3A%5Badd_collection%28%29+add_similar_torrent%28%29%5D&labels=documentation&body=Documentation+under+heading+%22create_torrent%3A%3A%5Badd_collection%28%29+add_similar_torrent%28%29%5D%22+could+be+improved)]

## add\_collection() add\_similar\_torrent()

```cpp
void add_similar_torrent (sha1_hash ih);
void add_collection (string_view c);
```

Add similar torrents (by info-hash) or collections of similar torrents.
Similar torrents are expected to share some files with this torrent.
Torrents sharing a collection name with this torrent are also expected
to share files with this torrent. A torrent may have more than one
collection and more than one similar torrents. For more information,
see [BEP 38](https://www.bittorrent.org/beps/bep_0038.html).

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:create_torrent%3A%3A%5Bmodification_time%5D&labels=documentation&body=Documentation+under+heading+%22create_torrent%3A%3A%5Bmodification_time%5D%22+could+be+improved)]

modification\_time
:   This will include the file modification time as part of the torrent.
    This is not enabled by default, as it might cause problems when you
    create a torrent from separate files with the same content, hoping to
    yield the same info-hash. If the files have different modification times,
    with this option enabled, you would get different info-hashes for the
    files.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:create_torrent%3A%3A%5Bsymlinks%5D&labels=documentation&body=Documentation+under+heading+%22create_torrent%3A%3A%5Bsymlinks%5D%22+could+be+improved)]

symlinks
:   If this flag is set, files that are symlinks get a symlink attribute
    set on them and their data will not be included in the torrent. This
    is useful if you need to reconstruct a file hierarchy which contains
    symlinks.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:create_torrent%3A%3A%5Bv2_only%5D&labels=documentation&body=Documentation+under+heading+%22create_torrent%3A%3A%5Bv2_only%5D%22+could+be+improved)]

v2\_only
:   Do not generate v1 metadata. The resulting torrent will only be usable by
    clients which support v2. This requires setting all v2 hashes, with
    [set\_hash2()](reference-Create_Torrents.md#set_hash2()) before calling [generate()](reference-Create_Torrents.md#generate()). Setting v1 hashes (with
    [set\_hash()](reference-Create_Torrents.md#set_hash())) is an error with this flag set.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:create_torrent%3A%3A%5Bv1_only%5D&labels=documentation&body=Documentation+under+heading+%22create_torrent%3A%3A%5Bv1_only%5D%22+could+be+improved)]

v1\_only
:   do not generate v2 metadata or enforce v2 alignment and padding rules
    this is mainly for tests, not recommended for production use. This
    requires setting all v1 hashes, with [set\_hash()](reference-Create_Torrents.md#set_hash()), before calling
    [generate()](reference-Create_Torrents.md#generate()). Setting v2 hashes (with [set\_hash2()](reference-Create_Torrents.md#set_hash2())) is an error with
    this flag set.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:create_torrent%3A%3A%5Bcanonical_files%5D&labels=documentation&body=Documentation+under+heading+%22create_torrent%3A%3A%5Bcanonical_files%5D%22+could+be+improved)]

canonical\_files
:   This flag only affects v1-only torrents, and is only relevant
    together with the v1\_only\_flag. This flag will force the
    same file order and padding as a v2 (or hybrid) torrent would have.
    It has the effect of ordering files and inserting pad files to align
    them with piece boundaries.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:create_torrent%3A%3A%5Bno_attributes%5D&labels=documentation&body=Documentation+under+heading+%22create_torrent%3A%3A%5Bno_attributes%5D%22+could+be+improved)]

no\_attributes
:   passing this flag to [add\_files()](reference-Create_Torrents.md#add_files()) will ignore file attributes (such as
    executable or hidden) when adding the files to the file storage.
    Since not all filesystems and operating systems support all file
    attributes the resulting torrent may differ depending on where it's
    created. If it's important for torrents to be created consistently
    across systems, this flag should be set.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:create_torrent%3A%3A%5Bcanonical_files_no_tail_padding%5D&labels=documentation&body=Documentation+under+heading+%22create_torrent%3A%3A%5Bcanonical_files_no_tail_padding%5D%22+could+be+improved)]

canonical\_files\_no\_tail\_padding
:   this flag enforces the file layout to be canonical according to the
    bittorrent v2 specification (just like the canonical\_files flag)
    with the one exception that tail padding is not added to the last
    file.
    This behavior deviates from the specification but was the way
    libtorrent created torrents in version up to and including 2.0.7.
    This flag is here for backwards compatibility.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:add_files%28%29&labels=documentation&body=Documentation+under+heading+%22add_files%28%29%22+could+be+improved)]

# add\_files()

Declared in "[libtorrent/create\_torrent.hpp](include/libtorrent/create_torrent.hpp)"

```cpp
void add_files (file_storage& fs, std::string const& file
   , create_flags_t flags = {});
void add_files (file_storage& fs, std::string const& file
   , std::function<bool(std::string)> p, create_flags_t flags = {});
```

Adds the file specified by path to the [file\_storage](reference-Storage.md#file_storage) object. In case path
refers to a directory, files will be added recursively from the directory.

If specified, the predicate p is called once for every file and directory that
is encountered. Files for which p returns true are added, and directories for
which p returns true are traversed. p must have the following signature:

```cpp
bool Pred(std::string const& p);
```

The path that is passed in to the predicate is the full path of the file or
directory. If no predicate is specified, all files are added, and all directories
are traversed.

The ".." directory is never traversed.

The flags argument should be the same as the flags passed to the [create\_torrent](#create-torrent)
constructor.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:set_piece_hashes%28%29&labels=documentation&body=Documentation+under+heading+%22set_piece_hashes%28%29%22+could+be+improved)]

# set\_piece\_hashes()

Declared in "[libtorrent/create\_torrent.hpp](include/libtorrent/create_torrent.hpp)"

```cpp
void set_piece_hashes (create_torrent& t, std::string const& p
   , std::function<void(piece_index_t)> const& f, error_code& ec);
inline void set_piece_hashes (create_torrent& t, std::string const& p
   , std::function<void(piece_index_t)> const& f);
inline void set_piece_hashes (create_torrent& t, std::string const& p
   , settings_interface const& settings
   , std::function<void(piece_index_t)> const& f);
inline void set_piece_hashes (create_torrent& t, std::string const& p);
void set_piece_hashes (create_torrent& t, std::string const& p
   , settings_interface const& settings
   , std::function<void(piece_index_t)> const& f, error_code& ec);
inline void set_piece_hashes (create_torrent& t, std::string const& p, error_code& ec);
void set_piece_hashes (create_torrent& t, std::string const& p
   , settings_interface const& settings, disk_io_constructor_type disk_io
   , std::function<void(piece_index_t)> const& f, error_code& ec);
```

This function will assume that the files added to the torrent file exists at path
p, read those files and hash the content and set the hashes in the create\_torrent
object. The optional function f is called in between every hash that is set. f
must have the following signature:

```cpp
void Fun(piece_index_t);
```

The overloads taking a [settings\_pack](reference-Settings.md#settings_pack) may be used to configure the
underlying disk access. Such as settings\_pack::aio\_threads.

The overloads that don't take an error\_code& may throw an exception in case of a
file error, the other overloads sets the error code to reflect the error, if any.
