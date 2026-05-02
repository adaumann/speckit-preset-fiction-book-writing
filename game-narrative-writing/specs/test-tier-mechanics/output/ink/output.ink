// Test Tier Mechanics
// Author: Speckit Test Suite
// Version: 1.0.0
// Test suite for Tier 1/2/3 mechanic system

-> node_001_start

// Start Node
=== node_001_start ===
Welcome to the test story!

~ game_started = true
~ act_counter += 1
~ has_rusty_key = true

You wake up in a mysterious room.

* [Explore the room] -> NODE_002_tier2_demo
* [Check inventory] -> NODE_003_tier3_demo

// Tier 2 Mechanics Demo
=== node_002_tier2_demo ===
You enter a library. There's a mysterious figure studying an ancient tome.

// KNOWLEDGE (Tier 2) — not supported in Ink; requires SugarCube/Escoria
// FACTION (Tier 2) — not supported in Ink; requires SugarCube/Escoria
// LOCATION_STATE (Tier 2) — not supported in Ink; requires SugarCube/Escoria
// OBJECT_STATE (Tier 2) — not supported in Ink; requires SugarCube/Escoria
// CLUE (Tier 2) — not supported in Ink; requires SugarCube/Escoria

The scholar nods at you knowingly. You feel like something important just happened.

* [Question the scholar] -> NODE_001_start
* [Examine the objects] -> NODE_003_tier3_demo

// Tier 3 Mechanics Demo
=== node_003_tier3_demo ===
You step into a grand chamber. Interactive elements surround you.

// VERB (Tier 3) — not supported in Ink; requires SugarCube/Escoria
// MOVE (Tier 3) — not supported in Ink; requires SugarCube/Escoria
// HOTSPOT (Tier 3) — not supported in Ink; requires SugarCube/Escoria
// AUDIO (Tier 3) — not supported in Ink; requires SugarCube/Escoria
// INVENTORY_COMBINE (Tier 3) — not supported in Ink; requires SugarCube/Escoria
// GATED_CHOICE (Tier 3) — not supported in Ink; requires SugarCube/Escoria

The statue glows with an ethereal light. You hear haunting music echo through the chamber.

What do you do?

* [Use the ornate key] -> NODE_001_start
* [Leave the chamber] -> NODE_002_tier2_demo
