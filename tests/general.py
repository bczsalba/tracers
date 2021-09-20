from random import randint

from tracer import trace


@trace("test")
class TestClass:
    """A test to showcase the tracer module"""

    attr = 0

    def __init__(self) -> None:
        """Initialize object"""

        # Set attribute using dot syntax
        self.test = 0

        # Set attribute using setattr()
        setattr(self, "attr", 1)

        # Set attribute in a method
        self.change_attr()

    def change_attr(self) -> None:
        """Change attr to a different value"""

        self.attr = randint(0, 10)


if __name__ == "__main__":
    print(TestClass().attr)
