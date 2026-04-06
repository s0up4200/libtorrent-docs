---
title: "forward declarations and ABI"
date: "2017-12"
source: "https://blog.libtorrent.org/2017/12/forward-declarations-and-abi/"
---

Sunday, December 31st, 2017 by arvid

This post argues the C++ rule:

> ***One should never forward declare a name from a 3rd party library***

This rule is a generalisation of the same rule for the standard library. The standard says [[namespace.std]](http://eel.is/c++draft/library#namespace.std-1):

> The behavior of a C++ program is undefined if it adds declarations or definitions to namespace std or to a namespace within namespace std unless otherwise specified.

This has also been covered by [guru of the week](http://www.gotw.ca/gotw/034.htm).

## inline namespaces

The most practical way to provide ABI compatibility in a C++ library is to use [inline namespaces](http://en.cppreference.com/w/cpp/language/namespace#Inline_namespaces). i.e. namespaces that contribute to the linker name of a symbol, but that remains invisible at the API level. Declarations in an inline namespace behave as if they had been in the parent namespace.

Inline namespaces allows a library to provide a single API, but multiple implementations of functions, to cover previous ABIs. Here’s a toy example:

library\_v1.hpp:

```
namespace library {
  inline namespace v1 {
    int foo();
  }
}
```

library\_v2.hpp:

```
namespace library {
  inline namespace v2 {
    int foo(int b = 42);
  }
}
```

In most senses, these APIs are the same (short of taking a pointer to the function). A client built against library\_v1.hpp will expect (at the binary level) a function not taking any arguments. A client built against library\_v2.hpp will expect one argument. The implementation of the new version of the library, in order to be backwards compatible, could be:

```
namespace library {
  inline namespace v1 {
    int foo() { return 42; }
  }
  inline namespace v2 {
    int foo(int b) { return b; }
  }
}
```

The beauty of this scheme is that the client (in principle) can be rebuilt against version 2 of the library with no source code changes. It will simply start linking against the v2 versions of functions at the ABI level.

## forward declarations

Imagine the client forward declaring foo(). It would probably look something like this:

```
namespace library { int foo(); }
```

And this would work for a version of the library that did not use inline namespaces for ABI versioning. But as soon as the library introduce inline namespaces, any reference to this symbol would (most likely) become a linker error (missing symbol).

This is a fundamental reason for the rule. The client does not know enough about symbols declared in 3rd party libraries to provide forward declarations for them.

## forward declaration headers

In order to get the benefits of forward declarations (limiting the amount of text included into a translation unit), libraries can provide forward declaration headers. The standard library does this in [<iosfwd>](http://en.cppreference.com/w/cpp/header/iosfwd). But it’s a practice that should be more widespread. I think an equally important rule as the one at the top is:

> ***libraries should provide forward declaration header(s)***

Starting in libtorrent 1.1.4, there is a [“libtorrent/fwd.hpp”](https://github.com/arvidn/libtorrent/blob/master/include/libtorrent/fwd.hpp) header, that provide forward declarations for all public symbols in libtorrent. Since this header is cheap to include, it is recommended over any forward declaration of libtorrent headers.

Posted in [c++](https://blog.libtorrent.org/category/c/)
**|**
 [No Comments](https://blog.libtorrent.org/2017/12/forward-declarations-and-abi/#respond)

---

### Leave a Reply [Cancel reply](/2017/12/forward-declarations-and-abi/#respond)

You must be [logged in](https://blog.libtorrent.org/wp-login.php?redirect_to=https%3A%2F%2Fblog.libtorrent.org%2F2017%2F12%2Fforward-declarations-and-abi%2F) to post a comment.
