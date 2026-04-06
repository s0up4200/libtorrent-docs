---
title: "storage_error"
source: "https://libtorrent.org/reference-Error_Codes.html"
---

[home](reference.md)

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:class+storage_error&labels=documentation&body=Documentation+under+heading+%22class+storage_error%22+could+be+improved)]

# storage\_error

Declared in "[libtorrent/error\_code.hpp](include/libtorrent/error_code.hpp)"

used by storage to return errors
also includes which underlying file the
error happened on

```cpp
struct storage_error
{
   explicit operator bool () const;
   file_index_t file () const;
   void file (file_index_t f);

   error_code ec;
   operation_t operation;
};
```

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:storage_error%3A%3A%5Bbool%28%29%5D&labels=documentation&body=Documentation+under+heading+%22storage_error%3A%3A%5Bbool%28%29%5D%22+could+be+improved)]

## bool()

```cpp
explicit operator bool () const;
```

explicitly converts to true if this object represents an error, and
false if it does not.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:storage_error%3A%3A%5Bfile%28%29%5D&labels=documentation&body=Documentation+under+heading+%22storage_error%3A%3A%5Bfile%28%29%5D%22+could+be+improved)]

## file()

```cpp
file_index_t file () const;
void file (file_index_t f);
```

set and query the index (in the torrent) of the file this error
occurred on. This may also have special values defined in
[torrent\_status](reference-Torrent_Status.md#torrent_status).

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:storage_error%3A%3A%5Bec%5D&labels=documentation&body=Documentation+under+heading+%22storage_error%3A%3A%5Bec%5D%22+could+be+improved)]

ec
:   the error that occurred

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:storage_error%3A%3A%5Boperation%5D&labels=documentation&body=Documentation+under+heading+%22storage_error%3A%3A%5Boperation%5D%22+could+be+improved)]

operation
:   A code from [operation\_t](reference-Alerts.md#operation_t) enum, indicating what
    kind of operation failed.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:gzip_category%28%29&labels=documentation&body=Documentation+under+heading+%22gzip_category%28%29%22+could+be+improved)]

# gzip\_category()

Declared in "[libtorrent/gzip.hpp](include/libtorrent/gzip.hpp)"

```cpp
boost::system::error_category& gzip_category ();
```

get the error\_category for zip errors

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:pcp_category%28%29&labels=documentation&body=Documentation+under+heading+%22pcp_category%28%29%22+could+be+improved)]

# pcp\_category()

Declared in "[libtorrent/natpmp.hpp](include/libtorrent/natpmp.hpp)"

```cpp
boost::system::error_category& pcp_category ();
```

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:bdecode_category%28%29&labels=documentation&body=Documentation+under+heading+%22bdecode_category%28%29%22+could+be+improved)]

# bdecode\_category()

Declared in "[libtorrent/bdecode.hpp](include/libtorrent/bdecode.hpp)"

```cpp
boost::system::error_category& bdecode_category ();
```

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:libtorrent_category%28%29&labels=documentation&body=Documentation+under+heading+%22libtorrent_category%28%29%22+could+be+improved)]

# libtorrent\_category()

Declared in "[libtorrent/error\_code.hpp](include/libtorrent/error_code.hpp)"

```cpp
boost::system::error_category& libtorrent_category ();
```

return the instance of the libtorrent\_error\_category which
maps libtorrent error codes to human readable error messages.

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:http_category%28%29&labels=documentation&body=Documentation+under+heading+%22http_category%28%29%22+could+be+improved)]

# http\_category()

Declared in "[libtorrent/error\_code.hpp](include/libtorrent/error_code.hpp)"

```cpp
boost::system::error_category& http_category ();
```

returns the error\_category for HTTP errors

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:i2p_category%28%29&labels=documentation&body=Documentation+under+heading+%22i2p_category%28%29%22+could+be+improved)]

# i2p\_category()

Declared in "[libtorrent/i2p\_stream.hpp](include/libtorrent/i2p_stream.hpp)"

```cpp
boost::system::error_category& i2p_category ();
```

