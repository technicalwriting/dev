====================
technicalwriting.dev
====================

A blog about technical writing by `Kayce Basques <https://kayce.basqu.es>`_.

.. _a11y:

-------------
Accessibility
-------------

* :ref:`skip-to-main-content`. A feature that makes your docs site much more
  user-friendly to people who don't use mouses and only navigate with
  keyboards.

-------------
Build systems
-------------

* :ref:`bazel`. Development log of my journey to migrate a docs site from a
  GN-based build system to a Bazel-based one.

.. _dac:

------------------
Docs-as-Code (DaC)
------------------

* :ref:`link-text-automation`. A killer feature from Sphinx that more docs systems
  should adopt.
* :ref:`verbatim-wrangling`. My struggles to get a plaintext diagram rendering correctly
  on a docs site that uses Sphinx, Breathe, and Doxygen.

.. _dad:

------------------
Docs-as-Data (DaD)
------------------

* :ref:`intertwingularity`. I’m building a web crawler so that I can track how pages in my docs
  site link to each other and to the outside web more broadly. If a lot of my docs pages link to
  some particular page, then that page is probably important. PageRank Lite, basically, except
  with much more focus on intra-site backlinks.
* :ref:`embeddings`. Machine learning (ML) has the potential to
  advance the state of the art in technical writing. No, I'm not talking
  about text generation models. The ML technology that might end up having the biggest
  impact on technical writing is **embeddings**. What embeddings offer to technical writers is
  **the ability to discover connections between texts at previously impossible scales**.

.. _ml:

----------------
Machine learning
----------------

* :ref:`genai-outlook-2023`. My initial thoughts on how GenAI might affect
  technical writing.
* :ref:`stateful-assistants`. GenAI chatbot assistants might be very useful if
  they can serve as companions for the entire journey that readers take when
  visiting my docs sites.
* :ref:`evals`. How do you measure whether your retrieval-augmented generation system
  is improving over time?
* :ref:`playing-nicely`. Early ideas about how to author docs that work well with
  generative models.
* :ref:`plugins`. You can't control when ChatGPT uses your plugin. You can only maximize
  the chance that ChatGPT uses your plugin by describing your API effectively.
* :ref:`principles`. My response to Tom Johnson's "10 principles for writing for AI"
  post.
* :ref:`huggingface`. Initial experiments around summarizing text with HuggingFace
  models.
* :ref:`style-guide-fine-tuning`. How and why one might fine-tune a generative
  model into a style guide editor.
* :ref:`embeddings`. Machine learning (ML) has the potential to greatly
  advance the state of the art in technical writing. No, I'm not talking
  about Claude Opus, Gemini Pro, LLaMa, etc. The ML technology that might end up
  having the biggest impact on technical writing is **embeddings**.

.. _seo:

--------------------------
Search engine optimization
--------------------------

* :ref:`sentry-overflow`. Sentry, the app monitoring company, appears to be
  competing with Stack Overflow.
* :ref:`discovered-not-indexed`. How I fixed this error for ``pigweed.dev``.

.. _strategy:

--------
Strategy
--------

* :ref:`decisions`. A quote from *Every Page Is Page One* that has deeply
  changed how I approach technical writing.

.. _ux:

---------------
User experience
---------------

* :ref:`methodology`. How I approach my field research.
* :ref:`searchboxes`. Where should I put the search box on my docs site?
  What placeholder text should it contain? What should happen when I type stuff
  into it? What should the search results look like?
* :ref:`offline`. There seems to be unmet demand for viewing documentation websites
  without an internet connection.
* :ref:`pdf`. Just append ``#page=X`` to your URL, where ``X`` is a placeholder
  for the page you want to link to.

.. toctree::
   :maxdepth: 1
   :hidden:

   a11y/skip
   build/bazel
   data/embeddings
   data/index
   data/intertwingularity
   ml/evals
   ml/outlook-2023
   ml/huggingface
   ml/playing-nicely
   ml/plugins
   ml/principles
   ml/stateful-assistants
   ml/style-guide-fine-tuning
   seo/discovered-not-indexed
   seo/sentry-overflow
   src/link-text-automation
   src/verbatim-wrangling
   strategy/decisions
   ux/methodology
   ux/offline
   ux/pdf
   ux/searchboxes
   ux/zephyr
