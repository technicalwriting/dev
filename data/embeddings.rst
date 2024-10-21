.. _embeddings:

=========================
Embeddings are underrated
=========================

Machine learning (ML) has the potential to advance the state of the
art in technical writing. No, I'm not talking about text generation models
like Claude Opus, Gemini Pro, LLaMa, etc. The ML technology that might end up
having the biggest impact on technical writing is **embeddings**.

.. raw:: html

   Embeddings aren't exactly new, but they have become much more widely
   accessible in the last couple years. What embeddings offer to technical
   writers is <b><i>the ability to discover connections between texts at
   previously impossible scales</i></b>.

.. _embeddings-intuition:

-----------------------------------
Building intuition about embeddings
-----------------------------------

I suspect that most of my fellow technical writers aren't familiar
with embeddings, so here's an overview of how you use them and how they work.

.. _embeddings-intuition-i/o:

Input and output
================

Someone asks you to "make some embeddings". What do you input? You input
text. It could be a single word, or sentence, or paragraph, or section,
or document, or set of documents, etc. You don't need to provide the same
amount of text every time.

.. _array: https://www.geeksforgeeks.org/what-is-array/

What do you get back? If you provide a single word as the
input, the output will be an array of numbers like this:

.. code-block:: text

   [-0.02387, -0.0353, 0.0456]

Now suppose your input is an entire set of documents. The output
turns into this:

.. code-block:: text

   [0.0451, -0.0154, 0.0020]

A little strange, right? One input was drastically smaller than the
other, yet they both produced an array of 3 numbers.
(When you work with real embeddings, the arrays will have
hundreds or thousands of numbers, not 3. More on that later.)

Here's the first key insight. Because we always get back the same amount of
numbers no matter how big or small the input text, **we now have a way to
mathematically compare any two pieces of arbitrary text to each other**.

Huh? How is this? Why would I want to use *math* to compare *docs*?
And what do those numbers *MEAN*??

.. _embeddings-intuition-api:

But first, how to literally make the embeddings
===============================================

The big service providers have made it very easy.
Here's how it's done with Gemini:

.. code-block:: py

   import google.generativeai as gemini


   gemini.configure(api_key='…')

   text = 'Hello, world!'
   response = gemini.embed_content(
       model='models/text-embedding-004',
       content=text,
       task_type='SEMANTIC_SIMILARITY'
   )
   embedding = response['embedding']

.. _text-embedding-004: https://ai.google.dev/gemini-api/docs/models/gemini#text-embedding
.. _voyage-3: https://docs.voyageai.com/docs/embeddings

The size of the array depends on what model you're using.
Gemini's `text-embedding-004`_ returns an array of 768 numbers whereas
Voyage AI's `voyage-3`_ returns an array of 1024 numbers. This is one of the
reasons why you can't use embeddings from different providers
interchangeably. (The other and main reason is that the numbers from
one model mean something completely different than the numbers from
another model.)

Does it cost a lot of money?
----------------------------

No.

What model is best?
-------------------

Ideally, your embedding model can accept a huge amount of input text,
so that you never need to worry about it erroring out because you fed
it too much text. As of October 2024 ``voyage-3`` is the
clear winner.

.. csv-table::
   :header: Organization, Model Name, Input Limit

   Voyage AI, `voyage-3 <https://docs.voyageai.com/docs/embeddings>`_, 32000
   Nomic, `Embed <https://www.nomic.ai/blog/posts/nomic-embed-text-v1>`__, 8192
   Mistral, `Embed <https://docs.mistral.ai/getting-started/models/models_overview/#premier-models>`__, 8000
   OpenAI, `text-embedding-3-large <https://platform.openai.com/docs/models/embeddings>`_, 3072
   Google, `text-embedding-004`_, 2048
   Cohere, `embed-english-v3.0 <https://docs.cohere.com/v2/docs/models#embed>`_, 512
   

.. _embeddings-intuition-meaning:

Very weird multi-dimensional space
==================================

Back to the big mystery. What the hell do these numbers **MEAN**?!?!?!

I'm no expert here, but for our purposes of building very basic intution,
I'm fairly confident that it's safe to begin our journey by thinking about
**coordinates on a map**.

Suppose I give you three points and their coordinates:

.. csv-table::
   :header: Point, X-Coordinate, Y-Coordinate

   A, 3, 2
   B, 1, 1
   C, -2, -2

There are 2 dimensions to this map: the X-Coordinate and the
Y-Coordinate. Each point lives at the intersection of an X-Coordinate
and a Y-Coordinate.

Is A closer to B or C?

.. plot::
   :show-source-link: False
   :include-source: False

   import matplotlib.pyplot as plt
   import networkx as nx


   graph = nx.Graph()

   graph.add_node("A", pos=(3, 2))
   graph.add_node("B", pos=(1, 1))
   graph.add_node("C", pos=(-2, -2))

   pos = nx.get_node_attributes(graph, 'pos')  # Get node positions
   x_coords = [pos[node][0] for node in graph.nodes()]
   y_coords = [pos[node][1] for node in graph.nodes()]
   x_min, x_max = min(x_coords) - 1, max(x_coords) + 1
   y_min, y_max = min(y_coords) - 1, max(y_coords) + 1

   nx.draw(graph, pos, with_labels=True, node_size=500, node_color="skyblue")
   labels = {}
   for node in graph.nodes():
       labels[node] = node
   nx.draw_networkx_labels(graph, pos, labels, font_size=12)

   plt.plot([x_min, x_max], [0, 0], color='gray', linestyle='--', linewidth=0.5)  # x-axis
   plt.plot([0, 0], [y_min, y_max], color='gray', linestyle='--', linewidth=0.5)  # y-axis
   plt.xlim(x_min, x_max)
   plt.ylim(y_min, y_max)

   plt.show()

