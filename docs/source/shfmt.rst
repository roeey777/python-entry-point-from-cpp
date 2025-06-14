.. _shfmt:

shfmt
=====

``shfmt`` is a simple, yet powerful, formatter for shell scripts.
It supports multiple shell dialects such as: ``POSIX`` Shell, ``Bash`` & ``mksh``.
``shfmt`` is also highly configurable and can format your code in several fashion & conventions, for example take a look at `Google's bash styling <https://google.github.io/styleguide/shell.xml>`_

Installation of ``shfmt``:
~~~~~~~~~~~~~~~~~~~~~~~~~~

``shfmt`` can be installed via ``conda-forge`` like this:

.. code-block:: bash

   conda install -c conda-forge go-shfmt


Usage of ``shfmt``:
~~~~~~~~~~~~~~~~~~~

In this project we use ``shfmt`` as follows:

.. code-block:: bash

   shfmt -i 4 -ci -sr --language-dialect bash <path to file>

In case you want ``shfmt`` to fix "inpace" than use it as follows:

.. code-block:: bash

   shfmt -i 4 -ci -sr --language-dialect bash -w <path to file>

