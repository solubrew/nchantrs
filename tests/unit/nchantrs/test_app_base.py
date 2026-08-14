#!/usr/bin/env python3
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name: Nchantrs Base Application Test
	description: >
		Example application using nchantment() entry point
	version: 0.0.0.0.0.1
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*
# ======================================================================================================================||
"""
Example Base Application
========================

This is a test application that demonstrates how to use the nchantment() entry point.
The nchantment function is the main entry point for launching Nchantrs applications.

Usage:
	python test_app_base.py

Or as an entry point:
	nchantment --name "Base App"
"""
import sys  # noqa: E402
from os.path import dirname  # noqa: E402

# Add the project to the path
here = dirname(__file__)
sys.path.insert(0, here)

# Import Nchantrs entry point
from nchantrs.nchantrs import nchantment  # noqa: E402
from nchantrs.widgets.applications.applications import NchantdCloak  # noqa: E402


class BaseApplication(NchantdCloak):
	"""Base Application extending NchantdCloak"""

	def __init__(self, name="Base App", instance=None, parent=None, cfg=None, args=None):
		"""Initialize the base application"""
		if cfg is None:
			cfg = {}
		# Configure as a basic app
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
		self.app_type = "base"

	def run_on_launch(self):
		"""Custom launch behavior"""
		print(f"Launching Base Application: {self.application_name}")


def main():
	"""Main entry point using nchantment()"""
	# Get application name from command line or use default
	name = "Base App"
	if len(sys.argv) > 1:
		name = sys.argv[1]

	# Create args dictionary
	args = {
		"name": name,
		"instance": None,
	}

	# Use nchantment entry point
	app = nchantment(name, args, main_app=BaseApplication)

	return app


if __name__ == "__main__":
	main()
