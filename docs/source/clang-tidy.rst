.. _clang-tidy:

clang-tidy
==========

``clang-tidy`` is a ``clang``-based ``C++`` “linter” tool. Its purpose is to provide an extensible framework for diagnosing and fixing typical programming errors, like style violations, interface misuse, or bugs that can be deduced via static analysis. ``clang-tidy`` is modular and provides a convenient interface for writing new checks.

For further explanation on ``clang-tidy`` please refer to it's `documentation <https://clang.llvm.org/extra/clang-tidy/>`_.

First of all, if you wish to use ``clang-tidy`` than you must install it first.
For instance, in ``conda-forge`` ``clang-tidy`` is packed within a recipe (package in ``conda``'s jargon) called ``clang-tools``.
Here is how to install ``clang-tidy`` using ``conda-forge``.

.. code-block:: bash

   conda install -c conda-forge clang-tools

.. warning::

   ``clang-tidy`` isn't compatible with ``GNU`` tools and libraries, i.e. it enforces the compiler to be ``clang``-based one.
   So in order for ``clang-tidy`` to **work properly** simply installing it **wouldn't be sufficient**.
   The **proper** installation of ``clang-tidy`` using ``conda-forge`` would be as follows:

   .. code-block:: bash

      conda install -c conda-forge clang-tools clang clangxx

   .. note::

      if you are using the ``conda`` environment ``poc`` managed from ``environment.yml`` then you are good to go since it's already being dealt with in that environment.


In addition ``clang-tidy`` is already a part of the ``poc`` ``conda`` environment (listed in ``environment.yml``).

In this project we invoke ``clang-tidy`` from within ``cmake`` itself, it can be done by setting the ``ENABLE_CLANG_TIDY`` option to ``ON`` (default is ``OFF``).
For example you can use it like this:

.. code-block:: bash

   cmake -S . -B bld -Wdev -Werror=dev -DCMAKE_FIND_ROOT_PATH=$CONDA_PREFIX -DENABLE_CLANG_TIDY=ON
   cmake --build bld --target Poc

This will create & use a build directory called ``bld`` and ``cmake`` will invoke ``clang-tidy`` on each ``C++`` source file.

``clang-tidy`` is highly configurable tool and it's current configuration can be found in a file called ``.clang-tidy``.