A is much closer to B.

.. _latent space: https://en.wikipedia.org/wiki/Latent_space

Here's the mental leap. *This is basically how embeddings work*.
Each number in the embedding array is a *dimension*, similar to our
X-Coordinates and Y-Coordinates, similar to how we physically live
in 3-dimensional space on Earth. When an embedding model sends you back an
array of 1000 numbers, it's telling you the point where that text
semantically lives in its 1000-dimension space, relative to all other
texts. 

.. figure:: /_static/mindblown.gif

.. _Word2vec paper: https://arxiv.org/pdf/1301.3781

The concept of positioning items in a multi-dimensional
space like this, where related items are clustered near each other,
goes by the wonderful name of `latent space`_.

The most famous example of the weird utility of this technology comes from
the `Word2vec paper`_, the foundational research that kickstarted interest
in embeddings 11 years ago. In the paper they shared this anecdote:

.. code-block:: text

   embedding("king") - embedding("man") + embedding("woman") ≈ embedding("queen")

Starting with the embedding for ``king``, subtract the embedding for ``man``,
then add the embedding for ``woman``. When you look around this vicinity of the
latent space, you find the embedding for ``queen`` nearby.

There appears to be an unspoken rule in ML culture that this anecdote must
always be followed by this quote from John Rupert Firth:

  You shall know a word by the company it keeps!

We started the section by thinking about distance between points on a 2D map.
It was a nice stepping stone for building intuition but now we need
to cast it aside, because embeddings operate in hundreds or thousands
of dimensions. It's (probably) impossible to visualize what "distance" looks
like in 1000 dimensions. Also, we don't know what each dimension represents,
hence the section heading "Very weird multi-dimensional space".\ :sup:`1`
One dimension might represent something close to color, another might
represent size, etc. ML researchers are still figuring that out.

.. _The Illustrated Word2vec: https://jalammar.github.io/illustrated-word2vec/

The mechanics of converting text into very weird multi-dimensional space are
complex, as you might imagine. They are teaching *machines* to *learn*, after all.
`The Illustrated Word2vec`_ is a good way to start your journey down that
rabbithole.

:sup:`1` I borrowed this phrase from `Embeddings: What they are why they
matter <https://simonwillison.net/2023/Oct/23/embeddings/>`_.

.. _embeddings-applications:

------------
Applications
------------

I could tell you exactly how I think we might advance the state of the art
in technical writing with embeddings, but where's the fun in that? 
Let's cover a basic example to put the intuition-building ideas into
practice and then wrap up this post.

Related pages
=============

Some docs sites have a recommendation system that makes you aware of other
relevant docs. The system looks at whatever page you're currently on, finds
other pages related to this one, and then recommends other pages to visit.
Embeddings provide a new way to support this feature, probably at a fraction
of the cost of previous methods. Here's how it works:

1. Generate an embedding for each page on your docs site.
2. For each page, compare its embedding against all other page embeddings
   in order to find what other pages are most related to this one.

This can be done as a batch operation. A page's embedding only needs to
change when the page's content changes.

.. _Sphinx: https://www.sphinx-doc.org/en/master/

I ran this experiment on the `Sphinx`_ docs. The results were pretty good.
:ref:`embeddings-appendix-implementation` and
:ref:`embeddings-appendix-results` have the details.

.. _Related content using embeddings: https://simonwillison.net/2023/Oct/23/embeddings/#related-content-using-embeddings

See `Related content using embeddings`_ for another example of this approach.

-------------
Parting words
-------------

Three years ago, if you had asked me what 768-dimensional space is,
I would have told you that it's just some abstract concept that physicists
and mathematicians need for unfathomable reasons. Embeddings gave me a reason
to think about this idea more deeply, and actually apply it to my own work.
I think that's beautiful.

Order-of-magnitude improvements in our ability to maintain our docs
may very well still be possible after all… perhaps we just need
an order-of-magnitude-more dimensions!!

.. _embeddings-appendix:

--------
Appendix
--------

.. _embeddings-appendix-implementation:

Implementation
==============

.. _Sphinx extension: https://www.sphinx-doc.org/en/master/development/tutorials/extending_build.html

I created a `Sphinx extension`_ to generate an embedding for each doc. Sphinx automatically invokes
this extension as it builds the docs.

.. code-block:: py

   import json
   import os


   import voyageai


   VOYAGE_API_KEY = os.getenv('VOYAGE_API_KEY')
   voyage = voyageai.Client(api_key=VOYAGE_API_KEY)


   def on_build_finished(app, exception):
       with open(srcpath, 'w') as f:
           json.dump(data, f, indent=4)


   def embed_with_voyage(text):
       try:
           embedding = voyage.embed([text], model='voyage-3', input_type='document').embeddings[0]
           return embedding
       except Exception as e:
           return None


   def on_doctree_resolved(app, doctree, docname):
       text = doctree.astext()
       embedding = embed_with_voyage(text)  # Generate an embedding for each document!
       data[docname] = {
           'embedding': embedding
       }


   # Use some globals because this is just an experiment and you can't stop me
   def init_globals(srcdir):
       global filename
       global srcpath
       global data
       filename = 'embeddings.json'
       srcpath = f'{srcdir}/{filename}'
       data = {}


   def setup(app):
       init_globals(app.srcdir)
       # https://www.sphinx-doc.org/en/master/extdev/appapi.html#sphinx-core-events
       app.connect('doctree-resolved', on_doctree_resolved)  # This event fires on every doc that's processed
       app.connect('build-finished', on_build_finished)
       return {
           'version': '0.0.1',
           'parallel_read_safe': True,
           'parallel_write_safe': True,
       }

