---
title: "building libtorrent for C.H.I.P.™"
date: "2017-02"
source: "https://blog.libtorrent.org/2017/02/building-libtorrent-for-c-h-i-p/"
---

Tuesday, February 28th, 2017 by arvid

I recently bought a [C.H.I.P.](https://getchip.com/) and naturally wanted to build libtorrent for it. I’m on a mac and chip runs arm, so first I needed to install the cross compiler toolchain. The target for chip is arm on linux, so the toolchain I’m looking for is “arm-linux-gnueabihf”.

## toolchain

It seems like [a fair number of people](https://gist.github.com/joegoggins/7763637#gistcomment-1287579) online suggest using “gcc-arm-none-eabi”, presumably because that’s a package that’s easily available on homebrew. However, having a generic build, not for linux, means linux specifics won’t work. Specifically, the “-pthread” argument is not recognized by that variant of GCC.

There are old binaries for a linaro gcc cross compiler build for mac OS [here](http://www.welzels.de/blog/downloads/?category=13). This installs all the gcc and binutils we need:

```
arm-linux-gnueabihf-g++
arm-linux-gnueabihf-ar
arm-linux-gnueabihf-ld
... etc ...
```

The tools we’re especially concerned with are **arm-linux-gnueabihf-g++** (the compiler) and **arm-linux-gnueabihf-ar** (the archiver for making static libraries) and **arm-linux-gnueabihf-ld** (the linker). Let’s first check out the compiler:

```
$ arm-linux-gnueabihf-g++ --version
arm-linux-gnueabihf-g++ (crosstool-NG linaro-1.13.1-4.9-2014.05 - Linaro GCC 4.9-2014.05) 4.9.1 20140505 (prerelease)
Copyright (C) 2014 Free Software Foundation, Inc.
This is free software; see the source for copying conditions. There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```

## user-config.jam

Next we need to configure [boost build](http://www.boost.org/build/) to know about this version of gcc. It’s possible to configure toolsets per project, but I like to configure my toolsets user-wide. For this, you put the definition in **~/user-config.jam**.

The rule for configuring a toolset in boost build is “[using](http://www.boost.org/build/doc/html/bbv2/reference/tools.html)” and its synopsis is:

using *toolset* : *version* : *compile-command* : *options* ;

**toolset:** The toolset is called **gcc**.  
**version:** To avoid clashing with the system compiler, we give this configuration of the toolset a unique name, “chip”. It will be referred to as “gcc-chip” on the b2 command line later.  
**compile-command:** This is the command to run the compiler, “arm-linux-gnueabihf-g++”.  
**options:** You need to specify which target-os and architecture this toolset builds for, you do this with:

```
<target-os>linux <architecture>arm
```

In this case I have an older version of GCC that doesn’t default to C++11, so I also need to specify:

```
<cxxflags>-std=c++11 <linkflags>-std=c++11
```

boost build will link via the compile command, but it will need to know which archiver to use to build static libraries/archives. You specify that like this:

```
<archiver>arm-linux-gnueabihf-ar
```

Putting it all together you get this line in your ~/user-config.jam:

```
using gcc : chip : arm-linux-gnueabihf-g++ : <archiver>arm-linux-gnueabihf-ar
   <cxxflags>-std=c++11 <linkflags>-std=c++11 ;
```

Keep in mind that whitespace matters in jam. You need those spaces around “:” and “;”.

This configures a GCC compiler for the specified target operating system and architecture.

## building libtorrent

To build libtorrent for this target, in the libtorrent example directory, run:

```
$ b2 gcc-chip -j4 link=static target-os=linux architecture=arm release
```

For a development build, you want to disable invariant checks, since they can be quite expensive, causing poor run-time performance:

```
$ b2 gcc-chip -j4 link=static target-os=linux architecture=arm invariant-checks=off
```

Posted in [Uncategorized](https://blog.libtorrent.org/category/uncategorized/)
**|**
 [No Comments](https://blog.libtorrent.org/2017/02/building-libtorrent-for-c-h-i-p/#respond)

---

### Leave a Reply [Cancel reply](/2017/02/building-libtorrent-for-c-h-i-p/#respond)

You must be [logged in](https://blog.libtorrent.org/wp-login.php?redirect_to=https%3A%2F%2Fblog.libtorrent.org%2F2017%2F02%2Fbuilding-libtorrent-for-c-h-i-p%2F) to post a comment.
