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
from os.path import dirname, join, isdir, expanduser, abspath, exists
from os import environ, chmod
import sys
import platform
import psutil
import yaml
import logging

logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from nchantrs.libraries import pyqt
from nchantrs.widgets.controls.radios import NchantdRadioButtonGroup
from nchantrs.wizards.pages import NchantdWizardPage
from nchantrs.widgets.media.editors.editors import NchantdEntryEditor, NchantdLabeledEntry
from nchantrs.wizards.instances import NchantdNewInstanceWizard
from nchantrs.wizards.users import NchantdNewUserWizard
from nchantrs.wizards.wizards import NchantdWizard
from ogma.logma import Logma
from squirl.orgnql import fonql, yonql
from subtrix.subtrix import Mechanism

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
debug = True
logma = Logma(__name__)
if not log:
    logma.off()

# Constants for magic number replacement
REMOVE_PATH_FLAGS = 3213  # Flag for fonql.removePath()
# logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "apps.yaml")


class NchantdApplicationStartupWizard(NchantdWizard):
    """"""

    def __init__(self, app=None, cfg=None):
        """ """
        super().__init__(app, cfg)
        self.config.override(condor.Instruct(pxcfg).select("NchantdApplicationStartupWizard"))
        self.config.override(app.config).override(cfg)
        self.app = app
        self.app.startup = self
        self.application_name = self.app.application_name
        self.accept_default = True
        self.app_pages = {}
        self.application_setup_details_page = None
        self.application_configuration_page = None
        self.slug = self.app.slug
        self.new_application = True
        self.application_path = None
        self.database_path = None
        self.desktop_path = None
        self.config_path = None
        self.icon_path = None
        self.instance_path = None
        self.new_instance = True
        self.instance = None
        self.instance_focus_selection = None
        self.instance_focus = None
        self.install_from_path = abspath(join(here, "..", ".."))
        self.library_path = None
        self.shortcut_path = None
        self.is_install_active = True
        self.is_installed = False
        self.is_install_optional = self.config.dikt["install"].get("optional", False)
        self.is_install_selected = self.config.dikt["install"].get("selected", True)
        self.is_private = None
        self.is_secure = None
        self.has_configuration_methods = False
        self.ran_by_binary = False
        self.ran_by_interpreter = True
        self.run_update = True
        self.check_run_method()
        self.new_user = False
        self.storage_location = None
        self.storage_style = None
        self.wizard = True
        if not self.is_private and not self.is_secure:
            self.newUser = False
        self.os_type = platform.system().lower()
        self.user_home = environ.get("HOME", None)
        if self.user_home is None:
            self.user_home = expanduser("~")
            if self.user_home is None:
                raise Exception(f"Cant determine user home directory")
        self.device = None
        self.install_doc = None

    def initModel(self, args=None):
        """"""
        if args is None:
            args = []
        paths = self.app.model.generate_paths()
        self.config_path = self.app.model.config_path
        self.application_path = self.app.model.application_path
        self.icon_path = self.app.model.icon_path
        self.library_path = self.app.model.library_path
        self.shortcut_path = self.app.model.shortcut_path
        if self.app.is_installable is True:  # Set by the Top Level Application
            # self.new_application = True  # default to uninstalled
            logma.info(f"Application Installable")
            installed = self.check_installed()  # check for current install
            logma.info(f"Currently Installed {installed}")
            if installed is True and "setup" not in args:
                self.run_application()
            else:
                logma.info(f"Install Application")
                self.run_application_install(paths)
                self.new_instance = True
        else:
            logma.info(f"Application Not Installable")
        super().initModel()
        return self

    def initView(self, args):
        """"""
        logma.info(f"Args {args}")
        super().initView()
        if "scratch" in args:
            self.wizard = False
            return self
        if self.config.dikt.get("profile", None):
            self._load_profile(self.config.dikt["profile"])
        if self.new_application is True:
            logma.info(f"Setup New Application")
            self.application_setup_details_page = NchantdApplicationSetupDetailsPage(self).initWidget()
            # install and storage locations
            self.addPage(self.application_setup_details_page)
            self.new_instance = True
            self.new_user = True
            if self.has_configuration_methods is True:
                self.application_configuration_page = NchantdApplicationConfigurationPage(self).initWidget()
                self.addPage(self.application_configuration_page)
        else:
            logma.info("Application Already Installed")
            if self.is_secure or self.is_private:
                user = self.app.model.get_user()
                if not user:
                    self.new_user = True
        if self.new_user:
            new_user_pages = NchantdNewUserWizard(self).initWidget()
            for page_id in new_user_pages.pageIds():
                logma.info(f"User Page Added {page_id}")
                self.addPage(new_user_pages.page(page_id))
        if self.new_application is True:
            instance_pages = NchantdNewInstanceWizard(self).initWidget()
            for page_id in instance_pages.pageIds():
                logma.info(f"Instance Page Added {page_id}")
                self.addPage(instance_pages.page(page_id))
        for page in self.pageIds():
            logma.info(f"Overall Page Index {page}")
        # self.currentIdChanged.connect(self.on_next_clicked)
        return self

    def initWizard(self, cfg=None):
        """"""
        self.initModel(cfg)
        self.initView(cfg)
        if self.wizard and len(self.pageIds()) > 0:
            self.show()
            self.exec_()

        return self

    def add_page(self, page):
        """"""
        return self

    def assign_page_sequence(self):
        """"""
        return self

    def ask_user_to_update(self):
        """"""
        return self

    def check_installed(self):
        """"""
        if exists(self.app.model.config_path):
            if isinstance(self.app.model.config_path, dict):
                doc = yaml.dump(self.app.model.config_path)
            elif isinstance(self.app.model.config_path, str):
                doc = self.app.model.config_path
            elif isinstance(self.app.model.config_path, condor.Instruct):
                doc = yaml.dump(self.app.model.config_path.dikt)
            else:
                raise TypeError(f"Unsupported config_path type: {type(self.app.model.config_path)}")
            self.install_doc = yonql.Doc(doc)
            data = next(self.install_doc.read())
            if data is None:
                return False
            if data.get("installed", False) is False:
                return False
        if exists(self.app.model.application_path):
            app_path = self.app.model.application_path
            if exists(join(app_path, f"{self.slug}.pyof")):
                return True
        return False

    def check_instance(self):
        """"""
        instance_path = self.app.model.instance_path
        if exists(join(instance_path, f"{self.slug}.sqlite")):
            return True
        return False

    def check_is_already_running(self):
        """
        Check if a program with the given name is running.
        :param program_name: The name (or part of the name) of the program to check.
        :return: True if the program is running, False otherwise.
        """
        for process in psutil.process_iter(["name"]):
            try:
                if self.application_name.lower() in process.info["name"].lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def check_is_os_supported(self):
        """"""
        os_list = self.app.store.get_supported_os()
        if self.os_type in os_list:
            return True
        return False

    def check_is_up_to_date(self):
        """
        Check to see if an update is available.
        :return:
        """
        if self.app.service_manager is None:
            return False
        self.app.service_manager.check_for_updates()
        return self.app.service_manager.is_update_available

    def check_run_method(self):
        """"""
        if hasattr(sys, "_MEIPASS"):
            self.ran_by_binary = True
            self.ran_by_interpreter = False
        logma.info(f"Execution Method is Binary: {self.ran_by_binary}")
        return self

    def copy_application(self):
        """"""

    def create_database_application(self):
        """"""
        logma.info(f"Initialize Application Database")
        self.app.model.store.init_database_application()
        logma.info(f"Create Application Database Objects")
        logma.info(self.app.model.config.dikt["dstruct"]["database"]["objects"])
        # not sure the proper location of this due to the need to access the database objects configuration file
        self.app.model.store.create_objects(self.app.model.config.dikt["dstruct"]["database"]["objects"])
        self.app.model.store.cache_app_install("installed", ["create_database"])
        return True

    def create_icon(self):
        """"""
        path = join(self.app.startup.install_from_path, "nchantrs", "themes", "_data_", "icons", "launch_icon.svg")
        if exists(path):
            fonql.fileCopy(path, self.icon_path)
            if exists(self.icon_path):
                return True
        if debug:
            raise Exception(f"Path {path} does not exist")
        return False

    def create_paths(self, os_type="linux"):
        """"""
        self.os_type = os_type
        paths = []
        state = False
        # if self.os_type not in self.config.dikt["os_types"].keys():
        #     raise Exception(f"Unknown OS Type: {self.os_type}")
        if self.create_paths_config(paths):
            if self.create_paths_application(paths):
                if self.app.has_library:
                    if not self.create_paths_library(paths):
                        if debug:
                            raise Exception(f"Installing Library Failed")
                if self.create_paths_shortcut(paths):
                    self.app.model.store.cache_app_install(
                        "install_succeeded", ["directories_created", {"paths": paths}]
                    )
        state = True
        return paths, state

    def create_paths_application(self, paths):
        """"""
        verified = self.app.model.store.create_directories(self.application_path)
        paths += [self.application_path]
        if not verified:
            return False
        return True

    def create_paths_config(self, paths):
        """"""
        verified = self.app.model.store.create_directories(self.config_path)
        paths += [self.config_path]
        if not verified:
            return False
        return True

    def create_paths_instance(self, paths):
        """"""
        data = {}
        path = self.config.dikt["os_types"][self.os_type].get("instance", "")
        self.instance_path = Mechanism(path, data).run()
        verified = self.app.model.store.create_directories(self.instance_path)
        paths += [self.instance_path]
        if not verified:
            return False
        return True

    def create_paths_library(self, paths):
        """"""
        verified = self.app.model.store.create_directories(self.library_path)
        paths += [self.library_path]
        if not verified:
            return False
        return True

    def create_paths_shortcut(self, paths):
        """"""
        verified = self.app.model.store.create_directories(self.shortcut_path)
        paths += [self.library_path]
        # [DONE] fix shortcut path
        # if not verified:
        #     msg = {
        #         "install": "failed",
        #         "msg": "failed to create library path",
        #         "data": {"path": self.shortcut_path},
        #     }
        #     self.run_uninstall(msg, paths)
        #     return False
        verified = self.app.model.store.create_directories(self.icon_path)
        paths += [self.icon_path]
        if not verified:
            return False
        return True

    def create_shortcut(self):
        """"""
        if self.os_type == "linux":
            entry = self.config.dikt["os_types"].get(self.os_type, "").get("shortcut", "").get("text", "")
            with open(self.shortcut_path, "w") as desktop_file:  # Write the .desktop file
                data = {
                    "<[application_name]>": self.slug,
                    "<[icon_path]>": self.icon_path,
                    "<[application_path]>": self.application_path,
                }
                desktop_file.write(Mechanism(entry, data).run())
            chmod(self.shortcut_path, 0o755)  # Make .desktop file executable [DONE] permissions for this
        elif self.os_type == "windows":
            if self.shortcut_path is None:
                self.desktop_path = join(environ["USERPROFILE"], "Desktop")
                self.shortcut_path = join(self.desktop_path, f"{self.slug}.lnk")
            lnk = Lnk()  # Create a Lnk object
            lnk.path = self.application_path  # Path to the target executable
            lnk.description = f"Shortcut for {self.slug}"  # Shortcut description
            lnk.relative_path = self.application_path
            # Add an icon if specified
            if self.icon_path:
                lnk.icon = self.icon_path
            # Save the shortcut file
            with open(self.shortcut_path, "wb") as f:
                lnk.dump(f)
        else:
            raise Exception(f"Unknown OS Type: {self.os_type}")
        logma.info(f"Icon created at {self.icon_path}")
        return self

    def reject(self):
        """"""
        # Optionally, confirm with the user before exiting
        reply = pyqt.QMessageBox.question(
            self,
            "Exit Installer",
            "Are you sure you want to cancel the installation?",
            pyqt.QMessageBox.Yes | pyqt.QMessageBox.No,
        )
        if reply == pyqt.QMessageBox.Yes:
            logma.info("Installation aborted")
            super().reject()  # Close the wizard
            self.app.model.store.disconnect()
            self.run_uninstall_application("cancel")
            sys.exit()
        else:
            logma.info("Cancel aborted")
        return

    def remove_directories(self, paths, db="db"):
        """"""
        if not isinstance(paths, list):
            paths = [paths]
        for path in paths:
            # logma.info(f"Check exists {path} {path[:-1]}")
            if exists(path) or exists(path[:-1]):
                # logma.info(f"Remove Path {path} {path[:-1]}")
                fonql.removePath(path, REMOVE_PATH_FLAGS)
                self.app.model.store.cache_app_install("uninstalled", ["remove_directory", {"path": path}])
        return

    def run_application(self):
        """"""
        self.app.model.initialize_application()
        cfg = {}
        self.app.model.store.init_database_application(cfg)
        logma.info(f"Check Application is Up to date")
        if self.check_is_up_to_date() is False or debug is True:
            if self.ask_user_to_update() is True or debug is True:
                self.run_application_update()
        self.app.model.store.load_instance()
        # [DONE] load primary instance
        self.new_application = False
        self.is_installed = True
        # if self.app.has_services or debug is True:
        #     if self.check_is_up_to_date() is False or debug is True:
        #         if self.ask_user_to_update() is True or debug is True:
        #             self.run_application_update()
        return self

    def run_application_install(self, paths):
        """"""
        self.run_install_application_prep(paths)
        self.app.model.initialize_application()  # Sets up the Data Policy and the User
        logma.info(f"Create Paths")
        paths, state = self.create_paths()  # Sets up local storage paths
        if state is True:
            self.create_database_application()
            self.copy_application()
            self.create_icon()
            # self.create_shortcut()
            self.run_install_complete()
        else:
            self.run_uninstall_application(paths)
        return self

    def run_application_update(self):
        """
        Get updated application
        Get updated hashes
        Verify application
        Copy application to temp location
        start new application
        remove old application
        copy new application to orginal location
        restart application from original location
        remove temp location
        :return:
        """
        # [DONE] focused on changes that need to be made to application and/or instance databases as a result of an
        # application code update or specific data related upgrade
        logma.info(f"Run Application Update")
        self.version = self.app.dbupdate.run_updates("db")
        logma.info(f"New Version {self.version}")
        self.app.set_version(self.version)
        self.app.model.update_version("db", self.version, True, "db")
        return self

    def run_install_application_prep(self, paths):
        """"""
        self.run_uninstall_application("preinstall", paths)
        return self

    def run_install_complete(self):
        """Write config path with install configuration settings"""
        if self.install_doc is None:
            self.install_doc = yonql.Doc(self.app.model.config_path)
            next(self.install_doc.read())
        if self.install_doc.dikt is None:
            self.install_doc.dikt = {}
        self.install_doc.dikt["install"] = self.config.dikt["install"]
        self.install_doc.dikt["installed"] = True
        self.install_doc.write(self.install_doc.dikt)
        return self

    def run_uninstall_application(self, reason="debug", paths=None):
        """"""
        if paths is None:
            paths = []
        paths.append(self.config_path)
        paths.append(self.application_path)
        paths.append(self.icon_path)
        paths.append(self.shortcut_path)
        paths.append(self.instance_path)
        paths = list(set([x for x in paths if x is not None]))
        # library = paths.pop(paths.index([x for x in paths if "NchantdLibrary" in x][0]))
        # if not isdir(library):
        #     paths.append(library)
        self.remove_directories(paths)
        # self.app.model.store.cache_app_install("uninstall", ["uninstalled", "uninstall", reason])
        return self

    def set_library_status(self):
        """
        TODO controls for allowing the user to turn the library on but only for paid versions
        :return:
        """
        self.library_active = True
        if self.library_active:
            self.library_path = join(expanduser("~"), "Documents", "NchantdLibrary/")
            if not exists(self.library_path):
                fonql.touch(self.library_path)
        return self

    def _load_profile(self, profile):
        """"""
        self.accept_default = profile.get("accept_default", None)
        if self.accept_default:
            self.isSecure = False
            self.isPrivate = False

        self.instance_focus = profile.get("focus", None)
        if self.instance_focus is None:
            self.instance_focus = "greenfield"

        self.storage_location = profile.get("storage_location", None)
        self.storage_style = profile.get("storage_style", None)
        if self.storage_location is None:
            if self.storage_style == "nchantd_library":
                self.storage_location = abspath(join(expanduser("~"), "Documents", "NchantdLibrary"))
        return self


