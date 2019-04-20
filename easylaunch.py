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
    def __init__(self, arg=None, remap=None, include=None, node=None):
        self.arg = arg # Dictionary of {name: default} pairs
        self.remap = remap
        self.include = include 
        self.node = node

    def write(self, filename="./launchFile.launch", verbose=False): # To do: put output text inside if statements controlled by verbose bool
        launch = ET.Element("launch")

        ## Create arg elenents
        if type(self.arg) is dict and len(self.arg) > 0:
            arg_keys = list(self.arg.keys())
            for i in range(len(arg_keys)):
                ET.SubElement(launch, 'arg', {'name': arg_keys[i], 'default': self.arg[arg_keys[i]]})
        else:
            print('No default arg elements / Invalid arg elements.')
        
        ## Create include elements
        if len(self.include) > 0:
            # Iterate through each include element
            for i in range(len(self.include)):
                # Set the file and ns attributes
                temp_include = ET.SubElement(launch, 'include', {'file': self.include[i].file})
                if self.include[i].ns is not None:
                    temp_include.set('ns', self.include[i].ns)
                
                # Set the arg elements with default values
                if self.include[i].defargs is not None and len(self.include[i].defargs) > 0:
                    for j in range(len(self.include[i].defargs)):
                        if self.include[i].defargs[j] in list(self.arg.keys()):
                            ET.SubElement(temp_include, 'arg', {'name': self.include.defargs[j], 'value': '$(arg ' + self.include.defargs[j] + ')'})
                        else:
                            print('Default arg ' + self.include.defargs[j] + ' not listed in default launchfile.arg dict')
                else:
                    print('Default args are "None" or empty')
                    
                # Set the arg elements which are not default values
                if self.include[i].args is not None and len(self.include[i].args) > 0:
                    temp_keys = list(self.include[i].args.keys())
                    for k in range(len(temp_keys)):
                        ET.SubElement(temp_include, 'arg', {'name': temp_keys[k], 'value': self.include[i].args[temp_keys[k]]})
        else:
            print('No include elements.')
        
        ## Create node elements
        if len(self.node) > 0:
            for i in range(len(self.node)):
                temp_node = ET.SubElement(launch, 'node', {'name': self.node[i].name})
        else:
            print('No (standalone) node elements. (Other nodes may be inside include files)')


#   def print(self):
        # Print to the screen as preview
    


class include:
    def __init__(self, file=None, ns=None, defargs=None, args=None):
        self.file = file
        self.ns = ns
        self.defargs = defargs
        self.args = args

    def copy(self, number_copies=1, ns_array=None):
        if ns_array is None:
            include_list = [self for i in range(number_copies)]
            for i in number_copies:
                include_list[i].ns = self.ns + str(i + 1)
            return include_list
        elif number_copies <= len(ns_array):
            if number_copies < len(ns_array):
                print('WARNING: number_copies < len(ns_array) for copy operation involving the include ' + self.file + '. Not all namespaces will be used.')
            include_list = [self for i in range(number_copies)] 
            for i in range(number_copies):
                include_list[i].ns = ns_array[i]
            return include_list
        else:
            raise ValueError('Value of "number_copies" is greater than length of "ns_array". Aborting.')




class node:
    def __init__(self, name, pkg, Type, launch_prefix=None, output=None, repetitions = None):
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
        elif number_copies <= len(name_array):
            if number_copies < len(name_array):
                print('WARNING: number_copies < len(name_array) for copy operation involving the node ' + self.name + '. Not all names will be used.')
            node_list = [self for i in range(number_copies)]
            for i in range(number_copies):
                node_list[i].name = name_array[i]
            return node_list
        else:
            raise ValueError('Value of "number_copies" is greater than length of "name_array". Aborting.')








    