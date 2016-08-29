import os, re, shutil, subprocess, sys
from shutil import move
import pprint

import docutils.nodes

from docutils.nodes import table, comment, title, Text, NodeVisitor, SkipNode


def remove_markup():
    # remove remaining markup from .txt files that are used to display search results

    regexp = re.compile("\*\**|"
           "\=\=*|"
           "\~\~*|"
           "\^\^*|"
           "\-\-*|"
           "(\[image\])*"
           "(\[Bild\])*")

    for subdir, dirs, files in os.walk('_build_txt'):
        for file in files:
            if file.endswith('.txt'):
                path = os.path.join(subdir, file)
                with open(path) as infile:
                    with open(file,'w') as new_file:
                        for line in infile:
                            line = re.sub(regexp, '', line)
                            new_file.write(line)
                os.remove(path)
                move(file, path)


def clean_txts(language, srcdir, outdir):
    if isinstance(outdir, unicode):
        outdir = outdir.encode('UTF-8')

    if isinstance(srcdir, unicode):
        srcdir = srcdir.encode('UTF-8')

    sources_path = outdir + '/_sources'
    sources_build_path = '_build_txt'

    if os.path.isdir(sources_path):
        shutil.rmtree(sources_path)

    if not os.path.isdir(sources_build_path):
        os.makedirs(sources_build_path)

    if not language:
        language = 'en'

    build_txt = subprocess.Popen(['sphinx-build', '-a', '-b', 'text','-D' 'language=' + language, \
                                  srcdir, sources_build_path])
    build_txt.wait()
    remove_markup()
    shutil.move(sources_build_path, sources_path)


def build_search_snippets(app, docname):
    if app.builder.name == 'html':
        clean_txts(app.config.language, app.srcdir, app.outdir)


def remove_text_markup(app, doctree, docname):
    if app.builder.name == 'text':
        for node in doctree.traverse(table):
            newnode = docutils.nodes.line('', node.astext())
            node.replace_self(newnode)


def setup(app):
    app.connect('build-finished', build_search_snippets)
    app.connect('doctree-resolved', remove_text_markup)