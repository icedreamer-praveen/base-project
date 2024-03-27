import functools
import inspect
import logging
import os


def get_full_module_name(cls):
    """
    This function retrieves the full module name of a given class in Python.
    
    :param cls: The `cls` parameter in the `get_full_module_name` function is typically a class object
    for which you want to determine the full module name. This function uses the `inspect` module to get
    the module of the class and then calculates the full module name based on the file path of the
    module
    :return: The function `get_full_module_name(cls)` returns the full module name of the class `cls`.
    """
    module = inspect.getmodule(cls)
    module_file = module.__file__

    if module_file.endswith('.pyc'):
        module_file = module_file[:-1]

    current_directory = os.path.abspath(os.path.dirname(__file__))
    module_name = os.path.relpath(module_file, start=current_directory)
    module_name = os.path.splitext(module_name)[0].replace(os.path.sep, '.')

    return module_name


def log_methods(cls):
    """
    The `log_methods` function is a Python decorator that logs method calls within a class.
    
    :param cls: The `cls` parameter in the `log_methods` function is a class that you want to decorate
    with logging functionality. The function adds logging before and after each method call in the class
    :return: The `log_methods` function returns a decorated class that logs information before and after
    each method call.
    """
    module_name = get_full_module_name(cls)

    class DecoratedClass(cls):
        def __getattribute__(self, name):
            attr = super().__getattribute__(name)
            if callable(attr) and not name.startswith('_'):
                @functools.wraps(attr)
                def wrapper(*args, **kwargs):
                    logger = logging.getLogger(module_name)
                    logger.info(f" >> {name}")
                    result = attr(*args, **kwargs)
                    logger.info(f" << {name}")
                    return result
                return wrapper
            return attr
    return DecoratedClass


def log_functions(func):
    """
    The `log_functions` function is a decorator that logs the entry and exit of a wrapped function with
    the function name and module name.
    
    :param func: The `func` parameter in the `log_functions` function is a function object that will be
    passed as an argument to the `get_full_module_name` function. The `log_functions` function is a
    decorator that logs information before and after calling the decorated function
    :return: The `log_functions` function is returning a wrapped version of the input function `func`.
    This wrapped function logs information before and after calling the original function `func`.
    """
    module_name = get_full_module_name(func)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(module_name)
        logger.info(f" >> {func.__name__}")
        result = func(*args, **kwargs)
        logger.info(f" << {func.__name__}")
        return result

    return wrapper