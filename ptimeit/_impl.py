import functools
import time
from contextlib import contextmanager
from typing import Callable


_depth = -1


@contextmanager
def timeit_section(
    section_name: str,
    should_print: Callable[[float], bool] = lambda t: True,
    additional_data_to_print: str = None
):
    """
    Returns a context manager for profiling code section execution time.

    :param section_name: section name to use in the output record.
    :param should_print: a function to determine whether to print the timings.
    :param additional_data_to_print: allows for passing in the additional data
                                     to print with the timings.

    example: the code below outputs

    >>> import time
    >>> from ptimeit import timeit_section
    >>>
    >>> with timeit_section('bar'):
    >>>     time.sleep(0.1)
    >>>
    >>> '->>>>>>>>         105.1ms      bar'

    """

    global _depth

    _depth += 1
    start_time = time.monotonic()
    try:
        yield
    finally:
        elapsed_time_s = time.monotonic() - start_time
        elapsed_time_ms = round(float(elapsed_time_s * 1000), 1)
        if should_print is None or should_print(elapsed_time_ms):
            elapsed_time_ms_str = str(elapsed_time_ms).rjust(14)
            offset = '|   ' * _depth
            section_full_name = offset + section_name
            print(f'->>>>>>>>{elapsed_time_ms_str}ms      {section_full_name}')
            if additional_data_to_print:
                print(f'->>>>>>>>>>>>>>>>>>>>>>>>      {offset}'
                f'Additional data: {additional_data_to_print}'
            )

        _depth -= 1


def timeit_function(
    function_name: str,
    should_print: Callable[[float], bool] = lambda t: True,
    additional_data_to_print: str = None
):
    """
    Returns a function decorator for profiling code section execution time.

    :param function_name: function name to use in the output record.
    :param should_print: a function to determine whether to print the timings.
    :param additional_data_to_print: allows for passing in the additional data
                                     to print with the timings.

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
            with timeit_section(f'{function_name}()', should_print, additional_data_to_print):
                return func(*args, **kwargs)

        return timeit_wrapper

    return decorator
