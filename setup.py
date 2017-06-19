import codecs, setuptools


setuptools.setup(
    name='sphinxprettysearchresults',
    packages=['sphinxprettysearchresults'],
    version='0.3.1',
    description='Decently styled search results for sphinx-doc projects',
    author='Timotheus Kampik',
    author_email='timotheus.kampik@gmail.com',
    url='https://github.com/TimKam/sphinx-pretty-searchresults',
    platforms=["any"],
    license="MIT",
    zip_safe=False,
    install_requires=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Documentation",
    ],
    long_description=codecs.open("README.rst", "r", "utf-8").read(),
)