returns the error category for I2P errors

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:socks_category%28%29&labels=documentation&body=Documentation+under+heading+%22socks_category%28%29%22+could+be+improved)]

# socks\_category()

Declared in "[libtorrent/socks5\_stream.hpp](include/libtorrent/socks5_stream.hpp)"

```cpp
boost::system::error_category& socks_category ();
```

returns the error\_category for SOCKS5 errors

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:upnp_category%28%29&labels=documentation&body=Documentation+under+heading+%22upnp_category%28%29%22+could+be+improved)]

# upnp\_category()

Declared in "[libtorrent/upnp.hpp](include/libtorrent/upnp.hpp)"

```cpp
boost::system::error_category& upnp_category ();
```

the boost.system error category for UPnP errors

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:enum+error_code_enum&labels=documentation&body=Documentation+under+heading+%22enum+error_code_enum%22+could+be+improved)]

# enum error\_code\_enum

Declared in "[libtorrent/gzip.hpp](include/libtorrent/gzip.hpp)"

| name | value | description |
| --- | --- | --- |
| no\_error | 0 | Not an error |
| invalid\_gzip\_header | 1 | the supplied gzip buffer has invalid header |
| inflated\_data\_too\_large | 2 | the gzip buffer would inflate to more bytes than the specified maximum size, and was rejected. |
| data\_did\_not\_terminate | 3 | available inflate data did not terminate |
| space\_exhausted | 4 | output space exhausted before completing inflate |
| invalid\_block\_type | 5 | invalid block type (type == 3) |
| invalid\_stored\_block\_length | 6 | stored block length did not match one's complement |
| too\_many\_length\_or\_distance\_codes | 7 | dynamic block code description: too many length or distance codes |
| code\_lengths\_codes\_incomplete | 8 | dynamic block code description: code lengths codes incomplete |
| repeat\_lengths\_with\_no\_first\_length | 9 | dynamic block code description: repeat lengths with no first length |
| repeat\_more\_than\_specified\_lengths | 10 | dynamic block code description: repeat more than specified lengths |
| invalid\_literal\_length\_code\_lengths | 11 | dynamic block code description: invalid literal/length code lengths |
| invalid\_distance\_code\_lengths | 12 | dynamic block code description: invalid distance code lengths |
| invalid\_literal\_code\_in\_block | 13 | invalid literal/length or distance code in fixed or dynamic block |
| distance\_too\_far\_back\_in\_block | 14 | distance is too far back in fixed or dynamic block |
| unknown\_gzip\_error | 15 | an unknown error occurred during gzip inflation |
| error\_code\_max | 16 | the number of error codes |

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:enum+pcp_errors&labels=documentation&body=Documentation+under+heading+%22enum+pcp_errors%22+could+be+improved)]

# enum pcp\_errors

Declared in "[libtorrent/natpmp.hpp](include/libtorrent/natpmp.hpp)"

| name | value | description |
| --- | --- | --- |
| pcp\_success | 0 |  |
| pcp\_unsupp\_version | 1 |  |
| pcp\_not\_authorized | 2 |  |
| pcp\_malformed\_request | 3 |  |
| pcp\_unsupp\_opcode | 4 |  |
| pcp\_unsupp\_option | 5 |  |
| pcp\_malformed\_option | 6 |  |
| pcp\_network\_failure | 7 |  |
| pcp\_no\_resources | 8 |  |
| pcp\_unsupp\_protocol | 9 |  |
| pcp\_user\_ex\_quota | 10 |  |
| pcp\_cannot\_provide\_external | 11 |  |
| pcp\_address\_mismatch | 12 |  |
| pcp\_excessive\_remote\_peers | 13 |  |

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:enum+error_code_enum&labels=documentation&body=Documentation+under+heading+%22enum+error_code_enum%22+could+be+improved)]

# enum error\_code\_enum

Declared in "[libtorrent/bdecode.hpp](include/libtorrent/bdecode.hpp)"

