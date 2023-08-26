#@@@@@@@@@@@@@@@@ Nchantrs.Utils @@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	docid: <^(UUID)^>
	name: Nchantrs Utils Python Execution Document
	description: >
	expirary: <[expiration]>
	version: <[version]>
	path: <[LEXIvrs]>
	outline: <[outline]>
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#==============================Core Modules=====================================||
from os.path import abspath, dirname, exists, join
#===============================================================================||
from condor import condor
from squirl.orgnql import yonql
#===============================================================================||
here = join(dirname(__file__),'')#												||
version = '0.0.0.0.0.0'#														||
#===============================================================================||
pxcfg = f'{here}_data_/utils.yaml'
def lookup(action, cfg=None):
	'''Lookup action with in the action configurations system'''
	pxcfg = f'{here}actions/z-data_/action.yaml'
	cfg = condor.instruct(pxcfg).override(cfg).dikt
	return search(action, cfg)
def search(action, cfg)->dict:
	'''Search dictionary for action recursively moving through tree levels'''
	if not isinstance(action, dict):
		for key, cfg in cfg.items():
			if cfg == None:
				continue
			if 'UUID' in cfg.keys():
				break
			if action in cfg.keys():
				return cfg[action]
	return {'Name': None, 'Description': None, 'UUID': None, 'Icon': None,
					'Shortcut': None, 'Tip': None, 'Fx': None, 'Params': None}
def restore(self, cmd):
	"""modify for nchantrs....Restore the main window state from saved settings."""
	pyqt.QSettings.setDefaultFormat(pyqt.QSettings.IniFormat)
	settings = pyqt.QSettings()
	settings.beginGroup("mainwindow")
	self.dock_widget.setExpanded(settings.value("canvasdock/expanded", True, type=bool))
	floatable = settings.value("toolbox-dock-floatable", False, type=bool)
	if floatable:
		self.dock_widget.setFeatures(self.dock_widget.features() | QDockWidget.DockWidgetFloatable)
	self.widgets_tool_box.setExclusive(settings.value("toolbox-dock-exclusive", True, type=bool))
	self.toogle_margins_action.setChecked(settings.value("scheme-margins-enabled", False, type=bool))
	self.show_log_action.setChecked(settings.value("output-dock/is-visible", False, type=bool))
	self.canvas_tool_dock.setQuickHelpVisible(settings.value("quick-help/visible", True, type=bool))
	self.float_widgets_on_top_action.setChecked(settings.value("widgets-float-on-top", False, type=bool))
#	self.__update_from_settings()
	cmd()

def calcERN(gvn):
	'''Calculate the Extended Roman Numeral Symbol from Arabic Numeral'''
	nsys = condor.instruct(pxcfg).select('calcERN').dikt
	keys = [int(x) for x in nsys['column'].keys()]
	keys.sort()
	ern = ''
	while gvn != 0:
		for val in reversed(keys):
			ngvn = gvn - val
			if ngvn < 0:
				continue
			gvn = ngvn
			ern += nsys['column'][str(val)]
			break
	return ern
'''




from datetime import datetime
import platform
import json
import logging
import os
import requests
import config
try:
	from Orange.version import full_version, release
except ImportError:
	full_version = '???'
	release = True
log = logging.getLogger(__name__)
statistics_path = os.path.join(config.data_dir(), "usage-statistics.json")
server_url = os.getenv('ORANGE_STATISTICS_API_URL', "https://orange.biolab.si/usage-statistics")
class UsageStatistics:
	"""
	Tracks and sends upon close usage statistics when error-reporting/send-statistics is true.
	This option can be changed in the preferences menu.
	Data is anonymously collected by the Bioinformatics Laboratory, University of Ljubljana,
	Faculty of Computer and Information Science.
	Data tracked per canvas session:
		date,
		Orange version,
		operating system,
		node additions by type:
			widget name
			type of addition:
				quick menu
				toolbox click
				toolbox drag
				drag from other widget
			(if dragged from other widget, other widget name)
	"""
	NodeAddClick = 0
	NodeAddDrag = 1
	NodeAddMenu = 2
	NodeAddExtendFromSink = 3
	NodeAddExtendFromSource = 4
	last_search_query = None
	def __init__(self):
		self.toolbox_clicks = []
		self.toolbox_drags = []
		self.quick_menu_actions = []
		self.widget_extensions = []
		self.__node_addition_type = None
	def log_node_added(self, widget_name, extended_widget=None):
		if not config.settings()["error-reporting/send-statistics"]:
			return
		if self.__node_addition_type == UsageStatistics.NodeAddMenu:
			self.quick_menu_actions.append({
				"Widget Name": widget_name,
				"Query": UsageStatistics.last_search_query,
			})
		elif self.__node_addition_type == UsageStatistics.NodeAddClick:
			self.toolbox_clicks.append({
				"Widget Name": widget_name,
			})
		elif self.__node_addition_type == UsageStatistics.NodeAddDrag:
			self.toolbox_drags.append({
				"Widget Name": widget_name,
			})
		elif self.__node_addition_type == UsageStatistics.NodeAddExtendFromSink:
			self.widget_extensions.append({
				"Widget Name": widget_name,
				"Extended Widget": extended_widget,
				"Direction": "FROM_SINK",
				"Query": UsageStatistics.last_search_query,
			})
		elif self.__node_addition_type == UsageStatistics.NodeAddExtendFromSource:
			self.widget_extensions.append({
				"Widget Name": widget_name,
				"Extended Widget": extended_widget,
				"Direction": "FROM_SOURCE",
				"Query": UsageStatistics.last_search_query,
			})
		else:
			log.warning("Invalid usage statistics state; "
						"attempted to log node before setting node type.")
	def set_node_type(self, addition_type):
		self.__node_addition_type = addition_type
	def write_statistics(self):
		if not release:
			log.info("Not sending usage statistics (non-release version of Orange detected).")
			return
		if not config.settings()["error-reporting/send-statistics"]:
			log.info("Not sending usage statistics (preferences setting).")
			return
		statistics = {
			"Date": str(datetime.now().date()),
			"Orange Version": full_version,
			"Operating System": platform.system() + " " + platform.release(),
			"Session": {
				"Quick Menu Search": self.quick_menu_actions,
				"Toolbox Click": self.toolbox_clicks,
				"Toolbox Drag": self.toolbox_drags,
				"Widget Extension": self.widget_extensions
			}
		}
		if os.path.isfile(statistics_path):
			with open(statistics_path) as f:
				data = json.load(f)
		else:
			data = []
		data.append(statistics)
		def store_data(d):
			with open(statistics_path, 'w') as f:
				json.dump(d, f)
		try:
			r = requests.post(server_url, files={'file': json.dumps(data)})
			if r.status_code != 200:
				log.warning("Error communicating with server while attempting to send "
							"usage statistics.")
				store_data(data)
				return
			# success - wipe statistics file
			log.info("Usage statistics sent.")
			with open(statistics_path, 'w') as f:
				json.dump([], f)
		except (ConnectionError, requests.exceptions.RequestException):
			log.warning("Connection error while attempting to send usage statistics.")
			store_data(data)
	@staticmethod
	def set_last_search_query(query):
		UsageStatistics.last_search_query = query







'''




