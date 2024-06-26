.. _discovered-not-indexed:

=================================================================
Fixing Google Search Console's "discovered but not indexed" error
=================================================================

2024 Jan 29

My workflow for solving the "Discovered - currently not indexed" error in
Google Search Console.

While digging into the Google Search Console data for
`pigweed.dev <https://pigweed.dev>`_ this month I discovered a peculiar problem:
we have a bunch of pages that are labeled as ``Discovered - currently not
indexed``. This post documents my findings on how to fix this problem.

Disclaimer / disclosure: Although I work for Google, you will never get any
"insider knowledge about the internal workings of Google Search" from me.
First, obviously I would not be able to share that kind of stuff if I knew it.
Second, I don't know any of that stuff. Your guess is as good as mine. I work
outside of the Search org, and the Search org maintains a super strict firewall
with Googlers outside their org.

OK, let's dig into the problem. On the bottom of my **Pages** tab there's
a row in the **Why pages aren't indexed** table saying that 56 pages are
**Discovered - currently not indexed**.

.. image:: /_static/gsc-pages.png
   :alt: "Google Search Console > Pages"

Apparently I've also got a bunch of pages with misconfigured canonical tags,
but that's perhaps a post for another day.

If I click that **Discovered - currently not indexed** row it takes me to a
breakdown of the problem:

.. image:: /_static/gsc-discovered1.png
   :alt: "Google Search Console > Pages > Discovered - not currently indexed"

.. _Discovered - currently not indexed: https://support.google.com/webmasters/answer/7440203#discovered__unclear_status

The **LEARN MORE** link points to `Discovered - currently not indexed`_
which doesn't say much:

  The page was found by Google, but not crawled yet. Typically, Google wanted
  to crawl the URL but this was expected to overload the site; therefore Google
  rescheduled the crawl. This is why the last crawl date is empty on the
  report.

.. _Why, by the way? Is it a soup metaphor?: https://youtu.be/UOs-4J6rr-w?t=122

The plot thickens, as they say. (`Why, by the way? Is it a soup metaphor?`_)
It doesn't sound like I've misconfigured anything. It sounds like I just need
to get Google Search to re-crawl the pages.

.. _sphinx-sitemap: https://github.com/jdillard/sphinx-sitemap

(Back in October I added `sphinx-sitemap`_ to start auto-generating pigweed.dev's
sitemap. Maybe Google Search discovered a bunch of new URLs through the sitemap
and decided that it would overload the site if it tried to index them all?)

How to fix this? Previously there was a **VALIDATE FIX** button. I clicked that
on 20 Jan 2024 but given that it's now 29 Jan 2024 and nothing has changed,
I'll have to assume that that button doesn't actually do anything. What else
can I do?

When I scroll down this page a bit I see a list of the offending URLs:

.. image:: /_static/gsc-discovered2.png
   :alt: "Google Search Console > Pages > Discovered - not currently indexed"

Clicking one of the table's rows shows an **INSPECT URL** option:

.. image:: /_static/gsc-inspect.png
   :alt: "Google Search Console > Pages > Discovered - not currently indexed > INSPECT URL"

On the URL's details page I see a **REQUEST INDEXING** button:

.. image:: /_static/gsc-request.png
   :alt: "Google Search Console > URL Inspection"

After clicking **REQUEST INDEXING** a modal pops up and tells me it'll take a
minute or two to kick off the manual indexing request and then it confirms that
the request has been added to the manual request queue.

It seems that there's a quota of 12 requests per day. That's fine for me; I
only have 56 unindexed pages so I'll be able to get them all done in 5 days.
When I initially tested this approach last week, I had 60 unindexed pages,
whereas the number is now down to 56, so it seems to be working.

I'll update this post if I find better ways to fix this problem.

--------
Update 1
--------

.. _Ahrefs: https://web.archive.org/web/20240130212256/https://ahrefs.com/blog/discovered-currently-not-indexed/

`Ahrefs`_ has a post on the topic. For pigweed.dev I suspect that the issue is
related to how we've configured redirects.

----------------------
Update 2 (30 Jan 2024)
----------------------

.. _Redirect error: https://web.archive.org/web/20240130213440/https://support.google.com/webmasters/answer/7440203#multiple_redirects

I checked back on one of the pages that got manually indexed yesterday. The
details page now confirms that Google Search could not crawl the page because
of a redirect issue. The **LEARN MORE** link points me to `Redirect error`_.

.. image:: /_static/gsc-redirect.png
   :alt: "Google Search Console > URL Inspection"