| name | value | description |
| --- | --- | --- |
| no\_error | 0 | Not an error |
| expected\_digit | 1 | expected digit in bencoded string |
| expected\_colon | 2 | expected colon in bencoded string |
| unexpected\_eof | 3 | unexpected end of file in bencoded string |
| expected\_value | 4 | expected value (list, dict, [int](reference-Core.md#int) or string) in bencoded string |
| depth\_exceeded | 5 | bencoded recursion depth limit exceeded |
| limit\_exceeded | 6 | bencoded item count limit exceeded |
| overflow | 7 | integer overflow |
| error\_code\_max | 8 | the number of error codes |

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:enum+error_code_enum&labels=documentation&body=Documentation+under+heading+%22enum+error_code_enum%22+could+be+improved)]

# enum error\_code\_enum

Declared in "[libtorrent/error\_code.hpp](include/libtorrent/error_code.hpp)"

| name | value | description |
| --- | --- | --- |
| no\_error | 0 | Not an error |
| file\_collision | 1 | Two torrents has files which end up overwriting each other |
| failed\_hash\_check | 2 | A piece did not match its piece hash |
| torrent\_is\_no\_dict | 3 | The .torrent file does not contain a bencoded dictionary at its top level |
| torrent\_missing\_info | 4 | The .torrent file does not have an info dictionary |
| torrent\_info\_no\_dict | 5 | The .torrent file's info [entry](reference-Bencoding.md#entry) is not a dictionary |
| torrent\_missing\_piece\_length | 6 | The .torrent file does not have a piece length [entry](reference-Bencoding.md#entry) |
| torrent\_missing\_name | 7 | The .torrent file does not have a name [entry](reference-Bencoding.md#entry) |
| torrent\_invalid\_name | 8 | The .torrent file's name [entry](reference-Bencoding.md#entry) is invalid |
| torrent\_invalid\_length | 9 | The length of a file, or of the whole .torrent file is invalid. Either negative or not an integer |
| torrent\_file\_parse\_failed | 10 | Failed to parse a file [entry](reference-Bencoding.md#entry) in the .torrent |
| torrent\_missing\_pieces | 11 | The pieces field is missing or invalid in the .torrent file |
| torrent\_invalid\_hashes | 12 | The pieces string has incorrect length |
| too\_many\_pieces\_in\_torrent | 13 | The .torrent file has more pieces than is supported by libtorrent |
| invalid\_swarm\_metadata | 14 | The metadata (.torrent file) that was received from the swarm matched the info-hash, but failed to be parsed |
| invalid\_bencoding | 15 | The file or buffer is not correctly bencoded |
| no\_files\_in\_torrent | 16 | The .torrent file does not contain any files |
| invalid\_escaped\_string | 17 | The string was not properly url-encoded as expected |
| session\_is\_closing | 18 | Operation is not permitted since the [session](reference-Session.md#session) is shutting down |
| duplicate\_torrent | 19 | There's already a torrent with that info-hash added to the [session](reference-Session.md#session) |
| invalid\_torrent\_handle | 20 | The supplied [torrent\_handle](reference-Torrent_Handle.md#torrent_handle) is not referring to a valid torrent |
| invalid\_entry\_type | 21 | The type requested from the [entry](reference-Bencoding.md#entry) did not match its type |
| missing\_info\_hash\_in\_uri | 22 | The specified URI does not contain a valid info-hash |
| file\_too\_short | 23 | One of the files in the torrent was unexpectedly small. This might be caused by files being changed by an external process |
| unsupported\_url\_protocol | 24 | The URL used an unknown protocol. Currently http and https (if built with openssl support) are recognized. For trackers udp is recognized as well. |
| url\_parse\_error | 25 | The URL did not conform to URL syntax and failed to be parsed |
| peer\_sent\_empty\_piece | 26 | The peer sent a piece message of length 0 |
| parse\_failed | 27 | A bencoded structure was corrupt and failed to be parsed |
| invalid\_file\_tag | 28 | The fast resume file was missing or had an invalid file version tag |
| missing\_info\_hash | 29 | The fast resume file was missing or had an invalid info-hash |
| mismatching\_info\_hash | 30 | The info-hash did not match the torrent |
| invalid\_hostname | 31 | The URL contained an invalid hostname |
| invalid\_port | 32 | The URL had an invalid port |
| port\_blocked | 33 | The port is blocked by the port-filter, and prevented the connection |
| expected\_close\_bracket\_in\_address | 34 | The IPv6 address was expected to end with "]" |
| destructing\_torrent | 35 | The torrent is being destructed, preventing the operation to succeed |
| timed\_out | 36 | The connection timed out |
| upload\_upload\_connection | 37 | The peer is upload only, and we are upload only. There's no point in keeping the connection |
| uninteresting\_upload\_peer | 38 | The peer is upload only, and we're not interested in it. There's no point in keeping the connection |
| invalid\_info\_hash | 39 | The peer sent an unknown info-hash |
| torrent\_paused | 40 | The torrent is paused, preventing the operation from succeeding |
| invalid\_have | 41 | The peer sent an invalid have message, either wrong size or referring to a piece that doesn't exist in the torrent |
| invalid\_bitfield\_size | 42 | The [bitfield](reference-Utility.md#bitfield) message had the incorrect size |
| too\_many\_requests\_when\_choked | 43 | The peer kept requesting pieces after it was choked, possible abuse attempt. |
| invalid\_piece | 44 | The peer sent a piece message that does not correspond to a piece request sent by the client |
| no\_memory | 45 | memory allocation failed |
| torrent\_aborted | 46 | The torrent is aborted, preventing the operation to succeed |
| self\_connection | 47 | The peer is a connection to ourself, no point in keeping it |
| invalid\_piece\_size | 48 | The peer sent a piece message with invalid size, either negative or greater than one block |
| timed\_out\_no\_interest | 49 | The peer has not been interesting or interested in us for too long, no point in keeping it around |
| timed\_out\_inactivity | 50 | The peer has not said anything in a long time, possibly dead |
| timed\_out\_no\_handshake | 51 | The peer did not send a handshake within a reasonable amount of time, it might not be a bittorrent peer |
| timed\_out\_no\_request | 52 | The peer has been unchoked for too long without requesting any data. It might be lying about its interest in us |
| invalid\_choke | 53 | The peer sent an invalid choke message |
| invalid\_unchoke | 54 | The peer send an invalid unchoke message |
| invalid\_interested | 55 | The peer sent an invalid interested message |
| invalid\_not\_interested | 56 | The peer sent an invalid not-interested message |
| invalid\_request | 57 | The peer sent an invalid piece request message |
| invalid\_hash\_list | 58 | The peer sent an invalid hash-list message (this is part of the merkle-torrent extension) |
| invalid\_hash\_piece | 59 | The peer sent an invalid hash-piece message (this is part of the merkle-torrent extension) |
| invalid\_cancel | 60 | The peer sent an invalid cancel message |
| invalid\_dht\_port | 61 | The peer sent an invalid DHT port-message |
| invalid\_suggest | 62 | The peer sent an invalid suggest piece-message |
| invalid\_have\_all | 63 | The peer sent an invalid have all-message |
| invalid\_have\_none | 64 | The peer sent an invalid have none-message |
| invalid\_reject | 65 | The peer sent an invalid reject message |
| invalid\_allow\_fast | 66 | The peer sent an invalid allow fast-message |
| invalid\_extended | 67 | The peer sent an invalid extension message ID |
| invalid\_message | 68 | The peer sent an invalid message ID |
| sync\_hash\_not\_found | 69 | The synchronization hash was not found in the encrypted handshake |
| invalid\_encryption\_constant | 70 | The encryption constant in the handshake is invalid |
| no\_plaintext\_mode | 71 | The peer does not support plain text, which is the selected mode |
| no\_rc4\_mode | 72 | The peer does not support RC4, which is the selected mode |
| unsupported\_encryption\_mode | 73 | The peer does not support any of the encryption modes that the client supports |
| unsupported\_encryption\_mode\_selected | 74 | The peer selected an encryption mode that the client did not advertise and does not support |
| invalid\_pad\_size | 75 | The pad size used in the encryption handshake is of invalid size |
| invalid\_encrypt\_handshake | 76 | The encryption handshake is invalid |
| no\_incoming\_encrypted | 77 | The client is set to not support incoming encrypted connections and this is an encrypted connection |
| no\_incoming\_regular | 78 | The client is set to not support incoming regular bittorrent connections, and this is a regular connection |
| duplicate\_peer\_id | 79 | The client is already connected to this peer-ID |
| torrent\_removed | 80 | Torrent was removed |
| packet\_too\_large | 81 | The packet size exceeded the upper sanity check-limit |
| reserved | 82 |  |
| http\_error | 83 | The web server responded with an error |
| missing\_location | 84 | The web server response is missing a location header |
| invalid\_redirection | 85 | The web seed redirected to a path that no longer matches the .torrent directory structure |
| redirecting | 86 | The connection was closed because it redirected to a different URL |
| invalid\_range | 87 | The HTTP range header is invalid |
| no\_content\_length | 88 | The HTTP response did not have a content length |
| banned\_by\_ip\_filter | 89 | The IP is blocked by the IP filter |
| too\_many\_connections | 90 | At the connection limit |
| peer\_banned | 91 | The peer is marked as banned |
| stopping\_torrent | 92 | The torrent is stopping, causing the operation to fail |
| too\_many\_corrupt\_pieces | 93 | The peer has sent too many corrupt pieces and is banned |
| torrent\_not\_ready | 94 | The torrent is not ready to receive peers |
| peer\_not\_constructed | 95 | The peer is not completely constructed yet |
| session\_closing | 96 | The [session](reference-Session.md#session) is closing, causing the operation to fail |
| optimistic\_disconnect | 97 | The peer was disconnected in order to leave room for a potentially better peer |
| torrent\_finished | 98 | The torrent is finished |
| no\_router | 99 | No UPnP router found |
| metadata\_too\_large | 100 | The metadata message says the metadata exceeds the limit |
| invalid\_metadata\_request | 101 | The peer sent an invalid metadata request message |
| invalid\_metadata\_size | 102 | The peer advertised an invalid metadata size |
| invalid\_metadata\_offset | 103 | The peer sent a message with an invalid metadata offset |
| invalid\_metadata\_message | 104 | The peer sent an invalid metadata message |
| pex\_message\_too\_large | 105 | The peer sent a peer exchange message that was too large |
| invalid\_pex\_message | 106 | The peer sent an invalid peer exchange message |
| invalid\_lt\_tracker\_message | 107 | The peer sent an invalid tracker exchange message |
| too\_frequent\_pex | 108 | The peer sent an pex messages too often. This is a possible attempt of and attack |
| no\_metadata | 109 | The operation failed because it requires the torrent to have the metadata (.torrent file) and it doesn't have it yet. This happens for magnet links before they have downloaded the metadata, and also torrents added by URL. |
| invalid\_dont\_have | 110 | The peer sent an invalid dont\_have message. The don't have message is an extension to allow peers to advertise that the no longer has a piece they previously had. |
| requires\_ssl\_connection | 111 | The peer tried to connect to an SSL torrent without connecting over SSL. |
| invalid\_ssl\_cert | 112 | The peer tried to connect to a torrent with a certificate for a different torrent. |
| not\_an\_ssl\_torrent | 113 | the torrent is not an SSL torrent, and the operation requires an SSL torrent |
| banned\_by\_port\_filter | 114 | peer was banned because its listen port is within a banned port range, as specified by the [port\_filter](reference-Filter.md#port_filter). |
| invalid\_session\_handle | 115 | The [session\_handle](reference-Session.md#session_handle) is not referring to a valid session\_impl |
| invalid\_listen\_socket | 116 | the listen socket associated with this request was closed |
| invalid\_hash\_request | 117 |  |
| invalid\_hashes | 118 |  |
| invalid\_hash\_reject | 119 |  |
| deprecated\_120 | 120 |  |
| deprecated\_121 | 121 |  |
| deprecated\_122 | 122 |  |
| deprecated\_123 | 123 |  |
| deprecated\_124 | 124 |  |
| missing\_file\_sizes | 130 | The resume data file is missing the file sizes [entry](reference-Bencoding.md#entry) |
| no\_files\_in\_resume\_data | 131 | The resume data file file sizes [entry](reference-Bencoding.md#entry) is empty |
| missing\_pieces | 132 | The resume data file is missing the pieces and slots [entry](reference-Bencoding.md#entry) |
| mismatching\_number\_of\_files | 133 | The number of files in the resume data does not match the number of files in the torrent |
| mismatching\_file\_size | 134 | One of the files on disk has a different size than in the fast resume file |
| mismatching\_file\_timestamp | 135 | One of the files on disk has a different timestamp than in the fast resume file |
| not\_a\_dictionary | 136 | The resume data file is not a dictionary |
| invalid\_blocks\_per\_piece | 137 | The blocks per piece [entry](reference-Bencoding.md#entry) is invalid in the resume data file |
| missing\_slots | 138 | The resume file is missing the slots [entry](reference-Bencoding.md#entry), which is required for torrents with compact allocation. *DEPRECATED* |
| too\_many\_slots | 139 | The resume file contains more slots than the torrent |
| invalid\_slot\_list | 140 | The slot [entry](reference-Bencoding.md#entry) is invalid in the resume data |
| invalid\_piece\_index | 141 | One index in the slot list is invalid |
| pieces\_need\_reorder | 142 | The pieces on disk needs to be re-ordered for the specified allocation mode. This happens if you specify sparse allocation and the files on disk are using compact storage. The pieces needs to be moved to their right position. *DEPRECATED* |
| resume\_data\_not\_modified | 143 | this error is returned when asking to save resume data and specifying the flag to only save when there's anything new to save ([torrent\_handle::only\_if\_modified](reference-Torrent_Handle.md#only_if_modified)) and there wasn't anything changed. |
| invalid\_save\_path | 144 | the save\_path in [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params) is not valid |
| http\_parse\_error | 150 | The HTTP header was not correctly formatted |
| http\_missing\_location | 151 | The HTTP response was in the 300-399 range but lacked a location header |
| http\_failed\_decompress | 152 | The HTTP response was encoded with gzip or deflate but decompressing it failed |
| no\_i2p\_router | 160 | The URL specified an i2p address, but no i2p router is configured |
| no\_i2p\_endpoint | 161 | i2p acceptor is not available yet, can't announce without endpoint |
| scrape\_not\_available | 170 | The tracker URL doesn't support transforming it into a scrape URL. i.e. it doesn't contain "announce. |
| invalid\_tracker\_response | 171 | invalid tracker response |
| invalid\_peer\_dict | 172 | invalid peer dictionary [entry](reference-Bencoding.md#entry). Not a dictionary |
| tracker\_failure | 173 | tracker sent a failure message |
| invalid\_files\_entry | 174 | missing or invalid files [entry](reference-Bencoding.md#entry) |
| invalid\_hash\_entry | 175 | missing or invalid hash [entry](reference-Bencoding.md#entry) |
| invalid\_peers\_entry | 176 | missing or invalid peers and peers6 [entry](reference-Bencoding.md#entry) |
| invalid\_tracker\_response\_length | 177 | UDP tracker response packet has invalid size |
| invalid\_tracker\_transaction\_id | 178 | invalid transaction id in UDP tracker response |
| invalid\_tracker\_action | 179 | invalid action field in UDP tracker response |
| announce\_skipped | 180 | skipped announce (because it's assumed to be unreachable over the given source network interface) |
| no\_entropy | 200 | random number generation failed |
| ssrf\_mitigation | 201 | blocked by SSRF mitigation |
| blocked\_by\_idna | 202 | blocked because IDNA host names are banned |
| torrent\_unknown\_version | 210 | the torrent file has an unknown meta version |
| torrent\_missing\_file\_tree | 211 | the v2 torrent file has no file tree |
| torrent\_missing\_meta\_version | 212 | the torrent contains v2 keys but does not specify meta version 2 |
| torrent\_inconsistent\_files | 213 | the v1 and v2 file metadata does not match |
| torrent\_missing\_piece\_layer | 214 | one or more files are missing piece layer hashes |
| torrent\_invalid\_piece\_layer | 215 | a piece layer has the wrong size or failed hash check |
| torrent\_missing\_pieces\_root | 216 | a v2 file [entry](reference-Bencoding.md#entry) has no root hash |
| torrent\_inconsistent\_hashes | 217 | the v1 and v2 hashes do not describe the same data |
| torrent\_invalid\_pad\_file | 218 | a file in the v2 metadata has the pad attribute set |
| error\_code\_max | 219 | the number of error codes |

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:enum+http_errors&labels=documentation&body=Documentation+under+heading+%22enum+http_errors%22+could+be+improved)]

# enum http\_errors

Declared in "[libtorrent/error\_code.hpp](include/libtorrent/error_code.hpp)"

| name | value | description |
| --- | --- | --- |
| cont | 100 |  |
| ok | 200 |  |
| created | 201 |  |
| accepted | 202 |  |
| no\_content | 204 |  |
| multiple\_choices | 300 |  |
| moved\_permanently | 301 |  |
| moved\_temporarily | 302 |  |
| not\_modified | 304 |  |
| bad\_request | 400 |  |
| unauthorized | 401 |  |
| forbidden | 403 |  |
| not\_found | 404 |  |
| internal\_server\_error | 500 |  |
| not\_implemented | 501 |  |
| bad\_gateway | 502 |  |
| service\_unavailable | 503 |  |

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:enum+i2p_error_code&labels=documentation&body=Documentation+under+heading+%22enum+i2p_error_code%22+could+be+improved)]

# enum i2p\_error\_code

Declared in "[libtorrent/i2p\_stream.hpp](include/libtorrent/i2p_stream.hpp)"

| name | value | description |
| --- | --- | --- |
| no\_error | 0 |  |
| parse\_failed | 1 |  |
| cant\_reach\_peer | 2 |  |
| i2p\_error | 3 |  |
| invalid\_key | 4 |  |
| invalid\_id | 5 |  |
| timeout | 6 |  |
| key\_not\_found | 7 |  |
| duplicated\_id | 8 |  |
| num\_errors | 9 |  |

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:enum+socks_error_code&labels=documentation&body=Documentation+under+heading+%22enum+socks_error_code%22+could+be+improved)]

# enum socks\_error\_code

Declared in "[libtorrent/socks5\_stream.hpp](include/libtorrent/socks5_stream.hpp)"

| name | value | description |
| --- | --- | --- |
| no\_error | 0 |  |
| unsupported\_version | 1 |  |
| unsupported\_authentication\_method | 2 |  |
| unsupported\_authentication\_version | 3 |  |
| authentication\_error | 4 |  |
| username\_required | 5 |  |
| general\_failure | 6 |  |
| command\_not\_supported | 7 |  |
| no\_identd | 8 |  |
| identd\_error | 9 |  |
| num\_errors | 10 |  |

[[report issue](http://github.com/arvidn/libtorrent/issues/new?title=docs:enum+error_code_enum&labels=documentation&body=Documentation+under+heading+%22enum+error_code_enum%22+could+be+improved)]

# enum error\_code\_enum

Declared in "[libtorrent/upnp.hpp](include/libtorrent/upnp.hpp)"

| name | value | description |
| --- | --- | --- |
| no\_error | 0 | No error |
| invalid\_argument | 402 | One of the arguments in the request is invalid |
| action\_failed | 501 | The request failed |
| value\_not\_in\_array | 714 | The specified value does not exist in the array |
| source\_ip\_cannot\_be\_wildcarded | 715 | The source IP address cannot be wild-carded, but must be fully specified |
| external\_port\_cannot\_be\_wildcarded | 716 | The external port cannot be a wildcard, but must be specified |
| port\_mapping\_conflict | 718 | The port mapping [entry](reference-Bencoding.md#entry) specified conflicts with a mapping assigned previously to another client |
| internal\_port\_must\_match\_external | 724 | Internal and external port value must be the same |
| only\_permanent\_leases\_supported | 725 | The NAT implementation only supports permanent lease times on port mappings |
| remote\_host\_must\_be\_wildcard | 726 | RemoteHost must be a wildcard and cannot be a specific IP address or DNS name |
| external\_port\_must\_be\_wildcard | 727 | ExternalPort must be a wildcard and cannot be a specific port |
