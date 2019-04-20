# Easy Launch
A simple Python module for generating repetitive ROS launch files.

The purpose of this module is to make writing large, repetitive ROS launch files as painless as possible. 
Creating large ROS XML launch files by hand can be tedious and frustrating, especially when many of the include elements or node
elements are essentially copies of each other with a few small changes to names or parameters. 
To the best of my knowledge, ROS launch files do not support notation for duplicating include or node elements--each individual
one must appear in the `.launch` file.
Generating XML files
programmatically is possible in a variety of languages (e.g. [MATLAB](https://www.mathworks.com/help/matlab/ref/xmlwrite.html),
[Python](https://docs.python.org/3/library/xml.etree.elementtree.html#xml.etree.ElementTree.ElementTree.write),
[C++](https://stackoverflow.com/questions/303371/whats-the-easiest-way-to-generate-xml-in-c), etc), but can almost feel just as
awkward (or more awkward) than simply coding the XML by hand and copy/pasting it.
After a few quick searches on Google, I was not able to find any software which programmatically generates large launch files in
a convenient manner. So I decided to write my own.

The easylaunch module provides the following capabilities:
1. An abbreviated syntax for writing launch files
2. Functions for easily making copies of include elenents and node elements
3. Automatic XML file generation

## Quick Examples:


## Explanation:

The easylaunch module contains three classes:
1. `launchFile`
2. `include`
3. `node`

The `launchFile` class contains the following attributes:
* `arg`: A dictionary of `{name: default}` pairs
* TO BE CONTINUED

**To do: Create a simple example file demonstrating all capabilities**
