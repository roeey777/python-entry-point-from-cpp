.. _entry_point:

Entry Points in Python
======================

The first paragraph taken from `python's specifications for entry-points <https://packaging.python.org/en/latest/specifications/entry-points/>`_.

..

   Entry points are a mechanism for an installed distribution to advertise components it provides to be discovered and used by other code. For example:

   #. Distributions can specify console_scripts entry points, each referring to a function.
      When pip (or another console_scripts aware installer) installs the distribution, it will create a command-line wrapper for each entry point.

   #. Applications can use entry points to load plugins; e.g. ``Pygments`` (a syntax highlighting tool) can use additional lexers and styles from separately installed packages.
      For more about this, see `Creating and discovering plugins <https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/>`_.

   The entry point file format was originally developed to allow packages built with ``setuptools`` to provide integration point metadata that would be read at runtime with ``importlib.metadata``.
   It is now defined as a ``PyPA`` interoperability specification in order to allow build tools other than ``setuptools`` to publish ``importlib.metadata`` compatible entry point metadata, and runtime libraries other than ``importlib.metadata`` to portably read published entry point metadata (potentially with different caching and conflict resolution strategies).

Please refer to `python's specifications for entry-points <https://packaging.python.org/en/latest/specifications/entry-points/>`_ for information about entry-points in ``python``.


Example Package with Entry Point
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is a very briefed walk-through of the adding an entry point in a python package.

First of all is the (minimal) required structure of the package, the structure should contain (at least) the following files:

#. ``pyproject.toml`` or ``setup.cfg`` or ``setup.py`` (can be a combination of those as well).
   In this example we use ``pyproject.toml``.

#. The actual code of the package.
   In this example it's ``example.py`` & ``__init__.py``.

.. code-block:: text

   example-package/
   ├── pyproject.toml
   └── src
       └── example
           ├── example.py
           └── __init__.py

The "magic" happens in the ``pyproject.toml``, which would contain the following section:

.. code-block:: toml

   [project.entry-points."example.group"]
   hello = "example.example:hello"

This section in the ``pyproject.toml`` will install an entry-point **named** ``hello`` in a **group** named ``example.group``.
This entry-point is a pointer to a function called ``hello`` which is imported as follows:

.. code-block:: python

   from exmaple.example import hello

(At least is an equivalent to this ``import`` statement).
