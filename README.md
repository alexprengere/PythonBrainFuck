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
./bf.py hello.bf
Hello World!
```

Speeding things up
------------------

The interpreter is actually written in Rpython, so it can be statically compiled using the Pypy toolchain. Download the latest source of Pypy and uncompress it in a `pypy-src` folder.

```bash
wget 'https://bitbucket.org/pypy/pypy/downloads/pypy-5.0.0-src.tar.bz2'
tar -xvjf pypy-5.0.0-src.tar.bz2
mv pypy-5.0.0-src pypy-src
```

Then you can build from the Python script `bf.py` an executable binary `bf-c`. This should take 5 minutes:
```bash
python pypy-src/rpython/bin/rpython bf.py
# Mandelbrot completes in a bit more than 1 minute
./bf-c examples/mandel.b
```

You can rebuild the `bf-c` using `--opt=jit` to add a JIT to your BrainFuck interpreter. This should take 20 minutes:
```bash
python pypy-src/rpython/bin/rpython --opt=jit bf.py
# Mandelbrot completes now in 15 seconds!
./bf-c examples/mandel.b
```

Here is a summary of the speed gain I could observe on a Fedora (22) VM (4 cores, 4Go of RAM), running `mandel.b`:
* the initial `bf.py` with CPython (2.7): about 4 hours (baseline)
* the initial `bf.py` with Pypy (2.4): 8 minutes (30x)
* the `bf-c` without JIT: 1min15s (x200)
* the `bf-c` with JIT: 15 seconds (x1000)

Interpreters written in C taken from [here](http://mazonka.com/brainf/) are available in the `interpreters` folder, and take from 15 to 20 seconds to run.
The JIT addition contains code from [this amazing tutorial on JITs](http://morepypy.blogspot.fr/2011/04/tutorial-part-2-adding-jit.html).
