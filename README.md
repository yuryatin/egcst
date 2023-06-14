# Python package _egcst_
This Python package helps to perform triangulation for engineering geological cross-sections.

# Installation
This Python package is uploaded to the PyPI repository and therefore can be installed with `pip install egcst` command line instruction and updated (this is critical at this early stage of development) with `pip install egcst --upgrade`.

# Polygon data format to feed
The only class `CrossSection()` of this package, when initiated, is expected to read an input text file that contains the polygons with unique geological characteristics in the following format: each polygon is placed on an individual line in the file with vertices' coordinates following one another separated with tabulation characters with x and y coordinates separated with a comma. The expected default name for this input file is `input.txt`. The object of the class `CrossSection()`, when initiated, can accept the optional argument `input_file_name` with another name for this input file. Another optional argument is `min_step`, which determines the approximate step for the triangulation grid. Its default value is 0.04, which is too small for certain input units and may dramatically slow the triangulation.

# Dependencies
This package depends on the standard Python module `sys` as well as the non-standard Python modules `numpy`, `matplotlib`, `shapely`, `ground`, and `sect`.

# How to use it
Very easy. The package has only one class `CrossSection()`, which is initiated with the input text file containing the coordinates for the polygons of the  engineering geological cross-section. This class has only 5 'public' methods: `.draw_blank()`, `.triangulate()`, `.save_triangles()`, `.draw_triangles()`, `.do_everything()`, which (except for the last one) are expected to be called in this order (and never repeated for the same object).<br/> The illustration of how to use this package can be found in the attached file [egcst_illustration.ipybn](https://github.com/yuryatin/egcst/blob/main/egcst_illustration.ipynb) .<br/> Briefly this can be expressed like this:
```python
from egcst import CrossSection
cs = CrossSection(input_file_name="input.txt", min_step=1.0)
cs.do_everything()
```
![output_triangles](https://github.com/yuryatin/egcst/assets/14263965/b549f8e7-071c-406c-b515-7ae984076e8f)

