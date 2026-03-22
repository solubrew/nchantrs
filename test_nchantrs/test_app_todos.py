#!/usr/bin/env python3
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name: Nchantrs Todo Application Test
	description: >
		Example todo application using Nchantrs entry points
	version: 0.0.0.0.0.1
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*
# ======================================================================================================================||
"""
Example Todo Application
=========================

This is a test application that demonstrates how to use Nchantrs entry points.
It creates a simple todo list application using the NchantdCloak base application.

Usage:
	python test_app_todos.py

Or as an entry point:
	nchantdtodos --name "My Todos"
"""
import sys
from os.path import dirname, join

# Add the project to the path
here = dirname(__file__)
sys.path.insert(0, here)

# Import Nchantrs core
from nchantrs.widgets.applications.applications import NchantdCloak


class TodoApplication(NchantdCloak):
	"""Todo Application extending NchantdCloak"""
	
	def __init__(self, name="Todo App", instance=None, parent=None, cfg=None, args=None):
		"""Initialize the todo application"""
		if cfg is None:
			cfg = {}
		# Configure as a todo app
		cfg.update({
			"config": {
				"version": "0.0.0.0.0.1",
				"has_agents": False,
				"has_comms": False,
				"has_services": False,
				"has_extensions": False,
				"has_library": False,
			},
			"startup": type("Startup", (), {"new_application": True})()
		})
		super().__init__(name, instance, parent, cfg, args)
		self.app_type = "todos"
	
	def run_on_launch(self):
		"""Custom launch behavior for todo app"""
		print(f"Launching Todo Application: {self.application_name}")


def main():
	"""Main entry point for the todo application"""
	# Get application name from command line or use default
	name = "My Todos"
	if len(sys.argv) > 1:
		name = sys.argv[1]
	
	# Create and run the application
	app = TodoApplication(name)
	app.initApp()
	
	return app


if __name__ == "__main__":
	main()
