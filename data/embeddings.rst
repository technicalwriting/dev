.. _embeddings:

==========
Embeddings
==========

----------
Experiment
----------

Implementation
==============

You don't need to understand the following code in-depth. My main goal is to show you
that it didn't require a lot of code to get this working.

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


   def init_globals(srcdir):  # Use some globals because this is just an experiment and you can't stop me
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

When the build finishes the embeddings data is stored in ``embeddings.json`` like this:

.. code-block:: json

   {
       "authors": {
           "embedding": [
               -0.02387414500117302,
               -0.03536511957645416,
               0.0456915982067585
           ]
       },
       "changes/0.1": {
           "embedding": [
               -0.026020174846053123,
               -0.033769506961107254,
               -0.02538042888045311
           ]
       }
   }

``authors`` and ``changes/0.1`` are docs. ``embedding`` contains the
embedding for that doc. Each ``embedding`` array actually contains
thousands of numbers (I shortened it to 3 for grokkability).

The last step is to find the closest neighbor for each doc:

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

Results
=======

:ref:`embeddings-appendix-complete-results` contains the full data.

--------
Appendix
--------

.. _embeddings-appendix-complete-results:

Complete results
================

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
