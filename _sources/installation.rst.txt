.. _installation:

Installation
============

Currently this library can only be installed from the source (no ``.deb``/``rpm``/``conda``).

Here are the steps for installing this library:

.. code-block:: bash

   # use from the repo's top directory
   # assumes all dependency are available in the environment (for example using ``conda``)
   cmake -S . -B build/upstream  -Wdev -Werror=dev -DCMAKE_INSTALL_PREFIX=$CONDA_PREFIX -DCMAKE_FIND_ROOT_PATH=$CONDA_PREFIX -DENABLE_TESTING=OFF
   cmake --build build/upstream --target install

Installation of the Documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The installation of the documentation is optional and controlled via 2 conditions:

#. Setting the ``ENABLE_DOCS`` option to ``ON`` (default is ``ON``).
#. Building the ``Sphinx`` target before the ``install`` target.

Here are the steps for installing this library **with** the documentation:

.. code-block:: bash

   # use from the repo's top directory
   # assumes all dependency are available in the environment (for example using ``conda``)
   cmake -S . -B build/upstream  -Wdev -Werror=dev -DCMAKE_INSTALL_PREFIX=$CONDA_PREFIX -DCMAKE_FIND_ROOT_PATH=$CONDA_PREFIX -DENABLE_TESTING=OFF
   cmake --build build/upstream --target Sphinx
   cmake --build build/upstream --target install


.. note::

   Using the middle ``cmake`` command for specifically building the target ``Sphinx`` is a bit cumbersome
   and it can be solved by applying this patch:

   .. code-block:: diff

      From: Eyal Royee <eyalroyee@gmail.com>
      Subject: [PATCH] build & install sphinx by default

      Signed-off-by: Eyal Royee <eyalroyee@gmail.com>
      --- a/docs/CMakeLists.txt
      +++ b/docs/CMakeLists.txt
      @@ -38,7 +38,7 @@ set(SPHINX_MARKER_FILE ${CMAKE_CURRENT_BINARY_DIR}/sphinx_build_done.stamp)
       configure_file(${CMAKE_CURRENT_SOURCE_DIR}/source/conf.py.in
                   ${CMAKE_CURRENT_SOURCE_DIR}/source/conf.py)

      -add_custom_target(Sphinx
      +add_custom_target(Sphinx ALL
                         COMMAND
                         ${SPHINX_EXECUTABLE} -b html
                         ${SPHINX_SOURCE} ${SPHINX_BUILD}
      --
      2.43.0

   Patch files can be applied via ``git apply`` or the ``patch`` command like this:

   .. code-block:: bash

      # -p1 tells patch to strip the first component of the file path (e.g., a/src/file.py becomes src/file.py).
      patch -p1 < my-fix.patch

      git apply --check file.patch
      git apply file.patch

    Please note that with this patch the ``Sphinx`` target will be added to the default build target so that it will be run every time.
    (According to `cmake documentation about ALL in add_custom_target <https://cmake.org/cmake/help/latest/command/add_custom_target.html#command:add_custom_target>`_).

After applying the patch the library & documentation can built & installed like this:

.. code-block:: bash

   # use from the repo's top directory
   # assumes all dependency are available in the environment (for example using ``conda``)
   cmake -S . -B build/upstream  -Wdev -Werror=dev -DCMAKE_INSTALL_PREFIX=$CONDA_PREFIX -DCMAKE_FIND_ROOT_PATH=$CONDA_PREFIX -DENABLE_TESTING=OFF
   cmake --build build/upstream --target install

