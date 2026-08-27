# RouteKit Lite reliability checklist

Run this checklist in a copy of the real game before publishing an update.

## Automated baseline

1. Run Ren'Py lint.
2. Run the RouteKit test suite.
3. Confirm that migration, rollback, save/load, math, and screen cases pass.

## Manual player paths

1. Start a new game, change affection, roll back one choice, and confirm the old value and stage return.
2. Save with a non-initial value, change it again, load the save, and confirm the saved value returns.
3. Quick-save, change affection several times, quick-load, and confirm the UI and value agree.
4. Reach the minimum and maximum repeatedly and confirm the value never leaves the configured range.
5. Change the configured minimum, maximum, and initial value, then load an older save and confirm it is clamped safely.
6. Remove the configured character from a copy of the project, load an older save, and confirm the game opens without an exception.
7. Replace a saved value with invalid test data, call `routekit_migrate_state()`, and confirm the configured initial value is used.
8. Test the same save on Windows and one additional target platform planned for release.

Keep a backup of every compatibility fixture used for a public release.
