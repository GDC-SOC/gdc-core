.. _coding-standards:

****************
Coding Standards
****************

The purpose of the page is to describe the standards that are expected of all the code in this repository.
All developers should read and abide by the following standards.
Code which does not follow these standards closely will generally not be accepted.

We try to closely follow the coding style and conventions proposed by `Astropy <https://docs.astropy.org/en/stable/development/codeguide.html#coding-style-conventions>`_.

Language Standard
=================

* All code must be compatible with Python 3.7 and later.

* The new Python 3 formatting style should be used (i.e.
  ``"{0:s}".format("spam")`` instead of ``"%s" % "spam"``).

Coding Style/Conventions
========================

* The code will follow the standard `PEP8 Style Guide for Python Code <https://www.python.org/dev/peps/pep-0008/>`_.
  In particular, this includes using only 4 spaces for indentation, and never tabs.

* **Follow the existing coding style** within a file and avoid making changes that are purely stylistic.
  Please try to maintain the style when adding or modifying code.

* Following PEP8's recommendation, absolute imports are to be used in general.
  We allow relative imports within a module to avoid circular import chains.

* The ``import numpy as np``, ``import matplotlib as mpl``, and ``import matplotlib.pyplot as plt`` naming conventions should be used wherever relevant.
  ``from packagename import *`` should never be used (except in ``__init__.py``)

* Classes should either use direct variable access, or Python's property mechanism for setting object instance variables.

* Classes should use the builtin `super` function when making calls to methods in their super-class(es) unless there are specific reasons not to.
  `super` should be used consistently in all subclasses since it does not work otherwise.

* Multiple inheritance should be avoided in general without good reason.

* ``__init__.py`` files for modules should not contain any significant implementation code. ``__init__.py`` can contain docstrings and code for organizing the module layout.


Private code
============

It is often useful to designate code as private, which means it is not part of the user facing API, only used internally by sunpy, and can be modified without a deprecation period.
Any classes, functions, or variables that are private should either:

- Have an underscore as the first character of their name, e.g., ``_my_private_function``.
- If you want to do that to entire set of functions in a file, name the file with a underscore as the first character, e.g., ``_my_private_file.py``.

Utilities
=========

Within this reposiotory, it might be useful to have a set of utility classes or functions that are used by internally to help with certain tasks or to provide a certain level of abstraction.
These should be placed either:

- ``.{subpackage}.utils.py``, if it is only used within that sub-package.
- ``.util`` if it is used across multiple sub-packages.

These can be private (see section above) or public.
The decision is up to the developer, but if these might be useful for other modules, they should be made public.
These utils may be taken up by the core repository if they are generally useful for other instrument teams.

Formatting
==========

We enforce a minimum level of code style with our continuous intergration.
This runs a tool called `pre-commit <https://pre-commit.com/>`__.

The settings and tools we use for the pre-commit can be found in the file :file:`.pre-commit-config.yaml` at the root of the sunpy git repository.
Some of the checks are:
* Checks (but doesn't fix) various PEP8 issues with flake8.
* Sort all imports in any Python files with isort.
* Remove any unused variables or imports with autoflake.

We suggest you use "tox" (which is used to run the sunpy test suite) to run these tools without having to setup anything within your own Python virtual environment::

    $ tox -e codestyle

This will inform you of what checks failed and why, and what changes (if any) the command has made to your code.

If you want to setup the pre-commit locally, you can do the following::

    $ pip install pre-commit

Now you can do::

    $ pre-commit run --all-files

which will run the tools on all files in the sunpy git repository.
The pre-commit tools can change some of the files, but in other cases it will report problems that require manual correction.
If the pre-commit tool changes any files, they will show up as new changes that will need to be committed.

Automate
--------

Instead of running the pre-commit command each time you can install the git hook::

    $ pre-commit install

which installs a command to :file:`.git/hooks/pre-commit` which will run these tools at the time you do ``git commit`` and means you don't have to run the first command each time.
We only suggest doing the install step if you are comfortable with git and the pre-commit tool.
If you are running inside of a Docker container but are managing git outside of it you will have to do this outside of the Docker.
This also means that you will have to install all of the dependencies on your local system.

By Hand
-------

Sometimes it is easier to run things by hand.
First, let's talk about Black. 
If you are using the docker container and VS Code it format be formatting your code automatically.
If you want to check if all of your files are compatible with Black run the following

    $ black --check folder_name

If you want it to go ahead and format the files remote `--check`.


Documentation and Testing
=========================

* American English is the default language for all documentation strings and inline commands.
  Variables names should also be based on English words.

* Documentation strings must be present for all public classes/methods/functions, and must follow the form outlined in the :ref:`docs_guidelines` page.
  Additionally, examples or tutorials in the package documentation are strongly recommended.

* Write usage examples in the docstrings of all classes and functions whenever possible.
  These examples should be short and simple to reproduce–users should be able to copy them verbatim and run them.
  These examples should, whenever possible, be in the :ref:`doctests` format and will be executed as part of the test suite.

* Unit tests should be provided for as many public methods and functions as possible, and should adhere to the standards set in the :ref:`testing` document.

Data and Configuration
======================

* We store test data in ``./data/test`` as long as it is less than about 100 kB.

* All persistent configuration should use the :ref:`config` mechanism.
  Such configuration items should be placed at the top of the module or package that makes use of them, and supply a description sufficient for users to understand what the setting
  changes.

Standard output, warnings, and errors
=====================================

The built-in ``print(...)`` function should only be used for output that is explicitly requested by the user, for example ``print_header(...)`` or ``list_catalogs(...)``.
Any other standard output, warnings, and errors should follow these rules:

* For errors/exceptions, one should always use ``raise`` with one of the built-in exception classes, or a custom exception class (e.g. ValueError, TypeError).
  The nondescript ``Exception`` class should be avoided as much as possible, in favor of more specific exceptions (`IOError`, `ValueError`, etc.).

* For warnings, use the appropriate custom warning classes (e.g. `hermes_core.util.exceptions.HERMESWarning`, `hermes_core.util.exceptions.HERMESUserWarning`) to enable them to be captured by the logging system.

* For debug messages, use the logging system `log.debug()` with a descriptive message.
  Remember that users may access those messages as well.

Including C Code
================

* C extensions are only allowed when they provide a significant performance enhancement over pure Python, or a robust C library already exists to provided the needed functionality.

* The use of `Cython`_ is strongly recommended for C extensions.

* If a C extension has a dependency on an external C library, the source code for the library should be bundled with sunpy, provided the license for the C library is compatible with the sunpy license.
  Additionally, the package must be compatible with using a system-installed library in place of the library included in sunpy.

* In cases where C extensions are needed but `Cython`_ cannot be used, the `PEP 7 Style Guide for C Code <https://www.python.org/dev/peps/pep-0007/>`_ is recommended.

* C extensions (`Cython`_ or otherwise) should provide the necessary information for building the extension.

.. _Cython: https://cython.org/