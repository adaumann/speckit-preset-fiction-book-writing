---
description: POV architecture — design, audit, schedule, and validate point-of-view structure for single-POV and multi-POV narratives. Works with any plot structure.
handoffs:
  - label: Update Story Structure
    agent: speckit.plan
    prompt: Update plan.md to reflect the POV schedule from pov-structure.md
    send: true
  - label: Audit Voice Differentiation
    agent: speckit.continuity
    prompt: Check drafted chapters for POV voice consistency and information leakage
    send: true
scripts:
  sh: scripts/bash/check-prerequisites.sh --json
  ps: scripts/powershell/check-prerequisites.ps1 -Json
agent_scripts:
  sh: scripts/bash/update-agent-context.sh __AGENT__
  ps: scripts/powershell/update-agent-context.ps1 -AgentType __AGENT__
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

Sub-modes are selected from `$ARGUMENTS`:
- `draft` — create `pov-structure.md` from scratch using `spec.md` and `plan.md`
- `audit` — audit voice differentiation across all POV characters
- `schedule` — generate or validate the chapter-by-chapter POV schedule
- `asymmetry` — check information asymmetry: who knows what, and when
- `relay` — review and tighten POV handoff points between chapters
- Any free-text question about POV design is answered directly without updating files

## Pre-Execution Checks

