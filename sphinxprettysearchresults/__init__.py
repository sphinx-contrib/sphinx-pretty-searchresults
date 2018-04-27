import pkg_resources, shutil, subprocess
import docutils

from docutils import nodes

from docutils.nodes import *

from sphinx.jinja2glue import SphinxFileSystemLoader

supported_builders = [
    'dirhtml',
    'html'
]
file_ending_dict = {}


def clean_txts(language, srcdir, outdir, source_suffixes, use_old_search_snippets):
    if not isinstance(outdir, str) and isinstance(outdir, unicode):
        outdir = outdir.encode('UTF-8')

    if not isinstance(srcdir, str) and isinstance(srcdir, unicode):
        srcdir = srcdir.encode('UTF-8')

    sources_path = outdir + '/_sources'
    sources_build_path = '_build_txt'

    if os.path.isdir(outdir + '/_raw_sources'):
        shutil.rmtree(outdir + '/_raw_sources')

    if os.path.isdir(sources_path):
        shutil.move(sources_path, outdir + '/_raw_sources')

    if not os.path.isdir(sources_build_path):
        os.makedirs(sources_build_path)

    if not language:
        language = 'en'

    build_txt = subprocess.Popen(['sphinx-build', '-a', '-b', 'text','-D' 'language=' + language, \
                                  srcdir, sources_build_path])

    build_txt.wait()

    shutil.move(sources_build_path, sources_path)

    if pkg_resources.get_distribution("sphinx").version >= "1.5.0" and not use_old_search_snippets:
        for root, dirs, files in os.walk(sources_path):
            for file in files:
                # determine correct suffix
                if file.endswith('.txt'):
                    source_suffix = None
                    for suffix in source_suffixes:
                        source_root = root.replace(sources_path, srcdir)
                        if os.path.isfile(source_root + '/' + file.replace('.txt', suffix)):
                            if suffix == '.txt':
                                source_suffix = ''
                            else:
                                source_suffix = suffix
                            break

                os.rename(os.path.join(root, file), os.path.join(root, file.replace('.txt', source_suffix + '.txt')))


def build_search_snippets(app, docname):
    if app.builder.name in supported_builders:
        source_suffixes = app.config.source_suffix
        clean_txts(app.config.language, app.srcdir, app.outdir, source_suffixes, app.config.use_old_search_snippets)



def remove_text_markup(app, doctree, docname):
    if app.builder.name == 'text':

        file_ending_dict[docname] = app.env.doc2path(docname).rsplit('.', 1)[1]

        nodes_to_replace = doctree.traverse(table)\
            + doctree.traverse(header)\
            + doctree.traverse(title)\
            + doctree.traverse(emphasis)\
            + doctree.traverse(strong)\
            + doctree.traverse(list_item)\
            + doctree.traverse(reference) \
            + doctree.traverse(transition)
        for node in nodes_to_replace:
            new_node = paragraph()
            new_node.append(line('', node.astext()))
            node.replace_self(new_node)

        nodes_to_remove = doctree.traverse(figure)\
            + doctree.traverse(image)\
            + doctree.traverse(compound)

        for node in nodes_to_remove:
            node.replace_self(docutils.nodes.line('',''))


def add_custom_source_link(app):
    if app.builder.name in supported_builders:
        template_index = None
        index = None
        for template_set in app.builder.templates.loaders:
            if index is None:
                index = 0
            else:
                index =+ 1
            if 'sourcelink.html' in template_set.list_templates():
                template_index = index
                break
        if index is not None:
            app.builder.templates.loaders.insert(
                template_index, SphinxFileSystemLoader(os.path.dirname(__file__)))


def setup(app):
    app.add_config_value('use_old_search_snippets', False, 'html')
    app.connect('build-finished', build_search_snippets)
    app.connect('doctree-resolved', remove_text_markup)
    app.connect('builder-inited', add_custom_source_link)
