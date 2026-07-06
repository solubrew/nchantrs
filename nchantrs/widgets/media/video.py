# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""#																			||
---  #																			||
<(META)>:  #																	||
        DOCid:   #																	||
        name:   #																	||
        description: >  #															||
                  #			||
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
from os.path import abspath, dirname, exists, join

# ===============================================================================||
from kahndor import kahndor

import logging
from nchantrs.libraries import pyqt

logger = logging.getLogger(__name__)
from nchantrs.widgets.widgets import NchantdWidget
from kahndor.logma import Logma

# ===============================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ===============================================================================||
pxcfg = join(here, "_data_", "video.yaml")


class NchantdVideo(NchantdWidget):
    """ """

    def __init__(self, parent=None, cfg={}):
        """'"""
        self.config = kahndor.Instruct(pxcfg).select("NchantdVideo").override(cfg)
        super().__init__(parent, self.config)

    def initModel(self, path=None):
        """ """
        return self

    def initView(self):
        """ """
        self.player = pyqt.QMediaPlayer(None, pyqt.QMediaPlayer.VideoSurface)
        self.video = pyqt.QVideoWidget()
        self.audio_output = QAudioOutput()

        self.audio_devices = pyqt.QAudioDeviceInfo.availableDevices(pyqt.QAudio.Mode())
        device = self.audio_devices[0]

        self.player.setVideoOutput(self.video)
        self.player.setSource(QUrl.fromLocalFile(self.file_path))
        self.player.setAudioOutput(self.audioOutput)
        self.player.audioOutput().setVolume(50)
        self.player.audioOutput().setMuted(False)

    def play_video(self):
        self.mediaPlayer.play()
        return self

    def initWidget(self, path=None):
        """ """
        self.initModel(path)
        self.initView()
        return self


class NchantdVideoPlayer(NchantdVideo):
    """add controls etc to vidoe player"""

    def __init__(self):
        """"""

    def initModel(self, path=None):
        """ """
        super().initModel(path)
        return self

    def initView(self):
        """ """
        super().initView()
        return self

    def initWidget(self, path):
        """ """
        self.initModel(path)
        self.initView()
        return self


class NchantdScreenCapture(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("Nchantd")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)

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


class NchantdDualVideoPlayer(NchantdWidget):
    """A Widget that allows for watching two videos side by side"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdDualVideoPlayer")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)

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


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
