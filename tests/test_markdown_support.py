import os.path
from sphinx_testing import with_app

lines = []
out_dir = ''


@with_app(buildername='html', srcdir='markdown_root', copy_srcdir_to_tmpdir=True, outdir='markdown_root/_build')
def setup(app, status, warning):
    global lines
    global out_dir
    out_dir = app.outdir
    app.build()
    with open(app.outdir + '/_sources/markdown.md.txt') as f:
        lines = f.readlines()
        lines = [line.replace('\n', '').replace('\r', '') for line in lines]


def test_file_ending():
    """
    In any case the test could fail, the setup will fail first;
    still let's keep it for the sake of documentation
    """
    assert os.path.isfile(out_dir + '/_sources/markdown.md.txt') is True


def test_markup():
    assert lines[0] == 'Level 1 Heading', '%s != "Level 1 Heading"' % (lines[0])
    assert lines[2] == 'italic', '%s != "italic"' % (lines[4])
