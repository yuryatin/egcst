from distutils.core import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='egcst',
    packages=['egcst'],
    version='0.0.10',
    license='MIT',
    description='This package performs triangulation for engineering geological cross-sections',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yuryatin/egcst',
    download_url='https://github.com/yuryatin/egcst/archive/refs/tags/v0.0.10.tar.gz',
    keywords=['engineering', 'geological', 'cross',
              'sections', 'mapping', 'triangulation', 'delaunay', 'step', 'stp', 'iso 10303-21'],
    classifiers=[],
    install_requires=['numpy', 'matplotlib', 'shapely', 'ground', 'sect']
)
