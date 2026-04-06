---
title: "unsigned integers"
date: "2016-05"
source: "https://blog.libtorrent.org/2016/05/unsigned-integers/"
---

Sunday, May 1st, 2016 by arvid

In this post I will talk about the use of unsigned (integral) types in C++, or perhaps more specifically the rationale for using them. In my experience, it is common to use unsigned types for any variable holding a value that cannot be negative. Say, the number of bytes in a buffer.

On the face of it, you’ll save 1 bit (supporting twice as large values), and if you have an upper bound you only need a single comparison (no need to check < 0).

In this post I hope to provide convincing arguments against this reasoning and to provide an alternative.

It’s important to first understand the mechanism in C and C++ called integer promotion. Roughly speaking, this is what allows intermediate values of expressions to enjoy wider storage than the operands. This allows the results to be less surprising. An example (adopted from [CERT](https://www.securecoding.cert.org/confluence/display/cplusplus/INT02-CPP.+Understand+integer+conversion+rules)):

```
int8_t c1 = 100;
int8_t c2 = 3;
int8_t c3 = 4;
int8_t result = c1 * c2 / c3;
```

The product of c1 and c2 (100 \* 3) is 300, which does not fit in an **int8\_t**, but the type of the intermediate value is **int**. This makes the final result correct, since once divided by 4, the value does fit in an **int8\_t**.

So far we’re good, this is clearly the right thing for the language to do. It makes the results intuitive and we don’t need to manually widen types in our expressions. You can imagine that intermediate values are loaded into CPU registers, which are as wide as **int**, so it makes sense all around.

**int** is special though, as it’s expected to be the native word size on the hardware. If you have an expression with **int** operands, that produce intermediate values requiring **int64\_t**, there will be no type promotion. However, operands are promoted to the widest operand. Multiplying an **int64\_t** with **int**, will yield an **int64\_t** result.

Another way of thinking about the rules is: operand types are always promoted to the widest among them, but no less than **int**. **int** being the narrowest type arithmetic operators perform on.

When dealing with expressions with mixed signed and unsigned operands of equal width, signed operands are promoted to unsigned. This is why your compiler insists on warning you of expressions mixing signed and unsigned types. Let’s look at an example:

```
int32_t a = -1;
uint32_t b = 1;
if (a > b) printf("wat");
```

Unsigned integers trump signed ones. a will be promoted to **uint32\_t**, and its value will be interpreted as UINT32\_MAX. It’s then tested for being greater than b, which is 1. The printf() statement will be executed.

Another example:

```
uint8_t a = 1;
int b = ~a;
printf("inverted a = %d\n", b);
```

Recall the narrowest type of any arithmetic operator is **int**. a will be promoted and zero-extended to **int**. It’s then negated (assuming **int** is 32 bits) turning its value to 0xfffffffe, which signed means -2. You may have expected the result to be 0xfe.

### in integer promotion, unsigned trump signed

cppreference.com has a [good writeup](http://en.cppreference.com/w/cpp/language/implicit_conversion) on conversion rules.

The main two properties of unsigned integers are:

1. underflow and overflow have well-defined wrapping semantics
2. when values are widened, there is no sign-extension

Wrapping (especially of intermediate values) violate our intuition of regular arithmetic. With it, expressions can no longer be manipulated according to regular algebraic rules. Take this example:

```
int32_t a = -2;
uint32_t b = 4;
int32_t c = 2;
int32_t d = (a - b) / c + 10;
```

Intuitively, this expression (-2 – 4) / 2 + 10 should evaluate to -3 + 10 = 7. However, since b is unsigned, the result of the subtraction is not -3, but 0xfffffffd. Dividing that by 2 will result in another large value that we add 10 to.

### The unsigned type adds discontinuities in the value space, breaking algebraic transformations and optimizations.

For instance, imagine a and c are known constants in this context, but b is an input argument. The compiler may want to transform that expression into:

```
int32_t d = 9 - (b >> 1);
```

Assuming regular rules for transforming expressions, this would be a valid simplification. It would remove the costly division altogether and remove the addition. This transformation would be valid if b was signed. However, because of the discontinuity of the unsigned value space, this transformed expression no longer yields the same result as the original one. This would be an invalid optimization.

In C++, causing a signed integer to over- or underflow has undefined behavior. This is a good thing. Without it the compiler would not be able to assume that normal algebraic rules apply, and it would be restricted in simplifying and optimizing expressions.

Another example is this snippet:

```
int32_t x = variable;
if (x+1 > x) printf("the world is sane\n");
```

Since x is signed the compiler can assume that x+1 will always be greater than x and optimize away the if-statement. If it had to assume that x+1 may wrap, it would not have been able to do that.

### in arithmetic, wrapping behavior is unintuitive

An alternative way to reason about whether a variable should be signed or unsigned is to ask yourself

“is it an error for the variable to over- or underflow?”

Sometimes the answer is “no” and wrap-around behavior is desirable. In my experience though, this is much more rare than the frequency with which you’ll find unsigned types used in C++.

If you feel worried about invoking undefined behavior by over- or underflowing your variables, a case can be made that undefined behavior may be a lot better than well-defined, silent incorrect behavior (i.e. wrapping). In practice, the undefined behavior will also yield an incorrect result (just like the wrapped result). However, there are are tools to help you sanitize and harden your code against these issues.

If it is more important that your application is correct than running, you could compile with the GCC and clang option **-ftrapv**. From the gcc [documentation](https://gcc.gnu.org/onlinedocs/gcc/Code-Gen-Options.html):

This option generates traps for signed overflow on addition, subtraction, multiplication operations.

This is especially useful to catch overflows in debuggers. Another option is to use the more modern [undefined behavior sanitizer](http://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html) (**-fsanitize=undefined**), which will not only trap on signed under- and overflow, but on invocations of other undefined behaviors as well.

In fact, I would argue the tool support itself is a great reason to prefer signed types. If an unsigned type overflows, no tool can warn you about it, because there’s technically nothing wrong with it.

A related issue is the eternal question wether a pointer to a byte buffer should be a **char\***, **uint8\_t\*** or **void\***. Let’s assume we want to perform some pointer arithmetic, so rule out **void\***.

When reasoning about raw bytes, it’s common to think of them as unsigned, since you may want to concatenate them into larger integer values or other bit-wise operations. It’s also commonly not desirable to trigger sign extensions when juggling raw bytes.

On the other hand, you may also want to treat memory as strings sometimes, and all string operations take **char\*** (normally signed).

Having different parts of your code disagree on whether bytes are signed or unsigned will cause a lot of reinterpret\_cast, which is not very fun.

In a recent [proposal](http://proposal http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0257r0.pdf), Neil MacIntosh suggests the solution is **neither**. A raw byte is not an arithmetic type, it should not be possible to add, subtract, multiply or divide them. Those operators imply an interpretation of the data, and raw bytes have no interpretation until the program assigns meaning to them (by casting to an appropriate type, e.g. string, hash or int). The definition of this type is quite simple:

```
enum class byte : unsigned char {};
```

Of course, pointer arithmetic can be significantly reduced and simplified by using the GSL [span](https://github.com/Microsoft/GSL/blob/master/include/span.h) class.

## Summary

What are unsigned types good for then? I can think of a few examples.

* The sequence number in a TCP implementation wraps at 32 bits. This is defined by the protocol and makes sense.
* The cursor into a circular buffer whose size is always a power of 2. This would also wrap by design, presumably the wrapping would be implemented by an explicit AND mask, but even intermediate values would want wrapping.

It’s common to add variables holding flags to this list, and while that makes sense, one could argue that flags should not be held by an integral type to begin with. It does not make sense to have multiplication defined for a flags variable. This is what the standard I/O stream library does for its [stream flags](http://en.cppreference.com/w/cpp/io/ios_base/fmtflags).

A summary of the takeaways:

* integer promotion rules are complex, especially when mixing in unsigned types. Even if you get it right, the code becomes complex and relies on every subsequent reader to also get it right.
* use unsigned types only when the value domain mandate wrapping semantics.

References

* [INT02-CPP. Understand integer conversion rules](https://www.securecoding.cert.org/confluence/display/cplusplus/INT02-CPP.+Understand+integer+conversion+rules)
* [cppreference.com implicit conversions](http://en.cppreference.com/w/cpp/language/implicit_conversion)

Posted in [algorithms](https://blog.libtorrent.org/category/algorithms/), [c++](https://blog.libtorrent.org/category/c/)
**|**
 [1 Comment](https://blog.libtorrent.org/2016/05/unsigned-integers/#comments)

---

### 1 Comment

### Leave a Reply [Cancel reply](/2016/05/unsigned-integers/#respond)

You must be [logged in](https://blog.libtorrent.org/wp-login.php?redirect_to=https%3A%2F%2Fblog.libtorrent.org%2F2016%2F05%2Funsigned-integers%2F) to post a comment.
