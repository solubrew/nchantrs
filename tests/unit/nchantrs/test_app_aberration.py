#!/usr/bin/env python3
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name: Aberration Test App
	description: >
		Test application demonstrating aberration entry point
		Aberration executes a single widget dialog useful for direct interaction widgets
	version: 0.0.0.0.0.1
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*-

# Usage:
# from nchantrs.nchantrs import aberration
# aberration("MyDialog", args={"title": "Hello"}, widget=NchantdButton, cfg={})


if __name__ == "__main__":
    from nchantrs.nchantrs import aberration
    from nchantrs.widgets.controls.buttons import NchantdButton

    # Aberration - Single widget dialog
    # Example: Launch a simple button dialog
    aberration(
        name="test_aberration",
        args={"title": "Test Aberration Dialog", "text": "Hello from Aberration!"},
        widget=NchantdButton,
        cfg={"modal": True, "width": 400, "height": 200}
    )
