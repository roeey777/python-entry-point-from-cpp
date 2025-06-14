.. _iwyu:

iwyu (Include-What-You-Use)
===========================

Include-What-You-Use is a tool for use with ``clang`` to analyze ``#includes`` in ``C`` and ``C++`` source files.

"Include what you use" means this: for every symbol (type, function variable, or macro) that you use in ``foo.cc``, either ``foo.cc`` or ``foo.h`` should ``#include`` a ``.h`` file that exports the declaration of that symbol.
The include-what-you-use tool is a program that can be built with the ``clang`` libraries in order to analyze ``#include`` directives of source files to find include-what-you-use violations, and suggest fixes for them.
The main goal of include-what-you-use is to remove superfluous ``#include`` directives.
It does this both by figuring out what ``#include`` directives are not actually needed for this file (for both ``.cc`` and ``.h`` files), and replacing ``#include`` directives with forward-declares when possible.

.. note::

   When referring to ``foo.cc`` the meaning is for a source file, the suffix can be different like using ``.cpp``.
   When referring to ``foo.cc`` the meaning is for a header file, the suffix can be different like using ``.hpp`` or ``.hh``.

.. note::

   In this project we use ``iwyu`` as an abbreviation/shorthand for Include-What-You-Use and henceforth we will refer
   to this tool as ``iwyu``.


Installation of ``iwyu``:
~~~~~~~~~~~~~~~~~~~~~~~~~~

``iwyu`` can be installed via ``conda-forge`` like this:

.. code-block:: bash

   conda install -c conda-forge include-what-you-use

Include-What-You-Use can be invoked manually, however in this project it's being done via ``cmake``.
It can be done by setting the ``ENABLE_IWYU`` option to ``ON`` (default is ``OFF``).
For example you can use it like this:

.. code-block:: bash

   cmake -S . -B bld -Wdev -Werror=dev -DCMAKE_FIND_ROOT_PATH=$CONDA_PREFIX -DENABLE_IWYU=ON
   cmake --build bld --target Poc

This will create & use a build directory called ``bld`` and ``cmake`` will invoke ``iwyu`` on each ``C++`` source file.

