---
title: "libtorrent python binding"
source: "https://libtorrent.org/python_binding.html"
---

# libtorrent python binding

# building

libtorrent can be built as a python module.

The best way to build the python bindings is using setup.py. This invokes
b2 under the hood, so you must have all of libtorrent's build dependencies
installed.

If you just want to build the shared library python extension without python
packaging semantics, you can also invoke b2 directly.

# prerequisites

Whether building with setup.py or directly invoking b2, you must
install the build prerequisites on your system:

1. All [the build prerequisites for the main libtorrent library](building.md), including
   boost libraries and b2, and your building toolchain (gcc, visual
   studio, etc).
2. Boost.Python, if not otherwise included in your boost installation
3. Python 3.7+. Older versions may work, but are not tested.

## environment variables

b2 is very sensitive to environment variables. At least the following are
required:

1. BOOST\_ROOT
2. BOOST\_BUILD\_PATH

b2 is also known to reference dozens of other environment variables when
detecting toolsets. Keep this in mind if you are building in an isolation
environment like tox.

# building with setup.py

By default, setup.py will invoke b2 to build libtorrent:

```cpp
python setup.py build
```

setup.py is a normal distutils-based setup script.

To install into your python environment:

```cpp
python setup.py install
```

To build a binary wheel package:

```cpp
python -m pip install wheel
python setup.py bdist_wheel
```

## build for a different python version

setup.py will target the running interpreter. To build for different python
versions, you must change how you invoke setup.py:

```cpp
# build for python3.7
python3.7 setup.py build
# build for python3.7
python3.7 setup.py build
```

## customizing the build

You can customize the build by passing options to the build\_ext step of
setup.py by passing arguments directly to b2 via --b2-args=:

```cpp
python setup.py build_ext --b2-args="toolset=msvc-14.2 linkflags=-L../../src/.libs"
```

For a full list of b2 build options, see [libtorrent build features](building.md#build-features).

Here, it's important to note that build\_ext has no "memory" of the build
config and arguments you passed to it before. This is *different* from the way
distutils normally works. Consider:

```cpp
python setup.py build_ext --b2-args="optimization=space"
# the following will build with DEFAULT optimization
python setup.py install
```

In order to customize the build *and* run other steps like installation, you
should run the steps inline with build\_ext:

```cpp
python setup.py build_ext --b2-args="optimization=space" install
```

# building with b2

You will need to update your user-config.jam so b2 can find your python
installation.

b2 has some auto-detection capabilities. You may be able to do just this:

```cpp
using python : 3.7 ;
```

However you may need to specify full paths. On windows, it make look like
this:

```cpp
using python : 3.7 : C:/Users/<UserName>/AppData/Local/Programs/Python/Python36 : C:/Users/<UserName>/AppData/Local/Programs/Python/Python36/include : C:/Users/<UserName>/AppData/Local/Programs/Python/Python36/libs ;
```

Or on Linux, like this:

```cpp
using python : 3.7 : /usr/bin/python3.7 : /usr/include/python3.7 : /usr/lib/python3.7 ;
```

Note that b2's python path detection is known to only work for global
python installations. It is known to be broken for virtualenvs or pyenv. If
you are using pyenv to manage your python versions, you must specify full
include and library paths yourself.

## invoking b2

Build the bindings like so:

```cpp
cd bindings/python
b2 release python=3.7 address-model=64
```

Note that address-model should match the python installation you are
building for.

For other build features, see [libtorrent build options](building.md#build-features).

## static linking

A python module is a shared library. Specifying link=static when building
the binding won't work, as it would try to produce a static library.

Instead, control whether the libtorrent main library or boost is linked
statically with libtorrent-link=static and boost-link=static
respectively.

By default both are built and linked as shared libraries.

Building and linking boost as static library is only possibly by building it
from source. Specify the BOOST\_ROOT environment variable to point to the
root directory of the boost source distribution.

For example, to build a self-contained python module:

```cpp
b2 release python=3.7 libtorrent-link=static boost-link=static
```

## helper targets

There are some targets for placing the build artifact in a helpful location:

```cpp
$ b2 release python=3.7 stage_module stage_dependencies
```

This will produce a libtorrent python module in the current directory (file
name extension depends on operating system). The libraries the python module depends
on will be copied into ./dependencies.

To install the python module, build it with the following command:

```cpp
b2 release python=3.7 install_module
```

By default the module will be installed to the python user site. This can be
changed with the python-install-scope feature. The valid values are user
(default) and system. e.g.:

```cpp
b2 release python=3.7 install_module python-install-scope=system
```

To specify a custom installation path for the python module, specify the desired
path with the python-install-path feature. e.g.:

```cpp
b2 release python=3.7 install_module python-install-path=/home/foobar/python-site/
```

# using libtorrent in python

The python interface is nearly identical to the C++ interface. Please refer to
the [library reference](reference.md). The main differences are:

asio::tcp::endpoint
:   The endpoint type is represented as a tuple of a string (as the address) and an int for
    the port number. E.g. ("127.0.0.1", 6881) represents the localhost port 6881.

lt::time\_duration
:   The time duration is represented as a number of seconds in a regular integer.

The following functions takes a reference to a container that is filled with
entries by the function. The python equivalent of these functions instead returns
a list of entries.

* torrent\_handle::get\_peer\_info
* torrent\_handle::file\_progress
* torrent\_handle::get\_download\_queue
* torrent\_handle::piece\_availability

create\_torrent::add\_node() takes two arguments, one string and one integer,
instead of a pair. The string is the address and the integer is the port.

session::apply\_settings() accepts a dictionary with keys matching the names
of settings in settings\_pack.
When calling apply\_settings, the dictionary does not need to have every settings set,
keys that are not present are not updated.

To get a python dictionary of the settings, call session::get\_settings.

Retrieving session statistics in Python is more convenient than that in C++. The
statistics are stored as an array in session\_stats\_alert, which will be
posted after calling post\_session\_stats() in the session object. In
order to interpret the statistics array, in C++ it is required to call
session\_stats\_metrics() to get the indices of these metrics, while in Python
it can be done using session\_stats\_alert.values["NAME\_OF\_METRIC"], where
NAME\_OF\_METRIC is the name of a metric.

# set\_alert\_notify

The set\_alert\_notify() function is not compatible with python. Since it
requires locking the GIL from within the libtorrent thread, to call the callback,
it can cause a deadlock with the main thread.

Instead, use the python-specific set\_alert\_fd() which takes a file descriptor
that will have 1 byte written to it to notify the client that there are new
alerts to be popped.

The file descriptor should be set to non-blocking mode. If writing to the
file/sending to the socket blocks, libtorrent's internal thread will stall.

This can be used with socket.socketpair(), for example. The file descriptor
is what fileno() returns on a socket.

# Example

For an example python program, see client.py in the bindings/python
directory.

A very simple example usage of the module would be something like this:

```cpp
import libtorrent as lt
import time
import sys

ses = lt.session({'listen_interfaces': '0.0.0.0:6881'})

info = lt.torrent_info(sys.argv[1])
h = ses.add_torrent({'ti': info, 'save_path': '.'})
s = h.status()
print('starting', s.name)

while (not s.is_seeding):
    s = h.status()

    print('\r%.2f%% complete (down: %.1f kB/s up: %.1f kB/s peers: %d) %s' % (
        s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000,
        s.num_peers, s.state), end=' ')

    alerts = ses.pop_alerts()
    for a in alerts:
        if a.category() & lt.alert.category_t.error_notification:
            print(a)

    sys.stdout.flush()

    time.sleep(1)

print(h.status().name, 'complete')
```
