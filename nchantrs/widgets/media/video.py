from typing import Any
'#\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n---  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n<(META)>:  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        DOCid:   #\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        name:   #\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        description: >  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n                  #\t\t\t||\n        expirary: <[expiration]>  #\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        version: <[version]>  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        path: <[LEXIvrs]>  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        outline: <[outline]>  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        authority: document|this  #\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        security: sec|lvl2  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        <(WT)>: -32  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n'
from os.path import abspath, dirname, exists, join
from kahndor import kahndor
import logging
from nchantrs.libraries import pyqt
logger = logging.getLogger(__name__)
from nchantrs.widgets.widgets import NchantdWidget
from kahndor.logma import Logma
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', 'video.yaml')

class NchantdVideo(NchantdWidget):
    """ """

    def __init__(self, parent=None, cfg={}) -> None:
        """'"""
        self.config = kahndor.Instruct(pxcfg).select('NchantdVideo').override(cfg)
        super().__init__(parent, self.config)
        logma.info(f'NchantdVideo initialized')

    def initModel(self, path=None) -> Any:
        super().initModel()
        logma.info(f'initModel {{type(self).__name__}}')
        return self

    def initView(self) -> None:
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

    def play_video(self) -> Any:
        self.mediaPlayer.play()
        return self

    def initWidget(self, path=None) -> Any:
        """ """
        self.initModel(path)
        self.initView()
        return self

class NchantdVideoPlayer(NchantdVideo):
    """add controls etc to vidoe player"""

    def __init__(self) -> None:
        """"""

    def initModel(self, path=None) -> Any:
        """ """
        super().initModel(path)
        return self

    def initView(self) -> Any:
        """ """
        super().initView()
        return self

    def initWidget(self, path) -> Any:
        """ """
        self.initModel(path)
        self.initView()
        return self

class NchantdScreenCapture(NchantdWidget):
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

class NchantdDualVideoPlayer(NchantdWidget):
    """A Widget that allows for watching two videos side by side"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdDualVideoPlayer')
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