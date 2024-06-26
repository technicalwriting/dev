.. _link-text-automation:

==============================
Link text automation in Sphinx
==============================

.. _explicit target: https://docs.readthedocs.io/en/stable/guides/cross-referencing-with-sphinx.html#explicit-targets
.. _Sphinx: https://www.sphinx-doc.org
.. _Structure link text: https://developers.google.com/style/link-text#structure-link-text
.. _A Link is a Promise: https://www.nngroup.com/articles/link-promise/
.. _"Learn More" Links\: You Can Do Better: https://www.nngroup.com/articles/learn-more-links/
.. _Better Link Labels\: 4 Ss for Encouraging Clicks: https://www.nngroup.com/articles/better-link-labels/
.. _toil: https://sre.google/sre-book/eliminating-toil/
.. _no raisin: https://www.youtube.com/watch?v=V3ZUhWuiQ20
.. _MyST: https://myst-parser.readthedocs.io/en/latest/
.. _reStructuredText: https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html
.. _IfThisThenThat: https://fuchsia.dev/fuchsia-src/development/source_code/presubmit_checks#ifthisthenthat
.. _If I wasn't so lazy: https://www.youtube.com/watch?v=siGFs_NhcOk

2023 Mar 30

Sphinx's approach to link text improves docs maintainability and reduces
toil.

(Throughout this post I use the term **docs site systems** to refer to the
static site generators (SSGs) and content management systems (CMSs) that
most documentation websites are built on top of: Docusaurus, Jekyll, Sphinx,
WordPress, and so on.

----------
Background
----------

The Nielsen Norman Group has done quite a bit of research on how to create
effective link text:

* `A Link is a Promise`_
* `"Learn More" Links: You Can Do Better`_
* `Better Link Labels: 4 Ss for Encouraging Clicks`_

Long story short, effective link text is specific, sincere, substantial, and
succinct.

The `Structure link text`_ section of the Google Developer Documentation Style
Guide has a helpful rule-of-thumb that gets you most of the way there without
having to think much: just use the exact text of the title or section heading
that you're referencing.

(Not having to think about this stuff is good! We technical writers have more
than enough to think about!!)

-----------------------------------------------------------
Problems with how most docs site systems approach link text
-----------------------------------------------------------

In most docs site systems, you have to manually create and maintain the link text.
For example, over in ``guide.md`` we might have a section heading like this:

.. code-block:: none

   ## How to enable text compression { #compression }

(Assume that ``{ #compression }`` is a non-standard feature that allows you
to define the ID for that section heading. This is another helpful feature that
is strangely lacking in many docs site systems! But, alas, I will have to save that
idea for another day.)

And then over in ``reference.md`` we link to this section like this:

.. code-block:: none

   See [How to enable text compression](./guide#compression).

(Assuming that both docs live in the same directory.)

One thing that bugs me about this manual approach is the tendency for the link
text to rot over time. If you change the section heading in ``guide.md`` there
is no automatic detection that the link text in ``reference.md`` is now
out-of-date.

But most importantly, this manual approach is textbook `toil`_. If you follow
the rule-of-thumb that link text should always match the document title or
section heading, then there should be a way to put a placeholder where you want
the title or heading to go, and when you build the site the placeholder is replaced
with the actual title or heading. There is `no raisin`_ to manually maintain
this crap.

----------------------------
How Sphinx handles link text
----------------------------

Automatic replacement of placeholders is exactly what `Sphinx`_ provides. Over in
``guide.rst`` (previously ``guide.md``, see the note below) you create an
[explicit target] to the section heading:

.. code-block:: rst

   .. _compression:

   ==============================
   How to enable text compression
   ==============================

(The filename changed from ``guide.md`` to ``guide.rst`` because most Sphinx sites
use `reStructuredText`_ (reST), not Markdown. Sphinx also supports a Markdown-y
syntax called `MyST`_.)

And then in ``reference.rst`` you simply add a reference to that section heading:

.. code-block:: rst

   See :ref:`compression`.

This gets replaced with ``How to enable text compression`` at build time.

This solution totally fixes the toil problem but it doesn't quite fix the rot
problem. If you change that section heading in ``guide.rst`` there isn't really an
automated way to make sure that the link in ``reference.rst`` still makes sense.
The only solution I can think of for that problem is to create a linter like
`IfThisThenThat`_.

Another huge benefit of this approach is that the build system warns you when
you're linking to a section that no longer exists:

.. code-block:: none

   $ make html
   Running Sphinx v6.1.3
   ...
   /.../reference.rst:4: WARNING: undefined label: 'compression'

-----------------------------------------------------
The status of this feature in other docs site systems
-----------------------------------------------------

`If I wasn't so lazy`_ I would list out the exact status of this feature on
other docs site systems. I am not going to do that, however, because, as previously
alluded to, I am lazy. I don't mean to imply that this feature is not supported
on any other docs site systems. I am sure there is some other docs site system out there that
has "seen the light." From what I can tell, though, most do not.

------------------------------
ChatGPT's summary of this post
------------------------------

  Sphinx's approach to link text in documentation websites enhances
  maintainability and reduces toil, using placeholders to automatically update
  link text. This method effectively tackles the toil problem but does not
  completely address the issue of outdated link text when a section heading
  changes. While Sphinx is not the only platform to offer such features, it
  stands out for its built-in support. Despite its advantages, this approach is
  not more common in other documentation site generators or content management
  systems.
