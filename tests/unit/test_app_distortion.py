#!/usr/bin/env python3
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name: Distortion Test App
	description: >
		Test application demonstrating distortion entry point
		Distortion executes a complex single widget dialog useful for direct interaction widgets
	version: 0.0.0.0.0.1
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*-

# IMPORTANT: Do NOT create QApplication before calling distortion
# distortion (NchantdCape) is a QApplication subclass and creates its own

# Usage:
# from nchantrs.nchantrs import distortion
# distortion("MyComplexDialog", args, widget=NchantdWebViewer, instance=None, cfg={})


if __name__ == "__main__":
    from nchantrs.nchantrs import distortion
    from nchantrs.widgets.browsers.browsers import NchantdWebViewer
    
    # Distortion - Complex single widget dialog
    # Example: Launch a web viewer dialog
    distortion(
        name="test_distortion",
        args={"title": "Web Browser", "url": "https://example.com"},
        widget=NchantdWebViewer,
        instance=None,
        cfg={"modal": True, "width": 800, "height": 600}
    )
