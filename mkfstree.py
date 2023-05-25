import os
import sys

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
parser.add_argument('templateflit', metavar='templateflit', type=str, nargs='?', help='Path to the template file')

# Parse the arguments
args = parser.parse_args()

# Access the parsed arguments
input = args.name
templateflit = args.templateflit
verbose = args.verbose

if templateflit: out = templateflit
else: out = "output"


with open(input, 'r') as f:
    lines = f.read()

sections = lines.split('===')[1:]


def parse_meta(lines):
    meta = {}
    for line in lines:
        if line.startswith('//') or not line.strip():
            continue
        k, v = line.split(':')
        meta[k.strip()] = v.strip()
    return meta


def parse_tree(lines,meta):
    array = []
    for line in lines:
        if line.startswith('//') or not line.strip():
            continue
        for k,v in meta.items():
            line = line.replace("{{" + k + "}}",v)
        if line.endswith('/'):
            folder = line
        if line.startswith('-'):
            file = line[1:].strip()
            line = folder + file
        array.append(line)
    folders = [line for line in array if line.endswith('/')]
    create_dir(folders)
    return array


def create_dir(folders):
    for folder in folders:
        path = os.path.join(out, folder)
        if not os.path.exists(path):
            os.makedirs(path)

def replace_meta(lines,meta):
    array = []
    for line in lines:
        for k,v in meta.items():
            line = line.replace("{{" + k + "}}",v)
        array.append(line)
    return array


def parse_file(lines,meta):
    lines = replace_meta(lines,meta)
    name = lines[0].strip()
    content = '\n'.join(lines[1:])
    path = os.path.join(out, name)
    with open(path, 'w') as f:
        f.write(content)
    
    

for section in sections:
    lines = section.split('\n')
    name = lines[0].strip()
    if name == 'meta':
        meta = parse_meta(lines[1:])
    elif name == 'tree':
        tree = parse_tree(lines[1:],meta)            
    else:
        parse_file(lines,meta)
    lines = lines[1:]

