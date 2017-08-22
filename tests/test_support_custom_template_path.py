from sphinx_testing import with_app

@with_app(
    buildername='html',
    srcdir='custom_template_path_root',
    copy_srcdir_to_tmpdir=True,
    outdir='custom_template_path_root/_build'
)
def test_support_custom_template_path(app, status, warning):
    app.build()
    with open(app.outdir + '/index.txt') as f:
        lines = f.readlines()
        lines = [line.replace('\n', '').replace('\r', '') for line in lines]

    expected = 'Can build project with custom template path'
    assert lines[0] == expected, '%s != "{0}"'.format(expected) % (
    lines[0])