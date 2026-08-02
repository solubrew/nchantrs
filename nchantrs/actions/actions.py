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
from os.path import abspath, dirname, join
import datetime as dt
import logging
logger = logging.getLogger(__name__)
from kahndor import kahndor
from typing import Optional, Dict, List, Any, Tuple
from kahndor.logma import Logma
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
pxcfg = join(here, '_data_', '.yaml')

class ActionBuilder:

    def __init__(self, cfg=None) -> None:
        self.config = cfg

    def buildAction(self, cfg) -> None:
        """Dynamically build action to be triggered from menu item"""
        icon = pyqt.QIcon(cfg['icon_txt'])
        kwargs = {}
        if 'shortcut_txt' in cfg.keys() and cfg['shortcut_txt'] != None:
            kwargs['shortcut'] = cfg['shortcut_txt']
        if 'tip_txt' in cfg.keys() and cfg['tip_txt'] != None:
            kwargs['statusTip'] = cfg['tip_txt']
        if 'fx_txt' in cfg.keys() and cfg['fx_txt'] != None and (cfg['fx_txt'] not in ['']):
            if log:
                logma.info(f"Function {cfg['fx_txt']}")
            try:
                kwargs['triggered'] = thingify(cfg['fx_txt'])
            except Exception as e:
                kwargs['triggered'] = None
        return pyqt.QAction(icon, cfg['name_txt'], self.parent, **kwargs)

    def load_scheme(self, filename) -> None:
        """
        Load a scheme from a file (`filename`) into the current
        document, updates the recent scheme list and the loaded scheme path
        property.
        """
        new_scheme = self.new_scheme_from(filename)
        if new_scheme is not None:
            self.set_new_scheme(new_scheme)
            scheme_doc_widget = self.current_document()
            scheme_doc_widget.setPath(filename)
            self.add_recent_scheme(new_scheme.title, filename)
            if not self.freeze_action.isChecked():
                scheme_doc_widget.activateDefaultWindowGroup()

    def load_scheme_xml(self, xml) -> None:
        new_scheme = widgetsscheme.WidgetsScheme(parent=self)
        scheme_load(new_scheme, StringIO(xml))
        self.set_new_scheme(new_scheme)
        return QDialog.Accepted

    def create_new_window(self) -> None:
        """Create a new top level CanvasMainWindow instance.
        The window is positioned slightly offset to the originating window
        (`self`).
        Note
        ----
        The window has `Qt.WA_DeleteOnClose` flag set. If this flag is unset
        it is the callers responsibility to explicitly delete the widget (via
        `deleteLater` or `sip.delete`).
        Returns
        -------
        window: CanvasMainWindow"""
        window = CanvasMainWindow()
        window.setAttribute(Qt.WA_DeleteOnClose)
        window.setGeometry(self.geometry().translated(20, 20))
        window.setStyleSheet(self.styleSheet())
        window.set_widget_registry(self.widget_registry)
        window.restoreState(self.saveState(self.SETTINGS_VERSION), self.SETTINGS_VERSION)
        window.set_tool_dock_expanded(self.dock_widget.expanded())
        window.set_float_widgets_on_top_enabled(self.float_widgets_on_top_action.isChecked())
        logview = window.log_view()
        te = logview.findChild(QPlainTextEdit)
        doc = self.log_view().findChild(QPlainTextEdit).document()
        doc = doc.clone(parent=te)
        doc.setDocumentLayout(QPlainTextDocumentLayout(doc))
        te.setDocument(doc)
        stdout, stderr = (sys.stdout, sys.stderr)
        if isinstance(stdout, TextStream):
            stdout.stream.connect(logview.write)
        if isinstance(stderr, TextStream):
            err_formater = logview.formated(color=Qt.red)
            stderr.stream.connect(err_formater.write)
        CanvasMainWindow._instances.append(window)
        window.destroyed.connect(lambda: CanvasMainWindow._instances.remove(window))
        return window

def about(app, cfg) -> None:
    """Launch dialog with information about application"""
    launch = NchantdDialog(app, cfg).initWidget()
    return

def add_tab(app, cfg) -> None:
    """"""
    app.model.add_tab()
    return

def mngBookmarks(self) -> None:
    logma.info(f'mngBookmarks called')
    return self

def admin() -> None:
    logma.info(f'admin called')
    return self

def close(app) -> None:
    logma.info(f'close called')
    return self

