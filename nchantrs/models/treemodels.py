# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""  #																			||
---  #																			||
<(META)>:  #																	||
	docid: 'ce981f8c-de77-4054-ae2f-e30049bb318a'  #							||
	name:	#																	||
	description: >  #															||
	expirary: <[expiration]>  #													||
	version: <[version]>  #														||
	authority: document|this  #													||
	security: sec|lvl2  #														||
	<(WT)>: -32  #																||
"""  # ||
# -*- coding: utf-8 -*-#														||
# ================================Core Modules===================================||
from os.path import abspath, dirname, join
import json as j
import datetime as dt
from math import isnan
from typing import Optional, Dict, List, Any, Tuple

import logging


logger = logging.getLogger(__name__)
# ===============================================================================||
from pandas import DataFrame
from subtrix.utilities import uuid
from condor.utils import thingify

# ===============================================================================||
from condor import condor
from nchantrs.libraries import pyqt, qpandas
from nchantrs.widgets.items.nodes import NchantdNode, NchantdTreeNode
from nchantrs.utilities.models import combine_records
from ogma.logma import Logma

# ===============================================================================||
here = join(dirname(__file__), "")  # ||
log = False
logma = Logma(__name__)
logma.off()

# ===============================================================================||
pxcfg = join(abspath(here), "_data_", "treemodels.yaml")


class NchantdFileSystemModel(pyqt.QFileSystemModel):
    """ """

    def __init__(self, parent=None, root=None, cfg={}) -> None:
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdTreeModel")
        self.config.override(cfg)
        if parent:
            self.config.override(parent.config)
        super().__init__()

    def initModel(self, new_instance=False) -> None:
        """ """
        self.setRootPath("")
        return self

    def buildNodes(self) -> None:
        """the app_tree_nodes table doesn't make sense with the file system as the
        data source but I need to figure out how to turn of the expectation"""
        return self


class NchantdTreeModel(pyqt.QStandardItemModel):
    """Model for standard Nchantd Tree used largely as the primary navigation structure for all Nchantd Apps"""

    def __init__(self, parent=None, root=None, cfg=None) -> None:
        """
        Provide the parent which will usually be the application model and a root if this this is an instance of a
        subtree
        :param parent:
        :param root:
        :param cfg:
        """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdTreeModel")
        if parent:
            self.config.override(parent.config)
        super().__init__()
        self.config.override(cfg)
        self.store = self.parent.app.model.store
        self.current_node = None
        self.current_nid = None
        self.today = None
        self.now = None
        self.nodes = DataFrame()
        self.rows = []
        self.tabs = []
        self.nodetable = "vw_tree_node"
        if log:
            logma.info(self.config.dikt["dstruct"]["database"]["objects"]["table"].keys())
        self.nodecolumns = [
            x["name"] for x in self.config.dikt["dstruct"]["database"]["objects"]["table"]["app_tree_node"]["columns"]
        ]
        self.nodebase = ["system_local", 0, 0, 1, 1, 1, 1, 0, 0, 0]
        self.tabbase = [0, 1, 1, 1]
        self.newNodes = []
        self.tabsets = self.config.dikt["tabsets"]
        self.previous_node = None
        self.home_node = None

    def initModel(self, position=False) -> None:
        """ """
        [DONE]
        logma.info(f"Model Initialize Application {self.parent.app.new_application}")
        # logma.info(f"Model Initialize Instance {self.parent.app.new_instance}")
        db = "db"
        if self.parent.app.model.instance.internal is False:
            db = self.parent.app.model.instance.db_instance_id
        objects = combine_records(self.config.dikt["dstruct"]["database"]["objects"])
        logma.info(f"New Application {self.parent.app.new_application}")
        if self.parent.app.new_application:
            self.create_objects(objects)
        if self.parent.app.new_application:  # or self.parent.app.new_instance:
            self.create_objects_instance(objects, db)
        self.nodes = self.get_nodes()
        return self

    def create_objects(self, objects) -> None:
        """"""
        records = objects["table"]["app_tree_node"]["records"]
        objects["table"]["app_tree_node"]["records"] = [x + self.nodebase for x in records if x is not None]
        app_objects = {
            "table": {
                "app_tree_node": {
                    "records": objects["table"]["app_tree_node"]["records"],
                    "columns": objects["table"]["app_tree_node"]["columns"],
                }
            },
            "view": self.config.dikt["dstruct"]["database"]["objects"].get("view", {}),
        }
        self.parent.app.model.store.create_objects(app_objects, "db", False)
        return self

    def create_objects_instance(self, objects, db="db") -> None:
        """"""
        records = objects["table"]["doc_tree_node"]["records"]
        objects["table"]["doc_tree_node"]["records"] = [x + self.nodebase for x in records if x is not None]
        doc_objects = {
            "table": {
                "doc_tree_node": {
                    "records": objects["table"]["doc_tree_node"]["records"],
                    "columns": objects["table"]["doc_tree_node"]["columns"],
                }
            }
        }
        self.parent.app.model.store.create_objects(doc_objects, db, False)
        return self

    def add_child(self, pid) -> None:
        """"""
        self.add_node(pid)
        return self

    def add_sibling(self, name, ntype, pid) -> None:
        """"""
        self.add_node(name, ntype, pid)
        return self

    def add_node_set(self) -> None:
        """"""
        return self

    def deleteNode(self, node) -> None:
        """ """
        self.deleteChildren(node.nid)
        data = [node.nid, node.name, node.type, node.pid, node.position, node.tabset]
        self.nodes.pop(self.nodes.index(data))
        return node.nid

    def canFetchMore(self, index) -> None:
        """
        called if canFetchMore returns True, then dynamically inserts nodes required for directory contents
        :param index:
        :return:
        """
        node = self.getNode(index)
        # if node.is_dir and not node.is_traversed:
        # 	return True
        return True

    def deleteChildren(self, pid) -> None:
        """"""

        return self

    def get_children(self, parent) -> None:
        """"""
        children = self.parent.app.model.get_nodes(by_parent=parent)
        return children

    def get_nodes(self) -> None:
        """"""
        return self.parent.app.model.get_nodes()

    def get_previous_node(self) -> None:
        """"""
        node = self.previous_node
        if node is None:
            node = self.home_node
        return node

    def insertColumns(self, position, columns, parent=pyqt.QModelIndex()):
        """ """
        self.beginInsertColumns(parent, position, position + columns - 1)
        success = self.root.insertColumns(position, columns)
        self.endInsertColumns()
        return success

    def insertRows(self, position, rows, parent=pyqt.QModelIndex()):
        """ """
        parentItem = self.getItem(parent)
        self.beginInsertRows(parent, position, position + rows - 1)
        success = parentItem.insertChildren(position, rows, self.root.columnCount())
        self.endInsertRows()  # ||
        return success

    def save_state(self, node, db="db") -> None:
        """"""
        if node.app_data_type == "doc":
            table = "doc_tree_node"
        elif node.app_data_type == "app":
            table = "app_tree_node"
        else:
            raise Exception(f"Unknown Instance Type {node.app_data_type}")
        data = {"table": {table: {"data": {}}}}
        if node.expanded is True:
            data["table"][table]["data"]["expanded_bit"] = 1
        else:
            data["table"][table]["data"]["expanded_bit"] = 0
        data["table"][table]["data"]["tabfocus_int"] = node.tab_focus
        data["table"][table]["data"]["readonly_bit"] = node.readonly
        data["table"][table]["data"]["editable_bit"] = node.editable
        data["table"][table]["data"]["moveable_bit"] = node.moveable
        data["table"][table]["data"]["pregnable_bit"] = node.pregnable
        data["table"][table]["data"]["isparent_bit"] = node.is_parent
        logma.info(f"Save Table {table}")
        logma.info(f"Save State {data}")
        logma.info(f"Save State {node.nid}")
        self.parent.app.model.store.update_record(data, "nid_txt", node.nid, db)
        return self

    # def sort_children(self, node, parent, db="db") -> None:
    #     """"""
    #     data = {"table": {"doc_tree_node": {"data": {}}}}
    #     children = self.get_children(node)
    #     children.sort(key=lambda x: x.name, reverse=False)
    #     for n, child in enumerate(children):
    #         data["table"]["doc_tree_node"]["data"]["position"] = n
    #         self.parent.app.model.store.update_record(data, "nid_txt", child.nid, db)

    def swap_parent(self, node, parent, db="db") -> None:
        """"""
        data = {"table": {"doc_tree_node": {"data": {}}}}
        data["table"]["doc_tree_node"]["data"]["pid_txt"] = parent.nid
        self.parent.app.model.store.update_record(data, "nid_txt", node.nid, db)
        return self

    def updateStatus(self, status) -> None:
        """Modifiy Application widgetStatus for driving global events in other \
			widget stacks"""
        # rerun the 2ndpane build sequence based on the tabaset of the node
        # self.app.updateStatus(self, status)
        return self


class NchantdApplicationTreeModel(NchantdTreeModel):
    """"""

    def __init__(self, parent=None, root=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdApplicationTreeModel")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self.parent, root, self.config)
        self.config.override(cfg)

    def initModel(self) -> None:
        """"""
        super().initModel()
        # self.parent.app.model.register_action(self.set_today)
        return self


class NchantdTimeTreeModel(NchantdApplicationTreeModel):
    """Nchantd Time Tree Model builds a dataset of year, month, week, day
    hiearchies with a few variations for how the nodes and tabs are created
    for each of the levels"""

    def __init__(self, parent=None, root=None, name=None, cfg={}) -> None:
        """ """
        if log:
            logma.info(f"NchantdTimeTreeModelParent {parent.config.dikt.keys()}")
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdTimeTreeModel")
        if parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        root = None
        super().__init__(self.parent, root, cfg)

        known_nodes = None
        if known_nodes is None:
            known_nodes = qpandas.DataFrame()
        self.known_nodes = known_nodes
        self.year = dt.datetime.now().strftime("%Y")

    def addCenturyNode(self) -> None:
        """ """
        return self

    def addDayNode(self) -> None:
        """"""
        return self

    def addDecadeNode(self) -> None:
        """ """
        return self

    def addHourNode(self) -> None:
        """"""
        return self

    def addMinuteNode(self) -> None:
        """"""
        return self

    def addMonthNode(self) -> None:
        """"""
        return self

    def addWeekNode(self) -> None:
        """ """
        return self

    def addYearNode(self, nid, name, pid, pos, base, year) -> None:
        """ """
        rnid = self.addNode(nid, name, "node", pid, pos, base, "NchantdYearTabSet")
        pid = nid
        for month in range(1, 13):
            name = calcts.getMonthLabel(month)
            tabset = "NchantdMonthOfDaysTabSet"
            rnid = self.addNode(rnid, name, "node", pid, pos, base, tabset)
            pos += 1
        return rnid

    def define_structure(self, structure) -> None:
        """select structure of Time Tree"""

        return self

    def genYearMonthTreeData(self, src, pos=0, pid=0) -> None:
        """Generate a table of date nodes for initilization of a timeline based
        tree widget
        need to get first data from data? or hand it the date?"""
        format = "%d/%m/%Y %H:%M:%S"
        self.known_nodes = self.getNodes()
        startdate = calcts.getDateObject(f"01/01/{self.year} 00:00:00", format)
        enddate = calcts.getTodayObject()  # .addDays(30)
        nodes, tabs = [], []
        if log:
            logma.info(f"Knwon Nodes {self.known_nodes}")
        for year in range(int(enddate.year) - int(startdate.year) + 5):
            year += startdate.year
            if log:
                logma.info(f"Year {year}")
            if str(year) in self.known_nodes["name"].values.tolist():
                if log:
                    logma.info(f"Year {year} exists in data")
                continue
            nid, nodes, tabs = self.genYearNode(tabs, nodes, Thing().uuid, year, pid, pos, year)
            pos += 1

        df = qpandas.DataFrame(nodes, columns=self.nodecolumns)
        # if not self.known_nodes.empty:
        # 	df = df[df['name'].isin(self.known_nodes['name'].values.tolist())]
        if log:
            logma.info(f"Date Nodes {df}")
        src.docs["db"].write({"app_tree_nodes": df})

        [DONE]
        # self.tabcolumns = self.config.dikt['dstruct']['database']['objects']['table']['tabs']['columns']
        # df = qpandas.DataFrame(tabs, columns=self.tabcolumns)
        # df['uuid'] = df['name'].apply(lambda x: uuid.UUID(str(uuid.uuid4())).hex)
        # src.docs['db'].write({'tabs': df})

        return nid

    def genYearNode(self, tabs, nodes, nid, name, pid, pos, year) -> None:
        """ """

        tbase = [0, 1, 1, 1, 0]
        tabset = "NchantdSummaryOfMonthsTabSet"
        icon = ""
        nodes.append([nid, icon, name, "node", pid, pos] + self.nodebase)
        widget = "dashboards.NchantdYearSummary"
        widget = "editors.NchantdJournalEditor"
        data = f"This is the data {year}"
        data = j.dumps({"text": data})
        tabs.append([name, widget, data, nid, 0] + tbase)
        pid = nid
        for month in range(1, 13):
            name = calcts.getMonthLabel(month)
            icon = ""
            nid = Thing().uuid
            nodes.append([nid, icon, name, "node", pid, pos, "{}"] + self.nodebase)
            tabs += self.genMonthOfDays(month, year, nid, tbase)
            pos += 1
        return nid, nodes, tabs

    def genMonthOfDays(self, month, year, pid, base) -> None:
        """ """
        widget = "editors.NchantdJournalEditor"
        lastday = int(calcts.getLastDayofMonth(month, year))
        tabs = []
        pos = 0
        for day in range(1, lastday + 1):
            # if log: print(f'Create Day {day} of Month {month} and Year {year}')
            data = f"This is the data {day}"
            data = j.dumps({"text": data})
            tabs.append([day, widget, data, pid, pos] + base)
            pos += 1
        return tabs

    def initData(self, pos=0, pid=0, nid=None) -> None:
        """Generate a table of date nodes for initilization of a timeline based
        tree widget
        need to get first data from data? or hand it the date?"""
        # raise Exception()
        format = "%d/%m/%Y %H:%M:%S"
        if pid != 0 and nid == None:
            node = self.store.getNode(pid)
            nid = node.nid
        else:
            nid = 1
        startdate = dt.datetime.strptime("01/01/2022 00:00:00", format)
        for year in range(int(startdate.year) + 5):
            year += startdate.year
            nid = self.addYearNode(nid, year, pid, pos, self.nodebase, year)
            pos += 1
        df = DataFrame(self.nodes, columns=self.nodecolumns)
        self.store.docs["db"].write({"app_tree_nodes": df})

    def initModel(self) -> None:
        """"""
        super().initModel()


# ===========================Code Source Examples================================||
"""
"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
