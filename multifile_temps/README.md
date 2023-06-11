# Multi-file Template

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
[![argparse](https://img.shields.io/badge/argparse->=1.4.0-blue.svg)](https://pypi.org/project/argparse/)
[![pyproject_parser](https://img.shields.io/badge/pyproject_parser->=0.9.0-blue.svg)](https://pypi.org/project/pyproject-parser/)
[![License](https://img.shields.io/npm/l/express?style=flat-square)](https://github.com/DiogoVieira63/SPLN-TP2/blob/main/multifile_temps/LICENSE)

### ⚙️ Installation

To install and use this tool follow the steps below:
- Clone this repository
- Run either *flit install* or *pip install -e* in the project directory

---

## **mkfstree - Create a file system tree from a template**

This tool has the purpose to create a file system tree given a template. 

As said before, to create a file system tree the user must provide a template. Each section of the template must begin with a header that must be defined like this: **=== meta**, for example. After the header, the user must define its content, which can be meta variables for the **=== meta** header, the pyroject file system tree or the **=== tree** header, the **toml file** for the **=== pyproject.toml** header or the content of the rest of the files of the filesystem the user wants to specify.

The text that must be changed by the meta variables must be defined like this between double brackets (**{{...}}**), e.g. === **{{name}}**/**{{name}}**.md 

To clarify what has been explained before, the template must have the following syntax.

```
=== meta
author: 
name: 
email:

=== tree
pyproject.toml
tests/
- _test-1.py
exemplo/
{{name}}/
- __init__.py
- {{name}}.md

=== pyproject.toml
[build-system]
requires = ["flit_core >=3.2,<4"]
build-backend = "flit_core.buildapi"
[project]
name = "{{name}}"
authors = [ {name = "{{author}}", email = "{{email}}"}]
license = {file = "LICENSE"}
dynamic = ["version", "description"]
dependencies = [ ]
readme = "{{name}}.md"
[project.scripts]
## script1 = "{{name}}:main"

=== tests/_test-1.py
import pytest
import {{name}}
def test_1():
    assert "FIXME" == "FIXME"=== {{name}}/__init__.py
""" FIXME: docstring """
__version__ = "0.1.0"

=== {{name}}/{{name}}.md
# NAME
{{name}} - FIXME the fantastic module for...

```

To run this tool, just use the command **mkfstree** combined with the arguments/options defined in the next subsection.

### **Options** 

- **-v VARS [VARS ...]**,**--vars VARS [VARS ...]** 
    - Meta variables of the project
    - VARS -> [VAR_NAME=VAR_VALUE], (e.g. name=my_project)
- **template ->** Path to the template file
- **-o OUTPUT**,**--output OUTPUT ->** Path of the output folder
- **-i**,**--interactive ->** Interactive mode
    - Ask if the user wants to replace the content of a meta variable, inform if meta variables are missing and ask for a value for such meta variables.
- **-h**,**--help->** Show help message

### **Strategy**

The strategy used to create the file system tree from a given template was the following:
- Split the template file by secctions
- Parse the meta variables and store them in a dictionary
- Parse the tree provided in the template and create the directories defined in the tree that will be needed for the pyproject
- Parse the file sections. Create the files with the provided content in the respective path.

> **Note:** In each of the parse operations realized, the meta variables are replaced with its value

---

## **mktemplateskel - Create Templates from a file system tree**
With **mktemplateskel**, from a file system tree, create a template file.
This template can be used to create a new file system tree, with the command **mkfstree**.

The file system tree must contain a **pyproject.toml**.


### **Options**

- **-v VARS [VARS ...]**,**--vars VARS [VARS ...]** 
    - Meta variables of the project
    - VARS -> [VAR_NAME=VAR_VALUE], (e.g. name=my_project)
- **-p PROJECT_PATH**,**--project_path PROJECT_PATH  ->** Path of the project folder
- **-o OUTPUT**,**--output OUTPUT  ->** Path of the output folder
- **-i**,**--interactive  ->** Interactive mode
    - Ask if the user wants to replace the content of a meta variable
- **-e**,**--exclude EXCLUDE [EXCLUDE ...]  ->** Exclude file content from being replaced with meta variables
    - all 
    - .[file_extension] (e.g. .py)
    - specific files (e.g. test.py, *.py, ...)
- **-h**,**--help  ->** Show help message

### **Strategy**

The strategy used to create the template file was the following:
- Walk through the file system tree with the **os.walk** function
- For each file, read its content and save it in an array
- For the pyproject.toml file, save some of its content as meta variables
- Add this with the meta variables provided by the user
- Replace the meta variables found in the files 
- Now, create the template, with the structure mentioned above.

---

### **Authors**

- [Diogo Vieira](https://github.com/DiogoVieira63)
- [Eduardo Magalhães](https://github.com/edumagalhaes10)