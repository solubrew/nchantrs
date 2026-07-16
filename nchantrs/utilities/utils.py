# @@@@@@@@@@@@@@@@ Nchantrs.Utils @@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
    docid: <^(UUID)^>
    name: Nchantrs Utils - General Utility Functions
    description: >
        General utility functions for nchantrs including dataframe to tree conversion,
        dialog lookup, action configuration search, and settings restoration.
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
from __future__ import annotations

import logging
from os.path import abspath, dirname, exists, join
from typing import Any, Optional

# ======================================3rd Party Library Modules======================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from nchantrs.libraries import pyqt
from kahndor.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  #                                                 ||

logma: Logma = Logma(__name__)
log = False
if not log:
    logma.off()
debug: bool = True

# ====================================================================================================================||
pxcfg = join(here, "_data_", "utils.yaml")


def convert_df_to_tree(df: Any, pid: str = "0", root: Optional[dict] = None) -> dict:
    """Convert a dataframe to a tree structure.

    Args:
        df: Pandas DataFrame with pid_txt, name_txt, and UUID columns
        pid: Parent ID to start from (default: "0")
        root: Root dictionary for the tree

    Returns:
        Dictionary representing the tree structure
    """
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


def get_dialog(parent: Any, dialog_name: str) -> None:
    """Get a dialog by name from the parent.

    Args:
        parent: Parent object containing dialogs dictionary
        dialog_name: Name of the dialog to retrieve
    """
    parent.dialogs[dialog_name] = lookup_dialog(dialog_name)


def lookup(
    app: Any, action: str, cfg: Optional[dict] = None, deep: bool = False, refresh: bool = False, debug: bool = True
) -> dict:
    """Lookup action within the action configurations system.

    Args:
        app: Application instance
        action: Action name to lookup
        cfg: Optional configuration override
        deep: Whether to do deep recursive search
        refresh: Whether to refresh from database
        debug: Whether to raise exceptions on errors

    Returns:
        Dictionary containing action configuration
    """
    pxcfg = kahndor.Instruct(join(here, "_data_", "actions.yaml")).override(cfg).dikt
    if not hasattr(app, "model"):
        return {}
    refresh = True
    cfg = next(app.model.store.docs["dbc"].read("app_actions"))
    if cfg is None or refresh:
        logma.info("Retrieve Actions from Database")
        table = "app_action"
        params = {"table": table}
        db_cfg = {"WHERE": {"EQUAL": {"code_group_txt": pxcfg["action_type"]}}}
        actions = next(app.model.store.docs["db"].read(params, db_cfg))
        cfg = actions.dikt[table]["df"].to_dict("records")
        cfg = {c["lookup_code_txt"]: c for c in cfg}
        app.model.store.docs["dbc"].write({"app_actions": cfg})
    logma.info(f"Action Lookup Config {cfg.keys()}")
    if cfg is None or cfg == {}:
        if debug:
            raise Exception(f"Action Lookup Config is Empty {cfg}")
        return {}
    return search(action, cfg, deep, debug=debug)


def search(action: str, gcfg: dict, deep: bool = False, debug: bool = True) -> dict:
    """Search dictionary for action recursively moving through tree levels.

    Args:
        action: Action name to search for
        gcfg: Configuration dictionary to search in
        deep: Whether to do deep recursive search
        debug: Whether to raise exceptions on errors

    Returns:
        Dictionary containing action configuration
    """
    if not isinstance(action, dict):
        if gcfg.get(action.lower(), None):
            return gcfg[action]
        elif deep:
            for key, cfg in gcfg.items():
                if cfg is None:
                    continue
                elif action in cfg.keys():
                    return cfg[action]
                elif "UUID" in cfg.keys():
                    break
                found = search(action, cfg)
                if "UUID" in found.keys():
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


def restore(self, cmd: Any) -> None:
    """Restore the main window state from saved settings.

    Args:
        self: Main window instance
        cmd: Command to execute after restoring settings
    """
    pyqt.QSettings.setDefaultFormat(pyqt.QSettings.IniFormat)
    settings = pyqt.QSettings()
    settings.beginGroup("mainwindow")
    self.dock_widget.setExpanded(settings.value("canvasdock/expanded", True, type=bool))
    floatable = settings.value("toolbox-dock-floatable", False, type=bool)
    if floatable:
        self.dock_widget.setFeatures(self.dock_widget.features() | pyqt.QDockWidget.DockWidgetFloatable)
    self.widgets_tool_box.setExclusive(settings.value("toolbox-dock-exclusive", True, type=bool))
    self.toogle_margins_action.setChecked(settings.value("scheme-margins-enabled", False, type=bool))
    self.show_log_action.setChecked(settings.value("output-dock/is-visible", False, type=bool))
    self.canvas_tool_dock.setQuickHelpVisible(settings.value("quick-help/visible", True, type=bool))
    self.float_widgets_on_top_action.setChecked(settings.value("widgets-float-on-top", False, type=bool))
    cmd()


# ===============================================================================||
"""
<(DNA)>:
"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
