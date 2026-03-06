#!/usr/bin/env python3
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name: Nchantrs Calculator Application Test
	description: >
		Example calculator application using Nchantrs widgets
	version: 0.0.0.0.0.1
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*
# ======================================================================================================================||
"""
Example Calculator Application
==============================

This is a test application that demonstrates how to use Nchantrs widgets.
It creates a calculator application using NchantdCalculator widget.

Usage:
	python test_app_calculator.py

Or as an entry point:
	nchantdcalculator --name "Calculator"
"""
import sys
from os.path import dirname, join

# Add the project to the path
here = dirname(__file__)
sys.path.insert(0, here)

# Import Nchantrs widgets
from nchantrs.widgets.applications.applications import NchantdCloak
from nchantrs.widgets.calculators.calculators import NchantdCalculator


class CalculatorApplication(NchantdCloak):
	"""Calculator Application extending NchantdCloak"""
	
	def __init__(self, name="Calculator", instance=None, parent=None, cfg=None, args=None):
		"""Initialize the calculator application"""
		if cfg is None:
			cfg = {}
		# Configure as a calculator app
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
		self.app_type = "calculator"
		self.calculator_widget = None
	
	def run_on_launch(self):
		"""Custom launch behavior for calculator app"""
		print(f"Launching Calculator Application: {self.application_name}")
		# Create the calculator widget
		self.calculator_widget = NchantdCalculator(self).initWidget()


def main():
	"""Main entry point for the calculator application"""
	# Get application name from command line or use default
	name = "Calculator"
	if len(sys.argv) > 1:
		name = sys.argv[1]
	
	# Create and run the application
	app = CalculatorApplication(name)
	app.initApp()
	
	return app


if __name__ == "__main__":
	main()
