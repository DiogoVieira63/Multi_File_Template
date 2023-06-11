# Template Multi-file

**Mudar e adicionar dependencias**
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
[![pytesseract](https://img.shields.io/badge/pytesseract->=0.3.10-blue.svg)](https://shields.io/)
[![License](https://img.shields.io/npm/l/express?style=flat-square)](https://github.com/edumagalhaes10/tp_spln/blob/main/LICENSE)

### ⚙️ Installation

To install and use this tool follow the steps below:
- Clone this repository
- Run either *flit install* or *pip install -e* in the project directory



## mkfstree - Create a file system tree from a template

This tool has the purpose to create a file system tree given a template. 

**FALAR DA ESTRUTURA DO TEMPLATE**

To run this tool, just use the command **mkfstree** combined with the following arguments/options.

### Options 

- **-v VARS [VARS ...]**,**--vars VARS [VARS ...]** 
    - Meta variables of the project
    - VARS -> [VAR_NAME=VAR_VALUE], (e.g. name=my_project)
- **template ->** Path to the template file
- **-o OUTPUT**,**--output OUTPUT ->** Path of the output folder
- **-i**,**--interactive ->** Interactive mode
- **-h**,**--help->** Show help message

### Strategy



## mktemplateskel - Create Templates from a file system tree
With **mktemplateskel**, from a file system tree, create a template file.
This template can be used to create a new file system tree, with the command **mkfstree**.

The file system tree must contain a **pyproject.toml**.


### Options

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

### Strategy

The strategy used to create the template file was the following:
- Walk through the file system tree with the **os.walk** function
- For each file, read its content and save it in an array
- For the pyproject.toml file, save some of its content as meta variables
- Add this with the meta variables provided by the user
- Replace the meta variables found in the files 
- Now, create the template, with the structure mentioned above.


---

### Authors

- [Diogo Vieira](https://github.com/DiogoVieira63)
- [Eduardo Magalhães](https://github.com/edumagalhaes10)