from typing import Any, Optional, Tuple, Union

'\n---\n<(META)>:\n        docid:\n        name:\n        description: >\n                NchantdColor — nchantrs-native color device, drop-in for\n                PyfficeColor. Lives in nchantrs so the framework does not\n                depend on pyffice (pyffice is a downstream consumer concern).\n        version: 0.0.1.0.1.0\n        authority: document|this\n        security: seclvl2\n        <(WT)>: -32\n'
import colorsys  # noqa: E402
from collections import OrderedDict  # noqa: E402
from os.path import abspath, dirname, join  # noqa: E402

from kahndor import kahndor  # noqa: E402
from kahndor.logma import Logma  # noqa: E402
from matplotlib.colors import CSS4_COLORS  # noqa: E402

here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(abspath(here), '_data_', 'themes.yaml')

def _xyz_to_rgb_pure(xyz) -> Union[Any, Tuple[int, int, int]]:
    """Convert CIE XYZ to sRGB (0-255) using the standard sRGB matrix.

    Pure-stdlib replacement for colormath's XYZColor.convert_srgb. The
    inverse D65 Bradford transform is intentionally avoided here — the
    embedded sRGB matrix is the canonical path and matches what callers
    expect from a color picker.
    """
    x, y, z = xyz
    r_lin = 3.2406 * x - 1.5372 * y - 0.4986 * z
    g_lin = -0.9689 * x + 1.8758 * y + 0.0415 * z
    b_lin = 0.0557 * x - 0.204 * y + 1.057 * z

    def _to_srgb(c) -> Any:
        if c <= 0.0031308:
            return 12.92 * c
        return 1.055 * c ** (1.0 / 2.4) - 0.055
    r, g, b = (_to_srgb(max(0.0, min(1.0, c))) for c in (r_lin, g_lin, b_lin))
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)))

