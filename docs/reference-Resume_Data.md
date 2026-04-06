---
title: "read_resume_data()"
source: "https://libtorrent.org/reference-Resume_Data.html"
---

[home](reference.md)

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:read_resume_data%28%29&labels=documentation&body=Documentation+under+heading+%22read_resume_data%28%29%22+could+be+improved)]

# read\_resume\_data()

Declared in "[libtorrent/read\_resume\_data.hpp](include/libtorrent/read_resume_data.hpp)"

```cpp
add_torrent_params read_resume_data (span<char const> buffer
   , load_torrent_limits const& cfg = {});
add_torrent_params read_resume_data (bdecode_node const& rd
   , int piece_limit = 0x200000);
add_torrent_params read_resume_data (span<char const> buffer
   , error_code& ec, load_torrent_limits const& cfg = {});
add_torrent_params read_resume_data (bdecode_node const& rd
   , error_code& ec, int piece_limit = 0x200000);
```

these functions are used to parse resume data and populate the appropriate
fields in an [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params) object. This object can then be used to add
the actual [torrent\_info](reference-Torrent_Info.md#torrent_info) object to and pass to session::add\_torrent() or
session::async\_add\_torrent().

If the client wants to override any field that was loaded from the resume
data, e.g. save\_path, those fields must be changed after loading resume
data but before adding the torrent.

The piece\_limit parameter determines the largest number of pieces
allowed in the torrent that may be loaded as part of the resume data, if
it contains an info field. The overloads that take a flat buffer are
instead configured with limits on torrent sizes via load\_torrent limits.

In order to support large torrents, it may also be necessary to raise the
[settings\_pack::max\_piece\_count](reference-Settings.md#max_piece_count) setting and pass a higher limit to calls
to [torrent\_info::parse\_info\_section()](reference-Torrent_Info.md#parse_info_section()).

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:write_resume_data%28%29+write_resume_data_buf%28%29&labels=documentation&body=Documentation+under+heading+%22write_resume_data%28%29+write_resume_data_buf%28%29%22+could+be+improved)]

# write\_resume\_data() write\_resume\_data\_buf()

Declared in "[libtorrent/write\_resume\_data.hpp](include/libtorrent/write_resume_data.hpp)"

```cpp
std::vector<char> write_resume_data_buf (add_torrent_params const& atp);
entry write_resume_data (add_torrent_params const& atp);
```

this function turns the resume data in an add\_torrent\_params object
into a bencoded structure

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:write_torrent_file_buf%28%29+write_torrent_file%28%29&labels=documentation&body=Documentation+under+heading+%22write_torrent_file_buf%28%29+write_torrent_file%28%29%22+could+be+improved)]

# write\_torrent\_file\_buf() write\_torrent\_file()

Declared in "[libtorrent/write\_resume\_data.hpp](include/libtorrent/write_resume_data.hpp)"

```cpp
std::vector<char> write_torrent_file_buf (add_torrent_params const& atp
   , write_torrent_flags_t flags);
entry write_torrent_file (add_torrent_params const& atp, write_torrent_flags_t flags);
entry write_torrent_file (add_torrent_params const& atp);
```

writes only the fields to create a .torrent file. This function may fail
with a std::system\_error exception if:

* The [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params) object passed to this function does not contain the
  info dictionary (the ti field)
* The piece layers are not complete for all files that need them

The write\_torrent\_file\_buf() overload returns the torrent file in
bencoded buffer form. This overload may be faster at the expense of lost
flexibility to add custom fields.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:write_torrent_flags_t&labels=documentation&body=Documentation+under+heading+%22write_torrent_flags_t%22+could+be+improved)]

# write\_torrent\_flags\_t

Declared in "[libtorrent/write\_resume\_data.hpp](include/libtorrent/write_resume_data.hpp)"

allow\_missing\_piece\_layer
:   this makes [write\_torrent\_file()](reference-Resume_Data.md#write_torrent_file()) not fail when attempting to write a
    v2 torrent file that does not have all the piece layers

no\_http\_seeds
:   don't include http seeds in the torrent file, even if some are
    present in the [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params) object

include\_dht\_nodes
:   When set, DHT nodes from the [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params) objects are included
    in the resulting .torrent file
