from typing import Any, Optional
'\n---\n<(META)>:\n        docid:\n        name:\n        description: >\n        version: 0.0.0.0.0.0\n        authority: filesystem\n        security: seclvl2\n        <(WT)>: -32\n'
from os.path import abspath, dirname, join
import datetime as dt
import json as j
import threading
from pandas import DataFrame
from kahndor import kahndor
from nchantrs.libraries import pyqt
from nchantrs.widgets.items.items import NchantdItem, NchantdTreeItem
from nchantrs.widgets.widgets import NchantdWidgetMixin
from kahndor.logma import Logma
here = join(dirname(__file__), '')
log = False
logma = Logma(__name__)
debug = False
if not log:
    logma.off()
pxcfg = join(abspath(here), '_data_/nodes.yaml')

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

    def __init__(self, parent, item, nid, node, children, df=DataFrame(), cfg=None) -> None:
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
        self.parent_widget = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdNode')
        if parent:
            self.config.override(parent.config)
        logma.info(f'Item {item}')
        self.name = item
        self.children_df = children
        self.item = item
        self.itemData = [item, nid]
        self.nid = nid
        self.node = node
        self.position = None

    def initModel(self) -> Any:
        """ """
        self.model.initModel()
        return self

    def initView(self) -> None:
        self.layout = pyqt.QVBoxLayout()
        self.setModel(self.parent.model)
        self.setLayout(self.layout)
        self.initUI()
        self.initContextMenu()
        self.initTriggers()

    def initWidget(self) -> Any:
        """ """
        self.initModel()
        self.initView()
        return self

    def addChildNode(self) -> Any:
        logma.info(f'addChildNode called')
        return self

    def addSibilingNode(self) -> Any:
        logma.info(f'addSibilingNode called')
        return self

    def deleteChildren(self, pid) -> Any:
        logma.info(f'deleteChildren called')
        return self

    def data(self, column) -> Optional[Any]:
        try:
            return self.itemData[column]
        except IndexError:
            return None

    def loadChildren(self, df) -> Any:
        """ """
        children = df[df['pid_txt'] == str(self.nid)]
        for index, child in children.iterrows():
            item = NchantdNode(self, child['name'], child['nid'], child, df[df['pid_txt'] == child['nid']])
            item.initWidget()
            item.loadChildren(df)
            item.hasChildren(child['nid'])
            self.appendRow(item)
        self.is_loaded = True
        return self

    def hasChildren(self, nid) -> Any:
        """ """
        self.is_expandable = True
        return self

    def initContextMenu(self) -> Any:
        """ """
        self.setContextMenuPolicy(pyqt.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.onRightClick)
        return self

    def initTriggers(self) -> Any:
        """ """
        self.doubleClicked.connect(self.onLeftDoubleClick)
        self.expanded.connect(self.onExpand)
        self.clicked.connect(self.onLeftClick)
        return self

    def initUI(self) -> Any:
        super().initUI()
        logma.info(f'initUI {{type(self).__name__}}')
        return self

    def onExpand(self) -> Any:
        logma.info(f'onExpand called')
        return self

    def onRightClick(self) -> None:
        logma.info(f'onRightClick called')
        return self

    def onLeftDoubleClick(self, signal) -> Any:
        return self

    def onLeftClick(self, signal) -> Any:
        return self

    def onMiddleClick(self) -> Any:
        logma.info(f'onMiddleClick called')
        return self

    def onSelection(self, fx, mod=None) -> None:
        """On selection of tree node load data for tabs in center widget"""
        event.on_clickleft_press(fx)
        return

    def onDeselection(self, fx, mod=None) -> None:
        """On deslection of tree node save any changes to node options"""
        event.on_clickleft_release(fx)
        return

    def onEnter(self, fx, mod=None) -> None:
        """Need to build if a node was selected an enter create a new sibling
        node. shift-enter creates a new child node, ctrl-enter creates
        a new tab in the node"""
        event.on_enter_kp(fx, mod)
        return

    def onDelete(self, fx, mod=None) -> None:
        logma.info(f'onDelete called')
        return self

    def update_position(self) -> None:
        logma.info(f'update_position called')
        return self

    def _set_font(self) -> None:
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

    def __init__(self, parent, name, nid, node, children=DataFrame(), cfg=None) -> None:
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
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdTreeNode').override(cfg))
        self.item = name
        self.name = node['name_txt']
        self.nid = nid
        self.itemData = [name, nid]
        self.node = node
        self.pid = self.node.get('pid_txt', '0')
        self.children_df = children
        try:
            self.parameters = j.loads(self.node['parameters_dict'].replace("'", '"'))
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

    def initModel(self, cfg=None) -> Any:
        """ """
        super().initModel(cfg)
        self.tab_focus = self.node.get('tabfocus_txt', 0)
        self.node_type = self.node['ntype_txt']
        self.expanded = self.node['expanded_bit']
        self.treeid = self.node['treeid_txt']
        self.readonly = self.node['readonly_bit']
        self.editable = self.node['editable_bit']
        self.visible = self.node['visible_bit']
        self.moveable = self.node['moveable_bit']
        self.pregnable = self.node['pregnable_bit']
        self.position = self.node['position_int']
        self.is_parent = self.node['isparent_bit']
        self.is_loaded = False
        self.tab_focus = self.node['tabfocus_int']
        logma.info('Name ' + self.node['name_txt'])
        self.setText(0, self.node['name_txt'], False)
        self._set_font()
        self._set_icon()
        self._set_font_color()
        self.app_data_type = self.node['app_data_type']
        self.set_data_focus()
        self.set_recent_tabs()
        self.setData(0, pyqt.Qt.UserRole, self.node)
        return self

    def initView(self, path=None) -> Any:
        """"""
        self.set_expanded(self.expanded)
        return self

    def initWidget(self) -> Any:
        """ """
        self.initModel()
        self.initView()
        return self

    def addChildNode(self) -> Any:
        logma.info(f'addChildNode called')
        return self

    def addSibilingNode(self) -> Any:
        logma.info(f'addSibilingNode called')
        return self

    def deleteChildren(self, pid) -> Any:
        logma.info(f'deleteChildren called')
        return self

    def hasChildren(self, nid) -> Any:
        """ """
        self.is_expandable = True
        return self

    def get_children(self) -> Any:
        """
        Get all child nodes of this tree item.
        """
        children = []
        for i in range(self.childCount()):
            child = self.child(i)
            if hasattr(child, 'nid'):
                children.append(child)
        return children

    def loadChildren(self, df) -> Any:
        """ """
        df.sort_values(by=['position_int', 'name_txt'], inplace=True)
        children = df[df['pid_txt'] == str(self.nid)]
        if self.expanded:
            self.place_holder = False
            for index, child in children.iterrows():
                item = self.treeWidget().view.node_widget(self, child['name_txt'], child['nid_txt'], child)
                item.initWidget()
                item.loadChildren(df)
                self.nodes.append(item)
                self.addChild(item)
        elif not children.empty:
            self.place_holder = True
            self.addChild(pyqt.QTreeWidgetItem(self, ['Loading...']))
        self.is_loaded = True
        return self

    def set_expanded(self, expand=True) -> Any:
        """"""
        self.setExpanded(expand)
        return self

    def set_data_focus(self) -> Any:
        """"""
        self.focus = self.parameters.get('focus', 'office')
        return self

    def set_recent_tabs(self) -> Any:
        """"""
        self.recent_center_tab = self.parameters.get('recent_tab', {}).get('center', {})
        self.recent_right_tab = self.parameters.get('recent_tab', {}).get('right', {})
        return self

    def setText(self, column, text, store=True) -> Any:
        """"""
        super().setText(column, text)
        return self

    def sort_by_criteria(self, criteria='name', order='ascending', update_db=True) -> Any:
        """
        Sort children by various criteria.

        Args:
            criteria: 'name', 'date_created', 'position', 'type'
            order: 'ascending' or 'descending'
            update_db: Whether to update database positions
        """
        children = self.get_children()
        sort_keys = {'name': lambda x: x.name.lower(), 'date_created': lambda x: getattr(x, 'date_created', ''), 'position': lambda x: getattr(x, 'position', 0), 'type': lambda x: getattr(x, 'node_type', ''), 'custom': lambda x: (x.node_type, x.name.lower())}
        if criteria not in sort_keys:
            raise ValueError(f'Invalid sort criteria: {criteria}')
        reverse_order = order == 'descending'
        children.sort(key=sort_keys[criteria], reverse=reverse_order)
        self._update_tree_ui(children)
        if update_db:
            self._batch_update_positions(children)
        return self

    def sortChildren(self, column=0, order='ascending', db='db', sort_key=None) -> Any:
        """
        Sort children of the tree node and update database positions efficiently.

        Args:
            column: Column to sort by (default: 0)
            order: Sort order - "ascending" or "descending"
            db: Database identifier
            sort_key: Custom sort function (optional)
        """
        if order == 'ascending':
            super().sortChildren(column, pyqt.Qt.SortOrder.AscendingOrder)
        else:
            super().sortChildren(column, pyqt.Qt.SortOrder.DescendingOrder)
        children = self.get_children()
        if not children:
            return self
        if sort_key:
            children.sort(key=sort_key, reverse=order == 'descending')
        else:
            children.sort(key=lambda x: x.item.lower(), reverse=order == 'descending')
        data = {'table': {'doc_tree_node': {'data': {}}}}
        for n, child in enumerate(children):
            data['table']['doc_tree_node']['data']['position_int'] = n
            self.parent.app.model.store.update_record(data, 'nid_txt', child.nid, db)
        return self

    def updateTabs(self, view='center') -> Any:
        """ """
        self.app.view.panes[view].clear()
        self.app.view.panes[view].model.buildTabSet(self, view)
        self.app.view.refresh_window_size()
        return self

    def _batch_update_positions(self, children, db='db') -> None:
        """
        Efficiently update positions in database using batch operations.
        """
        updates = []
        for position, child in enumerate(children):
            updates.append({'nid': child.nid, 'position': position, 'parent_id': self.nid})
        if hasattr(self.parent_widget.app.model.store, 'batch_update_positions'):
            self.parent_widget.app.model.store.batch_update_positions(updates, db)
        else:
            self._individual_updates_with_transaction(updates, db)

    def _individual_updates_with_transaction(self, updates, db) -> None:
        """
        Perform individual updates within a transaction for better performance.
        """
        try:
            if hasattr(self.parent_widget.app.model.store, 'begin_transaction'):
                self.parent_widget.app.model.store.begin_transaction(db)
            for update_data in updates:
                data = {'table': {'doc_tree_node': {'data': {'position': update_data['position']}}}}
                self.parent_widget.app.model.store.update_record(data, 'nid_txt', update_data['nid'], db)
            if hasattr(self.parent_widget.app.model.store, 'commit_transaction'):
                self.parent_widget.app.model.store.commit_transaction(db)
        except Exception as e:
            if hasattr(self.parent_widget.app.model.store, 'rollback_transaction'):
                self.parent_widget.app.model.store.rollback_transaction(db)
            raise e

    def _update_tree_ui(self, sorted_children) -> None:
        """Update the tree widget UI with sorted children."""
        for i in range(self.childCount()):
            self.removeChild(self.child(0))
        for child in sorted_children:
            self.addChild(child)

    def sort_with_lazy_loading(self) -> Any:
        """Sort considering lazy loading of children."""
        if not self.is_loaded:
            self.pending_sort = True
            return self
        return self.sortChildren()

    def debounced_sort(self, delay=0.5) -> None:
        """Debounce sort operations to avoid excessive database updates."""
        if hasattr(self, '_sort_timer'):
            self._sort_timer.cancel()
        self._sort_timer = threading.Timer(delay, self._perform_sort)
        self._sort_timer.start()

    def _perform_sort(self) -> None:
        """Actually perform the sort operation."""
        self.sortChildren()

    def _set_font(self) -> Any:
        """"""
        font = self.font(0)
        node_types = self.config.dikt['node_types']
        if self.node_type not in node_types:
            raise Exception(f'Unknown node type {self.node_type}')
        node_type = node_types[self.node_type]
        if not node_type.get('font', None):
            node_type['font'] = 12
        font.setPointSize(node_type['font'])
        self.setFont(0, font)
        return self

    def _set_font_color(self) -> Any:
        """"""
        node_types = self.config.dikt['node_types']
        if self.node_type not in node_types:
            raise Exception(f'Unknown node type {self.node_type}')
        node_type = node_types[self.node_type]
        logma.info(f"Set Font Color: {self.app.view.theme.colors[node_type['color']]}")
        self.setForeground(0, pyqt.QBrush(pyqt.QColor(self.app.view.theme.colors[node_type['color']])))
        if self.node['ntype_txt'] == 'displaynode':
            logma.info(f"NType {self.node['ntype_txt']}")
            logma.info(f"Node {self.node['name_txt']}")
            if self.node['name_txt'] == 'Action':
                self.setForeground(0, pyqt.QColor('#B71F1F'))
            elif self.node['name_txt'] == 'Fund':
                self.setForeground(0, pyqt.QColor('#19C26B'))
            elif self.node['name_txt'] == 'Vision':
                self.setForeground(0, pyqt.QColor('#F6FF00'))
            elif self.node['name_txt'] == 'Social':
                self.setForeground(0, pyqt.QColor('#D97BCB'))
            elif self.node['name_txt'] == 'Mech':
                self.setForeground(0, pyqt.QColor('#191CC2'))
            elif self.node['name_txt'] == 'Anal':
                self.setForeground(0, pyqt.QColor('#F77F05'))
            elif self.node['name_txt'] == 'Settings':
                self.setForeground(0, pyqt.QColor('#4F5665'))
            elif self.node['name_txt'] == 'Journal':
                self.setForeground(0, pyqt.QColor('#4F5665'))
            else:
                self.setForeground(0, pyqt.QColor('#5F5FDF'))
        return self

    def _set_icon(self, icon_type='accent') -> Any:
        """
        #need to get the correct icon based on the parameters focus

        :param icon_type:
        :return:
        """
        icon_cfg = self.config.dikt['node_types']
        try:
            icon = icon_cfg[self.node_type]['icon']
        except KeyError:
            raise Exception(f'Unknown node type {self.node_type}')
        logma.info(f'App Model {self.app.model}')
        self.setIcon(0, pyqt.QIcon(self.app.view.theme.get_icon_path(icon, icon_type)))
        return self

