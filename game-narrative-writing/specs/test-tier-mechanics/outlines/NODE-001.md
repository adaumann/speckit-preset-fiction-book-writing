---
node_id: NODE-001
title: Start
act: 1
status: APPROVED
pov: second-person
variables_read: []
variables_set:
  - visited_start
  - player_choice
choices_read: 2
outline_ref: specs/test-tier-mechanics/spec.yml
---

# NODE-001: Start

## Summary
The player awakens in a test chamber. This is the entry point for the tier mechanics demo.

## Beats
1. Establish scene: cold, clinical environment with flickering lights
2. Player realizes they can see game state via mechanic hooks
3. Present choice: explore the chamber or examine equipment

## Variables
| Variable | Type | Direction | Notes |
|----------|------|-----------|-------|
| visited_start | flag | set | Track first visit |
| player_choice | string | set | Remember which path chosen |

## NPCs & Dialogue
- None (solo scene)

## Choices

| Choice | Target | Condition | Effect |
|--------|--------|-----------|--------|
| Look around carefully | NODE-002 | - | Sets VISITED flag |
| Check the equipment | NODE-002 | - | Sets COUNTER mechanic |

## Mechanics to Test

- VISITED: Mark visited_start flag
- CHOICE_MEMORY: Record which path player chose

## Notes
- This is the minimal viable start node
- Tests Tier 1 mechanics: FLAG and CHOICE_MEMORY
- Node-002 will test Tier 2 mechanics
