.. _generate_docs:

Generate The Documentation
--------------------------

This project uses ``sphinx`` & ``doxygen`` in order to generate it's documentation & hosts them on `Github Pages <https://roeey777.github.io/modern-cmake/>`_.
There are a few steps for generating & hosting documentation.

Automatic generation of documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning::

   .. deprecated:: 58248f69ad8816a7dd4bb3b89089594196befebc

      This method of publishing the documentation to `Github Pages <https://roeey777.github.io/modern-cmake/>`_ is out-of-date.
      Please use ``publish-docs.sh`` script instead.

   At first you should verify that you are using the ``modern-cmake`` environment.

   .. code-block:: bash

      conda activate modern-cmake

   If not installed please refer to the installation page.

   Afterwards you should execute the following commands:

   .. code-block:: bash

      cmake -S . -B build/docs -Wdev -Werror=dev -DENABLE_DOCS=ON -DENABLE_TESTING=OFF
      cmake --build build/docs --target Sphinx
      mkdir -p docs/build
      cp -r build/docs/docs/docs/sphinx/* docs/build/

   And now your documentation is built!
   You can inspect it as follows:

   .. code-block:: bash

      firefox build/docs/docs/docs/sphinx/index.html

   Or via:

   .. code-block:: bash

      firefox docs/build/index.html


   **Publishing the Documentation to Github Pages**

   The directory ``docs/build/`` needs to be added to git worktree for the branch ``gh-pages``,
   which is the default branch `Github <https://github.com>`_ uses for the pages feature.
   All that is left to do is as follows:

   .. code-block:: bash

      cd docs/build/

   Now you need to verify that your working on ``gh-pages`` branch, this can be validated as follows:

   .. code-block:: bash

      # from docs/build/
      git branch

   After this verification we can add all the new documentation.

   .. code-block:: bash

      # from repo top directory
      git worktree add -f docs/build gh-pages
      cd docs/build

      # from docs/build/
      git add -A .
      git commit -sm "update documentation"
      git push origin gh-pages

   And Your'e Done!


.. note::

   Here is the **prefered** way of publishing the documentation.

Please execute the ``publish-docs.sh`` script like this:

.. code-block:: bash

   ./scripts/publish-docs.sh

The script will invoke all the right commands for working with ``git worktree`` properly and will
create a new commit on branch ``gh-pages``, then it will push the new commit onto the remote ``origin``.
The remote can be overridden as follows:

.. code-block:: bash

   ./scripts/publish-docs.sh other-remote-name

All-n`-all you can use read more by executing:

.. code-block:: bash

   ./scripts/publish-docs.sh --help

And Your'e Done!

