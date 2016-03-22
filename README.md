A BrainFuck interpreter in Python
=================================

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
$ ./bf.py hello.bf
Hello World!
```

What's coming next uses code from [this tutorial on JITs](http://morepypyyy.blogspot.fr/2011/04/tutorial-part-2-adding-jit.html).

The interpreter is actually written in Rpython, so it can be statically compiled using the Pypy toolchain. Download the latest source of Pypy and uncompress it in a `pypy-src` folder.

```bash
$ wget 'https://bitbucket.org/pypy/pypy/downloads/pypy-5.0.0-src.tar.bz2'
$ tar -xvjf pypy-5.0.0-src.tar.bz2
$ mv pypy-5.0.0-src pypy-src
```

Then you can build from the Python script `bf.py` an executable binary `bf-c`, this should take 5 minutes:
```bash
$ python pypy-src/rpython/bin/rpython bf.py
$ ./bf-c examples/mandel.b # Mandelbrot in a bit more than 1 minute
```

You can rebuild using `--opt=jit` to add a JIT to your BrainFuck interpreter(!), this should take 20 minutes:
```bash
$ python pypy-src/rpython/bin/rpython --opt=jit bf.py
$ ./bf-c examples/mandel.b # now 15 seconds!
```

Let's sum up the speed gain I could observe running `mandel.b`:
* the initial `bf.py` with CPython: about 4 hours (baseline)
* the initial `bf.py` with Pypy only 8 minutes (30x)
* the `bf-c` without JIT: about 1min15s (x200)
* the `bf-c` with JIT: about 15 seconds (x1000)

Interpreters written in C are available in the `interpreters` folder, and take from 15 to 20 seconds to run.
