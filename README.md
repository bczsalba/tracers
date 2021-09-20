<p align="center">
  <img src="https://raw.githubusercontent.com/bczsalba/tracer/master/assets/title.png"></img>
</p>

> Easily debug and trace attribute changes in your Python classes

[![PyPI version](https://raw.githubusercontent.com/bczsalba/tracer/master/assets/version.svg)](https://pypi.org/project/tracer)
[![Pylint quality](https://raw.githubusercontent.com/bczsalba/tracer/master/assets/quality.svg)](https://github.com/bczsalba/tracer/blob/master/utils/create_badge.py)

Usage
-----

<a href="https://raw.githubusercontent.com/bczsalba/tracer/master/assets/tracer.webp">
  <img src="https://raw.githubusercontent.com/bczsalba/tracer/master/assets/screenshot.png"></img>
</a>


To use this module, simply import `trace` from it, and decorate your chosen class:

```python
from tracer import trace

@trace("test")
class MyClass:
   def __init__(self) -> None:
       self.test = 0
   
   ...
```

You can set custom setter and getter methods for your trace, practically allowing you to subcribe to read/write events of an attribute.

```python
from typing import Any
from tracer import trace

def handle_get(obj: object) -> Any:
    """Get variable"""
    
    # Note the namespace-based reference to `attr`
    print(f"Trying to get {attr} from {obj}")
    return getattr(obj, "_" + attr)
    
def handle_set(obj: object, new: Any) -> None:
    """Set variable"""
    
    print(f"Setting {attr} for {obj} from {getattr(obj, attr)} -> {new}")
    setattr(obj, "_" + attr, new)
    
attr = "test"

@trace(attr, getter=handle_get, setter=handle_set)
class MyClass:
   def __init__(self) -> None:
       self.test = 0

```

Please note that these methods do **NOT** get a reference to `attr`. This is a quirk of properties, but you can work around it using namespace-based referencing, like above.

Inner workings
--------------

This module under the hood is just an easy way to assign properties to a class.

When decorated with `trace("attr")`, a class has its attribute `attr` replaced with a property. The default setter and getter of this property access the "_attr" attribute, as the property takes up "attr".

Essentially, what it becomes is this:
```python3
class MyClass:
    @property
    def attr(self) -> Any:
        return self._attr
        
    @attr.setter
    def attr(self, new: str) -> None:
        # Display current trace
        # Take input, quit or dismiss if chosen
        
        self._attr = new
```

Why use this over manually defining properties?
-----------------------------------------------

While defining the properties manually *is* doable, this module comes in really handy for debugging.

Imagine having a pretty complex hierarchy of class-inheritance and objects all relating to eachother (like it happens in [pytermgui](https://github.com/bczsalba/pytermgui)).
It often happens that there is a certain attribute that isn't quite behaving how it is supposed to. While you *could* define these properties yourself, being able to import `trace` and plop it on top of a class is really efficient for debugging.

It also looks much nicer!
