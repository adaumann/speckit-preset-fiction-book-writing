# Engine Configuration in Speckit

## Overview

The `export_engines` field in your constitution allows you to specify which game engines should be targeted during the implementation step. This controls both what speckit.implement generates and what compile.py will accept.

## Configuration

### In spec.yml

```yaml
title: My Game
author: Author Name
export_engines:
  - generic
  - sugarcube
  - ink
```

### In constitution.md (YAML front matter)

```yaml
---
title: My Game
author: Author Name
export_engines:
  - generic
  - sugarcube
  - ink
---
```

## Supported Engines

| Engine | Format | Output | Tier Support |
|--------|--------|--------|--------------|
| `generic` | Markdown | `.md` files with hooks | All tiers |
| `sugarcube` | Twee3 | `.twee` files → HTML | Tier 1/2/3 |
| `ink` | Ink | `.ink` files | Tier 1 only |
| `renpy` | Ren'py | `.rpy` files | Tier 1/2 |
| `ags` | AGS Script | `.asc` files | Limited |
| `escoria` | Escoria | `.esc` files | All tiers |
| `unity` | C# / YARN | `.cs` or `.yarn` | Limited |

## Usage

### Implementation

```bash
speckit.implement --spec my-game
# Only generates files for engines in export_engines
```

### Compilation

```bash
# Attempts to compile only allowed engines
python compile.py --spec my-game --engine sugarcube

# Will fail with error if engine not in export_engines
python compile.py --spec my-game --engine renpy
# ❌ Error: Engine 'renpy' not in constitution export_engines: ['generic', 'sugarcube', 'ink']
```

## Common Configurations

### Minimal (Markdown review only)
```yaml
export_engines:
  - generic
```

### SugarCube-focused (web-based interactive fiction)
```yaml
export_engines:
  - generic       # For editing/review
  - sugarcube     # Primary target
```

### Multi-engine support
```yaml
export_engines:
  - generic       # For review
  - sugarcube     # Web-based
  - ink           # Mobile-friendly narrative
  - renpy         # Visual novel version
```

## How It Works

1. **speckit.implement** reads `export_engines` from spec.yml or constitution.md
2. For each engine in the list, it generates the appropriate format:
   - `.md` files for `generic`
   - `.twee` files for `sugarcube`
   - `.ink` files for `ink`
   - etc.
3. **compile.py** validates that the requested engine is in export_engines before attempting compilation
4. If engine is not configured, compilation fails with clear error message

## Benefits

- **Consistency**: Prevents accidental generation of unsupported formats
- **Clarity**: Documents which engines are officially supported
- **Flexibility**: Easy to add/remove engines during development
- **Validation**: Compilation catches configuration mismatches early

## Default (if not specified)

If no `export_engines` is configured, compilation will:
- Work for any engine (backward compatible)
- Print a warning suggesting to configure export_engines

## Next Steps

1. Add `export_engines` to your spec.yml
2. Run `speckit.implement` to generate files for configured engines
3. Use `compile.py` to build final output from generated engine-specific files
