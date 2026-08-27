# Test-only paths used by RouteKit Lite's automated rollback and save/load checks.

label routekit_lite_test_rollback_path:
    $ routekit_reset(False)
    $ routekit_set("maya", 25, False)
    "ROUTEKIT LITE ROLLBACK CHECKPOINT A"
    $ routekit_set("maya", 80, False)
    "ROUTEKIT LITE ROLLBACK CHECKPOINT B"
    return


label routekit_lite_test_save_load_path:
    $ routekit_reset(False)
    $ routekit_set("maya", 40, False)
    "ROUTEKIT LITE SAVE CHECKPOINT"
    $ routekit_set("maya", 90, False)
    "ROUTEKIT LITE CHANGED AFTER SAVE"
    return
