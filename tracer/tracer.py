"""
tracer.tracer
-------------
author: bczsalba


This submodule provides all the methods for the module.
"""

from __future__ import annotations

import inspect
import pytermgui as ptg


TEMPLATE = """
Attribute [120 italic]"{attribute}"[/] of [183]{cls!r}[/] changing to[210 bold] {new}[/]!
Set by: [104]{filename}[/]:[222]{lineno}[/]
Code: [245 italic]{code}[/]
Press Y to accept changes, D to drop changes and Q to quit."""


def get_caller(depth=1) -> tuple[str, object | None, int, str]:
    """Get caller frame"""

    frame = inspect.currentframe()
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
):
    """Decorator to trace changes of an attribute

    Usage:
        >>> from tracer import trace
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

    def decorator(cls: object):
        sunder = "_" + attribute

        def default_getter(attr: str) -> Any:
            return getattr(cls, sunder)

        def default_setter(_: object, new: Any) -> None:
            filename, lineno, funcname, code, _ = get_caller()
            prop = getattr(cls, attribute)
            current = prop.fget(attribute)

            print(
                ptg.markup.parse(
                    TEMPLATE.format(
                        cls=cls,
                        attribute=attribute,
                        new=new,
                        filename=filename,
                        lineno=lineno,
                        code=ascii(code[0].strip()),
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
