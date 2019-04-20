# EasyLaunch python library
# Written by James Usevitch, University of Michigan

# Overall structure:
# 1. XML Version at top
# 2. launchFile class
#   -- dictionary of args with default values
#   -- dictionary of remaps
#   -- array of include classes
#   -- array of node classes

# 3. include class
#   -- Attributes:
#       > .file
#       > .namespace 
#   -- array of args which use the default value
#   -- dict of args which use custom values

# 4. node class
#   -- Attributes:
#       > .name
#       > .package
#       > .type
#       > .launch-prefix
#       > .output
#       > .namespace
#   -- array of parameters which use default arg values
#   -- dict of parameters which use custom values

# 5. Group class?

# !!! USE THE KEYWORDS USED IN THE XML FILES! (E.g. use pkg for package, ns for namespace, etc)

import copy
import xml.etree.ElementTree as ET
from xml.dom import minidom

class launchFile:
    def __init__(self, arg=None, remap=None, include=None, node=None):
        self.arg = arg # Dictionary of {name: default} pairs
        self.remap = remap
        self.include = include 
        self.node = node

    # Source for prettify function: https://bip.weizmann.ac.il/course/python/PyMOTW/PyMOTW/docs/xml/etree/ElementTree/create.html
    # Link works as of 4/20/19
    def prettify(self, element):
        # Returns an XML string with 'pretty' formatting
        # You can print the string to screen or to file
        rough_string = ET.tostring(element, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    # Creates a
    def write(self, filename="./launchFile.launch", prettyprint=True, verbose=False): 
        launch = self.getLaunchElement(verbose)
        if prettyprint:
            print(self.prettify(launch), file=open(filename, "w"))
        else:
            print('<?xml version="1.0"?>', file=open(filename, "w"))
            print(ET.tostring(launch).decode('UTF-8'), file=open(filename, "a"))

    # Prints a preview of the launch file to screen
    def print(self, verbose=False):
        launch = self.getLaunchElement(verbose)
        print(self.prettify(launch))


    def getLaunchElement(self, verbose=False): # To do: put output text inside if statements controlled by verbose bool
        launch = ET.Element("launch")
        
        ## Create arg elenents
        if type(self.arg) is dict and len(self.arg) > 0:
            arg_keys = list(self.arg.keys())
            for i in range(len(arg_keys)):
                ET.SubElement(launch, 'arg', {'name': arg_keys[i], 'default': self.arg[arg_keys[i]]})
        else:
            print('No default arg elements / Invalid arg elements.')
        
        ## Create include elements
        if self.include is not None and len(self.include) > 0:
            # Iterate through each include element
            for i in range(len(self.include)):
                # Set the file and ns attributes
                temp_include = ET.SubElement(launch, 'include', {'file': self.include[i].file})
                if self.include[i].ns is not None:
                    temp_include.set('ns', self.include[i].ns)
                
                # Set the arg elements with default values
                if self.include[i].defarg is not None and len(self.include[i].defarg) > 0:
                    for j in range(len(self.include[i].defarg)):
                        if self.include[i].defarg[j] in list(self.arg.keys()):
                            ET.SubElement(temp_include, 'arg', {'name': self.include[i].defarg[j], 'value': '$(arg ' + self.include[i].defarg[j] + ')'})
                        else:
                            print('Default arg ' + self.include[i].defarg[j] + ' not listed in default launchfile.arg dict')
                else:
                    print('Default args are "None" or empty')
                    
                # Set the arg elements which are not default values
                if self.include[i].arg is not None and len(self.include[i].arg) > 0:
                    temp_keys = list(self.include[i].arg.keys())
                    for k in range(len(temp_keys)):
                        ET.SubElement(temp_include, 'arg', {'name': temp_keys[k], 'value': self.include[i].arg[temp_keys[k]]})
        else:
            print('No include elements.')
        
        ## Create node elements
        if len(self.node) > 0:
            for i in range(len(self.node)):
                temp_node = ET.SubElement(launch, 'node', {'name': self.node[i].name, 'pkg': self.node[i].pkg, 'type': self.node[i].type})
                if self.node[i].launch_prefix is not None:
                    temp_node.set('launch_prefix', self.node[i].launch_prefix)
                
                if self.node[i].output is not None:
                    temp_node.set('output', self.node[i].output)

                if self.node[i].ns is not None:
                    temp_node.set('ns', self.node[i].ns)

                # Set the default param elements
                if self.node[i].defparam is not None and len(self.node[i].defparam) > 0:
                    for j in range(len(self.node[i].defparam)):
                        if self.node[i].defparam[j] in list(self.arg.keys()):
                            ET.SubElement(temp_node, 'param', {'name': self.node[i].defparam[j], 'value': '$(arg ' + self.node[i].defparam[j] + ')'})
                        else:
                            print('Default param ' + self.node[i].defparam[j] + ' not listed in default launchfile.arg dict')
                else:
                    print('Default params are "None" or empty')

                # Set the param elements which are not default values
                if self.node[i].param is not None and len(self.node[i].param) > 0:
                    temp_keys = list(self.node[i].param.keys())
                    for k in range(len(temp_keys)):
                        ET.SubElement(temp_node, 'param', {'name': temp_keys[k], 'value': self.node[i].param[temp_keys[k]]})
        else:
            print('No (standalone) node elements. (Other nodes may be inside include files)')
        
        return launch



#   def print(self):
        # Print to the screen as preview
    


class include:
    def __init__(self, file=None, ns=None, defarg=None, arg=None):
        self.file = file
        self.ns = ns
        self.defarg = defarg # Array of strings
        self.arg = arg # Dict

    def copy(self, number_copies=1, ns_array=None):
        if self.ns is None:
            raise ValueError('Value of "ns" is None. Set your include "ns" variable. Copying include elements without changing the namespace will cause problems.')
        elif ns_array is None:
            include_list = [copy.deepcopy(self) for i in range(number_copies)]
            for i in range(number_copies):
                include_list[i].ns = self.ns + str(i + 1)
            return include_list
        elif number_copies <= len(ns_array):
            if number_copies < len(ns_array):
                print('WARNING: number_copies < len(ns_array) for copy operation involving the include ' + self.file + '. Not all namespaces will be used.')
            include_list = [copy.deepcopy(self) for i in range(number_copies)] 
            for i in range(number_copies):
                include_list[i].ns = ns_array[i]
            return include_list
        elif number_copies > len(ns_array):
            raise ValueError('Value of "number_copies" is greater than length of "ns_array". Aborting.')
        else:
            raise ValueError('Something really bad happened. Check your ns_array variable.')




class node:
    def __init__(self, name, pkg, type, launch_prefix=None, output=None, ns=None, defparam=None, param=None):
        self.name = name
        self.pkg = pkg
        self.type = type
        self.launch_prefix = launch_prefix
        self.output = output
        self.ns = ns
        self.defparam = defparam # Array of strings
        self.param = param # Dict

    def copy(self, number_copies=1, name_array=None):
        if name_array is None:
            node_list = [copy.deepcopy(self) for i in range(number_copies)]
            for j in range(number_copies):
                node_list[j].name = self.name + str(j + 1)
            return node_list 
        elif number_copies <= len(name_array):
            if number_copies < len(name_array):
                print('WARNING: number_copies < len(name_array) for copy operation involving the node ' + self.name + '. Not all names will be used.')
            node_list = [copy.deepcopy(self) for i in range(number_copies)]
            for i in range(number_copies):
                node_list[i].name = name_array[i]
            return node_list
        else:
            raise ValueError('Value of "number_copies" is greater than length of "name_array". Aborting.')








    