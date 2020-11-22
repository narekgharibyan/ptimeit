[![BuildBadge](https://github.com/narekgharibyan/ptimeit/workflows/Build/badge.svg)](https://github.com/narekgharibyan/ptimeit/actions)
[![PyPIVersion](https://img.shields.io/pypi/v/ptimeit.svg)](https://pypi.python.org/pypi/ptimeit/)
[![PythonFormat](https://img.shields.io/pypi/format/ptimeit.svg)](https://pypi.python.org/pypi/ptimeit/)

# ptimeit
simple and pretty python code profiler for measuring execution time

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