#===========================Code Source Examples================================||
'''

"""Widget Registry cache."""
import os, pickle, logging, config
log = logging.getLogger(__name__)
def registry_cache_filename():
	"""Return the pickled registry cache filename. Also make sure the
	containing directory is created if it does not exists. """
	cache_dir = config.cache_dir()
	cache_filename = os.path.join(cache_dir, "registry-cache.pck")
	dirname = os.path.dirname(cache_filename)
	if not os.path.exists(dirname):
		log.info("Creating directory %r", dirname)
		os.makedirs(dirname)
	return cache_filename
def registry_cache():
	"""Return the registry cache dictionary."""
	filename = registry_cache_filename()
	log.debug("Loading widget registry cache (%r).", filename)
	if os.path.exists(filename):
		try:
			with open(filename, "rb") as f:
				return pickle.load(f)
		except Exception:
			log.error("Could not load registry cache.", exc_info=True)
	return {}
def save_registry_cache(cache):
	"""Save (pickle) the registry cache. Return True on success,
	False otherwise."""
	filename = registry_cache_filename()
	log.debug("Saving widget registry cache with %i entries (%r).",
			  len(cache), filename)
	try:
		with open(filename, "wb") as f:
			pickle.dump(cache, f)
		return True
	except Exception:
		log.error("Could not save registry cache", exc_info=True)
	return False


# -*- coding: UTF-8 -*-
#
#	   support.py
#
#	   Copyright 2009-2015 Giuseppe Penone <giuspen@gmail.com>
#
#	   This program is free software; you can redistribute it and/or modify
#	   it under the terms of the GNU General Public License as published by
#	   the Free Software Foundation; either version 3 of the License, or
#	   (at your option) any later version.
#
#	   This program is distributed in the hope that it will be useful,
#	   but WITHOUT ANY WARRANTY; without even the implied warranty of
#	   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	   GNU General Public License for more details.
#
#	   You should have received a copy of the GNU General Public License
#	   along with this program; if not, write to the Free Software
#	   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#	   MA 02110-1301, USA.
import gtk, pango, locale, os, webbrowser, re
import cons, config
def auto_decode_str(in_str, from_clipboard=False):
	"""Try to Detect Encoding and Decode"""
	if in_str.startswith("\xEF\xBB\xBF"): # UTF-8 "BOM"
		encodings = ["utf-8-sig"]
	elif in_str.startswith(("\xFF\xFE", "\xFE\xFF")): # UTF-16 BOMs
		encodings = [cons.STR_UTF16]
	elif from_clipboard:
		encodings = [cons.STR_UTF8, cons.STR_UTF16]
	else:
		encodings = [cons.STR_UTF8, cons.STR_ISO_8859, cons.STR_UTF16, "utf-16le", locale.getdefaultlocale()[1]]
	for enc in encodings:
		try:
			out_str = in_str.decode(enc)
			print enc
			break
		except: pass
	else:
		out_str = unicode(in_str, cons.STR_UTF8, cons.STR_IGNORE)
	return out_str
def apply_tag_try_automatic_bounds(dad, text_buffer=None, iter_start=None):
	"""Try to Select a Word Forward/Backward the Cursor"""
	if not text_buffer: text_buffer = dad.curr_buffer
	if not iter_start: iter_start = text_buffer.get_iter_at_mark(text_buffer.get_insert())
	iter_end = iter_start.copy()
	curr_char = iter_end.get_char()
	# 1) select alphanumeric + special
	match = re.match('\w', curr_char, re.UNICODE)
	if not match and not curr_char in dad.selword_chars:
		iter_start.backward_char()
		iter_end.backward_char()
		curr_char = iter_end.get_char()
		match = re.match('\w', curr_char, re.UNICODE)
		if not match and not curr_char in dad.selword_chars:
			return False
	while match or curr_char in dad.selword_chars:
		if not iter_end.forward_char(): break # end of buffer
		curr_char = iter_end.get_char()
		match = re.match('\w', curr_char, re.UNICODE)
	iter_start.backward_char()
	curr_char = iter_start.get_char()
	match = re.match('\w', curr_char, re.UNICODE)
	while match or curr_char in dad.selword_chars:
		if not iter_start.backward_char(): break # start of buffer
		curr_char = iter_start.get_char()
		match = re.match('\w', curr_char, re.UNICODE)
	if not match and not curr_char in dad.selword_chars: iter_start.forward_char()
	# 2) remove non alphanumeric from borders
	iter_end.backward_char()
	curr_char = iter_end.get_char()
	while curr_char in dad.selword_chars:
		if not iter_end.backward_char(): break # start of buffer
		curr_char = iter_end.get_char()
	iter_end.forward_char()
	curr_char = iter_start.get_char()
	while curr_char in dad.selword_chars:
		if not iter_start.forward_char(): break # end of buffer
		curr_char = iter_start.get_char()
	if iter_end.compare(iter_start) > 0:
		text_buffer.move_mark(text_buffer.get_insert(), iter_start)
		text_buffer.move_mark(text_buffer.get_selection_bound(), iter_end)
		return True
	return False
def on_sourceview_event_after_double_click_button1(dad, text_view, event):
	"""Called after every Double Click with button 1"""
	text_buffer = text_view.get_buffer()
	x, y = text_view.window_to_buffer_coords(gtk.TEXT_WINDOW_TEXT, int(event.x), int(event.y))
	iter_start = text_view.get_iter_at_location(x, y)
	apply_tag_try_automatic_bounds(dad, text_buffer=text_buffer, iter_start=iter_start)
def on_sourceview_event_after_button_press(dad, text_view, event):
	"""Called after every gtk.gdk.BUTTON_PRESS on the SourceView"""
	text_buffer = text_view.get_buffer()
	if event.button in [1, 2]:
		x, y = text_view.window_to_buffer_coords(gtk.TEXT_WINDOW_TEXT, int(event.x), int(event.y))
		text_iter = text_view.get_iter_at_location(x, y)
		tags = text_iter.get_tags()
		# check whether we are hovering a link
		if not tags: tags = []
		for tag in tags:
			tag_name = tag.get_property("name")
			if tag_name and tag_name[0:4] == cons.TAG_LINK:
				dad.link_clicked(tag_name[5:], event.button == 2)
				return False
		if dad.lists_handler.is_list_todo_beginning(text_iter):
			dad.lists_handler.todo_list_rotate_status(text_iter, text_buffer)
	elif event.button == 3 and not text_buffer.get_has_selection():
		x, y = text_view.window_to_buffer_coords(gtk.TEXT_WINDOW_TEXT, int(event.x), int(event.y))
		text_iter = text_view.get_iter_at_location(x, y)
		text_buffer.place_cursor(text_iter)
	return False
def on_sourceview_list_change_level(dad, iter_insert, list_info, text_buffer, level_increase):
	"""Called at list indent/unindent time"""
	end_offset = dad.lists_handler.get_multiline_list_element_end_offset(iter_insert, list_info)
	curr_offset = list_info["startoffs"]
	curr_level = list_info["level"]
	next_level = curr_level+1 if level_increase else curr_level-1
	iter_start = text_buffer.get_iter_at_offset(curr_offset)
	prev_list_info = dad.lists_handler.get_prev_list_info_on_level(iter_start, next_level)
	#print prev_list_info
	if list_info["num"] != 0:
		bull_offset = curr_offset + 3*list_info["level"]
		if list_info["num"] < 0:
			if prev_list_info != None and prev_list_info["num"] < 0:
				bull_idx = prev_list_info["num"]*(-1) - 1
			else:
				idx_old = list_info["num"]*(-1) - 1
				idx_offset = idx_old - curr_level % cons.NUM_CHARS_LISTBUL
				bull_idx = (next_level + idx_offset) % cons.NUM_CHARS_LISTBUL
			dad.replace_text_at_offset(cons.CHARS_LISTBUL[bull_idx],
				bull_offset, bull_offset+1, text_buffer)
		else:
			idx = list_info["aux"]
			if prev_list_info != None and prev_list_info["num"] > 0:
				this_num = prev_list_info["num"] + 1
				index = prev_list_info["aux"]
			else:
				this_num = 1
				idx_old = list_info["aux"]
				idx_offset = idx_old - curr_level % cons.NUM_CHARS_LISTNUM
				index = (next_level + idx_offset) % cons.NUM_CHARS_LISTNUM
			text_to = str(this_num) + cons.CHARS_LISTNUM[index] + cons.CHAR_SPACE
			dad.replace_text_at_offset(text_to, bull_offset,
				bull_offset+dad.lists_handler.get_leading_chars_num(list_info["num"]), text_buffer)
	iter_start = text_buffer.get_iter_at_offset(curr_offset)
	#print "%s -> %s" % (curr_offset, end_offset)
	while curr_offset < end_offset:
		if level_increase:
			text_buffer.insert(iter_start, 3*cons.CHAR_SPACE)
			end_offset += 3
			iter_start = text_buffer.get_iter_at_offset(curr_offset+3)
		else:
			text_buffer.delete(iter_start, text_buffer.get_iter_at_offset(curr_offset+3))
			end_offset -= 3
			iter_start = text_buffer.get_iter_at_offset(curr_offset+1)
		if not dad.lists_handler.char_iter_forward_to_newline(iter_start) or not iter_start.forward_char():
			break
		curr_offset = iter_start.get_offset()
def on_sourceview_event_after_key_press(dad, text_view, event):
	"""Called after every gtk.gdk.KEY_PRESS on the SourceView"""
	text_buffer = text_view.get_buffer()
	keyname = gtk.gdk.keyval_name(event.keyval)
	if (event.state & gtk.gdk.SHIFT_MASK):
		if keyname == cons.STR_KEY_RETURN:
			iter_insert = text_buffer.get_iter_at_mark(text_buffer.get_insert())
			if not iter_insert: return False
			iter_start = iter_insert.copy()
			iter_start.backward_char()
			list_info = dad.lists_handler.get_paragraph_list_info(iter_start)
			if list_info:
				text_buffer.insert(text_buffer.get_iter_at_mark(text_buffer.get_insert()), 3*(1+list_info["level"])*cons.CHAR_SPACE)
	elif keyname in [cons.STR_KEY_RETURN, cons.STR_KEY_SPACE]:
		iter_insert = text_buffer.get_iter_at_mark(text_buffer.get_insert())
		if not iter_insert: return False
		iter_start = iter_insert.copy()
		if keyname == cons.STR_KEY_RETURN:
			cursor_key_press = iter_insert.get_offset()
			#print "cursor_key_press", cursor_key_press
			if cursor_key_press == dad.cursor_key_press:
				# problem of event-after called twice, once before really executing
				return False
			if not iter_start.backward_char(): return False
			if iter_start.get_char() != cons.CHAR_NEWLINE: return False
			if iter_start.backward_char() and iter_start.get_char() == cons.CHAR_NEWLINE:
				return False # former was an empty row
			list_info = dad.lists_handler.get_paragraph_list_info(iter_start)
			if not list_info:
				if dad.auto_indent:
					iter_start = iter_insert.copy()
					former_line_indent = get_former_line_indentation(iter_start)
					if former_line_indent: text_buffer.insert_at_cursor(former_line_indent)
				return False # former was not a list
			# possible list quit
			insert_offset = iter_insert.get_offset()
			chars_to_startoffs = 1 + dad.lists_handler.get_leading_chars_num(list_info["num"]) + 3*list_info["level"]
			if (insert_offset - list_info["startoffs"]) == chars_to_startoffs:
				iter_list_quit = text_buffer.get_iter_at_offset(list_info["startoffs"])
				text_buffer.delete(iter_list_quit, iter_insert)
				return False # former was an empty paragraph => list quit
			# list new element
			curr_level = list_info["level"]
			pre_spaces = 3*curr_level*cons.CHAR_SPACE if curr_level else ""
			if list_info["num"] < 0:
				index = list_info["num"]*(-1) - 1
				text_buffer.insert(iter_insert, pre_spaces+cons.CHARS_LISTBUL[index]+cons.CHAR_SPACE)
			elif list_info["num"] == 0:
				text_buffer.insert(iter_insert, pre_spaces+cons.CHAR_LISTTODO+cons.CHAR_SPACE)
			else:
				new_num = list_info["num"] + 1
				index = list_info["aux"]
				text_buffer.insert(iter_insert, pre_spaces + str(new_num) + cons.CHARS_LISTNUM[index] + cons.CHAR_SPACE)
				new_num += 1
				iter_start = text_buffer.get_iter_at_offset(insert_offset)
				dad.lists_handler.char_iter_forward_to_newline(iter_start)
				list_info = dad.lists_handler.get_next_list_info_on_level(iter_start, curr_level)
				#print list_info
				while list_info and list_info["num"] > 0:
					iter_start = text_buffer.get_iter_at_offset(list_info["startoffs"])
					end_offset = dad.lists_handler.get_multiline_list_element_end_offset(iter_start, list_info)
					iter_end = text_buffer.get_iter_at_offset(end_offset)
					iter_start, iter_end, chars_rm = dad.lists_handler.list_check_n_remove_old_list_type_leading(iter_start, iter_end, text_buffer)
					end_offset -= chars_rm
					text_buffer.insert(iter_start, str(new_num) + cons.CHARS_LISTNUM[index] + cons.CHAR_SPACE)
					end_offset += dad.lists_handler.get_leading_chars_num(new_num)
					iter_start = text_buffer.get_iter_at_offset(end_offset)
					new_num += 1
					list_info = dad.lists_handler.get_next_list_info_on_level(iter_start, curr_level)
		elif keyname == cons.STR_KEY_SPACE:
			if iter_start.backward_chars(2):
				if iter_start.get_char() == cons.CHAR_GREATER and iter_start.backward_char():
					# Start bulleted list on "<> ", "-> " and "=> " at line start
					if iter_start.get_line_offset() == 0:
						if iter_start.get_char() == cons.CHAR_LESSER:
							dad.special_char_replace(cons.CHARS_LISTBUL[1], iter_start, iter_insert, text_buffer)
						elif iter_start.get_char() == cons.CHAR_MINUS:
							dad.special_char_replace(cons.CHARS_LISTBUL[4], iter_start, iter_insert, text_buffer)
						elif iter_start.get_char() == cons.CHAR_EQUAL:
							dad.special_char_replace(cons.CHARS_LISTBUL[5], iter_start, iter_insert, text_buffer)
					elif iter_start.get_char() == cons.CHAR_MINUS and iter_start.backward_char():
						if iter_start.get_char() == cons.CHAR_LESSER:
							dad.special_char_replace(cons.SPECIAL_CHAR_ARROW_DOUBLE, iter_start, iter_insert, text_buffer)
						elif iter_start.get_char() == cons.CHAR_MINUS:
							dad.special_char_replace(cons.SPECIAL_CHAR_ARROW_RIGHT, iter_start, iter_insert, text_buffer)
				elif iter_start.get_char() == cons.CHAR_MINUS and iter_start.backward_char()\
				and iter_start.get_char() == cons.CHAR_MINUS and iter_start.backward_char()\
				and iter_start.get_char() == cons.CHAR_LESSER:
					dad.special_char_replace(cons.SPECIAL_CHAR_ARROW_LEFT, iter_start, iter_insert, text_buffer)
				elif iter_start.get_char() == cons.CHAR_PARENTH_CLOSE and iter_start.backward_char():
					if iter_start.get_char().lower() == "c" and iter_start.backward_char()\
					and iter_start.get_char() == cons.CHAR_PARENTH_OPEN:
						dad.special_char_replace(cons.SPECIAL_CHAR_COPYRIGHT, iter_start, iter_insert, text_buffer)
					elif iter_start.get_char().lower() == "r" and iter_start.backward_char()\
					and iter_start.get_char() == cons.CHAR_PARENTH_OPEN:
						dad.special_char_replace(cons.SPECIAL_CHAR_REGISTERED_TRADEMARK, iter_start, iter_insert, text_buffer)
					elif iter_start.get_char().lower() == "m" and iter_start.backward_char()\
					and iter_start.get_char() == "t" and iter_start.backward_char()\
					and iter_start.get_char() == cons.CHAR_PARENTH_OPEN:
						dad.special_char_replace(cons.SPECIAL_CHAR_UNREGISTERED_TRADEMARK, iter_start, iter_insert, text_buffer)
				elif iter_start.get_char() == cons.CHAR_STAR and iter_start.get_line_offset() == 0:
					# Start bulleted list on "* " at line start
					dad.special_char_replace(cons.CHARS_LISTBUL[0], iter_start, iter_insert, text_buffer)
				elif iter_start.get_char() == cons.CHAR_SQ_BR_CLOSE and iter_start.backward_char():
					# Start todo list on "[] " at line start
					if iter_start.get_line_offset() == 0 and iter_start.get_char() == cons.CHAR_SQ_BR_OPEN:
						dad.special_char_replace(cons.CHAR_LISTTODO, iter_start, iter_insert, text_buffer)
				elif iter_start.get_char() == cons.CHAR_COLON and iter_start.backward_char():
					# Start todo list on ":: " at line start
					if iter_start.get_line_offset() == 0 and iter_start.get_char() == cons.CHAR_COLON:
						dad.special_char_replace(cons.CHARS_LISTBUL[2], iter_start, iter_insert, text_buffer)
	return False
def sourceview_cursor_and_tooltips_handler(dad, text_view, x, y):
	"""Looks at all tags covering the position (x, y) in the text view,
	   and if one of them is a link, change the cursor to the HAND2 cursor"""
	hovering_link_iter_offset = -1
	text_iter = text_view.get_iter_at_location(x, y)
	if dad.lists_handler.is_list_todo_beginning(text_iter):
		text_view.get_window(gtk.TEXT_WINDOW_TEXT).set_cursor(gtk.gdk.Cursor(gtk.gdk.X_CURSOR))
		text_view.set_tooltip_text(None)
		return
	tags = text_iter.get_tags()
	if not tags: tags = []
	for tag in tags:
		tag_name = tag.get_property("name")
		if tag_name and tag_name[0:4] == cons.TAG_LINK:
			hovering_link_iter_offset = text_iter.get_offset()
			tooltip = dad.sourceview_hovering_link_get_tooltip(tag_name[5:])
			break
	else:
		iter_anchor = text_iter.copy()
		for i in [0, 1]:
			if i == 1: iter_anchor.backward_char()
			anchor = iter_anchor.get_child_anchor()
			if anchor and "pixbuf" in dir(anchor):
				pixbuf_attrs = dir(anchor.pixbuf)
				if "link" in pixbuf_attrs and anchor.pixbuf.link:
					hovering_link_iter_offset = text_iter.get_offset()
					tooltip = dad.sourceview_hovering_link_get_tooltip(anchor.pixbuf.link)
					break
	if dad.hovering_link_iter_offset != hovering_link_iter_offset:
		dad.hovering_link_iter_offset = hovering_link_iter_offset
		#print "link", dad.hovering_link_iter_offset
	if dad.hovering_link_iter_offset >= 0:
		text_view.get_window(gtk.TEXT_WINDOW_TEXT).set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))
		text_view.set_tooltip_text(tooltip)
	else:
		text_view.get_window(gtk.TEXT_WINDOW_TEXT).set_cursor(gtk.gdk.Cursor(gtk.gdk.XTERM))
		text_view.set_tooltip_text(None)
def rich_text_node_modify_codeboxes_font(start_iter, code_font):
	"""Modify Font to CodeBoxes"""
	curr_iter = start_iter.copy()
	while 1:
		anchor = curr_iter.get_child_anchor()
		if anchor and "sourcebuffer" in dir(anchor):
			anchor.sourceview.modify_font(pango.FontDescription(code_font))
		if not curr_iter.forward_char(): break
def rich_text_node_modify_codeboxes_color(start_iter, dad):
	"""Modify Color to CodeBoxes"""
	curr_iter = start_iter.copy()
	while 1:
		anchor = curr_iter.get_child_anchor()
		if anchor and "sourcebuffer" in dir(anchor):
			dad.widget_set_colors(anchor.sourceview, dad.rt_def_fg, dad.rt_def_bg, True)
		if not curr_iter.forward_char(): break
def text_file_rm_emptylines(filepath):
	"""Remove empty lines in a text file"""
	overwrite_needed = False
	fd = open(filepath, 'r')
	file_lines = []
	for file_line in fd:
		if file_line not in ["\r\n", "\n\r", cons.CHAR_NEWLINE]:
			file_lines.append(file_line)
		else: overwrite_needed = True
	fd.close()
	if overwrite_needed:
		print filepath, "empty lines removed"
		fd = open(filepath, 'w')
		fd.writelines(file_lines)
		fd.close()
def get_proper_platform_filepath(filepath_in, is_file):
	"""From Slash to Backslash when needed"""
	filepath_out = filepath_in
	if cons.IS_WIN_OS:
		if cons.CHAR_SLASH in filepath_in:
			filepath_out = filepath_in.replace(cons.CHAR_SLASH, cons.CHAR_BSLASH)
	else:
		if cons.CHAR_BSLASH in filepath_in:
			filepath_out = filepath_in.replace(cons.CHAR_BSLASH, cons.CHAR_SLASH)
	return filepath_out
def clean_from_chars_not_for_filename(filename_in):
	"""Clean a string from chars not good for filename"""
	filename_out = filename_in.replace(cons.CHAR_SLASH, cons.CHAR_MINUS).replace(cons.CHAR_BSLASH, cons.CHAR_MINUS)
	filename_out = filename_out.replace(cons.CHAR_STAR, "").replace(cons.CHAR_QUESTION, "").replace(cons.CHAR_COLON, "")
	filename_out = filename_out.replace(cons.CHAR_LESSER, "").replace(cons.CHAR_GREATER, "")
	filename_out = filename_out.replace(cons.CHAR_PIPE, "").replace(cons.CHAR_DQUOTE, "")
	filename_out = filename_out.replace(cons.CHAR_NEWLINE, "").replace(cons.CHAR_CR, "").strip()
	return filename_out.replace(cons.CHAR_SPACE, cons.CHAR_USCORE)
def get_node_hierarchical_name(dad, tree_iter, separator="--", for_filename=True, root_to_leaf=True):
	"""Get the Node Hierarchical Name"""
	hierarchical_name = dad.treestore[tree_iter][1].strip()
	father_iter = dad.treestore.iter_parent(tree_iter)
	while father_iter:
		if root_to_leaf:
			hierarchical_name = dad.treestore[father_iter][1].strip() + separator + hierarchical_name
		else:
			hierarchical_name = hierarchical_name + separator + dad.treestore[father_iter][1].strip()
		father_iter = dad.treestore.iter_parent(father_iter)
	if for_filename:
		hierarchical_name = clean_from_chars_not_for_filename(hierarchical_name)
		if len(hierarchical_name) > cons.MAX_FILE_NAME_LEN:
			hierarchical_name = hierarchical_name[-cons.MAX_FILE_NAME_LEN:]
	return hierarchical_name
def strip_trailing_spaces(text_buffer):
	"""Remove trailing spaces/tabs"""
	cleaned_lines = 0
	removed_something = True
	while removed_something:
		removed_something = False
		curr_iter = text_buffer.get_start_iter()
		curr_state = 0
		start_offset = 0
		while curr_iter:
			curr_char = curr_iter.get_char()
			if curr_state == 0:
				if curr_char in [cons.CHAR_SPACE, cons.CHAR_TAB]:
					start_offset = curr_iter.get_offset()
					curr_state = 1
			elif curr_state == 1:
				if curr_char == cons.CHAR_NEWLINE:
					text_buffer.delete(text_buffer.get_iter_at_offset(start_offset), curr_iter)
					removed_something = True
					cleaned_lines += 1
					break
				elif not curr_char in [cons.CHAR_SPACE, cons.CHAR_TAB]:
					curr_state = 0
			if not curr_iter.forward_char():
				if curr_state == 1:
					text_buffer.delete(text_buffer.get_iter_at_offset(start_offset), curr_iter)
				break
	return cleaned_lines
def get_next_chars_from_iter_are(iter_start, chars_list):
	"""Returns True if the Given Chars are the next 'num' after iter"""
	for chars in chars_list:
		text_iter = iter_start.copy()
		num = len(chars)
		for i in range(num):
			if text_iter.get_char().encode(cons.STR_UTF8) != chars[i]: break
			if i != num-1 and not text_iter.forward_char(): break
		else: return True
	return False
def get_former_line_indentation(iter_start):
	"""Returns the indentation of the former paragraph or empty string"""
	if not iter_start.backward_chars(2) or iter_start.get_char() == cons.CHAR_NEWLINE: return ""
	buffer_start = False
	while iter_start:
		if iter_start.get_char() == cons.CHAR_NEWLINE: break # we got the previous paragraph start
		elif not iter_start.backward_char():
			buffer_start = True
			break # we reached the buffer start
	if not buffer_start: iter_start.forward_char()
	if iter_start.get_char() == cons.CHAR_SPACE:
		num_spaces = 1
		while iter_start.forward_char() and iter_start.get_char() == cons.CHAR_SPACE:
			num_spaces += 1
		return num_spaces*cons.CHAR_SPACE
	if iter_start.get_char() == cons.CHAR_TAB:
		num_tabs = 1
		while iter_start.forward_char() and iter_start.get_char() == cons.CHAR_TAB:
			num_tabs += 1
		return num_tabs*cons.CHAR_TAB
	return ""
def windows_cmd_prepare_path(filepath):
	"""Prepares a Path to be digested by windows command line"""
	return cons.CHAR_DQUOTE + filepath + cons.CHAR_DQUOTE
def dialog_file_save_as(filename=None, filter_pattern=None, filter_name=None, curr_folder=None, parent=None):
	"""The Save file as dialog, Returns the retrieved filepath or None"""
	chooser = gtk.FileChooserDialog(title=_("Save File as"),
									action=gtk.FILE_CHOOSER_ACTION_SAVE,
									buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_ACCEPT) )
	chooser.set_do_overwrite_confirmation(True)
	if parent != None:
		chooser.set_transient_for(parent)
		chooser.set_property("modal", True)
		chooser.set_property("destroy-with-parent", True)
		chooser.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
	else: chooser.set_position(gtk.WIN_POS_CENTER)
	if curr_folder == None or os.path.isdir(curr_folder) == False:
		chooser.set_current_folder(os.path.expanduser('~'))
	else:
		chooser.set_current_folder(curr_folder)
	if filename != None:
		chooser.set_current_name(filename)
	if filter_pattern != None:
		filter = gtk.FileFilter()
		filter.set_name(filter_name)
		filter.add_pattern(filter_pattern)
		chooser.add_filter(filter)
	if chooser.run() == gtk.RESPONSE_ACCEPT:
		filepath = chooser.get_filename()
		chooser.destroy()
		return unicode(filepath, cons.STR_UTF8, cons.STR_IGNORE) if filepath != None else None
	else:
		chooser.destroy()
		return None
def dialog_file_select(filter_pattern=[], filter_mime=[], filter_name=None, curr_folder=None, parent=None):
	"""The Select file dialog, Returns the retrieved filepath or None"""
	chooser = gtk.FileChooserDialog(title = _("Select File"),
									action=gtk.FILE_CHOOSER_ACTION_OPEN,
									buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_ACCEPT) )
	if parent != None:
		chooser.set_transient_for(parent)
		chooser.set_property("modal", True)
		chooser.set_property("destroy-with-parent", True)
		chooser.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
	else: chooser.set_position(gtk.WIN_POS_CENTER)
	if curr_folder == None or os.path.isdir(curr_folder) == False:
		chooser.set_current_folder(os.path.expanduser('~'))
	else:
		chooser.set_current_folder(curr_folder)
	if filter_pattern or filter_mime:
		filefilter = gtk.FileFilter()
		filefilter.set_name(filter_name)
		for element in filter_pattern:
			filefilter.add_pattern(element)
		for element in filter_mime:
			filefilter.add_mime_type(element)
		chooser.add_filter(filefilter)
	if chooser.run() == gtk.RESPONSE_ACCEPT:
		filepath = chooser.get_filename()
		chooser.destroy()
		return unicode(filepath, cons.STR_UTF8, cons.STR_IGNORE) if filepath != None else None
	else:
		chooser.destroy()
		return None
def dialog_folder_select(curr_folder=None, parent=None):
	"""The Select folder dialog, returns the retrieved folderpath or None"""
	chooser = gtk.FileChooserDialog(title = _("Select Folder"),
									action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
									buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_ACCEPT) )
	if parent != None:
		chooser.set_transient_for(parent)
		chooser.set_property("modal", True)
		chooser.set_property("destroy-with-parent", True)
		chooser.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
	else: chooser.set_position(gtk.WIN_POS_CENTER)
	if curr_folder == None or os.path.isdir(curr_folder) == False:
		chooser.set_current_folder(os.path.expanduser('~'))
	else:
		chooser.set_current_folder(curr_folder)
	if chooser.run() == gtk.RESPONSE_ACCEPT:
		folderpath = chooser.get_filename()
		chooser.destroy()
		return unicode(folderpath, cons.STR_UTF8, cons.STR_IGNORE) if folderpath != None else None
	else:
		chooser.destroy()
		return None
def dialog_question(message, parent=None):
	"""The Question dialog, returns True if the user presses OK"""
	dialog = gtk.MessageDialog(parent=parent,
							   flags=gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
							   type=gtk.MESSAGE_QUESTION,
							   message_format=message)
	dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
	dialog.set_title(_("Question"))
	dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT)
	dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT)
	response = dialog.run()
	dialog.hide()
	return True if response == gtk.RESPONSE_ACCEPT else False
def dialog_info(message, parent):
	"""The Info dialog"""
	dialog = gtk.MessageDialog(parent=parent,
							   flags=gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
							   type=gtk.MESSAGE_INFO,
							   buttons=gtk.BUTTONS_OK,
							   message_format=message)
	dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
	dialog.set_title(_("Info"))
	dialog.run()
	dialog.destroy()
def dialog_info_after_restart(parent=None):
	"""Change Only After Restart"""
	dialog_info(_("This Change will have Effect Only After Restarting CherryTree"), parent)
def dialog_warning(message, parent):
	"""The Warning dialog"""
	dialog = gtk.MessageDialog(parent=parent,
							   flags=gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
							   type=gtk.MESSAGE_WARNING,
							   buttons=gtk.BUTTONS_OK,
							   message_format=message)
	dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
	dialog.set_title(_("Warning"))
	dialog.run()
	dialog.destroy()
def dialog_error(message, parent):
	"""The Error dialog"""
	dialog = gtk.MessageDialog(parent=parent,
							   flags=gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
							   type=gtk.MESSAGE_ERROR,
							   buttons=gtk.BUTTONS_OK,
							   message_format=message)
	dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
	dialog.set_title(_("Error"))
	dialog.run()
	dialog.destroy()
def dialog_about(dad):
	"""Application About Dialog"""
	dialog = gtk.AboutDialog()
	dialog.set_program_name("CherryTree")
	dialog.set_version(cons.VERSION)
	dialog.set_copyright("""Copyright © 2009-2015
Giuseppe Penone <giuspen@gmail.com>""")
	dialog.set_comments(_("A Hierarchical Note Taking Application, featuring Rich Text and Syntax Highlighting"))
	dialog.set_license(_("""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
MA 02110-1301, USA.
"""))
	dialog.set_website("http://www.giuspen.com/cherrytree/")
	dialog.set_authors(["Giuseppe Penone <giuspen@gmail.com>"])
	dialog.set_documenters(["Robert Boudreau <RobtTheB@gmail.com>"])
	dialog.set_artists(["OCAL <http://www.openclipart.org/>", "Zeltak <zeltak@gmail.com>", "Angelo Penone <angelo.penone@gmail.com>"])
	dialog.set_translator_credits(_("Armenian")+" (hy) Seda Stamboltsyan <sedastam@yandex.com>"+cons.CHAR_NEWLINE+
_("Chinese Simplified")+" (zh_CN) Channing Wong <channing.wong@qq.com>"+cons.CHAR_NEWLINE+
_("Czech")+" (cs) Pavel Fric <fripohled@blogspot.com>"+cons.CHAR_NEWLINE+
_("Dutch")+" (nl) Patrick Vijgeboom <pj.vijgeboom@gmail.com>"+cons.CHAR_NEWLINE+
_("French")+" (fr) Klaus Becker <colonius@free.fr>"+cons.CHAR_NEWLINE+
_("German")+" (de) Frank Brungräber <calexu@arcor.de>"+cons.CHAR_NEWLINE+
_("Italian")+" (it) Vincenzo Reale <smart2128@baslug.org>"+cons.CHAR_NEWLINE+
_("Japanese")+" (ja) Piyo <py2@live.jp>"+cons.CHAR_NEWLINE+
_("Polish")+" (pl) Marcin Swierczynski <orneo1212@gmail.com>"+cons.CHAR_NEWLINE+
_("Portuguese Brazil")+" (pt_BR) Vinicius Schmidt <viniciussm@rocketmail.com>"+cons.CHAR_NEWLINE+
_("Russian")+" (ru) Andriy Kovtun <kovtunos@yandex.ru>"+cons.CHAR_NEWLINE+
_("Spanish")+" (es) Daniel MC <i.e.betel@gmail.com>"+cons.CHAR_NEWLINE+
_("Turkish")+" (tr) Ferhat Aydin <ferhataydin44@gmail.com>"+cons.CHAR_NEWLINE+
_("Ukrainian")+" (uk) Andriy Kovtun <kovtunos@yandex.ru>")
	dialog.set_logo(gtk.gdk.pixbuf_new_from_file(os.path.join(cons.GLADE_PATH, "cherrytree.png")))
	dialog.set_title(_("About CherryTree"))
	dialog.set_transient_for(dad.window)
	dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
	dialog.set_modal(True)
	def f_url_hook(dialog, link, user_data):
		webbrowser.open(link)
	gtk.about_dialog_set_url_hook(f_url_hook, None)
	dialog.run()
	dialog.hide()
def dialog_choose_element_in_list(father_win, title, elements_list, column_title, icon_n_label_list=None):
	"""Choose Between Elements in List"""
	class ListParms:
		def __init__(self):
			self.sel_iter = None
	list_parms = ListParms()
	dialog = gtk.Dialog(title=title,
		parent=father_win,
		flags=gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
		buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
				 gtk.STOCK_OK, gtk.RESPONSE_ACCEPT) )
	dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
	dialog.set_default_size(400, 300)
	scrolledwindow = gtk.ScrolledWindow()
	scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
	if not icon_n_label_list: elements_liststore = gtk.ListStore(str)
	else: elements_liststore = gtk.ListStore(str,str,str)
	elements_treeview = gtk.TreeView(elements_liststore)
	elements_renderer_text = gtk.CellRendererText()
	if not icon_n_label_list:
		elements_column = gtk.TreeViewColumn(column_title, elements_renderer_text, text=0)
	else:
		elements_treeview.set_headers_visible(False)
		renderer_pixbuf = gtk.CellRendererPixbuf()
		renderer_text = gtk.CellRendererText()
		elements_column = gtk.TreeViewColumn()
		elements_column.pack_start(renderer_pixbuf, False)
		elements_column.pack_start(renderer_text, True)
		elements_column.set_attributes(renderer_pixbuf, stock_id=1)
		elements_column.set_attributes(renderer_text, text=2)
	elements_treeview.append_column(elements_column)
	elements_treeviewselection = elements_treeview.get_selection()
	if not icon_n_label_list:
		for element_name in elements_list:
			elements_liststore.append(element_name)
	else:
		for element in icon_n_label_list:
			elements_liststore.append([element[0], element[1], element[2]])
	scrolledwindow.add(elements_treeview)
	list_parms.sel_iter = elements_liststore.get_iter_first()
	if list_parms.sel_iter:
		elements_treeview.set_cursor(elements_liststore.get_path(list_parms.sel_iter))
	content_area = dialog.get_content_area()
	content_area.pack_start(scrolledwindow)
	def on_mouse_button_clicked_elements_list(widget, event):
		if event.button != 1: return
		if event.type == gtk.gdk._2BUTTON_PRESS:
			try: dialog.get_widget_for_response(gtk.RESPONSE_ACCEPT).clicked()
			except: print cons.STR_PYGTK_222_REQUIRED
	def on_treeview_event_after(treeview, event):
		if event.type not in [gtk.gdk.BUTTON_PRESS, gtk.gdk.KEY_PRESS]: return
		model, list_parms.sel_iter = elements_treeviewselection.get_selected()
	def on_key_press_elementslistdialog(widget, event):
		keyname = gtk.gdk.keyval_name(event.keyval)
		if keyname == cons.STR_KEY_RETURN:
			try: dialog.get_widget_for_response(gtk.RESPONSE_ACCEPT).clicked()
			except: print cons.STR_PYGTK_222_REQUIRED
			return True
		return False
	elements_treeview.connect('event-after', on_treeview_event_after)
	dialog.connect('key_press_event', on_key_press_elementslistdialog)
	elements_treeview.connect('button-press-event', on_mouse_button_clicked_elements_list)
	content_area.show_all()
	elements_treeview.grab_focus()
	response = dialog.run()
	dialog.hide()
	if response != gtk.RESPONSE_ACCEPT or not list_parms.sel_iter: return ""
	return unicode(elements_liststore[list_parms.sel_iter][0], cons.STR_UTF8, cons.STR_IGNORE)
def dialog_img_n_entry(father_win, title, entry_content, img_stock):
	"""Insert/Edit Anchor Name"""
	dialog = gtk.Dialog(title=title,
		parent=father_win,
		flags=gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
		buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
				 gtk.STOCK_OK, gtk.RESPONSE_ACCEPT) )
	dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
	dialog.set_default_size(300, -1)
	image = gtk.Image()
	image.set_from_stock(img_stock, gtk.ICON_SIZE_BUTTON)
	entry = gtk.Entry()
	entry.set_text(entry_content)
	hbox = gtk.HBox()
	hbox.pack_start(image, expand=False)
	hbox.pack_start(entry)
	hbox.set_spacing(5)
	content_area = dialog.get_content_area()
	content_area.pack_start(hbox)
	def on_key_press_anchoreditdialog(widget, event):
		keyname = gtk.gdk.keyval_name(event.keyval)
		if keyname == cons.STR_KEY_RETURN:
			try: dialog.get_widget_for_response(gtk.RESPONSE_ACCEPT).clicked()
			except: print cons.STR_PYGTK_222_REQUIRED
			return True
		return False
	dialog.connect('key_press_event', on_key_press_anchoreditdialog)
	content_area.show_all()
	entry.grab_focus()
	response = dialog.run()
	dialog.hide()
	return unicode(entry.get_text(), cons.STR_UTF8, cons.STR_IGNORE).strip() if response == gtk.RESPONSE_ACCEPT else ""
def dialog_image_handle(father_win, title, original_pixbuf):
	"""Insert/Edit Image"""
	class ImgParms:
		def __init__(self, original_pixbuf):
			self.original_pixbuf = original_pixbuf
			self.width = original_pixbuf.get_width()
			self.height = original_pixbuf.get_height()
			self.image_w_h_ration = float(self.width)/self.height
	img_parms = ImgParms(original_pixbuf)
	dialog = gtk.Dialog(title=title,
		parent=father_win,
		flags=gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
		buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
				 gtk.STOCK_OK, gtk.RESPONSE_ACCEPT) )
	dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
	dialog.set_default_size(600, 500)
	button_rotate_90_ccw = gtk.Button()
	button_rotate_90_ccw.set_image(gtk.image_new_from_stock("object-rotate-left", gtk.ICON_SIZE_DND))
	button_rotate_90_cw = gtk.Button()
	button_rotate_90_cw.set_image(gtk.image_new_from_stock("object-rotate-right", gtk.ICON_SIZE_DND))
	scrolledwindow = gtk.ScrolledWindow()
	scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
	viewport = gtk.Viewport()
	image = gtk.image_new_from_pixbuf(original_pixbuf)
	scrolledwindow.add(viewport)
	viewport.add(image)
	hbox_1 = gtk.HBox()
	hbox_1.pack_start(button_rotate_90_ccw, expand=False)
	hbox_1.pack_start(scrolledwindow)
	hbox_1.pack_start(button_rotate_90_cw, expand=False)
	hbox_1.set_spacing(2)
	label_width = gtk.Label(_("Width"))
	adj_width = gtk.Adjustment(value=img_parms.width, lower=1, upper=10000, step_incr=1)
	spinbutton_width = gtk.SpinButton(adj_width)
	label_height = gtk.Label(_("Height"))
	adj_height = gtk.Adjustment(value=img_parms.height, lower=1, upper=10000, step_incr=1)
	spinbutton_height = gtk.SpinButton(adj_height)
	hbox_2 = gtk.HBox()
	hbox_2.pack_start(label_width)
	hbox_2.pack_start(spinbutton_width)
	hbox_2.pack_start(label_height)
	hbox_2.pack_start(spinbutton_height)
	content_area = dialog.get_content_area()
	content_area.pack_start(hbox_1)
	content_area.pack_start(hbox_2, expand=False)
	content_area.set_spacing(6)
	def image_load_into_dialog():
		spinbutton_width.set_value(img_parms.width)
		spinbutton_height.set_value(img_parms.height)
		if img_parms.width <= 900 and img_parms.height <= 600:
			# original size into the dialog
			pixbuf = img_parms.original_pixbuf.scale_simple(int(img_parms.width), int(img_parms.height), gtk.gdk.INTERP_BILINEAR)
		else:
			# reduced size visible into the dialog
			if img_parms.width > 900:
				img_parms_width = 900
				img_parms_height = img_parms_width / img_parms.image_w_h_ration
			else:
				img_parms_height = 600
				img_parms_width = img_parms_height * img_parms.image_w_h_ration
			pixbuf = img_parms.original_pixbuf.scale_simple(int(img_parms_width), int(img_parms_height), gtk.gdk.INTERP_BILINEAR)
		image.set_from_pixbuf(pixbuf)
	def on_button_rotate_90_cw_clicked(*args):
		img_parms.original_pixbuf = img_parms.original_pixbuf.rotate_simple(270)
		img_parms.image_w_h_ration = 1/img_parms.image_w_h_ration
		new_width = img_parms.height # new width is the former height and vice versa
		img_parms.height = img_parms.width
		img_parms.width = new_width
		image_load_into_dialog()
	def on_button_rotate_90_ccw_clicked(*args):
		img_parms.original_pixbuf = img_parms.original_pixbuf.rotate_simple(90)
		img_parms.image_w_h_ration = 1/img_parms.image_w_h_ration
		new_width = img_parms.height # new width is the former height and vice versa
		img_parms.height = img_parms.width
		img_parms.width = new_width
		image_load_into_dialog()
	def on_spinbutton_image_width_value_changed(spinbutton):
		img_parms.width = spinbutton_width.get_value()
		img_parms.height = img_parms.width/img_parms.image_w_h_ration
		image_load_into_dialog()
	def on_spinbutton_image_height_value_changed(spinbutton):
		img_parms.height = spinbutton_height.get_value()
		img_parms.width = img_parms.height*img_parms.image_w_h_ration
		image_load_into_dialog()
	def on_key_press_imagehandledialog(widget, event):
		keyname = gtk.gdk.keyval_name(event.keyval)
		if keyname == cons.STR_KEY_RETURN:
			spinbutton_width.update()
			spinbutton_height.update()
			try: dialog.get_widget_for_response(gtk.RESPONSE_ACCEPT).clicked()
			except: print cons.STR_PYGTK_222_REQUIRED
			return True
		return False
	button_rotate_90_ccw.connect('clicked', on_button_rotate_90_ccw_clicked)
	button_rotate_90_cw.connect('clicked', on_button_rotate_90_cw_clicked)
	spinbutton_width.connect('value-changed', on_spinbutton_image_width_value_changed)
	spinbutton_height.connect('value-changed', on_spinbutton_image_height_value_changed)
	dialog.connect('key_press_event', on_key_press_imagehandledialog)
	image_load_into_dialog()
	content_area.show_all()
	try: dialog.get_widget_for_response(gtk.RESPONSE_ACCEPT).grab_focus()
	except: pass
	response = dialog.run()
	dialog.hide()
	if response != gtk.RESPONSE_ACCEPT: return None
	return img_parms.original_pixbuf.scale_simple(int(img_parms.width), int(img_parms.height), gtk.gdk.INTERP_BILINEAR)
def dialog_node_delete(father_win, warning_label):
	"""Confirmation before Node Remove"""
	dialog = gtk.Dialog(title=_("Warning"),
		parent=father_win,
		flags=gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
		buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
				 gtk.STOCK_OK, gtk.RESPONSE_ACCEPT) )
	dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
	dialog.set_default_size(350, 150)
	image = gtk.Image()
	image.set_from_stock(gtk.STOCK_DIALOG_WARNING, gtk.ICON_SIZE_DIALOG)
	label = gtk.Label(warning_label)
	label.set_use_markup(True)
	hbox = gtk.HBox()
	hbox.pack_start(image)
	hbox.pack_start(label)
	hbox.set_spacing(5)
	content_area = dialog.get_content_area()
	content_area.pack_start(hbox)
	def on_key_press_nodedeletedialog(widget, event):
		keyname = gtk.gdk.keyval_name(event.keyval)
		if keyname == cons.STR_KEY_RETURN:
			try: dialog.get_widget_for_response(gtk.RESPONSE_ACCEPT).clicked()
			except: print cons.STR_PYGTK_222_REQUIRED
			return True
		return False
	dialog.connect('key_press_event', on_key_press_nodedeletedialog)
	content_area.show_all()
	try: dialog.get_widget_for_response(gtk.RESPONSE_ACCEPT).grab_focus()
	except: pass
	response = dialog.run()
	dialog.hide()
	return response
def dialog_exit_del_temp_files(dad):
	"""Temporary Files will be deleted, close applications using them"""
	dialog = gtk.Dialog(title=_("Warning"),
		parent=dad.window,
		flags=gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
		buttons=(_("Cancel"), 2,
				 _("Yes"), 1) )
	dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
	dialog.set_default_size(350, 150)
	try:
		button = dialog.get_widget_for_response(2)
		button.set_image(gtk.image_new_from_stock(gtk.STOCK_CANCEL, gtk.ICON_SIZE_BUTTON))
		button = dialog.get_widget_for_response(1)
		button.set_image(gtk.image_new_from_stock(gtk.STOCK_DIALOG_WARNING, gtk.ICON_SIZE_BUTTON))
		button.grab_focus()
	except: pass
	image = gtk.Image()
	image.set_from_stock(gtk.STOCK_DIALOG_WARNING, gtk.ICON_SIZE_DIALOG)
	label = gtk.Label("<b>"+_("Temporary Files were Created and Opened with External Applications.")+"</b>"+2*cons.CHAR_NEWLINE+"<b>"+_("Quit the External Applications Before Quit CherryTree.")+"</b>"+2*cons.CHAR_NEWLINE+"<b>"+_("Did you Quit the External Applications?")+"</b>")
	label.set_use_markup(True)
	hbox = gtk.HBox()
	hbox.pack_start(image)
	hbox.pack_start(label)
	hbox.set_spacing(5)
	content_area = dialog.get_content_area()
	content_area.pack_start(hbox)
	def on_key_press_exitdialog(widget, event):
		keyname = gtk.gdk.keyval_name(event.keyval)
		if keyname == cons.STR_KEY_RETURN:
			try: dialog.get_widget_for_response(1).clicked()
			except: print cons.STR_PYGTK_222_REQUIRED
			return True
		elif keyname == "Escape":
			try: dialog.get_widget_for_response(2).clicked()
			except: print cons.STR_PYGTK_222_REQUIRED
			return True
		return False
	dialog.connect('key_press_event', on_key_press_exitdialog)
	content_area.show_all()
	response = dialog.run()
	dialog.hide()
	return False if response != 1 else True
def dialog_exit_save(father_win):
	"""Save before Exit Dialog"""
	dialog = gtk.Dialog(title=_("Warning"),
		parent=father_win,
		flags=gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
		buttons=(_("Cancel"), 6,
				 _("No"), 4,
				 _("Yes"), 2) )
	dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
	dialog.set_default_size(350, 150)
	try:
		button = dialog.get_widget_for_response(6)
		button.set_image(gtk.image_new_from_stock(gtk.STOCK_CANCEL, gtk.ICON_SIZE_BUTTON))
		button = dialog.get_widget_for_response(4)
		button.set_image(gtk.image_new_from_stock(gtk.STOCK_CLEAR, gtk.ICON_SIZE_BUTTON))
		button = dialog.get_widget_for_response(2)
		button.set_image(gtk.image_new_from_stock(gtk.STOCK_SAVE, gtk.ICON_SIZE_BUTTON))
		button.grab_focus()
	except: pass
	image = gtk.Image()
	image.set_from_stock(gtk.STOCK_DIALOG_WARNING, gtk.ICON_SIZE_DIALOG)
	label = gtk.Label("<b>"+_("The Current Document was Updated.")+"</b>"+2*cons.CHAR_NEWLINE+"<b>"+_("Do you want to Save the Changes?")+"</b>")
	label.set_use_markup(True)
	hbox = gtk.HBox()
	hbox.pack_start(image)
	hbox.pack_start(label)
	hbox.set_spacing(5)
	content_area = dialog.get_content_area()
	content_area.pack_start(hbox)
	def on_key_press_exitdialog(widget, event):
		keyname = gtk.gdk.keyval_name(event.keyval)
		if keyname == cons.STR_KEY_RETURN:
			try: dialog.get_widget_for_response(2).clicked()
			except: print cons.STR_PYGTK_222_REQUIRED
			return True
		elif keyname == "Escape":
			try: dialog.get_widget_for_response(6).clicked()
			except: print cons.STR_PYGTK_222_REQUIRED
			return True
		return False
	dialog.connect('key_press_event', on_key_press_exitdialog)
	content_area.show_all()
	response = dialog.run()
	dialog.hide()
	return response
def dialog_link_handle(dad, title, sel_tree_iter):
	"""Dialog to Insert/Edit Links"""
	class LinksParms:
		def __init__(self):
			self.sel_iter = sel_tree_iter if sel_tree_iter else dad.links_entries['node']
			self.first_in = True
	links_parms = LinksParms()
	dialog = gtk.Dialog(title=title,
		parent=dad.window,
		flags=gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
		buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
		gtk.STOCK_OK, gtk.RESPONSE_ACCEPT) )
	dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
	dialog.set_default_size(600, 500)
	hbox_webs = gtk.HBox()
	image_webs = gtk.Image()
	image_webs.set_from_stock("link_website", gtk.ICON_SIZE_BUTTON)
	radiobutton_webs = gtk.RadioButton(label=_("To WebSite"))
	entry_webs = gtk.Entry()
	entry_webs.set_text(dad.links_entries['webs'])
	hbox_webs.pack_start(image_webs, expand=False)
	hbox_webs.pack_start(radiobutton_webs, expand=False)
	hbox_webs.pack_start(entry_webs)
	hbox_webs.set_spacing(5)
	hbox_file = gtk.HBox()
	image_file = gtk.Image()
	image_file.set_from_stock(gtk.STOCK_FILE, gtk.ICON_SIZE_BUTTON)
	radiobutton_file = gtk.RadioButton(label=_("To File"))
	radiobutton_file.set_group(radiobutton_webs)
	entry_file = gtk.Entry()
	entry_file.set_text(dad.links_entries['file'])
	button_browse_file = gtk.Button()
	button_browse_file.set_image(gtk.image_new_from_stock("find", gtk.ICON_SIZE_BUTTON))
	hbox_file.pack_start(image_file, expand=False)
	hbox_file.pack_start(radiobutton_file, expand=False)
	hbox_file.pack_start(entry_file)
	hbox_file.pack_start(button_browse_file, expand=False)
	hbox_file.set_spacing(5)
	hbox_folder = gtk.HBox()
	image_folder = gtk.Image()
	image_folder.set_from_stock(gtk.STOCK_DIRECTORY, gtk.ICON_SIZE_BUTTON)
	radiobutton_folder = gtk.RadioButton(label=_("To Folder"))
	radiobutton_folder.set_group(radiobutton_webs)
	entry_folder = gtk.Entry()
	entry_folder.set_text(dad.links_entries['fold'])
	button_browse_folder = gtk.Button()
	button_browse_folder.set_image(gtk.image_new_from_stock("find", gtk.ICON_SIZE_BUTTON))
	hbox_folder.pack_start(image_folder, expand=False)
	hbox_folder.pack_start(radiobutton_folder, expand=False)
	hbox_folder.pack_start(entry_folder)
	hbox_folder.pack_start(button_browse_folder, expand=False)
	hbox_folder.set_spacing(5)
	hbox_node = gtk.HBox()
	image_node = gtk.Image()
	image_node.set_from_stock("cherrytree", gtk.ICON_SIZE_BUTTON)
	radiobutton_node = gtk.RadioButton(label=_("To Node"))
	radiobutton_node.set_group(radiobutton_webs)
	hbox_node.pack_start(image_node, expand=False)
	hbox_node.pack_start(radiobutton_node)
	hbox_node.set_spacing(5)
	hbox_detail = gtk.HBox()
	treeview_2 = gtk.TreeView(dad.treestore)
	treeview_2.set_headers_visible(False)
	treeview_2.set_search_column(1)
	renderer_pixbuf_2 = gtk.CellRendererPixbuf()
	renderer_text_2 = gtk.CellRendererText()
	column_2 = gtk.TreeViewColumn()
	column_2.pack_start(renderer_pixbuf_2, False)
	column_2.pack_start(renderer_text_2, True)
	column_2.set_attributes(renderer_pixbuf_2, stock_id=0)
	column_2.set_attributes(renderer_text_2, text=1)
	treeview_2.append_column(column_2)
	treeviewselection_2 = treeview_2.get_selection()
	scrolledwindow = gtk.ScrolledWindow()
	scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
	scrolledwindow.add(treeview_2)
	vbox_anchor = gtk.VBox()
	label_over = gtk.Label()
	label_below = gtk.Label()
	hbox_anchor = gtk.HBox()
	entry_anchor = gtk.Entry()
	entry_anchor.set_text(dad.links_entries['anch'])
	button_browse_anchor = gtk.Button()
	button_browse_anchor.set_image(gtk.image_new_from_stock("anchor", gtk.ICON_SIZE_BUTTON))
	hbox_anchor.pack_start(entry_anchor)
	hbox_anchor.pack_start(button_browse_anchor, expand=False)
	frame_anchor = gtk.Frame(label="<b>"+_("Anchor Name (optional)")+"</b>")
	frame_anchor.get_label_widget().set_use_markup(True)
	frame_anchor.set_shadow_type(gtk.SHADOW_NONE)
	frame_anchor.add(hbox_anchor)
	vbox_anchor.pack_start(label_over)
	vbox_anchor.pack_start(frame_anchor, expand=False)
	vbox_anchor.pack_start(label_below)
	hbox_detail.pack_start(scrolledwindow)
	hbox_detail.pack_start(vbox_anchor, expand=False)
	content_area = dialog.get_content_area()
	content_area.pack_start(hbox_webs, expand=False)
	content_area.pack_start(hbox_file, expand=False)
	content_area.pack_start(hbox_folder, expand=False)
	content_area.pack_start(hbox_node, expand=False)
	content_area.pack_start(hbox_detail)
	content_area.set_spacing(5)
	radiobutton_webs.set_active(dad.link_type == cons.LINK_TYPE_WEBS)
	radiobutton_node.set_active(dad.link_type == cons.LINK_TYPE_NODE)
	radiobutton_file.set_active(dad.link_type == cons.LINK_TYPE_FILE)
	radiobutton_folder.set_active(dad.link_type == cons.LINK_TYPE_FOLD)
	def link_type_changed_on_dialog():
		entry_webs.set_sensitive(dad.link_type == cons.LINK_TYPE_WEBS)
		hbox_detail.set_sensitive(dad.link_type == cons.LINK_TYPE_NODE)
		entry_file.set_sensitive(dad.link_type == cons.LINK_TYPE_FILE)
		entry_folder.set_sensitive(dad.link_type == cons.LINK_TYPE_FOLD)
		if dad.link_type == cons.LINK_TYPE_WEBS: entry_webs.grab_focus()
		elif dad.link_type == cons.LINK_TYPE_NODE:
			treeview_2.grab_focus()
			if links_parms.first_in:
				links_parms.first_in = False
				config.get_tree_expanded_collapsed_string(dad)
				config.set_tree_expanded_collapsed_string(dad, treeview=treeview_2)
			if not links_parms.sel_iter: links_parms.sel_iter = dad.treestore.get_iter_first()
			sel_path = dad.treestore.get_path(links_parms.sel_iter)
			treeview_2.expand_to_path(sel_path)
			treeview_2.set_cursor(sel_path)
			treeview_2.scroll_to_cell(sel_path)
		elif dad.link_type == cons.LINK_TYPE_FILE: entry_file.grab_focus()
		else: entry_folder.grab_focus()
	def on_radiobutton_link_website_toggled(radiobutton):
		if radiobutton.get_active(): dad.link_type = cons.LINK_TYPE_WEBS
		link_type_changed_on_dialog()
	def on_radiobutton_link_node_anchor_toggled(radiobutton):
		if radiobutton.get_active(): dad.link_type = cons.LINK_TYPE_NODE
		link_type_changed_on_dialog()
	def on_radiobutton_link_file_toggled(radiobutton):
		if radiobutton.get_active(): dad.link_type = cons.LINK_TYPE_FILE
		link_type_changed_on_dialog()
	def on_radiobutton_link_folder_toggled(radiobutton):
		if radiobutton.get_active(): dad.link_type = cons.LINK_TYPE_FOLD
		link_type_changed_on_dialog()
	def on_button_browse_for_file_to_link_to_clicked(self, *args):
		filepath = dialog_file_select(curr_folder=dad.pick_dir, parent=dialog)
		if not filepath: return
		dad.pick_dir = os.path.dirname(filepath)
		if dad.links_relative:
			try: filepath = os.path.relpath(filepath, dad.file_dir)
			except: print "cannot set relative path for different drives"
		entry_file.set_text(filepath)
	def on_button_browse_for_folder_to_link_to_clicked(self, *args):
		filepath = dialog_folder_select(curr_folder=dad.pick_dir, parent=dialog)
		if not filepath: return
		dad.pick_dir = filepath
		if dad.links_relative:
			try: filepath = os.path.relpath(filepath, dad.file_dir)
			except: print "cannot set relative path for different drives"
		entry_folder.set_text(filepath)
	def on_browse_anchors_button_clicked(*args):
		if not links_parms.sel_iter:
			dialog_warning(_("No Node is Selected"), dialog)
			return
		anchors_list = []
		text_buffer = dad.get_textbuffer_from_tree_iter(links_parms.sel_iter)
		curr_iter = text_buffer.get_start_iter()
		while 1:
			anchor = curr_iter.get_child_anchor()
			if anchor != None:
				if "pixbuf" in dir(anchor) and "anchor" in dir(anchor.pixbuf):
					anchors_list.append([anchor.pixbuf.anchor])
			if not curr_iter.forward_char(): break
		dad.objects_buffer_refresh()
		if not anchors_list:
			dialog_info(_("There are No Anchors in the Selected Node"), dialog)
			return
		ret_anchor_name = dialog_choose_element_in_list(dialog, _("Choose Existing Anchor"), anchors_list, _("Anchor Name"))
		if ret_anchor_name: entry_anchor.set_text(ret_anchor_name)
	def on_treeview_event_after(treeview, event):
		if event.type not in [gtk.gdk.BUTTON_PRESS, gtk.gdk._2BUTTON_PRESS, gtk.gdk.KEY_PRESS]: return
		model, links_parms.sel_iter = treeviewselection_2.get_selected()
		if event.type == gtk.gdk.BUTTON_PRESS:
			if event.button == 2:
				path_at_click = treeview.get_path_at_pos(int(event.x), int(event.y))
				if path_at_click:
					if treeview.row_expanded(path_at_click[0]):
						treeview.collapse_row(path_at_click[0])
					else: treeview.expand_row(path_at_click[0], False)
		elif event.type == gtk.gdk._2BUTTON_PRESS and event.button == 1:
			if links_parms.sel_iter:
				treestore = treeview.get_model()
				if treeview.row_expanded(treestore.get_path(links_parms.sel_iter)):
					treeview.collapse_row(treestore.get_path(links_parms.sel_iter))
				else:
					treeview.expand_row(treestore.get_path(links_parms.sel_iter), open_all=False)
		elif event.type == gtk.gdk.KEY_PRESS:
			if links_parms.sel_iter:
				treestore = treeview.get_model()
				keyname = gtk.gdk.keyval_name(event.keyval)
				if keyname == cons.STR_KEY_LEFT:
					treeview.collapse_row(treestore.get_path(links_parms.sel_iter))
				elif keyname == cons.STR_KEY_RIGHT:
					treeview.expand_row(treestore.get_path(links_parms.sel_iter), open_all=False)
	def on_key_press_links_handle_dialog(widget, event):
		keyname = gtk.gdk.keyval_name(event.keyval)
		if keyname == cons.STR_KEY_RETURN:
			try: dialog.get_widget_for_response(gtk.RESPONSE_ACCEPT).clicked()
			except: print cons.STR_PYGTK_222_REQUIRED
			return True
		elif keyname == cons.STR_KEY_TAB:
			if dad.link_type == cons.LINK_TYPE_WEBS: radiobutton_file.set_active(True)
			elif dad.link_type == cons.LINK_TYPE_FILE: radiobutton_folder.set_active(True)
			elif dad.link_type == cons.LINK_TYPE_FOLD: radiobutton_node.set_active(True)
			else: radiobutton_webs.set_active(True)
			return True
		return False
	radiobutton_webs.connect("toggled", on_radiobutton_link_website_toggled)
	radiobutton_node.connect("toggled", on_radiobutton_link_node_anchor_toggled)
	radiobutton_file.connect("toggled", on_radiobutton_link_file_toggled)
	radiobutton_folder.connect("toggled", on_radiobutton_link_folder_toggled)
	button_browse_file.connect('clicked', on_button_browse_for_file_to_link_to_clicked)
	button_browse_folder.connect('clicked', on_button_browse_for_folder_to_link_to_clicked)
	button_browse_anchor.connect('clicked', on_browse_anchors_button_clicked)
	treeview_2.connect('event-after', on_treeview_event_after)
	dialog.connect("key_press_event", on_key_press_links_handle_dialog)
	content_area.show_all()
	link_type_changed_on_dialog()
	response = dialog.run()
	dialog.hide()
	if response != gtk.RESPONSE_ACCEPT: return False
	dad.links_entries['webs'] = unicode(entry_webs.get_text(), cons.STR_UTF8, cons.STR_IGNORE).strip()
	dad.links_entries['file'] = unicode(entry_file.get_text(), cons.STR_UTF8, cons.STR_IGNORE).strip()
	dad.links_entries['fold'] = unicode(entry_folder.get_text(), cons.STR_UTF8, cons.STR_IGNORE).strip()
	dad.links_entries['anch'] = unicode(entry_anchor.get_text(), cons.STR_UTF8, cons.STR_IGNORE).strip()
	dad.links_entries['node'] = links_parms.sel_iter
	return True
def dialog_choose_node(dad, title, treestore, sel_tree_iter):
	"""Dialog to Select a Node"""
	class NodeParms:
		def __init__(self):
			self.sel_iter = sel_tree_iter
	node_parms = NodeParms()
	dialog = gtk.Dialog(title=title,
		parent=dad.window,
		flags=gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
		buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
		gtk.STOCK_OK, gtk.RESPONSE_ACCEPT) )
	dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
	dialog.set_default_size(600, 500)
	treeview_2 = gtk.TreeView(treestore)
	treeview_2.set_headers_visible(False)
	treeview_2.set_search_column(1)
	renderer_pixbuf_2 = gtk.CellRendererPixbuf()
	renderer_text_2 = gtk.CellRendererText()
	column_2 = gtk.TreeViewColumn()
	column_2.pack_start(renderer_pixbuf_2, False)
	column_2.pack_start(renderer_text_2, True)
	column_2.set_attributes(renderer_pixbuf_2, stock_id=0)
	column_2.set_attributes(renderer_text_2, text=1)
	treeview_2.append_column(column_2)
	treeviewselection_2 = treeview_2.get_selection()
	scrolledwindow = gtk.ScrolledWindow()
	scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
	scrolledwindow.add(treeview_2)
	content_area = dialog.get_content_area()
	content_area.pack_start(scrolledwindow)
	def on_key_press_choose_node_dialog(widget, event):
		if gtk.gdk.keyval_name(event.keyval) == cons.STR_KEY_RETURN:
			try: dialog.get_widget_for_response(gtk.RESPONSE_ACCEPT).clicked()
			except: print cons.STR_PYGTK_222_REQUIRED
			return True
		return False
	def on_treeview_event_after(treeview, event):
		if event.type not in [gtk.gdk.BUTTON_PRESS, gtk.gdk._2BUTTON_PRESS, gtk.gdk.KEY_PRESS]: return
		model, node_parms.sel_iter = treeviewselection_2.get_selected()
		if event.type == gtk.gdk.BUTTON_PRESS:
			if event.button == 2:
				path_at_click = treeview.get_path_at_pos(int(event.x), int(event.y))
				if path_at_click:
					if treeview.row_expanded(path_at_click[0]):
						treeview.collapse_row(path_at_click[0])
					else: treeview.expand_row(path_at_click[0], False)
		elif event.type == gtk.gdk._2BUTTON_PRESS and event.button == 1:
			if node_parms.sel_iter:
				treestore = treeview.get_model()
				if treeview.row_expanded(treestore.get_path(node_parms.sel_iter)):
					treeview.collapse_row(treestore.get_path(node_parms.sel_iter))
				else:
					treeview.expand_row(treestore.get_path(node_parms.sel_iter), open_all=False)
		elif event.type == gtk.gdk.KEY_PRESS:
			if node_parms.sel_iter:
				treestore = treeview.get_model()
				keyname = gtk.gdk.keyval_name(event.keyval)
				if keyname == cons.STR_KEY_LEFT:
					treeview.collapse_row(treestore.get_path(node_parms.sel_iter))
				elif keyname == cons.STR_KEY_RIGHT:
					treeview.expand_row(treestore.get_path(node_parms.sel_iter), open_all=False)
	dialog.connect("key_press_event", on_key_press_choose_node_dialog)
	treeview_2.connect('event-after', on_treeview_event_after)
	content_area.show_all()
	config.get_tree_expanded_collapsed_string(dad)
	config.set_tree_expanded_collapsed_string(dad, treeview=treeview_2)
	if node_parms.sel_iter:
		sel_path = treestore.get_path(node_parms.sel_iter)
		treeview_2.expand_to_path(sel_path)
		treeview_2.set_cursor(sel_path)
		treeview_2.scroll_to_cell(sel_path)
	response = dialog.run()
	dialog.hide()
	return None if response != gtk.RESPONSE_ACCEPT else node_parms.sel_iter
def dialog_selnode_selnodeandsub_alltree(dad, also_selection, also_include_node_name=False, also_new_node_page=False, also_index_in_page=False):
	"""Dialog to select between the Selected Node/Selected Node + Subnodes/All Tree"""
	dialog = gtk.Dialog(title=_("Involved Nodes"),
		parent=dad.window,
		flags=gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
		buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
		gtk.STOCK_OK, gtk.RESPONSE_ACCEPT) )
	dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
	if also_selection: radiobutton_selection = gtk.RadioButton(label=_("Selected Text Only"))
	radiobutton_selnode = gtk.RadioButton(label=_("Selected Node Only"))
	radiobutton_selnodeandsub = gtk.RadioButton(label=_("Selected Node and Subnodes"))
	radiobutton_alltree = gtk.RadioButton(label=_("All the Tree"))
	radiobutton_selnodeandsub.set_group(radiobutton_selnode)
	radiobutton_alltree.set_group(radiobutton_selnode)
	if also_selection: radiobutton_selection.set_group(radiobutton_selnode)
	content_area = dialog.get_content_area()
	if also_selection: content_area.pack_start(radiobutton_selection)
	content_area.pack_start(radiobutton_selnode)
	content_area.pack_start(radiobutton_selnodeandsub)
	content_area.pack_start(radiobutton_alltree)
	if also_include_node_name:
		separator_item = gtk.HSeparator()
		checkbutton_node_name = gtk.CheckButton(label=_("Include Node Name"))
		checkbutton_node_name.set_active(dad.last_include_node_name)
		content_area.pack_start(separator_item)
		content_area.pack_start(checkbutton_node_name)
	if also_index_in_page:
		separator_item = gtk.HSeparator()
		checkbutton_index_in_page = gtk.CheckButton(label=_("Links Tree in Every Page"))
		checkbutton_index_in_page.set_active(dad.last_index_in_page)
		content_area.pack_start(separator_item)
		content_area.pack_start(checkbutton_index_in_page)
	if also_new_node_page:
		checkbutton_new_node_page = gtk.CheckButton(label=_("New Node in New Page"))
		checkbutton_new_node_page.set_active(dad.last_new_node_page)
		content_area.pack_start(checkbutton_new_node_page)
	def on_key_press_enter_dialog(widget, event):
		if gtk.gdk.keyval_name(event.keyval) == cons.STR_KEY_RETURN:
			try: dialog.get_widget_for_response(gtk.RESPONSE_ACCEPT).clicked()
			except: print cons.STR_PYGTK_222_REQUIRED
			return True
		return False
	dialog.connect("key_press_event", on_key_press_enter_dialog)
	content_area.show_all()
	response = dialog.run()
	if radiobutton_selnode.get_active(): ret_val = 1
	elif radiobutton_selnodeandsub.get_active(): ret_val = 2
	elif radiobutton_alltree.get_active(): ret_val = 3
	else: ret_val = 4
	if also_include_node_name:
		dad.last_include_node_name = checkbutton_node_name.get_active()
	if also_index_in_page:
		dad.last_index_in_page = checkbutton_index_in_page.get_active()
	if also_new_node_page:
		dad.last_new_node_page = checkbutton_new_node_page.get_active()
	dialog.destroy()
	if response != gtk.RESPONSE_ACCEPT: ret_val = 0
	return ret_val
def set_bookmarks_menu_items(inst):
	"""Set Bookmarks Menu Items"""
	bookmarks_menu = inst.ui.get_widget("/MenuBar/BookmarksMenu").get_submenu()
	for menu_item in inst.bookmarks_menu_items:
		bookmarks_menu.remove(menu_item)
	menu_item = gtk.SeparatorMenuItem()
	menu_item.show()
	bookmarks_menu.append(menu_item)
	inst.bookmarks_menu_items = [menu_item]
	bookmarks_to_rm = []
	for node_id_str in inst.bookmarks:
		if not long(node_id_str) in inst.nodes_names_dict:
			bookmarks_to_rm.append(node_id_str)
			continue
		menu_item = gtk.ImageMenuItem(inst.nodes_names_dict[long(node_id_str)])
		menu_item.set_image(gtk.image_new_from_stock("pin", gtk.ICON_SIZE_MENU))
		menu_item.connect("activate", select_bookmark_node, node_id_str, inst)
		menu_item.show()
		bookmarks_menu.append(menu_item)
		inst.bookmarks_menu_items.append(menu_item)
	for element in bookmarks_to_rm: inst.bookmarks.remove(element)
def set_menu_items_special_chars(inst):
	"""Set Special Chars menu items"""
	if not "special_menu_1" in dir(inst):
		inst.special_menu_1 = gtk.Menu()
		first_run = True
	else:
		children_1 = inst.special_menu_1.get_children()
		for children in children_1:
			children.hide()
			del children
		first_run = False
	for special_char in inst.special_chars:
		menu_item = gtk.MenuItem(special_char)
		menu_item.connect("activate", insert_special_char, special_char, inst)
		menu_item.show()
		inst.special_menu_1.append(menu_item)
	if first_run:
		# main menu
		special_menuitem = gtk.ImageMenuItem(_("Insert _Special Character"))
		special_menuitem.set_image(gtk.image_new_from_stock("insert", gtk.ICON_SIZE_MENU))
		special_menuitem.set_tooltip_text(_("Insert a Special Character"))
		special_menuitem.set_submenu(inst.special_menu_1)
		inst.ui.get_widget("/MenuBar/EditMenu").get_submenu().insert(special_menuitem, 14)
def set_menu_items_recent_documents(inst):
	"""Set Recent Documents menu items on Menu and Toolbar"""
	if not "recent_menu_1" in dir(inst):
		inst.recent_menu_1 = gtk.Menu()
		inst.recent_menu_2 = gtk.Menu()
		first_run = True
	else:
		children_1 = inst.recent_menu_1.get_children()
		children_2 = inst.recent_menu_2.get_children()
		for children in children_1:
			children.hide()
			del children
		for children in children_2:
			children.hide()
			del children
		first_run = False
	for target in [1, 2]:
		for i, filepath in enumerate(inst.recent_docs):
			if i >= cons.MAX_RECENT_DOCS: break
			menu_item = gtk.ImageMenuItem(filepath)
			menu_item.set_image(gtk.image_new_from_stock("gtk-open", gtk.ICON_SIZE_MENU))
			menu_item.connect("activate", open_recent_document, filepath, inst)
			menu_item.show()
			if target == 1: inst.recent_menu_1.append(menu_item)
			else: inst.recent_menu_2.append(menu_item)
	if first_run:
		# main menu
		recent_menuitem = gtk.ImageMenuItem(_("_Recent Documents"))
		recent_menuitem.set_image(gtk.image_new_from_stock("gtk-open", gtk.ICON_SIZE_MENU))
		recent_menuitem.set_tooltip_text(_("Open a Recent CherryTree Document"))
		recent_menuitem.set_submenu(inst.recent_menu_1)
		inst.ui.get_widget("/MenuBar/FileMenu").get_submenu().insert(recent_menuitem, 3)
		# toolbar
		if inst.toolbar_open_n_recent >= 0:
			menu_toolbutton = gtk.MenuToolButton("gtk-open")
			menu_toolbutton.set_tooltip_text(_("Open a CherryTree Document"))
			menu_toolbutton.set_arrow_tooltip_text(_("Open a Recent CherryTree Document"))
			menu_toolbutton.set_menu(inst.recent_menu_2)
			menu_toolbutton.connect("clicked", inst.file_open)
			inst.ui.get_widget("/ToolBar").insert(menu_toolbutton, inst.toolbar_open_n_recent)
def add_recent_document(inst, filepath):
	"""Add a Recent Document if Needed"""
	if filepath in inst.recent_docs and inst.recent_docs[0] == filepath:
		return
	if filepath in inst.recent_docs: inst.recent_docs.remove(filepath)
	inst.recent_docs.insert(0, filepath)
	set_menu_items_recent_documents(inst)
def insert_special_char(menu_item, special_char, dad):
	"""A Special character insert was Requested"""
	text_view, text_buffer, from_codebox = dad.get_text_view_n_buffer_codebox_proof()
	if not text_buffer: return
	text_buffer.insert_at_cursor(special_char)
def open_recent_document(menu_item, filepath, dad):
	"""A Recent Document was Requested"""
	if os.path.isfile(filepath):
		#dad.filepath_boss_open(filepath, "")
		dad.filepath_open(filepath)
	else:
		dialog_error(_("The Document %s was Not Found") % filepath, dad.window)
		try:
			idx = dad.recent_docs.index(filepath)
			dad.recent_docs.append(dad.recent_docs.pop(idx))
			set_menu_items_recent_documents(dad)
		except:
			pass
def select_bookmark_node(menu_item, node_id_str, dad):
	"""Select a Node in the Bookmarks List"""
	node_iter = dad.get_tree_iter_from_node_id(long(node_id_str))
	if node_iter: dad.treeview_safe_set_cursor(node_iter)
def bookmarks_handle(dad):
	"""Handle the Bookmarks List"""
	dialog = gtk.Dialog(title=_("Handle the Bookmarks List"),
		parent=dad.window,
		flags=gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
		buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
		gtk.STOCK_OK, gtk.RESPONSE_ACCEPT) )
	dialog.set_default_size(500, 400)
	dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
	liststore = gtk.ListStore(str, str, str)
	for node_id_str in dad.bookmarks:
		# icon, node name, node id string
		liststore.append(["pin", dad.nodes_names_dict[long(node_id_str)], node_id_str])
	treeview = gtk.TreeView(liststore)
	treeview.set_headers_visible(False)
	treeview.set_reorderable(True)
	treeviewselection = treeview.get_selection()
	def on_key_press_liststore(widget, event):
		keyname = gtk.gdk.keyval_name(event.keyval)
		if keyname == cons.STR_KEY_DELETE:
			model, tree_iter = treeviewselection.get_selected()
			if tree_iter: model.remove(tree_iter)
	def on_mouse_button_clicked_liststore(widget, event):
		"""Catches mouse buttons clicks"""
		if event.button != 1: return
		if event.type != gtk.gdk._2BUTTON_PRESS: return
		path_n_tvc = treeview.get_path_at_pos(int(event.x), int(event.y))
		if not path_n_tvc: return
		tree_path = path_n_tvc[0]
		dad_tree_path = dad.get_tree_iter_from_node_id(long(liststore[tree_path][2]))
		dad.treeview_safe_set_cursor(dad_tree_path)
	treeview.connect('key_press_event', on_key_press_liststore)
	treeview.connect('button-press-event', on_mouse_button_clicked_liststore)
	renderer_pixbuf = gtk.CellRendererPixbuf()
	renderer_text = gtk.CellRendererText()
	column = gtk.TreeViewColumn()
	column.pack_start(renderer_pixbuf, False)
	column.pack_start(renderer_text, True)
	column.set_attributes(renderer_pixbuf, stock_id=0)
	column.set_attributes(renderer_text, text=1)
	treeview.append_column(column)
	scrolledwindow = gtk.ScrolledWindow()
	scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
	scrolledwindow.add(treeview)
	content_area = dialog.get_content_area()
	hbox = gtk.HBox()
	vbox = gtk.VBox()
	vbox.set_spacing(1)
	button_move_up = gtk.Button()
	button_move_up.set_image(gtk.image_new_from_stock("gtk-go-up", gtk.ICON_SIZE_DND))
	button_move_down = gtk.Button()
	button_move_down.set_image(gtk.image_new_from_stock("gtk-go-down", gtk.ICON_SIZE_DND))
	button_delete = gtk.Button()
	button_delete.set_image(gtk.image_new_from_stock("gtk-clear", gtk.ICON_SIZE_DND))
	button_sort_desc = gtk.Button()
	button_sort_desc.set_image(gtk.image_new_from_stock("gtk-sort-descending", gtk.ICON_SIZE_DND))
	button_sort_asc = gtk.Button()
	button_sort_asc.set_image(gtk.image_new_from_stock("gtk-sort-ascending", gtk.ICON_SIZE_DND))
	def on_button_move_up_clicked(*args):
		model, tree_iter = treeviewselection.get_selected()
		if tree_iter:
			prev_iter = dad.get_tree_iter_prev_sibling(model, tree_iter)
			if prev_iter:
				model.swap(tree_iter, prev_iter)
	button_move_up.connect('clicked', on_button_move_up_clicked)
	def on_button_move_down_clicked(*args):
		model, tree_iter = treeviewselection.get_selected()
		if tree_iter:
			next_iter = model.iter_next(tree_iter)
			if next_iter:
				model.swap(tree_iter, next_iter)
	button_move_down.connect('clicked', on_button_move_down_clicked)
	def on_button_delete_clicked(*args):
		model, tree_iter = treeviewselection.get_selected()
		if tree_iter:
			model.remove(tree_iter)
	button_delete.connect('clicked', on_button_delete_clicked)
	def on_button_sort_desc_clicked(*args):
		while dad.node_siblings_sort_iteration(liststore, None, False, 1):
			pass
	button_sort_desc.connect('clicked', on_button_sort_desc_clicked)
	def on_button_sort_asc_clicked(*args):
		while dad.node_siblings_sort_iteration(liststore, None, True, 1):
			pass
	button_sort_asc.connect('clicked', on_button_sort_asc_clicked)
	vbox.pack_start(button_move_up, expand=False)
	vbox.pack_start(button_move_down, expand=False)
	vbox.pack_start(button_delete, expand=False)
	vbox.pack_start(button_sort_desc, expand=False)
	vbox.pack_start(button_sort_asc, expand=False)
	hbox.pack_start(scrolledwindow, expand=True)
	hbox.pack_start(vbox, expand=False)
	content_area.pack_start(hbox)
	content_area.show_all()
	response = dialog.run()
	temp_bookmarks = []
	tree_iter = liststore.get_iter_first()
	while tree_iter != None:
		temp_bookmarks.append(liststore[tree_iter][2])
		tree_iter = liststore.iter_next(tree_iter)
	dialog.destroy()
	if response != gtk.RESPONSE_ACCEPT: return False
	removed_bookmarks = []
	for old_bookmark in dad.bookmarks:
		if not old_bookmark in temp_bookmarks:
			removed_bookmarks.append(old_bookmark)
	dad.bookmarks = temp_bookmarks
	for removed_bookmark in removed_bookmarks:
		tree_iter = dad.get_tree_iter_from_node_id(int(removed_bookmark))
		if tree_iter:
			dad.update_node_pre_icon(tree_iter)
			if dad.curr_tree_iter and dad.treestore[tree_iter][3] == dad.treestore[dad.curr_tree_iter][3]:
				dad.menu_tree_update_for_bookmarked_node(False)
	set_bookmarks_menu_items(dad)
	dad.ctdb_handler.pending_edit_db_bookmarks()
	return True
def set_object_highlight(inst, obj_highl):
	"""Set the Highlight to obj_highl only"""
	if inst.highlighted_obj:
		inst.highlighted_obj.drag_unhighlight()
		inst.highlighted_obj = None
	if obj_highl:
		obj_highl.drag_highlight()
		inst.highlighted_obj = obj_highl





'''
#===============================================================================||
'''
<(DNA)>:
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
