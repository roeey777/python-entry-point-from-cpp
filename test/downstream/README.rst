.. _demo:

.. _downstream_test:

Demo (a.k.a Downstream Test)
============================

This demo is sort of "integration" test since it verifies a combined set of elements, and they are:

#. The ability of "downstream" installation of this library.
#. The ability to find & load entry-points.
#. The ability to invoke loaded entry-points.

The steps of the test are as follows:

#. Install the example package, which registers an entry-point to a group called "example.group"
#. Build the library.
#. Build the loader executable (linked against the library).
#. Execute the loader.
#. Expect to see the output of the pythonic entry-point.

Using the ``poc`` ``conda`` environment, all commands should be executed from the repo's top directory.
The test requires the following commands to be executed are:

#. Install the example package:

   .. code-block:: bash

      cd example-package && pip install . && cd -

#. Build & install the library

   .. code-block:: bash

      cmake -S . -B build/upstream  -Wdev -Werror=dev -DCMAKE_INSTALL_PREFIX=$CONDA_PREFIX -DCMAKE_FIND_ROOT_PATH=$CONDA_PREFIX -DENABLE_TESTING=OFF
      cmake --build build/upstream --target install

#. Build the demo (loader) executable

   .. code-block:: bash

      cmake -S test/downstream -B build/downstream  -Wdev -Werror=dev -DCMAKE_FIND_ROOT_PATH=$CONDA_PREFIX
      cmake --build build/downstream

#. Execute the demo (loader) executable

   .. code-block:: bash

      ./build/downstream/downstream

When the demo executable is running it will dynamically load entry-point group called ``"example.group"``.
In that group the demo will find 2 entry-points, one called ``hello`` and the other called ``42``.
Then the demo will *ignore* the ``hello`` entry-point since it's name isn't a valid name (not an unsigned number) and load the other entry-point (which has a valid name).

.. note::

   Both entry-points names are valid fron the viewpoint of ``python``, however in this library there is some "filterring" of entry-points based on thier names.
   A very crud filterring technique indeed, but it's still proves the point - the library is *able* to filter entry-points by name.

Afterwards the demo will invoke the loaded entry-point (which points to a function called ``hello`` in the ``example`` package) with ``b"asdf"`` as the input.
The expected output of the demo is the same as the expected output of calling ``hello(b"asdf")`` from the ``python`` interpreter (with some addional logging messages).
Here is how it suppose to look:

.. code-block:: text

   [2025-06-17 19:24:59.812] [info] loading plugins for group example.group
   [2025-06-17 19:24:59.841] [warning] Ignoring entry-point named "hello" since it's not an unsigned number!
   Got 4 bytes!
   They are: b'asdf'

