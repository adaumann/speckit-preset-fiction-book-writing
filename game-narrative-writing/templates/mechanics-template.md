# Mechanic Hook Schemas: [GAME_TITLE]

<!-- Reference document for all mechanic hooks used in this project.
     Cross-referenced by speckit.implement, speckit.checklist, speckit.continuity, and export.py.
     Only hooks declared as enabled in constitution.md Section II are active. -->

---

## Tier 1 Hooks — Fully Exported (v1.0)

### lag — Boolean State

`
[MECHANIC:FLAG set=[variable_name] value=true|false]
[MECHANIC:FLAG check=[variable_name]]
[conditional prose]
[/MECHANIC]
`

| Parameter | Sugarcube Export | Ink Export | Ren'Py |
|---|---|---|---|
| set=true | <<set $[var] to true>> | ~ [var] = true | $ [var] = True |
| set=false | <<set $[var] to false>> | ~ [var] = false | $ [var] = False |
| check (true) | <<if $[var]>>...<</if>> | {[var]: ...} | if [var]: |
| check (false) | <<if not $[var]>>...<</if>> | {not [var]: ...} | if not [var]: |

---

### counter — Integer Increment/Decrement

`
[MECHANIC:COUNTER set=[variable_name] delta=+1|-1|N]
[MECHANIC:COUNTER check=[variable_name] op=gte|lte|eq value=N]
[conditional prose]
[/MECHANIC]
`

| Parameter | Sugarcube Export | Ink Export | Ren'Py |
|---|---|---|---|
| delta=+1 | <<set $[var] += 1>> | ~ [var]++ | $ [var] += 1 |
| delta=-1 | <<set $[var] -= 1>> | ~ [var]-- | $ [var] -= 1 |
| delta=N | <<set $[var] += N>> | ~ [var] += N | $ [var] += N |
| check gte N | <<if $[var] gte N>>...<</if>> | {[var] >= N: ...} | if [var] >= N: |
| check lte N | <<if $[var] lte N>>...<</if>> | {[var] <= N: ...} | if [var] <= N: |
| check eq N | <<if $[var] is N>>...<</if>> | {[var] == N: ...} | if [var] == N: |

---

### isited — Node Seen Tracking

`
[MECHANIC:VISITED set=[variable_name]]
[MECHANIC:VISITED check=[variable_name]]
[prose shown only on first visit]
[/MECHANIC]
`

| Parameter | Sugarcube Export | Ink Export | Ren'Py |
|---|---|---|---|
| set | <<run memorize(\"[var]\", true)>> or <<set $[var] to true>> | ~ [var] = true | $ [var] = True |
| check (first visit) | <<if not $[var]>>...<</if>> | {not [var]: ...} | if not [var]: |
| check (revisit) | <<if $[var]>>...<</if>> | {[var]: ...} | if [var]: |

---

### inventory — Item Management

`
[MECHANIC:INVENTORY add=[item_variable]]
[prose describing item acquisition]
[/MECHANIC]

[MECHANIC:INVENTORY remove=[item_variable]]

[MECHANIC:INVENTORY check=[item_variable]]
[prose shown when item is present]
[/MECHANIC]
`

| Parameter | Sugarcube Export | Ink Export | Ren'Py |
|---|---|---|---|
| add | <<set \[item] to true>> | ~ inv_[item] = true | $ inv_[item] = True |
| remove | <<set \[item] to false>> | ~ inv_[item] = false | $ inv_[item] = False |
| check present | <<if \[item]>>...<</if>> | {inv_[item]: ...} | if inv_[item]: |
| check absent | <<if not \[item]>>...<</if>> | {not inv_[item]: ...} | if not inv_[item]: |

---

## Tier 3 Hooks — Point-and-Click / High-Fidelity

### move — Actor Navigation

| Engine | Syntax |
|---|---|
| Escoria | :walk [actor] [target] |
| AGS | c[Actor].Walk([x], [y]); |
| Unity | character.MoveTo(\"[target]\"); |

---

### udio — Sound Triggers

| Engine | Syntax |
|---|---|
| Escoria | snd_play [file] |
| Ren'Py | play sound \"[file]\" |
| Sugarcube | <<audio \"[file]\" play>> |

---

## Generic/Markdown Annotations

When export_target: generic is set, all hooks are written as:
[MECHANIC:TYPE parameter=value] prose [/MECHANIC]
or
[MECHANIC:TYPE parameter=value] (inline)
