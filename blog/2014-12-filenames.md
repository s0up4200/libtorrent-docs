---
title: "filenames"
date: "2014-12"
source: "https://blog.libtorrent.org/2014/12/filenames/"
---

A .torrent file is very flexible in what it allows a path or filename to contain. Each directory name in a path is a length-prefixed utf-8 string. It can be an empty string, and it can have any character imaginable in it. The way a .torrent file represents filenames and paths is also agnostic to the way your OS/filesystem may represent paths (it does assume a directory hierarchy though).

A file is represented by a list of directory entries, where the last one is the name of the file. Like this:

```
["the","quick","brown","fox","jumps","over","the","lazy","dog"]
```

On a unix system, this path would be

```
the/quick/brown/fox/jumps/over/the/lazy/dog
```

and on windows the forward slashes would be backslashes. Typical filesystems are more restrictive. They may have restrictions on:

* how long each name entry can be.
* how long the total path can be.
* which characters are allowed to be used in the names.
* certain names may be reserved (“prn”, “con”, etc. on windows)

On windows, a file may not have a trailing period (“.”). It also may not have a trailing space (” “).

In order to map the directory structure from a .torrent file to a filesystem, filenames and directory names need to be transformed into something that’s allowed and supported by it. These are some of the transformations:

* trailing spaces and periods must be removed, recursively (if both the last an penultimate character is a dot, just removing the last won’t be enough).
* empty names must be made non-empty. After removing all trailing spaces and dots, perhaps there are no more characters left.
* [invalid characters](http://en.wikipedia.org/wiki/Filename#Reserved_characters_and_words) must be made valid. On windows these include all character codes 0-31 and <>:”/\|?\*. Posix is typically a bit more forgiving, allowing many more characters, essentially only prohibiting null and /.
* on windows, [reserved words](http://msdn.microsoft.com/en-us/library/windows/desktop/aa365247(v=vs.85).aspx#naming_conventions) must be converted to non-reserved. For instance “con”, “prn”, “aux”, etc. These words are reserved with any arbitrary filename extension as well.
* absolute paths and directory names “..” should not be allowed, as a security feature. Downloading a torrent should not be able to change files outside of the download directory.
* filenames are typically restricted to certain maximum lengths. Honoring these involves truncating filenames. It’s probably a good idea to preserve filename extensions when truncating.
* filenames may not be case sensitive. This involves disambiguating filenames that would refer to the same file on the target filesystem. This can be done with the old trick of adding an enumerator at the end. libtorrent adds file-1, file-2, etc. for duplicate filenames.

The kinds of attacks one can launch against a client lacking these kinds of tests may not be obvious. Consider a maliciously crafted torrent where one of the files path is:

```
["..", ".profile"]
```

and that your download directory is /Users/arvid/downloads. The file may end up downloading at “/Users/arvid/downloads/../.profile”, which resolves to “/Users/arvid/.profile”. The creator of that torrent can now control the contents in your terminal startup script and essentially do anything the next time you launch a shell.

Windows supports a more modern way of specifying paths with some nice properties. [UNC paths](http://msdn.microsoft.com/en-us/library/gg465305.aspx) are more general paths that can refer to windows shares, but also files on the local computer (using “?” as the hostname). The benefit of UNC paths is that many of the old DOS restrictions no longer apply to them:

* There are no reserved words, “con”, “prn” etc. are OK to use as filenames.
* The max path length is significantly longer (about 32 k, instead of 256 characters).
* Paths are not allowed to be relative (security feature, if you want to use current working directory, do so explicitly).
* Paths are not allowed to include path elements “..” or “.”, to step backwards the directory hierarchy. (security feature, no more injection of “..” to escape the download directory). This means you are allowed to have file and directory names called “..”.
* forward slashes are not automatically transformed into backslashes.
* multiple backslashes are not collapsed into single ones (i.e. “\\” -> “\”) and disallowed (apart from the prefix).

By default, libtorrent uses UNC paths on windows.

All strings in .torrent files are UTF-8 encoded, or at least they are treated as UTF-8. One of my favorite attacks is generating invalid UTF-8 sequences in attempts to circumvent security checks.

First, a brief review. [UTF-8](http://en.wikipedia.org/wiki/UTF-8#Description) is a scheme to encode any unicode codepoint (each representing a character) with variable length sequences. There are about 1,1 million unicode codepoints, and UTF-8 encodes the first 127 as a single bytes, the next 1920 characters as 2 bytes and so on. The higher the value of the codepoint, the more bytes you need to encode it in UTF-8.

A naive UTF-8 decoder may accept a 2 or 3 byte sequence encoding a codepoint <= 127. Just encode redundant leading zeros. For instance, imagine encoding the character “.” as a 2 byte sequence, instead of the single byte it’s supposed to be. This may trick security checks looking for a “..” directory entry, but still be allowed, and be decoded into a “.”. Such encodings are called overlong and are not legal UTF-8.

libtorrent verifies all encoding by decoding all characters and re-encodes them. If any illegal sequence is encountered, it’s replaced by a replacement character.

All the rules of how the filename mappings are done cause compatibility issues. Between:

* the same software running on different operating systems
* different implementations coming up with different mapping rules
* different versions of the same software

The last one may be the most surprising. libtorrent has experienced this once and will experience it again. For security reasons, it may be important to update how filenames are formed from torrents, and when upgrading from one version to the next, you may no longer be seeding the files you thought you were.

Specifically what has happened in libtorrent was turning empty folder names into “\_”. Previous versions would leave the empty string, let it end up as a path like this:

```
["foo", "", "bar"] -> "foo//bar" -> (OS collapses) "foo/bar"
```

Relying on the operating system to collapse empty folders seemed inelegant and potentially dangerous. Also, UNC paths on windows don’t allow for this. This was the main motivation behind the change.

Another upcoming change for the next major version of libtorrent is that path elements will be preserved as specified in the torrent, rather than split. For example, current libtorrent makes this transform:

```
["foo/bar", "abc", "def"] -> "foo/bar/abc/def"
```

The next major version will instead make the following transform:

```
["foo/bar", "abc", "def"] -> "foo_bar/abc/def"
```

The good news though, is that only edge cases and borderline exploit attempts are affected by these changes. The majority of torrents presumably honor the typical naming restrictions of modern operating systems.

---