When the build finishes, the embeddings data is stored in ``embeddings.json`` like this:

.. code-block:: text

   {
       "authors": {
           "embedding": […]
       },
       "changes/0.1": {
           "embedding": […]
       },
       …
   }

``authors`` and ``changes/0.1`` are docs. ``embedding`` contains the
embedding for that doc.

.. _Linear Algebra for Machine Learning and Data Science: https://www.coursera.org/learn/machine-learning-linear-algebra

The last step is to find the closest neighbor for each doc. I.e. to
find the other page that is considered relevant to the page you're currently on.
`Linear Algebra for Machine Learning and Data Science`_ gave me a basic idea
of what this math does.

.. code-block:: py

   import json


   import numpy as np
   from sklearn.metrics.pairwise import cosine_similarity


   def find_docname(data, target):
       for docname in data:
           if data[docname]['embedding'] == target:
               return docname
       return None


   # Adapted from the Voyage AI docs
   # https://web.archive.org/web/20240923001107/https://docs.voyageai.com/docs/quickstart-tutorial
   def k_nearest_neighbors(target, embeddings, k=5):
       # Convert to numpy array
       target = np.array(target)
       embeddings = np.array(embeddings)
       # Reshape the query vector embedding to a matrix of shape (1, n) to make it 
       # compatible with cosine_similarity
       target = target.reshape(1, -1)
       # Calculate the similarity for each item in data
       cosine_sim = cosine_similarity(target, embeddings)
       # Sort the data by similarity in descending order and take the top k items
       sorted_indices = np.argsort(cosine_sim[0])[::-1]
       # Take the top k related embeddings
       top_k_related_embeddings = embeddings[sorted_indices[:k]]
       top_k_related_embeddings = [
           list(row[:]) for row in top_k_related_embeddings
       ]  # convert to list
       return top_k_related_embeddings


   with open('doc/embeddings.json', 'r') as f:
       data = json.load(f)
   embeddings = [data[docname]['embedding'] for docname in data]
   print('.. csv-table::')
   print('   :header: "Target", "Neighbor"')
   print()
   for target in embeddings:
       dot_products = np.dot(embeddings, target)
       neighbors = k_nearest_neighbors(target, embeddings, k=3)
       # ignore neighbors[0] because that is always the target itself
       nearest_neighbor = neighbors[1]
       target_docname = find_docname(data, target)
       target_cell = f'`{target_docname} <https://www.sphinx-doc.org/en/master/{target_docname}.html>`_'
       neighbor_docname = find_docname(data, nearest_neighbor)
       neighbor_cell = f'`{neighbor_docname} <https://www.sphinx-doc.org/en/master/{neighbor_docname}.html>`_'
       print(f'   "{target_cell}", "{neighbor_cell}"')

As you may have noticed, I did not actually implement the recommendation
UI in this experiment. My main goal was to get basic data on whether
the embeddings approach generates decent recommendations or not.

.. _embeddings-appendix-results:

Results
=======

How to interpret the data: ``Target`` would be the page that you're
currently on. ``Neighbor`` would be the recommended page.

