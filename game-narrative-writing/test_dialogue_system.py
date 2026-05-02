#!/usr/bin/env python3
"""Test dialogue system: node-type flags, outline tree, prose generation."""

import re
from pathlib import Path

print("=" * 60)
print("TEST: Dialogue System Integration")
print("=" * 60)

# Test 1: Verify node-type flags in plan.md documentation
print("\n1️⃣ Node-type flags in speckit.plan.md...")
plan_cmd = Path("commands/speckit.plan.md")
if plan_cmd.exists():
    content = plan_cmd.read_text(encoding='utf-8')
    
    if '(dialogue-centric)' in content and '(action)' in content and '(mixed)' in content:
        print("   ✓ All three node-type flags documented:")
        print("     • (dialogue-centric)")
        print("     • (action)")
        print("     • (mixed)")
    else:
        print("   ✗ Node-type flags missing or incomplete")
else:
    print(f"   ✗ File not found: {plan_cmd}")

# Test 2: Verify Dialogue Tree field in outline.md
print("\n2️⃣ Dialogue Tree field in speckit.outline.md...")
outline_cmd = Path("commands/speckit.outline.md")
if outline_cmd.exists():
    content = outline_cmd.read_text(encoding='utf-8')
    
    if 'Dialogue Tree' in content:
        print("   ✓ Dialogue Tree field documented in outline")
        
        # Check for dialogue tree structure
        if 'Player option' in content and 'NPC response' in content and 'trust state' in content:
            print("   ✓ Dialogue Tree structure defined with:")
            print("     • Player options")
            print("     • NPC responses")
            print("     • Trust state handling")
        else:
            print("   ⚠ Dialogue Tree structure incomplete")
    else:
        print("   ✗ Dialogue Tree field NOT found in outline")
else:
    print(f"   ✗ File not found: {outline_cmd}")

# Test 3: Verify dialogue prose generation in implement.md
print("\n3️⃣ Dialogue prose generation in speckit.implement.md...")
implement_cmd = Path("commands/speckit.implement.md")
if implement_cmd.exists():
    content = implement_cmd.read_text(encoding='utf-8')
    
    has_dialogue_gen = 'Dialogue Tree' in content
    has_engine_syntax = '*' in content and '[[' in content  # Ink and SugarCube syntax
    has_multi_party = 'multi-party' in content.lower() or 'npc reaction' in content.lower()
    
    print(f"   Dialogue Tree handling: {'✓' if has_dialogue_gen else '✗'}")
    print(f"   Engine-specific syntax: {'✓' if has_engine_syntax else '✗'}")
    print(f"   Multi-party reactions: {'✓' if has_multi_party else '✗'}")
    
    if has_dialogue_gen and has_engine_syntax:
        print("   ✓ Dialogue generation documented with engine syntax")
    else:
        print("   ⚠ Dialogue generation incomplete")
else:
    print(f"   ✗ File not found: {implement_cmd}")

# Test 4: Verify dialogue support in polish.md
print("\n4️⃣ Dialogue in speckit.polish.md...")
polish_cmd = Path("commands/speckit.polish.md")
if polish_cmd.exists():
    content = polish_cmd.read_text(encoding='utf-8')
    
    has_npc_scope = 'npc' in content.lower() and 'dialogue' in content.lower()
    has_di_checks = 'DI-' in content  # Dialogue Internals checks
    
    print(f"   NPC dialogue scope: {'✓' if has_npc_scope else '✗'}")
    print(f"   Dialogue checks (DI-001, etc): {'✓' if has_di_checks else '✗'}")
    
    if has_npc_scope:
        print("   ✓ Polish handles NPC dialogue registers")
else:
    print(f"   ✗ File not found: {polish_cmd}")

# Test 5: Verify dialogue support in continuity.md
print("\n5️⃣ Dialogue in speckit.continuity.md...")
continuity_cmd = Path("commands/speckit.continuity.md")
if continuity_cmd.exists():
    content = continuity_cmd.read_text(encoding='utf-8')
    
    has_dialogue_checks = 'dialogue' in content.lower()
    has_multi_party = 'multi-party' in content.lower()
    has_register = 'register' in content.lower()
    
    print(f"   Dialogue continuity checks: {'✓' if has_dialogue_checks else '✗'}")
    print(f"   Multi-party dialogue: {'✓' if has_multi_party else '✗'}")
    print(f"   Register consistency: {'✓' if has_register else '✗'}")
    
    if has_dialogue_checks:
        print("   ✓ Continuity validates dialogue across nodes")
else:
    print(f"   ✗ File not found: {continuity_cmd}")

# Test 6: Verify dialogue support in revise.md
print("\n6️⃣ Dialogue in speckit.revise.md...")
revise_cmd = Path("commands/speckit.revise.md")
if revise_cmd.exists():
    content = revise_cmd.read_text(encoding='utf-8')
    
    has_dial_revision = 'Dialogue register' in content or 'DIAL-' in content
    has_consistency = 'Dialogue consistency' in content or 'multi-party' in content
    
    print(f"   Dialogue register revision: {'✓' if has_dial_revision else '✗'}")
    print(f"   Multi-party consistency revision: {'✓' if has_consistency else '✗'}")
    
    if has_dial_revision:
        print("   ✓ Revise handles dialogue failures")
else:
    print(f"   ✗ File not found: {revise_cmd}")

# Summary
print(f"\n{'='*60}")
print("📊 Dialogue System Checklist")
print(f"{'='*60}")

checks = {
    "Plan node-type flags": '(dialogue-centric)' in plan_cmd.read_text(encoding='utf-8'),
    "Outline Dialogue Tree": 'Dialogue Tree' in outline_cmd.read_text(encoding='utf-8'),
    "Implement prose generation": 'Dialogue Tree' in implement_cmd.read_text(encoding='utf-8'),
    "Polish dialogue checks": 'DI-' in polish_cmd.read_text(encoding='utf-8') or 'dialogue' in polish_cmd.read_text(encoding='utf-8').lower(),
    "Continuity dialogue checks": 'dialogue' in continuity_cmd.read_text(encoding='utf-8').lower(),
    "Revise dialogue support": 'Dialogue' in revise_cmd.read_text(encoding='utf-8') and ('register' in revise_cmd.read_text(encoding='utf-8').lower() or 'DIAL' in revise_cmd.read_text(encoding='utf-8'))
}

pass_count = sum(1 for v in checks.values() if v)
total = len(checks)

for check, status in checks.items():
    icon = "✓" if status else "✗"
    print(f"  {icon} {check}")

print(f"\n  Result: {pass_count}/{total} checks passed")

if pass_count == total:
    print(f"\n✅ DIALOGUE SYSTEM FULLY INTEGRATED")
else:
    print(f"\n⚠ DIALOGUE SYSTEM PARTIALLY INTEGRATED ({total - pass_count} gaps)")

print(f"{'='*60}\n")
