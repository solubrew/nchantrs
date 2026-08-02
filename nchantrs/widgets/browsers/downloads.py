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
from os import environ
import sys
import os
import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import logging
logger = logging.getLogger(__name__)
import sys
import os
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.libraries import pyqt
from nchantrs.widgets.widgets import NchantdWidget
from nchantrs.widgets.browsers.codecs.h264 import OpenH264Downloader
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
pxcfg = join(here, '_data_', '.yaml')

class NchantdDownloadStatus(Enum):
    """Download status states"""
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    FAILED = 'failed'
    PAUSED = 'paused'

@dataclass
class NchantdDownloadInfo:
    """Information about a download"""
    id: str
    url: str
    filename: str
    save_path: str
    total_bytes: int = 0
    received_bytes: int = 0
    status: NchantdDownloadStatus = NchantdDownloadStatus.PENDING
    start_time: float = 0
    end_time: float = 0
    mime_type: str = ''
    suggested_filename: str = ''
    error_message: str = ''

    def __post_init__(self) -> None:
        logma.info(f'NchantdDownloadInfo created: {self.id}')

    @property
    def progress_percentage(self) -> float:
        """Get download progress as percentage"""
        if self.total_bytes > 0:
            return self.received_bytes / self.total_bytes * 100
        return 0.0

    @property
    def speed_bps(self) -> float:
        """Get download speed in bytes per second"""
        if self.start_time > 0 and self.received_bytes > 0:
            elapsed = time.time() - self.start_time
            return self.received_bytes / elapsed if elapsed > 0 else 0
        return 0.0

    @property
    def formatted_size(self) -> str:
        """Get formatted file size"""
        return self._format_bytes(self.total_bytes)

    @property
    def formatted_received(self) -> str:
        """Get formatted received bytes"""
        return self._format_bytes(self.received_bytes)

    @property
    def formatted_speed(self) -> str:
        """Get formatted download speed"""
        speed = self.speed_bps
        if speed > 1024 * 1024:
            return f'{speed / (1024 * 1024):.1f} MB/s'
        elif speed > 1024:
            return f'{speed / 1024:.1f} KB/s'
        else:
            return f'{speed:.0f} B/s'

    def _format_bytes(self, bytes_value: int) -> str:
        """Format bytes into human readable string"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f'{bytes_value:.1f} {unit}'
            bytes_value /= 1024.0
        return f'{bytes_value:.1f} PB'

class NchantdDownloadManager(pyqt.QObject):
    """Manages all downloads"""
    downloadStarted = pyqt.Signal(NchantdDownloadInfo)
    downloadProgress = pyqt.Signal(str, int, int)
    downloadFinished = pyqt.Signal(str, bool)
    downloadStatusChanged = pyqt.Signal(str, NchantdDownloadStatus)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.downloads: Dict[str, NchantdDownloadInfo] = {}
        self.active_downloads: Dict[str, pyqt.QWebEngineDownloadRequest] = {}
        self.download_counter = 0
        self.default_download_path = self._get_default_download_path()
        self.load_download_history()

    def _get_default_download_path(self) -> str:
        """Get default download directory"""
        download_path = pyqt.QStandardPaths.writableLocation(pyqt.QStandardPaths.StandardLocation.DownloadLocation)
        if not download_path:
            download_path = os.path.expanduser('~/Downloads')
        os.makedirs(download_path, exist_ok=True)
        return download_path

    def handle_download_request(self, download: pyqt.QWebEngineDownloadRequest) -> str:
        """Handle a new download request"""
        self.download_counter += 1
        download_id = f'download_{self.download_counter}_{int(time.time())}'
        suggested_name = download.suggestedFileName()
        if not suggested_name:
            suggested_name = f'download_{self.download_counter}'
        save_path = self._get_save_path(suggested_name)
        if not save_path:
            download.cancel()
            return ''
        download_info = NchantdDownloadInfo(id=download_id, url=download.url().toString(), filename=os.path.basename(save_path), save_path=save_path, total_bytes=download.totalBytes(), mime_type=download.mimeType(), suggested_filename=suggested_name, start_time=time.time(), status=NchantdDownloadStatus.IN_PROGRESS)
        download.setDownloadDirectory(os.path.dirname(save_path))
        download.setDownloadFileName(os.path.basename(save_path))
        download.downloadProgress.connect(lambda received, total, did=download_id: self._on_download_progress(did, received, total))
        download.finished.connect(lambda did=download_id: self._on_download_finished(did))
        download.stateChanged.connect(lambda state, did=download_id: self._on_download_state_changed(did, state))
        self.downloads[download_id] = download_info
        self.active_downloads[download_id] = download
        download.accept()
        self.downloadStarted.emit(download_info)
        self.downloadStatusChanged.emit(download_id, NchantdDownloadStatus.IN_PROGRESS)
        logma.info(f'Started download: {download_info.filename} -> {save_path}')
        return download_id

    def _get_save_path(self, suggested_name: str) -> str:
        """Get save path for download"""
        save_path = os.path.join(self.default_download_path, suggested_name)
        counter = 1
        original_path = save_path
        while os.path.exists(save_path):
            name, ext = os.path.splitext(original_path)
            save_path = f'{name}_{counter}{ext}'
            counter += 1
        return save_path

    @pyqt.Slot(str, int, int)
    def _on_download_progress(self, download_id: str, received: int, total: int) -> None:
        """Handle download progress updates"""
        if download_id in self.downloads:
            download_info = self.downloads[download_id]
            download_info.received_bytes = received
            download_info.total_bytes = total
            self.downloadProgress.emit(download_id, received, total)

    @pyqt.Slot(str)
    def _on_download_finished(self, download_id: str) -> None:
        """Handle download completion"""
        if download_id in self.downloads:
            download_info = self.downloads[download_id]
            download_info.end_time = time.time()
            if download_id in self.active_downloads:
                download_request = self.active_downloads[download_id]
                success = download_request.state() == pyqt.QWebEngineDownloadRequest.DownloadState.DownloadCompleted
                if success:
                    download_info.status = NchantdDownloadStatus.COMPLETED
                    logma.info(f'Download completed: {download_info.filename}')
                else:
                    download_info.status = NchantdDownloadStatus.FAILED
                    download_info.error_message = 'Download failed'
                    logma.info(f'Download failed: {download_info.filename}')
                del self.active_downloads[download_id]
                self.downloadFinished.emit(download_id, success)
                self.downloadStatusChanged.emit(download_id, download_info.status)
                self.save_download_history()

    @pyqt.Slot(str, 'pyqt.QWebEngineDownloadRequest::DownloadState')
    def _on_download_state_changed(self, download_id: str, state) -> None:
        """Handle download state changes"""
        if download_id not in self.downloads:
            return
        download_info = self.downloads[download_id]
        if state == pyqt.QWebEngineDownloadRequest.DownloadState.DownloadCancelled:
            download_info.status = NchantdDownloadStatus.CANCELLED
            download_info.error_message = 'Cancelled by user'
        elif state == pyqt.QWebEngineDownloadRequest.DownloadState.DownloadInterrupted:
            download_info.status = NchantdDownloadStatus.FAILED
            download_info.error_message = 'Download interrupted'
        self.downloadStatusChanged.emit(download_id, download_info.status)

    def cancel_download(self, download_id: str) -> None:
        """Cancel an active download"""
        if download_id in self.active_downloads:
            download_request = self.active_downloads[download_id]
            download_request.cancel()
            logma.info(f'Cancelled download: {download_id}')

    def pause_download(self, download_id: str) -> None:
        """Pause an active download"""
        if download_id in self.active_downloads:
            download_request = self.active_downloads[download_id]
            download_request.pause()
            if download_id in self.downloads:
                self.downloads[download_id].status = NchantdDownloadStatus.PAUSED
                self.downloadStatusChanged.emit(download_id, NchantdDownloadStatus.PAUSED)

    def resume_download(self, download_id: str) -> None:
        """Resume a paused download"""
        if download_id in self.active_downloads:
            download_request = self.active_downloads[download_id]
            download_request.resume()
            if download_id in self.downloads:
                self.downloads[download_id].status = NchantdDownloadStatus.IN_PROGRESS
                self.downloadStatusChanged.emit(download_id, NchantdDownloadStatus.IN_PROGRESS)

    def get_download_info(self, download_id: str) -> Optional[NchantdDownloadInfo]:
        """Get download information"""
        return self.downloads.get(download_id)

    def get_all_downloads(self) -> List[NchantdDownloadInfo]:
        """Get all download information"""
        return list(self.downloads.values())

    def get_active_downloads(self) -> List[NchantdDownloadInfo]:
        """Get currently active downloads"""
        return [info for info in self.downloads.values() if info.status == NchantdDownloadStatus.IN_PROGRESS]

    def clear_completed_downloads(self) -> None:
        """Clear completed downloads from history"""
        completed_ids = [download_id for download_id, info in self.downloads.items() if info.status in [NchantdDownloadStatus.COMPLETED, NchantdDownloadStatus.FAILED, NchantdDownloadStatus.CANCELLED]]
        for download_id in completed_ids:
            del self.downloads[download_id]
        self.save_download_history()
        logma.info(f'Cleared {len(completed_ids)} completed downloads')

    def save_download_history(self) -> None:
        """Save download history to file"""
        try:
            history_data = []
            for download_info in self.downloads.values():
                if download_info.status not in [NchantdDownloadStatus.IN_PROGRESS, NchantdDownloadStatus.PAUSED]:
                    data = asdict(download_info)
                    data['status'] = download_info.status.value
                    history_data.append(data)
            with open('download_history.json', 'w') as f:
                json.dump(history_data, f, indent=2)
        except Exception as e:
            logma.info(f'Error saving download history: {e}')

    def load_download_history(self) -> None:
        """Load download history from file"""
        try:
            with open('download_history.json', 'r') as f:
                history_data = json.load(f)
            for data in history_data:
                data['status'] = NchantdDownloadStatus(data['status'])
                download_info = NchantdDownloadInfo(**data)
                self.downloads[download_info.id] = download_info
            logma.info(f'Loaded {len(history_data)} downloads from history')
        except FileNotFoundError:
            pass
        except Exception as e:
            logma.info(f'Error loading download history: {e}')

    def set_default_download_path(self, path: str) -> None:
        """Set default download directory"""
        if os.path.isdir(path):
            self.default_download_path = path
            logma.info(f'Default download path set to: {path}')
        else:
            logma.info(f'Invalid download path: {path}')

class DownloadItemWidget(pyqt.QWidget):
    """Widget representing a single download item"""
    cancelRequested = pyqt.Signal(str)
    pauseRequested = pyqt.Signal(str)
    resumeRequested = pyqt.Signal(str)
    openFileRequested = pyqt.Signal(str)
    openFolderRequested = pyqt.Signal(str)

    def __init__(self, download_info: NchantdDownloadInfo, parent=None) -> None:
        super().__init__(parent)
        self.download_info = download_info
        self.setup_ui()
        logma.info(f'DownloadItemWidget initialized')

    def setup_ui(self) -> None:
        """Setup the download item UI"""
        layout = pyqt.QVBoxLayout(self)
        top_layout = pyqt.QHBoxLayout()
        self.filename_label = pyqt.QLabel(self.download_info.filename)
        self.filename_label.setStyleSheet('font-weight: bold;')
        top_layout.addWidget(self.filename_label)
        self.status_label = pyqt.QLabel(self.download_info.status.value.title())
        top_layout.addWidget(self.status_label)
        top_layout.addStretch()
        layout.addLayout(top_layout)
        self.progress_bar = pyqt.QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(int(self.download_info.progress_percentage))
        layout.addWidget(self.progress_bar)
        bottom_layout = pyqt.QHBoxLayout()
        self.info_label = pyqt.QLabel(self._get_info_text())
        bottom_layout.addWidget(self.info_label)
        bottom_layout.addStretch()
        if self.download_info.status == NchantdDownloadStatus.IN_PROGRESS:
            self.pause_button = pyqt.QPushButton('Pause')
            self.pause_button.clicked.connect(lambda: self.pauseRequested.emit(self.download_info.id))
            bottom_layout.addWidget(self.pause_button)
            self.cancel_button = pyqt.QPushButton('Cancel')
            self.cancel_button.clicked.connect(lambda: self.cancelRequested.emit(self.download_info.id))
            bottom_layout.addWidget(self.cancel_button)
        elif self.download_info.status == NchantdDownloadStatus.PAUSED:
            self.resume_button = pyqt.QPushButton('Resume')
            self.resume_button.clicked.connect(lambda: self.resumeRequested.emit(self.download_info.id))
            bottom_layout.addWidget(self.resume_button)
            self.cancel_button = pyqt.QPushButton('Cancel')
            self.cancel_button.clicked.connect(lambda: self.cancelRequested.emit(self.download_info.id))
            bottom_layout.addWidget(self.cancel_button)
        elif self.download_info.status == NchantdDownloadStatus.COMPLETED:
            self.open_button = pyqt.QPushButton('Open')
            self.open_button.clicked.connect(lambda: self.openFileRequested.emit(self.download_info.id))
            bottom_layout.addWidget(self.open_button)
            self.show_folder_button = pyqt.QPushButton('Show in Folder')
            self.show_folder_button.clicked.connect(lambda: self.openFolderRequested.emit(self.download_info.id))
            bottom_layout.addWidget(self.show_folder_button)
        layout.addLayout(bottom_layout)

    def _get_info_text(self) -> str:
        """Get information text for download"""
        if self.download_info.status == NchantdDownloadStatus.COMPLETED:
            return f'{self.download_info.formatted_size}'
        elif self.download_info.status == NchantdDownloadStatus.IN_PROGRESS:
            return f'{self.download_info.formatted_received} / {self.download_info.formatted_size} - {self.download_info.formatted_speed}'
        else:
            return f'{self.download_info.formatted_received} / {self.download_info.formatted_size}'

    def update_progress(self, received: int, total: int) -> None:
        """Update progress display"""
        self.download_info.received_bytes = received
        self.download_info.total_bytes = total
        progress = int(self.download_info.progress_percentage)
        self.progress_bar.setValue(progress)
        self.info_label.setText(self._get_info_text())

    def update_status(self, status: NchantdDownloadStatus) -> None:
        """Update download status"""
        self.download_info.status = status
        self.status_label.setText(status.value.title())
        self.setup_ui()

class DownloadsDialog(pyqt.QDialog):
    """Dialog showing all downloads"""

    def __init__(self, download_manager: NchantdDownloadManager, parent=None) -> None:
        super().__init__(parent)
        self.download_manager = download_manager
        self.download_widgets: Dict[str, DownloadItemWidget] = {}
        self.setup_ui()
        self.setup_connections()
        self.load_downloads()
        logma.info(f'DownloadsDialog initialized')

    def setup_ui(self) -> None:
        """Setup downloads dialog UI"""
        self.setWindowTitle('Downloads')
        self.setModal(False)
        self.resize(800, 600)
        layout = pyqt.QVBoxLayout(self)
        toolbar_layout = pyqt.QHBoxLayout()
        self.clear_completed_button = pyqt.QPushButton('Clear Completed')
        self.pause_all_button = pyqt.QPushButton('Pause All')
        self.resume_all_button = pyqt.QPushButton('Resume All')
        self.settings_button = pyqt.QPushButton('Settings')
        toolbar_layout.addWidget(self.clear_completed_button)
        toolbar_layout.addWidget(self.pause_all_button)
        toolbar_layout.addWidget(self.resume_all_button)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.settings_button)
        layout.addLayout(toolbar_layout)
        from PySide6.QtWidgets import QScrollArea
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(scroll_area.ScrollBarPolicy.ScrollBarAsNeeded)
        self.downloads_widget = pyqt.QWidget()
        self.downloads_layout = pyqt.QVBoxLayout(self.downloads_widget)
        self.downloads_layout.addStretch()
        scroll_area.setWidget(self.downloads_widget)
        layout.addWidget(scroll_area, 1)

    def setup_connections(self) -> None:
        """Setup signal connections"""
        self.download_manager.downloadStarted.connect(self.add_download)
        self.download_manager.downloadProgress.connect(self.update_download_progress)
        self.download_manager.downloadStatusChanged.connect(self.update_download_status)
        self.clear_completed_button.clicked.connect(self.clear_completed_downloads)
        self.pause_all_button.clicked.connect(self.pause_all_downloads)
        self.resume_all_button.clicked.connect(self.resume_all_downloads)
        self.settings_button.clicked.connect(self.show_settings)

    def load_downloads(self) -> None:
        """Load existing downloads"""
        for download_info in self.download_manager.get_all_downloads():
            self.add_download(download_info)

    @pyqt.Slot(NchantdDownloadInfo)
    def add_download(self, download_info: NchantdDownloadInfo) -> None:
        """Add a new download to the UI"""
        if download_info.id in self.download_widgets:
            return
        download_widget = DownloadItemWidget(download_info)
        download_widget.cancelRequested.connect(self.download_manager.cancel_download)
        download_widget.pauseRequested.connect(self.download_manager.pause_download)
        download_widget.resumeRequested.connect(self.download_manager.resume_download)
        download_widget.openFileRequested.connect(self.open_file)
        download_widget.openFolderRequested.connect(self.open_folder)
        self.downloads_layout.insertWidget(self.downloads_layout.count() - 1, download_widget)
        self.download_widgets[download_info.id] = download_widget

    @pyqt.Slot(str, int, int)
    def update_download_progress(self, download_id: str, received: int, total: int) -> None:
        """Update download progress in UI"""
        if download_id in self.download_widgets:
            self.download_widgets[download_id].update_progress(received, total)

    @pyqt.Slot(str, NchantdDownloadStatus)
    def update_download_status(self, download_id: str, status: NchantdDownloadStatus) -> None:
        """Update download status in UI"""
        if download_id in self.download_widgets:
            self.download_widgets[download_id].update_status(status)

    @pyqt.Slot(str)
    def open_file(self, download_id: str) -> None:
        """Open downloaded file"""
        download_info = self.download_manager.get_download_info(download_id)
        if download_info and os.path.exists(download_info.save_path):
            os.startfile(download_info.save_path)

    @pyqt.Slot(str)
    def open_folder(self, download_id: str) -> None:
        """Open folder containing downloaded file"""
        download_info = self.download_manager.get_download_info(download_id)
        if download_info:
            folder_path = os.path.dirname(download_info.save_path)
            os.startfile(folder_path)

    @pyqt.Slot()
    def clear_completed_downloads(self) -> None:
        """Clear completed downloads"""
        for download_id, download_info in list(self.download_manager.downloads.items()):
            if download_info.status in [NchantdDownloadStatus.COMPLETED, NchantdDownloadStatus.FAILED, NchantdDownloadStatus.CANCELLED]:
                if download_id in self.download_widgets:
                    widget = self.download_widgets[download_id]
                    self.downloads_layout.removeWidget(widget)
                    widget.deleteLater()
                    del self.download_widgets[download_id]
        self.download_manager.clear_completed_downloads()

    @pyqt.Slot()
    def pause_all_downloads(self) -> None:
        """Pause all active downloads"""
        for download_id, download_info in self.download_manager.downloads.items():
            if download_info.status == NchantdDownloadStatus.IN_PROGRESS:
                self.download_manager.pause_download(download_id)

    @pyqt.Slot()
    def resume_all_downloads(self) -> None:
        """Resume all paused downloads"""
        for download_id, download_info in self.download_manager.downloads.items():
            if download_info.status == NchantdDownloadStatus.PAUSED:
                self.download_manager.resume_download(download_id)

    @pyqt.Slot()
    def show_settings(self) -> None:
        """Show download settings"""
        path = pyqt.QFileDialog.getExistingDirectory(self, 'Select Download Directory', self.download_manager.default_download_path)
        if path:
            self.download_manager.set_default_download_path(path)

class CodecDownloadThread(pyqt.QThread):
    """Background thread for downloading OpenH264."""
    finished = pyqt.Signal(bool, str)
    progress = pyqt.Signal(str)

    def __init__(self, downloader: OpenH264Downloader) -> None:
        super().__init__()
        self.downloader = downloader

    def run(self) -> None:
        try:
            self.progress.emit('Downloading OpenH264 codec...')
            library_path = self.downloader.download_and_extract()
            self.progress.emit('Setting up codec...')
            self.finished.emit(True, f'OpenH264 codec ready at: {library_path}')
        except Exception as e:
            self.finished.emit(False, f'Failed to setup codec: {str(e)}')

class NchantdDownload(NchantdWidget):
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

class NchantdDownloadsManagerSigil(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdDownloadsManager')
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)
        self.download_list = None
        self.clear_button = None
        logma.info(f'NchantdDownloadsManagerSigil initialized')

    def add_download(self, download) -> Any:
        """"""
        self.download_list.append(download)
        return self

    def initModel(self, days_of_history=10) -> Any:
        """"""
        super().initModel()
        [self.add_download(x) for x in self.app.model.downloads.history(days_of_history)]
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        self.download_list = NchantdListWidget(self, self.config)
        self.download_list.initWidget()
        self.layout.addWidget(self.download_list)
        self.clear_button = NchantdButtonWidget(self, self.config)
        self.clear_button.initWidget()
        self.layout.addWidget(self.clear_button)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdDownloadNew(NchantdWidget):
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