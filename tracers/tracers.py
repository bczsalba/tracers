"""
tracers.tracers
---------------
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
Attribute [code 173]{attribute}[/] of [code]{obj!r}[/] changing from [code 173]\
{current}[/] to [code 208]{new}[/]!
Set by: [code 208]{filename}[/fg]:[173]{lineno}[/] in method [code]{funcname}[/code]
Code: [code]{code}[/code]
Press [bold 208]Y[/] to accept changes, [bold 138]D[/] to drop changes and\
 [bold 210]Q[/] to quit."""


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
        >>> from tracers import trace
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

        def default_getter(obj: object) -> Any:
            """Get single-underscore attribute from `cls`"""

            return getattr(obj, sunder)

        def default_setter(obj: object, new: Any) -> None:
            """Print current trace and offer choices with setting"""

            filename, lineno, funcname, code, _ = get_caller()

            print(
                ptg.markup.parse(
                    TEMPLATE.format(
                        obj=obj,
                        attribute=attribute,
                        current=getattr(obj, sunder),
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
