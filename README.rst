.. image:: https://travis-ci.org/TimKam/sphinx-pretty-searchresults.svg?branch=master
    :target: https://travis-ci.org/TimKam/sphinx-pretty-searchresults


Sphinx: pretty search results
=============================
*Sphinx: pretty search results* is an extension for the
`Sphinx documentation tool <http://www.sphinx-doc.org/en/stable/>`__.

To display search results, Sphinx is fetching the source files of search hits and rendering excerpts in raw markup
(`Example <http://www.sphinx-doc.org/en/stable/search.html?q=quickstart&check_keywords=yes&area=default>`__).

This extension removes the markup from these source files (during build time), so the search results look decent.


Installation
------------
Run ``pip install sphinxprettysearchresults``.


Configuration
-------------
After installing the extension, all you need to do is to register it.

Add ``sphinxprettysearchresults`` to the ``extensions`` array in your ``conf.py`` file, for example::

   extensions = [
      'sphinxprettysearchresults'
   ]

After your next build, your project will no longer display raw markup in the search result excerpts.

Since version 1.5.0, Sphinx is adding the source file extension to the source files it includes in the output folder.
For example, when your source file extension is `rst` (specified in the config variable `source_suffix` as `[.rst]`,
your index file appears in the output's source folder as `index.rst.txt`. If you use a Sphinx version lower than 1.5.0,
it appears as `index.txt`. *Sphinx: pretty search results* considers this difference and changes its behavior according
to your Sphinx version. However, if you use a Sphinx theme that expects the old file names although you are using a
later Sphinx version, you can fall back to the old file names by setting the following configuration variable::

   use_old_search_snippets = True


Source links
------------
By default Sphinx copies the source files into the build's `_sources` directory and uses it for both search snippets and
- if `activated <http://www.sphinx-doc.org/en/stable/config.html#confval-html_show_sourcelink>`_ - source links.
*Sphinx: pretty search results* uses the `_sources` directory for the prettified text snippets and moves the raw sources
(for the source links) into its own `_raw_sources` directory. On build time, it overwrites the `sourcelink.html`
template to reference the files in `_raw_sources`. If you want to use the extension with a custom source link, you need
to adjust it to point to `_raw_sources` instead of `_sources`.

Testing
-------
*Sphinx: pretty search results* uses `nose <https://github.com/nose-devs/nose>`__ as its test framework.

To run the tests, you first need to install the dev dependencies::

    pip install -r pip install -r dev_requirements.txt

Then, navigate to the ``tests`` directory and run::

    python run.py

