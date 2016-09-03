import os, shutil, subprocess
import docutils.nodes

from docutils.nodes import table, header, image, figure, title, emphasis, strong


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
    shutil.move(sources_build_path, sources_path)


def build_search_snippets(app, docname):
    if app.builder.name == 'html':
        clean_txts(app.config.language, app.srcdir, app.outdir)


def remove_text_markup(app, doctree, docname):
    if app.builder.name == 'text':

        nodes_to_replace = doctree.traverse(table)\
            + doctree.traverse(header)\
            + doctree.traverse(title)\
            + doctree.traverse(emphasis)\
            + doctree.traverse(strong)
        for node in nodes_to_replace:
            newnode = docutils.nodes.line('', node.astext())
            node.replace_self(newnode)

        nodes_to_remove = doctree.traverse(figure)\
            + doctree.traverse(image)
        for node in nodes_to_remove:
            node.replace_self(docutils.nodes.line('',''))


def setup(app):
    app.connect('build-finished', build_search_snippets)
    app.connect('doctree-resolved', remove_text_markup)