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
from typing import Any, Optional, Dict, List
import logging
logger = logging.getLogger(__name__)
from kahndor import kahndor
from nchantrs.dialogs.colors import NchantdColorSelectSigil
from nchantrs.libraries import pyqt
from nchantrs.utilities.utils import lookup
from kahndor.logma import Logma
from nchantrs.widgets.media.editors.selectors import NchantdComboBox
from nchantrs.widgets.widgets import NchantdWidget, NchantdWidgetMixin
from nchantrs.widgets.controls.buttons import NchantdButton
from nchantrs.widgets.annotations import NchantdLabel
from nchantrs.widgets.controls.advanced_buttons import NchantdSpinBox
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
DEFAULT_GRID_COLUMNS: int = 3
DEFAULT_FONT_SIZE: int = 12
pxcfg = join(here, '_data_', 'button_groups.yaml')

class NchantdButtonGrid(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('Nchantd')
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView({'layout': 'grid'})
        row, col = (0, 0)
        for button in self.config.dikt['buttons']:
            button_widget = NchantdButton(self, button).initWidget()
            self.config.dikt['buttons'][button]['widget'] = button_widget
            self.layout.addWidget(button_widget, row, col)
            col += 1
            if col >= self.config.dikt.get('n_columns', 3):
                col = 0
                row += 1
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdAcceptButtons(NchantdWidget):
    """ """

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdOkButtons')
        if parent:
            self.config.override(self.parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)
        self.ok_button = None
        self.cancel_button = None

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView({'layout': 'horizontal'})
        self.config.override({'buttons': {'ok': lookup(self.app, 'ok')}})
        self.ok_button = NchantdButton(self, self.config.dikt['buttons']['ok'])
        self.ok_button.initWidget()
        self.layout.addWidget(self.ok_button)
        self.config.override({'buttons': {'cancel': lookup(self.app, 'cancel')}})
        self.cancel_button = NchantdButton(self, self.config.dikt['buttons']['cancel'])
        self.cancel_button.initWidget()
        self.layout.addWidget(self.cancel_button)
        if self.config.dikt.get('justify', None) is not None:
            self.layout.setAlignment(self.getAlignment(self.config.dikt.get('justify', '')))
        return self

class NchantdOkButtons(NchantdWidget):
    """ """

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdOkButtons'))
        if parent:
            self.config.override(self.parent.config)
        self.config.override(cfg)
        self.ok_button = None
        self.cancel_button = None

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView({'layout': 'horizontal'})
        self.config.override({'buttons': {'ok': lookup(self.app, 'ok')}})
        logma.info(f"Ok Button {self.config.dikt['buttons']['ok']}")
        self.ok_button = NchantdButton(self, self.config.dikt['buttons']['ok'])
        self.ok_button.initWidget()
        self.layout.addWidget(self.ok_button)
        if self.config.dikt.get('justify', None) is not None:
            self.layout.setAlignment(self.getAlignment(self.config.dikt.get('justify', '')))
        return self

class NchantdSaveButtons(NchantdWidget):
    """ """

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdSaveButtons')
        if parent:
            self.config.override(self.parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)
        self.newbutton = None
        self.savebutton = None

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        layout = pyqt.QHBoxLayout()
        if log:
            logma.info(f'Nchantd Save Buttons {self.config.dikt}')
        self.config.dikt['buttons']['new']['text'] = 'New'
        self.newbutton = NchantdButton(self, self.config.dikt['buttons']['new'])
        self.newbutton.initWidget()
        layout.addWidget(self.newbutton)
        self.config.dikt['buttons']['save']['text'] = 'Save'
        self.savebutton = NchantdButton(self, self.config.dikt['buttons']['save'])
        self.savebutton.initWidget(self.handler)
        layout.addWidget(self.savebutton)
        layout.setAlignment(self.getAlignment(self.config.dikt['justify']))
        self.layout.addLayout(layout)
        return self

    def initWidget(self, handler) -> Any:
        """ """
        self.handler = handler
        self.initModel()
        self.initView()
        return self

class NchantdSubmissionButtons(pyqt.QWidget):
    """A single pane widget with a button set for submitting a form"""

    def __init__(self, parent=None, cfg={}) -> None:
        """ """
        self.config = kahndor.Instruct(pxcfg).override(cfg)
        self.config.select('NchantdSubmissionButtons')
        if parent:
            self.config.override(parent.config)
        self.parent = parent
        pyqt.QWidget.__init__(self)
        self.layout = pyqt.QHBoxLayout()
        if log:
            logger.debug(f'Nchantd Submission Buttons', self.config.dikt)
        self.config.dikt['buttons']['new']['text'] = 'New'
        self.newbutton = NchantdButton(self, self.config.dikt['buttons']['new'])
        self.newbutton.initWidget()
        self.layout.addWidget(self.newbutton)
        self.config.dikt['buttons']['submit']['text'] = 'Submit'
        self.submitbutton = NchantdButton(self, self.config.dikt['buttons']['submit'])
        self.submitbutton.initWidget()
        self.layout.addWidget(self.submitbutton)
        self.config.dikt['buttons']['delete']['text'] = 'Delete'
        self.deletebutton = NchantdButton(self, self.config.dikt['buttons']['delete'])
        self.deletebutton.initWidget()
        self.layout.addWidget(self.deletebutton)
        self.setLayout(self.layout)

    def initWidget(self) -> Any:
        super().initWidget()
        logma.info(f'initWidget {{type(self).__name__}}')
        return self

class NchantdTabSideButtons(NchantdWidget):
    """ """

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdOkButtons')
        if parent:
            self.config.override(self.parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)
        self.centertab_button = None
        self.righttab_button = None

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """
        TODO: make this a checkable group? or maybe switch to a radio button?
        :return:
        """
        super().initView({'layout': 'horizontal'})
        self.config.override({'buttons': {'center_tab': lookup(self.app, 'left_tab_active')}})
        if log:
            logma.info(f"Center Button {self.config.dikt['buttons']['center_tab']}")
        self.centertab_button = NchantdButton(self, self.config.dikt['buttons']['center_tab'])
        self.centertab_button.initWidget()
        self.layout.addWidget(self.centertab_button)
        self.config.override({'buttons': {'right_tab': lookup(self.app, 'right_tab_active')}})
        if log:
            logma.info(f"Center Button {self.config.dikt['buttons']['right_tab']}")
        self.righttab_button = NchantdButton(self, self.config.dikt['buttons']['right_tab'])
        self.righttab_button.initWidget()
        self.layout.addWidget(self.righttab_button)
        self.layout.setAlignment(self.getAlignment(self.config.dikt['justify']))
        return self

class NchantdMathPad(NchantdWidget):
    """ """

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdMathPad')
        if parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> None:
        """"""
        super().initView()
        self.layout = pyqt.QGridLayout()
        self.btn_plus = NchantdButton(self, {'text': '+'}).initWidget()
        self.layout.addWidget(self.btn_plus, 0, 1, 0, 0)
        self.btn_minus = NchantdButton(self, {'text': '-'}).initWidget()
        self.layout.addWidget(self.btn_minus, 0, 2, 0, 0)
        self.btn_equal = NchantdButton(self, {'text': '*'}).initWidget()
        self.layout.addWidget(self.btn_equal, 0, 3, 0, 0)
        self.btn_multiply = NchantdButton(self, {'text': '/'}).initWidget()
        self.layout.addWidget(self.btn_multiply, 0, 4, 0, 0)
        self.btn_divide = NchantdButton(self, {'text': '='}).initWidget()
        self.layout.addWidget(self.btn_divide, 0, 5, 0, 0)
        self.btn_decimal = NchantdButton(self, {'text': '.'}).initWidget()
        self.layout.addWidget(self.btn_decimal, 0, 6, 0, 0)
        self.setLayout(self.layout)

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdNumberPad(pyqt.QWidget):
    """ """

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdNumberPad')
        if parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        pyqt.QWidget.__init__(self)

    def initModel(self) -> None:
        logma.info(f'initModel {{type(self).__name__}}')
        return self

    def initView(self) -> Any:
        """ """
        self.layout = pyqt.QGridLayout()
        self.btn_seven = NchantdButton(self, {'text': '7'}).initWidget()
        self.layout.addWidget(self.btn_seven, 0, 0)
        self.btn_eight = NchantdButton(self, {'text': '8'}).initWidget()
        self.layout.addWidget(self.btn_eight, 0, 1)
        self.btn_nine = NchantdButton(self, {'text': '9'}).initWidget()
        self.layout.addWidget(self.btn_nine, 0, 2)
        self.btn_four = NchantdButton(self, {'text': '4'}).initWidget()
        self.layout.addWidget(self.btn_four, 1, 0)
        self.btn_five = NchantdButton(self, {'text': '5'}).initWidget()
        self.layout.addWidget(self.btn_five, 1, 1)
        self.btn_six = NchantdButton(self, {'text': '6'}).initWidget()
        self.layout.addWidget(self.btn_six, 1, 2)
        self.btn_one = NchantdButton(self, {'text': '1'}).initWidget()
        self.layout.addWidget(self.btn_one, 2, 0)
        self.btn_two = NchantdButton(self, {'text': '2'}).initWidget()
        self.layout.addWidget(self.btn_two, 2, 1)
        self.btn_three = NchantdButton(self, {'text': '3'}).initWidget()
        self.layout.addWidget(self.btn_three, 2, 2)
        self.btn_zero = NchantdButton(self, {'text': '0'}).initWidget()
        self.layout.addWidget(self.btn_zero, 3, 1)
        self.setLayout(self.layout)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdFontConfigBar(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdFontConfigBar'))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.can_highlight = None
        self.editor = None
        self.is_extended = None
        self.show_label = None
        self.font_style = None
        self.font_size = None
        self.font_color = None
        self.highlight_color = None
        self.bold_button = None
        self.italic_button = None
        self.underline_button = None
        logma.info(f'NchantdFontConfigBar initialized')

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        self.can_highlight = self.config.dikt.get('highlight', True)
        self.is_extended = self.config.dikt.get('extend', False)
        self.show_label = self.config.dikt.get('show_label', True)
        self.is_two_rows = self.config.dikt.get('two_rows', False)
        self.editor = self.config.dikt.get('editor', None)
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        if cfg is None:
            cfg = {}
        if self.is_two_rows:
            cfg = {'layout': 'vertical'}
        cfg['size'] = ['auto', 30]
        super().initView(cfg)
        if self.is_two_rows:
            layout = pyqt.QHBoxLayout()
            self.layout.addLayout(layout)
        else:
            layout = self.layout
        if self.show_label:
            cfg = {'text': self.config.dikt.get('label', 'Missing Label')}
            label = NchantdLabel(self, cfg).initWidget()
            self.layout.addWidget(label)
        cfg = {'options': self.get_font_styles(), 'value': self.get_font_style(), 'handler': self.cmd_on_change_style, 'size': ['auto', 'auto']}
        self.font_style = NchantdComboBox(self, cfg).initWidget()
        layout.addWidget(self.font_style)
        cfg = {'handler': self.cmd_on_change_size}
        self.font_size = NchantdSpinBox(self, cfg).initWidget()
        layout.addWidget(self.font_size)
        cfg = {'action': 'set_text_font_color', 'handler': self.cmd_on_change_color}
        self.font_color = NchantdButton(self, cfg).initWidget()
        layout.addWidget(self.font_color)
        if self.can_highlight:
            cfg = {'action': 'set_text_highlight_color', 'handler': self.cmd_on_change_highlight_color}
            self.highlight_color = NchantdButton(self, cfg).initWidget()
            layout.addWidget(self.highlight_color)
        if self.is_extended:
            if self.is_two_rows:
                layout = pyqt.QHBoxLayout()
                self.layout.addLayout(layout)
            else:
                layout = self.layout
            cfg = {'action': 'set_text_bold', 'handler': self.cmd_on_change_bold}
            self.bold_button = NchantdButton(self, cfg).initWidget()
            layout.addWidget(self.bold_button)
            cfg = {'action': 'set_text_italic', 'handler': self.cmd_on_change_italic}
            self.italic_button = NchantdButton(self, cfg).initWidget()
            layout.addWidget(self.italic_button)
            cfg = {'action': 'set_text_underline', 'handler': self.cmd_on_change_underline}
            self.underline_button = NchantdButton(self, cfg).initWidget()
            layout.addWidget(self.underline_button)
            cfg = {'action': 'set_text_strike', 'handler': self.cmd_on_change_strike}
            self.strike_button = NchantdButton(self, cfg).initWidget()
            layout.addWidget(self.strike_button)
            cfg = {'action': 'set_text_superscript', 'handler': self.cmd_on_change_superscript}
            self.superscript_button = NchantdButton(self, cfg).initWidget()
            layout.addWidget(self.superscript_button)
            cfg = {'action': 'set_text_subscript', 'handler': self.cmd_on_change_subscript}
            self.subscript_button = NchantdButton(self, cfg).initWidget()
            layout.addWidget(self.subscript_button)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def cmd_on_change_color(self, event, *args, **kwargs) -> Any:
        """"""
        self.font_color_select_sigil = NchantdColorSelectSigil(self).initWidget()
        self.set_font_color(self.font_color_select_sigil.get_color())
        if self.font_color.isValid():
            format_to_apply = pyqt.QTextCharFormat()
            format_to_apply.setForeground(self.font_color)
            self.editor.apply_format_to_selected_text(format_to_apply)
        return self

    def cmd_on_change_highlight_color(self, event, *args, **kwargs) -> Any:
        """"""
        self.font_highlight_color_sigil = NchantdColorSelectSigil(self).initWidget()
        color = self.font_highlight_color_sigil.get_color()
        if color.isValid():
            format_to_apply = pyqt.QTextCharFormat()
            format_to_apply.setBackground(color)
            self.editor.apply_format_to_selected_text(format_to_apply)
        return self

    def cmd_on_change_background_color(self, event, *args, **kwargs) -> Any:
        """"""
        self.font_background_color_sigil = NchantdColorSelectSigil(self).initWidget()
        color = self.font_background_color_sigil.get_color()
        if color.isValid():
            format_to_apply = pyqt.QTextCharFormat()
            format_to_apply.setBackground(color)
            self.editor.apply_format_to_selected_text(format_to_apply)
        self.set_font_background_color(color)
        return self

    def cmd_on_change_style(self, event, *args, **kwargs) -> Any:
        """"""
        self.editor.setFontFamily(self.font_style.currentText())
        return self

    def cmd_on_change_size(self, event, *args, **kwargs) -> Any:
        """"""
        self.editor.setFontPointSize(self.font_size.value())
        return self

    def cmd_on_change_bold(self, event, *args, **kwargs) -> Any:
        """"""
        if self.editor.is_bold():
            self.editor.setFontWeight(pyqt.QFont.Weight.Normal)
            return self
        self.editor.setFontWeight(pyqt.QFont.Weight.Bold)
        return self

    def cmd_on_change_italic(self, event, *args, **kwargs) -> Any:
        """"""
        if self.editor.is_italic():
            self.editor.setFontItalic(False)
            return self
        self.editor.setFontItalic(True)
        return self

    def cmd_on_change_underline(self, event, *args, **kwargs) -> Any:
        """"""
        if self.editor.is_underlined():
            self.editor.setFontUnderline(False)
            return self
        self.editor.setFontUnderline(True)
        return self

    def cmd_on_change_underline_double(self, event, *args, **kwargs) -> Any:
        logma.info(f'cmd_on_change_underline_double invoked')
        return self

    def cmd_on_change_strike(self, event, *args, **kwargs) -> Any:
        """"""
        cursor = self.editor.textCursor()
        if not cursor.hasSelection():
            return
        fmt = pyqt.QTextCharFormat()
        char_format = cursor.charFormat()
        is_striked = char_format.fontStrikeOut()
        fmt.setFontStrikeOut(not is_striked)
        cursor.mergeCharFormat(fmt)
        return self

    def cmd_on_change_superscript(self, event, *args, **kwargs) -> Any:
        """"""
        self.set_vertical_alignment(pyqt.QTextCharFormat.AlignSuperScript)
        return self

    def cmd_on_change_subscript(self, event, *args, **kwargs) -> Any:
        """"""
        self.set_vertical_alignment(pyqt.QTextCharFormat.AlignSubScript)
        return self

    def get_font_color_selected(self) -> Any:
        """"""
        color = 'Black'
        return color

    def get_font_size_selected(self) -> int:
        """"""
        size = '12'
        return size

    def get_font_style_selected(self) -> Any:
        """"""
        style = 'Arial'
        return style

    def get_font_style_options(self) -> Any:
        """

        :return:
        """
        styles = ['Arial', 'San Serif']
        return styles

    def get_text_background_color_options(self) -> Any:
        """"""
        colors = ['White', 'Black']
        return colors

    def get_text_background_color_selected(self) -> Any:
        """"""
        color = 'White'
        return color

    def get_font_styles(self) -> Any:
        """"""
        fonts = []
        return fonts

    def get_font_style(self) -> Any:
        """"""
        font = 'Arial'
        return font

    def set_font_color(self, color) -> Any:
        """"""
        self.font_color = color
        return self

    def set_font_color_background(self, color) -> Any:
        """"""
        self.font_color_background = color
        return self

    def set_font_color_color(self, color) -> Any:
        """"""
        self.font_color_color = color
        return self

    def set_vertical_alignment(self, alignment) -> Any:
        """"""
        cursor = self.editor.textCursor()
        if not cursor.hasSelection():
            return
        char_format = pyqt.QTextCharFormat()
        current_format = cursor.charFormat()
        if current_format.verticalAlignment() == alignment:
            char_format.setVerticalAlignment(pyqt.QTextCharFormat.AlignNormal)
        else:
            char_format.setVerticalAlignment(alignment)
        cursor.mergeCharFormat(char_format)
        return self

class NchantdBorderConfigBar(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdBorderConfigBar'))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.can_highlight = None
        logma.info(f'NchantdBorderConfigBar initialized')

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        self.can_highlight = self.config.dikt.get('highlight', True)
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        super().initView(cfg)
        cfg = {'text': self.config.dikt.get('label', 'Border Style: ')}
        label = NchantdLabel(self, cfg).initWidget()
        self.layout.addWidget(label)
        cfg = {'options': self.get_border_styles(), 'value': self.get_border_style(), 'handler': self.cmd_on_change_border_style, 'size': ['auto', 'auto']}
        self.border_style = NchantdComboBox(self, cfg).initWidget()
        self.layout.addWidget(self.border_style)
        cfg = {'handler': self.cmd_on_size_change}
        self.border_thickness = NchantdSpinBox(self, cfg).initWidget()
        self.layout.addWidget(self.border_thickness)
        cfg = {'action': 'set_text_font_color', 'handler': self.cmd_on_change_border_color}
        self.border_color = NchantdButton(self, cfg).initWidget()
        self.layout.addWidget(self.border_color)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def cmd_on_change_border_color(self, event, *args, **kwargs) -> Any:
        """"""
        self.border_color_select_sigil = NchantdColorSelectSigil(self).initWidget()
        return self

    def cmd_on_change_border_style(self, event, *args, **kwargs) -> Any:
        logma.info(f'cmd_on_change_border_style invoked')
        return self

    def cmd_on_size_change(self, event, *args, **kwargs) -> Any:
        logma.info(f'cmd_on_size_change invoked')
        return self

    def get_border_styles(self) -> Any:
        """"""
        borders = []
        return borders

    def get_border_style(self) -> Any:
        """"""
        border = 'Arial'
        return border