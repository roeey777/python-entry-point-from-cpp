"""
An example of a package with a plugin registered via an entry-point.
"""

from poc.typing import Plugin


def hello(raw: bytes) -> bytes:
    """
    An example of a plugin, in this example there are some prints and
    the input is returned in reversed order.

    :param raw: the input of the plugin, raw bytes which can be de-serialized.
    :return: reversed order of the input bytes.
    """
    print(f"Got {len(raw)} bytes!")
    print(f"They are: {raw!r}")  # adding the !r is for decoding the raw bytes as str
    return raw[::-1]


typed_plugin: Plugin = hello
