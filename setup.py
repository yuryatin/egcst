from distutils.core import setup

setup(
    name = 'egcst',
    packages = ['egcst'],
    version = '0.0.3',
    license = 'MIT',
    description = 'This package performs triangulation for engineering geological cross-sections',
    url = 'https://github.com/yuryatin/egcst',
    download_url = 'https://github.com/yuryatin/egcst/archive/refs/tags/v0.0.3.tar.gz',
    keywords = ['engineering', 'geological', 'cross', 'sections', 'mapping', 'triangulation', 'delaunay'],
    classifiers = [],
    install_requires = ['numpy', 'matplotlib', 'shapely', 'ground', 'sect']
)