.. csv-table::
   :header: "Target", "Neighbor"

   "`authors <https://www.sphinx-doc.org/en/master/authors.html>`_", "`changes/0.6 <https://www.sphinx-doc.org/en/master/changes/0.6.html>`_"
   "`changes/0.1 <https://www.sphinx-doc.org/en/master/changes/0.1.html>`_", "`changes/0.5 <https://www.sphinx-doc.org/en/master/changes/0.5.html>`_"
   "`changes/0.2 <https://www.sphinx-doc.org/en/master/changes/0.2.html>`_", "`changes/1.2 <https://www.sphinx-doc.org/en/master/changes/1.2.html>`_"
   "`changes/0.3 <https://www.sphinx-doc.org/en/master/changes/0.3.html>`_", "`changes/0.4 <https://www.sphinx-doc.org/en/master/changes/0.4.html>`_"
   "`changes/0.4 <https://www.sphinx-doc.org/en/master/changes/0.4.html>`_", "`changes/1.2 <https://www.sphinx-doc.org/en/master/changes/1.2.html>`_"
   "`changes/0.5 <https://www.sphinx-doc.org/en/master/changes/0.5.html>`_", "`changes/0.6 <https://www.sphinx-doc.org/en/master/changes/0.6.html>`_"
   "`changes/0.6 <https://www.sphinx-doc.org/en/master/changes/0.6.html>`_", "`changes/1.6 <https://www.sphinx-doc.org/en/master/changes/1.6.html>`_"
   "`changes/1.0 <https://www.sphinx-doc.org/en/master/changes/1.0.html>`_", "`changes/1.3 <https://www.sphinx-doc.org/en/master/changes/1.3.html>`_"
   "`changes/1.1 <https://www.sphinx-doc.org/en/master/changes/1.1.html>`_", "`changes/1.2 <https://www.sphinx-doc.org/en/master/changes/1.2.html>`_"
   "`changes/1.2 <https://www.sphinx-doc.org/en/master/changes/1.2.html>`_", "`changes/1.1 <https://www.sphinx-doc.org/en/master/changes/1.1.html>`_"
   "`changes/1.3 <https://www.sphinx-doc.org/en/master/changes/1.3.html>`_", "`changes/1.4 <https://www.sphinx-doc.org/en/master/changes/1.4.html>`_"
   "`changes/1.4 <https://www.sphinx-doc.org/en/master/changes/1.4.html>`_", "`changes/1.3 <https://www.sphinx-doc.org/en/master/changes/1.3.html>`_"
   "`changes/1.5 <https://www.sphinx-doc.org/en/master/changes/1.5.html>`_", "`changes/1.6 <https://www.sphinx-doc.org/en/master/changes/1.6.html>`_"
   "`changes/1.6 <https://www.sphinx-doc.org/en/master/changes/1.6.html>`_", "`changes/1.5 <https://www.sphinx-doc.org/en/master/changes/1.5.html>`_"
   "`changes/1.7 <https://www.sphinx-doc.org/en/master/changes/1.7.html>`_", "`changes/1.8 <https://www.sphinx-doc.org/en/master/changes/1.8.html>`_"
   "`changes/1.8 <https://www.sphinx-doc.org/en/master/changes/1.8.html>`_", "`changes/1.6 <https://www.sphinx-doc.org/en/master/changes/1.6.html>`_"
   "`changes/2.0 <https://www.sphinx-doc.org/en/master/changes/2.0.html>`_", "`changes/1.8 <https://www.sphinx-doc.org/en/master/changes/1.8.html>`_"
   "`changes/2.1 <https://www.sphinx-doc.org/en/master/changes/2.1.html>`_", "`changes/1.2 <https://www.sphinx-doc.org/en/master/changes/1.2.html>`_"
   "`changes/2.2 <https://www.sphinx-doc.org/en/master/changes/2.2.html>`_", "`changes/1.2 <https://www.sphinx-doc.org/en/master/changes/1.2.html>`_"
   "`changes/2.3 <https://www.sphinx-doc.org/en/master/changes/2.3.html>`_", "`changes/2.1 <https://www.sphinx-doc.org/en/master/changes/2.1.html>`_"
   "`changes/2.4 <https://www.sphinx-doc.org/en/master/changes/2.4.html>`_", "`changes/3.5 <https://www.sphinx-doc.org/en/master/changes/3.5.html>`_"
   "`changes/3.0 <https://www.sphinx-doc.org/en/master/changes/3.0.html>`_", "`changes/4.3 <https://www.sphinx-doc.org/en/master/changes/4.3.html>`_"
   "`changes/3.1 <https://www.sphinx-doc.org/en/master/changes/3.1.html>`_", "`changes/3.3 <https://www.sphinx-doc.org/en/master/changes/3.3.html>`_"
   "`changes/3.2 <https://www.sphinx-doc.org/en/master/changes/3.2.html>`_", "`changes/3.0 <https://www.sphinx-doc.org/en/master/changes/3.0.html>`_"
   "`changes/3.3 <https://www.sphinx-doc.org/en/master/changes/3.3.html>`_", "`changes/3.1 <https://www.sphinx-doc.org/en/master/changes/3.1.html>`_"
   "`changes/3.4 <https://www.sphinx-doc.org/en/master/changes/3.4.html>`_", "`changes/4.3 <https://www.sphinx-doc.org/en/master/changes/4.3.html>`_"
   "`changes/3.5 <https://www.sphinx-doc.org/en/master/changes/3.5.html>`_", "`changes/1.3 <https://www.sphinx-doc.org/en/master/changes/1.3.html>`_"
   "`changes/4.0 <https://www.sphinx-doc.org/en/master/changes/4.0.html>`_", "`changes/3.0 <https://www.sphinx-doc.org/en/master/changes/3.0.html>`_"
   "`changes/4.1 <https://www.sphinx-doc.org/en/master/changes/4.1.html>`_", "`changes/4.4 <https://www.sphinx-doc.org/en/master/changes/4.4.html>`_"
   "`changes/4.2 <https://www.sphinx-doc.org/en/master/changes/4.2.html>`_", "`changes/4.4 <https://www.sphinx-doc.org/en/master/changes/4.4.html>`_"
   "`changes/4.3 <https://www.sphinx-doc.org/en/master/changes/4.3.html>`_", "`changes/3.0 <https://www.sphinx-doc.org/en/master/changes/3.0.html>`_"
   "`changes/4.4 <https://www.sphinx-doc.org/en/master/changes/4.4.html>`_", "`changes/7.4 <https://www.sphinx-doc.org/en/master/changes/7.4.html>`_"
   "`changes/4.5 <https://www.sphinx-doc.org/en/master/changes/4.5.html>`_", "`changes/4.4 <https://www.sphinx-doc.org/en/master/changes/4.4.html>`_"
   "`changes/5.0 <https://www.sphinx-doc.org/en/master/changes/5.0.html>`_", "`changes/3.5 <https://www.sphinx-doc.org/en/master/changes/3.5.html>`_"
   "`changes/5.1 <https://www.sphinx-doc.org/en/master/changes/5.1.html>`_", "`changes/5.0 <https://www.sphinx-doc.org/en/master/changes/5.0.html>`_"
   "`changes/5.2 <https://www.sphinx-doc.org/en/master/changes/5.2.html>`_", "`changes/3.5 <https://www.sphinx-doc.org/en/master/changes/3.5.html>`_"
   "`changes/5.3 <https://www.sphinx-doc.org/en/master/changes/5.3.html>`_", "`changes/5.2 <https://www.sphinx-doc.org/en/master/changes/5.2.html>`_"
   "`changes/6.0 <https://www.sphinx-doc.org/en/master/changes/6.0.html>`_", "`changes/6.2 <https://www.sphinx-doc.org/en/master/changes/6.2.html>`_"
   "`changes/6.1 <https://www.sphinx-doc.org/en/master/changes/6.1.html>`_", "`changes/6.2 <https://www.sphinx-doc.org/en/master/changes/6.2.html>`_"
   "`changes/6.2 <https://www.sphinx-doc.org/en/master/changes/6.2.html>`_", "`changes/6.1 <https://www.sphinx-doc.org/en/master/changes/6.1.html>`_"
   "`changes/7.0 <https://www.sphinx-doc.org/en/master/changes/7.0.html>`_", "`extdev/deprecated <https://www.sphinx-doc.org/en/master/extdev/deprecated.html>`_"
   "`changes/7.1 <https://www.sphinx-doc.org/en/master/changes/7.1.html>`_", "`changes/7.2 <https://www.sphinx-doc.org/en/master/changes/7.2.html>`_"
   "`changes/7.2 <https://www.sphinx-doc.org/en/master/changes/7.2.html>`_", "`changes/7.4 <https://www.sphinx-doc.org/en/master/changes/7.4.html>`_"
   "`changes/7.3 <https://www.sphinx-doc.org/en/master/changes/7.3.html>`_", "`changes/7.4 <https://www.sphinx-doc.org/en/master/changes/7.4.html>`_"
   "`changes/7.4 <https://www.sphinx-doc.org/en/master/changes/7.4.html>`_", "`changes/7.3 <https://www.sphinx-doc.org/en/master/changes/7.3.html>`_"
   "`changes/8.0 <https://www.sphinx-doc.org/en/master/changes/8.0.html>`_", "`changes/8.1 <https://www.sphinx-doc.org/en/master/changes/8.1.html>`_"
   "`changes/8.1 <https://www.sphinx-doc.org/en/master/changes/8.1.html>`_", "`changes/1.8 <https://www.sphinx-doc.org/en/master/changes/1.8.html>`_"
   "`changes/index <https://www.sphinx-doc.org/en/master/changes/index.html>`_", "`changes/8.0 <https://www.sphinx-doc.org/en/master/changes/8.0.html>`_"
   "`development/howtos/builders <https://www.sphinx-doc.org/en/master/development/howtos/builders.html>`_", "`usage/extensions/index <https://www.sphinx-doc.org/en/master/usage/extensions/index.html>`_"
   "`development/howtos/index <https://www.sphinx-doc.org/en/master/development/howtos/index.html>`_", "`development/tutorials/index <https://www.sphinx-doc.org/en/master/development/tutorials/index.html>`_"
   "`development/howtos/setup_extension <https://www.sphinx-doc.org/en/master/development/howtos/setup_extension.html>`_", "`usage/extensions/index <https://www.sphinx-doc.org/en/master/usage/extensions/index.html>`_"
   "`development/html_themes/index <https://www.sphinx-doc.org/en/master/development/html_themes/index.html>`_", "`usage/theming <https://www.sphinx-doc.org/en/master/usage/theming.html>`_"
   "`development/html_themes/templating <https://www.sphinx-doc.org/en/master/development/html_themes/templating.html>`_", "`development/html_themes/index <https://www.sphinx-doc.org/en/master/development/html_themes/index.html>`_"
   "`development/index <https://www.sphinx-doc.org/en/master/development/index.html>`_", "`usage/index <https://www.sphinx-doc.org/en/master/usage/index.html>`_"
   "`development/tutorials/adding_domain <https://www.sphinx-doc.org/en/master/development/tutorials/adding_domain.html>`_", "`extdev/domainapi <https://www.sphinx-doc.org/en/master/extdev/domainapi.html>`_"
   "`development/tutorials/autodoc_ext <https://www.sphinx-doc.org/en/master/development/tutorials/autodoc_ext.html>`_", "`usage/extensions/autodoc <https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html>`_"
   "`development/tutorials/examples/README <https://www.sphinx-doc.org/en/master/development/tutorials/examples/README.html>`_", "`tutorial/end <https://www.sphinx-doc.org/en/master/tutorial/end.html>`_"
   "`development/tutorials/extending_build <https://www.sphinx-doc.org/en/master/development/tutorials/extending_build.html>`_", "`usage/extensions/todo <https://www.sphinx-doc.org/en/master/usage/extensions/todo.html>`_"
   "`development/tutorials/extending_syntax <https://www.sphinx-doc.org/en/master/development/tutorials/extending_syntax.html>`_", "`extdev/markupapi <https://www.sphinx-doc.org/en/master/extdev/markupapi.html>`_"
   "`development/tutorials/index <https://www.sphinx-doc.org/en/master/development/tutorials/index.html>`_", "`development/howtos/index <https://www.sphinx-doc.org/en/master/development/howtos/index.html>`_"
   "`examples <https://www.sphinx-doc.org/en/master/examples.html>`_", "`index <https://www.sphinx-doc.org/en/master/index.html>`_"
   "`extdev/appapi <https://www.sphinx-doc.org/en/master/extdev/appapi.html>`_", "`extdev/index <https://www.sphinx-doc.org/en/master/extdev/index.html>`_"
   "`extdev/builderapi <https://www.sphinx-doc.org/en/master/extdev/builderapi.html>`_", "`usage/builders/index <https://www.sphinx-doc.org/en/master/usage/builders/index.html>`_"
   "`extdev/collectorapi <https://www.sphinx-doc.org/en/master/extdev/collectorapi.html>`_", "`extdev/envapi <https://www.sphinx-doc.org/en/master/extdev/envapi.html>`_"
   "`extdev/deprecated <https://www.sphinx-doc.org/en/master/extdev/deprecated.html>`_", "`changes/1.8 <https://www.sphinx-doc.org/en/master/changes/1.8.html>`_"
   "`extdev/domainapi <https://www.sphinx-doc.org/en/master/extdev/domainapi.html>`_", "`usage/domains/index <https://www.sphinx-doc.org/en/master/usage/domains/index.html>`_"
   "`extdev/envapi <https://www.sphinx-doc.org/en/master/extdev/envapi.html>`_", "`extdev/collectorapi <https://www.sphinx-doc.org/en/master/extdev/collectorapi.html>`_"
   "`extdev/event_callbacks <https://www.sphinx-doc.org/en/master/extdev/event_callbacks.html>`_", "`extdev/appapi <https://www.sphinx-doc.org/en/master/extdev/appapi.html>`_"
   "`extdev/i18n <https://www.sphinx-doc.org/en/master/extdev/i18n.html>`_", "`usage/advanced/intl <https://www.sphinx-doc.org/en/master/usage/advanced/intl.html>`_"
   "`extdev/index <https://www.sphinx-doc.org/en/master/extdev/index.html>`_", "`extdev/appapi <https://www.sphinx-doc.org/en/master/extdev/appapi.html>`_"
   "`extdev/logging <https://www.sphinx-doc.org/en/master/extdev/logging.html>`_", "`extdev/appapi <https://www.sphinx-doc.org/en/master/extdev/appapi.html>`_"
   "`extdev/markupapi <https://www.sphinx-doc.org/en/master/extdev/markupapi.html>`_", "`development/tutorials/extending_syntax <https://www.sphinx-doc.org/en/master/development/tutorials/extending_syntax.html>`_"
   "`extdev/nodes <https://www.sphinx-doc.org/en/master/extdev/nodes.html>`_", "`extdev/domainapi <https://www.sphinx-doc.org/en/master/extdev/domainapi.html>`_"
   "`extdev/parserapi <https://www.sphinx-doc.org/en/master/extdev/parserapi.html>`_", "`extdev/appapi <https://www.sphinx-doc.org/en/master/extdev/appapi.html>`_"
   "`extdev/projectapi <https://www.sphinx-doc.org/en/master/extdev/projectapi.html>`_", "`extdev/envapi <https://www.sphinx-doc.org/en/master/extdev/envapi.html>`_"
   "`extdev/testing <https://www.sphinx-doc.org/en/master/extdev/testing.html>`_", "`internals/contributing <https://www.sphinx-doc.org/en/master/internals/contributing.html>`_"
   "`extdev/utils <https://www.sphinx-doc.org/en/master/extdev/utils.html>`_", "`extdev/appapi <https://www.sphinx-doc.org/en/master/extdev/appapi.html>`_"
   "`faq <https://www.sphinx-doc.org/en/master/faq.html>`_", "`usage/configuration <https://www.sphinx-doc.org/en/master/usage/configuration.html>`_"
   "`glossary <https://www.sphinx-doc.org/en/master/glossary.html>`_", "`usage/quickstart <https://www.sphinx-doc.org/en/master/usage/quickstart.html>`_"
   "`index <https://www.sphinx-doc.org/en/master/index.html>`_", "`usage/quickstart <https://www.sphinx-doc.org/en/master/usage/quickstart.html>`_"
   "`internals/code-of-conduct <https://www.sphinx-doc.org/en/master/internals/code-of-conduct.html>`_", "`internals/index <https://www.sphinx-doc.org/en/master/internals/index.html>`_"
   "`internals/contributing <https://www.sphinx-doc.org/en/master/internals/contributing.html>`_", "`usage/advanced/intl <https://www.sphinx-doc.org/en/master/usage/advanced/intl.html>`_"
   "`internals/index <https://www.sphinx-doc.org/en/master/internals/index.html>`_", "`usage/index <https://www.sphinx-doc.org/en/master/usage/index.html>`_"
   "`internals/organization <https://www.sphinx-doc.org/en/master/internals/organization.html>`_", "`internals/contributing <https://www.sphinx-doc.org/en/master/internals/contributing.html>`_"
   "`internals/release-process <https://www.sphinx-doc.org/en/master/internals/release-process.html>`_", "`extdev/deprecated <https://www.sphinx-doc.org/en/master/extdev/deprecated.html>`_"
   "`latex <https://www.sphinx-doc.org/en/master/latex.html>`_", "`usage/configuration <https://www.sphinx-doc.org/en/master/usage/configuration.html>`_"
   "`man/index <https://www.sphinx-doc.org/en/master/man/index.html>`_", "`usage/index <https://www.sphinx-doc.org/en/master/usage/index.html>`_"
   "`man/sphinx-apidoc <https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html>`_", "`man/sphinx-autogen <https://www.sphinx-doc.org/en/master/man/sphinx-autogen.html>`_"
   "`man/sphinx-autogen <https://www.sphinx-doc.org/en/master/man/sphinx-autogen.html>`_", "`usage/extensions/autosummary <https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html>`_"
   "`man/sphinx-build <https://www.sphinx-doc.org/en/master/man/sphinx-build.html>`_", "`usage/configuration <https://www.sphinx-doc.org/en/master/usage/configuration.html>`_"
   "`man/sphinx-quickstart <https://www.sphinx-doc.org/en/master/man/sphinx-quickstart.html>`_", "`tutorial/getting-started <https://www.sphinx-doc.org/en/master/tutorial/getting-started.html>`_"
   "`support <https://www.sphinx-doc.org/en/master/support.html>`_", "`tutorial/end <https://www.sphinx-doc.org/en/master/tutorial/end.html>`_"
   "`tutorial/automatic-doc-generation <https://www.sphinx-doc.org/en/master/tutorial/automatic-doc-generation.html>`_", "`usage/extensions/autosummary <https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html>`_"
   "`tutorial/deploying <https://www.sphinx-doc.org/en/master/tutorial/deploying.html>`_", "`tutorial/first-steps <https://www.sphinx-doc.org/en/master/tutorial/first-steps.html>`_"
   "`tutorial/describing-code <https://www.sphinx-doc.org/en/master/tutorial/describing-code.html>`_", "`usage/domains/index <https://www.sphinx-doc.org/en/master/usage/domains/index.html>`_"
   "`tutorial/end <https://www.sphinx-doc.org/en/master/tutorial/end.html>`_", "`usage/index <https://www.sphinx-doc.org/en/master/usage/index.html>`_"
   "`tutorial/first-steps <https://www.sphinx-doc.org/en/master/tutorial/first-steps.html>`_", "`tutorial/getting-started <https://www.sphinx-doc.org/en/master/tutorial/getting-started.html>`_"
   "`tutorial/getting-started <https://www.sphinx-doc.org/en/master/tutorial/getting-started.html>`_", "`tutorial/index <https://www.sphinx-doc.org/en/master/tutorial/index.html>`_"
   "`tutorial/index <https://www.sphinx-doc.org/en/master/tutorial/index.html>`_", "`tutorial/getting-started <https://www.sphinx-doc.org/en/master/tutorial/getting-started.html>`_"
   "`tutorial/more-sphinx-customization <https://www.sphinx-doc.org/en/master/tutorial/more-sphinx-customization.html>`_", "`usage/theming <https://www.sphinx-doc.org/en/master/usage/theming.html>`_"
   "`tutorial/narrative-documentation <https://www.sphinx-doc.org/en/master/tutorial/narrative-documentation.html>`_", "`usage/quickstart <https://www.sphinx-doc.org/en/master/usage/quickstart.html>`_"
   "`usage/advanced/intl <https://www.sphinx-doc.org/en/master/usage/advanced/intl.html>`_", "`internals/contributing <https://www.sphinx-doc.org/en/master/internals/contributing.html>`_"
   "`usage/advanced/websupport/api <https://www.sphinx-doc.org/en/master/usage/advanced/websupport/api.html>`_", "`usage/advanced/websupport/quickstart <https://www.sphinx-doc.org/en/master/usage/advanced/websupport/quickstart.html>`_"
   "`usage/advanced/websupport/index <https://www.sphinx-doc.org/en/master/usage/advanced/websupport/index.html>`_", "`usage/advanced/websupport/quickstart <https://www.sphinx-doc.org/en/master/usage/advanced/websupport/quickstart.html>`_"
   "`usage/advanced/websupport/quickstart <https://www.sphinx-doc.org/en/master/usage/advanced/websupport/quickstart.html>`_", "`usage/advanced/websupport/api <https://www.sphinx-doc.org/en/master/usage/advanced/websupport/api.html>`_"
   "`usage/advanced/websupport/searchadapters <https://www.sphinx-doc.org/en/master/usage/advanced/websupport/searchadapters.html>`_", "`usage/advanced/websupport/api <https://www.sphinx-doc.org/en/master/usage/advanced/websupport/api.html>`_"
   "`usage/advanced/websupport/storagebackends <https://www.sphinx-doc.org/en/master/usage/advanced/websupport/storagebackends.html>`_", "`usage/advanced/websupport/api <https://www.sphinx-doc.org/en/master/usage/advanced/websupport/api.html>`_"
   "`usage/builders/index <https://www.sphinx-doc.org/en/master/usage/builders/index.html>`_", "`usage/configuration <https://www.sphinx-doc.org/en/master/usage/configuration.html>`_"
   "`usage/configuration <https://www.sphinx-doc.org/en/master/usage/configuration.html>`_", "`changes/1.2 <https://www.sphinx-doc.org/en/master/changes/1.2.html>`_"
   "`usage/domains/c <https://www.sphinx-doc.org/en/master/usage/domains/c.html>`_", "`usage/domains/cpp <https://www.sphinx-doc.org/en/master/usage/domains/cpp.html>`_"
   "`usage/domains/cpp <https://www.sphinx-doc.org/en/master/usage/domains/cpp.html>`_", "`usage/domains/c <https://www.sphinx-doc.org/en/master/usage/domains/c.html>`_"
   "`usage/domains/index <https://www.sphinx-doc.org/en/master/usage/domains/index.html>`_", "`extdev/domainapi <https://www.sphinx-doc.org/en/master/extdev/domainapi.html>`_"
   "`usage/domains/javascript <https://www.sphinx-doc.org/en/master/usage/domains/javascript.html>`_", "`usage/domains/python <https://www.sphinx-doc.org/en/master/usage/domains/python.html>`_"
   "`usage/domains/mathematics <https://www.sphinx-doc.org/en/master/usage/domains/mathematics.html>`_", "`usage/referencing <https://www.sphinx-doc.org/en/master/usage/referencing.html>`_"
   "`usage/domains/python <https://www.sphinx-doc.org/en/master/usage/domains/python.html>`_", "`extdev/domainapi <https://www.sphinx-doc.org/en/master/extdev/domainapi.html>`_"
   "`usage/domains/restructuredtext <https://www.sphinx-doc.org/en/master/usage/domains/restructuredtext.html>`_", "`extdev/markupapi <https://www.sphinx-doc.org/en/master/extdev/markupapi.html>`_"
   "`usage/domains/standard <https://www.sphinx-doc.org/en/master/usage/domains/standard.html>`_", "`usage/domains/index <https://www.sphinx-doc.org/en/master/usage/domains/index.html>`_"
   "`usage/extensions/autodoc <https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html>`_", "`tutorial/automatic-doc-generation <https://www.sphinx-doc.org/en/master/tutorial/automatic-doc-generation.html>`_"
   "`usage/extensions/autosectionlabel <https://www.sphinx-doc.org/en/master/usage/extensions/autosectionlabel.html>`_", "`usage/quickstart <https://www.sphinx-doc.org/en/master/usage/quickstart.html>`_"
   "`usage/extensions/autosummary <https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html>`_", "`tutorial/automatic-doc-generation <https://www.sphinx-doc.org/en/master/tutorial/automatic-doc-generation.html>`_"
   "`usage/extensions/coverage <https://www.sphinx-doc.org/en/master/usage/extensions/coverage.html>`_", "`usage/extensions/autodoc <https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html>`_"
   "`usage/extensions/doctest <https://www.sphinx-doc.org/en/master/usage/extensions/doctest.html>`_", "`tutorial/describing-code <https://www.sphinx-doc.org/en/master/tutorial/describing-code.html>`_"
   "`usage/extensions/duration <https://www.sphinx-doc.org/en/master/usage/extensions/duration.html>`_", "`tutorial/more-sphinx-customization <https://www.sphinx-doc.org/en/master/tutorial/more-sphinx-customization.html>`_"
   "`usage/extensions/example_google <https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html>`_", "`usage/extensions/example_numpy <https://www.sphinx-doc.org/en/master/usage/extensions/example_numpy.html>`_"
   "`usage/extensions/example_numpy <https://www.sphinx-doc.org/en/master/usage/extensions/example_numpy.html>`_", "`usage/extensions/example_google <https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html>`_"
   "`usage/extensions/extlinks <https://www.sphinx-doc.org/en/master/usage/extensions/extlinks.html>`_", "`usage/extensions/intersphinx <https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html>`_"
   "`usage/extensions/githubpages <https://www.sphinx-doc.org/en/master/usage/extensions/githubpages.html>`_", "`tutorial/deploying <https://www.sphinx-doc.org/en/master/tutorial/deploying.html>`_"
   "`usage/extensions/graphviz <https://www.sphinx-doc.org/en/master/usage/extensions/graphviz.html>`_", "`usage/extensions/math <https://www.sphinx-doc.org/en/master/usage/extensions/math.html>`_"
   "`usage/extensions/ifconfig <https://www.sphinx-doc.org/en/master/usage/extensions/ifconfig.html>`_", "`usage/extensions/doctest <https://www.sphinx-doc.org/en/master/usage/extensions/doctest.html>`_"
   "`usage/extensions/imgconverter <https://www.sphinx-doc.org/en/master/usage/extensions/imgconverter.html>`_", "`usage/extensions/math <https://www.sphinx-doc.org/en/master/usage/extensions/math.html>`_"
   "`usage/extensions/index <https://www.sphinx-doc.org/en/master/usage/extensions/index.html>`_", "`development/index <https://www.sphinx-doc.org/en/master/development/index.html>`_"
   "`usage/extensions/inheritance <https://www.sphinx-doc.org/en/master/usage/extensions/inheritance.html>`_", "`usage/extensions/graphviz <https://www.sphinx-doc.org/en/master/usage/extensions/graphviz.html>`_"
   "`usage/extensions/intersphinx <https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html>`_", "`usage/quickstart <https://www.sphinx-doc.org/en/master/usage/quickstart.html>`_"
   "`usage/extensions/linkcode <https://www.sphinx-doc.org/en/master/usage/extensions/linkcode.html>`_", "`usage/extensions/viewcode <https://www.sphinx-doc.org/en/master/usage/extensions/viewcode.html>`_"
   "`usage/extensions/math <https://www.sphinx-doc.org/en/master/usage/extensions/math.html>`_", "`usage/configuration <https://www.sphinx-doc.org/en/master/usage/configuration.html>`_"
   "`usage/extensions/napoleon <https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html>`_", "`usage/extensions/example_google <https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html>`_"
   "`usage/extensions/todo <https://www.sphinx-doc.org/en/master/usage/extensions/todo.html>`_", "`development/tutorials/extending_build <https://www.sphinx-doc.org/en/master/development/tutorials/extending_build.html>`_"
   "`usage/extensions/viewcode <https://www.sphinx-doc.org/en/master/usage/extensions/viewcode.html>`_", "`usage/extensions/linkcode <https://www.sphinx-doc.org/en/master/usage/extensions/linkcode.html>`_"
   "`usage/index <https://www.sphinx-doc.org/en/master/usage/index.html>`_", "`tutorial/end <https://www.sphinx-doc.org/en/master/tutorial/end.html>`_"
   "`usage/installation <https://www.sphinx-doc.org/en/master/usage/installation.html>`_", "`tutorial/getting-started <https://www.sphinx-doc.org/en/master/tutorial/getting-started.html>`_"
   "`usage/markdown <https://www.sphinx-doc.org/en/master/usage/markdown.html>`_", "`extdev/parserapi <https://www.sphinx-doc.org/en/master/extdev/parserapi.html>`_"
   "`usage/quickstart <https://www.sphinx-doc.org/en/master/usage/quickstart.html>`_", "`index <https://www.sphinx-doc.org/en/master/index.html>`_"
   "`usage/referencing <https://www.sphinx-doc.org/en/master/usage/referencing.html>`_", "`usage/restructuredtext/roles <https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html>`_"
   "`usage/restructuredtext/basics <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_", "`usage/restructuredtext/directives <https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html>`_"
   "`usage/restructuredtext/directives <https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html>`_", "`usage/restructuredtext/basics <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_"
   "`usage/restructuredtext/domains <https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html>`_", "`usage/domains/index <https://www.sphinx-doc.org/en/master/usage/domains/index.html>`_"
   "`usage/restructuredtext/field-lists <https://www.sphinx-doc.org/en/master/usage/restructuredtext/field-lists.html>`_", "`usage/restructuredtext/directives <https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html>`_"
   "`usage/restructuredtext/index <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_", "`usage/restructuredtext/basics <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_"
   "`usage/restructuredtext/roles <https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html>`_", "`usage/referencing <https://www.sphinx-doc.org/en/master/usage/referencing.html>`_"
   "`usage/theming <https://www.sphinx-doc.org/en/master/usage/theming.html>`_", "`development/html_themes/index <https://www.sphinx-doc.org/en/master/development/html_themes/index.html>`_"