class NchantdCanvasNodeMixin(NchantdWidgetMixin):
    """"""

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def launch_update_sigil(self) -> None:
        logma.info(f'launch_update_sigil called')
        return self

class NchantdRectangleNode(NchantdCanvasNodeMixin, pyqt.QGraphicsRectItem):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('Nchantd')
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        self.setBrush(pyqt.QBrush(pyqt.QColor(100, 100, 250, 100)))
        self.setPen(pyqt.QPen(pyqt.Qt.black, 2))
        self.text_item = pyqt.QGraphicsTextItem(self.config.dikt['text'], self)
        self.text_item.setDefaultTextColor(pyqt.Qt.black)
        self.text_item.setPos(self.rect().center() - self.text_item.boundingRect().center())
        self.setFlags(pyqt.QGraphicsItem.ItemIsSelectable | pyqt.QGraphicsItem.ItemIsMovable)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdEllipseNode(NchantdCanvasNodeMixin, pyqt.QGraphicsEllipseItem):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('Nchantd')
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdCircleNode(NchantdEllipseNode):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdCircleItem')
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdLineNode(NchantdCanvasNodeMixin, pyqt.QGraphicsLineItem):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdLineItem')
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdLineArrowNode(NchantdLineNode):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdLineNode')
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdLineDoubleArrowNode(NchantdLineArrowNode):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdLineNode')
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdImageNode(NchantdCanvasNodeMixin, pyqt.QGraphicsPixmapItem):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdImageItem')
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdTextNode(NchantdCanvasNodeMixin, pyqt.QGraphicsTextItem):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdTextItem')
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdIrregularShapeNode(NchantdCanvasNodeMixin, pyqt.QGraphicsPathItem):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdIrregularShapeItem')
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdPolygonNode(NchantdCanvasNodeMixin, pyqt.QGraphicsPolygonItem):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdPolygonItem')
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdTriangleNode(NchantdPolygonNode):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('Nchantd')
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self