# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name:
	description: >
	version: 0.0.0.0.0.0
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, join
import datetime as dt

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from nchantdoffice.models import NchantdOfficeCloakModel
from ogma.logma import Logma
from pyffice.notes.cherrytree import PyfficeCherryTree
from pyffice.pyffice import PyfficeDocument
from squirl.orgnql import fonql

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "nchantrs.yaml")


def convert_cherrytree_2_nchantdbook(path, name=None, import_=False):
    """"""
    doc = PyfficeNchantdBook(cfg)
    cherry_doc = PyfficeCherryTree.open(path)
    for node in cherry_doc.get_nodes():
        doc.create_node()


def convert_filesystem_2_nchantdbook(path, name=None, import_=False):
    """"""
    doc = PyfficeNchantdBook(path)
    doc.create_note_book()
    f_doc = fonql.Doc(path)
    while True:
        data = next(f_doc, None)
        if data is None:
            break
        for node in data:
            if name is None:
                name = node["name"]
            doc.create_node(node, node["name"], node["content"])
            doc.finish_node()
    doc.finish_note_book()
    doc.save_as(f"{path}/{name}.ctd")


def convert_excel_2_nchantdmatrix(path, name=None):
    """"""


def convert_word_2_nchantdscript(path, name=None):
    """"""


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
