import os
import sys
import re

if len(sys.argv) != 2:
    print("Usage: python mktemplateskel.py <input>")
    sys.exit(1)

input = sys.argv[1]

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
    folder = root.replace(input, "")[1:]        
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
        filename = filename.replace(input+ "/", "")
        files_section.append(f"=== {filename}\n" + lines)

def replace_meta(meta,lines):
    array = []
    for line in lines:
        for k,v in meta.items():
            line =re.sub(rf"(?<!\w)({v})", "{{"+ k +"}}", line)
        array.append(line)
    return array

print("=== meta")
print("\n".join([f"{k}: {v}" for k,v in meta.items()]))
tree = replace_meta(meta,tree)
print("\n=== tree")
print("\n".join(tree) + "\n")
files_section = replace_meta(meta,files_section)
print("".join(files_section))

