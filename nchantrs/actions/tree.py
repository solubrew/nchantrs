# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid: 62ea7f1-d120-4d97-92b4-2ed26d0aee4a
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
from nchantrs.dialogs.new import NewNchantdNodeSigil
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "tree.yaml")


# def add_node(name, app, params=None):
#     """"""
#     logma.info(f"Name {name}")
#     logma.info(f"App {app}")
#     sigil = NewNchantdNodeSigil(app).initWidget()
#     if sigil.ok:
#         name = sigil.name.textbox.entry_data
#         logma.info(f"Name {name}")
#         ntype = "node"
#         pid = app.view.panes["left"].model.current_node.nid
#         app.view.panes["left"].model.current_node.max_position += 1
#         pos = app.view.panes["left"].model.current_node.max_position
#         app.view.panes["left"].model.add_node(name, ntype, pid, pos)
#         app.view.panes["left"].view.refresh()
#         # app.model.get_nodes()
#         # app.view.panes['left'].view.initView()


# def add_node_child(name, app, params=None):
#     """
#     Launch dialog
#             enter node name
#             select node icon
#     create node with the parent as the current node
#     :return:
#     """
#     logma.info(f"Name {name}")
#     logma.info(f"App {app}")
#     sigil = NewNchantdNodeSigil(app).initWidget()
#     if sigil.ok:
#         name = sigil.name.textbox.entry_data
#         logma.info(f"Name {name}")
#         ntype = "node"
#         pid = app.view.panes["left"].model.current_node.nid
#         app.view.panes["left"].model.current_node.max_position += 1
#         pos = app.view.panes["left"].model.current_node.max_position
#         app.view.panes["left"].model.add_node(name, ntype, pid, pos)
#         app.view.panes["left"].view.refresh()
#         # app.view.panes['left'].view.refresh()


# def add_node_sibling(name, app, params=None):
#     """
#     Launch dialog
#             enter node name
#             select node icon
#     create node with the same parent as the current node
#     :return:
#     """
#     logma.info(f"Name {name}")
#     logma.info(f"App {app}")
#     sigil = NewNchantdNodeSigil(app).initWidget()
#     if sigil.ok:
#         name = sigil.name.textbox.entry_data
#         ntype = "node"
#         pid = app.view.panes["left"].model.current_node.pid
#         app.view.panes["left"].model.current_node.max_position += 1
#         pos = app.view.panes["left"].model.current_node.max_position
#         app.view.panes["left"].model.add_node(name, ntype, pid, pos)
#         app.view.panes["left"].view.refresh()
#         # app.view.panes['left'].view.refresh()


# def add_node_subtree(name, app, params=None):
#     """"""
#     sigil = ImportNchantdSubtreeSigil(app).initWidget()
#     if sigil.ok:
#         name = sigil.name.entry_data
#         ntype = "node"
#         pid = app.view.panes["left"].model.current_node.nid
#         app.view.panes["left"].model.current_node.max_position += 1
#         for node in sigil.nodes:
#             name = node.name
#             ntype = node.ntype
#             pid = node.pid
#             pos = app.view.panes["left"].model.current_node.max_position
#             app.view.panes["left"].model.add_node(name, ntype, pid, pos)
#
#
# def add_node_top(name, app, params=None):
#     """
#     Launch dialog
#             enter node name
#             select node icon
#     create top level node refresh tree
#     :return:
#     """
#     logma.info(f"Name {name}")
#     logma.info(f"App {app}")
#     sigil = NewNchantdNodeSigil(app).initWidget()
#     if sigil.ok:
#         name = sigil.name.textbox.entry_data
#         ntype = "topnode"
#         pid = "0"
#         app.view.panes["left"].model.current_node.max_position += 1
#         pos = app.view.panes["left"].model.current_node.max_position
#         app.view.panes["left"].model.add_node(name, ntype, pid, pos)
#         app.view.panes["left"].view.refresh()
#
#
# def childadd():
#     """Add a child to the currently selected node"""
#
#
# def childrendelete():
#     """Mark the currently selected nodes children deleted"""
#
#
# def nodedelete():
#     """Mark the currently selected node deleted"""
#
#
# def nodedown():
#     """Move currently selected node down in the tree structure"""
#
#
# def nodeedit():
#     """Edit currently selected node features"""
#
#
# def nodeup():
#     """Move currently seleted node up in the tree structure"""
#
#
# def siblingadd():
#     """Add a sibling node to the currently selected node"""
#

# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
