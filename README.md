# RouteKit Lite — public Ren'Py tests

This repository makes the complete RouteKit Lite `0.1.2` demo and test suite public so anyone can inspect the implementation and reproduce the results.

RouteKit does not replace Ren'Py variables or introduce a new relationship algorithm. Lite packages the repetitive parts around a one-character relationship route: configuration, value clamping, stages, a reusable screen, scene checks, save migration, and rollback-aware state.

## Verified with Ren'Py 8.5.3

The current suite passes **7/7 test cases and 26/26 assertions**:

| Test | What it checks |
| --- | --- |
| `configuration` | Version, schema, configuration, and after-load callback |
| `legacy_and_damaged_save_migration` | Old Pro-shaped values, removed data, clamping, and damaged-state repair |
| `rollback_restores_relationship_state` | A real Ren'Py rollback restores Maya from 80 to the previous value of 25 |
| `save_load_round_trip` | A real save/load round trip restores 40 after the live value changes to 90 |
| `relationship_math` | Initial value, stages, clamping, progression, and unlock checks |
| `relationship_screen` | The reusable relationship screen opens and exposes its expected controls |
| `unlocked_memory_screen` | A scene-gate screen becomes available when its requirement is met |

The exact test definitions are in [`demo/game/testcases.rpy`](demo/game/testcases.rpy). Test-only story paths are kept separately in [`demo/game/routekit_test_support.rpy`](demo/game/routekit_test_support.rpy).

## Run the same tests

1. Download the [Ren'Py 8.5.3 SDK](https://www.renpy.org/latest.html).
2. Clone or download this repository.
3. Run the command below from the SDK directory, replacing the repository path as needed.

Windows:

```powershell
lib\py3-windows-x86_64\python.exe renpy.py C:\path\to\routekit-lite\demo test routekit --report-detailed
```

macOS or Linux:

```bash
./renpy.sh /path/to/routekit-lite/demo test routekit --report-detailed
```

Expected summary:

```text
Test cases : 7 | 7 passed | 0 failed
Assertions : 26 | 26 passed | 0 failed
Status: PASSED
```

The latest recorded run is in [`test-results/renpy-8.5.3-summary.txt`](test-results/renpy-8.5.3-summary.txt), and screenshots created by the screen tests are under [`test-results/screenshots`](test-results/screenshots).

## Repository map

- `demo/game/routekit_lite.rpy` — relationship state and reusable UI
- `demo/game/routekit_config.rpy` — example character configuration
- `demo/game/script.rpy` — interactive demo
- `demo/game/testcases.rpy` — complete automated test suite
- `docs/` — English and Spanish setup and reliability guides
- `test-results/` — latest sanitized summary and test screenshots

## Download the packaged free edition

RouteKit Lite is free/name-your-own-price on itch.io:

https://samokampo.itch.io/routekit-lite

## AI disclosure

The source and documentation were created with AI assistance. They were then reviewed, linted, visually inspected, and executed with Ren'Py's official automated test framework. Public tests are provided so the technical claims can be checked directly instead of taken on trust.

## License

See [`LICENSE.txt`](LICENSE.txt). The included license permits use in commercial and non-commercial Ren'Py projects, subject to its terms.
