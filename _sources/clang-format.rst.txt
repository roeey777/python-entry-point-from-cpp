.. _clang-format:

clang-format
============

``ClangFormat`` describes a set of tools that are built on top of ``LibFormat``. It can support your workflow in a variety of ways including a standalone tool and editor integrations.

For further explanation on ``clang-format`` please refer to it's `documentation <https://clang.llvm.org/docs/ClangFormat.html>`_.

First of all, if you wish to use ``clang-format`` than you must install it first.
For instance, in ``conda-forge`` ``clang-format`` is packed within a recipe (package in ``conda``'s jargon) called ``clang-tools``.
Here is how to install ``clang-format`` using ``conda-forge``.

.. code-block:: bash

   conda install -c conda-forge clang-tools

Using ``clang-format`` is fairly simple, and it can be done like this:

.. code-block:: bash

   find . -iname '*.h' -o -iname '*.cpp' -o -iname '*.hpp' | clang-format -i --files=/dev/stdin

