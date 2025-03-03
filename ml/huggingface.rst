.. _huggingface:

============================================
Generating summaries with HuggingFace models
============================================

.. _HuggingFace Transformers: https://huggingface.co/docs/transformers/index
.. _biodigitaljazz.net: https://biodigitaljazz.net
.. _Sphinx: https://www.sphinx-doc.org/en/master/development/index.html
.. _extension: https://www.sphinx-doc.org/en/master/development/index.html
.. _the vault: https://www.youtube.com/watch?v=6S5ZuXhNbL4
.. _No prisoners! No prisoners!: https://www.youtube.com/watch?v=dLl1TeEZQq0
.. _csebuetnlp/mT5_multilingual_XLSum: https://huggingface.co/csebuetnlp/mT5_multilingual_XLSum

2023 Dec 6

Can I use one of the summarization models published on HuggingFace to locally
generate summaries for each page of my Sphinx site? The answer after one
night of Covid-delirious experimentation appears to be a resounding "maybe"!

Summarization is attractive to me for a few reasons. By "attractive" I mean I
may actually try to ship page summarization on the docs sites I work on.

* It's actually useful. A lot of technical docs use Too. Many. Damn. Words.
  Summaries are very helpful for making quick `information
  scent <https://www.nngroup.com/articles/information-scent/>`_ decisions.
* It can be architectified as a batch job. Generate the summary at build time and
  store it somewhere. You don't need to re-generate until the page content
  changes.

`HuggingFace Transformers`_ is super cool. The API is really beginner-friendly
and the docs site seems really well done. It took me a comically long time to
realize that I'm supposed to mentally replace every instance of "🤗" in their
docs with "HuggingFace" but once I got past that hiccup I was cruising.

My other site, `biodigitaljazz.net`_, runs on `Sphinx`_. I spun up a simple
`extension`_ to generate a summary for each page. First, let's look at an even
simpler extension that just spits out the text of a single page:

.. code-block::

   import docutils

   def show_me_the_text(app, doctree, docname):
       if docname != 'blog/picam':
           return
       text = doctree.astext()
       print(text)

   def setup(app):
       app.connect('doctree-resolved', show_me_the_text)
       return {
           'parallel_read_safe': True,
           'parallel_write_safe': True,
       }

There are some setup steps I'm skipping but after it's all rigged up it
prints out the following text:

.. code-block::

   The eleventh circle of hell: setting up an RPi camera module

   2023 Nov 22

   Short story long, don’t trust any of the community content; it’s full of ghosts
   and wolverines and those people you meet at parties that start the
   conversation with “so what do you do?”… Rely solely on the official RPi
   docs. And make sure that whatever you’re reading was written for the
   specific HW/SW permutation that you’re using. In my case (RPi4 + RPi OS
   Bookworm + RPi Camera Module 3) the correct doc is The Picamera2 Library.

   Once I found the right doc it was trivial to get everything working. The
   picamera2 repo has an extensive collection of examples. It’s downright magical
   that I can get started with computer vision in a matter of minutes. OpenCV is
   really cool stuff.

   This gem of a quote from an RPi engineer sums up the situation:

   Hi, yes it’s a bit of a minefield out there on the web because so much
   content is still referring to the legacy camera stack which will never
   (for example) support the camera module 3, or even work at all on any
   reasonably modern Raspberry Pi OS image.

   I’m not writing this post to complain; who has time for that? This is just
   a courtesy heads up to my fellow hackers.

   <p style="margin-top: 10000px;">
       Huh? You're still here? And you scrolled all the way down here just
       to ask "What's the tenth circle?" Excellent question. I have no idea.
   </p>

Every model sees exactly this same text. Now let's do some summarizing!

.. code-block:: python

   import docutils
   import transformers

   models = [
       'facebook/bart-large-cnn',
       'sshleifer/distilbart-cnn-12-6',
       'philschmid/bart-large-cnn-samsum',
       'pszemraj/led-base-book-summary',
       'google/pegasus-cnn_dailymail',
       'google/pegasus-xsum',
       'Falconsai/medical_summarization',
       'google/bigbird-pegasus-large-arxiv',
       'knkarthick/MEETING_SUMMARY',
       'pszemraj/led-large-book-summary',
       'google/pegasus-large',
       'knkarthick/MEETING-SUMMARY-BART-LARGE-XSUM-SAMSUM-DIALOGSUM-AMI',
       'facebook/bart-large-xsum',
       'csebuetnlp/mT5_multilingual_XLSum',
       'ArtifactAI/led_large_16384_arxiv_summarization'
   ]

   def summarize(app, doctree, docname):
       if docname != 'blog/picam':
           return
       text = doctree.astext()
       for model in models:
           print(f'\n\n\n********** {model} **********\n\n')
           try:
               summarizer = transformers.pipeline('summarization', model=model)
               result = summarizer(text)
               print(result[0]['summary_text'])
           except Exception as e:
               print('error')

   def setup(app):
       app.connect('doctree-resolved', summarize)
       return {
           'parallel_read_safe': True,
           'parallel_write_safe': True,
       }

I pulled that list of models from the `most downloaded models that support
the summarization pipeline <https://huggingface.co/models?pipeline_tag=summarization&sort=downloads>`_.

And now the results!

