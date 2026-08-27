testsuite routekit:
    teardown:
        exit

    testcase configuration:
        assert eval (routekit_validate_config() == [])
        assert eval (ROUTEKIT_VERSION == "0.1.2")
        assert eval (ROUTEKIT_STATE_SCHEMA == 2)
        assert eval (routekit_migrate_state in config.after_load_callbacks)

    testcase legacy_and_damaged_save_migration:
        $ renpy.store.routekit_values = {"maya": {"affection": 999}, "removed": 20}
        $ renpy.store.routekit_state_version = 0
        $ routekit_migrate_state()
        assert eval (routekit_state_version == ROUTEKIT_STATE_SCHEMA)
        assert eval (routekit_values == {"maya": 100})
        assert eval (routekit_value("maya") == 100)
        $ renpy.store.routekit_values = ["damaged"]
        $ routekit_migrate_state()
        assert eval (routekit_values == {})
        assert eval (routekit_value("maya") == 10)

    testcase rollback_restores_relationship_state:
        run Start("routekit_lite_test_rollback_path")
        advance until "ROUTEKIT LITE ROLLBACK CHECKPOINT A"
        assert eval (routekit_value("maya") == 25)
        advance until "ROUTEKIT LITE ROLLBACK CHECKPOINT B"
        assert eval (routekit_value("maya") == 80)
        run Rollback()
        assert eval (routekit_value("maya") == 25)
        run MainMenu(confirm=False)

    testcase save_load_round_trip:
        $ renpy.unlink_save("routekit-lite-0-1-2-test")
        run Start("routekit_lite_test_save_load_path")
        advance until "ROUTEKIT LITE SAVE CHECKPOINT"
        assert eval (routekit_value("maya") == 40)
        run FileSave("routekit-lite-0-1-2-test", confirm=False)
        advance until "ROUTEKIT LITE CHANGED AFTER SAVE"
        assert eval (routekit_value("maya") == 90)
        run FileLoad("routekit-lite-0-1-2-test", confirm=False)
        assert eval (routekit_value("maya") == 40)
        $ renpy.unlink_save("routekit-lite-0-1-2-test")
        run MainMenu(confirm=False)

    testcase relationship_math:
        $ routekit_reset(False)
        assert eval (routekit_value("maya") == 10)
        assert eval (routekit_stage("maya") == "Stranger")

        $ routekit_change("maya", 20, False)
        assert eval (routekit_value("maya") == 30)
        assert eval (routekit_stage("maya") == "Friend")
        assert eval routekit_can_unlock("maya", 25)

        $ routekit_change("maya", 500, False)
        assert eval (routekit_value("maya") == 100)
        assert eval (routekit_next_stage("maya") is None)

        $ routekit_change("maya", -500, False)
        assert eval (routekit_value("maya") == 0)
        assert eval (routekit_points_to_next_stage("maya") == 15)

    testcase relationship_screen:
        $ routekit_reset(False)
        run Show("routekit_relationship_hub")
        pause until screen "routekit_relationship_hub"
        assert id "routekit_close"
        screenshot "routekit_relationship_hub.png"
        run Hide("routekit_relationship_hub")
        pause until not screen "routekit_relationship_hub"

    testcase unlocked_memory_screen:
        $ routekit_reset(False)
        $ routekit_set("maya", 30, False)
        run Show("routekit_demo_memories")
        pause until screen "routekit_demo_memories"
        assert id "routekit_memory_card"
        screenshot "routekit_memory_unlocked.png"
        run Hide("routekit_demo_memories")
        pause until not screen "routekit_demo_memories"
