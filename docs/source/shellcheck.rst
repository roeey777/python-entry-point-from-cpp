.. _shellcheck:

ShellCheck
==========

ShellCheck, a static analysis tool for shell scripts.
The goals of ShellCheck are:

* To point out and clarify typical beginner's syntax issues that cause a shell to give cryptic error messages.
* To point out and clarify typical intermediate level semantic problems that cause a shell to behave strangely and counter-intuitively.
* To point out subtle caveats, corner cases and pitfalls that may cause an advanced user's otherwise working script to fail under future circumstances.

See the `gallery of bad code <https://github.com/koalaman/shellcheck/blob/master/README.md#user-content-gallery-of-bad-code>`_ for examples of what ``shellcheck`` can help you identify!

Installation of ``shellcheck``:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``shellcheck`` can be installed via ``conda-forge`` like this:

.. code-block:: bash

   conda install -c conda-forge shellcheck


Usage of ``shellcheck``:
~~~~~~~~~~~~~~~~~~~~~~~~

In this project we use ``shellcheck`` as follows:

.. code-block:: bash

   shellcheck --shell=bash <path to file>

