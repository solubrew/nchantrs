# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
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
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, join
import datetime as dt
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), '')  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, '_data_', '.yaml')

# Default keyboard modifier states (to be set by event handlers)
ctrl: bool = False
shift: bool = False
alt: bool = False
# Default action object (to be set by event handlers)
action = None

def on_backspace_press():
	"""Action to take upon event of Backspace key press"""
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  pass
	return

def on_backspace_release():
	"""Action to take upon event of Backspace key release"""
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  pass
	return

def on_clickleft_release(fx):
	""" """
	return

def on_clickright_release(fx):
	""" """
	return

def on_delete_press():
	"""Action to take upon event of Delete key press"""
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  pass
	return

def on_delete_release():
	"""Action to take upon event of Delete key release"""
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  pass
	return

def on_downarrow_press():
	"""Action to take upon event of Down Arrow key press"""
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  pass
	return

def on_downarrow_release():
	"""Action to take upon event of Down Arrow key release"""
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  pass
	return

def on_end_press():
	"""Action to take upon event of End key press"""
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  pass
	return

def on_end_release():
	"""Action to take upon event of End key release"""
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  pass
	return

def on_enter_press():
	"""Action to take upon event of Enter key press"""
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  pass
	return

def on_enter_release():
	"""Action to take upon event of Enter key release"""
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  pass
	return

def on_escape_press():
	"""Action to take upon event of Escape key press"""
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  pass
	return

def on_escape_release():
	"""Action to take upon event of Escape key release"""
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  pass
	return

def on_focus():
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  pass
	return

def on_home_press():
	"""Action to take upon event of Home key press"""
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  pass
	return

def on_home_release():
	"""Action to take upon event of Home key release"""
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  pass
	return

def on_key_press():
	"""Action to take upon event of key press"""
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  pass
	return

def on_key_release():
	"""Action to take upon event of key release"""
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  pass
	return

def on_leftarrow_press():
	"""Action to take upon event of Left Arrow key press"""
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  pass
	return

def on_leftarrow_release():
	"""Action to take upon event of Left Arrow key release"""
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  pass
	return
def on_letter_a_press():
	"""Action to take upon event of Letter a key press"""
	if ctrl == True:
		action.selectall()
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_a_release():
	"""Action to take upon event of Letter a key release"""
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_b_press():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_b_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_c_press():
	""" """
	if ctrl == True:
		action.copy()
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_c_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_d_press():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_d_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_e_press():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_e_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_f_press():
	""" """
	if ctrl == True:
		action.find()
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_f_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_g_press():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_g_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_h_press():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_h_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_i_press():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_i_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_j_press():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_j_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_k_press():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_k_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_l_press():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_l_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_m_press():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_m_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_n_press():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_n_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_o_press():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_o_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_p_press():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_p_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_q_press():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_q_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_r_press():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_r_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_s_press():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_s_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_t_press():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_t_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_u_press():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_u_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_v_press():
	""" """
	if ctrl == True:
		action.paste()
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_v_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_w_press():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_w_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_x_press():
	""" """
	if ctrl == True:
		action.cut()
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_x_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_y_press():
	""" """
	if ctrl == True:
		action.redo()
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_y_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_z_press():
	""" """
	if ctrl == True:
		action.undo()
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_z_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_dash_press():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_dash_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return

def on_letter_equal_press():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_equal_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_leftbracket_press():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_leftbracket_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_rightbracket_press():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_rightbracket_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_semicolon_press():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_semicolon_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_apostrophe_press():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_apostrophe_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_slashback_press():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_slashback_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_comma_press():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_comma_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_period_press():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_period_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_slashforward_press():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_letter_slashforward_release():
	""" """
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		pass
	return
def on_rightarrow_press():
	"""Action to take upon event of Right Arrow key press"""
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  pass
	return
def on_rightarrow_release():
	"""Action to take upon event of Right Arrow key release"""
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  pass
	return
def on_spacebar_press():
	"""Action to take upon event of Spacebar key press"""
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  pass
	return
def on_spacebar_release():
	"""Action to take upon event of Spacebar key release"""
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  pass
	return
def on_tab_press():
	"""Action to take upon event of key press"""
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  pass
	return
def on_tab_release():
	"""Action to take upon event of key release"""
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  pass
	return
def on_uparrow_press():
	"""Action to take upon event of key press"""
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  pass
	return
def on_uparrow_release():
	"""Action to take upon event of key release"""
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  pass
	return


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
