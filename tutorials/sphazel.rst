.. _sphazel:

==============================
Build a Sphinx site with Bazel
==============================

.. _Sphinx: https://www.sphinx-doc.org
.. _Bazel: https://bazel.build
.. _minimal, reproducible example: https://stackoverflow.com/help/minimal-reproducible-example

This tutorial provides a `minimal, reproducible example`_ of building a
`Sphinx`_ site with `Bazel`_.

-----------------------
Set up a Sphinx project
-----------------------

#. Create a directory for your project:

   .. code-block:: console

      $ mkdir sphazel

#. Make the project directory your working directory:

   .. code-block:: console

      $ cd sphazel

#. Create ``conf.py`` and add the following content to it:

   .. code-block:: py

      project = 'sphazel'
      author = 'sphazel'
      copyright = f'2025, The sphazel authors'
      release = '0.0.1'
      exclude_patterns = [
          '.gitignore',
          'requirements.txt',
          'requirements.lock',
      ]
      pygments_style = 'sphinx'

#. Create ``index.rst`` and add the following content to it:

   .. code-block:: rst

      .. _sphazel:

      =======
      sphazel
      =======

      Hello, world!

-------------------------------
Set up third-party dependencies
-------------------------------

#. Create ``requirements.txt`` and add the following content to it:

   .. code-block:: text

      sphinx==8.1.3

#. Create a virtual environment:

   .. code-block:: console

      $ python3 -m venv venv

#. Activate the virtual environment.

   Bash:

   .. code-block:: console

      $ source venv/bin/activate

   fish:

   .. code-block:: console

      $ . venv/bin/activate.fish

#. Use the latest version of ``pip`` in the virtual environment:

   .. code-block:: console

      $ python3 -m pip install --upgrade pip

#. Install your third-party dependencies in the virtual environment:

   .. code-block:: console

      $ python3 -m pip install -r requirements.txt

#. Record your full list of dependencies in a lockfile:

   .. code-block:: console

      $ python3 -m pip freeze > requirements.lock

#. Deactivate your virtual environment:

   .. code-block:: console

      $ deactivate

#. Delete the virtual environment:

   .. code-block:: console

      $ rm -rf venv

------------
Set up Bazel
------------

#. Create ``MODULE.bazel`` and add the following content to it:

   .. code-block:: py

      bazel_dep(name = "rules_python", version = "1.2.0")

      pip = use_extension("@rules_python//python/extensions:pip.bzl", "pip")
      pip.parse(
          hub_name = "pypi",
          python_version = "3.12",
          requirements_lock = "//:requirements.lock",
      )
      use_repo(pip, "pypi")

#. Create ``BUILD.bazel`` and add the following content to it:

   .. code-block:: py

      load("@rules_python//sphinxdocs:sphinx.bzl", "sphinx_build_binary", "sphinx_docs")
      load("@rules_python//sphinxdocs:sphinx_docs_library.bzl", "sphinx_docs_library")

      sphinx_build_binary(
          name = "sphinx",
          deps = [
              "@pypi//sphinx",
          ]
      )

      sphinx_docs_library(
          name = "sources",
          srcs = [
              "index.rst",
          ],
      )

      sphinx_docs(
          name = "docs",
          config = "conf.py",
          formats = [
              "html",
          ],
          sphinx = ":sphinx",
          deps = [
              ":sources",
          ]
      )

#. Create ``.bazelversion`` and add the following content to it:

   .. code-block:: text

      8.1.1

---------------
Set up Bazelisk
---------------

#. Download Bazelisk:

   .. code-block:: console

      $ curl -L -O https://github.com/bazelbuild/bazelisk/releases/download/v1.25.0/bazelisk-linux-amd64

#. Make the file executable:

   .. code-block:: console

      $ chmod +x bazelisk-linux-amd64

--------------
Build the docs
--------------

#. Build the docs:

   .. code-block:: console

      $ ./bazelisk-linux-amd64 build //:docs

   Example of a successful build:

   .. code-block:: console

      $ ./bazelisk-linux-amd64 build //:docs

      INFO: Analyzed target //:docs (120 packages loaded, 6055 targets configured).
      INFO: Found 1 target...
      Target //:docs up-to-date:
        bazel-bin/docs/_build/html
      INFO: Elapsed time: 13.725s, Critical Path: 2.62s
      INFO: 8 processes: 7 internal, 1 linux-sandbox.
      INFO: Build completed successfully, 8 total actions

--------------------------
Inspect the generated HTML
--------------------------

#. Open

https://linux.die.net/man/1/xdg-open

------------------------
Locally preview the docs
------------------------

-----------------------
Check the code into Git
-----------------------

#. Create ``.gitignore`` and add the following content to it:

   .. code-block:: text

	    bazel-bin
	    bazel-out
	    bazel-sphazel
	    bazel-testlogs

#. Check in everything else:

   .. code-block:: console

      $ git add .

#. And commit:

   .. code-block:: console

      $ git commit -m 'Init'


