import functools
import time
from contextlib import contextmanager


_depth = -1


@contextmanager
def timeit_section(section_name):
    global _depth

    _depth += 1
    try:
        start_time = time.monotonic()
        yield

        elapsed_time_s = time.monotonic() - start_time
        elapsed_time_ms = round(elapsed_time_s * 1000, 1)
        elapsed_time_ms_str = str(elapsed_time_ms).rjust(14)
        section_full_name = '|   ' * _depth + section_name
        print(f'->>>>>>>>{elapsed_time_ms_str}ms      {section_full_name}')

    finally:
        _depth -= 1


def timeit_function(function_name):
    def decorator(func):
        @functools.wraps(func)
        def timeit_wrapper(*args, **kwargs):
            with timeit_section(f'{function_name}()'):
                return func(*args, **kwargs)

        return timeit_wrapper

    return decorator
