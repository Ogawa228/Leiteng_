from cwmm_config import *

cwmm_strings = [
    ("cwmm_api_tick_server", CWMM_BACKEND_HOST + "tick?n={s13}"),
    ("cwmm_api_player_join", CWMM_BACKEND_HOST + "player-join?p={reg11}&i={reg12}&n={s9}&s={s10}"),
    ("cwmm_api_cancel_match", CWMM_BACKEND_HOST + "cancel?s={s11}&p={s10}"),
    ("cwmm_api_finish_match", CWMM_BACKEND_HOST + "finish?s={s11}&p={s10}&s1={reg11}&s2={reg12}"),

    ("cwmm_s14_belong_to_team_1", "{s14} is teammate of team 1"),
    ("cwmm_s14_belong_to_team_2", "{s14} is teammate of team 2"),
    ("cwmm_you_are_not_allowed_by_this_team", "You are not teammate of this team"),

    ("cwmm_reg11_seconds_wait_reg12_reg13", "Remaining time: {reg11}. Present: {reg12} / {reg13}"),
    ("cwmm_start_countdown_reg14", "Countdown: {reg14}"),

    ("cwmm_troop_count_reg31_reg32_reg33_reg34_reg35_reg36", "Ranged: {reg31} / {reg32}, Inf: {reg33} / {reg34}, Cav: {reg35} / {reg36}"),
    ("cwmm_current_score_reg21_reg22", "Score: {reg21} - {reg22}"),
]
