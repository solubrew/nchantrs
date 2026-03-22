#!/usr/bin/env python3
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
Integration Tests for Nchantrs Entry Points
=============================================

These tests verify that all entry points work correctly.
"""
import sys
from os.path import dirname
from unittest import TestCase, main as unittest_main

# Add project to path
here = dirname(__file__)
sys.path.insert(0, here)


class TestNchantrsEntryPoints(TestCase):
	"""Test all Nchantrs entry points"""
	
	def test_import_nchantdCloak(self):
		"""Test that NchantdCloak can be imported"""
		from nchantrs.widgets.applications.applications import NchantdCloak
		self.assertIsNotNone(NchantdCloak)
	
	def test_import_nchantdPanties(self):
		"""Test that NchantdPanties can be imported"""
		from nchantrs.widgets.applications.applications import NchantdPanties
		self.assertIsNotNone(NchantdPanties)
	
	def test_import_nchantment(self):
		"""Test that nchantment function can be imported"""
		from nchantrs.nchantrs import nchantment
		self.assertIsNotNone(nchantment)
	
	def test_import_flection(self):
		"""Test that flection function can be imported"""
		from nchantrs.nchantrs import flection
		self.assertIsNotNone(flection)
	
	def test_import_aberation(self):
		"""Test that aberration function can be imported"""
		from nchantrs.nchantrs import aberration
		self.assertIsNotNone(aberration)
	
	def test_import_distortion(self):
		"""Test that distortion function can be imported"""
		from nchantrs.nchantrs import distortion
		self.assertIsNotNone(distortion)
	
	def test_import_calculator(self):
		"""Test that NchantdCalculator can be imported"""
		from nchantrs.widgets.calculators.calculators import NchantdCalculator
		self.assertIsNotNone(NchantdCalculator)
	
	def test_import_browser(self):
		"""Test that browser widgets can be imported"""
		from nchantrs.widgets.browsers.browsers import NchantdWebBrowser
		self.assertIsNotNone(NchantdWebBrowser)
	
	def test_import_calendar(self):
		"""Test that calendar widgets can be imported"""
		from nchantrs.widgets.calendars.calendars import NchantdCalendar
		self.assertIsNotNone(NchantdCalendar)
	
	def test_import_table(self):
		"""Test that table widgets can be imported"""
		from nchantrs.widgets.tables.tables import NchantdTable
		self.assertIsNotNone(NchantdTable)


class TestExampleApps(TestCase):
	"""Test the example applications"""
	
	def test_import_test_app_todos(self):
		"""Test that test_app_todos can be imported"""
		from tests import test_app_todos
		self.assertIsNotNone(test_app_todos)
	
	def test_import_test_app_calculator(self):
		"""Test that test_app_calculator can be imported"""
		from tests import test_app_calculator
		self.assertIsNotNone(test_app_calculator)
	
	def test_import_test_app_base(self):
		"""Test that test_app_base can be imported"""
        from tests import test_app_base
        self.assertIsNotNone(test_app_base)


if __name__ == "__main__":
	unittest_main(verbosity=2)
