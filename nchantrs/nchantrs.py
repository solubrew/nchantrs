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
from os.path import abspath, dirname, join, expanduser
import datetime as dt
import tracemalloc
from os import environ

# ======================================3rd Party Library Modules=====================================================||
# from guppy import hpy
# from pympler import muppy, summary

# ======================================Solutions Brewer Library Modules==============================================||
from nchantrs.widgets.applications.applications import NchantdCloak
from nchantrs.dialogs.dialogs import NchantdCape, NchantdClip
from nchantrs.widgets.browsers.initialize import _configure_qt_environment
from nchantrs.wizards.apps import NchantdApplicationStartupWizard  # , NchantdQuickStartWizard
from ogma.logma import Logma
from squirl.objnql import txtonql
#from pyularity.pyularity import Pyularity

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)
debug = False

# ====================================================================================================================||
pxcfg = join(here, "_data_", "nchantrs.yaml")
pxcfg = {}


def aberration(name, args=None, widget=None, cfg=None):
    """Aberration executes a single widget dialog useful for direct interaction widgets"""
    if cfg is None:
        cfg = {}
    cfg["widget"] = widget
    aber = NchantdClip(name, args, widget, cfg)
    aber.initApp()


def distortion(name, args, widget, instance=None, cfg=None, log_file=None):
    """A Distortion executes a complex single widget dialog useful for direct interaction widgets"""
    if cfg is None:
        cfg = {}
    cfg["widget"] = widget
    _configure_qt_environment()
    cape = NchantdCape(name, instance, None, cfg, args, log_file=log_file)
    # quick_start = NchantdQuickStartWizard(cape, {})
    # quick_start.initWizard(args)
    result = cape.initApp(cfg)
    # Ensure the application exits properly
    return result


def nchantment(name, args, main_app=None, cfg=None, startup_app=None, profile_override=None):
    """An Nchantment executes a complex Nchantrs application with defined storage and installation paths"""
    logma.info("Begin Nchantment")
    if debug:
        tracemalloc.start()
    if main_app is None:
        main_app = NchantdCloak
    if startup_app is None:
        startup_app = NchantdApplicationStartupWizard
    instance = None
    if "instance" in args:
        instance = args["instance"]
    # Call configuration before Qt imports
    _configure_qt_environment()
    # implement an update mode for the app accessible by pyularity
    app = main_app(name, instance, None, cfg, args)
    startup = startup_app(app, {"profile": profile_override})
    logma.info("Nchantment Initialized")
    startup.initWizard(args)
    logma.info("Nchantment Complete")
    # TODO: add connections to the collected wizard data to launch the correct application
    app.initApp({"startup": startup})
    logma.info("Complete")
    if debug:
        analyze_strings()
        memory_analysis()
        memory_summary()
    return app


def flection(name, args, main_app=None, cfg=None, startup_app=None, profile_override=None):
    """An Flection executes a complex Nchantrs application supervisor with defined storage and installation paths"""
    # NOTE: Pyularity integration - requires pyularity package to be installed
    # Uncomment when package is available:
    # from pyularity.pyularity import Pyularity
    logma.info("Begin Flection")
    if debug:
        tracemalloc.start()
    if main_app is None:
        main_app = NchantdCloak
    if startup_app is None:
        startup_app = NchantdApplicationStartupWizard
    logma.info("Flection Initialized")
    
    # Lazy import - only load Pyularity if needed
    try:
        from pyularity.pyularity import Pyularity
        supervisor = Pyularity({"name": name, "args": args, "cfg": cfg, "profile": profile_override})
        supervisor.set_main_app(main_app).set_startup_app(startup_app)
        instance = "latest"
        logma.info(f"Flection Launch App {instance}")
        supervisor.launch_app(instance=instance)
    except ImportError:
        logma.warning("Pyularity not installed - falling back to standard nchantment")
        # Fall back to nchantment behavior
        instance = None
        if "instance" in args:
            instance = args["instance"]
        _configure_qt_environment()
        app = main_app(name, instance, None, cfg, args)
        startup = startup_app(app, {"profile": profile_override})
        startup.initWizard(args)
        app.initApp({"startup": startup})
    
    logma.info("Complete")
    if debug:
        analyze_strings()
        memory_analysis()
        memory_summary()
    return app if 'app' in locals() else supervisor


def analyze_strings():
    """"""
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics("lineno")
    logma.info("[ Top 10 Memory Consumers ]")
    for stat in top_stats[:10]:
        logma.info(stat)
    tracemalloc.stop()


def memory_analysis():
    """"""
    heap = hpy().heap()
    logma.info("Heap Analysis:")
    logma.info(heap)


def memory_summary():
    """"""
    all_objects = muppy.get_objects()
    logma.info("Memory Summary:")
    path = join(expanduser("~"), "_work", "memory_summary.txt")
    txtonql.Doc(path).write(summary.summarize(all_objects))


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
