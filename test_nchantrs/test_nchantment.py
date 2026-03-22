# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name: Nchantment Test App
	description: >
		Example of nchantment (L3) entry point - full application
	version: 0.0.0.0.0.0
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*
import sys
from os.path import dirname, join

# Add nchantrs to path
here = join(dirname(__file__), "")
sys.path.insert(0, here)

from nchantrs.nchantrs import nchantment


if __name__ == "__main__":
    print("="*60)
    print("Testing Nchantment (L3 Entry Point)")
    print("="*60)
    
    # Call nchantment entry point
    # This launches a full Nchantrs application with startup wizard
    nchantment(
        name="Test Nchantment",
        args={"instance": "test"},  # Use 'test' for testing without wizard
        main_app=None,  # Uses default NchantdCloak
        cfg={"title": "Nchantment Test"},
        startup_app=None,  # Uses default startup wizard
        profile_override=None
    )
    
    print("Nchantment complete")
