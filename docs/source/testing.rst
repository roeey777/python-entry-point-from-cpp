.. _testing:

.. _integration_tests:

Testing
=======

This library is a bit odd when it comes to testing since it's much harder to isolate & differentiate between units/components.
The reason boils down to the fact this library (written in ``C++``) is working with ``python``'s entry-points mechanism which requires multiple environments just for testing different edge cases.

Integration Tests
-----------------

In order to test this library a small testing program was written in ``C++`` with the help of the ``argparse`` `library <https://github.com/p-ranav/argparse>`_.
This small utility exposes the ``C++`` library as a command-line program which is then used by ``pytest`` for the testing itself.
The integration tests utilize `tox <https://tox.wiki/en/4.27.0/>`_ for an automated management of ``python`` virtual environments and simulates 2 environments scenarios:

#. An environment **without** entry-points registered to a specific group.
#. An environment **with** entry-points registered to a specific group.

Running the Integration Tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Running the integration tests is quite easy and it can be done as follows:

.. code-block:: bash

   # assume we're in the repo's top directory.
   tox

And if you want a bit more verbosity then use:

.. code-block:: bash

   # assume we're in the repo's top directory.
   tox -v

One can also run the integration tests without ``tox`` directly on ``conda``'s environment like this:

.. code-block:: bash

   # assume we're in the repo's top directory.
   cmake -S . -B build/integration-tests  -Wdev -Werror=dev -DCMAKE_INSTALL_PREFIX=$CONDA_PREFIX -DCMAKE_FIND_ROOT_PATH=$CONDA_PREFIX -DENABLE_TESTING=ON
   cmake --build build/integration-tests --target install
   pytest test/ --loader build/integration-tests/test/loader

.. note::

   Be sure to remember & verify that ``pytest`` is installed into ``conda``'s environment (when using ``tox`` that's not an issue since ``tox`` installs it for us).
   This can be verified like this:

   .. code-block:: bash

      pip list | grep pytest

      # or alternativly
      pip show pytest

   If ``pytest`` wasn't installed then you can run:

   .. code-block:: bash

      pip install pytest