def _xyz_to_lab_pure(xyz) -> Union[Any, Tuple[Any, Any, Any]]:
    """Convert CIE XYZ to CIELAB using the standard D65 reference white.

    Pure-stdlib replacement for colormath. Reference white is X=0.95047,
    Y=1.00000, Z=1.08883 (D65 / 2° observer).
    """
    x, y, z = xyz
    x_n, y_n, z_n = (0.95047, 1.0, 1.08883)

    def _f(t) -> Any:
        if t > 0.008856:
            return t ** (1.0 / 3.0)
        return 7.787 * t + 16.0 / 116.0
    fx = _f(x / x_n)
    fy = _f(y / y_n)
    fz = _f(z / z_n)
    l = 116.0 * fy - 16.0  # noqa: E741  # L* in CIELAB
    a = 500.0 * (fx - fy)
    b = 200.0 * (fy - fz)
    return (l, a, b)

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
    VERSION = '0.0.1.0.1.0'

    def __init__(self, cfg=None) -> None:
        """
        Initialize the NchantdColor object.

        Args:
            cfg (dict, optional): Configuration object. May contain a
                ``unit`` dict with ``color`` and ``style`` keys used by
                ``load_unit()``.
        """
        self.config = kahndor.Instruct(pxcfg).select('NchantdColor').override(cfg)
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
        self.color_name = self.config.dikt.get('color_name', None)
        logma.info('NchantdColor initialized')

    def calculate_complementary_color(self) -> Tuple[Any, Any, Any]:
        """
        Calculate the opposite (or complementary) color by inverting the RGB components.

        Returns:
            Tuple containing the RGB of the opposite color.
        """
        r, g, b = self.get_rgb()
        return (255 - r, 255 - g, 255 - b)

    def calculate_text_color(self) -> Union[Any, str]:
        """
        Determine whether text should be black or white based on the
        luminance of the background color (per W3C formula).

        Returns:
            "black" or "white" depending on contrast requirements.
        """
        rgb = self.get_rgb()
        if rgb is None:
            return 'black'
        r, g, b = rgb
        luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
        return 'black' if luminance > 128 else 'white'

    def get_cmyk(self) -> Any:
        """Return the color in CMYK format."""
        self.cmyk = self.rgb_to_cmyk(self.get_rgb())
        return self.cmyk

    def get_hex(self) -> Any:
        """Return the color in HEX format."""
        self.hex = self.rgb_to_hex(self.get_rgb())
        return self.hex

    def get_hls(self) -> Any:
        """Return the color in HLS format."""
        return self.hls

    def get_hsl(self) -> Any:
        """Return the color in HSL format."""
        self.hsl = self.rgb_to_hsl(self.get_rgb())
        return self.hsl

    def get_hsv(self) -> Any:
        """Return the color in HSV format."""
        self.hsv = colorsys.rgb_to_hsv(*[v / 255.0 for v in self.get_rgb()])
        return self.hsv

    def get_lab(self) -> Any:
        """Return the color in LAB format."""
        self.get_xyz()
        self.lab = self.xyz_to_lab(self.xyz)
        return self.lab

    def get_lch(self) -> Any:
        """Return the color in LCH format."""
        return self.lch

    def get_lms(self) -> Any:
        """Return the color in LMS format."""
        return self.lms

    def get_rgb(self) -> Any:
        """Return the color in RGB format."""
        return self.rgb

    def get_rgba(self) -> Any:
        """Return the color in RGB format."""
        return self.rgba

    def get_xyz(self) -> Any:
        """Return the color in XYZ format."""
        self.xyz = self.rgb_to_xyz(self.get_rgb())
        return self.xyz

    def get_yiq(self) -> Any:
        """Return the color in YIQ format."""
        return self.yiq

    def load_unit(self, unit=None) -> Any:
        """
        Load a unit dict into this color object.

        Args:
            unit: dict with ``color`` and ``style`` keys. If None, falls
                back to ``self.config.dikt['unit']``.

        Returns:
            Self for chaining.
        """
        if unit is None:
            unit = self.config.dikt.get('unit', {})
        self.set_color(unit.get('color', 'black'), unit.get('style', 'name'))
        return self
    _COLOR_FORMATS = OrderedDict([('rgb', 'set_rgb'), ('rgba', 'set_rgba'), ('hex', 'set_hex'), ('name', 'set_color_name'), ('hsv', 'set_hsv'), ('hsl', 'set_hsl'), ('cmyk', 'set_cmyk'), ('yiq', 'set_yiq'), ('xyz', 'set_xyz'), ('lab', 'set_lab'), ('lms', 'set_lms')])

    def set_color(self, color, style) -> None:
        """
        Set the initial color based on the provided style.

        Args:
            color (str | tuple): The color value (e.g., HEX string or RGB tuple).
            style (str): The format of the color (e.g., "rgb", "hex", etc.).
        """
        method_name = self._COLOR_FORMATS.get(style)
        if method_name is None:
            raise ValueError(f'Unsupported color style: {style}')
        getattr(self, method_name)(color)

    def set_cmyk(self, value) -> None:
        """
        Set the CMYK value.

        Args:
            value (tuple): CMYK tuple (C, M, Y, K), values between 0-1.
        """
        self.cmyk = value
        self.set_rgb(self.cmyk_to_rgb(value))

    def set_hex(self, value) -> None:
        """
        Set the HEX value and update other formats.

        Args:
            value (str): HEX color string (e.g., "#FFFFFF").
        """
        self.hex = value
        self.set_rgb(self.hex_to_rgb(value))

    def set_hsl(self, value) -> None:
        """Set the hsl and update derived formats.

        Args:
            value: HSL tuple.
        """
        self.hsl = value
        self.set_rgb(self.hsl_to_rgb(value))
        self.set_hex(self.rgb_to_hex(self.get_rgb()))

    def set_hsv(self, value) -> None:
        """
        Set the HSV value and update other formats.

        Args:
            value (tuple): HSV tuple (H, S, V) with values in appropriate ranges.
        """
        self.hsv = value
        self.set_rgb(self.hsv_to_rgb(value))

    def set_lab(self, value) -> None:
        """
        Set the LAB value and update other formats.

        Args:
            value (tuple): LAB tuple (L, A, B).
        """
        self.lab = value
        xyz_color = self.lab_to_xyz(value)
        self.set_xyz(xyz_color)

    def set_lms(self, value) -> None:
        """
        Set the LMS value.

        Args:
            value (tuple): LMS tuple.
        """
        self.lms = value

    def set_color_name(self, value) -> Any:
        """Set the color name and resolve via CSS4_COLORS if known.

        Args:
            value: Color name (e.g., "red", "midnightblue").

        Returns:
            Self for chaining.
        """
        self.color_name = value
        if self.color_name in CSS4_COLORS:
            self.set_hex(CSS4_COLORS[self.color_name])
        return self

    def set_rgb(self, value) -> Any:
        """
        Set the RGB value.

        Args:
            value (tuple): RGB tuple (R, G, B) with values in range [0, 255].
        """
        self.rgb = value
        return self

    def set_rgba(self, value) -> Any:
        """
        Set the RGBA value.

        Args:
            value (tuple): RGBA tuple (R, G, B, A) with values in range [0, 255].
        """
        self.rgba = value
        return self

    def set_xyz(self, value) -> None:
        """
        Set the XYZ color value.

        Args:
            value (tuple): XYZ tuple.
        """
        self.xyz = value
        rgb_color = self.xyz_to_rgb(value)
        self.set_rgb(rgb_color)

    def set_yiq(self, value) -> None:
        """
        Set the YIQ value and update other formats.

        Args:
            value (tuple): YIQ tuple.
        """
        self.yiq = value
        self.set_rgb(self.yiq_to_rgb(value))

    @staticmethod
    def rgb_to_cmyk(rgb) -> Tuple[int, int, int]:
        """Convert RGB (0-255) to CMYK (0-1)."""
        r, g, b = [v / 255.0 for v in rgb]
        k = 1 - max(r, g, b)
        if k == 1:
            return (0, 0, 0, 1)
        c = (1 - r - k) / (1 - k)
        m = (1 - g - k) / (1 - k)
        y = (1 - b - k) / (1 - k)
        return (round(c, 4), round(m, 4), round(y, 4), round(k, 4))

    @staticmethod
    def rgb_to_hex(rgb) -> Optional[str]:
        """Convert RGB (0-255) to HEX string (e.g. '#FF8800')."""
        if rgb is None:
            return None
        return '#{:02X}{:02X}{:02X}'.format(*rgb)

    @staticmethod
    def hex_to_rgb(hex_color) -> Tuple:
        """Convert a HEX color string to an RGB tuple (0-255 per channel)."""
        hex_color = hex_color.lstrip('#')
        return tuple((int(hex_color[i:i + 2], 16) for i in (0, 2, 4)))

    @staticmethod
    def rgb_to_hsl(rgb) -> Any:
        """Convert RGB (0-255) to HSL (h, l, s) on 0-1 scale."""
        return colorsys.rgb_to_hls(*[v / 255.0 for v in rgb])

    @staticmethod
    def hsl_to_rgb(h, s, lightness) -> Union[Any, Tuple[int, int, int]]:  # noqa: E741
        """
        Convert HSL to RGB.

        Args:
            h (float): Hue (0-1 range).
            s (float): Saturation (0-1 range).
            lightness (float): Lightness (0-1 range).

        Returns:
            tuple: RGB values (0-255 scale).
        """

        def hue_to_rgb(p, q, t) -> Any:
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
            r = g = b = lightness
        else:
            q = lightness * (1 + s) if lightness < 0.5 else lightness + s - lightness * s
            p = 2 * lightness - q
            r = hue_to_rgb(p, q, h + 1 / 3)
            g = hue_to_rgb(p, q, h)
            b = hue_to_rgb(p, q, h - 1 / 3)
        return (round(r * 255), round(g * 255), round(b * 255))

    @staticmethod
    def hsv_to_rgb(hsv) -> Tuple[int, int, int]:
        """Convert HSV (0-1) to RGB (0-255)."""
        r, g, b = colorsys.hsv_to_rgb(*hsv)
        return (int(r * 255), int(g * 255), int(b * 255))

    @staticmethod
    def rgb_to_xyz(rgb) -> Union[Any, Tuple[Any, Any, Any]]:
        """Convert sRGB (0-255) to CIE XYZ (D65)."""

        def _to_linear(c) -> Any:
            c = c / 255.0
            if c <= 0.04045:
                return c / 12.92
            return ((c + 0.055) / 1.055) ** 2.4
        r, g, b = (_to_linear(c) for c in rgb)
        x = 0.4124 * r + 0.3576 * g + 0.1805 * b
        y = 0.2126 * r + 0.7152 * g + 0.0722 * b
        z = 0.0193 * r + 0.1192 * g + 0.9505 * b
        return (x, y, z)

    @staticmethod
    def xyz_to_lab(xyz) -> Any:
        """Convert CIE XYZ (D65) to CIELAB."""
        return _xyz_to_lab_pure(xyz)

    @staticmethod
    def xyz_to_rgb(xyz) -> Any:
        """Convert CIE XYZ (D65) to sRGB (0-255)."""
        return _xyz_to_rgb_pure(xyz)

    @staticmethod
    def lab_to_xyz(lab) -> Union[Any, Tuple[Any, Any, Any]]:
        """Convert CIELAB to CIE XYZ (D65)."""
        l, a, b = lab  # noqa: E741  # L*, a*, b* in CIELAB
        fy = (l + 16.0) / 116.0  # noqa: E741
        fx = a / 500.0 + fy
        fz = fy - b / 200.0

        def _finv(t) -> Any:
            t3 = t ** 3
            if t3 > 0.008856:
                return t3
            return (t - 16.0 / 116.0) / 7.787
        x = 0.95047 * _finv(fx)
        y = 1.0 * _finv(fy)
        z = 1.08883 * _finv(fz)
        return (x, y, z)
