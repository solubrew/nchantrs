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

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class NchantdColor(object):
    """
    NchantdColor provides utilities for working with various color formats.

    Supported formats:
    - RGB (Red-Green-Blue)
    - HEX (Hexadecimal notation for colors)
    - RGBA (RGB with Alpha/Transparency Channel)
    - HSV (Hue-Saturation-Value)
    - HSL (Hue-Saturation-Light)
    - CMYK (Cyan-Magenta-Yellow-Black)
    - YIQ (Luma-Chrominance model for NTSC)
    - HLS (Hue-Light-Saturation)
    - LAB (Color in CIELAB format)
    - LCH (Lightness-Chroma-Hue)
    - XYZ (CIE 1931 Color Space)
    - LMS (Long-Medium-Short cone response)
    """

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """
        Initialize the PyfficeColor object.

        Args:
            color (str | tuple): Initial color input in one of the supported formats.
            style (str): The format of the input color. Default is "rgb".
            cfg (dict, optional): Configuration object.
        """
        self.config = condor.Instruct(pxcfg).select("PyfficeColor").override(cfg)
        self.rgb = None
        self.hex = None
        self.rgba = None
        self.hsv = None
        self.hsl = None
        self.cmyk = None
        self.yiq = None
        self.hls = None
        self.lab = None
        self.lch = None
        self.xyz = None
        self.lms = None
        self.color_name = self.config.dikt.get("color_name", None)  # Optional name for the color

    def calculate_complementary_color(self):
        """
        Calculate the opposite (or complementary) color by inverting the RGB components.

        Args:
            r, g, b: The red, green, and blue components of the original color (0-255).

        Returns:
            Tuple containing the RGB of the opposite color.
        """
        r, g, b = self.get_rgb()
        return (255 - r, 255 - g, 255 - b)

    def calculate_text_color(self):
        """Given the color of this object calculate an appropriate text color to place on top of it.
        Determine whether text should be black or white based on the luminance of the background color.
        Args:
            r, g, b: The red, green, and blue components of the background color (0-255).
        Returns:
            "black" or "white" depending on contrast requirements.
        """
        # Calculate luminance (per W3C formula)
        rgb = self.get_rgb()
        if rgb is None:
            return "black"
        r, g, b = rgb
        luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
        # If luminance is greater than 128, use black text; otherwise, use white text
        return "black" if luminance > 128 else "white"

    def get_cmyk(self):
        """Return the color in CMYK format."""
        self.cmyk = self.rgb_to_cmyk(self.get_rgb())
        return self.cmyk

    def get_hex(self):
        """Return the color in HEX format."""
        self.hex = self.rgb_to_hex(self.get_rgb())
        return self.hex

    def get_hls(self):
        """Return the color in HLS format."""

        return self.hls

    def get_hsl(self):
        """Return the color in HSL format."""
        self.hsl = self.rgb_to_hsl(self.get_rgb())
        return self.hsl

    def get_hsv(self):
        """Return the color in HSV format."""
        self.hsv = colorsys.rgb_to_hsv(*[v / 255.0 for v in self.get_rgb()])
        return self.hsv

    def get_lab(self):
        """Return the color in LAB format."""
        self.get_xyz()
        self.lab = self.xyz_to_lab(self.xyz)
        return self.lab

    def get_lch(self):
        """Return the color in LCH format."""
        return self.lch

    def get_lms(self):
        """Return the color in LMS format."""
        return self.lms

    def get_rgb(self):
        """Return the color in RGB format."""
        return self.rgb

    def get_rgba(self):
        """Return the color in RGB format."""
        return self.rgba

    def get_xyz(self):
        """Return the color in XYZ format."""
        self.xyz = self.rgb_to_xyz(self.get_rgb())
        return self.xyz

    def get_yiq(self):
        """Return the color in YIQ format."""
        return self.yiq

    def load_unit(self, unit=None):
        """"""
        logma.info(f"Load Unit {unit}")
        if unit is None:
            unit = self.config.dikt.get("unit", {})
        # Initialize the color based on the input style
        self.set_color(unit.get("color", "black"), unit.get("style", "name"))
        return self

    def set_color(self, color, style):
        """
        Set the initial color based on the provided style.

        Args:
            color (str | tuple): The color value (e.g., HEX string or RGB tuple).
            style (str): The format of the color (e.g., "rgb", "hex", etc.).
        """
        if style == "rgb":
            self.set_rgb(color)
        elif style == "hex":
            self.set_hex(color)
        elif style == "name":
            self.set_color_name(color)
        elif style == "rgba":
            self.set_rgba(color)
        elif style == "hsv":
            self.set_hsv(color)
        elif style == "hsl":
            self.set_hsl(color)
        elif style == "cmyk":
            self.set_cmyk(color)
        elif style == "yiq":
            self.set_yiq(color)
        elif style == "xyz":
            self.set_xyz(color)
        elif style == "lab":
            self.set_lab(color)
        elif style == "lms":
            self.set_lms(color)
        else:
            raise ValueError(f"Unsupported color style: {style}")

    def set_cmyk(self, value):
        """
        Set the CMYK value.

        Args:
            value (tuple): CMYK tuple (C, M, Y, K), values between 0-1.
        """
        self.cmyk = value
        # Convert to RGB (indirectly updates other formats as well)
        self.set_rgb(self.cmyk_to_rgb(value))

    def set_hex(self, value):
        """
        Set the HEX value and update other formats.

        Args:
            value (str): HEX color string (e.g., "#FFFFFF").
        """
        self.hex = value
        self.set_rgb(self.hex_to_rgb(value))

    def set_hsl(self, value):
        """"""
        self.hsl = value
        self.set_rgb(self.hsl_to_rgb(value))
        self.set_hex(self.rgb_to_hex(self.get_rgb()))

    def set_hsv(self, value):
        """
        Set the HSV value and update other formats.

        Args:
            value (tuple): HSV tuple (H, S, V) with values in appropriate ranges.
        """
        self.hsv = value
        self.set_rgb(self.hsv_to_rgb(value))

    def set_lab(self, value):
        """
        Set the LAB value and update other formats.

        Args:
            value (tuple): LAB tuple (L, A, B).
        """
        self.lab = value
        # Convert LAB → XYZ → RGB
        xyz_color = self.lab_to_xyz(value)
        self.set_xyz(xyz_color)

    def set_lms(self, value):
        """
        Set the LMS value.

        Args:
            value (tuple): LMS tuple.
        """
        self.lms = value
        # LMS is typically derived from XYZ; no direct conversion provided here.

    def set_color_name(self, value):
        """"""
        self.color_name = value
        if self.color_name in CSS4_COLORS:
            self.set_hex(CSS4_COLORS[self.color_name])
        return self

    def set_rgb(self, value):
        """
        Set the RGB value and update other formats.

        Args:
            value (tuple): RGB tuple (R, G, B) with values in range [0, 255].
        """
        self.rgb = value
        return self

    def set_rgba(self, value):
        """
        Set the RGBA value and update other formats.

        Args:
            value (tuple): RGBA tuple (R, G, B, A) with values in range [0, 255].
        """
        self.rgba = value
        return self

    def set_xyz(self, value):
        """
        Set the XYZ color value.

        Args:
            value (tuple): XYZ tuple.
        """
        self.xyz = value
        # Convert to RGB directly
        rgb_color = self.xyz_to_rgb(value)
        self.set_rgb(rgb_color)

    def set_yiq(self, value):
        """
        Set the YIQ value and update other formats.

        Args:
            value (tuple): YIQ tuple.
        """
        self.yiq = value
        # Convert to RGB (YIQ → RGB)
        self.set_rgb(self.yiq_to_rgb(value))

    # ---- Static Conversion Utilities ----

    @staticmethod
    def rgb_to_cmyk(rgb):
        r, g, b = [v / 255.0 for v in rgb]
        k = 1 - max(r, g, b)
        if k == 1:
            return 0, 0, 0, 1
        c = (1 - r - k) / (1 - k)
        m = (1 - g - k) / (1 - k)
        y = (1 - b - k) / (1 - k)
        return round(c, 4), round(m, 4), round(y, 4), round(k, 4)

    @staticmethod
    def rgb_to_hex(rgb):
        if rgb is None:
            return None
        return "#{:02X}{:02X}{:02X}".format(*rgb)

    @staticmethod
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    @staticmethod
    def rgb_to_hsl(rgb):
        return colorsys.rgb_to_hls(*[v / 255.0 for v in rgb])

    @staticmethod
    def hsl_to_rgb(h, s, l):
        """
        Convert HSL to RGB.
        Args:
            h (float): Hue (0-1 range).
            s (float): Saturation (0-1 range).
            l (float): Lightness (0-1 range).
        Returns:
            tuple: RGB values (0-255 scale).
        """

        def hue_to_rgb(p, q, t):
            if t < 0:
                t += 1
            if t > 1:
                t -= 1
            if t < 1 / 6:
                return p + (q - p) * 6 * t
            if t < 1 / 2:
                return q
            if t < 2 / 3:
                return p + (q - p) * (2 / 3 - t) * 6
            return p

        if s == 0:
            # Achromatic color (gray)
            r = g = b = l
        else:
            q = l * (1 + s) if l < 0.5 else l + s - l * s
            p = 2 * l - q
            r = hue_to_rgb(p, q, h + 1 / 3)
            g = hue_to_rgb(p, q, h)
            b = hue_to_rgb(p, q, h - 1 / 3)
        # Convert to 0-255 scale
        return (round(r * 255), round(g * 255), round(b * 255))

    @staticmethod
    def hsv_to_rgb(hsv):
        r, g, b = colorsys.hsv_to_rgb(*hsv)
        return int(r * 255), int(g * 255), int(b * 255)

    @staticmethod
    def xyz_to_lab(xyz):
        xyz_color = XYZColor(*xyz)
        lab_color = convert_color(xyz_color, LabColor)
        return lab_color.lab_l, lab_color.lab_a, lab_color.lab_b

    @staticmethod
    def xyz_to_rgb(xyz):
        # Use colormath to convert XYZ → sRGB
        xyz_color = XYZColor(*xyz)
        srgb_color = convert_color(xyz_color, sRGBColor)
        return tuple(
            int(c * 255)
            for c in (
                srgb_color.clamped_rgb_r,
                srgb_color.clamped_rgb_g,
                srgb_color.clamped_rgb_b,
            )
        )

    def to_dict(self):
        """"""
        doc = {
            "unit": {
                "color_name": self.color_name,
                "hex": self.hex,
                "rgb": self.rgb,
                "rgba": self.rgba,
                "xyz": self.xyz,
            }
        }
        return doc

    def to_html(self):
        """"""
        return self.html


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
