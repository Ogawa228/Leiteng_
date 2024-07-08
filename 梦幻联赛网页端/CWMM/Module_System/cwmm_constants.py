# -*- coding: utf8 -*-

CWMM_DEFAULT_TICK_INTERVAL = 10
CWMM_MATCH_START_COUNDOWN = 10
CWMM_TEAM_SWITCH_COUNDOWN = 20

# 字典存储guid到data_array index的映射
# 每条data占9个数据：guid, kill, team_kill，death，damage，team_damage，hit，team_hit, spawned_as_infantry
# 别修改，前端和后端代码也依赖这些值
CWMM_DATA_ARRAY_SLOTS = 10
INDEX_GUID = 0
INDEX_KILL = 1
INDEX_TEAM_KILL = 2
INDEX_DEATH = 3
INDEX_DAMAGE = 4
INDEX_TEAM_DAMAGE = 5
INDEX_HIT = 6
INDEX_TEAM_HIT = 7
INDEX_SPAWNED_AS_INFANTRY = 8

CWMM_DEATH_MODE_TIME = 120 + 20 # 2:20

slot_player_allowed_team = 201
slot_player_not_allowed_team_counter = 202