**Check for extension hooks (before POV planning)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_pov` key.
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

## Goal

POV architecture governs which minds the reader inhabits, in what sequence, and to what effect. It applies to every story — single-POV and multi-POV alike. This command manages that layer of craft and ensures that:

1. The POV mode is correctly identified and documented (single or multi)
2. POV voice is distinct, consistent, and appropriate to the character's wound and arc
3. Information asymmetry is deliberate and serves the story's tension
4. The POV schedule aligns with the plot structure and pacing needs (multi-POV)
5. Relay transitions between POV chapters feel earned, not arbitrary (multi-POV)
6. No POV character "knows" something their position in the story forbids

## POV Mode Reference

Use this reference when drafting or auditing `pov-structure.md`:

| Mode | Core mechanic | Best for |
|---|---|---|
| **Alternating** | Named chapters, one POV each | Commercial fiction, thriller, multi-strand drama |
| **Dual narrative** | 2 POVs; often different timelines or social mirrors | Suspense, literary fiction with strong foil structure |
| **Braided** | 3+ storylines converge at structural joints | Epic fiction, historical multilayered narratives |
| **Ensemble** | 4+ equal-weight POVs, episodic | Community stories, sprawling family sagas |
| **Mosaic** | Many short fragments, POV tied to theme not plot | Literary fiction, experimental structure |
| **Frame + Embedded** | Outer narrator frames inner narrators | Gothic, unreliable narrator, metafiction |
| **Chorus / Community** | Collective "we" with individual emergence | Loss narratives, community witness stories |
| **First-person-multiple** | Each POV uses "I"; voice must differentiate | High-literary fiction, maximum interiority |

## Execution Steps

### Step 1 — Setup and Document Load

Run `{SCRIPT}` and parse `FEATURE_DIR`.

Load available documents:
- Required: `spec.md`
- If present: `plan.md`, `pov-structure.md`, `characters.md`, `characters/` profiles, `timeline.md`
- If present: `draft/*.md` (needed for `audit`, `asymmetry`, `relay` modes)

Report what was found and what is missing. If `spec.md` is absent, abort with a clear error.

### Step 2 — Route to Sub-Mode

Branch on `$ARGUMENTS`:

---

#### Sub-mode: `draft`

**Goal**: Create `FEATURE_DIR/pov-structure.md` from `spec.md` (and `plan.md` if present).

1. Read `spec.md`:
   - Extract all characters with defined arcs (P1, P2, P3…)
   - Extract `POV Strategy` from the Narrative Parameters table if present
   - Extract `Plot Structure` from the Narrative Parameters table
   - Extract the story's central dramatic question

2. Determine POV mode:
   - If `spec.md` names a POV mode explicitly, use it
   - If only one character has a defined arc, default to single-POV; confirm with the user before drafting multi-POV structure
   - If multiple characters have defined arcs, reason over which POV mode best fits the story's structure and propose it with justification
   - State 2–3 alternative modes with trade-offs

3. **If single POV**: create `pov-structure.md` with:
   - POV Configuration (mode: Single POV, one character)
   - One POV Character Profile with voice fingerprint and information profile
   - Information Asymmetry Map (dramatic irony and mystery still apply to single-POV)
   - POV Schedule (single-POV block — verify every chapter maps to the same narrator)
   - Continuity Constraints (tense consistency, narrative distance drift, knowledge fencing)
   - Skip: Voice Differentiation Matrix, Convergence Points, Relay Rules, Arc Weighting

4. **If multi-POV**: for each POV candidate character:
   - Extract: wound, want, need, transformation (from spec.md)
   - Draft a voice fingerprint (3–5 distinguishing features) from the character arc and any notes
   - Identify what this POV uniquely enables that no other POV could provide
   - Flag if a POV character's arc is too similar to another's (homogeneity risk)

5. Draft the Information Asymmetry Map:
   - List each plot secret / revelation from `spec.md`
   - Assign which characters know it, from what chapter, and when the reader learns it
   - Flag any asymmetry that feels contrived ("withholding this feels forced") vs. earned ("the reader genuinely doesn't have access to this through any POV")

6. **Multi-POV only** — Draft the Convergence Points:
   - Identify where the plot structure requires multiple POV characters to occupy the same moment (midpoint, climax, etc.)
   - Ensure convergence points are mapped to specific chapters in plan.md (if plan.md exists)

7. Draft the POV Schedule:
   - **Single POV**: verify all `plan.md` chapter entries map to the narrator; flag any deviations for Deviation Notes
   - **Multi-POV**: propose chapter-by-chapter POV assignments aligned with `plan.md ## Scene Outline`; apply the POV order logic appropriate to the chosen mode; highlight any beats where POV assignment is unclear

8. Write `FEATURE_DIR/pov-structure.md` using `pov-structure-template.md` as the schema.

9. Report what was created and what fields remain `[NEEDS CLARIFICATION]`.

---

#### Sub-mode: `audit`

**Goal**: Audit whether drafted chapters maintain genuine POV voice consistency (single POV) or voice differentiation (multi-POV).

1. Load all `draft/*.md` files. For each, read the frontmatter field `pov_character`.

2. **If single POV**:
   - Verify all chapters share the same `pov_character` value. Flag any deviation.
   - For the narrator, check consistency across chapters:
     - Tense: does it drift (past → present or vice versa)?
     - Narrative distance: does it slip from close-limited to omniscient without justification?
     - Voice: do sentence rhythm, vocabulary field, and emotional register stay consistent with the POV Character Profile in `pov-structure.md`?
     - Knowledge fencing: does the narrator reference something they could not yet know at that chapter?
   - Report: Single-POV Consistency Audit Table

   | Dimension | Chapters checked | Verdict | Flagged passages | Recommendation |
   |---|---|---|---|---|
   | Tense consistency | [count] | [PASS/WARN/FAIL] | | |
   | Narrative distance | [count] | [PASS/WARN/FAIL] | | |
   | Voice consistency | [count] | [PASS/WARN/FAIL] | | |
   | Knowledge fencing | [count] | [PASS/WARN/FAIL] | | |

3. **If multi-POV**: for each POV character with at least 2 drafted chapters:
   - Sample 3–4 paragraphs of interiority from different chapters
   - Apply the Voice Differentiation Matrix from `pov-structure.md`:
     - Sentence length default: does it match the profile?
     - Sensory channel: is it consistent with the character's profile?
     - Emotional register: is the distance / tone consistent?
     - Vocabulary field: are characteristic words present?
     - Interiority level: is it consistent?
   - Identify any passage that could be mistaken for another POV character's voice
   - Flag: `PASS`, `WARN` (correctable), or `FAIL` (voices are indistinct)

4. Report: Voice Differentiation Audit Table

| POV Character | Chapters audited | Verdict | Flagged passages | Recommendation |
|---|---|---|---|---|
| [Name] | [count] | [PASS/WARN/FAIL] | [IDs] | [Fix or None] |

4. If any FAIL: quote the specific passage, explain why it fails the fingerprint, and suggest a revision approach without rewriting the prose.

---

#### Sub-mode: `schedule`

**Goal**: Generate or validate the POV schedule against `plan.md ## Scene Outline`.

1. Load `plan.md ## Scene Outline`. Extract all chapter entries with their POV fields.

2. Check:
   - Every chapter has a `POV` field populated (not `[NEEDS CLARIFICATION]`)
   - No two consecutive chapters share the same POV when the mode is `alternating` or `dual` (flag if so — may be intentional but needs justification)
   - The distribution of chapters per POV matches the Arc Weighting in `pov-structure.md`
   - Convergence points from `pov-structure.md` have matching chapter IDs in `plan.md`
   - The final chapter (closing image) is assigned to the POV justified in `pov-structure.md`

3. If `pov-structure.md` does not exist yet:
   - Generate a proposed POV schedule from `plan.md` based on the best-fit assignments
   - Output as a schedule table the user can paste into `pov-structure.md`

4. Report: POV Schedule Table with PASS/WARN/FAIL per row.

| Chapter ID | Chapter Name | Assigned POV | Mode Check | Arc Weight Check | Convergence Check |
|---|---|---|---|---|---|
| [ID] | [Name] | [POV] | [PASS/WARN] | [PASS/WARN] | [N/A / PASS / FAIL] |

---

#### Sub-mode: `asymmetry`

**Goal**: Validate that no POV character "knows" something they shouldn't at any given chapter.

1. Load: `pov-structure.md ## Information Asymmetry Map`, `plan.md ## Scene Outline`, and all available `draft/*.md` files.

2. For each secret/revelation in the Asymmetry Map:
   - Find the chapter(s) where each POV character is stated to learn this fact
   - Search all drafted chapters written from that POV character's perspective that occur BEFORE that chapter
   - Flag any passage where the character appears to have prior knowledge they should not have (explicit statement, implicit assumption, or telling inference)

3. Narrator-level violations:
   - Check for passages where the narration provides information that would require the POV character to know something outside their scope
   - Flag "author intrusion" — where the narrative voice slips from limited to omniscient without justification

4. Report: Information Asymmetry Audit Table

| Secret / Revelation | POV character | Chapter where they learn it | Earlier violation found | Severity | Recommended fix |
|---|---|---|---|---|---|
| [Name] | [POV] | [Chapter ID] | [Chapter ID or None] | [CRITICAL/MAJOR/MINOR] | [Fix] |

---

#### Sub-mode: `relay`

**Goal**: Audit POV handoff points for momentum and editorial cohesion.

1. Identify all chapter-boundary transitions in `plan.md ## Scene Outline` where the POV changes.

2. For each transition:
   - Load the closing paragraph of chapter N and the opening paragraph of chapter N+1
   - Evaluate against the relay rules in `pov-structure.md ## Relay Rules`
   - Classify: `cliffhanger`, `echo`, `contrast`, `time-jump`, `thematic rhyme`, `flat` (no technique)
   - Flag `flat` transitions and any that violate the documented relay conventions

3. Report: Relay Audit Table

| Transition | Chapter N (ends) | Chapter N+1 (opens) | Relay type | Verdict | Suggestion |
|---|---|---|---|---|---|
| N→N+1 | [ID: last line summary] | [ID: first line summary] | [type] | [PASS/WARN/FAIL] | |

4. Offer to rewrite closing or opening lines for flagged transitions only if the user explicitly asks.

---

#### Free-text mode

If `$ARGUMENTS` is not one of the named sub-modes:
- Treat the input as a direct question about POV design for this story
- Answer with reference to `spec.md`, `plan.md`, and `pov-structure.md` where applicable
- Be concrete: reference specific characters, chapters, and plot structure stages
- Do not use theory in the abstract — ground every suggestion in this story's material

---

## Output Standards

- Use tables for all audit results; narrative prose only for recommendations
- Every `FAIL` or `WARN` must cite a specific chapter ID, passage, or file location
- Never rewrite prose unless the sub-mode explicitly produces output (draft) or the user asks
- When proposing POV assignments or schedule changes, always state the structural reasoning, not just the recommendation
- Flag contradictions between `pov-structure.md` and `plan.md` as `CONFLICT` — do not silently resolve them

## Constraints

- If no `pov-structure.md` exists and the sub-mode requires it, offer to create it (`draft` mode) before proceeding
- If `spec.md` shows only one POV character, default to Single POV mode and draft a single-POV `pov-structure.md` unless the user explicitly requests multi-POV
- The `relay` and `convergence` sub-modes are only meaningful for multi-POV; if run against a single-POV story, report "Not applicable for Single POV mode" and suggest `audit` instead
- Do not invent POV characters not present in `spec.md` or `characters.md`
- Information asymmetry violations are `CRITICAL` — they directly break story logic and reader trust
