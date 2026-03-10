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
import json as j
import threading

# ======================================3rd Party Library Modules=====================================================||
from pandas import DataFrame

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from nchantrs.libraries import pyqt
from nchantrs.widgets.items.items import NchantdItem, NchantdTreeItem
from nchantrs.widgets.widgets import NchantdWidgetMixin
from ogma.logma import Logma


# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
debug = False
if not log:
    logma.off()

# ====================================================================================================================||
pxcfg = join(abspath(here), "_data_/nodes.yaml")


class NchantdNode(NchantdItem):
    """
    NchantdNode

    This class represents a node in the Nchantd tree structure.

    __init__(self, parent, item, nid, node, df=DataFrame())
        Initializes a NchantdNode object.
        :param parent: The parent node.
        :param item: The item name.
        :param nid: The node ID.
        :param node: The node data.
        :param df: The DataFrame containing children nodes data. Default value is an empty DataFrame.

    addChildNode(self)
        Adds a child node to the current node.
        :return: The added child node.

    addSibilingNode(self)
        Adds a sibling node to the current node.
        :return: The added sibling node.

    deleteChildren(self, pid)
        Deletes children nodes with the given parent ID.
        :param pid: The parent ID of the nodes to be deleted.

    initModel(self)
        Initializes the model of the node.

    initView(self)
        Initializes the view of the node.

    initWidget(self)
        Initializes the widget of the node.
        :return: The initialized NchantdNode object.

    data(self, column)
        Retrieves data of the node at the specified column index.
        :param column: The column index.
        :return: The data at the specified column index.

    loadChildren(self, df)
        Loads children nodes from the provided DataFrame.
        :param df: The DataFrame containing children nodes data.
        :return: The current node with loaded children nodes.

    hasChildren(self, nid)
        Checks if the node has children with the given node ID.
        :param nid: The node ID.
        :return: True if the node has children, False otherwise.

    updateTabs(self, view='center')
        Updates the tabs of the parent node.
        :param view: The view to update the tabs in. Default value is 'center'.
        :return: The updated parent node.
    """

    def __init__(self, parent, item, nid, node, children, df=DataFrame(), cfg=None):
        """
        :param parent: The parent node of the current node.
        :param item: The item displayed in the tree node.
        :param nid: The unique identifier for the node.
        :param node: The node configuration information.
        :param df: The DataFrame object associated with the node.

        This method initializes a new instance of the NchantdNode class. It sets the parent, config, name,
        children_df, item, itemData, nid, node, expanded, treeid, readonly, editable, visible, moveable, pregnable,
        isparent, tabfocus, model, and view attributes of the object.

        """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdNode")
        if parent:
            self.config.override(parent.config)
        logma.info(f"Item {item}")
        self.name = item
        self.children_df = children
        self.item = item  # data displayed in the tree node
        self.itemData = [item, nid]
        self.nid = nid
        self.node = node
        self.position = None

        # self.setDragEnabled(True)
        # self.model = NchantdNodeModel(self, self.config)
        # self.view = NchantdNodeView(self)

    def initModel(self):
        """ """
        self.model.initModel()
        return self

    def initView(self):
        self.layout = pyqt.QVBoxLayout()

        self.setModel(self.parent.model)
        self.setLayout(self.layout)
        self.initUI()
        self.initContextMenu()
        self.initTriggers()

    def initWidget(self):
        """ """
        self.initModel()
        self.initView()
        return self

    def addChildNode(self):
        """ """
        return self

    def addSibilingNode(self):
        """ """
        return self

    def deleteChildren(self, pid):
        """"""

        return self

    def data(self, column):
        try:
            return self.itemData[column]
        except IndexError:
            return None

    def loadChildren(self, df):
        """ """
        children = df[df["parentid"] == str(self.nid)]
        for index, child in children.iterrows():
            item = NchantdNode(self, child["name"], child["nid"], child, df[df["parentid"] == child["nid"]])
            item.initWidget()
            item.loadChildren(df)
            item.hasChildren(child["nid"])
            self.appendRow(item)
        self.is_loaded = True
        return self

    def hasChildren(self, nid):
        """ """
        self.is_expandable = True
        return self

    def initContextMenu(self):
        """ """
        self.setContextMenuPolicy(pyqt.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.onRightClick)
        return self

    def initTriggers(self):
        """ """
        self.doubleClicked.connect(self.onLeftDoubleClick)
        self.expanded.connect(self.onExpand)
        self.clicked.connect(self.onLeftClick)
        return self

    def initUI(self):
        """ """
        return self

    def onExpand(self):
        """ """
        return self

    def onRightClick(self):
        """ """

    def onLeftDoubleClick(self, signal):
        return self

    def onLeftClick(self, signal):
        return self

    def onMiddleClick(self):
        """ """
        return self

    def onSelection(self, fx, mod=None):
        """On selection of tree node load data for tabs in center widget"""
        event.on_clickleft_press(fx)

        return

    def onDeselection(self, fx, mod=None):
        """On deslection of tree node save any changes to node options"""
        event.on_clickleft_release(fx)
        return

    def onEnter(self, fx, mod=None):
        """Need to build if a node was selected an enter create a new sibling
        node. shift-enter creates a new child node, ctrl-enter creates
        a new tab in the node"""
        event.on_enter_kp(fx, mod)
        return

    def onDelete(self, fx, mod=None):
        """Launch Dialog to confirm deletion of node, which marks as deleted in database
        and is not removed until a database cleanup is run"""

    def update_position(self):
        """"""

    def _set_font(self):
        """"""
        font = self.font()
        font.setPointSize(20)
        self.setFont(font)


