"""This is a module docstring."""


def greeting(repeat: int, name: str = "Mike") -> str:
    """A restructureText docstring.

    :param repeat: Repeat the name this number of times.
    :type repeat: int
    :param name: Name of the person, defaults to "Mike"
    :type name: str, optional
    :return: Formatted greeting.
    :rtype: str
    """

    return f"Hello {name * repeat}"


class Person:
    """A Person class."""

    def __init__(self, name):
        self.name = name

    def greeting(self) -> str:
        """Creates a greeting.

        :return: A formatted greeting
        :rtype: str
        """

        return f"Hello, {self.name}"
