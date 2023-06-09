#!/usr/bin/env python3

'''Module to create templates given a project path (mktemplateskel) and create a file system tree given a template (mkfstree)
'''
__version__ = "0.1"

from multifile_temps.mkfstree import mkfstree
from multifile_temps.mktemplateskel import mktemplateskel


def run_mkfstree():
    mkfstree()

def run_mktemplateskel():
    mktemplateskel()
