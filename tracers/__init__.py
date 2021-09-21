"""
tracers
-------
author: bczsalba


This module provides an easy way to interactively trace
instance attribute changes for debugging purposes.

Simply use the `trace` decorator on your chosen class and step
through each change while choosing between accepting changes,
dropping them or quitting altogether.

Usage:
    >>> from tracers import trace
    >>> @trace("my_attr")
    >>> class MyClass:
    >>>    my_attr = 0
    >>>
    >>> MyClass().my_attr = 1
    Attribute "my_attr" of <MyClass> changing to 1!
    Set by: __main__:4
    Code: "MyClass().my_attr = 1"
    Press Y to accept changes, D to drop changes and Q to quit.
    >>> Q
"""

from .tracers import trace, get_caller
