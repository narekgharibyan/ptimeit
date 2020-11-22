import functools
import time
from contextlib import contextmanager


_depth = -1


@contextmanager
def timeit_section(section_name: str):
    """
    Returns a context manager for profiling code section execution time.

    :param section_name: section name to use in the output record.

    example: the code below outputs

    >>> import time
    >>> from ptimeit import timeit_section
    >>>
    >>> with timeit_section('section:foo'):
    >>>     time.sleep(0.1)
    >>>
    >>> '->>>>>>>>         105.1ms      section:foo'

    """

    global _depth

    _depth += 1
    start_time = time.monotonic()
    try:
        yield
    finally:
        elapsed_time_s = time.monotonic() - start_time
        elapsed_time_ms = round(float(elapsed_time_s * 1000), 1)
        elapsed_time_ms_str = str(elapsed_time_ms).rjust(14)
        section_full_name = '|   ' * _depth + section_name
        print(f'->>>>>>>>{elapsed_time_ms_str}ms      {section_full_name}')

        _depth -= 1


def timeit_function(function_name: str):
    """
    Returns a function decorator for profiling code section execution time.

    :param function_name: function name to use in the output record.

    example: the code below outputs

    >>> import time
    >>> from ptimeit import timeit_function
    >>>
    >>>
    >>> @timeit_function('foo')
    >>> def foo():
    >>>     time.sleep(0.1)
    >>>
    >>>
    >>> foo()
    >>>
    >>> '->>>>>>>>         102.7ms      foo()'

    """

    def decorator(func):
        @functools.wraps(func)
        def timeit_wrapper(*args, **kwargs):
            with timeit_section(f'{function_name}()'):
                return func(*args, **kwargs)

        return timeit_wrapper

    return decorator
