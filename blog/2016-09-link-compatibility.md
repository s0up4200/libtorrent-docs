---
title: "link compatibility"
date: "2016-09"
source: "https://blog.libtorrent.org/2016/09/link-compatibility/"
---

Thursday, September 29th, 2016 by arvid

A major source of errors among users of libtorrent has traditionally been caused by binary incompatibility between the (built) libtorrent library and the client linking against it. Binary- or link compatibility is having two sides of a shared library (or translation unit) boundary have different understandings about the layout of objects or calling conventions.

Consider the following library interface:

```
// A.hpp
struct A {
#ifdef USE_ASSERTS
 int c;
#endif
 int a;
 int b;
};

void foobar(A const& a);
```

The A.hpp header file is included by (at least) two separate translation units. One in the client and one in the library. In order for them to interoperate correctly, it is critical that both translation units have the same view of the USE\_ASSERTS define. If they don’t, they will look for the members at different offsets.

The symptom of getting this wrong is subtle memory corruption.

There are a few ways consistent build configurations can be managed by build tools.

1. boost-build has great support for having first-class support for builds to propagate requirements both up and down the dependency tree. Boost build is primary build system for libtorrent, and does just this.
2. pkg-config can be used to define requirements on builds depending on your library. Specifically, you have a chance to inject compile flags and link flags in the build of whomever immediately depends on you. (this also requires that you know what compiler that project will use, so people typically just assum GCC)

My experience is that not a lot of people use boost build as their build system and people mostly use pkg-config \*after\* having been bitten by these kinds of problems.

The problem is still that submitting a bug report is still part of the loop of resolving these kinds of issues.

To improve the situation, libtorrent introduced a build configuration header, illustrated by this code:

```
// build_config.hpp
#ifdef NO_DEPRECATED_FUNCTIONS
#define CFG_DEPR nodeprecate_
#else
#define CFG_DEPR deprecated_
#endif

#if USE_ASSERTS
#define CFG_ASSERTS asserts_
#else
#define CFG_ASSERTS noasserts_
#endif

#define CFG BOOST_PP_CAT(CFG_DEPR, CFG_ASSERTS)

#define CFG_STRING BOOST_PP_STRINGIZE(CFG)

void CFG();
```

This code declares a function whose name indicates what build configuration options are used. Somewhere in the library, this function will need to be defined.

Say, in A.cpp:

```
// A.cpp
#include "build_config.hpp"
void CFG() {}
```

The last thing is to make the client somehow create a reference to this function. Since the build\_config.hpp is included in a client translation unit, it will form a name based on the client’s configuration, and try to call a function with that name. If the configurations match, the function will be found and it will work. If the configuraions differ, the funciton won’t be found and it will either end up being a link-time error (in the case of static linking) or a startup error in the case of shared linking.

There are a few ways to make your client call this function, the simplest is to wrap a common function in an inlined wrapper, that first calls your configuration function and then passes the arguments on to the actual function. Or you could do the same thing to a constructor of a class your client is likely to instantiate.

```
struct B {
 B() { CFG(); init(); }
private:
 void init();
};

inline int foobar(int a) {
 CFG();
 return detail::foobar_impl();
}
```

This has been deployed in libtorrent for a few years now and it has turned hard-to-diagnose memory corruption errors into link errors like this:

```
Undefined symbols for architecture x86_64:
 "library_link_check::deprecated_asserts_()", referenced from:
 _main in client.o
ld: symbol(s) not found for architecture x86_64
```

Posted in [c++](https://blog.libtorrent.org/category/c/)
**|**
 [No Comments](https://blog.libtorrent.org/2016/09/link-compatibility/#respond)

---
