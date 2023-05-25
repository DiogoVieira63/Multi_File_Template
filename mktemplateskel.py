import os
import re

import argparse

def name_type(string):
    if '=' not in string:
        raise argparse.ArgumentTypeError("Invalid format for name argument. Should be 'name=<name of the project>'.")
    key, name = string.split('=', 1)
    return name

# Create the argument parser
parser = argparse.ArgumentParser(description='mkfstree - Create a file system tree')

# Add the arguments
parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
parser.add_argument('name', metavar='name', type=name_type, help='Name of the project')
parser.add_argument('project_path', metavar=str, type=str, help='Path to the input project')
parser.add_argument('-o','--output', metavar='output', type=str, help='Path of the output file (template)')

# Parse the arguments
args = parser.parse_args()

# Access the parsed arguments
name = args.name
input = args.project_path
verbose = args.verbose
output = args.output

import pyproject_parser as parser

def find_meta(filename):
    meta = {}
    pyproject = parser._load_toml(filename)
    author = pyproject["project"]["authors"][0]["name"]
    project_name = pyproject.get("project", {}).get("name", "")
    meta["author"] = author
    meta["name"] = project_name
    return meta



tree = []
walk = os.walk(input)
files_section = []
for root, dirs, files in walk:
    folder = root.replace(input, "", 1)[1:]   

    if folder.strip():
        tree.append(folder + "/")

    for file in files:
        if folder:
            tree.append("- " + file)
        else:
            tree.append(file)
        
        filename = os.path.join(root, file)

        with open(filename, 'r') as f:
            lines = f.read()
        if file == "pyproject.toml":
            meta = find_meta(filename)
        filename = filename.replace(input+ "/", "", 1)
        files_section.append(f"=== {filename}\n" + lines)

def replace_meta(meta,lines):
    array = []
    for line in lines:
        for k,v in meta.items():
            line =re.sub(rf"(?<!\w)({v})", "{{"+ k +"}}", line)
        array.append(line)
    return array

template="=== meta\n"
template+="\n".join([f"{k}: {v}" for k,v in meta.items()])
tree = replace_meta(meta,tree)
template+="\n\n=== tree\n"
template+="\n".join(tree) + "\n\n"
files_section = replace_meta(meta,files_section)
template+="".join(files_section)

if output:
    with open(output, "w") as f:
        f.write(template)
else:
    print(template)