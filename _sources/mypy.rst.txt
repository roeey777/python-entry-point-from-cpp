.. _mypy:

Mypy
====

Mypy is an optional static type checker for Python that aims to combine the benefits of dynamic (or "duck") typing and static typing.
Mypy combines the expressive power and convenience of Python with a powerful type system and compile-time type checking.
Mypy type checks standard Python programs; run them using any Python VM with basically no runtime overhead.
tl;dr - ``mypy`` is static type checker for ``python`` code which utilizes type annotations.

It can be used as follows:

.. code-block:: bash

   mypy <directory> [<file> [<another file> [...]]]

In this project the ``example-package`` used during the downstream test is validated by ``mypy``
**and** it's plugin function annotations are verified due to the last line which is:

.. code-block:: python

   typed_plugin: Plugin = hello

Where the type hint ``Plugin`` is taken from the ``poc.typing`` which is a typing module installed by ``poc`` package via ``cmake``.
The validation of ``example-package`` is done by invoking ``mypy`` as follows:

.. code-block:: bash

   mypy example-package

