from typing import Any
'\n---\n<(META)>:\n        docid:\n        name:\n        description: >\n        version: 0.0.0.0.0.0\n        authority: filesystem\n        security: seclvl2\n        <(WT)>: -32\n'
from os.path import abspath, dirname, join
import datetime as dt
from turtle import Screen, Turtle
import logging
logger = logging.getLogger(__name__)
from kahndor import kahndor
from nchantrs.libraries import pyqt
from kahndor.logma import Logma
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', '.yaml')

class NchantdLogoScreen(pyqt.QWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdLogoScreen')
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdLogoScreen, self).__init__()
        self.screen = None
        self.turtle = None

    def initModel(self) -> Any:
        super_method = getattr(super(type(self), self), method_name, None)
        if callable(super_method):
            try:
                super_method()
            except TypeError:
                pass
        logma.info(f'initModel {{type(self).__name__}}')
        return self

    def initView(self) -> Any:
        """"""
        self.screen = Screen()
        self.screen.bgcolor('black')
        self.turtle = Turtle()
        self.turtle.speed(0)
        self.turtle.color('white')
        self.turtle.penup()
        self.turtle.hideturtle()
        self.turtle.goto(x, y)
        self.turtle.pendown()
        self.turtle.circle(radius)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self