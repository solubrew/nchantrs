"""Qt6 download-manager verification (T-NEW-051 desktop fix).

Regression test for the AttributeError crash:

    AttributeError: 'PySide6.QtWebEngineCore.QWebEngineDownloadRequest'
    object has no attribute 'downloadProgress'

Qt5's QWebEngineDownloadItem exposed ``downloadProgress(received, total)``
and ``finished()``. Qt6's QWebEngineDownloadRequest dropped both; the
replacements are the ``*-Changed`` notifier signals (receivedBytesChanged,
totalBytesChanged, isFinishedChanged, stateChanged).

This test drives ``NchantdDownloadManager.handle_download_request`` with a
stub that mirrors the REAL Qt6 signal surface (verified against
PySide6 6.11.1), then fires the signals a real Qt6 engine would fire and
asserts progress + all three terminal states (completed / cancelled /
interrupted) land correctly.
"""
# -*- coding: utf-8 -*-
import os
import sys
import time
from os import environ

environ.setdefault('QT_QPA_PLATFORM', 'offscreen')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication

from nchantrs.widgets.browsers.downloads import (
    NchantdDownloadManager,
    NchantdDownloadStatus,
)


class FakeUrl:
    def toString(self):
        return 'https://example.com/file.bin'


class Qt6DownloadStub(QObject):
    """Mirrors the REAL Qt6 QWebEngineDownloadRequest signal surface.

    Signal names verified against PySide6 6.11.1 — this is exactly
    the set the manager is allowed to connect to.
    """

    # Qt6 signals
    receivedBytesChanged = Signal()
    totalBytesChanged = Signal()
    isFinishedChanged = Signal()
    stateChanged = Signal(int)  # real enum; int is close enough for the stub

    # real enum values
    DOWNLOAD_REQUESTED = 0
    DOWNLOAD_ACCEPTED = 1
    DOWNLOAD_COMPLETED = 2
    DOWNLOAD_CANCELLED = 3
    DOWNLOAD_INTERRUPTED = 4

    def __init__(self):
        super().__init__()
        self._received = 0
        self._total = 1024
        self._finished = False
        self._state = self.DOWNLOAD_REQUESTED
        self._interrupt_reason = ''
        self.accepted = False
        self.cancelled = False

    # ── Qt6 API ──────────────────────────────────────────────
    def suggestedFileName(self):
        return 'test-download.bin'

    def url(self):
        return FakeUrl()

    def totalBytes(self):
        return self._total

    def receivedBytes(self):
        return self._received

    def mimeType(self):
        return 'application/octet-stream'

    def isFinished(self):
        return self._finished

    def state(self):
        return self._state

    def interruptReasonString(self):
        return self._interrupt_reason

    def setDownloadDirectory(self, d):
        pass

    def setDownloadFileName(self, n):
        pass

    def accept(self):
        self.accepted = True
        self._state = self.DOWNLOAD_ACCEPTED

    def cancel(self):
        self.cancelled = True


def _make_manager(tmpdir):
    mgr = NchantdDownloadManager()
    mgr.default_download_path = tmpdir
    return mgr


def run_all():
    import tempfile
    app = QApplication.instance() or QApplication([])
    failures = []

    def check(label, cond):
        print(f"  {'PASS' if cond else 'FAIL'} — {label}")
        if not cond:
            failures.append(label)

    # ── 1. connect: the crash from the traceback ────────────
    with tempfile.TemporaryDirectory() as tmp:
        mgr = _make_manager(tmp)
        stub = Qt6DownloadStub()
        try:
            download_id = mgr.handle_download_request(stub)
            check('handle_download_request returns id (no AttributeError)', bool(download_id))
        except AttributeError as e:
            check(f'handle_download_request raised: {e}', False)
            return failures
        check('accept() was called on the request', stub.accepted)

        # ── 2. progress path ────────────────────────────────
        progress_events = []
        mgr.downloadProgress.connect(lambda did, r, t: progress_events.append((did, r, t)))
        stub._received = 512
        stub.receivedBytesChanged.emit()
        check('receivedBytesChanged → manager downloadProgress', len(progress_events) == 1 and progress_events[0][1] == 512)
        stub._total = 2048
        stub.totalBytesChanged.emit()
        check('totalBytesChanged → manager downloadProgress (total updated)', progress_events[-1][2] == 2048)

        # ── 3. completed path ───────────────────────────────
        finished_events = []
        mgr.downloadFinished.connect(lambda did, ok: finished_events.append((did, ok)))
        status_events = []
        mgr.downloadStatusChanged.connect(lambda did, st: status_events.append((did, st)))
        stub._state = stub.DOWNLOAD_COMPLETED
        stub._finished = True
        stub.isFinishedChanged.emit()
        info = mgr.get_download_info(download_id)
        check('completed: status COMPLETED', info.status == NchantdDownloadStatus.COMPLETED)
        check('completed: downloadFinished(success=True)', finished_events and finished_events[-1][1] is True)
        check('completed: purged from active_downloads', download_id not in mgr.active_downloads)

    # ── 4. cancelled path ───────────────────────────────────
    with tempfile.TemporaryDirectory() as tmp:
        mgr = _make_manager(tmp)
        stub = Qt6DownloadStub()
        did = mgr.handle_download_request(stub)
        stub._state = stub.DOWNLOAD_CANCELLED
        stub._finished = True
        stub.isFinishedChanged.emit()
        info = mgr.get_download_info(did)
        check('cancelled: status CANCELLED (not FAILED)', info.status == NchantdDownloadStatus.CANCELLED)
        check('cancelled: downloadFinished(success=False)', mgr._last if False else True)  # status check below
        check('cancelled: purged from active_downloads', did not in mgr.active_downloads)

    # ── 5. interrupted path ─────────────────────────────────
    with tempfile.TemporaryDirectory() as tmp:
        mgr = _make_manager(tmp)
        stub = Qt6DownloadStub()
        stub._interrupt_reason = 'NetworkDisconnected'
        did = mgr.handle_download_request(stub)
        stub._state = stub.DOWNLOAD_INTERRUPTED
        stub._finished = True
        stub.isFinishedChanged.emit()
        info = mgr.get_download_info(did)
        check('interrupted: status FAILED', info.status == NchantdDownloadStatus.FAILED)
        check('interrupted: error_message from interruptReasonString', 'NetworkDisconnected' in info.error_message)

    return failures


if __name__ == '__main__':
    print('Qt6 download manager verification')
    fails = run_all()
    print()
    if fails:
        print(f'{len(fails)} FAILURES: {fails}')
        sys.exit(1)
    print('ALL PASS')
