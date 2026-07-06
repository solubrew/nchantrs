#!/usr/bin/env python3
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name: Nchantment Test App
	description: >
		Test application demonstrating nchantment entry point
		Nchantment executes a full application with all features
	version: 0.0.0.0.0.1
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*-

# IMPORTANT: Do NOT create QApplication before calling nchantment
# nchantment creates its own QApplication via NchantdCloak

# Usage:
# from nchantrs.nchantrs import nchantment
# nchantment("MyApp", args={"title": "Hello"}, cfg={})


if __name__ == "__main__":
    from nchantrs.nchantrs import nchantment
    
    # Nchantment - Full application
    # Example: Launch a complete application
    nchantment(
        name="test_nchantment",
        args={"title": "Test Nchantment Application"},
        cfg={"modal": False, "width": DEFAULT_WINDOW_WIDTH, "height": 800}
    )
