import os, shutil, sys

import nose

build_dir = 'root/_build'

if os.path.isdir(build_dir):
    shutil.rmtree(build_dir)
os.makedirs(build_dir)

print('Running sphinx-pretty-search-results tests (with Python %s)...' % sys.version.split()[0])
sys.stdout.flush()

nose.main()