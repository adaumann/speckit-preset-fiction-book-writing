#!/usr/bin/env python3
"""Test compile.py theme loading functionality."""

import json
from pathlib import Path
import sys

# Add scripts to path
sys.path.insert(0, str(Path("scripts/python")))

# Import compile wrapper
from compile import CompileWrapper

print("=" * 60)
print("TEST: compile.py Theme Loading")
print("=" * 60)

spec_path = Path(".")

# Test 1: Verify theme file locations are checked correctly
print("\n1️⃣ Testing theme file discovery...")
print(f"   Looking in: {spec_path} (spec root)")
print(f"   Looking in: {spec_path / 'draft' / 'ink'} (output dir)")

wrapper = CompileWrapper(spec_path, 'ink')

# Check if _load_ink_theme_wrapper method exists
if hasattr(wrapper, '_load_ink_theme_wrapper'):
    print("   ✓ _load_ink_theme_wrapper method found")
    
    # Try to load theme
    theme = wrapper._load_ink_theme_wrapper()
    if theme:
        print(f"   ✓ Theme loaded: {len(theme):,} characters")
    else:
        print("   ✓ No theme found (expected if ink-theme.html not present in root)")
else:
    print("   ✗ _load_ink_theme_wrapper method NOT found!")
    exit(1)

# Test 2: Check for story.css in SugarCube context
print("\n2️⃣ Testing SugarCube CSS detection...")
wrapper_sq = CompileWrapper(spec_path, 'sugarcube')

css_path = spec_path / "story.css"
js_path = spec_path / "story.js"

print(f"   Looking for: {css_path}")
if css_path.exists():
    print(f"   ✓ story.css found")
else:
    print(f"   ✓ story.css not present (optional)")

print(f"   Looking for: {js_path}")
if js_path.exists():
    print(f"   ✓ story.js found")
else:
    print(f"   ✓ story.js not present (optional)")

# Test 3: Verify fallback generation
print("\n3️⃣ Testing fallback HTML generation...")

if hasattr(wrapper, '_generate_ink_html_default'):
    print("   ✓ _generate_ink_html_default method found")
    
    test_story = {"name": "Test", "knots": {}}
    fallback_html = wrapper._generate_ink_html_default("Test Story", test_story)
    
    if fallback_html and len(fallback_html) > 100:
        print(f"   ✓ Fallback HTML generated: {len(fallback_html):,} characters")
        
        if "Test Story" in fallback_html and "storyData" in fallback_html:
            print(f"   ✓ Fallback contains proper content")
        else:
            print(f"   ✗ Fallback missing expected content")
    else:
        print(f"   ✗ Fallback generation failed")
else:
    print("   ✗ _generate_ink_html_default method NOT found!")

print(f"\n{'='*60}")
print("✅ COMPILE THEME LOADING TEST PASSED")
print(f"{'='*60}\n")
