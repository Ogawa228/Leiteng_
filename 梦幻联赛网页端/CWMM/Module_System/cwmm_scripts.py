# -*- coding: utf8 -*-
from header_operations import *
from header_common import *
from cwmm_constants import *
from module_constants import *
from header_items import *

cwmm_scripts = [

    ("cwmm_event_player_spawn_as_troop_class", [
        (store_script_param, ":player_no", 1),
        (store_script_param, ":troop_class", 2), # multi_troop_class_infantry, ...

        (try_begin),
            (eq, ":troop_class", multi_troop_class_infantry),
            (call_script, "script_cwmm_add_player_stat", ":player_no", INDEX_SPAWNED_AS_INFANTRY, 1),
        (try_end),
    ]),

    ("cwmm_show_team_score", [
        (try_begin),
            (multiplayer_is_server),
            (eq, "$g_cwmm_server_is_in_match", 1),
            (team_get_score, ":team_1_score", 0),
            (team_get_score, ":team_2_score", 1),
            (try_begin),
                (eq, "$g_cwmm_switched_team", 1),
                (val_add, ":team_1_score", "$g_cwmm_team_2_score"),
                (val_add, ":team_2_score", "$g_cwmm_team_1_score"),
            (try_end),
            (assign, reg21, ":team_1_score"),
            (assign, reg22, ":team_2_score"),
            (str_store_string, s1, "str_cwmm_current_score_reg21_reg22"),
            (call_script, "script_adimi_tool_server_message"),
        (try_end),
    ]),

    ("cwmm_broadcast_troop_selection", [
        (store_script_param, ":team_no", 1),

        (assign, ":num_infantry", 0),
        (assign, ":num_archer", 0),
        (assign, ":num_cavalry", 0),

        (try_for_players, ":player_no"),
            (player_is_active, ":player_no"),
            (player_get_team_no,  ":player_team", ":player_no"),
            (is_between, ":player_team", 0, 2),
            (eq, ":player_team", ":team_no"),
            (player_get_troop_id, ":troop_no", ":player_no"),
            (call_script, "script_adimi_tool_get_troop_class", ":troop_no"),
            (assign, ":troop_class", reg0),
            (neq, ":troop_class", -1),
            (try_begin),
                (eq, ":troop_class", multi_troop_class_infantry),
                (val_add, ":num_infantry", 1),
            (else_try),
                (eq, ":troop_class", multi_troop_class_archer),
                (val_add, ":num_archer", 1),
            (else_try),
                (eq, ":troop_class", multi_troop_class_cavalry),
                (val_add, ":num_cavalry", 1),
            (try_end),
        (try_end),

        (assign, reg31, ":num_archer"),
        (assign, reg32, "$g_cwmm_archer_limit"),
        (assign, reg33, ":num_infantry"),
        (assign, reg34, "$g_cwmm_infantry_limit"),
        (assign, reg35, ":num_cavalry"),
        (assign, reg36, "$g_cwmm_cavalry_limit"),
        (try_for_players, ":player_no"),
            (player_is_active, ":player_no"),
            (player_get_team_no,  ":player_team", ":player_no"),
            (is_between, ":player_team", 0, 2),
            (eq, ":player_team", ":team_no"),
            (multiplayer_send_string_to_player, ":player_no", multiplayer_event_show_server_message, "str_cwmm_troop_count_reg31_reg32_reg33_reg34_reg35_reg36"),
        (try_end),


    ]),

    #response format should be like this:
    #  [a number or a string]|[another number or a string]|[yet another number or a string] ...
    # here is an example response:
    # 12|Player|100|another string|142|323542|34454|yet another string
    # INPUT: arg1 = num_integers, arg2 = num_strings
    # reg0, reg1, reg2, ... up to 128 registers contain the integer values
    # s0, s1, s2, ... up to 128 strings contain the string values
    ("cwmm_process_url_response", [
        (try_begin),
            (multiplayer_is_dedicated_server),
            (try_begin),
                (eq, reg0, 1),
                # 1|距离下次tick时间（秒）
                (val_min, "$g_cwmm_next_tick_seconds", reg1),
                (try_begin),
                    (eq, "$g_cwmm_server_is_in_match", 1),
                    (try_begin),
                        #(eq, "$g_cwmm_server_is_waiting_for_players", 1),
                        (eq, "$g_cwmm_should_finish_match", 0),
                        (call_script, "script_cwmm_cancel_match"),
                    (else_try),
                        (call_script, "script_cwmm_finish_match"),
                    (try_end),
                (try_end),
            (else_try),
                (eq, reg0, 2),
                # 2|模式ID|场景ID|1队国家|2队国家|每队人数|射手限制|步兵限制|骑兵限制|等待时间|Match ID
                (try_begin),
                    (eq, "$g_cwmm_server_is_in_match", 0),
                    (is_between, reg1, 1, 10),
                    (is_between, reg2, multiplayer_scenes_begin, multiplayer_scenes_end),
                    (is_between, reg3, npc_kingdoms_begin, npc_kingdoms_end),
                    (is_between, reg4, npc_kingdoms_begin, npc_kingdoms_end),
                    (gt, reg5, 0),
                    (ge, reg6, 0),
                    (ge, reg7, 0),
                    (ge, reg8, 0),
                    (gt, reg9, 0),
                    (gt, reg10, 0),

                    #(display_message, "@start_match"),

                    (try_begin),
                        (eq, reg1, 1),
                        (assign, "$g_multiplayer_disallow_ranged_weapons", 1),
                        (assign, "$g_multiplayer_initial_gold_multiplier", 100),
                        (assign, "$g_multiplayer_battle_earnings_multiplier", 0),
                        (assign, "$g_multiplayer_round_earnings_multiplier", 0),
                    (else_try),
                        (assign, "$g_multiplayer_disallow_ranged_weapons", 0),
                        (assign, "$g_multiplayer_initial_gold_multiplier", 100),
                        (assign, "$g_multiplayer_battle_earnings_multiplier", 100),
                        (assign, "$g_multiplayer_round_earnings_multiplier", 100),
                    (try_end),

                    (assign, "$g_cwmm_server_is_in_match", 1),
                    (assign, "$g_cwmm_mode_id", reg1),
                    (assign, "$g_cwmm_map_id", reg2),
                    (assign, "$g_cwmm_team_1_faction", reg3),
                    (assign, "$g_cwmm_team_2_faction", reg4),
                    (assign, "$g_cwmm_team_size", reg5),
                    (assign, "$g_cwmm_archer_limit", reg6),
                    (assign, "$g_cwmm_infantry_limit", reg7),
                    (assign, "$g_cwmm_cavalry_limit", reg8),
                    (assign, "$g_cwmm_wait_time_seconds", reg9),
                    (assign, "$g_cwmm_server_match_id", reg10),
                    (assign, "$g_cwmm_should_cancel_match", 0),
                    (assign, "$g_cwmm_should_finish_match", 0),
                    (assign, "$g_cwmm_server_is_waiting_for_players", 1),
                    (assign, "$g_cwmm_switched_team", 0),
                    (assign, "$g_cwmm_team_1_score", 0),
                    (assign, "$g_cwmm_team_2_score", 0),
                    (assign, "$g_cwmm_match_countdown", 10000000),
                    (assign, "$g_cwmm_last_round_entry_point", -1),

                    (assign, "$g_multiplayer_selected_map", reg2),
                    (assign, "$g_multiplayer_next_team_1_faction", "$g_cwmm_team_1_faction"),
                    (assign, "$g_multiplayer_next_team_2_faction", "$g_cwmm_team_2_faction"),
                    (team_set_faction, 0, "$g_multiplayer_next_team_1_faction"),
                    (team_set_faction, 1, "$g_multiplayer_next_team_2_faction"),
                    (start_multiplayer_mission, "mt_multiplayer_bt", "$g_multiplayer_selected_map", 1),
                (try_end),
            (else_try),
                (eq, reg0, 3),
                # def message_show_server_message(index, msg: str):
                #     return "3|%d|%s" % (index, msg)
                (try_begin),
                    (player_is_active, reg1),
                    (multiplayer_send_string_to_player, reg1, multiplayer_event_show_server_message, s0),
                (try_end),
            (else_try),
                (eq, reg0, 4),
                (try_begin),
                    (player_is_active, reg1),
                    (kick_player, reg1),
                (try_end),
            (else_try),
                (eq, reg0, 5),
                (try_begin),
                    (player_is_active, reg1),
                    (ban_player, reg1, 1),
                (try_end),
            (else_try),
                (eq, reg0, 6),
                (try_begin),
                    (str_store_string, s1, s0),
                    (call_script, "script_adimi_tool_server_message"),
                (try_end),
            (else_try),
                (eq, reg0, 7),
                # 允许玩家reg1进入队伍reg2，其中reg2为1或2，因此需要减1
                (try_begin),
                    (player_is_active, reg1),
                    (val_sub, reg2, 1),
                    (player_set_slot, reg1, slot_player_allowed_team, reg2),
                    (multiplayer_send_int_to_player, reg1, multiplayer_event_return_ghost_mode, 3),
                    (try_begin),
                        (eq, reg2, 0),
                        (str_store_player_username, s14, reg1),
                        (str_store_string, s1, "str_cwmm_s14_belong_to_team_1"),
                        (call_script, "script_adimi_tool_server_message"),
                        (player_set_troop_id, reg1, -1),
                        (try_begin),
                            (eq, "$g_cwmm_switched_team", 1),
                            (store_sub, reg2, 1, reg2),
                        (try_end),
                        (player_set_team_no, reg1, reg2),
                    (else_try),
                        (eq, reg2, 1),
                        (str_store_player_username, s14, reg1),
                        (str_store_string, s1, "str_cwmm_s14_belong_to_team_2"),
                        (call_script, "script_adimi_tool_server_message"),
                        (player_set_troop_id, reg1, -1),
                        (try_begin),
                            (eq, "$g_cwmm_switched_team", 1),
                            (store_sub, reg2, 1, reg2),
                        (try_end),
                        (player_set_team_no, reg1, reg2),
                    (try_end),

                    (player_get_unique_id, ":guid", reg1),
                    (try_begin),
                        (assign, reg17, ":guid"),
                        (str_store_string, s17, "@{reg17}"),
                        (neg|dict_has_key, "$cwmm_data_dict", s17),

                        (array_set_val, "$cwmm_data_array", ":guid", "$cwmm_next_data_index", INDEX_GUID),
                        (dict_set_int, "$cwmm_data_dict", s17, "$cwmm_next_data_index"),
                        (val_add, "$cwmm_next_data_index", 1),
                    (try_end),
                (try_end),
            (try_end),
        (try_end),
    ]),

    ("cf_cwmm_allow_player_join_team", [
        (store_script_param, ":player_no", 1),
        (store_script_param, ":team_no", 2),

        (player_get_slot, ":allowed_team", ":player_no", slot_player_allowed_team),
        (try_begin),
            (is_between, ":allowed_team", 0, 2),
            (eq, "$g_cwmm_switched_team", 1),
            (store_sub, ":allowed_team", 1, ":allowed_team"),
        (try_end),

        (assign, ":allow", 1),
        (try_begin),
            (is_between, ":team_no", 0, 2),
            (try_begin),
                (eq, "$g_cwmm_server_is_in_match", 1),
                (eq, ":allowed_team", ":team_no"),
                (assign, ":allow", 1),
            (else_try),
                (assign, ":allow", 0),
                (player_get_slot, ":counter", ":player_no", slot_player_not_allowed_team_counter),
                (val_add, ":counter", 1),
                (player_set_slot, ":player_no", slot_player_not_allowed_team_counter, ":counter"),
                (store_mod, ":show", ":counter", 2),
                (try_begin),
                    (eq, ":show", 1),
                    (multiplayer_send_string_to_player, ":player_no", multiplayer_event_show_server_message, "str_cwmm_you_are_not_allowed_by_this_team"),
                (try_end),
            (try_end),
        (try_end),

        (eq, ":allow", 1),
    ]),

    ("cwmm_check_team_switch", [
        (try_begin),
            (multiplayer_is_server),
            (eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
            (eq, "$g_cwmm_server_is_in_match", 1),
            (eq, "$g_cwmm_should_cancel_match", 0),
            (eq, "$g_cwmm_should_finish_match", 0),
            (lt, "$g_cwmm_match_countdown", 0),

            (assign, ":max_score", 3),
            (try_begin),
                (eq, "$g_cwmm_mode_id", 1),
                (assign, ":max_score", 5),
            (try_end),

            (try_begin),
                (eq, "$g_cwmm_switched_team", 0),
                (team_get_score, ":team_1_score", 0),
                (team_get_score, ":team_2_score", 1),

                (this_or_next|ge, ":team_1_score", ":max_score"),
                (ge, ":team_2_score", ":max_score"),

                (assign, "$g_cwmm_switched_team", 1),
                (assign, "$g_cwmm_team_1_score", ":team_1_score"),
                (assign, "$g_cwmm_team_2_score", ":team_2_score"),
                (assign, "$g_cwmm_last_round_entry_point", -1),

                # reset map and switch team
                (assign, "$g_cwmm_match_countdown", CWMM_TEAM_SWITCH_COUNDOWN),
                #clear scene and end round
                (multiplayer_clear_scene),

                (try_begin),
                    (eq, "$g_battle_death_mode_started", 2),
                    (call_script, "script_move_death_mode_flags_down"),
                (try_end),

                (assign, "$g_battle_death_mode_started", 0),
                (assign, "$g_reduced_waiting_seconds", 0),

                #initialize moveable object positions
                (call_script, "script_multiplayer_initialize_belfry_wheel_rotations"),
                (call_script, "script_multiplayer_close_gate_if_it_is_open"),
                (call_script, "script_adimi_tool_close_new_gates_if_open"),#AdimiTools close gates
                (call_script, "script_adimi_tool_respawn_items_after_round_end"),#AdimiTools respawn items
                (call_script, "script_multiplayer_move_moveable_objects_initial_positions"),

                (assign, "$g_round_ended", 0), 

                (assign, "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_team_1"), 
                (assign, "$g_multiplayer_num_bots_required_team_2", "$g_multiplayer_num_bots_team_2"), 

                (store_mission_timer_a, "$g_round_start_time"),
                (call_script, "script_initialize_all_scene_prop_slots"),
                (call_script, "script_initialize_objects"),

                (team_set_score, 0, 0),
                (team_set_score, 1, 0),
                (try_for_players, ":cur_player_a"), 
                    (player_is_active, ":cur_player_a"),
                    (try_begin),
                        (player_set_troop_id, ":cur_player_a", -1),
                        (player_get_team_no,  ":team", ":cur_player_a"),
                        (is_between,":team", 0, 2),
                        (assign,":new_team", -1),
                        (try_begin),
                            (eq, ":team", 0),
                            (assign, ":new_team", 1),
                        (else_try),
                            (eq, ":team", 1),
                            (assign, ":new_team", 0),
                        (try_end),

                        (neq, ":new_team", -1),
                        (player_set_team_no, ":cur_player_a", ":new_team"),
                        (multiplayer_send_message_to_player, ":cur_player_a", multiplayer_event_force_start_team_selection),
                    (try_end),
                    (multiplayer_send_int_to_player, ":cur_player_a", multiplayer_event_set_round_start_time, -9999),# this will also initialize moveable object slots.
                    (player_set_slot, ":cur_player_a", slot_player_spawned_this_round, 0),
                    (player_set_slot, ":cur_player_a", slot_player_last_rounds_used_item_earnings, 0),
                    (player_set_slot, ":cur_player_a", slot_player_poll_disabled_until_time, 0),
                    (store_mission_timer_a, ":player_join_time"),
                    (player_set_slot, ":cur_player_a", slot_player_join_time, ":player_join_time"),
                    (player_set_slot, ":cur_player_a", slot_player_spawned_this_round, 0),
                    #  fight and destroy only
                    (player_set_slot, ":cur_player_a", slot_player_damage_given_to_target_1, 0),
                    (player_set_slot, ":cur_player_a", slot_player_damage_given_to_target_2, 0),
                    # #fight and destroy only end
                    (assign, ":initial_gold", multi_initial_gold_value),
                    (val_mul, ":initial_gold", "$g_multiplayer_initial_gold_multiplier"),
                    (val_div, ":initial_gold", 100),
                    (player_set_gold, ":cur_player_a", ":initial_gold"),
                    (player_set_score, ":cur_player_a", 0),
                    (player_set_kill_count, ":cur_player_a", 0),
                    (player_set_death_count, ":cur_player_a", 0),
                    (multiplayer_send_2_int_to_player, ":cur_player_a", multiplayer_event_set_team_score, 0, 0),    
                    (multiplayer_send_2_int_to_player, ":cur_player_a", multiplayer_event_set_team_score, 1, 0),    
                    (multiplayer_send_2_int_to_player, ":cur_player_a", multiplayer_event_return_num_bots_in_team, 1, "$g_multiplayer_num_bots_team_1"),
                    (multiplayer_send_2_int_to_player, ":cur_player_a", multiplayer_event_return_num_bots_in_team, 2, "$g_multiplayer_num_bots_team_2"),
                    (try_for_players, ":cur_player_b"), 
                        (player_is_active, ":cur_player_b"),
                        (multiplayer_send_4_int_to_player, ":cur_player_b", multiplayer_event_set_player_score_kill_death, ":cur_player_a", 0, 0, 0),
                    (try_end),
                    (multiplayer_send_int_to_player, ":cur_player_a", multiplayer_event_draw_this_round, -9), #to end presentation for master of the field on clients
                (try_end),
            (else_try),
                (eq, "$g_cwmm_switched_team", 1),
                (team_get_score, ":team_1_score", 0),
                (team_get_score, ":team_2_score", 1),

                (this_or_next|ge, ":team_1_score", ":max_score"),
                (ge, ":team_2_score", ":max_score"),

                (val_add, "$g_cwmm_team_1_score", ":team_2_score"),
                (val_add, "$g_cwmm_team_2_score", ":team_1_score"),
                (call_script, "script_cwmm_set_should_finish_match"),
            (try_end),
        (try_end),
    ]),

    ("cwmm_cancel_match", [
        (try_for_players, ":player_no"),
            (player_is_active, ":player_no"),
            (kick_player, ":player_no"),
        (try_end),

        (call_script, "script_cwmm_init_variables"),
    ]),

    ("cf_cwmm_item_is_available", [
        (store_script_param, ":item_no", 1),
        (assign, ":available", 1),

        (try_begin),    
            (eq, "$g_cwmm_server_is_in_match", 1),
            (eq, "$g_cwmm_mode_id", 1),

            (item_get_type, ":item_type", ":item_no"),
            (try_begin),
                (this_or_next|eq, ":item_type", itp_type_two_handed_wpn),
                (this_or_next|eq, ":item_type", itp_type_polearm),
                (eq, ":item_type", itp_type_thrown),
                (assign, ":available", 0),
            (try_end),
        (try_end), 

        (eq, ":available", 1),
    ]),

    ("cwmm_finish_match", [
        (try_for_players, ":player_no"),
            (player_is_active, ":player_no"),
            (kick_player, ":player_no"),
        (try_end),

        (call_script, "script_cwmm_init_variables"),
    ]),

    ("cwmm_add_player_stat", [
        (store_script_param, ":player_no", 1),
        (store_script_param, ":index_no", 2),
        (store_script_param, ":value", 3),

        (player_get_unique_id, ":guid", ":player_no"),
        (try_begin),
            (is_between, ":index_no", 0, CWMM_DATA_ARRAY_SLOTS),
            (assign, reg17, ":guid"),
            (str_store_string, s17, "@{reg17}"),
            (dict_has_key, "$cwmm_data_dict", s17),
            (dict_get_int, ":record_no", "$cwmm_data_dict", s17, -1),
            (ge, ":record_no", 0),

            (array_get_val, ":raw_value", "$cwmm_data_array", ":record_no", ":index_no"),
            (val_add, ":raw_value", ":value"),
            (array_set_val, "$cwmm_data_array", ":raw_value", ":record_no", ":index_no"),
        (try_end),
    ]),

    ("cwmm_set_should_cancel_match", [
        (assign, "$g_cwmm_should_cancel_match", 1),
    ]),

    ("cwmm_set_should_finish_match", [
        (assign, "$g_cwmm_should_finish_match", 1),
    ]),

    ("cwmm_init_variables", [
        (dict_clear, "$cwmm_data_dict"),
        (array_set_val_all, "$cwmm_data_array", 0),
        (assign, "$cwmm_next_data_index", 0),

        (assign, "$g_cwmm_server_is_in_match", 0),
        (assign, "$g_cwmm_server_match_id", -1),
        (assign, "$g_cwmm_server_is_waiting_for_players", 0),
        (assign, "$g_cwmm_match_countdown", 10000000),
        (assign, "$g_cwmm_should_cancel_match", 0),
        (assign, "$g_cwmm_should_finish_match", 0),
        (assign, "$g_cwmm_wait_time_seconds", 10000000),
        (assign, "$g_cwmm_next_tick_seconds", 10),
        (assign, "$g_cwmm_last_round_entry_point", -1),

        (assign, "$g_cwmm_mode_id", -1),
        (assign, "$g_cwmm_map_id", -1),
        (assign, "$g_cwmm_team_1_faction", -1),
        (assign, "$g_cwmm_team_2_faction", -1),
        (assign, "$g_cwmm_team_size", 0),
        (assign, "$g_cwmm_archer_limit", 0),
        (assign, "$g_cwmm_infantry_limit", 0),
        (assign, "$g_cwmm_cavalry_limit", 0),
        (assign, "$g_cwmm_switched_team", 0),
        (assign, "$g_cwmm_team_1_score", 0),
        (assign, "$g_cwmm_team_2_score", 0),

    ]),

    ("cwmm_server_tick", [
        (str_store_server_name, s13),
        (send_message_to_url, "str_cwmm_api_tick_server"),
    ]),

]
