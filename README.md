[![BuildBadge](https://github.com/narekgharibyan/ptimeit/workflows/Build/badge.svg)](https://github.com/narekgharibyan/ptimeit/actions)

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

