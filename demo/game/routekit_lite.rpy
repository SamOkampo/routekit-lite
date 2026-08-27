# RouteKit Lite 0.1.2
# A reusable relationship system for Ren'Py 8.

default routekit_values = {}
default routekit_state_version = 2

init -20 python:
    from collections.abc import Mapping

    ROUTEKIT_VERSION = "0.1.2"
    ROUTEKIT_STATE_SCHEMA = 2

    def routekit_safe_value(character_id, value):
        """Convert and clamp a saved value, falling back to the configured initial value."""
        try:
            value = int(value)
        except (TypeError, ValueError):
            value = routekit_initial(character_id)
        return max(routekit_minimum(character_id), min(routekit_maximum(character_id), value))

    def routekit_migrate_state():
        """Normalize old or damaged saves to the current Lite state schema."""
        global routekit_values, routekit_state_version

        source = routekit_values if isinstance(routekit_values, Mapping) else {}
        normalized = {}

        for character_id in routekit_characters:
            if character_id not in source:
                continue

            saved_value = source.get(character_id)
            if isinstance(saved_value, Mapping):
                saved_value = saved_value.get("affection", routekit_initial(character_id))
            normalized[character_id] = routekit_safe_value(character_id, saved_value)

        changed = normalized != source or routekit_state_version != ROUTEKIT_STATE_SCHEMA
        routekit_values = normalized
        routekit_state_version = ROUTEKIT_STATE_SCHEMA

        if changed:
            renpy.block_rollback()
        return changed

    def routekit_character(character_id):
        """Returns the validated configuration for one character."""
        if character_id not in routekit_characters:
            raise Exception("RouteKit: unknown character id {!r}.".format(character_id))
        return routekit_characters[character_id]

    def routekit_minimum(character_id):
        return int(routekit_character(character_id).get("minimum", 0))

    def routekit_maximum(character_id):
        return int(routekit_character(character_id).get("maximum", 100))

    def routekit_initial(character_id):
        data = routekit_character(character_id)
        return int(data.get("initial", data.get("minimum", 0)))

    def routekit_value(character_id):
        routekit_character(character_id)
        return routekit_safe_value(
            character_id,
            routekit_values.get(character_id, routekit_initial(character_id)),
        )

    def routekit_set(character_id, value, notify=False):
        data = routekit_character(character_id)
        minimum = int(data.get("minimum", 0))
        maximum = int(data.get("maximum", 100))
        new_value = max(minimum, min(maximum, int(value)))
        old_value = routekit_value(character_id)
        routekit_values[character_id] = new_value

        if notify and new_value != old_value:
            difference = new_value - old_value
            sign = "+" if difference > 0 else ""
            renpy.notify("{} {}{}".format(data.get("name", character_id), sign, difference))

        return new_value

    def routekit_change(character_id, amount, notify=True):
        return routekit_set(character_id, routekit_value(character_id) + int(amount), notify)

    def routekit_stage(character_id):
        data = routekit_character(character_id)
        stages = list(data.get("stages", []))
        if not stages:
            return ""

        current_value = routekit_value(character_id)
        current_stage = str(stages[0][1])

        for threshold, stage_name in sorted(stages, key=lambda item: int(item[0])):
            if current_value >= int(threshold):
                current_stage = str(stage_name)
            else:
                break

        return current_stage

    def routekit_next_stage(character_id):
        current_value = routekit_value(character_id)
        stages = routekit_character(character_id).get("stages", [])

        for threshold, stage_name in sorted(stages, key=lambda item: int(item[0])):
            if int(threshold) > current_value:
                return (int(threshold), str(stage_name))

        return None

    def routekit_points_to_next_stage(character_id):
        next_stage = routekit_next_stage(character_id)
        if next_stage is None:
            return 0
        return max(0, next_stage[0] - routekit_value(character_id))

    def routekit_progress(character_id):
        minimum = routekit_minimum(character_id)
        maximum = routekit_maximum(character_id)
        span = max(1, maximum - minimum)
        return float(routekit_value(character_id) - minimum) / float(span)

    def routekit_percent(character_id):
        return int(round(routekit_progress(character_id) * 100))

    def routekit_can_unlock(character_id, threshold):
        return routekit_value(character_id) >= int(threshold)

    def routekit_reset(notify=False):
        routekit_values.clear()
        if notify:
            renpy.notify("RouteKit progress reset")

    if routekit_migrate_state not in config.after_load_callbacks:
        config.after_load_callbacks.append(routekit_migrate_state)

    def routekit_initial_letter(character_id):
        name = str(routekit_character(character_id).get("name", character_id)).strip()
        return name[:1].upper() if name else "?"

    def routekit_validate_config():
        errors = []

        if not isinstance(routekit_characters, dict) or not routekit_characters:
            return ["routekit_characters must contain one character."]

        if len(routekit_characters) > 1:
            errors.append("RouteKit Lite supports one configured character.")

        for character_id, data in routekit_characters.items():
            prefix = "Character {!r}: ".format(character_id)

            if not isinstance(character_id, str) or not character_id:
                errors.append("Character ids must be non-empty strings.")
                continue

            if not isinstance(data, dict):
                errors.append(prefix + "configuration must be a dictionary.")
                continue

            if not str(data.get("name", "")).strip():
                errors.append(prefix + "name is required.")

            minimum = int(data.get("minimum", 0))
            maximum = int(data.get("maximum", 100))
            initial = int(data.get("initial", minimum))

            if maximum <= minimum:
                errors.append(prefix + "maximum must be greater than minimum.")
            if initial < minimum or initial > maximum:
                errors.append(prefix + "initial must be between minimum and maximum.")

            stages = data.get("stages", [])
            if not stages:
                errors.append(prefix + "at least one relationship stage is required.")
            else:
                previous = None
                first_threshold = None

                for stage in stages:
                    if not isinstance(stage, (list, tuple)) or len(stage) != 2:
                        errors.append(prefix + "each stage must be a (threshold, name) pair.")
                        break

                    threshold, stage_name = stage

                    try:
                        threshold = int(threshold)
                    except (TypeError, ValueError):
                        errors.append(prefix + "stage thresholds must be whole numbers.")
                        break

                    if first_threshold is None:
                        first_threshold = threshold

                    if previous is not None and threshold <= previous:
                        errors.append(prefix + "stage thresholds must be strictly increasing.")
                        break
                    if threshold < minimum or threshold > maximum:
                        errors.append(prefix + "stage thresholds must be inside the configured range.")
                        break
                    if not str(stage_name).strip():
                        errors.append(prefix + "stage names cannot be empty.")
                        break
                    previous = threshold

                if first_threshold is not None and first_threshold != minimum:
                    errors.append(prefix + "the first stage threshold must equal minimum.")

        return errors


