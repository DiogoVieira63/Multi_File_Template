import os
import re

import argparse
import pyproject_parser as parser

def name_type(string):
        if '=' not in string:
            raise argparse.ArgumentTypeError("Invalid format for name argument. Should be 'name=<name of the project>'.")
        key, name = string.split('=', 1)
        return key,name

def find_meta(filename):
    meta = {}
    pyproject = parser._load_toml(filename)
    authors = pyproject["project"]["authors"]
    if len(authors) == 1:
        meta["author"] = authors[0]["name"]
        meta["email"] = authors[0]["email"]
    else:
        for index,author in enumerate(authors):
            meta["author_" + str(index)] = author["name"]
            meta["email_" + str(index)] = author["email"]
    project_name = pyproject.get("project", {}).get("name", "")
    meta['name'] = project_name
    return meta

def replace_meta(meta,lines,exclude=False):
    array = []
    first = True
    for line in lines:
        if not exclude or first or line.startswith('import') or line.startswith('from'):
            first = False
            for k,v in meta.items():
                line =re.sub(rf"(?<!\w)({v})", "{{"+ k +"}}", line,count=1)
        array.append(line)
    return array

def not_excluded(file,exclude):
    if "all" in exclude:
        return False
    if file in exclude:
        return False
    ext = "." + file.split(".")[-1]
    if ext in exclude:
        return False
    return True

def mktemplateskel(): 
    argparser = argparse.ArgumentParser(prog='mktemplateskel', epilog='Create Templates', description='mktemplateskel - Create Templates')

    argparser.add_argument('-v', '--vars',type=name_type, nargs='+',help='Name of the template')
    # parser.add_argument('-n','--name', metavar='name', type=str, help='Name of the template')
    argparser.add_argument('-p','--project_path', metavar=str, type=str, help='Path to the input project')
    argparser.add_argument('-o','--output', metavar='output', type=str, help='Path of the output file (template)')
    argparser.add_argument('-i','--interactive',action='store_true',help='Interactive mode')
    argparser.add_argument('-e','--exclude',nargs='+',help="Don't change content of provided files. If you want to exclude all files just type -e all")

    args = argparser.parse_args()
    exclude = []
    if args.exclude:
        exclude = args.exclude
    vars = {}
    if args.vars:
        vars = {key:value for (key,value) in args.vars}
    path = args.project_path
    output = args.output
    interactive = args.interactive

    tree = []
    walk = os.walk(path)
    files_section = []
    for root, dirs, files in walk:
        folder = root.replace(path, "", 1)[1:]   

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
                lines = lines.split("\n")
            if file == "pyproject.toml":
                meta = find_meta(filename)
            filename = filename.replace(path+ "/", "", 1)
            files_section.append((filename,[f"=== {filename}"] + lines))

    
    tree = replace_meta(meta,tree)

    files_section = [replace_meta(meta,lines) if not_excluded(filename, exclude) else replace_meta(meta, lines, exclude=True) for (filename,lines) in files_section ] 
    files_section = ["\n".join(file) for file in files_section]
    meta['name'] = ''

    for key in vars:
        if key in meta:
            meta[key] = vars[key]
        else:
            print(f"Meta variable {key} does not exist")

    if interactive:
        for key in meta:
            if key not in vars:
                answer = False
                if key in meta:
                    while not answer:
                        answer = input(f"Meta variable {key} has this value: {meta[key]}. If you want to change it input a new value, else just press Enter.\n> ")
                        if answer:
                            meta[key] = answer
                        else:
                            answer = True

    template="=== meta\n"
    template+="\n".join([f"{k}: {v}" for k,v in meta.items()])
    template+="\n\n=== tree\n"
    template+="\n".join(tree) + "\n\n"
    template+="\n".join(files_section)

    if output:
        with open(output, "w") as f:
            f.write(template)
    else:
        print(template)