# RouteKit Lite — Quick Start

RouteKit Lite adds affection points, relationship stages, a relationship screen, and simple content-unlock checks to a Ren'Py project.

## Requirements

- Ren'Py 8.5.3 or a compatible Ren'Py 8 release
- A project using the standard Ren'Py screen system

## Installation

1. Copy `routekit_lite.rpy` into your project's `game` folder.
2. Copy `routekit_config.rpy` into the same folder.
3. Edit the character inside `routekit_config.rpy`.
4. Launch the project and run Ren'Py's **Check Script (Lint)** command.

## Change affection

Use a Python line after a choice:

```renpy
menu:
    "Support her":
        $ routekit_change("maya", 20)

    "Ignore her":
        $ routekit_change("maya", -10)
```

Pass `False` as the third argument to disable the on-screen notification:

```renpy
$ routekit_change("maya", 20, False)
```

## Open the relationship screen

```renpy
call screen routekit_relationship_hub
```

## Unlock content

```renpy
if routekit_can_unlock("maya", 25):
    jump maya_bonus_scene
else:
    "You need 25 affection points to unlock this scene."
```

## Main API

- `routekit_value(character_id)` — current affection
- `routekit_change(character_id, amount, notify=True)` — add or subtract affection
- `routekit_set(character_id, value, notify=False)` — set an exact value
- `routekit_stage(character_id)` — current stage name
- `routekit_next_stage(character_id)` — next `(threshold, name)` pair or `None`
- `routekit_points_to_next_stage(character_id)` — remaining points
- `routekit_can_unlock(character_id, threshold)` — unlock condition
- `routekit_reset(notify=False)` — clear RouteKit state
- `routekit_migrate_state()` — normalize an old or damaged save immediately
- `routekit_validate_config()` — return configuration errors

## Notes

RouteKit state is stored in a Ren'Py `default` variable and is covered by real rollback and save/load round-trip tests. Version 0.1.2 registers a callback in `config.after_load_callbacks`; it does not replace your project's `after_load` label. Old Pro-shaped values, invalid values, removed characters, and out-of-range values are normalized automatically after loading. Lite supports one configured character.

Read `RELIABILITY_CHECKLIST_EN.md` before shipping an update that changes characters or stat ranges.

## Need deeper routes?

RouteKit Pro is available for projects that need:

- Unlimited configurable characters
- Multiple stats such as affection, trust, rivalry, or corruption
- Events with combined stat requirements
- A multi-character dashboard
- A persistent replay gallery
- Configurable colors and relationship stages

You write the story and choices. RouteKit Pro handles the shared relationship state, screens, unlock rules, save-safe values, and persistent replays.

Get RouteKit Pro: https://samokampo.itch.io/routekit-pro
