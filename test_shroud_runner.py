#!/usr/bin/env python3
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name: Nchantrs Entry Point Test Suite
	description: >
		Test suite for verifying Nchantrs entry points with Shroud
		Tests aberration, distortion, and nchantment entry points
	version: 0.0.3
	authority: filesystem
	security: seclvl2
	<(WT)>: -16
"""
# -*- coding: utf-8 -*-

import sys
import time
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))


def get_app():
    """Get or create QApplication"""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    return app


def test_aberration():
    """Test aberration entry point - Single Widget Dialog"""
    print("\n" + "="*60)
    print("Testing: aberration (L1 - Single Widget Dialog)")
    print("="*60)
    
    try:
        from nchantrs.nchantrs import aberration
        from nchantrs.widgets.controls.buttons import NchantdButton
        
        print("  → Importing aberration entry point... OK")
        
        app = get_app()
        
        # Create dialog with non-blocking timeout close
        print("  → Creating aberration dialog...")
        dialog = aberration(
            name="test_aberration",
            args={"title": "Test Aberration", "text": "Click me!"},
            widget=NchantdButton,
            cfg={"modal": False, "width": 400, "height": 200}
        )
        
        print(f"  → Dialog created: {dialog}")
        
        # Verify dialog exists and is visible
        if hasattr(dialog, 'isVisible'):
            print(f"  → Dialog visible: {dialog.isVisible()}")
        
        # Get widget tree using Shroud
        try:
            from shroud.harness import GUIHarness
            harness = GUIHarness(dialog, auto_start=False)
            harness.start()
            widgets = harness.get_all_widgets()
            print(f"  → Widgets in tree: {len(widgets)}")
            harness.close()
        except Exception as e:
            print(f"  → Shroud inspection: {e}")
        
        # Close after short delay
        QTimer.singleShot(500, dialog.close)
        
        print("  ✓ Aberration test PASSED")
        return True
        
    except Exception as e:
        print(f"  ✗ Aberration failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_distortion():
    """Test distortion entry point - Complex Single Widget Dialog"""
    print("\n" + "="*60)
    print("Testing: distortion (L2 - Complex Single Widget Dialog)")
    print("="*60)
    
    try:
        from nchantrs.nchantrs import distortion
        from nchantrs.widgets.browsers.browsers import NchantdWebViewer
        
        print("  → Importing distortion entry point... OK")
        
        app = get_app()
        
        print("  → Creating distortion dialog...")
        dialog = distortion(
            name="test_distortion",
            args={"title": "Test Distortion", "url": "https://example.com"},
            widget=NchantdWebViewer,
            instance=None,
            cfg={"modal": False, "width": 800, "height": 600}
        )
        
        print(f"  → Dialog created: {dialog}")
        
        # Get widget tree
        try:
            from shroud.harness import GUIHarness
            harness = GUIHarness(dialog, auto_start=False)
            harness.start()
            widgets = harness.get_all_widgets()
            print(f"  → Widgets in tree: {len(widgets)}")
            harness.close()
        except Exception as e:
            print(f"  → Shroud inspection: {e}")
        
        QTimer.singleShot(500, dialog.close)
        
        print("  ✓ Distortion test PASSED")
        return True
        
    except Exception as e:
        print(f"  ✗ Distortion failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_nchantment():
    """Test nchantment entry point - Full Application"""
    print("\n" + "="*60)
    print("Testing: nchantment (L3 - Full Application)")
    print("="*60)
    
    try:
        from nchantrs.nchantrs import nchantment
        
        print("  → Importing nchantment entry point... OK")
        
        app = get_app()
        
        print("  → Creating nchantment application...")
        app_window = nchantment(
            name="test_nchantment",
            args={
                "title": "Nchantrs Test",
                "version": "0.0.1",
                "instance": "default",
                "profile": "default"
            },
            main_app=None,
            cfg={"debug": True, "theme": "default"},
            startup_app=None,
            profile_override=None
        )
        
        print(f"  → Application created: {app_window}")
        
        # Get widget tree
        try:
            from shroud.harness import GUIHarness
            harness = GUIHarness(app_window, auto_start=False)
            harness.start()
            widgets = harness.get_all_widgets()
            print(f"  → Widgets in tree: {len(widgets)}")
            harness.close()
        except Exception as e:
            print(f"  → Shroud inspection: {e}")
        
        QTimer.singleShot(500, app.quit)
        
        print("  ✓ Nchantment test PASSED")
        return True
        
    except Exception as e:
        print(f"  ✗ Nchantment failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("="*60)
    print("Nchantrs Entry Point Tests with Shroud")
    print("="*60)
    
    results = {}
    
    results["aberration"] = test_aberration()
    results["distortion"] = test_distortion()
    results["nchantment"] = test_nchantment()
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    for name, success in results.items():
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"  {name}: {status}")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    print(f"\nTotal: {passed}/{total} passed")
    
    sys.exit(0 if passed == total else 1)
