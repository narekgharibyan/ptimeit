import mock
import pytest

from ptimeit import timeit_function, timeit_section


@mock.patch('time.monotonic', mock.MagicMock(side_effect=[0, 0.5]))
def test_single_section(capsys):
    with timeit_section('single_section'):
        pass

    captured = capsys.readouterr()
    assert captured.out == '->>>>>>>>         500.0ms      single_section\n'


@mock.patch('time.monotonic', mock.MagicMock(side_effect=[0, 0.5, 1, 2]))
def test_double_section(capsys):
    with timeit_section('section_1'):
        pass
    with timeit_section('section_2'):
        pass

    captured = capsys.readouterr()
    assert captured.out == '->>>>>>>>         500.0ms      section_1\n' \
                           '->>>>>>>>        1000.0ms      section_2\n'


@mock.patch('time.monotonic', mock.MagicMock(side_effect=[0, 0.5, 1, 2.2]))
def test_nested_sections(capsys):
    with timeit_section('section_outer'):
        with timeit_section('section_inner'):
            pass

    captured = capsys.readouterr()
    assert captured.out == '->>>>>>>>         500.0ms      |   section_inner\n' \
                           '->>>>>>>>        2200.0ms      section_outer\n'


@mock.patch('time.monotonic', mock.MagicMock(side_effect=[0, 0.5, 0.7, 0.7702, 1, 2.2]))
def test_3_nested_sections(capsys):
    with timeit_section('section_outer'):
        with timeit_section('section_middle'):
            with timeit_section('section_inner'):
                pass

    captured = capsys.readouterr()
    assert captured.out == '->>>>>>>>          70.2ms      |   |   section_inner\n' \
                           '->>>>>>>>         500.0ms      |   section_middle\n' \
                           '->>>>>>>>        2200.0ms      section_outer\n'


@mock.patch('time.monotonic', mock.MagicMock(side_effect=[0, 0.5, 1, 2]))
def test_section_rising_exception(capsys):
    with pytest.raises(Exception):
        with timeit_section('section_1'):
            raise Exception('')
    with timeit_section('section_2'):
        pass

    captured = capsys.readouterr()
    assert captured.out == '->>>>>>>>         500.0ms      section_1\n' \
                           '->>>>>>>>        1000.0ms      section_2\n'


@mock.patch('time.monotonic', mock.MagicMock(side_effect=[0, 0.5, 1.1, 2.8]))
def test_nested_section_rising_exception(capsys):
    with pytest.raises(Exception):
        with timeit_section('section_outer'):
            with timeit_section('section_inner'):
                raise Exception('')

    captured = capsys.readouterr()
    assert captured.out == '->>>>>>>>         600.0ms      |   section_inner\n' \
                           '->>>>>>>>        2800.0ms      section_outer\n'


@mock.patch('time.monotonic', mock.MagicMock(side_effect=[0, 0.5]))
def test_single_function(capsys):
    @timeit_function('single_function')
    def single_function():
        pass

    single_function()

    captured = capsys.readouterr()
    assert captured.out == '->>>>>>>>         500.0ms      single_function()\n'


@mock.patch('time.monotonic', mock.MagicMock(side_effect=[0, 0.5, 2, 3.5]))
def test_double_function_call(capsys):
    @timeit_function('function')
    def function():
        pass

    function()
    function()

    captured = capsys.readouterr()
    assert captured.out == '->>>>>>>>         500.0ms      function()\n' \
                           '->>>>>>>>        1500.0ms      function()\n'


@mock.patch('time.monotonic', mock.MagicMock(side_effect=[0, 0.5, 2, 3.5]))
def test_nested_functions(capsys):
    @timeit_function('function_inner')
    def function_inner():
        pass

    @timeit_function('function_outer')
    def function_outer():
        function_inner()

    function_outer()

    captured = capsys.readouterr()
    assert captured.out == '->>>>>>>>        1500.0ms      |   function_inner()\n' \
                           '->>>>>>>>        3500.0ms      function_outer()\n'


