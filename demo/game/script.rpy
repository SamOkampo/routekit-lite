define rk = Character("RouteKit", color="#ff7ba1")
define maya = Character("Maya", color="#8dd8ff")

image routekit_demo_bg = Solid("#0b0d19")
image routekit_memory_bg = Solid("#241426")


screen routekit_demo_character():
    zorder 0

    frame:
        xalign 0.5
        yalign 0.38
        xysize (360, 310)
        padding (28, 26)
        background Solid("#171b31")

        vbox:
            align (0.5, 0.5)
            spacing 18

            frame:
                xalign 0.5
                xysize (132, 132)
                background Solid("#ff5c8a")

                text "M":
                    align (0.5, 0.5)
                    color "#ffffff"
                    size 72
                    bold True

            text "MAYA":
                xalign 0.5
                color "#ffffff"
                size 30
                bold True

            text "Independent photographer":
                xalign 0.5
                color "#aeb6d8"
                size 19


screen routekit_demo_memories():
    tag routekit_overlay
    modal True
    zorder 200

    $ unlocked = routekit_can_unlock("maya", 25)

    add Solid("#0b0d19")

    frame:
        align (0.5, 0.5)
        xmaximum 920
        padding (42, 36)
        background Solid("#111426")

        vbox:
            xsize 836
            spacing 24

            text "MEMORIES" style "routekit_eyebrow"
            text "A simple scene unlock" style "routekit_heading"

            button:
                id "routekit_memory_card"
                xfill True
                yminimum 210
                padding (28, 24)
                background Solid("#1a1e34")
                hover_background Solid("#232944")
                action (Return("memory") if unlocked else NullAction())

                hbox:
                    spacing 26

                    frame:
                        xysize (170, 150)
                        background Solid("#ff5c8a" if unlocked else "#303650")

                        text ("♥" if unlocked else "LOCKED"):
                            align (0.5, 0.5)
                            color "#ffffff"
                            size (58 if unlocked else 20)
                            bold True

                    vbox:
                        yalign 0.5
                        spacing 10

                        text "The rooftop photograph":
                            color ("#ffffff" if unlocked else "#8f96b5")
                            size 28
                            bold True

                        if unlocked:
                            text "Unlocked — select to view the scene":
                                color "#7ee2b8"
                                size 20
                        else:
                            text "Requires 25 affection points with Maya":
                                color "#ff9ab6"
                                size 20

            fixed:
                xfill True
                ysize 60

                textbutton "BACK":
                    id "routekit_memories_back"
                    xpos 836
                    xanchor 1.0
                    yalign 0.5
                    action Return("back")
                    style "routekit_button"


label start:
    $ routekit_reset(False)

    scene routekit_demo_bg
    show screen routekit_demo_character
    with dissolve

    rk "Welcome to RouteKit Lite. This short demo shows the complete buyer workflow."
    rk "Maya begins with 10 affection points. Your decision will update her relationship stage automatically."

    maya "I have my first gallery exhibition tomorrow... and I am starting to think nobody will come."

    menu:
        "Listen and encourage her  (+20)":
            $ routekit_change("maya", 20)
            maya "Thank you. I really needed someone to believe in me."

        "Invite her for a quick coffee  (+10)":
            $ routekit_change("maya", 10)
            maya "Coffee sounds good. Maybe it will help me relax."

        "Change the subject  (-5)":
            $ routekit_change("maya", -5)
            maya "Oh... never mind, then."

    rk "The same helper works after any dialogue choice: routekit_change(\"maya\", amount)."
    rk "Now open the reusable relationship screen."

    call screen routekit_relationship_hub

    rk "Content can be gated with a single check. This memory requires 25 affection points."

    call screen routekit_demo_memories

    if _return == "memory":
        hide screen routekit_demo_character
        scene routekit_memory_bg
        with dissolve

        maya "The city lights look incredible from up here. Stand beside me — I want this photograph to remember both of us."
        rk "Memory unlocked. The commercial version can replace this placeholder with any scene, image, replay, or route."
    else:
        rk "The memory is still locked. A different choice can meet the same 25-point requirement."

    menu:
        "Try another choice":
            jump start

        "Finish the demo":
            rk "That is RouteKit Lite: configure, change points, show progress, and unlock content."
            return
