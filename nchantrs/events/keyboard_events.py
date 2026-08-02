"""
---
<(META)>:
        docid:
        name:
        description: >
                        Connect various user inputs to test_nchantrs actions based on context and
                focus
        version: 0.0.0.0.0.0
        authority: filesystem
        security: seclvl2
        <(WT)>: -32
"""
from os.path import abspath, dirname, join
import datetime as dt
import logging
logger = logging.getLogger(__name__)
from kahndor import kahndor
from kahndor.logma import Logma
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', '.yaml')
ctrl: bool = False
shift: bool = False
alt: bool = False
action = None

def on_backspace_press() -> None:
    """Action to take upon event of Backspace key press"""
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_backspace_release() -> None:
    """Action to take upon event of Backspace key release"""
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_clickleft_release(fx) -> None:
    logma.info(f'on_clickleft_release event received')
    if getattr(self, 'app', None) is not None and hasattr(self.app, 'model'):
        self.app.model.has_changed = True
    return self

def on_clickright_release(fx) -> None:
    logma.info(f'on_clickright_release event received')
    if getattr(self, 'app', None) is not None and hasattr(self.app, 'model'):
        self.app.model.has_changed = True
    return self

def on_delete_press() -> None:
    """Action to take upon event of Delete key press"""
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_delete_release() -> None:
    """Action to take upon event of Delete key release"""
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_downarrow_press() -> None:
    """Action to take upon event of Down Arrow key press"""
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_downarrow_release() -> None:
    """Action to take upon event of Down Arrow key release"""
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_end_press() -> None:
    """Action to take upon event of End key press"""
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_end_release() -> None:
    """Action to take upon event of End key release"""
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_enter_press() -> None:
    """Action to take upon event of Enter key press"""
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_enter_release() -> None:
    """Action to take upon event of Enter key release"""
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_escape_press() -> None:
    """Action to take upon event of Escape key press"""
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_escape_release() -> None:
    """Action to take upon event of Escape key release"""
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_focus() -> None:
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_home_press() -> None:
    """Action to take upon event of Home key press"""
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_home_release() -> None:
    """Action to take upon event of Home key release"""
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_key_press() -> None:
    """Action to take upon event of key press"""
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_key_release() -> None:
    """Action to take upon event of key release"""
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_leftarrow_press() -> None:
    """Action to take upon event of Left Arrow key press"""
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_leftarrow_release() -> None:
    """Action to take upon event of Left Arrow key release"""
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_a_press() -> None:
    """Action to take upon event of Letter a key press"""
    if ctrl:
        action.selectall()
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_a_release() -> None:
    """Action to take upon event of Letter a key release"""
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_b_press() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_b_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_c_press() -> None:
    """ """
    if ctrl:
        action.copy()
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_c_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_d_press() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_d_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_e_press() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_e_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_f_press() -> None:
    """ """
    if ctrl:
        action.find()
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_f_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_g_press() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_g_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_h_press() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_h_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_i_press() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_i_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_j_press() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_j_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_k_press() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_k_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_l_press() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_l_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_m_press() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_m_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_n_press() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_n_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_o_press() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_o_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_p_press() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_p_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_q_press() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_q_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_r_press() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_r_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_s_press() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_s_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_t_press() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_t_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_u_press() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_u_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_v_press() -> None:
    """ """
    if ctrl:
        action.paste()
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_v_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_w_press() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_w_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_x_press() -> None:
    """ """
    if ctrl:
        action.cut()
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_x_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_y_press() -> None:
    """ """
    if ctrl:
        action.redo()
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_y_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_z_press() -> None:
    """ """
    if ctrl:
        action.undo()
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_z_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_dash_press() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_dash_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_equal_press() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_equal_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_leftbracket_press() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_leftbracket_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_rightbracket_press() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_rightbracket_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_semicolon_press() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_semicolon_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_apostrophe_press() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_apostrophe_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_slashback_press() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_slashback_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_comma_press() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_comma_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_period_press() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_period_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_slashforward_press() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_letter_slashforward_release() -> None:
    """ """
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_rightarrow_press() -> None:
    """Action to take upon event of Right Arrow key press"""
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_rightarrow_release() -> None:
    """Action to take upon event of Right Arrow key release"""
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_spacebar_press() -> None:
    """Action to take upon event of Spacebar key press"""
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_spacebar_release() -> None:
    """Action to take upon event of Spacebar key release"""
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_tab_press() -> None:
    """Action to take upon event of key press"""
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_tab_release() -> None:
    """Action to take upon event of key release"""
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_uparrow_press() -> None:
    """Action to take upon event of key press"""
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return

def on_uparrow_release() -> None:
    """Action to take upon event of key release"""
    if ctrl:
        pass
    elif shift:
        pass
    elif alt:
        pass
    else:
        pass
    return