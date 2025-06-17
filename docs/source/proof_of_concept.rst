.. _proof_of_concept:

Proof of Concept
================

In this repository, I've tried to take advantage of ``python``'s dynamic & powerful entry-points mechanism from within ``C++`` code!
The actual implementation is simply using ``pybind11`` in order to embed ``python`` code into ``C++`` rather than exposing ``C++`` functionality to ``python`` (which is the most common use-case of ``pybind11``).

Currently in ``src/`` there is only the loading functionality, not the usage of it.
It is implemented as a library, which is also exported properly via ``cmake``.
However in ``test/downstream/`` there is an executable which is linked against the library and demonstrates how to call a ``python``-inc entry-point from ``C++`` using this library.

The Embedded ``python`` Code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The embedded ``python`` code is thus (ideally):

.. code-block:: python

   from importlib import metadata
   from poc.typing import Plugin

   def load_by_group(group_name: str) -> dict[int, Plugin]:
       loaded: dict[int, Plugin] = {}

       entry_points: metadata.EntryPoints = metadata.entry_points()
       group_entries = entry_points.select(group=group_name)

       for entry_point in group_entries:
           try:
               number = int(entry_point.name);
           except ValueError:
               continue
           callback = entry_point.load()
           loaded[number] = callback

       return loaded

However it's much closer to this version:

.. code-block:: python

   from importlib import metadata

   def load_by_group(group_name: str) -> dict[int, object]:
       loaded: dict[int, object] = {}

       entry_points: metadata.EntryPoints = metadata.entry_points()
       group_entries = entry_points.select(group=group_name)

       for entry_point in group_entries:
           try:
               number = int(entry_point.name);
           except ValueError:
               continue
           obj = entry_point.load()
           loaded[number] = obj

       return loaded

This is due to ``python`` being a weakly-typed language, however there is a slightly hope for verifying the plugins signatures.
All a package has to do is to add the 2 following lines:

#. Import the correct type annotation for plugins:

.. _import_poc_typing:

.. code-block:: python

   from poc.typing import Plugin

#. Add a "casting" of the desired entry-point plugin function into a typed plugin like this:

.. code-block:: python

   # assuming that the plugin function is called foo.
   typed_plugin: Plugin = foo

#. Use ``mypy`` in order to verify the signature.

.. note::

   This requires 2 things:

   #. ``mypy`` should be installed in the environment.
   #. The ``poc`` library should be installed in the environment as well (so :ref:`importing from poc would work <import_poc_typing>`)

