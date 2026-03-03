# @@@@@@@@@@@@@@@@ Nchantrs.Utils @@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
    docid: <^(UUID)^>
    name: Nchantrs Utils Python Execution Document
    description: >
    expirary: <[expiration]>
    version: <[version]>
    path: <[LEXIvrs]>
    outline: <[outline]>
    authority: document|this
    security: sec|lvl2
    <(WT)>: -32
"""
# -*- coding: utf-8 -*-
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, exists, join

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from nchantrs.libraries import pyqt
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  #                                                 ||
logma = Logma(__name__)
# logma.off()
debug = True

# ====================================================================================================================||
pxcfg = join(here, "_data_", "utils.yaml")


def convert_df_to_tree(df, pid="0", root=None):
    """"""
    if root is None:
        root = {}
    if df.empty:
        return root
    pdf = df[df["pid_txt"] == pid]
    if not pdf.empty:
        dikt = pdf.to_dict("records")
        for row in dikt:
            if row["name_txt"] != "":
                logma.info(f"Row {row['name_txt']}")
                root[row["name_txt"]] = convert_df_to_tree(df, row["UUID"])
    return root


def get_dialog(parent, dialog_name):
    """"""
    parent.dialogs[dialog_name] = lookup_dialog(dialog_name)


def lookup(app, action, cfg=None, deep=False, refresh=False, debug=True):
    """Lookup action with in the action configurations system"""
    pxcfg = condor.Instruct(join(here, "../actions", "_data_", "actions.yaml")).override(cfg).dikt
    if not hasattr(app, "model"):
        return None
    cfg = next(app.model.store.docs["dbc"].read("app_actions"))
    # logma.info(f"CFG {cfg}")
    if cfg is None or refresh:
        logma.info("Retrieve Actions from Database")
        table = "app_action"
        params = {"table": table}
        db_cfg = {"WHERE": {"EQUAL": {"code_group_txt": pxcfg["action_type"]}}}
        # logma.info(f"DB Config {app.model.store.docs['db'].dbase}")
        actions = next(app.model.store.docs["db"].read(params, db_cfg))
        # logma.info(f"Retrieved Actions {actions.dikt[table]['df']}")
        cfg = actions.dikt[table]["df"].to_dict("records")
        cfg = {c["lookup_code_txt"]: c for c in cfg}
        # logma.info(f"Lookups {cfg}")
        app.model.store.docs["dbc"].write({"app_actions": cfg})
    if cfg is None or cfg == {}:
        # logma.warning(f"Action Lookup Config is Empty {cfg}")
        if debug:
            raise Exception(f"Action Lookup Config is Empty {cfg}")
        return {}
    # logma.info(f"Lookups {cfg.keys()}")
    return search(action, cfg, deep, debug=debug)


def search(action, gcfg, deep=False, debug=True) -> dict:
    """Search dictionary for action recursively moving through tree levels"""
    # logma.info(f"Action {action}")
    if not isinstance(action, dict):
        if gcfg.get(action.lower(), None):
            # logma.info(f"Action Found: {action}")
            return gcfg[action]
        elif deep:
            # logma.info(f"Search for {action}")
            for key, cfg in gcfg.items():
                if cfg is None:
                    # logma.info(f"No config for {key}")
                    continue
                elif action in cfg.keys():
                    # logma.info(f"Action {action}")
                    return cfg[action]
                elif "UUID" in cfg.keys():  # this is used for recursive searching
                    # logma.info(f"Action Overrun")
                    break
                found = search(action, cfg)
                if "UUID" in found.keys():
                    # logma.info(f"Action Found {found}")
                    return found
    logma.warning(f"Action {action} Not Found")
    if debug:
        raise Exception(f"Action {action} Not Found")
    return {
        "name_txt": None,
        "description_ltxt": None,
        "UUID": None,
        "icon_txt": None,
        "shortcut_txt": None,
        "tip_txt": None,
        "advanced_tip_txt": None,
        "widget_txt": None,
        "params_dict": None,
    }


def restore(self, cmd):
    """modify for test_nchantrs....Restore the main window state from saved settings."""
    pyqt.QSettings.setDefaultFormat(pyqt.QSettings.IniFormat)
    settings = pyqt.QSettings()
    settings.beginGroup("mainwindow")
    self.dock_widget.setExpanded(settings.value("canvasdock/expanded", True, type=bool))
    floatable = settings.value("toolbox-dock-floatable", False, type=bool)
    if floatable:
        self.dock_widget.setFeatures(self.dock_widget.features() | QDockWidget.DockWidgetFloatable)
    self.widgets_tool_box.setExclusive(settings.value("toolbox-dock-exclusive", True, type=bool))
    self.toogle_margins_action.setChecked(settings.value("scheme-margins-enabled", False, type=bool))
    self.show_log_action.setChecked(settings.value("output-dock/is-visible", False, type=bool))
    self.canvas_tool_dock.setQuickHelpVisible(settings.value("quick-help/visible", True, type=bool))
    self.float_widgets_on_top_action.setChecked(settings.value("widgets-float-on-top", False, type=bool))
    #     self.__update_from_settings()
    cmd()


# ===============================================================================||
"""
<(DNA)>:
"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