.. code-block:: none

   ********** facebook/bart-large-cnn **********

   vern totality totality totalityグググflagsググ Fieldsググlysググ derivativeググ
   78グ Fieldslysグ Fields Fields Fieldsグlys Fieldsグ Fields scathing Fields
   Fieldslys Fields Fields ne Fields Fields 78 Fields Fields derivative Fields
   Fields scathingグ Fields nelys Fieldslyslys Fields ne ne Fieldslys ne Fields
   scathing ne Fields ne Fif Fields FieldsAMES Fields Fields Excel Fields Fields
   Reeves Fields Fields Fif Fields Fiflys Fields Fif ne Fields Fif Fif Fif
   Fieldslys Fif Fif ne Fif Fiflys Fif Fieldsouk Fif Fifoukoukouk
   Charlottesvilleouk LauderSnapouk LauderReviewReview Lauder Lauder Lauder
   Contrast Lauder Lauder brewing profiles brewing brewing brewing Lauder brewing
   Contrast Contrast Contrast brewing brewing Registration brewing brewing matching
   brewing brewing Contrast brewing

Holy shit, talk about a terrible start. I have no idea what ``scathingグ``
means but I definitely feel threatened by it. Let's just put that one in
`the vault`_ and keep going...

(Of course, the real answer is that I'm just holding something wrong or the
model isn't actually intended for this task. Never underestimate pilot error.)

.. code-block:: none

   ********** sshleifer/distilbart-cnn-12-6 **********

   error

   ********** philschmid/bart-large-cnn-samsum **********

   error

   ********** pszemraj/led-base-book-summary **********

   The eleventh circle of hell: setting up an RPi camera module In this chapter,
   the author explains how to get everything working without relying on any of
   the official RPi docs. He uses OpenCV and OpenCV to get things running. This is
   just a courtesy post to his fellow hackers.

OK! 4 models in and we've got something almost usable. The formatting is off
though and there's actually a huge factual error. It says I got everything
working without relying on any of the official docs. That is categorically *not*
what I say in the post.

(A lot of the models error'd. I think that's just because I'm running these
tests via ``transformers[tf-cpu]`` on a Linux.)

Onwards! `No prisoners! No prisoners!`_

.. code-block:: none

   ********** google/pegasus-cnn_dailymail **********

   error

   ********** google/pegasus-xsum **********

   All images are copyrighted.

What in the sam hell. That text doesn't even appear on my page.

.. code-block:: none

   ********** Falconsai/medical_summarization **********

   the eleventh circle of hell: setting up an RPi camera module 2023 Nov 22 Short
   story long , don’t trust any of the community content; it’s full of ghosts and
   wolverines and those people you meet at parties that start the conversation with
   “so what do you do?”... Rely solely on the official docs . once I found the
   right doc it was trivial to get everything working . the picamera2 repo has an
   extensive collection of examples .

   ********** google/bigbird-pegasus-large-arxiv **********

   error

   ********** knkarthick/MEETING_SUMMARY **********

   Setting up a camera module on a Raspberry Pi is a daunting task. The correct
   documentation can be found in The Picamera2 Library. OpenCV is really cool.

Not bad! I might be able to actually use this.

.. code-block:: none

   ********** pszemraj/led-large-book-summary **********

   Bookworm + RPi OS = nightmare #1: setting up an RPi camera module Warning: The
   community site is full of ghost and wolverines and people asking "so what do you
   do?” Do not trust the community site. Instead, read the official RPi docs. In my
   case, the correct doc is The Picamera2 Library. Once I found the right doc, it
   was trivial to get everything working. It's downright magical that I can get
   started with computer vision in a matter of minutes. OpenCV is really cool
   stuff. This gem of a quote sums up the situation:Hi, yes it's a minefield out
   there on the web because so much content is still referring to the legacy camera
   stack which will never support the camera module 3, or even work at all on any
   reasonably modern Raspberry Pi OS image.I'm not writing this post to complain;
   who has time for that? This is just a courtesy heads up to my fellow hackers.

A lot of these things seem to just be verbatim regurgitations of my original
text, with worse formatting. ``Bookworm + RPi OS = nightmare`` has a nice ring
to it, though...

.. code-block:: none

   ********** google/pegasus-large **********

   error

   ********** knkarthick/MEETING-SUMMARY-BART-LARGE-XSUM-SAMSUM-DIALOGSUM-AMI **********

   The eleventh circle of hell: setting up an RPi camera module. The correct doc is
   The Picamera2 Library. OpenCV is cool stuff.

This is a variant of the other model that worked well. This text is a little
better than that previous model.

.. code-block:: none

   ********** facebook/bart-large-xsum **********

   I’m a big fan of OpenCV, but I’ve found that if you want to get started with
   computer vision on a Raspberry Pi it’s best to stick to the official
   documentation.

What stands out to me most is how *different* this text is than the other
models. It's sending a negative message about OpenCV that doesn't exist in the
source text, though.

.. code-block:: none

   ********** csebuetnlp/mT5_multilingual_XLSum **********

   error

   ********** ArtifactAI/led_large_16384_arxiv_summarization **********

   the eleventh circle of hell: setting up an RPi camera module 

`Well, that about does 'er. Wraps 'er all up. <https://youtu.be/sYsw0KVRjCM?si=Hvpt8aYhc2XyC7FO&t=73>`_
I'll get those errors fixed and keep exploring other models. I'll also try
more sophisticated model invocations, such as the example from
`csebuetnlp/mT5_multilingual_XLSum`_.

Assuming that I can find a model that works, the next hurdle is the size of
the dependencies. The ``transformers[tf-cpu]`` library that I used appears to be
hundreds of megabytes. The model is usually another gigabyte at least. And
of course there's all the licensing uncertainty around generated content. I also
imagine that these models can't handle that much text. I guess I could do a 
divide-and-conquer approach where I generate a summary for each section,
concatenate all those summaries together, and then run the summarization one
last time on the concatenated section-level summaries. Sphinx makes it trivial
to process a doc section-by-section. Sphinx rules.

P.S. the next time you find yourself battling an evil wizard, remember the auric defense
incantation: ``Fields scathingグ Fields nelys Fieldslyslys Fields ne ne Fieldslys ne Fields``
