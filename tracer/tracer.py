"""
tracer.tracer
-------------
author: bczsalba


This submodule provides all the methods for the module.
"""

from __future__ import annotations

import inspect
from typing import Any, Callable

import pytermgui as ptg

# I'm not sure where this class is defined.
Traceback = Any


TEMPLATE = """
Attribute [code green]{attribute}[/] of [code cyan]{cls!r}[/] changing to [code red]{new}[/]!
Set by: [code blue]{filename}[/fg]:[yellow]{lineno}[/] in method [code]{funcname}[/code]
Code: [code]{code}[/code]
Press [bold green]Y[/] to accept changes, [bold yellow]D[/] to drop changes and\
 [bold red]Q[/] to quit."""


ptg.markup.alias("code", "@236 246")


def get_caller(depth: int = 1) -> Traceback:
    """Get caller frame"""

    # Find frame at index
    frame = inspect.currentframe()
    assert frame is not None

    if frame.f_back is None:
        return inspect.getframeinfo(frame)

    previous_frame = frame
    for _ in range(depth + 1):
        f_back = getattr(previous_frame, "f_back")
        if f_back is None:
            break

        previous_frame = f_back

    return inspect.getframeinfo(previous_frame)


def trace(
    attribute: str,
    getter: Callable[[str], Any] | None = None,
    setter: Callable[[object, Any], None] | None = None,
) -> Callable[[object], Any]:
    """Decorator to trace changes of an attribute

    Usage:
        >>> from tracer import trace
        >>> @trace("my_attr")
        >>> class MyClass:
        >>>    my_attr = 0
        >>>
        >>> MyClass().my_attr = 1
        Attribute "my_attr" of <MyClass> changing to 1!
        Set by: __main__:4 in __main__()
        Code: "MyClass().my_attr = 1"
        Press Y to accept changes, D to drop changes and Q to quit.
        >>> Q
    """

    def decorator(cls: object) -> object:
        sunder = "_" + attribute

        def default_getter(_: str) -> Any:
            """Get single-underscore attribute from `cls`"""

            return getattr(cls, sunder)

        def default_setter(_: object, new: Any) -> None:
            """Print current trace and offer choices with setting"""

            filename, lineno, funcname, code, _ = get_caller()

            print(
                ptg.markup.parse(
                    TEMPLATE.format(
                        cls=cls,
                        attribute=attribute,
                        new=new,
                        filename=filename,
                        funcname=funcname,
                        lineno=lineno,
                        code=code[0].strip(),
                    )
                )
            )

            inp = input(">>> ").lower()
            if inp == "y":
                setattr(cls, sunder, new)
                return

            if inp == "d":
                print("Dropping change.")
                return

            if inp == "q":
                raise SystemExit

        setattr(cls, sunder, getattr(cls, attribute, None))
        setattr(
            cls,
            attribute,
            property(
                fget=getter or default_getter,
                fset=setter or default_setter,
            ),
        )
        return cls

    return decorator
