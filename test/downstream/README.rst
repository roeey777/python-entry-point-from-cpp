Downstream Test
===============

This is sort of "integration" test since it verifies a combined set of elements, they are:

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

#. Build the loader executable

.. code-block:: bash

   cmake -S test/downstream -B build/downstream  -Wdev -Werror=dev -DCMAKE_FIND_ROOT_PATH=$CONDA_PREFIX
   cmake --build build/downstream

#. Execute the loader

.. code-block:: bash

   ./build/downstream/downstream

