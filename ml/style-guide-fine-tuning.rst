.. _style-guide-fine-tuning:

============================================
Fine-tuning an LLM into a style guide editor
============================================

2023 Apr 29

Style guides usually have far more rules than I can possibly remember all at
once while editing a doc. Can I fine-tune an large language model (LLM) to
automate the process of editing a doc for style guide rules?

---------------------------------------------------
A crash course in fine-tuning for technical writers
---------------------------------------------------

The main idea is that you take a generic, off-the-shelf LLM and continue its
formal training. Your continued training gets baked into the LLM and it "remembers"
that training. See [Context injection versus fine-tuning] for more detail.

----------------------
Reinventing the wheel?
----------------------

.. image:: /_static/linter.jpg
   :alt: A variation of the meme where the top image is a fancy dinner described
         as 'a breaded chicken piccata with lemon jasmine rice' and the bottom image
         is a skeptical man who responds with 'This is chicken nuggets.' The top
         caption has been replaced to say 'a fine-tuned LLM to enforce style guide'
         and the bottom image now says 'this is linter'.

(This is one of my favorite memes. It gets used a lot within Google but I don't see
it as often in public. Here's the `original </assets/nuggets.jpg>`_.)

We don't need LLMs to solve this problem. In fact, in a past life I built a webhook bot
that listens for incoming PRs and parses/analyzes the updated Markdown to detect style
guide issues: `chrome-devrel-review-bot`_.

I'm going forward with this fine-tuning experiment nonetheless because my primary goal is to
get familiar with exploring whether fine-tuning in general can be applied to
docs needs.

There are a lot of docs sites pursuing the retrieval-augmented generation
approach pioneered by Supabase Clippy. `Knowledge Retrieval Architecture for LLMs`_
is an excellent general technical overview of that approach. I'm not aware of any
docs sites using formal fine-tuning.

Potential advantages
====================

The fine-tuned-LLM approach might have a couple advantages over the
linter approach:

* I might not need to implement every rule explicitly. For example, in this post
  I'm going to attempt to fine-tune an LLM to edit ``it is`` down to ``it's``.
  Maybe the LLM will also edit ``what is`` down to ``what's`` even though that rule is
  not explicitly mentioned in the training data.
* The preparation of the training data doesn't require any programming knowledge.
* If the LLM can "remember" hundreds or thousands of rules simultaneously then
  that would be `awesome. Awesome to the max.`_

-------------------------
My implementation journey
-------------------------

The rest of this post documents the lessons I learned as I tried to implement
this idea.

Making sense of training data
=============================

To fine-tune an LLM using OpenAI's API, you provide training data in this format:

.. code-block:: none

   {"prompt": "<prompt>", "completion": "<completion>"}
   {"prompt": "<prompt>", "completion": "<completion>"}
   ...

This is `JSONL`_ format. Each line is a valid JSON value. Why didn't OpenAI use
a more common format? `That's an excellent question. I have no idea.`_

The primordial soup of an implementation begins to form. ``<prompt>`` should hold the
original text. ``<completion>`` should hold the edited text.

.. code-block:: none

   {
       "prompt":     "It is possible to fine-tune an LLM to enforce a style guide.", 
       "completion": "It's possible to fine-tune an LLM to enforce a style guide.", 
   }

`General best practices`_ says that I need at least a few hundred high-quality examples.
Here's our first big insight. If we really go for this "LLM as style guide editor" thing,
**we may need a few hundred prompt-completion pairs for every single style guide
rule.**

First attempt
=============

The "primordial soup" approach won't work. I need to give the LLM some cues to go into
editing mode. And it needs to know when to stop editing. This should work:

.. code-block:: none

   {
       "prompt":     "FIXME: It is good.@STOP!!", 
       "completion": "It's good.", 
   }

(After finishing the experiment I realized that the "primordial soup" approach might
actually work, after all. If you've got hundreds of examples where the completion is
very similar to the prompt, the LLM might learn through the fine-tuning process that
its role is to just edit the prompt.)

Every prompt that I send to the LLM will have to include ``FIXME: `` and ``@STOP!!`` in
order to activate the LLM's editor mode. There are probably better ways to do this.
But this is good enough for a first prototype.

Now I need to prepare the training data. OpenAI says to use a few hundred examples but
I'm going to see if I can get away with only 10. I'm going to hack together a little
Python script to automate the formatting of the training data and creation of the JSONL
file. I'll skip those implementation details but the source code is in my
`technicalwriting/hank`_ repository.

The final training data that I feed to OpenAI looks like this:

.. code-block:: none

   {
       "prompt": "FIXME: It is possible to fine-tune an LLM to enforce a style guide.@STOP!!",
       "completion": " It's possible to fine-tune an LLM to enforce a style guide."
   }
   {
       "prompt": "FIXME: It is raining men, hallelujah@STOP!!",
       "completion": " It's raining men, hallelujah"
   }
   {
       "prompt": "FIXME: I think it is Travis.@STOP!!", 
       "completion": " I think it's Travis."
   }
   {
       "prompt": "FIXME: I can't believe it is not butter!@STOP!!",
       "completion": " I can't believe it's not butter!"
   }
   {
       "prompt": "FIXME: The problem is that it is a complicated sentence.@STOP!!",
       "completion": " The problem is that it's a complicated sentence."
   }
   ...

Assessing the first attempt
===========================

After using the OpenAI CLI tool to upload the data and create the fine-tuned
model, I can try out the new model in the OpenAI Playground!

<img src="/assets/playground.png"
     alt="The text 'FIXME: I hope that it is working.@STOP!!' was inserted into the OpenAI
          Playground. The fine-tuned model responded with 'I hope that it's working.' as expected."/>

``FIXME: I hope that it is working.@STOP!!`` is the text that I entered. After clicking
``Submit`` the LLM responded with ``I hope that it's working.`` So it seems like it worked!

Configuration tweaks to note:

* I dropped **Temperature** to `0` to get more deterministic responses.
* I added `@STOP!!` to the **Stop sequences** field as a clue that the LLM
  should stop generating text when it encounters that sequence.
* I set the **Maximum length** to `100` simply because all of my examples are small
  and I currently never need a response bigger than 100 tokens.

Let's try some more. There are some instances of ``it is`` that should not get
changed. For example, ``tell it like it is`` shouldn't get edited to
``tell it like it's``.

(Now that you're familiar with the OpenAI Playground UI, I'm just going to show the
prompts and completions as text.)

.. code-block:: none

   FIXME: I hope that my fine-tuned LLM keeps this text as it is.@STOP!!
   I hope that my fine-tuned LLM keeps this text as it is.
   I hope that my fine-tuned LLM keeps this text as it is.
   I hope that my fine-tuned LLM keeps this text as it is.
   I hope that my fine-tuned LLM keeps this text as it is.
   I hope that my fine-tuned LLM keeps this text as it is.
   I hope that my fine-tuned LLM keeps this text as it

(I am changing the line breaks for readability.)

Well, the good news is that it kept ``it is``. The bad news is that the text is
repeating. I have seen this before. I thought that setting the **Stop sequences**
field to ``@STOP!!`` would prevent it from happening. The stop sequence thing worked
in the first attempt. But now the "repeating text" problem is back. It's annoying
but there are probably workarounds so I don't think it's a dealbreaker.

How about a contraction that doesn't appear in my training data like ``what is``?
Will the LLM change it to ``what's``?

```
FIXME: What is the LLM going to do?@STOP!! What's the LLM going to do?
```

The LLM changed ``What is`` to ``What's`` even though that rule isn't in the training data!
I also tried ``you are`` and the same thing happened. The LLM seems to have extrapolated
that the real rule is "use contractions". It did not limit itself strictly to what it
saw in the training data. Is that a blessing or a curse? Last, the repeating text
problem is gone.

Second attempt
==============

Next I tried adding another rule. I added training data to remove ``please``.
I created only 5 examples.

.. code-block:: none

   {
       "prompt":     "Please click the button.",
       "completion": "Click the button."
   },
   {
       "prompt":     "To run the job, please select Go.",
       "completion": "To run the job, select Go."
   },
   {
       "prompt":     "Please enter your username.",
       "completion": "Enter your username."
   },
   {
       "prompt":     "Please note that the feature is now generally available.",
       "completion": "Note that the feature is now generally available."
   },
   {
       "prompt":     "For more information, please see the FAQ.",
       "completion": "For more information, see the FAQ."
   }

I think there is a way to continue training the first fine-tuned model that I created,
but I'll just create a new one because that seems less prone to pilot error. The new one
will have both the ``it is`` training data in addition to this new ``please`` data.

First I test the ``please`` rule by itself:

.. code-block:: none

   FIXME: Please configure the app to run on HTTPS only.@STOP!!
   Please configure the app to run on HTTPS only.

It didn't work. 5 examples is probably just not enough. I added
5 more examples, went through the rigmarole of creating a new fine-tuned
model, and then tried again:

.. code-block:: none

   FIXME: Please configure the app to run on HTTPS only.@STOP!!
   Configure the app to run on HTTPS only. Configure the app to run on HTTPS only.
   Configure the app to run on HTTPS only. Configure the app to run on HTTPS only.
   ...

The repeating text problem happened again. But the ``please`` was deleted!

Subsequent tests had the same behavior. Another problem that popped up: sometimes
the ``@STOP!!`` sequence was not removed from the output, like this:

.. code-block:: none

   FIXME: Remember to please return to your car.@STOP!! Remember to return to your car.@STOP!

That second ``@STOP!!`` at the very end shouldn't be there.

Finally, I tested the ``it is`` and ``please`` rules together:

.. code-block:: none

   FIXME: Please remember that it is not a toy.@STOP!!
   Remember that it's not a toy. STOP: Remember that it's not a toy. STOP:
   Remember that it's not a toy. STOP: Remember that it's not a toy. STOP: 
   ...

Yes, the fine-tuned LLLM "remembered" both rules! OK, I've seen enough.
Let's wrap this up.

----
Cost
----

I can't pinpoint the exact cost because I've been doing a lot of experimentation
of different ideas over the last month but I can tell you that my total cost so
far is $1.37. Ballpark estimate, this fine-tuning experimentation cost $1.

-------------------
Concluding thoughts
-------------------

* I think the "fine-tuning an LLM into a style guide editor" thing can work.
  I'm going to keep hacking on it. You can follow my progress in this repo:
  [technicalwriting/hank]
* The fact that I started to see results with only 10 examples for each rule
  suggests to me that this thing will work robustly if I train it properly
  on hundreds of examples for each rule, as OpenAI recommends.
* When I prepare the training data, I need to make sure that I provide examples on both
  when to enforce the rule and when not to enforce the rule. For example, the
  LLM shouldn't always edit ``it is`` down to ``it's``.
* This approach seems like it has great potential for collaboration across the
  technical writing community because the heart of the work is the training data,
  and that can just be "before" and "after" text in a spreadsheet. The linter
  approach requires programming and regex. REGEX! The training data is just words.
  Maybe we will see huge, open source training datasets for style guide rules. You'll
  be able to mix and match by just grabbing the training data for only the rules
  that your style guide follows. Maybe I'll submit this as a
  [Write The Docs Portland 2023 Writing Day] project...
* I need to research OpenAI's models to figure out which one is best suited
  for this job. I just defaulted to ``ada`` because it seemed cheap and well-supported.
  Also, in the OpenAI Playground I noticed that OpenAI has a beta model that is
  specifically designed for editing.

.. _ft: https://platform.openai.com/docs/guides/fine-tuning
.. _chrome-devrel-review-bot: https://github.com/GoogleChromeLabs/chrome-devrel-review-bot
.. _etymology of "behemoth": https://www.etymonline.com/word/behemoth
.. _awesome. Awesome to the max.: https://youtu.be/K0ll5yizGLo
.. _Context injection versus fine-tuning: /posts/playing-nicely-with-generative-ai/#context-injection-versus-fine-tuning
.. _JSONL: https://jsonlines.org/
.. _That's an excellent question. I have no idea.: https://youtu.be/Ig6iSbqPcKw
.. _General best practices: https://platform.openai.com/docs/guides/fine-tuning/general-best-practices
.. _Preparing your dataset: https://platform.openai.com/docs/guides/fine-tuning/preparing-your-dataset
.. _Specific guidelines: https://platform.openai.com/docs/guides/fine-tuning/specific-guidelines
.. _technicalwriting/hank: https://github.com/technicalwriting/hank
.. _Potential impact of generative AI on technical writing: /posts/generative-ai/
.. _Knowledge Retrieval Architecture for LLMs: https://mattboegner.com/knowledge-retrieval-architecture-for-llms/
.. _Write The Docs Portland 2023 Writing Day: https://www.writethedocs.org/conf/portland/2022/writing-day/
