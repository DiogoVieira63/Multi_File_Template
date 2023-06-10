import os
import argparse
import sys

def name_type(string):
        if '=' not in string:
            raise argparse.ArgumentTypeError("Invalid format for name argument. Should be 'name=<name of the project>'.")
        key, name = string.split('=', 1)
        return key,name

def parse_meta(lines):
        meta = {}
        for line in lines:
            if line.startswith('//') or not line.strip():
                continue
            k, v = line.split(':')
            meta[k.strip()] = v.strip()
        return meta


def parse_tree(lines,meta,out):
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
    create_dir(folders,out)
    return array

def create_dir(folders, out):
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

def parse_file(lines,meta,out):
    lines = replace_meta(lines,meta)
    name = lines[0].strip()
    content = '\n'.join(lines[1:])
    path = os.path.join(out, name)
    with open(path, 'w') as f:
        f.write(content)

def mkfstree():
    
    parser = argparse.ArgumentParser(prog="mkfstree", epilog="Create a file system tree",description='mkfstree - Create a file system tree')

    parser.add_argument('-v','--vars', type=name_type, nargs='+', help='Meta variables of the project')
    parser.add_argument('template', nargs='?', type=str, help='Path to the template file')
    parser.add_argument('-o','--output', type=str, help='Path of the output folder')
    parser.add_argument('-i','--interactive',action='store_true',help='Interactive mode')
    parser.add_argument('-t','--template-default',nargs='?',type=str,const=sys.stdout,help='Print or store the default template')
    


    args = parser.parse_args()

    if args.template_default:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(current_dir,'templates/template')
        with open(filename, 'r') as f:
            text = f.read()
            if type(args.template_default) != str:
                print(text)
            else:
                with open(args.template_default, "w") as f1:
                    f1.write(text)
            exit()

    if args.vars:
        vars = {key:value for (key,value) in args.vars}
    else:
        vars={}

    #input = args.name
    template = args.template

    out = args.output
    if not out: out = "output"

    interactive = args.interactive

    with open(template, 'r') as f:
        lines = f.read()

    sections = lines.split('===')[1:]

    for section in sections:
        lines = section.split('\n')
        name = lines[0].strip()
        if name == 'meta':
            meta = parse_meta(lines[1:])
            for key in vars:
                meta[key] = vars[key]

            for m in meta:
                if interactive:
                    answer = False
                    if meta[m]:
                        while not answer:
                            answer = input(f"Meta variable {m} has this value: {meta[m]}. If you want to change it input a new value, else just press Enter.\n> ")
                            if answer:
                                meta[m] = answer
                            else:
                                answer = True

                    else:
                        while not meta[m]: 
                            meta[m] = input(f"Meta Variable {m} missing. Please enter a value for {m}: ").strip()
                else:
                    if not meta[m]:
                        print(f"Meta Variable {m} missing. Pass {m} as a parameter with -v {m}=... or use interactive mode with -i")
                        exit()


        elif name == 'tree':
            tree = parse_tree(lines[1:],meta,out)            
        else:
            parse_file(lines,meta,out)
        lines = lines[1:]