def exit(app, ce) -> None:
    """ """
    app.fileQuit()

def file() -> None:
    logma.info(f'file called')
    return self

def help() -> None:
    logma.info(f'help called')
    return self

def insert() -> None:
    logma.info(f'insert called')
    return self

def newFile(path) -> None:
    logma.info(f'newFile called')
    return self

def newRecord() -> None:
    logma.info(f'newRecord called')
    return self

def open(path) -> None:
    logma.info(f'open called')
    return self

def paste(app) -> None:
    logma.info(f'paste called')
    return self

def preferences(app, cfg: dict={}) -> None:
    logma.info(f'preferences called')
    return self

def redo() -> None:
    logma.info(f'redo called')
    return self

def save() -> None:
    logma.info(f'save called')
    return self

def saveall() -> None:
    logma.info(f'saveall called')
    return self

def saveas(path, data) -> None:
    logma.info(f'saveas called')
    return self

def savecopy() -> None:
    logma.info(f'savecopy called')
    return self

def undo() -> None:
    logma.info(f'undo called')
    return self

def aboutApplication(self) -> None:
    """"""
    text = 'For Help Contact: Joe Brewer at joebrewer@solutionsbrewer.com'
    return text

def addBookmark(self) -> None:
    """"""
    linenumber = self.getLineNumber()
    linetext = self.editor.textCursor().block().text().strip()
    self.bookmarks.addItem(linetext, linenumber)
    return self

def bookmarks(self) -> None:
    logma.info(f'bookmarks called')
    return self

def closeEvent(self, ce) -> None:
    self.fileQuit()

def copySelection(self) -> None:
    logma.info(f'copySelection called')
    return self

def createTabDocument(self) -> None:
    logma.info(f'createTabDocument called')
    return self

def cutSelection(self) -> None:
    logma.info(f'cutSelection called')
    return self

def exitAccess(self) -> None:
    logma.info(f'exitAccess called')
    return self

def exitCherryTree(self) -> None:
    logma.info(f'exitCherryTree called')
    return self

def exitCSV(self) -> None:
    logma.info(f'exitCSV called')
    return self

def exitExcel(self) -> None:
    logma.info(f'exitExcel called')
    return self

def exitGui(self) -> None:
    logma.info(f'exitGui called')
    return self

def expCSV(self) -> None:
    logma.info(f'expCSV called')
    return self

def fileQuit(self) -> None:
    self.close()

def findData(self) -> None:
    logma.info(f'findData called')
    return self

def linkData(self) -> None:
    logma.info(f'linkData called')
    return self

def loadData(self) -> None:
    logma.info(f'loadData called')
    return self

def loadDevMode(self) -> None:
    logma.info(f'loadDevMode called')
    return self

def newFile(self) -> None:
    """"""
    self.newAct = QAction('&New', self, shortcut=QKeySequence.New, statusTip='new file', triggered=self.newFile)
    self.newAct.setIcon(QIcon.fromTheme(self.root + '/icons/new24'))
    if self.maybeSave():
        self.editor.clear()
        self.editor.setPlainText(self.mainText)
        self.filename = ''
        self.setModified(False)
        self.editor.moveCursor(self.cursor.End)
        self.statusBar().showMessage('new File created.')
        self.editor.setFocus()
        self.bookmarks.clear()
        self.setWindowTitle('new File[*]')
    return self

def new_workflow_window(self) -> None:
    """Create and show a new CanvasMainWindow instance."""
    newwindow = self.create_new_window()
    newwindow.raise_()
    newwindow.show()
    newwindow.activateWindow()
    settings = QSettings()
    show = settings.value('schemeinfo/show-at-new-scheme', True, type=bool)
    if show:
        newwindow.show_scheme_properties()

def newAppContainer(self, cfgs=None) -> None:
    """"""
    self.nodes.append(appContainer, cfgs)
    return self

def newCanvas(self) -> None:
    """"""
    self.nodes.append(canvasContainer, cfgs)
    return self

def newChart(self) -> None:
    """"""
    self.nodes.append(chartContainer, cfgs)
    return self

def newDashboard(self) -> None:
    """"""
    self.nodes.append(dashContainer, cfgs)
    return self

def newEditor(self) -> None:
    """"""
    self.nodes.append(editorContainer, cfgs)
    return self

def newSheet(self) -> None:
    """"""
    self.nodes.append(sheetContainer, cfgs)
    return self