class NchantdAddExtensionWizard(NchantdWizardPage):
    """"""

    def __init__(self, parent=None, cfg=None):
        """"""
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdFundAccountsTab")
        if parent:
            self.config.override(parent.config)
        self.config.override(cfg)

    def initModel(self):
        """"""

    def initView(self):
        """"""

    def initWidget(self):
        """"""


class NchantdRemoveExtensionWizard(NchantdWizardPage):
    """"""

    def __init__(self, parent=None, cfg=None):
        """"""
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdFundAccountsTab")
        if parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdRemoveExtensionWizard, self).__init__(self.parent, self.config)

    def initModel(self):
        """"""

    def initView(self):
        """"""

    def initWidget(self):
        """"""


class NchantdApplicationSetupDetailsPage(NchantdWizardPage):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdApplicationSetupDetailsPage")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)
        self.privacy_level = None
        self.security_level = None

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        self.setTitle("New Application Setup")
        self.setSubTitle("Enter Application Details")

        cfg = {"text": "Enter Application Name:", "layout": "horizontal"}
        self.application_name = NchantdLabeledEntry(self, cfg).initWidget()
        self.application_name.setPlaceholderText(self.parent.app.application_name)  # "NchantdOffice")
        self.layout.addWidget(self.application_name)
        self.registerField("application_name", self.application_name)

        cfg = {"text": "Enter Document Storage Location:", "layout": "horizontal"}
        self.storage_location = NchantdLabeledEntry(self, cfg).initWidget()
        if self.config.dikt.get("library_path", None):
            self.storage_location.setPlaceholderText(self.config.dikt.get("library_path"))
        else:
            library = f"{abspath(join(expanduser('~'), 'Documents', f'{self.parent.app.application_name}Library'))}"
            self.storage_location.setPlaceholderText(library)
        self.layout.addWidget(self.storage_location)
        self.registerField("storage_location", self.storage_location)

        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdApplicationConfigurationPage(NchantdWizardPage):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(condor.Instruct(pxcfg).select("Nchantd"))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)

    def initModel(self, cfg=None):
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None):
        """"""
        super().initView(cfg)
        cfg = {"text": "Select Security Level", "options": ["Medium", "High"]}
        self.security_level = NchantdRadioButtonGroup(self, cfg).initWidget()
        self.layout.addWidget(self.security_level)
        self.registerField("security_level", self.security_level)

        cfg = {"text": "Select Privacy Level", "options": ["Medium", "High"]}
        self.privacy_level = NchantdRadioButtonGroup(self, cfg).initWidget()
        self.layout.addWidget(self.security_level)
        self.registerField("privacy_level", self.security_level)

        # cfg = {"text": "Select Install", "options": ["Install Locally", "Run as Portable"]}
        # self.install_option = NchantdRadioButtonGroup(self, cfg).initWidget()
        # self.layout.addWidget(self.install_option)
        # self.registerField("install_option", self.install_option)
        #
        # cfg = {"text": "Select Install Location:", "layout": "horizontal"}
        #
        # self.config.override({"buttons": {f"open_{self.file_type}": lookup(self.app, f"open_{self.file_type}")}})
        # self.open_file = NchantdButton(self, self.config.dikt["buttons"][f"open_{self.file_type}"]).initWidget()
        # params = self.config
        # self.open_file.set_handler(self.open_file_sigil, params)
        #
        # self.install_location.setPlaceholderText("NchantdOffice")
        # self.layout.addWidget(self.install_location)
        # self.registerField("install_location", self.install_location)

        cfg = {
            "text": "Select Data Storage Method",
            "options": [
                "Nchantd Library",
                "In-Place File System",
            ],
        }
        self.method = NchantdRadioButtonGroup(self, cfg).initWidget()
        self.layout.addWidget(self.method)
        self.registerField("method", self.method)

        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
