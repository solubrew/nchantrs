# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""#																			||
---  #																			||
<(META)>:  #																	||
        docid: 'a4955210-9422-43dd-8a94-6f9f90568004'  #							||
        name:	#																	||
        description: >  #															||
        expirary: <[expiration]>  #													||
        version: <[version]>  #														||
        authority: document|this  #													||
        security: sec|lvl2  #														||
        <(WT)>: -32  #																||
"""  # ||

# -*- coding: utf-8 -*-#														||
# ===============================Core Modules====================================||
from os.path import abspath, dirname, join

# ===============================================================================||
from condor import condor
from nchantrs.libraries import pyqt
from subtrix import subtrix
from ogma.logma import Logma
from nchantrs.widgets.items.nodes import NchantdNode, NchantdTreeNode
from nchantrs.widgets.widgets import NchantdWidget

# ===============================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
# logma.off()

# ===============================================================================||
pxcfg = join(abspath(here), "_data_", "treeviews.yaml")


class NchantdTreeView(NchantdWidget):
    """ """

    def __init__(self, parent, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(condor.Instruct(pxcfg).select("NchantdTreeView"))
        if parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.node_widget = None
        # self.current_node = None

    def initView(self) -> None:
        """"""
        super().initView()
        self.parent.setColumnCount(1)
        self.parent.setHeaderLabel("Navigation")
        self.parent.setHeaderHidden(True)
        self.layout.addWidget(self.parent)
        self.set_node_widget(self.config.dikt.get("node_widget", NchantdTreeNode))
        self.init_tree()
        self.initContextMenu()
        self.initTriggers()
        # self.layout.addWidget(self)
        return self

    def init_tree(self) -> None:
        """"""
        self.treedf = self.parent.model.get_nodes()
        self.parent.clear()
        if self.treedf.empty:
            raise Exception("Tree is empty")
        multiroot = self.treedf[self.treedf["pid_txt"] == str(0)]
        multiroot.sort_values(by=["position_int", "name_txt"], inplace=True)
        for index, root in multiroot.iterrows():
            item = self.node_widget(self.parent, root["name_txt"], root["nid_txt"], root)
            item.initWidget()
            if self.parent.model.current_node is None:  # and root["ntype"] != "displaynode":
                self.set_current_node(item)
            item.loadChildren(self.treedf)
            self.parent.addTopLevelItem(item)
        return self

    def initContextMenu(self) -> None:
        """ """
        self.setContextMenuPolicy(pyqt.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.onRightClick)
        return self

    def initTriggers(self) -> None:
        """ """
        # self.doubleClicked.connect(self.onLeftDoubleClick)
        # self.expanded.connect(self.onExpand)
        # self.clicked.connect(self.onLeftClick)
        self.parent.itemPressed.connect(self.onLeftClick)
        self.parent.itemCollapsed.connect(self.on_item_collapsed)
        self.parent.itemExpanded.connect(self.on_item_expanded)
        self.parent.itemSelectionChanged.connect(self.handle_selection_change)
        # Connect signals to methods
        # self.parent.itemClicked.connect(self.on_item_clicked)
        # self.parent.itemActivated.connect(self.on_item_activated)
        # self.parent.itemSelectionChanged.connect(self.on_selection_changed)
        return self

    def initUI(self) -> None:
        """ """
        cfgview = self.config.dikt
        # self.setFixedWidth(cfgview["FixedWidth"])
        self.setAnimated(cfgview["Animated"])
        self.setIndentation(cfgview["IndentSize"])
        return self

    def collapse_children(self, item) -> None:
        """Recursively collapses all child nodes"""
        for i in range(item.childCount()):
            child = item.child(i)
            # Collapse the child
            self.parent.collapseItem(child)
            # Recursively collapse its children
            self.collapse_children(child)
        return self

    def handle_selection_change(self) -> None:
        """"""
        logma.info("Selection Changed")
        # h_scroll = self.parent.horizontalScrollBar().value()
        # logma.info(f"Horizontal scroll position: {h_scroll}")
        # Call parent selection changed
        # super().selectionChanged(selected, deselected)
        selected_items = self.parent.selectedItems()
        if selected_items:
            current_item = selected_items[0]
            # Store the QModelIndex (persistent reference to the item)
            self.previous_index = self.parent.indexFromItem(current_item)
            logma.info(f"Previous index set: {self.previous_index}")
        # # Restore horizontal scroll position
        # logma.info(f"Horizontal set scroll position: {h_scroll}")
        # self.parent.horizontalScrollBar().setValue(h_scroll)
        return self

    def go_to_previous_node(self) -> None:
        """"""
        if self.previous_index:
            # Retrieve and select the previous item using its QModelIndex
            previous_item = self.parent.itemFromIndex(self.previous_index)
            if previous_item:  # Ensure the item still exists
                self.parent.setCurrentItem(previous_item)
                logma.info(f"Returned to previous item: {previous_item.text(0)}")
        return self

    def mousePressEvent(self, event) -> None:
        """ """
        # tree.mousePressEventLog(event, 1)
        if event.button() == pyqt.Qt.RightButton:
            pass
        else:
            pass
        # self.setNodeFocus(event.data)
        super().mousePressEvent(event)
        return self

    def on_item_collapsed(self, item) -> None:
        """"""
        # self.collapse_children(item)
        # if item.expanded is True or item.expanded is None:
        item.expanded = False
        self.parent.model.save_state(item)
        return self

    def on_item_expanded(self, item) -> None:
        """ """
        if item.expanded is True:
            return self
        item.expanded = True
        if item.place_holder is True:
            item.takeChild(0)
            item.loadChildren(self.treedf)
        self.parent.model.save_state(item)
        return self

    def onLeftClick(self, signal=None) -> None:
        """Need to send signal to load center widget with correct tabset and
        populate those tabs with data based on the node selected

        will need to run the pane building function from the nchantrs.Cloak

        """
        h_scroll = self.parent.horizontalScrollBar().value()
        self.cached_splitter_size = self.app.view.splitter.sizes()
        logma.info(f"Horizontal scroll position: {h_scroll}")
        try:
            if self.parent.model.current_node != signal:
                self.set_current_node(signal)
        except Exception as e:
            self.set_current_node(signal)
        # Restore horizontal scroll position
        logma.info(f"Horizontal set scroll position: {h_scroll}")
        self.parent.horizontalScrollBar().setValue(h_scroll)
        self.app.view.splitter.setSizes(self.cached_splitter_size)
        return self

    def onLeftDoubleClick(self, signal) -> None:
        """launch a dialog that allows for modification of parameters
        of the tree node if node is marked as editable:
        - font/style/color of text
        - icon
        - position
        - readonly
        """
        logger.debug(f"Tested Double Click")
        node = self.model.getNodeData(signal.data())
        if node["editable"]:
            dialog = self.config.dikt["nodeeditordialog"]["widget"]
            launchDialog(dialog, node)
        return self

    def onMiddleClick(self) -> None:
        """ """
        self.parent.app.model.update_actions()
        return self

    def onRightClick(self, position=0) -> None:
        """ """
        self.parent.app.model.update_actions()
        # need to replace with build menu
        # here is where context will be introduced to the action decision tree
        indexes = self.treeView.selectedIndexes()
        if len(indexes) > 0:
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1
        menu = pyqt.QMenu()
        if level == 0:
            menu.addAction(self.tr("Edit Node Options"))
        elif level == 1:
            menu.addAction(self.tr("Edit Workbook Options"))
        elif level == 2:
            menu.addAction(self.tr("Edit object"))
        menu.exec_(self.treeView.viewport().mapToGlobal(position))
        return self

    def onNodeSelection(self, fx, mod=None) -> None:
        """On selection of tree node load data for tabs in center widget"""
        event.on_clickleft_press(fx)
        return self

    def onNodeDeselection(self, fx, mod=None) -> None:
        """On deslection of tree node save any changes to node options"""
        event.on_clickleft_release(fx)
        return self

    def onEnter(self, fx, mod=None) -> None:
        """Need to build if a node was selected an enter create a new sibling
        node. shift-enter creates a new child node, ctrl-enter creates
        a new tab in the node"""
        event.on_enter_kp(fx, mod)
        return self

    def onDelete(self, fx, mod=None) -> None:
        """Launch Dialog to confirm deletion of node, which marks as deleted in database
        and is not removed until a database cleanup is run"""
        return self

    def set_current_node(self, node) -> None:
        """"""
        # node.set_expanded(True)
        self.parent.model.current_node = node
        self.parent.setCurrentItem(node)
        self.parent.scrollToItem(node)
        self.parent.setFocus()
        if "center" in self.parent.app.view.panes.keys():
            # self.parent.app.view.panes["center"].model.current_tab.save()
            node.updateTabs("center")
        # Save last selected node to instance for restoration on next launch
        self._save_last_node(node)
        return self

    def _save_last_node(self, node) -> None:
        """"""
        # try:
        #     # TODO: 0 must be fixed to be the correct value for the last node
        #     if hasattr(self.parent.app, "model") and self.parent.app.model:
        #         store = self.parent.app.model.store
        #         instance = self.parent.app.model.instance
        #         if store and instance:
        #             # Get the node's nid
        #             node_nid = getattr(node, "nid", None) or getattr(node, "data", {}).get("nid_txt", None)
        #             if node_nid:
        #                 # Update instance metadata with last node
        #                 if not hasattr(instance, "meta_data"):
        #                     instance.meta_data = {}
        #                 instance.meta_data["last_node_nid_txt"] = node_nid
        #                 # Store the updated instance
        #                 store.store_app_instance(instance, how="UPDATE")
        #                 logma.info(f"Saved last node: {node_nid}")
        # except Exception as e:
        #     logma.warning(f"Could not save last node: {e}")
        return self

    def set_node_widget(self, widget) -> None:
        """"""
        self.node_widget = widget
        return self

    def _set_background(self) -> None:
        """"""
        url = f"{here}../themes/_data_/images/Smile_a001.png"
        self.setStyleSheet("QTreeWidget {background-image: url(" + url + ");}")
        return self


# ===========================Code Source Examples================================||
"""
"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