class NchantdTreeNode(NchantdTreeItem):
    """
    NchantdTreeNode - TODO: is failing due to not accepting NchantdTreeItem to the NchantdTreeModel

    This class represents a node in the Nchantd tree structure.

    __init__(self, parent, item, nid, node, df=DataFrame())
        Initializes a NchantdNode object.
        :param parent: The parent node.
        :param item: The item name.
        :param nid: The node ID.
        :param node: The node data.
        :param df: The DataFrame containing children nodes data. Default value is an empty DataFrame.

    addChildNode(self)
        Adds a child node to the current node.
        :return: The added child node.

    addSibilingNode(self)
        Adds a sibling node to the current node.
        :return: The added sibling node.

    deleteChildren(self, pid)
        Deletes children nodes with the given parent ID.
        :param pid: The parent ID of the nodes to be deleted.

    initModel(self)
        Initializes the model of the node.

    initView(self)
        Initializes the view of the node.

    initWidget(self)
        Initializes the widget of the node.
        :return: The initialized NchantdNode object.

    data(self, column)
        Retrieves data of the node at the specified column index.
        :param column: The column index.
        :return: The data at the specified column index.

    loadChildren(self, df)
        Loads children nodes from the provided DataFrame.
        :param df: The DataFrame containing children nodes data.
        :return: The current node with loaded children nodes.

    hasChildren(self, nid)
        Checks if the node has children with the given node ID.
        :param nid: The node ID.
        :return: True if the node has children, False otherwise.

    updateTabs(self, view='center')
        Updates the tabs of the parent node.
        :param view: The view to update the tabs in. Default value is 'center'.
        :return: The updated parent node.
    """

    def __init__(self, parent, name, nid, node, children=DataFrame()):
        """
        :param parent: The parent node of the current node.
        :param item: The item displayed in the tree node.
        :param nid: The unique identifier for the node.
        :param node: The node configuration information.
        :param df: The DataFrame object associated with the node.

        This method initializes a new instance of the NchantdNode class. It sets the parent, config, name,
        children_df, item, itemData, nid, node, expanded, treeid, readonly, editable, visible, moveable, pregnable,
        isparent, tabfocus, model, and view attributes of the object.

        """
        super().__init__(parent)
        self.parent = parent
        self.config.override(condor.Instruct(pxcfg).select("NchantdTreeNode"))
        self.item = name  # data displayed in the tree node
        self.name = node["name_txt"]
        self.nid = nid
        self.itemData = [name, nid]
        self.node = node
        self.pid = self.node.get("pid_txt", "0")
        self.children_df = children
        try:
            self.parameters = j.loads(self.node["parameters_dict"].replace("'", '"'))
        except Exception as e:
            logma.info(f"Parameters: {self.node['parameters_dict']}")
            self.parameters = {}
            if debug:
                raise e
        self.nodes = []
        self.max_position = 0
        self.position = 0
        self.tabs = []
        self.place_holder = None

    def initModel(self, cfg=None):
        """ """
        super().initModel(cfg)
        self.tab_focus = self.node.get("tabfocus_txt", 0)
        self.node_type = self.node["ntype_txt"]
        self.expanded = self.node["expanded_bit"]
        self.treeid = self.node["treeid_txt"]
        self.readonly = self.node["readonly_bit"]
        self.editable = self.node["editable_bit"]
        self.visible = self.node["visible_bit"]
        self.moveable = self.node["moveable_bit"]
        self.pregnable = self.node["pregnable_bit"]
        self.position = self.node["position_int"]
        self.is_parent = self.node["isparent_bit"]
        self.is_loaded = False
        self.tab_focus = self.node["tabfocus_int"]
        logma.info('Name ' + self.node['name_txt'])
        self.setText(0, self.node["name_txt"], False)
        self._set_font()
        self._set_icon()
        self._set_font_color()
        self.app_data_type = self.node["app_data_type"]
        self.set_data_focus()
        self.set_recent_tabs()

        return self

    def initView(self, path=None):
        """"""
        self.set_expanded(self.expanded)
        return self

    def initWidget(self):
        """ """
        self.initModel()
        self.initView()
        return self

    def addChildNode(self):
        """ """
        return self

    def addSibilingNode(self):
        """ """
        return self

    def deleteChildren(self, pid):
        """"""

        return self

    def hasChildren(self, nid):
        """ """
        self.is_expandable = True
        return self

    def get_children(self):
        """
        Get all child nodes of this tree item.
        """
        children = []
        for i in range(self.childCount()):
            child = self.child(i)
            if hasattr(child, "nid"):  # Ensure it's a proper node
                children.append(child)
        return children

    def loadChildren(self, df):
        """ """
        df.sort_values(by=["position_int", "name_txt"], inplace=True)
        children = df[df["pid_txt"] == str(self.nid)]
        if self.expanded:
            self.place_holder = False
            for index, child in children.iterrows():
                item = self.treeWidget().view.node_widget(self, child["name_txt"], child["nid_txt"], child)
                item.initWidget()
                item.loadChildren(df)
                self.nodes.append(item)
                self.addChild(item)
        else:
            if not children.empty:
                self.place_holder = True
                self.addChild(pyqt.QTreeWidgetItem(self, ["Loading..."]))
        self.is_loaded = True
        return self

    def set_expanded(self, expand=True):
        """"""
        self.setExpanded(expand)
        return self

    def set_data_focus(self):
        """"""
        self.focus = self.parameters.get("focus", "office")
        # TODO: causing an error over pulling two themes midnight_dusk
        # if self.focus != self.app.view.theme.focus:
        #    self.app.view.theme.refocus_theme(self.focus)
        return self

    def set_recent_tabs(self):
        """"""
        self.recent_center_tab = self.parameters.get("recent_tab", {}).get("center", {})
        self.recent_right_tab = self.parameters.get("recent_tab", {}).get("right", {})
        return self

    # def set_as_current(self):
    #     """Set this node as the current/focused node in the tree"""
    #     if hasattr(self, "app") and hasattr(self.app.view.panes["left"], "tree"):
    #         tree = self.app.view.panes["left"].tree
    #         if hasattr(tree, "setCurrentItem"):
    #             tree.setCurrentItem(self)
    #         if hasattr(tree, "setFocus"):
    #             tree.setFocus()
    #     return self

    def setText(self, column, text, store=True):
        """"""
        super().setText(column, text)
        return self

    def sort_by_criteria(self, criteria="name", order="ascending", update_db=True):
        """
        Sort children by various criteria.

        Args:
            criteria: 'name', 'date_created', 'position', 'type'
            order: 'ascending' or 'descending'
            update_db: Whether to update database positions
        """
        children = self.get_children()

        # Define sort keys for different criteria
        sort_keys = {
            "name": lambda x: x.name.lower(),
            "date_created": lambda x: getattr(x, "date_created", ""),
            "position": lambda x: getattr(x, "position", 0),
            "type": lambda x: getattr(x, "node_type", ""),
            "custom": lambda x: (x.node_type, x.name.lower()),  # Sort by type, then name
        }

        if criteria not in sort_keys:
            raise ValueError(f"Invalid sort criteria: {criteria}")

        # Sort children
        reverse_order = order == "descending"
        children.sort(key=sort_keys[criteria], reverse=reverse_order)

        # Update UI
        self._update_tree_ui(children)

        # Update database if requested
        if update_db:
            self._batch_update_positions(children)

        return self

    def sortChildren(self, column=0, order="ascending", db="db", sort_key=None):
        """
        Sort children of the tree node and update database positions efficiently.

        Args:
            column: Column to sort by (default: 0)
            order: Sort order - "ascending" or "descending"
            db: Database identifier
            sort_key: Custom sort function (optional)
        """
        # Sort the UI first
        if order == "ascending":
            super().sortChildren(column, pyqt.Qt.SortOrder.AscendingOrder)
        else:
            super().sortChildren(column, pyqt.Qt.SortOrder.DescendingOrder)

        # Get children and prepare for batch update
        children = self.get_children()
        if not children:
            return self

        # Apply custom sorting if provided, otherwise sort by name
        if sort_key:
            children.sort(key=sort_key, reverse=(order == "descending"))
        else:
            children.sort(key=lambda x: x.item.lower(), reverse=(order == "descending"))

        # TODO: Batch update database positions
        # self._batch_update_positions(children, db)
        data = {"table": {"doc_tree_node": {"data": {}}}}  # This will not allow for sorting of application tree nodes
        for n, child in enumerate(children):
            data["table"]["doc_tree_node"]["data"]["position_int"] = n
            self.parent.app.model.store.update_record(data, "nid_txt", child.nid, db)
        return self

    def updateTabs(self, view="center"):
        """ """
        # logma.inspect_caller()
        self.app.view.panes[view].clear()
        self.app.view.panes[view].model.buildTabSet(self, view)
        self.app.view.refresh_window_size()
        return self

    def _batch_update_positions(self, children, db="db"):
        """
        Efficiently update positions in database using batch operations.
        """
        # Prepare batch update data
        updates = []
        for position, child in enumerate(children):
            updates.append({"nid": child.nid, "position": position, "parent_id": self.nid})

        # Use batch update if available, otherwise fallback to individual updates
        if hasattr(self.parent.app.model.store, "batch_update_positions"):
            self.parent.app.model.store.batch_update_positions(updates, db)
        else:
            # Fallback to individual updates with transaction
            self._individual_updates_with_transaction(updates, db)

    def _individual_updates_with_transaction(self, updates, db):
        """
        Perform individual updates within a transaction for better performance.
        """
        try:
            # Start transaction if supported
            if hasattr(self.parent.app.model.store, "begin_transaction"):
                self.parent.app.model.store.begin_transaction(db)

            for update_data in updates:
                data = {"table": {"doc_tree_node": {"data": {"position": update_data["position"]}}}}
                self.parent.app.model.store.update_record(data, "nid_txt", update_data["nid"], db)

            # Commit transaction
            if hasattr(self.parent.app.model.store, "commit_transaction"):
                self.parent.app.model.store.commit_transaction(db)

        except Exception as e:
            # Rollback on error
            if hasattr(self.parent.app.model.store, "rollback_transaction"):
                self.parent.app.model.store.rollback_transaction(db)
            raise e

    def _update_tree_ui(self, sorted_children):
        """Update the tree widget UI with sorted children."""
        # Remove all children from UI
        for i in range(self.childCount()):
            self.removeChild(self.child(0))

        # Add back in sorted order
        for child in sorted_children:
            self.addChild(child)

    def sort_with_lazy_loading(self):
        """Sort considering lazy loading of children."""
        if not self.is_loaded:
            # Sort will happen when children are loaded
            self.pending_sort = True
            return self

        return self.sortChildren()

    def debounced_sort(self, delay=0.5):
        """Debounce sort operations to avoid excessive database updates."""
        if hasattr(self, "_sort_timer"):
            self._sort_timer.cancel()

        self._sort_timer = threading.Timer(delay, self._perform_sort)
        self._sort_timer.start()

    def _perform_sort(self):
        """Actually perform the sort operation."""
        self.sortChildren()

    def _set_font(self):
        """"""
        font = self.font(0)
        node_types = self.config.dikt["node_types"]
        if self.node_type not in node_types:
            raise Exception(f"Unknown node type {self.node_type}")
        node_type = node_types[self.node_type]
        if not node_type.get("font", None):
            node_type["font"] = 12
        font.setPointSize(node_type["font"])
        self.setFont(0, font)
        return self

    def _set_font_color(self):
        """"""
        node_types = self.config.dikt["node_types"]
        if self.node_type not in node_types:
            raise Exception(f"Unknown node type {self.node_type}")
        node_type = node_types[self.node_type]
        logma.info(f"Set Font Color: {self.app.view.theme.colors[node_type['color']]}")
        self.setForeground(0, pyqt.QBrush(pyqt.QColor(self.app.view.theme.colors[node_type['color']])))
        if self.node["ntype_txt"] == "displaynode":
            logma.info(f"NType {self.node['ntype_txt']}")
            logma.info(f"Node {self.node['name_txt']}")
            # item.setFlags(pyqt.Qt.ItemFlag.NoItemFlags)
            # item.setBackground(0, pyqt.QColor("#5F5FDF"))
            if self.node["name_txt"] == "Action":
                self.setForeground(0, pyqt.QColor("#B71F1F"))
            #    item.setBackground(0, pyqt.QColor("#4F5665"))
            elif self.node["name_txt"] == "Fund":
                self.setForeground(0, pyqt.QColor("#19C26B"))
            #    item.setBackground(0, pyqt.QColor("#4F5665"))
            elif self.node["name_txt"] == "Vision":
                self.setForeground(0, pyqt.QColor("#F6FF00"))
            #    item.setBackground(0, pyqt.QColor("#4F5665"))
            elif self.node["name_txt"] == "Social":
                self.setForeground(0, pyqt.QColor("#D97BCB"))
            #    item.setBackground(0, pyqt.QColor("#4F5665"))
            elif self.node["name_txt"] == "Mech":
                self.setForeground(0, pyqt.QColor("#191CC2"))
            #    item.setBackground(0, pyqt.QColor("#4F5665"))
            elif self.node["name_txt"] == "Anal":
                self.setForeground(0, pyqt.QColor("#F77F05"))
            #    item.setBackground(0, pyqt.QColor("#4F5665"))
            elif self.node["name_txt"] == "Settings":
                self.setForeground(0, pyqt.QColor("#4F5665"))
            #    item.setBackground(0, pyqt.QColor("#4F5665"))
            elif self.node["name_txt"] == "Journal":
                self.setForeground(0, pyqt.QColor("#4F5665"))
            #    item.setBackground(0, pyqt.QColor("#4F5665"))
            else:
                # item.setBackground(0, pyqt.QColor("#5F5FDF"))
                self.setForeground(0, pyqt.QColor("#5F5FDF"))
        # self.setForeground(0, pyqt.QColor("white"))
        return self

    def _set_icon(self, icon_type="accent"):
        """
        #need to get the correct icon based on the parameters focus

        :param icon_type:
        :return:
        """
        icon_cfg = self.config.dikt["node_types"]
        try:
            icon = icon_cfg[self.node_type]["icon"]
        except KeyError:
            raise Exception(f"Unknown node type {self.node_type}")
        logma.info(f"App Model {self.app.model}")
        if self.app.model.user.easter_egg:
            icon = "mist_easter_egg_a0001"
        self.setIcon(0, pyqt.QIcon(self.app.view.theme.get_icon_path(icon, icon_type)))
        return self