screen routekit_relationship_hub():
    """Displays the RouteKit Lite relationship overview."""

    tag routekit_overlay
    modal True
    zorder 200

    add Solid("#0b0d19")

    frame:
        xalign 0.5
        yalign 0.5
        xmaximum 1040
        ymaximum 500
        padding (44, 36)
        background Solid("#111426")

        vbox:
            spacing 26

            fixed:
                xfill True
                ysize 70

                vbox:
                    spacing 4
                    text "RELATIONSHIPS" style "routekit_eyebrow"
                    text "People you know" style "routekit_heading"

                textbutton "BACK":
                    id "routekit_close"
                    xalign 1.0
                    yalign 0.5
                    action Return()
                    style "routekit_button"

            viewport:
                xfill True
                ymaximum 300
                mousewheel True
                draggable True

                vbox:
                    xfill True
                    spacing 18

                    for character_id in routekit_characters:
                        use routekit_relationship_card(character_id)


screen routekit_relationship_card(character_id):
    $ data = routekit_character(character_id)
    $ accent = str(data.get("accent", "#ff5c8a"))
    $ current_value = routekit_value(character_id)
    $ maximum = routekit_maximum(character_id)
    $ next_stage = routekit_next_stage(character_id)

    frame:
        xfill True
        padding (24, 22)
        background Solid("#1a1e34")

        vbox:
            spacing 18

            hbox:
                spacing 20

                frame:
                    xysize (78, 78)
                    background Solid(accent)

                    text routekit_initial_letter(character_id):
                        align (0.5, 0.5)
                        color "#ffffff"
                        size 38
                        bold True

                vbox:
                    yalign 0.5
                    spacing 5

                    text str(data.get("name", character_id)) style "routekit_name"
                    text str(data.get("subtitle", "")) style "routekit_subtitle"

            fixed:
                xfill True
                ysize 30

                text routekit_stage(character_id):
                    align (0.0, 0.5)
                    color accent
                    size 23
                    bold True

                text "{}/{}  •  {}%".format(current_value, maximum, routekit_percent(character_id)):
                    align (1.0, 0.5)
                    color "#dfe3ff"
                    size 20

            bar:
                value routekit_percent(character_id)
                range 100
                xfill True
                ysize 16
                left_bar Solid(accent)
                right_bar Solid("#303650")

            if next_stage is None:
                text "Maximum relationship stage reached" style "routekit_hint"
            else:
                text "{} points until {}".format(routekit_points_to_next_stage(character_id), next_stage[1]) style "routekit_hint"


style routekit_eyebrow is default:
    color "#ff7ba1"
    size 17
    bold True
    kerning 2

style routekit_heading is default:
    color "#ffffff"
    size 39
    bold True

style routekit_name is default:
    color "#ffffff"
    size 30
    bold True

style routekit_subtitle is default:
    color "#9ca5c9"
    size 20

style routekit_hint is default:
    color "#9ca5c9"
    size 18

style routekit_button is button:
    padding (22, 12)
    background Solid("#ff5c8a")
    hover_background Solid("#ff7ba1")

style routekit_button_text is button_text:
    color "#ffffff"
    hover_color "#ffffff"
    size 18
    bold True
