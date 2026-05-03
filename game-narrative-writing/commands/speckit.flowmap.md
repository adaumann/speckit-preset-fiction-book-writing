---
description: Generate or update a Mermaid flowchart of the node graph with mechanic trigger annotations, ending markers, and act boundary labels.
handoffs:
  - label: Update Plan
    agent: speckit.plan
    prompt: The plan.md source needs updating based on the diagram
    send: false
  - label: Analyze Unreachable Nodes
    agent: speckit.analyze
    prompt: Check for unreachable nodes visible in the diagram
    send: true
---

# speckit.flowmap

Generate a Mermaid flowchart of the full node graph. Annotates mechanic triggers, ending nodes, and act boundaries.

## User Input

Provide one of:
- Nothing — generate full flowchart from all node files and `plan.md`
- `--act [N]` — diagram one act only
- `--endings` — highlight ending nodes only
- `--hooks` — annotate mechanic trigger types on edges

Optional flags:
- `--act [N]` — scope to one act
- `--endings` — bold or colour-code ending nodes
- `--hooks` — add edge labels for mechanic triggers (trust, flag, inventory check)
- `--output [filename]` — write to a named file instead of printing

## Pre-Execution Checks

1. Load `specs/plan.md` — authoritative node graph source.
2. Load all node files in `nodes/` to extract actual choice targets.
3. If node files exist: prefer actual node file links over plan.md estimates.

## Outline

1. **Build graph model**:
   - Every node becomes a Mermaid node (`NODE_001[Opening]`)
   - Every choice becomes a directed edge (`NODE_001 -->|choice label| NODE_002`)
   - Gated choices: annotate the condition on the edge label (e.g. `-->|"Trust ≥ 75: Tell me"| NODE_005`)
   - Terminal/ending nodes: marked with double-bracket shape `NODE_END_A[[Ending A]]`
   - Act boundaries: add comment dividers `%% ACT 1 %%`
   - **Hub nodes**: if a node is tagged `hub` in `plan.md`, render it with a stadium shape `NODE_HUB([Hub Label])` and annotate topic sub-nodes as `:::hub-topic`; add a `%% DIALOGUE HUB %%` comment above the hub node group

2. **Mechanic annotations** (if `--hooks`):
   - Trust shift: append `[±N trust]` to edge label
   - Flag set: append `[flag_name=true]` to edge label
   - Inventory change: append `[+item / -item]` to edge label
   - Ending condition trigger: append `[end_A_progress+1]`

3. **Unreachable nodes** (cross-reference with speckit.analyze):
   - Shade or mark nodes with no incoming edges as `:::orphan`

4. **Output**:
   ```mermaid
   flowchart TD
   %% ACT 1 %%
   NODE_001[Opening]
   NODE_001 -->|"A: Ask for help"| NODE_002A
   NODE_001 -->|"B: Walk away"| NODE_002B
   ...
   NODE_END_A[[Ending A — Redemption]]
   NODE_END_B[[Ending B — Exile]]
   ```
   - Write to `flowmap-diagram.md` or specified `--output` file
   - Report: "Diagram generated: [N] nodes, [N] edges, [N] ending nodes."
