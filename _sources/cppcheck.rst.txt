.. _cppcheck:

Cppcheck
========

``Cppcheck`` is a static analysis tool for ``C``/``C++`` code. It provides unique code analysis to detect bugs and focuses on detecting undefined behaviour and dangerous coding constructs.
The goal is to have very few false positives.
``Cppcheck`` is designed to be able to analyze your ``C``/``C++`` code even if it has non-standard syntax (common in embedded projects).
Cppcheck is available both as open-source and as Cppcheck Premium with extended functionality and support.
Please visit `Cppcheck's homepage <http://www.cppcheck.com/>`_ for more information and purchase options for the commercial version.

First of all, if you wish to use ``cppcheck`` than you must install it first, for instance with ``conda-forge`` it can be done like this:

.. code-block:: bash

   conda install -c conda-forge cppcheck

In addition ``cppcheck`` is already a part of the ``poc`` ``conda`` environment (listed in ``environment.yml``).

In this project we invoke ``cppcheck`` from within ``cmake`` itself, it can be done by setting the ``ENABLE_CPPCHECK`` option to ``ON`` (default is ``OFF``).
For example you can use it like this:

.. code-block:: bash

   cmake -S . -B bld -Wdev -Werror=dev -DCMAKE_FIND_ROOT_PATH=$CONDA_PREFIX -DENABLE_CPPCHECK=ON
   cmake --build bld --target Poc

This will create & use a build directory called ``bld`` and ``cmake`` will invoke ``cppcheck`` on each ``C++`` source file.

