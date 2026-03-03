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

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from nchantrs.libraries import pyqt
from nchantrs.widgets.annotations import NchantdLabel
from nchantrs.widgets.media.editors.selectors import NchantdDropDownExplainer
from nchantrs.widgets.groups import NchantdVScrollGroupBox
from nchantrs.widgets.media.editors.entries import NchantdActivateEntry, NchantdCheckboxEditor, NchantdCheckbox
from nchantrs.widgets.media.editors.selectors import NchantdDropDown
from ogma.logma import Logma
from nchantrs.widgets.config.settings import NchantdSettingsWidget

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "storage.yaml")
pxcfg = {}


class NchantdStorageSettings(NchantdSettingsWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(condor.Instruct(pxcfg).select("NchantdStorageSettings"))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.primary_settings_group = None

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        cfg = {"size": ["auto", "auto"]}
        self.primary_settings_group = pyqt.QGroupBox()
        self.primary_settings_group_layout = pyqt.QVBoxLayout()
        self.primary_settings_group.setLayout(self.primary_settings_group_layout)
        self.primary_settings_group.setTitle("Storage Settings")
        self.document_manager_group = pyqt.QGroupBox()
        self.document_manager_group.setTitle("Document Manager")
        document_manager_layout = pyqt.QGridLayout()
        document_manager_layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignTop)
        self.document_manager_group.setLayout(document_manager_layout)
        self.primary_settings_group_layout.addWidget(self.document_manager_group)
        cfg = {
            "text": "Enable auto save on close",
            "layout": "horizontal",
            "size": ["auto", "auto"],
            "entrybox": {"size": ["auto", "auto"]},
        }
        self.auto_save_close = NchantdCheckbox(self, cfg).initWidget()
        document_manager_layout.addWidget(self.auto_save_close, 2, 0)
        cfg = {
            "label": "Enable auto save every (mins): ",
            "layout": "horizontal",
            "size": ["auto", "auto"],
            "entrybox": {"size": [100, "auto"]},
        }
        self.auto_save_activator = NchantdCheckboxEditor(self, cfg).initWidget()
        document_manager_layout.addWidget(self.auto_save_activator, 3, 0)
        options = [3, 5, 14, 30, 365, 730, 1825]
        cfg = {
            "text": "Data in application is MARKED DELETED when deleted. This allows for long term undo and versioning. The number of days selected will control the date after which data marked DELETED will actually be erased from the application database",
            "label": "Hold Time to Keep DELETE Marked data: ",
            "layout": "vertical",
            "size": ["auto", "auto"],
            "combobox": {"size": ["auto", "auto"], "options": options},
        }
        self.delete_hold_time = NchantdDropDown(self, cfg).initWidget()
        document_manager_layout.addWidget(self.delete_hold_time, 4, 0)
        options = ["In-Place", "Locally Managed Library", "Internal Database"]
        cfg = {
            "label": "Select Default Document Storage: ",
            "layout": "horizontal",
            "size": ["auto", "auto"],
            "combobox": {"size": ["auto", "auto"], "options": options},
            "explainer": {"text": "", "size": ["auto", "auto"]},
        }
        self.default_document_storage = NchantdDropDown(self, cfg).initWidget()
        document_manager_layout.addWidget(self.default_document_storage, 5, 0)
        self.document_library_group = pyqt.QGroupBox()
        self.document_library_group.setTitle("Library Manager")
        document_library_layout = pyqt.QGridLayout()
        document_library_layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignTop)
        self.document_library_group.setLayout(document_library_layout)
        self.primary_settings_group_layout.addWidget(self.document_library_group)
        cfg = {
            "text": """The Library Manager handles storage of documents created within the application, documents downloaded with the application and documents imported into the application. 
            When the user selects a location in the entry box below the Library Manager will use that location to create the necessary locations based on the other configurations 
            provided.""",
            "wrap_limit": 600,
            "size": ["auto", "auto"],
            "justify": "Left",
        }
        library_manager_description = NchantdLabel(self, cfg).initWidget()
        document_library_layout.addWidget(library_manager_description, 1, 0)
        cfg = {
            "action": "open_local",
            "default_text": "Select Filesystem Path for Storing Local Documents: ",  # show the default library location
            "layout": "horizontal",
            "size": ["auto", "auto"],
            "entrybox": {"size": [100, "auto"]},
        }
        self.library_local_path = NchantdActivateEntry(self, cfg).initWidget()
        document_library_layout.addWidget(self.library_local_path, 2, 0)
        cfg = {
            "label": "Select Default Document Naming Convention: ",
            "default_text": "Select Filesystem Path for Storing Local Documents: ",
            "layout": "horizontal",
            "size": [300, "auto"],
            "combobox": {
                "size": ["auto", "auto"],
                "options": [
                    "{YYYYMMDD}{file_name}{extension}",
                    "{YYYYMMDDHHMM}{file_name}{extension}",
                    "{YYYYMMDDHHMMSS}{file_name}{extension}",
                    "{file_name}{YYYYMMDD}{extension}",
                    "{file_name}{YYYYMMDDHHMM}{extension}",
                    "{file_name}{YYYYMMDDHHMMSS}{extension}",
                    "{file_name}{increment}{extension}",
                    "{increment}{file_name}{extension}",
                ],
            },
        }
        self.document_storage_naming = NchantdDropDown(self, cfg).initWidget()
        document_library_layout.addWidget(self.document_storage_naming, 3, 0)

        # cfg = {
        #     "label": "Select Default Document Naming Convention: ",
        #     "default_text": "Select Filesystem Path for Storing Local Documents: ",
        #     "layout": "horizontal",
        #     "size": [300, "auto"],
        #     "entrybox": {"size": [100, "auto"]},
        # }
        # self.document_storage_naming = NchantdEntryEditor(self, cfg).initWidget()
        # document_library_layout.addWidget(self.document_storage_naming, 3, 0)

        # self.layout.addLayout(self.primary_settings_group.layout)
        self.layout.addWidget(self.primary_settings_group)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    def get_settings(self):
        """"""
        return super().get_settings("storage")

    def save(self):
        """"""
        super().save()
        # if self.auto_save_activator.changed:
        #     if self.auto_save_activator.isChecked():
        #         mins = self.auto_save_activator.get_value()
        #         self.app.model.store.store_settings_auto_save(mins)
        # if self.delete_hold_time.changed:
        #     mins = self.delete_hold_time.get_value()
        #     self.app.model.store.store_settings_delete_hold_time(mins)
        # if self.library_document_storage.changed:
        #     value = self.library_local_path.get_value()
        #     previous_value = self.app.model.store.get_settings_library_document_storage()
        #     self.app.model.store.store_settings_library_document_storage(value)
        #     if value == "Locally Managed Library":
        #         if previous_value == "Internal Database":
        #             pass  # Move from locally managed library to internal database
        #             # will require ingesting a large amount of files into the database
        #         elif previous_value == "In-Place":
        #             pass  # Move from Locally managed Library to In-Place
        #             # will require stop the movement of files to the Library...files in the Library will not have a
        #             # home to return to so they will just stay in place unless manually relocated
        #         else:
        #             raise Exception("")
        #     elif value == "Internal Database":
        #         if previous_value == "Locally Managed Library":
        #             pass  # Move from Internal Database to Locally Managed Library
        #             # will require the exporting of many documents to the locally managed library this is part of a path to and setup
        #             # reduce database size and will likely be deployed often
        #         elif previous_value == "In-Place":
        #             pass  # Move from Internal Database to In Place files
        #             # will require stoping the ingesting of new files probably give the option to output to the library
        #             # or other specified location
        #         else:
        #             raise Exception("")
        #     elif value == "In-Place":
        #         if previous_value == "Internal Database":
        #             pass  # Move from In-Place to internal Database will require ingesting a lot of documents
        #         elif previous_value == "Locally Managed Library":
        #             pass  # Move from In Place to Locally Managed Library will require move lots of documents and setting up the library
        #         else:
        #             raise Exception("")
        #     else:
        #         raise Exception("")
        #     if self.library_local_path.changed:
        #         value = self.library_local_path.get_value()
        #         self.app.model.store.store_settings_library_local_path(value)
        #     if self.document_storage_naming.changed:
        #         value = self.document_storage_naming.get_value()
        #         self.app.model.store.store_settings_document_storage_naming(value)


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
