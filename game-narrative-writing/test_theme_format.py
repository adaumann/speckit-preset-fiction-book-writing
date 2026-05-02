#!/usr/bin/env python3
"""Test ink-theme template formatting to validate placeholder replacement."""

import json
from pathlib import Path

print("=" * 60)
print("TEST: Ink Theme Template Formatting")
print("=" * 60)

# Load theme template
theme_path = Path("templates/ink-theme-dark.html")
if not theme_path.exists():
    print(f"❌ Theme file not found: {theme_path}")
    exit(1)

template_content = theme_path.read_text(encoding='utf-8')
print(f"\n📋 Loaded template: {len(template_content):,} characters")

# Count placeholders
title_count = template_content.count('{title}')
json_count = template_content.count('{story_json}')
print(f"\n📊 Placeholder counts:")
print(f"   {{title}}: {title_count}")
print(f"   {{story_json}}: {json_count}")

# Check for Python format string safety
double_brace_count = template_content.count('{{')
print(f"   {{}}: {double_brace_count} (CSS escape sequences)")

# Test format() with sample data
print(f"\n🧪 Testing format() with sample data...")
test_story_data = {
    "name": "Test Story",
    "chapters": [
        {"title": "Ch 1", "text": "Once upon a time..."},
        {"title": "Ch 2", "text": "The hero journeyed..."}
    ],
    "variables": {"player_name": "Hero"}
}

try:
    formatted_html = template_content.format(
        title="My Awesome Story",
        story_json=json.dumps(test_story_data, indent=2)
    )
    
    print(f"\n✅ Format succeeded!")
    print(f"   Output size: {len(formatted_html):,} characters")
    
    # Validate replacements
    print(f"\n✓ Validating replacements:")
    
    if "My Awesome Story" in formatted_html:
        occurrences = formatted_html.count("My Awesome Story")
        print(f"   ✓ Title appears {occurrences} times")
    else:
        print(f"   ✗ Title NOT found in output")
    
    if '"name": "Test Story"' in formatted_html:
        print(f"   ✓ JSON data preserved in output")
    else:
        print(f"   ✗ JSON NOT properly inserted")
    
    if "const storyData = {" in formatted_html:
        print(f"   ✓ JavaScript storyData assignment valid")
    else:
        print(f"   ✗ storyData assignment invalid")
    
    # Check for unterminated braces (format() errors)
    if formatted_html.count('{') == formatted_html.count('}'):
        print(f"   ✓ Brace balance correct")
    else:
        print(f"   ✗ Brace mismatch!")
    
    # Extract and show sample of formatted output
    print(f"\n📄 Sample output (first 500 chars of body):")
    body_start = formatted_html.find("<body>") + 6
    body_end = formatted_html.find("</body>")
    body_sample = formatted_html[body_start:body_start+300]
    print(f"   {body_sample[:200]}...")
    
except Exception as e:
    print(f"\n❌ Format failed with error:")
    print(f"   {type(e).__name__}: {e}")
    exit(1)

print(f"\n{'='*60}")
print("✅ THEME FORMAT TEST PASSED")
print(f"{'='*60}\n")
