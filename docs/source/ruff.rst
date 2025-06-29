.. _ruff:

ruff
====

Ruff is an extremely fast Python linter and code formatter, written in Rust.
Ruff is a drop-in parity with Flake8, isort, and Black.
Ruff aims to be orders of magnitude faster than alternative tools while integrating more functionality behind a single, common interface.
Ruff documentation can be found `here <https://docs.astral.sh/ruff/>`_.

``ruff`` can be used as a linter like this:

.. code-block:: bash

   ruff check .

It can also fix automatically some of the errors, like this:

.. code-block:: bash

   ruff check . --fix

In order to use ``ruff`` as a formatter one should run the following command:

.. code-block:: bash

   ruff format .

All-'n'-all ``ruff`` is super easy to use!

.. note::

   ``ruff`` is now used and invoked automatically by ``tox``.
   If you want to use ``ruff`` from ``tox`` then please use the following command:

   .. code-block:: bash

      tox -e ruff

