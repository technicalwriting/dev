.. _offline:

======================
SWEs want offline docs
======================

2023 May 31

I don't have any grand ideas here. I just want to kick off a discussion
within the technical writing community about the need for offline docs
and how we might go about making our docs more easily consumable in offline
contexts. I know that some docs sites already support this. I also know
that it's not a new idea. My main question is: should we make it more ubiquitous?
If so, how?

`Hacker News <https://news.ycombinator.com>`_ (HN) is a forum for technology news.
A lot of software engineers visit and discuss stuff on HN. There's a
`thread <https://news.ycombinator.com/item?id=36135955>`_ on the "front page"
of HN right now about `Zeal <https://zealdocs.org>`_, "an offline documentation
browser for software developers." It's basically a desktop app that lets you
pick and choose documentation sets to download. The doc sets get saved to disk
and you can read the docs offline through the Zeal browser.

This is `the most upvoted comment in the thread <https://news.ycombinator.com/item?id=36137032>`_:

  I wish this approach were more supported by those producing documentation.
  Looking things up in reference docs is one of those cases where reducing
  friction yields huge productivity benefits, but I still end up using a search
  engine (Kagi now as Google hides authoritative reference docs under a pile of poor-quality,
  irrelevant spam these days). I've tried Zeal multiple times but while the app is nice and
  many of the docsets are good, many of them aren't good: badly formatted, badly indexed,
  outdated or simply nonexistent. A search engine requires no setup and covers everything.
  It's just so horribly slow.
  
  If we were grown ups, all software authors/vendors would be providing their reference docs
  in a standardised form, findable, downloadable and displayable by a wide range of tooling,
  consistent across languages, IDEs and platforms. Zeal is the closest we have, and it's a
  noble effort, but IME it doesn't solve the problem well enough to be useful because there's
  no buy-in from the people producing the docs.
  
  (First to mention ChatGPT gets slapped with a wet fish. Just try me.)

I.e. offline docs systems are great but they need better search interfaces.

Similar products:

* `devdocs.io <https://devdocs.io>`_
* `Dash <https://kapeli.com/dash>`_

I personally have felt the need for offline docs on quite a few occasions. Flying on an
airplane is the most common use case. But sometimes I just want to go to a coffee shop
and work on one of my little toy projects without needing to connect to the shop's
Wi-Fi. Or the Wi-Fi in my house is acting spotty for whatever reason. And so on.

Another `comment <https://news.ycombinator.com/item?id=36140344>`__ from the same thread:

  I have Zeal installed on my Linux desktop but I rarely use it.
 
  The reason is that most of the time, I want to read documentation for a specific version
  of whatever thing I'm using. Zeal only has docs for the latest version, or in some cases,
  major versions. Take Ansible and Python, for example. These tend to have breaking changes,
  new features, and hard deprecations in their minor version releases. So knowing that I'm
  looking at the docs for Python 3.8 vs 3.11 can be very important.

  One of my "someday" projects is to write a doc viewer with an obnoxious plethora of sources
  including docs shipped for every minor version of a program, docs for operating systems,
  man pages, info pages, maybe even wiki content for exceptional wikis like arch and gentoo.

I.e. offline docs systems need all versions of the doc sets.

This `comment <https://news.ycombinator.com/item?id=36137521>`__ kicked off a discussion on why
people like and use offline docs systems:

* Google Search isn't surfacing the official docs as the top result any more
* Intentionally going offline to think through problems and remove distractions
* Docs sites are too slow
