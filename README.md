[![BuildBadge](https://github.com/narekgharibyan/ptimeit/workflows/Build/badge.svg)](https://github.com/narekgharibyan/ptimeit/actions)
[![PyPIVersion](https://img.shields.io/pypi/v/ptimeit.svg)](https://pypi.python.org/pypi/ptimeit/)
[![PythonFormat](https://img.shields.io/pypi/format/ptimeit.svg)](https://pypi.python.org/pypi/ptimeit/)

# ptimeit
pretty timeit - simple and pretty python code profiler for measuring execution time

```
pip install ptimeit
```
---

## examples

### function execution time
use `timeit_function` decorator for measuring function execution time
```python
import time
from ptimeit import timeit_function


@timeit_function('foo')
def foo():
    time.sleep(0.1)


foo()
```

outputs:
```
->>>>>>>>         102.7ms      foo()
```

Adding a conditional function that determines if something is printed. The function receives elapsed time in milliseconds as an input and is expected to return a boolean.

```python
import time
from ptimeit import timeit_function


@timeit_function('foo', lambda t: t > 500)
def foo():
    time.sleep(0.1)

@timeit_function('bar', condition=lambda t: t > 500)
def bar():
    time.sleep(1)

foo()
bar()
```

No output for `foo` - measured time needs to be over 500ms to be printed.

`bar` outputs:
```
->>>>>>>>        1003.1ms      bar()
```

Adding extra data
```python
import time
from ptimeit import timeit_function


@timeit_function('foo', extra_data_to_print="This is a string")
def foo():
    time.sleep(0.1)


foo()
```

outputs:
```
->>>>>>>>         103.3ms      foo() - This is a string
```

---

### code section execution time
use `timeit_section` context manager for measuring code section execution time
```python
import time
from ptimeit import timeit_section

with timeit_section('bar'):
     time.sleep(0.1)
```
outputs:
```
->>>>>>>>         105.1ms      bar
```
It is also possible to use conditional `condition` function and `extra_data_to_print` the same way as in `timeit_function`.

---
### nested mixture of functions and sections

```python
import time
from ptimeit import timeit_function, timeit_section


@timeit_function('foo_inner')
def foo_inner():
    with timeit_section('foo_inner:section_1'):
        time.sleep(0.05)
    with timeit_section('foo_inner:section_2'):
        time.sleep(0.25)


@timeit_function('foo_outer')
def foo_outer():
    with timeit_section('foo_outer:section_1'):
        time.sleep(0.2)

    foo_inner()

    with timeit_section('foo_outer:section_2'):
        time.sleep(0.4)


with timeit_section('bar:outer'):
    foo_outer()
    time.sleep(0.1)

```
outputs:
```
->>>>>>>>         200.1ms      |   |   foo_outer:section_1
->>>>>>>>          51.3ms      |   |   |   foo_inner:section_1
->>>>>>>>         252.8ms      |   |   |   foo_inner:section_2
->>>>>>>>         304.3ms      |   |   foo_inner()
->>>>>>>>         403.0ms      |   |   foo_outer:section_2
->>>>>>>>         907.6ms      |   foo_outer()
->>>>>>>>        1010.8ms      bar:outer
```
