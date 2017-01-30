A very (!) fast BrainFuck interpreter in Python
===============================================

Here is a BrainFuck example:

```bf
+++++ +++++             initialize counter (cell #0) to 10
[                       use loop to set the next four cells to 70/100/30/10
> +++++ ++              add  7 to cell #1
> +++++ +++++           add 10 to cell #2
> +++                   add  3 to cell #3
> +                     add  1 to cell #4
<<<< -                  decrement counter (cell #0)
]
> ++ .                  print 'H'
> + .                   print 'e'
+++++ ++ .              print 'l'
.                       print 'l'
+++ .                   print 'o'
> ++ .                  print ' '
<< +++++ +++++ +++++ .  print 'W'
> .                     print 'o'
+++ .                   print 'r'
----- - .               print 'l'
----- --- .             print 'd'
> + .                   print '!'
> .                     print '\n'
```

How to use the interpreter:

```bash
./bf.py hello.bf
Hello World!
```

## Speeding things up

### With Pypy

If you try to run a long BrainFuck program like `mandel.b`, you will realize our interpreter is pretty slow.

```bash
./bf.py examples/mandel.b
# wait 4 hours
```

A first simple way of speeding things up is to use Pypy instead of CPython. You can use `portable-pypy` to get Pypy without compiling it yourself:

```bash
wget 'https://bitbucket.org/squeaky/portable-pypy/downloads/pypy-5.6-linux_x86_64-portable.tar.bz2'
tar -xvjf 'pypy-5.6-linux_x86_64-portable.tar.bz2'
mv pypy-5.6-linux_x86_64-portable pypy-portable
# Only 8 minutes now!
./pypy-portable/bin/pypy ./bf.py ./examples/mandel.b
```

### With a JIT

The interpreter is actually written in Rpython, so it can be statically compiled using the Pypy toolchain.
Download the latest source of Pypy and uncompress it in a `pypy-src` folder.

```bash
wget 'https://bitbucket.org/pypy/pypy/downloads/pypy2-v5.6.0-src.tar.bz2'
tar -xvjf 'pypy2-v5.6.0-src.tar.bz2'
mv pypy2-v5.6.0-src pypy-src
```

Then you can build from the Python script `bf.py` an executable binary `bf-c`:

```bash
# This will take about 1 minute
python pypy-src/rpython/bin/rpython bf.py
# Mandelbrot completes in a bit more than 1 minute
./bf-c examples/mandel.b
```

You can rebuild the `bf-c` using `--opt=jit` to add a JIT to your BrainFuck interpreter:

```bash
# This will take about 25 minutes
python pypy-src/rpython/bin/rpython --opt=jit bf.py
# Mandelbrot now completes in 15 seconds(!)
./bf-c examples/mandel.b
```

### Let's compare with a C implementation

I also tested BrainFuck interpreters written in C ([source](http://mazonka.com/brainf/)). After compilation with `gcc -O3` (5.1), running `mandel.b` take from 12 to 15 seconds to run, so it is in the same order of magnitude as the JIT version (without `-O3`, it takes 30 seconds).

```bash
gcc -O3 ./resources/bff4.c -o bff4
# 12-15 seconds
./bff4 < examples/mandel.b
```

### Let's compile the BrainFuck directly

To complete those numbers, I finally tested a [Brainfuck to C translator](https://gist.github.com/Ricket/939687), then compiled the C version of the `mandel.b` program. With `-O3`, the compiled `mandel.b` runs in about 2 seconds (without `-O3`, it takes 30 seconds).

```bash
gcc resources/brainfucc.c -o brainfucc
./brainfucc < examples/mandel.b > mandel.c
gcc -O3 mandel.c -o mandel
# 1-2 seconds
./mandel
```

### Summary

Here is a summary of the speed gain I could observe on a Fedora (22) VM (4 cores, 4Go of RAM), running `mandel.b`:

* the initial `bf.py` with CPython (2.7): about 4 hours (baseline)
* the initial `bf.py` with Pypy (2.4): 8 minutes (30x)
* the initial `bf.py` with Pypy (5.0.1): 4 minutes (60x)
* the `bf-c` without JIT: 1min15s (x200)
* the `bf-c` with JIT: 15 seconds (x1000)
* the `bff4` C implementation: 12-15 seconds
* the `mandel` binary built when compiling `mandel.b` directly: 1-2 seconds

The JIT addition contains code from [this amazing tutorial on JITs](http://morepypy.blogspot.fr/2011/04/tutorial-part-2-adding-jit.html).
If the BrainFuck interpreter `bf.py`  is a bit hairy to look at, you can check out the `step_by_step` folder to go from the simplest interpreter, then
using only Rpython code, then with a JIT, then with some final optimizations.
