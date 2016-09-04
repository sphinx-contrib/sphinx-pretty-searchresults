from sphinx_testing import with_app

lines = []
@with_app(buildername='text', srcdir='root', copy_srcdir_to_tmpdir=True, outdir='root/_build')
def setup(app, status, warning):
    app.build()
    global lines
    with open(app.outdir + '/index.txt') as f:
        lines = f.readlines()
        lines = [line.replace('\n', '').replace('\r', '') for line in lines]


def test_headings():
    assert lines[0] == 'Level 1 Heading', '%s != "Level 1 Heading"' % (lines[0])
    assert lines[4] == 'Level 2 Heading', '%s != "Level 2 Heading"' % (lines[4])


def test_plain_text():
    assert lines[6] == 'Lorem ipsum', '%s != "Lorem ipsum"' % (lines[6])


def test_strong():
    assert lines[8] == 'strong', '%s != "strong"' % (lines[8])


def test_emphasis():
    assert lines[10] == 'emphasized', '%s != "emphasized"' % (lines[10])


def test_figure():
    assert any('figure' in line for line in lines) == False, '"figure" is in line in lines'


def test_image():
    assert any('image' in line for line in lines) == False, '"image" is in line in lines'


def test_table():
    assert lines[12] == '    cell1/1  cell1/2  cell2/1  cell2/2', '%s !=\
        "    cell1/1  cell1/2  cell2/1  cell2/2"' % (lines[10])