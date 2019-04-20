# EasyLaunch python library
# Written by James Usevitch, University of Michigan

# Overall structure:
# 1. XML Version at top
# 2. launchFile class
#   -- dictionary of args with default values
#   -- dictionary of remaps
#   -- vector of include classes
#   -- vector of node classes

# 3. include class
#   -- Attributes:
#       > .file
#       > .namespace 
#   -- vector of args which use the default value
#   -- dict of args which use custom values

# 4. node class
#   -- Attributes:
#       > .name
#       > .package
#       > .type
#       > .launch-prefix
#       > .output
#       > .namespace
#   -- Vector of parameters which use default arg values
#   -- dict of parameters which use custom values

# 5. Group class?

# !!! USE THE KEYWORDS USED IN THE XML FILES! (E.g. use pkg for package, ns for namespace, etc)


import xml.etree.ElementTree as ET

class launchFile:
    def __init__(self, args = None, remap = None, include = None, node = None):
        self.args = args
        self.remap = remap
        self.include = include 
        self.node = node

    def write(self, filename="./launchFile.launch"):
        # Export to XML
    


class include:
    def __init__(self, file = None, ns = None, defargs = None, args = None):
        self.file = file
        self.ns = ns
        self.defargs = defargs
        self.args = args




class node:
    def __init__(self, name=None, pkg=None, Type=None, launch_prefix=None, output=None, repetitions = None):
        self.name = name
        self.pkg = pkg
        self.type = Type
        self.launch_prefix = launch_prefix
        self.output = output

    def copy(self, number_copies=1, name_array=None):
        if name_array is None:
            node_list = [self for i in range(number_copies)]
            for j in range(number_copies):
                node_list[j].name = self.name + str(j + 1)
            return node_list 
        elif number_copies <= name_array.__len__():
            if number_copies < name_array.__len__():
                print('WARNING: number_copies < name_array for copy operation involving the node ' + self.name + '. Not all names will be used.')
            for i in range(number_copies):
                node_list[i] = self
                node_list[i].name = name_array[i]
            return node_list
        else:
            raise ValueError('Value of "number_copies" is greater than length of "name_array". Aborting.')








    