class NchantdCanvasNodeMixin(NchantdWidgetMixin):
    """"""

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    def launch_update_sigil(self):
        """"""


class NchantdRectangleNode(NchantdCanvasNodeMixin, pyqt.QGraphicsRectItem):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("Nchantd")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        self.setBrush(pyqt.QBrush(pyqt.QColor(100, 100, 250, 100)))  # Set a light blue color
        self.setPen(pyqt.QPen(pyqt.Qt.black, 2))  # Set the pen color and width

        # Create a text item
        self.text_item = pyqt.QGraphicsTextItem(self.config.dikt["text"], self)
        self.text_item.setDefaultTextColor(pyqt.Qt.black)

        # Position the text item on top of the rectangle
        self.text_item.setPos(self.rect().center() - self.text_item.boundingRect().center())

        # Enable item to be selectable and movable
        self.setFlags(pyqt.QGraphicsItem.ItemIsSelectable | pyqt.QGraphicsItem.ItemIsMovable)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdEllipseNode(NchantdCanvasNodeMixin, pyqt.QGraphicsEllipseItem):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("Nchantd")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdCircleNode(NchantdEllipseNode):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdCircleItem")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdLineNode(NchantdCanvasNodeMixin, pyqt.QGraphicsLineItem):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdLineItem")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdLineArrowNode(NchantdLineNode):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdLineNode")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdLineDoubleArrowNode(NchantdLineArrowNode):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdLineNode")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdImageNode(NchantdCanvasNodeMixin, pyqt.QGraphicsPixmapItem):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdImageItem")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdTextNode(NchantdCanvasNodeMixin, pyqt.QGraphicsTextItem):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdTextItem")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdIrregularShapeNode(NchantdCanvasNodeMixin, pyqt.QGraphicsPathItem):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdIrregularShapeItem")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdPolygonNode(NchantdCanvasNodeMixin, pyqt.QGraphicsPolygonItem):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdPolygonItem")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdTriangleNode(NchantdPolygonNode):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("Nchantd")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
