#!/usr/bin/env python3
"""
Nchantrs Entry Point Test Suite
Tests aberration, distortion, nchantment entry points
"""
import sys
from pathlib import Path

# Add project to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))


def test_imports():
    """Test all imports work"""
    print("Testing imports...")
    
    from nchantrs.nchantrs import aberration, distortion, nchantment
    from nchantrs.widgets.controls.buttons import NchantdButton
    from nchantrs.widgets.browsers.browsers import NchantdWebViewer
    
    print("  ✓ All entry points imported")
    print("  ✓ All widgets imported")
    return True


def test_aberration_signature():
    """Test aberration signature"""
    print("\nTesting aberration signature...")
    
    from nchantrs.nchantrs import aberration
    from nchantrs.widgets.controls.buttons import NchantdButton
    
    # Verify callable with expected signature
    import inspect
    sig = inspect.signature(aberration)
    params = list(sig.parameters.keys())
    
    assert 'name' in params, "aberration missing 'name' param"
    assert 'args' in params, "aberration missing 'args' param"
    assert 'widget' in params, "aberration missing 'widget' param"
    assert 'cfg' in params, "aberration missing 'cfg' param"
    
    print(f"  ✓ aberration params: {params}")
    return True


def test_distortion_signature():
    """Test distortion signature"""
    print("\nTesting distortion signature...")
    
    from nchantrs.nchantrs import distortion
    import inspect
    sig = inspect.signature(distortion)
    params = list(sig.parameters.keys())
    
    assert 'name' in params, "distortion missing 'name' param"
    assert 'args' in params, "distortion missing 'args' param"
    assert 'widget' in params, "distortion missing 'widget' param"
    assert 'instance' in params, "distortion missing 'instance' param"
    assert 'cfg' in params, "distortion missing 'cfg' param"
    
    print(f"  ✓ distortion params: {params}")
    return True


def test_nchantment_signature():
    """Test nchantment signature"""
    print("\nTesting nchantment signature...")
    
    from nchantrs.nchantrs import nchantment
    import inspect
    sig = inspect.signature(nchantment)
    params = list(sig.parameters.keys())
    
    assert 'name' in params, "nchantment missing 'name' param"
    assert 'args' in params, "nchantment missing 'args' param"
    assert 'main_app' in params, "nchantment missing 'main_app' param"
    assert 'cfg' in params, "nchantment missing 'cfg' param"
    assert 'startup_app' in params, "nchantment missing 'startup_app' param"
    assert 'profile_override' in params, "nchantment missing 'profile_override' param"
    
    print(f"  ✓ nchantment params: {params}")
    return True


def test_entry_point_docs():
    """Test entry point documentation"""
    print("\nTesting entry point documentation...")
    
    from nchantrs.nchantrs import aberration, distortion, nchantment
    
    print(f"  aberration: {aberration.__doc__}")
    print(f"  distortion: {distortion.__doc__}")
    print(f"  nchantment: {nchantment.__doc__}")
    
    assert aberration.__doc__, "aberration has no docstring"
    assert distortion.__doc__, "distortion has no docstring"
    assert nchantment.__doc__, "nchantment has no docstring"
    
    print("  ✓ All entry points have documentation")
    return True


if __name__ == "__main__":
    print("="*60)
    print("Nchantrs Entry Point Test Suite")
    print("="*60)
    
    tests = [
        ("Import Test", test_imports),
        ("Aberration Signature", test_aberration_signature),
        ("Distortion Signature", test_distortion_signature),
        ("Nchantment Signature", test_nchantment_signature),
        ("Documentation Test", test_entry_point_docs),
    ]
    
    results = {}
    
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"  ✗ {name} failed: {e}")
            results[name] = False
    
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