@mock.patch('time.monotonic', mock.MagicMock(side_effect=[0, 0.5, 2, 2.0101, 2.2503, 3.5]))
def test_3_nested_functions(capsys):
    @timeit_function('function_inner')
    def function_inner():
        pass

    @timeit_function('function_middle')
    def function_middle():
        function_inner()

    @timeit_function('function_outer')
    def function_outer():
        function_middle()

    function_outer()

    captured = capsys.readouterr()
    assert captured.out == '->>>>>>>>          10.1ms      |   |   function_inner()\n' \
                           '->>>>>>>>        1750.3ms      |   function_middle()\n' \
                           '->>>>>>>>        3500.0ms      function_outer()\n'


@mock.patch('time.monotonic', mock.MagicMock(side_effect=[
    0, 0.1, 0.234, 0.5, 2, 2.001, 2.001, 2.05, 2.07, 2.1101, 2.2503, 3.5]
))
def test_3_nested_functions_with_sections_rising_exception(capsys):
    @timeit_function('function_inner')
    def function_inner():
        with timeit_section('function_inner:section_1'):
            pass
        with timeit_section('function_inner:section_2'):
            raise Exception('')

    @timeit_function('function_middle')
    def function_middle():
        function_inner()

    @timeit_function('function_outer')
    def function_outer():
        with timeit_section('function_outer:section'):
            pass
        function_middle()

    with pytest.raises(Exception):
        function_outer()

    captured = capsys.readouterr()
    assert captured.out == '->>>>>>>>         134.0ms      |   function_outer:section\n' \
                           '->>>>>>>>           0.0ms      |   |   |   function_inner:section_1\n' \
                           '->>>>>>>>          20.0ms      |   |   |   function_inner:section_2\n' \
                           '->>>>>>>>         110.1ms      |   |   function_inner()\n' \
                           '->>>>>>>>        1750.3ms      |   function_middle()\n' \
                           '->>>>>>>>        3500.0ms      function_outer()\n'


@mock.patch('time.monotonic', mock.MagicMock(side_effect=[0, 0.5]))
def test_section_extra_data(capsys):
    with timeit_section('section', extra_data_to_print="Extra, extra! Read all about it!"):
        pass

    expected = '->>>>>>>>         500.0ms      section - Extra, extra! Read all about it!\n'
    captured = capsys.readouterr()
    assert captured.out == expected


@mock.patch('time.monotonic', mock.MagicMock(side_effect=[0, 0.5]))
def test_function_extra_data(capsys):
    @timeit_function('function', extra_data_to_print="Extra, extra! Read all about it!")
    def single_function():
        pass

    single_function()

    expected = '->>>>>>>>         500.0ms      function() - Extra, extra! Read all about it!\n'
    captured = capsys.readouterr()
    assert captured.out == expected


@mock.patch('time.monotonic', mock.MagicMock(side_effect=[0, 0.2, 0, 0.5, 0, 1, 0, 2, 0, 0.7]))
def test_function_condition_time(capsys):
    @timeit_function('function', condition=lambda t: t > 750)
    def single_function():
        pass

    single_function()  # 200ms
    single_function()  # 500ms
    single_function()  # 1000ms
    single_function()  # 2000ms
    single_function()  # 700ms

    expected = '->>>>>>>>        1000.0ms      function()\n' \
               '->>>>>>>>        2000.0ms      function()\n'
    captured = capsys.readouterr()
    assert captured.out == expected


@pytest.mark.parametrize(
    'func, expected',
    (
        (lambda t: True, '->>>>>>>>         500.0ms      function()\n'),
        (lambda t: False, ''),
        (lambda t: t > 100, '->>>>>>>>         500.0ms      function()\n'),
        (lambda t: t > 1000, ''),
        (None, '->>>>>>>>         500.0ms      function()\n'),
    )
)
@mock.patch('time.monotonic', mock.MagicMock(side_effect=[0, 0.5, 0, 0.5, 0, 0.5, 0, 0.5, 0, 0.5]))
def test_function_condition_lambda(func, expected, capsys):
    @timeit_function('function', condition=func)
    def single_function():
        pass

    single_function()  # 500ms

    captured = capsys.readouterr()
    assert captured.out == expected
