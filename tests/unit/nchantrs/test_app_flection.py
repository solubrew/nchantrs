#!/usr/bin/env python3
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name: Flection Test App
	description: >
		Test application demonstrating flection entry point
		Flection executes a complex Nchantrs application supervisor with defined storage and installation paths
		Includes Pyularity for app updates and management 0.0
	version:.0.0.0.1
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*-

# Usage:
# from nchantrs.nchantrs import flection
# supervisor = flection("MyApp", args, main_app=None, cfg=None, startup_app=None, profile_override=None)


if __name__ == "__main__":
    from nchantrs.nchantrs import flection

    # Flection - App supervisor with Pyularity
    # Example: Launch Nchantrs with update supervisor
    supervisor = flection(
        name="test_flection",
        args={
            "title": "Nchantrs Supervised Application",
            "version": "0.0.1",
            "instance": "latest",
            "profile": "default",
            "auto_update": True
        },
        main_app=None,  # Uses default NchantdCloak
        cfg={"debug": True, "theme": "default", "update_check": True},
        startup_app=None,  # Uses default NchantdApplicationStartupWizard
        profile_override=None
    )

    print(f"Supervisor started: {supervisor}")
