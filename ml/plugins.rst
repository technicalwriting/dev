.. _plugins:

======================================================================
The role of web service API reference documentation in ChatGPT Plugins
======================================================================

.. _ChatGPT Plugins: https://openai.com/blog/chatgpt-plugins
.. _Plugin flow: https://platform.openai.com/docs/plugins/introduction/plugin-flow
.. _OpenAPI specification: https://swagger.io/specification/
.. _Best practices: https://platform.openai.com/docs/plugins/getting-started/best-practices
.. _impact: https://technicalwriting.tools/posts/generative-ai/
.. _Introduction: https://platform.openai.com/docs/plugins/introduction
.. _Defining Well-Known URIs: https://www.ietf.org/rfc/rfc5785.txt

2024 Apr 5

ChatGPT Plugins enable ChatGPT to access real-time information. Web service
API reference documentation plays a big and important role in the ChatGPT
Plugin architecture. You can't force ChatGPT to use your plugin. You can only
persuade ChatGPT to do so by documenting your API effectively.

This post is part of my ongoing series to explore the potential impact of
generative AI on technical writing.

(ChatGPT Plugins are in "Limited Alpha" which means that OpenAI might still make
fundamental changes to the ChatGPT Plugin architecture. In other words, this
post might be completely outdated in a year.)

----------
Background
----------

ChatGPT is an AI chatbot that can generate detailed answers across many domains.
The large language model that powers ChatGPT was trained on data from 2021 so
ChatGPT can't provide information about stuff that has happened recently.
`ChatGPT Plugins`_ fill in this information gap by enabling ChatGPT to access web
service APIs. In other words, plugins enable ChatGPT to get post-2021
information.

---------------------------------------------------------------
How ChatGPT Plugins use web service API reference documentation
---------------------------------------------------------------

Here's the fascinating bit for technical writers. From `Introduction`_:

  The AI model acts as an intelligent API caller. Given an API spec and a
  natural-language description of when to use the API, the model proactively
  calls the API to perform actions. For instance, if a user asks, "Where should
  I stay in Paris for a couple nights?", the model may choose to call a hotel
  reservation plugin API, receive the API response, and generate a user-facing
  answer combining the API data and its natural language capabilities.

In other words, you can't control when ChatGPT uses your plugin. You can only
maximize the chance that ChatGPT uses your plugin by describing your API
effectively!

Implementation details
======================

`Plugin flow`_ gives you a peek into how ChatGPT plugins are built. You create a
plugin manifest at ``<domain>/.well-known/ai-plugin.json`` where ``<domain>`` is
just a placeholder for your actual domain. The plugin manifest contains a
description of the overall web service API as well as descriptions for each API
endpoint. The endpoint descriptions must conform to the `OpenAPI specification`_.

----------------------------------
Implications for technical writers
----------------------------------

There are two scenarios to watch out for:

* ChatGPT stays popular and becomes a fundamental tool
* Some other AI-powered tool becomes fundamental and adopts the ChatGPT Plugins
  architecture

Good news for technical writer demand
=====================================

Effective API reference documentation will probably become much more closely
tied to organization success and much easier to measure. A high-quality API
reference that closely matches the vocabulary of users and is easy for ChatGPT
to consume should result in increased plugin usage.

OpenAPI is good to know
-----------------------

Technical writers who have lots of experience with the `OpenAPI specification`_
in particular should see continued strong demand for their `very particular
set of skills <https://youtu.be/gR3kEa8rVD0>`_.

Shifting API reference audiences
================================

As hinted at in the last section, when writing API reference documentation for
ChatGPT, your main audiences are ChatGPT users and ChatGPT itself. This is a
big change in focus for technical writers. Currently, we optimize API reference
documentation for human developers.

Let's start with ChatGPT users. Remember that the name of the game is to
*persuade* ChatGPT to call your plugin. Presumably, the more your API reference
matches the vocabulary of your customers (the people using ChatGPT), the higher
the chances that ChatGPT will recognize that your plugin is a match for the task
at hand.

(Emphasis on "persuade" in the last paragraph because OpenAI makes it very
clear in `Best practices`_ that the API reference must be accurate and objective
and must not attempt any manipulation. `Plugin flow`_ says that plugins will only
be accessible to all ChatGPT users after passing a review.)

Next, ChatGPT itself. I don't have much to say here, other than the fact that
the plugin manifest must be structured and written in a way that makes it easy
for ChatGPT to consume your API.

Finally, human developers. As far as plugin manifests are concerned, I don't
really see much of a need to optimize for human developers. Maybe we learn
eventually that an API reference that is easy for a human developer to read also
happens to be what's easiest for ChatGPT to consume.

The rise of LLMO?
=================

Along with "prompt engineer" I wouldn't be surprised if "LLMO" (large language
model optimization) becomes a trendy new tagline on LinkedIn.

Continued momentum to use standards
===================================

The API reference section of the plugin manifest must conform to the OpenAPI
specification. The ``.well-known`` part of the example plugin manifest URL that
you saw earlier is an IETF standard: `Defining Well-Known URIs`_
