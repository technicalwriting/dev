.. _principles:

======================================
Re: "10 principles for writing for AI"
======================================

2023 Apr 21

.. _10 principles for writing for AI: https://idratherbewriting.com/blog/ai-chat-interfaces-are-the-new-user-interface-for-docs#10-principles-for-writing-for-ai
.. _Supabase Clippy: https://supabase.com/blog/chatgpt-supabase-docs
.. _Text Embeddings Visually Explained: https://txt.cohere.com/text-embeddings/
.. _Markprompt: https://markprompt.com
.. _minimal, reproducible examples: https://stackoverflow.com/help/minimal-reproducible-example

This post continues my exploration into how docs strategy might need to adjust
in order take full advantage of generative AI. In this post I respond to Tom
Johnson's `10 principles for writing for AI`_, one by one.

(I ran this post idea by Tom and he heartily encouraged it. He has not
reviewed the content. Hopefully it's clear from my tone that I respect Tom and
intend for this post to be a friendly and professional discussion of important
ideas. It's more fun to figure this stuff out together through dialogue!)

-------------------
Discl{aimer,osure}s
-------------------

These are early ideas. I am not an AI expert. I have only prototyped AI-powered
documentation features. This space is moving quickly; therefore this post may be
irrelevant in a year. Tom and I both work at Google as technical writers but we
do not work on anything together. Google of course is heavily invested in AI but
everything in the post is completely my own view only. I am completely basing my
ideas off of open source work that others are doing (like `Supabase Clippy`_).

---------------------------------------------
We only have *potential* principles right now
---------------------------------------------

At this early stage, there aren't actually any principles for writing for AI. We
collectively have not figured them out yet. Only when we have a lot of rigorous
evidence and methodology can we call something a principle. For now, we just
have hypotheses about potential principles.  Based on the quote from Tom below
it's clear that he's also talking about possibilites and is not claiming that
these are tried-and-true:

  How do you write your documentation to be consumed by an AI? While I’m not an
  expert, and many are still scratching their heads about how AI chats work, the
  responses from Phind, ChatGPT, and Bard suggest that the same principles of
  writing good documentation for end users might apply to writing for AI too.
  (Sorry for the lack of more authoritative research here—this is an area I plan
  to research more.) For now, I’ll speculate on a few best practices and the
  reasons for them. Here are 10 principles for writing for AI consumption.

I'm highlighting this idea because we (the technical writer community at large)
will go farther and faster if we openly share our "lessons learned" in a spirit
of exploration and experimentation.  I don't know the answers. Tom doesn't know
the answers. That's OK! Let's figure them out together!

---------
Responses
---------

OK, let's dig in! Each section begins with the direct quote from Tom's post.

.. _galore:

"Headings and subheadings galore"
=================================

  Chunk information into headings and subheadings to keep the information clear
  and identifiable.  Subheadings help keep the writing focused and on point. The
  semantic tagging of headings with h1, h2, h3, h4 tags elevates the hierarchy and
  importance of the content, signaling to AI that this content is a high-level
  description of the section. Headings serve as a quick summary of what the
  information follows, thus reinforcing the summary of the content that it might
  spin up.

I think this is spot-on but for different reasons than what Tom mentions. In
order for context injection to work you basically need a database of your
content chunked into logical sections.  All of the content in each section must
be closely related due to how embeddings work.  See :ref:`crash-course`
for a detailed explanation of my thinking here.  Rigorous, methodical
use of headings positions your docs well for logical chunking.

Regarding "the semantic tagging... elevates the hierarchy and importance of the
content...  signaling to AI" it's important to remember that LLMs are *weird as
hell*. The way they determine relationships between text is probably not the
same as how we humans do it. I'm sure that hierarchy factors into its
calculations somehow. But remember that we are working with machines with a
different rhyme and reason than humans. SEO is sometimes in conflict with
technical writing because SEO practitioners are thinking about the needs of the
search engine whereas technical writers are thinking about the needs of the
humans. Maybe it will be the same dynamic between LLMO (Large Language Model
Optimization) practitioners and technical writers. Our job is to find harmony
between the needs of the machines and the needs of the humans.

"Semantic tags"
===============

.. _plugins: https://web.archive.org/web/20250222025828/https://technicalwriting.dev/ml/plugins.html

  Similar to heading tags, AI can infer information from semantic tagging. Is the
  information set off as a note, a blockquote, a code sample, a variable, a
  section, or something else?  Better yet, does the information conform to the
  OpenAPI specification? Machines operate well when information conforms to
  specifications. This is why almost every CCMS is XML-based—because semantically
  tagged content you can manipulate programmatically.

I don't have any firsthand insights here but my hunch is that this will turn out
to be correct. The most obvious candidates to me are DITA, DocBook, and Schema.org.

Actually, I do have one firsthand insight. ChatGPT Plugins must conform to the
OpenAPI specification. See `plugins`_. Technical writers with OpenAPI expertise
will probably see sustained or increased demand.

"Code samples"
==============

  Code samples are also a way AI can understand content, since code operates
  according to programming language rules. AI can infer the inner workings of a
  system by analyzing the meaning and syntax of the code.

No insights here. It sounds reasonable. For fine-tuning there may be increased
emphasis on `minimal, reproducible examples`_. AI is all about prediction. Given
this temperature, this wind, this day of the year, what is the chance of rain?
Temperature, wind, and date are your inputs. Chance of rain is your desired
output. Now, try to apply this same type of thinking towards documentation. What
are your inputs? What's your output? The page title and code block could be your
inputs. Whether or not the code builds could be your output. Or maybe the code
block should be the output? This is why I keep saying that applying fine-tuning
to docs is tricky. What are the inputs and outputs?

"Fewer images"
==============

  Images might be an anti-pattern for AI consumption and processing. If you’ve
  ever checked an image (a binary file) in Git and looked at a diff, you’ll see
  the gibberish-like code behind that image.  Machines don’t process this code
  well, so if the documentation is visually based, this could lead to less AI
  processing and understanding. If you use images, add detailed captions below
  them.  Additionally, any graphics, including buttons, should have a text label
  that describes them.

OK, now we can finally get a little spicy! I disagree with this one. We already
have multimodal LLMs that can input/output images. It seems like generative AI
can handle images just fine.  If anything, I feel *more optimistic* about the
future of using images in documentation.  Take for example the age-old problem
of terrible ``alt`` descriptions. It breaks my heart when someone puts an
intricate diagram in a doc with a lot of important information yet the ``alt``
description only says "diagram". All of the important information conveyed
through the diagram is not accessible to people who rely on assistive
technology. LLMs offer the possibility of auto-generating useful ``alt``
descriptions. I have experimented with this and have seen some promising
results.

"Longer pages with context and modularity"
==========================================

  Having more fully developed pages with sufficient context and modularity will
  help AI tools better understand the coherence of information. By context and
  modularity, I mean the content should be able to stand on its own, without
  supporting content (aka “Every Page Is Page One’’ content models). Docs that are
  sharded into a hundred different topics connected through a JS-driven sidebar to
  expand and collapse the topics in various folders will probably be harder for
  machines to read, since the sidebar code might be more visually oriented to end
  users than machine-friendly. With this fragmented model, AI tools would need a
  thread weaving together all the different topics.

In :ref:`playing-nicely` my hunch was the
opposite. I thought small pages were more likely to work well with generative AI
than long pages for reasons related to what I just said in :ref:`galore`
But now I'm not so sure. We've
been debating this in the Write The Docs Slack. Tom brought up the good point
that if you're providing a UI like `phind.com <https://phind.com>`_ which shows
sources alongside the generated answers, then lots of small pages will mean
having to sift through lots of results in the sources UI.

I will note however that the comment about JS-driven sidebars only applies if
the LLM is trying to read entire HTML pages. That's now how context injection
currently works.

Remember, also, that token limits are a constraint right now. You can only
provide around 16K characters of input to GPT-3.5. Will the situation improve?
Surely. But still, it's a real limitation right now.

"Consistent terms"
==================

  Consistent terms, especially matching the user’s query, are important in
  connecting the user’s query with the AI chat response. Although AI tools can
  likely interpret synonyms and make this connection, it’s better if the terms
  match.

Agreed. The inner workings of LLMs are profoundly statistical. It seems very
likely to me that using consistent terminology will make the LLM's job easier.

(`Text Embeddings Visually Explained`_ is a very satisfying rabbit hole for
building intuition about the statistical nature of LLMs.)

"Cross-references"
==================

  Cross-references can enable AI to make sense of similar information.
  Cross-references help build a better web of information to power relationships
  through a semantic connection. AIs work fundamentally by prediction, by
  associating the most likely way to fill in the blank. Cross-references help
  associate topics with each other, teaching AI tools that the information is
  related and similar, which then might lead to a collection of cross-referenced
  sources used for the response.

This is an open-ended idea so I might be misunderstanding what Tom is getting
at. To me, this sounds related to the fundamental problem of context injection:
figuring out which docs content to inject into the prompt. It seems like Tom is
suggesting a manual process where humans explicitly markup the associations
between docs. It could work, but we already have another approach that is easier
to automate: embeddings.

"Plain language"
================

  Sentence structures should be easy for AI to parse. This means avoiding long
  sentence structures or ambiguous constructions. Documentation that consists of
  clear, almost staccato-like sentences will probably be interpreted better, even
  if it’s not as eloquent. We might balk a string of short constructions, but the
  prime consideration in docs is always intelligibility. Plain language and short
  sentences are hallmarks of simplified language, and this will help AI parse the
  meaning of the documentation better.

This also seems likely.

"More documentation, not less"
==============================

  Previous trends toward minimalism, with the concern that too much
  documentation might overwhelm the user, might not be applicable. More detail,
  more documentation, and more information seem to lead to better AI experiences.
  Almost all AI training involves an extensive set of data (the large language
  model). With enough training, the AI can more intelligently respond to the
  variety of user queries.

Strongly agree. This is what I'm most excited about. I'm sorry for the
cliffhanger but it will take too long to flesh out all my thoughts on this topic
so you'll just have to stay tuned for a full post later.

"Glossaries"
============

  A comprehensive glossary can help AI explain confusing components. For
  example, if the AI says to “implement a recursive pattern,” but it doesn’t know
  what recursive means in the context of the application, the AI’s responses will
  be limited or potentially wrong. A glossary could allow AI to break down
  confusing language and jargon for users. It could also help with synonyms.

Terminology could be a great application of fine-tuning for docs. Remember, LLMs
are prediction machines. Given this text, what is the next most likely text to
occur? Training an LLM on your glossary and terminology seems like exactly the
same thing. Given this word or short phrase (the term), the expected output is
the definition of the term.

Fine-tuning for terminology may not be necessary, though. As mentioned
elsewhere, I am prototyping an experience along the lines of `Supabase Clippy`_.
With context injection, the LLM usually infers the meaning of the term
correctly. For example, one time the prompt was ``Ninja``. With context injection
the LLM correctly inferred that we were talking about the software build system,
whereas the out-of-the-box LLM reply (without context injection) assumed that we
were talking about the black-robed assassins from Japanese history.
