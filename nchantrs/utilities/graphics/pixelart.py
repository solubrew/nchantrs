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
import datetime as dt
import numpy as np

import logging

logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||
from PIL import Image, ImageDraw, ImageFont
import random

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "pixelart.yaml")


class PixelArtGenerator:
    """"""

    def __init__(self, cfg=None):
        """"""
        self.config = kahndor.Instruct(pxcfg).select("").override(cfg)
        self.x_dim = 50
        self.y_dim = 50
        self.image = None
        self.palette = None
        self.border = None

    def create_palette(self, colors=None):
        """"""
        if colors is None:
            self.create_random_palette()

    def create_random_palette(self, blank=False, min_color=0, max_color=255):
        """"""
        random_ = lambda: random.randint(min_color, max_color)
        random_color = lambda: (random_(), random_(), random_())
        self.palette = [random_color(), random_color(), random_color(), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        return self.palette

    def generate_random_image(self, blank=False, min_color=0, max_color=255):
        """"""
        color_range_low = min_color
        color_range_high = min_color if blank else max_color
        self.pixels = np.random.randint(low=color_range_low, high=color_range_high, size=(self.x_dim, self.y_dim))
        self.image = Image.fromarray(self.pixels)
        return self

    def generate_restricted_palette_random_image(self):
        """"""
        matrix = [[random.choice(self.palette) for j in range(self.y_dim)] for i in range(self.x_dim)]
        self.pixels = np.array(matrix, dtype=np.uint8)
        self.image = Image.fromarray(self.pixels)
        return self

    def save(self):
        """"""
        today = dt.datetime.now().strftime("%Y%m%d%H%M%S")
        path = f"/home/solubrew/Downloads/{today}.png"
        self.image.save(path)


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
