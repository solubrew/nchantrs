# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""#																			||
---  #																			||
<(META)>:  #																	||
        docid:   #																	||
        name:	#																	||
        description: >  #															||
                Develop Qt5TreeModel module and leverage it instead of adhoc
                building it here  #			||
        expirary: <[expiration]>  #													||
        version: <[version]>  #														||
        path: <[LEXIvrs]>  #														||
        outline: <[outline]>  #														||
        authority: document|this  #													||
        security: sec|lvl2  #														||
        <(WT)>: -32  #																||
"""  # ||

# -*- coding: utf-8 -*-#														||
# ===============================Core Modules====================================||
from os.path import abspath, dirname, join, expanduser
from pathlib import Path

import logging

logger = logging.getLogger(__name__)
# ===============================================================================||
from kahndor import kahndor
from nchantrs.libraries import pyqt
from nchantrs.views.treeviews import NchantdTreeView  # , NchantdTimeTreeView
from nchantrs.models.treemodels import NchantdApplicationTreeModel, NchantdTreeModel, NchantdTimeTreeModel
from nchantrs.widgets.widgets import NchantdWidgetMixin
from kahndor.logma import Logma

# ===============================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)
# logma.off()

# ===============================================================================||
pxcfg = join(here, "_data_", "trees.yaml")


class NchantdTree(NchantdWidgetMixin, pyqt.QTreeWidget):
    """
    :class: NchantdTree(pyqt.QTreeWidget)

    The NchantdTree class is a subclass of pyqt.QTreeWidget. It is used to create a simple tree view widget.

    Parameters:
        - parent (QWidget): The parent widget for the NchantdTree. Default is None.
        - cfg (dict): The configuration settings for the NchantdTree. Default is an empty dictionary.
        - root: The root item for the tree. Default is None.

    Attributes:
        - parent_widget: The parent widget of the NchantdTree.
        - config: The configuration settings for the NchantdTree.
        - new_instance: The function to create a new instance of the parent widget.
        - model: The NchantdTreeModel object associated with the NchantdTree.
        - view: The NchantdTreeView object associated with the NchantdTree.
        - nodes: The list of tree nodes in the NchantdTree.
        - clipboard_state: Clipboard for cut/copy/paste operations.

    Methods:
        - __init__(self, parent=None, cfg={}, root=None): Initializes the NchantdTree object.
        - initModel(self): Initializes the model for the NchantdTree.
        - initView(self): Initializes the view for the NchantdTree.
        - initWidget(self, pos=None): Initializes the NchantdTree widget.
        - init_context_menu(self): Initialize context menu for the tree.
        - show_context_menu(position): Display context menu at position.
        - get_context_menu_items(node_type): Get menu items for node type.
        - execute_context_action(action): Execute a context menu action.
        - get_selected_item(self): Get currently selected item.
        - get_clipboard(self): Get clipboard state.
        - set_clipboard(node, mode): Set clipboard for cut/copy.

    Example Usage:
        tree = NchantdTree()
        tree.initWidget()
    """

    def __init__(self, parent=None, cfg={}, root=None):
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdTree").override(cfg)
        self.init_variables()
        super().__init__()
        self.model = NchantdTreeModel(self, root)
        self.view = NchantdTreeView(self, self.config)
        self.setDragEnabled(True)  # Enable dragging
        self.setAcceptDrops(True)  # Allow drops
        self.setDropIndicatorShown(True)  # Show where drops will occur
        self.nodes = []
        self.expansion_state = {}
        # Clipboard state for cut/copy/paste/duplicate
        self.clipboard_state = {"nodes": [], "mode": None}
        # Context menu initialization
        self.context_menu = None
        self.initialize_context_menu()

    def initModel(self):
        """ """
        super().initModel()
        self.model.initModel()
        return self

    def initView(self):
        """ """
        self.view.initView()
        # Adjust header size policy to allow horizontal scrolling
        header = self.header()
        header.setSectionResizeMode(pyqt.QHeaderView.ResizeToContents)  # Auto resize to fit content
        header.setStretchLastSection(False)  # Prevent stretching the last column
        # Enable horizontal scroll
        # self.setHorizontalScrollBarPolicy(pyqt.Qt.ScrollBarAsNeeded)
        self.setAutoScroll(False)
        return self

    def initWidget(self, pos=None, initialize_database_objects=True):
        """ """
        self.initModel()
        self.initView()
        return self

    def closeEvent(self, event):
        """Handle window close event to save the tree state."""
        self.save_tree_expansion_state()
        super().closeEvent(event)

    def dragEnterEvent(self, event):
        """Handle drag enter event with validation."""
        if event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        """Allow drag move inside the tree with visual feedback."""
        item = self.itemAt(event.pos())
        
        # Validate drop target
        if item and hasattr(item, "moveable") and not item.moveable:
            event.ignore()
            return
        
        # Accept the drop if we have a valid target
        if item:
            event.acceptProposedAction()
        else:
            # Allow drops on empty tree area (becomes root-level)
            event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        """Handle drag leave event for cleanup."""
        event.accept()

    def dropEvent(self, event):
        """Handle the drop event to reparent dragged nodes with position awareness.
        
        Drop behavior:
        - On folder/expandable node: becomes child
        - Above item (top half): becomes previous sibling
        - Below item (bottom half): becomes next sibling
        """
        dragged_item = self.currentItem()
        target_item = self.itemAt(event.pos())
        
        logma.info(f"Dragged Item: {dragged_item}")
        logma.info(f"Target Item: {target_item}")
        logma.info(f"Drop Position: {event.pos()}")
        
        # Validate dragged item can be moved
        if not dragged_item:
            event.ignore()
            return
        
        if hasattr(dragged_item, "moveable") and not dragged_item.moveable:
            logma.info("Item is not moveable")
            event.ignore()
            return
        
        # Prevent dropping item onto itself or its descendants
        if target_item:
            if target_item == dragged_item:
                event.ignore()
                return
            if self._is_descendant(dragged_item, target_item):
                logma.info("Cannot drop item onto its own descendant")
                event.ignore()
                return
        
        # Determine drop position relative to target
        drop_mode = self._determine_drop_mode(target_item, event.pos())
        
        if target_item:
            # Get the visual rect of the target item
            target_rect = self.visualItemRect(target_item)
            relative_y = event.pos().y() - target_rect.top()
            item_height = target_rect.height()
            
            # Determine drop behavior based on position
            if item_height > 0:
                relative_position = relative_y / item_height
            else:
                relative_position = 0.5
        else:
            # Dropped on empty area - becomes root-level item
            drop_mode = "root"
        
        # Perform the appropriate move operation
        if drop_mode == "child":
            self._drop_as_child(dragged_item, target_item)
        elif drop_mode == "sibling_before":
            self._drop_as_sibling(dragged_item, target_item, before=True)
        elif drop_mode == "sibling_after":
            self._drop_as_sibling(dragged_item, target_item, before=False)
        elif drop_mode == "root":
            self._drop_as_root(dragged_item)

        # We performed the move ourselves. Neutralize the drop action so Qt's own
        # drag machinery does not ALSO remove a "source" row afterwards: our manual
        # re-parenting has already shifted the rows, so the row at the dragged
        # item's original index is now the drop target, and a MoveAction here would
        # make Qt delete it (the underlying node disappears).
        event.setDropAction(pyqt.Qt.IgnoreAction)
        event.accept()
        self.viewport().update()

    def _is_descendant(self, potential_parent, potential_child):
        """Check if potential_child is a descendant of potential_parent."""
        current = self._item_parent(potential_child)
        while current:
            if current == potential_parent:
                return True
            current = self._item_parent(current)
        return False

    @staticmethod
    def _item_parent(item):
        """Return an item's parent QTreeWidgetItem.

        Tree items store the owning tree widget on self.parent, which shadows
        QTreeWidgetItem.parent(); call the base method explicitly so we walk the
        actual item hierarchy instead of trying to call the tree widget.
        """
        return pyqt.QTreeWidgetItem.parent(item)

    def _child_nodes(self, container):
        """Return a container's child items in UI order. container may be a node
        item or None, in which case the invisible root (top level) is used."""
        if container is None:
            container = self.invisibleRootItem()
        return [container.child(i) for i in range(container.childCount())]

    def _renormalize(self, container):
        """Renumber a container's children to sequential, gap-free positions in
        the store, matching their current UI order."""
        nodes = self._child_nodes(container)
        if nodes:
            self.model.renormalize_positions(nodes)

    def _determine_drop_mode(self, target_item, pos):
        """Determine the drop mode based on target item and position.
        
        Returns:
            'child': Drop onto target as child
            'sibling_before': Drop before target as sibling
            'sibling_after': Drop after target as sibling
            'root': Drop as root-level item
        """
        if not target_item:
            return "root"
        
        # Check if target can accept children
        if hasattr(target_item, "pregnable") and target_item.pregnable:
            # Check if dropped in the upper portion of the item
            target_rect = self.visualItemRect(target_item)
            relative_y = pos.y() - target_rect.top()
            item_height = target_rect.height()
            
            if item_height > 0:
                relative_position = relative_y / item_height
            else:
                relative_position = 0.5
            
            # Upper 25% = become first child, Middle = sibling, Lower 25% = become last child
            if relative_position < 0.25:
                return "sibling_before"  # Top edge - become sibling before
            elif relative_position > 0.75:
                return "child"  # Bottom edge - become child (last)
            else:
                return "sibling_before"  # Middle - become sibling before
        
        return "sibling_before"

    def _drop_as_child(self, dragged_item, new_parent):
        """Move dragged_item to become the last child of new_parent."""
        logma.info(f"Dropping {dragged_item.name} as child of {new_parent.name}")
        
        # Remove from current parent
        old_parent = self._item_parent(dragged_item)
        if old_parent:
            old_parent.removeChild(dragged_item)
        else:
            self.invisibleRootItem().removeChild(dragged_item)

        # Add to new parent
        new_parent.addChild(dragged_item)
        new_parent.setExpanded(True)

        # Update database - reparent, then renormalize sibling positions in both
        # the destination and the source container (to close the vacated gap).
        self.model.swap_parent(dragged_item, new_parent)
        self._renormalize(new_parent)
        self._renormalize(old_parent)

        logma.info(f"Successfully moved {dragged_item.name} as child of {new_parent.name}")

    def _drop_as_sibling(self, dragged_item, target_item, before=True):
        """Move dragged_item to become a sibling of target_item."""
        logma.info(f"Dropping {dragged_item.name} as sibling of {target_item.name} (before={before})")
        
        parent = self._item_parent(target_item)
        if not parent:
            parent = self.invisibleRootItem()

        # Remove from current parent FIRST, so the target index is computed
        # against the post-removal layout. Computing it beforehand overshoots by
        # one whenever the dragged item preceded the target under the same parent
        # (removeChild shifts every later sibling, including the target, down one).
        old_parent = self._item_parent(dragged_item)
        if old_parent:
            old_parent.removeChild(dragged_item)
        else:
            self.invisibleRootItem().removeChild(dragged_item)

        # Calculate target index against the current (post-removal) children
        target_index = parent.indexOfChild(target_item)
        if not before:
            target_index += 1

        # Insert at new position
        parent.insertChild(target_index, dragged_item)

        # Update database - reparent, then renormalize sibling positions in both
        # the destination and the source container (to close the vacated gap).
        self.model.move_sibling(dragged_item, parent)
        self._renormalize(parent)
        self._renormalize(old_parent)

        logma.info(f"Successfully moved {dragged_item.name} as sibling")

    def _drop_as_root(self, dragged_item):
        """Move dragged_item to become a root-level item."""
        logma.info(f"Dropping {dragged_item.name} as root-level item")
        
        # Remove from current parent
        old_parent = self._item_parent(dragged_item)
        if old_parent:
            old_parent.removeChild(dragged_item)
        else:
            self.invisibleRootItem().removeChild(dragged_item)

        # Add as root-level item at the end
        root = self.invisibleRootItem()
        root.addChild(dragged_item)

        # Update database - set as root (pid = '0'), then renormalize positions
        # at root and in the source container (to close the vacated gap).
        self.model.move_to_root(dragged_item)
        self._renormalize(root)
        self._renormalize(old_parent)

        logma.info(f"Successfully moved {dragged_item.name} to root level")

    def goto_node(self, node):
        """"""
        self.view.set_current_node(node)
        return self

    def refresh(self):
        """"""
        h_scroll = self.horizontalScrollBar().value()
        # self.cached_splitter_size = self.app.view.splitter.sizes()
        self.view.init_tree()
        self.horizontalScrollBar().setValue(h_scroll)
        # self.app.view.splitter.setSizes(self.cached_splitter_size)
        return self

    def reset_expansion_state(self):
        """Reset the saved expansion state to the tree."""
        if not self.expansion_state:
            return
        self._reset_tree_state(self.invisibleRootItem())
        return self

    def save_expansion_state(self):
        """Save the expansion state of the tree."""
        self.expansion_state = {}
        self._save_tree_state(self.invisibleRootItem())
        return self

    def scrollTo(self, index, hint=None):
        # Store current horizontal scroll position
        h_scroll = self.horizontalScrollBar().value()
        # Call parent scrollTo (this will handle vertical scrolling)
        super().scrollTo(index, hint)
        # Restore horizontal scroll position
        self.horizontalScrollBar().setValue(h_scroll)
        return self

    def sort_tree(self, column=0):
        """Sort the tree items based on the specified column."""
        self.model.sort(column)

    def sort_children(self, pid, column=0):
        """"""

    def _reset_tree_state(self, item):
        """Recursive helper to reset state of each item."""
        for i in range(item.childCount()):
            child = item.child(i)
            if id(child) in self.expansion_state:
                child.setExpanded(self.expansion_state[id(child)])
            self._reset_tree_state(child)
        return self

    def _save_tree_state(self, item):
        """Recursive helper to save state of each item."""
        for i in range(item.childCount()):
            child = item.child(i)
            self.expansion_state[id(child)] = child.isExpanded()
            self._save_tree_state(child)
        return self


class NchantdGroupTree(NchantdTree):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("Nchantd")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)

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


class NchantdApplicationTree(NchantdTree):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdApplicationTree"))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.model = NchantdApplicationTreeModel(self, None, self.config)
        self.note = None

    def initModel(self):
        """"""
        super().initModel()

        return self

    def initView(self):
        """"""
        super().initView()
        return self

    def initWidget(self, pos=None, initialize_database_objects=True):
        """"""
        self.initModel()
        self.initView()
        return self

    def on_node_changed(self):
        """"""
        # if self.model.current_tab_has_changed is True:
        #     self.model.save_tab()  # store the current tab data to the database
        return self

    def __getstate__(self):
        """"""
        state = self.__dict__.copy()
        # Remove the unpicklable entries.
        if state.get("unpickable_attribute", False):
            del state["unpicklable_attribute"]
        return state

    def __setstate__(self, state):
        """"""


class NchantdFileSystem(pyqt.QTreeWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent)
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdFileSystem")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.file_system_toolbar = None
        self.root_path = None
        self.root_dir = None
        self.current_level_files = []
        self.current_level_directories = []
        self.current_level_path = None
        self.setColumnCount(1)
        self.setHeaderLabel("File System")
        self.setSortingEnabled(True)

    def initModel(self):
        """"""
        # super().initModel()
        logma.info(f"Root Path: {self.config.dikt.get('root', None)}")
        self.set_root(self.config.dikt.get("root", None))
        # Add the root item
        # self.add_root_item()
        # self.context_menu = self.parent.context_menu
        return self

    def initView(self):
        """"""
        # super().initView()#causes some looping issues
        # Initial population of the directory structure
        self.itemExpanded.connect(self.on_item_expanded)  # Connect to the itemExpanded signal
        self.itemPressed.connect(self.on_item_expanded)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    def build_tree(self):
        """
        Build the entire tree structure from the root directory.
        """
        self.clear()  # Clear the tree before rebuilding

        # Add the root folder to the tree
        root_item = pyqt.QTreeWidgetItem(self, [str(self.root_dir)])
        root_item.setExpanded(True)  # Expand the root node
        self.add_top_level_items(self.root_dir, root_item)

    def add_root_item(self):
        """
        Add the root directory node and lazily load its children.
        """
        self.clear()
        logma.info(f"Root Dir: {self.root_dir}")
        root_item = pyqt.QTreeWidgetItem(self, [str(self.root_dir)])
        root_item.setData(0, pyqt.Qt.UserRole, self.root_dir)  # Store the path data
        root_item.setChildIndicatorPolicy(pyqt.QTreeWidgetItem.ShowIndicator)  # Show "+" for expandable
        self.addTopLevelItem(root_item)

    def add_top_level_items(self, path, parent_item):
        """
        Recursively add items to the tree structure.
        :param path: Current directory path.
        :param parent_item: The parent tree widget item to which child items will be added.
        """
        try:
            for item in sorted(path.iterdir(), key=lambda x: x.name):  # Iterate through files and directories
                if item.is_dir():  # If the item is a directory, recursively add its children
                    tree_item = pyqt.QTreeWidgetItem(parent_item, [item.name])
                    self.add_top_level_items(item, tree_item)
        except PermissionError:  # Handle directories the user does not have permission to access
            pass

    def get_children(self, tree_item, location="local"):
        """"""
        if location == "local":
            directory = tree_item.data(0, pyqt.Qt.UserRole)
            for child in sorted(directory.iterdir()):
                yield child
        elif location == "google_drive":
            self.get_children_google_drive()
        elif location == "dropbox":
            self.get_children_dropbox()
        else:
            pass

    def get_current_level_files(self):
        """"""
        logma.info(f"Current Level Files: {self.current_level_files}")
        return self.current_level_files

    def get_current_level_directories(self):
        """"""
        logma.info(f"Current Level Files: {self.current_level_directories}")
        return self.current_level_directories

    def lazy_load_children(self, tree_item):
        """
        Load and append the children of the given directory item.
        :param tree_item: The QTreeWidgetItem representing a directory.
        """
        logma.inspect_caller()
        self.current_level_files = []
        self.current_level_directories = []
        directory = tree_item.data(0, pyqt.Qt.UserRole)  # Get the directory path stored in the item's data
        # TODO implement read depth to allow for flattening files
        logma.info(f"Directory {directory}")
        if directory is None:
            return
        if not directory.is_dir():  # Ensure it's a directory
            self.current_level_files.append(tree_item)
            self.current_level_path = directory.parent
            return
        self.current_level_path = directory
        # Clear any existing placeholder children
        tree_item.takeChildren()
        logma.info(f"Current Level Files: {self.current_level_files}")
        try:
            for child in sorted(directory.iterdir(), key=lambda x: x.name):
                if child.is_dir():
                    child_item = pyqt.QTreeWidgetItem(tree_item, [child.name])
                    child_item.setData(0, pyqt.Qt.UserRole, child)  # Store path data in the item
                    # For directories, add a placeholder child to make them expandable
                    child_item.setChildIndicatorPolicy(pyqt.QTreeWidgetItem.ShowIndicator)
                    self.current_level_directories.append(child)
                else:
                    # logma.info(f"Item {tree_item}")
                    self.current_level_files.append(child)
        except PermissionError:
            logma.info("Skip directories we don't have permission to access")
        logma.info(f"Current Level Files: {self.current_level_files}")
        logma.info(f"Current Level Path: {self.current_level_path}")
        return self

    def on_item_expanded(self, item):
        """
        Handle the expansion of an item to lazily load its children.
        :param item: The QTreeWidgetItem that was expanded.
        """
        # if item.childCount() == 0:  # Only load children if none are already loaded
        self.lazy_load_children(item)
        logma.info(f"Current Level Files: {self.current_level_files}")
        # else:
        #    pass
        # need to fill out file list
        return self

    def set_root(self, path=None):
        """"""
        self.root_path = path
        if self.root_path is None:
            self.root_path = expanduser("~")
        self.current_level_path = self.root_path
        self.root_dir = Path(self.root_path)
        # self.build_tree()
        self.add_root_item()
        return self

    def sync_filesystem(self):
        """
        Synchronize the tree with the current state of the filesystem.
        """
        self.build_tree()


# ===========================Code Source Examples================================||
"""
"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
