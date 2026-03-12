"""
This source file is part of the Warlords
Copyright (c) 2024
See LICENSE.txt for details
"""

from module_constants import *
from ID_factions import *
from header_items import  *
from header_operations import *
from header_triggers import *
from mercenaries_triggers import *
from mercenaries_items_modification import starter_items
from module_meshes import native_banner_meshes, native_banner_kingdom_meshes
from mercenaries_banners import mercenaries_banner_meshes, mercenaries_clan_banner_meshes

itc_m_2h_mace = itc_cut_two_handed | itcf_thrust_polearm | itc_parry_two_handed | itcf_thrust_onehanded_lance
itc_m_heavy_greatsword = itc_cut_two_handed | itc_parry_two_handed | itcf_thrust_polearm
itc_m_dagger = itcf_force_64_bits | itcf_thrust_onehanded
itc_m_broad_dagger = itc_m_dagger | itcf_overswing_onehanded

mercenaries_items = [

    # PRACTICE WEAPON
    ["m_practice_sword", "Practice Sword", [("practice_sword", 0)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_wooden_parry|itp_wooden_attack|itp_merchandise, itc_longsword,                            40,weight(0.75)| difficulty(0) | spd_rtng(102) | weapon_length(100) | swing_damage(14, blunt) | thrust_damage(17, blunt), imodbits_none],
    ["m_heavy_practice_sword", "Two Handed Practice Sword", [("heavy_practicesword", 0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary|itp_wooden_parry|itp_wooden_attack|itp_merchandise, itc_greatsword,    50,weight(1.0) | difficulty(0) | spd_rtng(99)  | weapon_length(117) | swing_damage(15, blunt) | thrust_damage(18, blunt), imodbits_none],
    ["m_staff", "Practice Staff", [("wooden_staff", 0)], itp_type_polearm|itp_offset_lance|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_wooden_attack|itp_merchandise, itc_staff|itcf_carry_sword_back, 30,weight(0.75)| difficulty(0) | spd_rtng(99)  | weapon_length(128) | swing_damage(14, blunt) | thrust_damage(17, blunt), imodbits_polearm ],
    ["m_arena_axe", "Practice Axe", [("arena_axe", 0)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_axe_left_hip,          60,weight(1.0) | difficulty(0) | spd_rtng(102) | weapon_length(70)  | swing_damage(25, cut)   | thrust_damage(0, pierce), imodbits_axe ],
    # ["m_arena_lance", "Practice Lance", [("arena_lance", 0)], itp_type_polearm|itp_offset_lance|itp_primary|itp_couchable|itp_penalty_with_shield|itp_wooden_parry, itc_cutting_spear,                              70,weight(1.5) | difficulty(0) | spd_rtng(95)  | weapon_length(150) | swing_damage(15, blunt) | thrust_damage(18, blunt), imodbits_polearm ], 
    ["m_wooden_stick", "Wooden Stick", [("wooden_stick", 0)], itp_type_one_handed_wpn|itp_primary|itp_wooden_attack|itp_wooden_parry, itc_scimitar,                                                                 2, weight(0.75)| difficulty(0) | spd_rtng(102) | weapon_length(63)  | swing_damage(14, blunt) | thrust_damage(0,  pierce), imodbits_none], 

    # ONE-HANDED WEAPON

    # Daggers
    ["m_pikeman_dagger", "Cross-Hilt Dagger", [("15_pikeman_dagger", 0), ("15_pikeman_dagger_scab", ixmesh_carry),("15_pikeman_dagger_inv", ixmesh_inventory)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_no_parry|itp_penalty_with_shield|itp_merchandise|custom_kill_info(7), itc_m_dagger|itcf_carry_dagger_front_left|itcf_show_holster_when_drawn,
     3250, weight(1.25) | difficulty(0) | spd_rtng(98) | weapon_length(42) | swing_damage(0, cut) | thrust_damage(25, pierce), imodbits_sword_high ], 
    ["m_dagger_b", "Tapered Dagger", [("dagger_b", 0), ("dagger_b_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_no_parry|itp_penalty_with_shield|itp_merchandise|custom_kill_info(7), itc_m_dagger|itcf_carry_dagger_front_left|itcf_show_holster_when_drawn,
     3300, weight(1.25) | difficulty(0) | spd_rtng(99) | weapon_length(38) | swing_damage(0, cut) | thrust_damage(26, pierce), imodbits_sword_high ], 
    ["m_dagger", "Long Dagger", [("dagger", 0), ("m_dagger_scab", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_no_parry|itp_penalty_with_shield|itp_merchandise|custom_kill_info(7), itc_m_dagger|itcf_carry_dagger_front_left|itcf_show_holster_when_drawn,
     3400, weight(1.25) | difficulty(0) | spd_rtng(98) | weapon_length(48) | swing_damage(0, cut) | thrust_damage(24, pierce), imodbits_sword_high ],
    ["m_broad_dagger", "Broad Dagger", [("m_norman_dagger", 0), ("m_norman_dagger_scab", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_no_parry|itp_penalty_with_shield|itp_merchandise|custom_kill_info(7), itc_m_broad_dagger|itcf_carry_dagger_front_left|itcf_show_holster_when_drawn,
     3500, weight(1.25) | difficulty(0) | spd_rtng(98) | weapon_length(44) | swing_damage(20, cut)| thrust_damage(24, pierce), imodbits_sword_high ], 


#elim ilen dayi
    ["m_fire_arrows", "Flaming Arrows", [("warlords_arrow_flaming_mesh", 0), ("m_flying_missile_fire", ixmesh_flying_ammo), ("warlords_arrow_flaming_quiver_mesh", ixmesh_carry)], itp_type_arrows|itp_merchandise, itcf_carry_quiver_back_right,                                0, weight(1.5) | abundance(100) | weapon_length(91) | thrust_damage(2, pierce) | max_ammo(12), imodbits_missile, [(ti_on_init_item, [(set_position_delta, 0, 80, 0),(particle_system_add_new, "psys_torch_fire", pos1),]),(ti_on_init_missile, [(set_position_delta, 0, 80, 0),(particle_system_add_new, "psys_torch_fire", pos1),]),m_missile_init_trigger,(ti_on_missile_dive, [(particle_system_remove),]), m_fire_arrow_hit_trigger] ],


    # 1h pickaxes
    ["m_rusty_pick", "Rusty Pick", [("swup_rusty_pick", 0)], itp_type_one_handed_wpn|itp_primary|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_axe_left_hip,
     700,  weight(1.0) | difficulty(0)  | spd_rtng(102) | weapon_length(70) | swing_damage(26, pierce) | thrust_damage(0, pierce), imodbits_pick ], 
    ["m_military_sickle_a", "Sickle", [("military_sickle_a", 0)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_axe_left_hip,
     1000,  weight(1.3) | difficulty(9)  | spd_rtng(101) | weapon_length(75) | swing_damage(26, pierce) | thrust_damage(0, pierce), imodbits_axe ], 
    ["m_fighting_pick", "Pick", [("fighting_pick_new", 0)], itp_type_one_handed_wpn|itp_primary|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_axe_left_hip,
     1200,  weight(1.5)| difficulty(8)  | spd_rtng(101) | weapon_length(70) | swing_damage(27, pierce) | thrust_damage(0, pierce), imodbits_pick ], 

    ["m_military_pick", "Iron Pick", [("steel_pick_new", 0)], itp_type_one_handed_wpn|itp_primary|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_axe_left_hip,     
     4540, weight(1.8) | difficulty(12) | spd_rtng(96)  | weapon_length(70) | swing_damage(31, pierce) | thrust_damage(0, pierce), imodbits_pick ], 
    ["gg_steel_pick_new","Steel Pick", [("gg_steel_pick", 0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary, itcf_carry_axe_left_hip|itc_scimitar,
     4700, weight(1.6) | difficulty(12) | spd_rtng(98)  | weapon_length(68) | swing_damage(30, pierce) | thrust_damage(0, pierce), imodbits_pick ], 

    # ["gg_steel_pick", "Steel Pick", [("gg_steel_pick", 0)], itp_type_one_handed_wpn|itp_primary|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_axe_left_hip,
     # 5000, weight(2) | difficulty(17) | spd_rtng(96)  | weapon_length(65) | swing_damage(33, pierce) | thrust_damage(0, pierce), imodbits_pick ], 
    ["gg_one_handed_short_morningstar", "One Handed Short Morningstar", [("gg_one_handed_short_morningstar", 0)], itp_type_one_handed_wpn|itp_primary|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_axe_left_hip,
     4800, weight(2.3) | difficulty(13) | spd_rtng(99)  | weapon_length(60) | swing_damage(31, pierce) | thrust_damage(0, pierce), imodbits_pick ], 
    ["gg_bastard_pick", "Outlanders Strange Pick", [("gg_bastard_pick", 0)], itp_type_one_handed_wpn|itp_primary|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_axe_left_hip,
     4900, weight(2) | difficulty(13) | spd_rtng(100)  | weapon_length(65) | swing_damage(29, pierce) | thrust_damage(0, pierce), imodbits_pick ], 

    # 1h blunt weapon
    ["m_mace_1", "Spiked Club", [("mace_d", 0)], itp_type_one_handed_wpn|itp_primary|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_mace_left_hip,                                                                    
    300,  weight(1.0)  | difficulty(0)  | spd_rtng(101) | weapon_length(71) | swing_damage(21, pierce)| thrust_damage(0, pierce), imodbits_mace ], 
    ["m_mace_3", "Spiked Mace", [("mace_c", 0)], itp_type_one_handed_wpn|itp_primary|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_mace_left_hip,                                                                    
    700,  weight(1.75) | difficulty(8)  | spd_rtng(101) | weapon_length(72) | swing_damage(25, blunt) | thrust_damage(0, pierce), imodbits_mace ], 
    ["m_mace_4", "Winged Mace", [("mace_b", 0)], itp_type_one_handed_wpn|itp_primary|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_mace_left_hip,                                                                    
    1000, weight(2.0) | difficulty(10) | spd_rtng(99)  | weapon_length(72) | swing_damage(26, blunt) | thrust_damage(0, pierce), imodbits_mace ], 
    ["m_mace_2", "Knobbed Mace", [("mace_a", 0)], itp_type_one_handed_wpn|itp_primary|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_mace_left_hip,
    1500,  weight(1.8) | difficulty(10) | spd_rtng(101) | weapon_length(71) | swing_damage(25, blunt) | thrust_damage(0, pierce), imodbits_mace ], 
    ["m_heavy_spiked_mace", "Knobbed Mace", [("faradon_iberianmace", 0)], itp_type_one_handed_wpn|itp_primary|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_mace_left_hip,                                           
    1550,  weight(1.8) | difficulty(10) | spd_rtng(101) | weapon_length(71) | swing_damage(25, blunt) | thrust_damage(0, pierce), imodbits_mace ], 
    ["m_hammer", "Small Hammer", [("iron_hammer_new", 0)], itp_type_one_handed_wpn|itp_primary|itp_wooden_parry|itp_merchandise, itc_scimitar,                                                                                   
    1600,  weight(1.7)  | difficulty(8)  | spd_rtng(100) | weapon_length(58) | swing_damage(28, blunt) | thrust_damage(0, pierce), imodbits_mace ], 
    ["gg_outlander_flanged_mace", "Outlanders Flanged Mace", [("gg_outlander_flanged_mace", 0)], itp_type_one_handed_wpn|itp_can_knock_down|itp_primary|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_mace_left_hip,
     2500,  weight(2.0) | difficulty(11) | spd_rtng(98) | weapon_length(60) | swing_damage(28, blunt) | thrust_damage(0, pierce), imodbits_mace ], 
    ["m_winged_mace", "Flanged Mace", [("flanged_mace", 0)], itp_type_one_handed_wpn|itp_primary|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_mace_left_hip,
     2400, weight(2.0)  | difficulty(11) | spd_rtng(98)  | weapon_length(70) | swing_damage(27, blunt) | thrust_damage(0, pierce), imodbits_mace ], 
    ["m_military_hammer", "Heavy Hammer", [("military_hammer", 0)], itp_type_one_handed_wpn|itp_can_knock_down|itp_primary|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_axe_left_hip,                                                  
     4100, weight(2.2)  | difficulty(12) | spd_rtng(95)  | weapon_length(70) | swing_damage(29, blunt) | thrust_damage(0, pierce), imodbits_mace ], 
    ["m_one_handed_warhammer", "Warhammer", [("faradon_warhammer", 0), ("faradon_warhammer_carry", ixmesh_carry)], itp_type_one_handed_wpn|itp_can_knock_down|itp_primary|itp_wooden_parry|itp_merchandise, itc_longsword|itcf_carry_axe_left_hip,
     4980, weight(1.8)  | difficulty(12) | spd_rtng(96)  | weapon_length(75) | swing_damage(28, blunt) | thrust_damage(23,pierce), imodbits_mace ], 
    ["m_spiked_mace", "Iron Spiked Mace", [("spiked_mace_new", 0)], itp_type_one_handed_wpn|itp_can_knock_down|itp_primary|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_mace_left_hip,
     4290, weight(2.2) | difficulty(13) | spd_rtng(95)  | weapon_length(70) | swing_damage(29, blunt) | thrust_damage(0, pierce), imodbits_pick ], 
    ["gg_outlanders_spiked_mace", "Outlander Spiked Mace", [("gg_outlanders_spiked_mace", 0)], itp_type_one_handed_wpn|itp_primary|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_mace_left_hip,
     4300,  weight(2.25) | difficulty(13) | spd_rtng(98) | weapon_length(72) | swing_damage(28, blunt) | thrust_damage(0, pierce), imodbits_mace ], 
    ["m_sarranid_mace_1", "Iron Mace", [("mace_small_d", 0)], itp_type_one_handed_wpn|itp_can_knock_down|itp_primary|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_mace_left_hip,
     4380, weight(2.2)  | difficulty(14) | spd_rtng(95)  | weapon_length(70) | swing_damage(29, blunt) | thrust_damage(0, pierce), imodbits_mace ],
    ["m_8_flanged_mace", "Masterwork Flanged Mace", [("m_8_flanged_mace", 0)], itp_type_one_handed_wpn|itp_can_knock_down|itp_primary|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_mace_left_hip,                                      
    85000,weight(2.0) | difficulty(13) | spd_rtng(95)  | weapon_length(70) | swing_damage(29, blunt) | thrust_damage(0, pierce), imodbits_mace ],	
    ["gg_outlanders_iberian_mace", "Outlanders Iberian Mace", [("gg_outlanders_iberian_mace", 0)], itp_type_one_handed_wpn|itp_can_knock_down|itp_primary|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_mace_left_hip,
     4400,  weight(2.2) | difficulty(14) | spd_rtng(95) | weapon_length(70) | swing_damage(29, blunt) | thrust_damage(0, pierce), imodbits_mace ], 
    ["gg_outlanders_warhammer", "Outlander Warhammer", [("gg_outlanders_warhammer", 0)], itp_type_one_handed_wpn|itp_can_knock_down|itp_primary|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_mace_left_hip,
     4500,  weight(2.20) | difficulty(14) | spd_rtng(96) | weapon_length(65) | swing_damage(29, blunt) | thrust_damage(0, pierce), imodbits_mace ], 
    ["gg_one_handed_barmace", "One Handed Bar Mace", [("gg_one_handed_barmace", 0)], itp_type_one_handed_wpn|itp_can_knock_down|itp_primary|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_mace_left_hip,
     4800,  weight(2.6) | difficulty(18) | spd_rtng(93) | weapon_length(72) | swing_damage(30, blunt) | thrust_damage(0, pierce), imodbits_mace ], 
    ["gg_outlanders_horseman_hammer", "Outlanders Horseman Hammer", [("gg_outlanders_horseman_hammer", 0)], itp_type_one_handed_wpn|itp_can_knock_down|itp_primary|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_mace_left_hip,
     0,  weight(2.6) | difficulty(20) | spd_rtng(91) | weapon_length(82) | swing_damage(28, blunt) | thrust_damage(0, pierce), imodbits_mace ], 
    ["gg_outlanders_iron_hammer", "Outlanders Iron Hammer", [("gg_outlanders_iron_hammer", 0)], itp_type_one_handed_wpn|itp_can_knock_down|itp_primary|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_mace_left_hip,
     0,  weight(5) | difficulty(17) | spd_rtng(94) | weapon_length(74) | swing_damage(27, blunt) | thrust_damage(0, pierce), imodbits_mace ], 



    # Light 1h swords
    # ["m_medieval_falchion_a", "Short Falchion", [("medieval_falchion_a", 0)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_scimitar|itcf_carry_sword_left_hip,                                                                                                       450,  weight(1.0)  | difficulty(0) | spd_rtng(102) | weapon_length(60) | swing_damage(27, cut) | thrust_damage(0,  pierce), imodbits_sword ], 
    # ["m_italian_falchion", "Italian Falchion", [("italian_falchion", 0), ("italian_falchion_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,                                 470,  weight(1.0)  | difficulty(0) | spd_rtng(102) | weapon_length(70) | swing_damage(28, cut) | thrust_damage(0,  pierce), imodbits_sword ], 
    ["m_falchion", "Falchion", [("falchion_new", 0)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_scimitar|itcf_carry_sword_left_hip,                                                                                                                               
    500,  weight(1.0)  | difficulty(8) | spd_rtng(102) | weapon_length(74) | swing_damage(30, cut) | thrust_damage(0,  pierce), imodbits_sword ],
    # ["m_medieval_falchion_b", "Heavy Falchion", [("medieval_falchion_b", 0)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_scimitar|itcf_carry_sword_left_hip,                                                                                                       550,  weight(1.5)  | difficulty(8) | spd_rtng(99)  | weapon_length(80) | swing_damage(30, cut) | thrust_damage(0,  pierce), imodbits_sword ], 	
    ["m_sword_medieval_c_small", "Short Sword", [("sword_medieval_c_small", 0), ("sword_medieval_c_small_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,                   
    1200, weight(1.0) | difficulty(8) | spd_rtng(102) | weapon_length(82) | swing_damage(25, cut) | thrust_damage(32, pierce), imodbits_sword_high ], 
    ["m_sword_viking_2_small", "Nordic Short Sword", [("sword_viking_b_small", 0), ("sword_viking_b_small_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,                  
    1230, weight(1.3) | difficulty(8) | spd_rtng(102) | weapon_length(82) | swing_damage(26, cut) | thrust_damage(31, pierce), imodbits_sword_high ],
    ["m_sword_viking_3_small", "Nordic Short Sword with Curved Guard", [("sword_viking_a_small", 0), ("sword_viking_a_small_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
    1300, weight(1.5) | difficulty(9) | spd_rtng(101) | weapon_length(82) | swing_damage(28, cut) | thrust_damage(30, pierce), imodbits_sword_high ], 
    ["m_sword_medieval_e", "Light Sabre", [("sword_medieval_e", 0), ("sword_medieval_e_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,                                     
    1450, weight(1.3) | difficulty(9) | spd_rtng(103) | weapon_length(95) | swing_damage(29, cut) | thrust_damage(25, pierce), imodbits_sword ], 

 #   ["m_mon_saber_2_1", "Long Sabre", [("mon_saber_2_1", 0), ("mon_saber_2_2", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 #    1870, weight(1.25) | difficulty(9) | spd_rtng(101) | weapon_length(95) | swing_damage(27, cut) | thrust_damage(26, pierce), imodbits_sword_high ], 

    ["m_sword_khergit_2", "Nomad Sabre", [("khergit_sword_b", 0), ("khergit_sword_c_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,                                        
    1500, weight(1.6) | difficulty(9) | spd_rtng(101) | weapon_length(86) | swing_damage(31, cut) | thrust_damage(23, pierce), imodbits_sword_high ],
    # ["m_grosse_messer_2", "Grosse Messer", [("grosse_messer", 0)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip,                                                                                                                 1970, weight(1.25) | difficulty(9) | spd_rtng(101) | weapon_length(86) | swing_damage(30, cut) | thrust_damage(22, pierce), imodbits_sword ], 
    ["m_sword_khergit_1", "Sabre", [("khergit_sword_c", 0), ("khergit_sword_b_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,                                              
    1800, weight(1.5) | difficulty(9) | spd_rtng(101) | weapon_length(88) | swing_damage(30, cut) | thrust_damage(24, pierce), imodbits_sword_high ], 
    # ["m_mon_saber_1_1", "Sabre", [("mon_saber_1_1", 0), ("mon_saber_1_2", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,                                                             2250, weight(1.25) | difficulty(9) | spd_rtng(101) | weapon_length(88) | swing_damage(29, cut) | thrust_damage(24, pierce), imodbits_sword_high ], 
	
    # Medium 1h swords
    ["m_scimitar", "Scimitar", [("scimitar_a", 0), ("scab_scimeter_a", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,                                                                
    2100, weight(1.3)| difficulty(10) | spd_rtng(99) | weapon_length(96) | swing_damage(32, cut) | thrust_damage(0,  pierce), imodbits_sword_high ], 
    ["m_sword_medieval_a", "Sword", [("sword_medieval_a", 0), ("sword_medieval_a_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,                                          
    2500, weight(1.5) | difficulty(12) | spd_rtng(99) | weapon_length(95) | swing_damage(29, cut) | thrust_damage(29, pierce), imodbits_sword_high ], 
    ["m_sword_medieval_c", "Sword with Curved Guard", [("sword_medieval_c", 0), ("sword_medieval_c_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,                        
    2600, weight(1.6) | difficulty(12) | spd_rtng(99) | weapon_length(95) | swing_damage(30, cut) | thrust_damage(27, pierce), imodbits_sword_high ], 
    ["m_sword_viking_2", "Nordic Sword", [("sword_viking_b", 0), ("sword_viking_b_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,                                         
    2650, weight(1.7) | difficulty(12) | spd_rtng(98) | weapon_length(95) | swing_damage(31, cut) | thrust_damage(26, pierce), imodbits_sword_high ], 
    # ["m_side_sword", "Side Sword", [("side_sword", 0), ("side_sword_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,                                                       2800, weight(1.5) | difficulty(12) | spd_rtng(98) | weapon_length(95) | swing_damage(30, cut) | thrust_damage(26, pierce), imodbits_sword_high ], 
    ["m_longbowman_sword", "Sword with Knuckle-Bow", [("15_longbowman_sword", 0), ("15_longbowman_sword_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,                   
    2900, weight(1.25)| difficulty(10) | spd_rtng(100) | weapon_length(90) | swing_damage(29, cut) | thrust_damage(29, pierce), imodbits_sword ],
    # ["m_Shot_dual", "Short Sword", [("Shot_dual", 0), ("Shot_dual_scab", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,                                                             70000,weight(1.5) | difficulty(12) | spd_rtng(98) | weapon_length(95) | swing_damage(30, cut) | thrust_damage(26, pierce), imodbits_sword_high ], 
	
    # Heavy 1h swords
    ["m_military_cleaver_b", "Cleaver", [("military_cleaver_b", 0)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_scimitar|itcf_carry_sword_left_hip,                                                                                                               
    2750,   weight(2.2) | difficulty(14) | spd_rtng(97) | weapon_length(92)  | swing_damage(34, cut) | thrust_damage(0,  pierce), imodbits_sword_high ],
    ["m_grosse_messer", "Great Knife", [("15_grosse_messer_b", 0), ("15_grosse_messer_b_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,                                   
    2500,   weight(2.0)| difficulty(14) | spd_rtng(97) | weapon_length(92)  | swing_damage(34, cut) | thrust_damage(24, pierce), imodbits_sword ],
    # ["m_espada_eslavona_a", "Espada Sword", [("espada_eslavona_a", 0)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip,                                                                                                           3050,   weight(1.75)| difficulty(14) | spd_rtng(97) | weapon_length(92)  | swing_damage(33, cut) | thrust_damage(22, pierce), imodbits_sword ],
    ["m_scimitar_b", "Heavy Scimitar", [("scimitar_b", 0), ("scab_scimeter_b", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,                                                        
    4800,   weight(1.7) | difficulty(13) | spd_rtng(98) | weapon_length(100) | swing_damage(33, cut) | thrust_damage(0,  pierce), imodbits_sword_high ],
    ["m_sword_khergit_4", "Heavy Sabre", [("khergit_sword_d", 0), ("khergit_sword_d_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,                                        
    4900,   weight(1.8)| difficulty(13) | spd_rtng(99) | weapon_length(88)  | swing_damage(33, cut) | thrust_damage(0,  pierce), imodbits_sword_high ],
    ["m_arabian_sword_a", "Sarranid Guard Sword", [("arabian_sword_a", 0), ("scab_arabian_sword_a", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
    5000,   weight(1.8)| difficulty(13) | spd_rtng(98) | weapon_length(100) | swing_damage(33, cut) | thrust_damage(25, pierce), imodbits_sword_high ],
    ["m_arabian_sword_b", "Broad Sarranid Sword", [("arabian_sword_b", 0), ("scab_arabian_sword_b", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,                                  
    5100,   weight(2.0)| difficulty(13) | spd_rtng(96) | weapon_length(100) | swing_damage(34, cut) | thrust_damage(23, pierce), imodbits_sword_high ],
    ["m_military_cleaver_c", "Heavy Cleaver", [("military_cleaver_c", 0)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_scimitar|itcf_carry_sword_left_hip,                                                                                                               
    5450,   weight(2.3) | difficulty(14) | spd_rtng(96) | weapon_length(92)  | swing_damage(36, cut) | thrust_damage(0,  pierce), imodbits_sword_high ],
    ["m_sarranid_cavalry_sword", "Sarranid Cavalry Sword", [("arabian_sword_c",0),("scab_arabian_sword_c", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
    5350,   weight(2.0)| difficulty(14) | spd_rtng(95) | weapon_length(105) | swing_damage(34, cut) | thrust_damage(23, pierce), imodbits_sword_high ],
    ["gg_demi_knight_cavalry_sword", "Demi Knight Cavalary Sword", [("gg_demi_knight_cavalry_sword",0),("gg_demi_knight_cavalry_sword_sheath", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
    5900,   weight(1.8)| difficulty(14) | spd_rtng(96) | weapon_length(105) | swing_damage(33, cut) | thrust_damage(25, pierce), imodbits_sword_high ],

    # ["m_Gallowglass", "Long Sword", [("Gallowglass",0),("Gallowglass_scabb", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,                                                         4430,   weight(1.75)| difficulty(14) | spd_rtng(95) | weapon_length(105) | swing_damage(33, cut) | thrust_damage(22, pierce), imodbits_sword_high ],
    ["m_sword_medieval_c_long", "Heavy Sword", [("sword_medieval_c_long", 0), ("sword_medieval_c_long_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,                     
    5550,   weight(1.8)| difficulty(13) | spd_rtng(97) | weapon_length(102) | swing_damage(33, cut) | thrust_damage(26, pierce), imodbits_sword ],
    # ["m_espada_eslavona_b", "Espada", [("espada_eslavona_b", 0), ("espada_eslavona_b_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,                                      4590,   weight(1.75)| difficulty(13) | spd_rtng(97) | weapon_length(102) | swing_damage(31, cut) | thrust_damage(25, pierce), imodbits_sword_high ], 
    ["m_sword_viking_a_long", "Heavy Nordic Sword", [("sword_viking_a_long", 0), ("sword_viking_a_long_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,                    
    5630,   weight(1.8)| difficulty(13) | spd_rtng(97) | weapon_length(102) | swing_damage(33, cut) | thrust_damage(26, pierce), imodbits_sword ],
    ["m_arabian_sword_d", "Heavy Sarranid Sword", [("arabian_sword_d", 0), ("scab_arabian_sword_d", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,                                  
    5750,   weight(2.0)| difficulty(13) | spd_rtng(97) | weapon_length(100) | swing_damage(33, cut) | thrust_damage(26, pierce), imodbits_sword_high ],

    ["gg_demi_knight_sword", "Demi Knight Sword", [("gg_demi_knight_sword", 0), ("gg_demi_knight_sword_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
    5880,   weight(1.8)| difficulty(15) | spd_rtng(98) | weapon_length(100) | swing_damage(32, cut) | thrust_damage(28, pierce), imodbits_sword ],

    # ["m_w_light_kopis_officer", "Epic Sword", [("w_light_kopis_officer", 0)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip,                                                                                                     4790,   weight(1.75)| difficulty(13) | spd_rtng(97) | weapon_length(100) | swing_damage(32, cut) | thrust_damage(23, pierce), imodbits_sword ],
    # ["m_Truth", "English Sword", [("Truth", 0), ("Truth_scab", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,                                                                       4810,   weight(1.75)| difficulty(13) | spd_rtng(97) | weapon_length(100) | swing_damage(32, cut) | thrust_damage(23, pierce), imodbits_sword ],
    ["m_sword_medieval_d_long", "Heavy Swadian Sword", [("sword_medieval_d_long", 0), ("sword_medieval_d_long_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,             
    5850,   weight(1.8)| difficulty(13) | spd_rtng(97) | weapon_length(102) | swing_damage(33, cut) | thrust_damage(26, pierce), imodbits_sword ],
    # ["m_rus_sword_1_1", "Heavy Rus Sword", [("rus_sword_1_1", 0), ("rus_sword_1_2", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,                                                  5000,   weight(1.75)| difficulty(13) | spd_rtng(97) | weapon_length(102) | swing_damage(31, cut) | thrust_damage(25, pierce), imodbits_sword ],
    ["gg_nordlander_chosen_sword", "Nordlander Elite Sword", [("gg_nordlander_chosen_sword", 0), ("gg_nordlander_chosen_sword_scab", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
    5000,   weight(1.8)| difficulty(15) | spd_rtng(98) | weapon_length(102) | swing_damage(33, cut) | thrust_damage(24, pierce), imodbits_sword ],
    ["m_noble_sword", "Noble Sword", [("gg_noble_sword", 0), ("gg_noble_sword_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
     110000, weight(2)| difficulty(13) | spd_rtng(97) | weapon_length(103) | swing_damage(33, cut) | thrust_damage(27, pierce), imodbits_sword ],
	
    # 1h axes
    ["m_one_handed_war_axe_b", "Old Axe", [("one_handed_war_axe_b", 0)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_axe_left_hip,                                                     
    400,  weight(1.2) | difficulty(0)  | spd_rtng(101) | weapon_length(71) | swing_damage(28, cut) | thrust_damage(0, pierce), imodbits_axe ],
    ["m_one_handed_battle_axe_a", "Axe", [("one_handed_battle_axe_a", 0)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_axe_left_hip,                                                   
    1500,  weight(1.25)| difficulty(9)  | spd_rtng(100) | weapon_length(73) | swing_damage(31, cut) | thrust_damage(0, pierce), imodbits_axe ],
    ["m_vaegir_cavalry_axe", "Vaegir Cavalry Axe", [("bb_nevsky_axe", 0)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_axe_left_hip,                                                   
    2100, weight(1.5)| difficulty(10) | spd_rtng(99) | weapon_length(70) | swing_damage(31, cut) | thrust_damage(0, pierce), imodbits_axe ],
    ["m_axe_1", "Short Bearded Axe", [("faradon_axe_1", 0), ("faradon_axe_1_carry", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_axe_left_hip,                          
    0, weight(1.75)| difficulty(11) | spd_rtng(99)  | weapon_length(70) | swing_damage(33, cut) | thrust_damage(0, pierce), imodbits_axe ],
    # ["m_Greyjoy_axe", "Varag Axe", [("Greyjoy_axe", 0)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_axe_left_hip,                                                                     1230, weight(1.75)| difficulty(11) | spd_rtng(99)  | weapon_length(70) | swing_damage(33, cut) | thrust_damage(0, pierce), imodbits_axe ],
    ["m_axe_2", "Heavy Axe", [("faradon_axe_2", 0), ("faradon_axe_2_carry", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_axe_left_hip,                                  
    2950, weight(2.3) | difficulty(13) | spd_rtng(97)  | weapon_length(73) | swing_damage(35, cut) | thrust_damage(0, pierce), imodbits_axe ],
    ["m_one_handed_battle_axe_b", "Broad Bladed Axe", [("one_handed_battle_axe_b", 0)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_axe_left_hip,                                      
    3300, weight(1.8)| difficulty(13) | spd_rtng(98)  | weapon_length(75) | swing_damage(34, cut) | thrust_damage(0, pierce), imodbits_axe ],
    ["m_one_handed_battle_axe_c", "Heavy Broad Bladed Axe", [("one_handed_battle_axe_c", 0)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_axe_left_hip,                                
    3850, weight(2.0) | difficulty(14) | spd_rtng(97)  | weapon_length(75) | swing_damage(35, cut) | thrust_damage(0, pierce), imodbits_axe ],
    ["m_sarranid_axe_b", "Iron Axe", [("one_handed_battle_axe_h", 0)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_axe_left_hip,
    5200, weight(2.25)| difficulty(15) | spd_rtng(97)  | weapon_length(70) | swing_damage(36, cut) | thrust_damage(0, pierce), imodbits_axe ],
    ["m_sarranid_axe_a", "Broad Bladed Iron Axe", [("one_handed_battle_axe_g", 0)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry|itp_merchandise, itc_scimitar|itcf_carry_axe_left_hip,
    5400, weight(2.4)| difficulty(16) | spd_rtng(94)  | weapon_length(70) | swing_damage(38, cut) | thrust_damage(0, pierce), imodbits_axe ],


#   ["gg_1h_pickaxe_c","War Pick-axe", [("gg_1h_pickaxe_c", 0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary|itp_secondary|itp_next_item_as_melee|itp_bonus_against_shield, itcf_carry_axe_left_hip|itc_longsword,
#    7500, weight(2)|abundance(100)|difficulty(14)|hit_points(35840)|spd_rtng(95)|weapon_length(72)|thrust_damage(20, pierce)|swing_damage(37, cut), imodbits_axe, []],

    ["gg_outlanders_one_handed_axe", "Masterwork One Handed Axe", [("gg_outlanders_one_handed_axe", 0)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry|itp_merchandise, itc_longsword|itcf_carry_axe_left_hip,
     60000, weight(2.5)| difficulty(15) | spd_rtng(95)  | weapon_length(72) | swing_damage(37, cut) | thrust_damage(24, pierce), imodbits_axe ],

    ["knightly_axe", "One Handed Knightly Axe", [("knightly_axe", 0)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry|itp_merchandise, itc_longsword|itcf_carry_axe_left_hip,
     5900, weight(2.2)| difficulty(15) | spd_rtng(96)  | weapon_length(70) | swing_damage(36, cut) | thrust_damage(24, pierce), imodbits_axe ],
   

    # TWO-HANDED WEAPON
    
    # 2h swords
    ["m_bastard_sword_b", "Long Bastard Sword", [("bastard_sword_b", 0), ("bastard_sword_b_scabbard", ixmesh_carry)], itp_type_two_handed_wpn|itp_primary|itp_merchandise, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
     4200,  weight(2.5)  | difficulty(14) | spd_rtng(98) | weapon_length(106) | swing_damage(34, cut) | thrust_damage(26, pierce), imodbits_sword_high ],
    ["m_sword_two_handed_b", "Two Handed Sword", [("sword_two_handed_b",0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary|itp_merchandise, itc_greatsword|itcf_carry_sword_back,
     3300,  weight(3.0)  | difficulty(16) | spd_rtng(96) | weapon_length(110) | swing_damage(36, cut) | thrust_damage(25, pierce), imodbits_sword_high ],
 #   ["m_flambard_v2", "Flambard", [("flambard_v2", 0)], itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_merchandise, itc_greatsword|itcf_carry_sword_back,
##    3700,  weight(2.5)  | difficulty(17) | spd_rtng(94) | weapon_length(116) | swing_damage(35, cut) | thrust_damage(26, pierce), imodbits_sword_high ],

    ["m_sword_two_handed_a", "Long Sword", [("sword_two_handed_a", 0)], itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_merchandise, itc_greatsword|itcf_carry_sword_back,
     4800,  weight(3.25) | difficulty(18) | spd_rtng(94) | weapon_length(118) | swing_damage(35, cut) | thrust_damage(26, pierce), imodbits_sword_high ],
    ["gg_outlander_elite_long_sword", "Outlander Elite Long Sword", [("gg_outlander_elite_long_sword", 0)], itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_merchandise, itc_greatsword|itcf_carry_sword_back,
     5000,  weight(3.25) | difficulty(18) | spd_rtng(93) | weapon_length(123) | swing_damage(37, cut) | thrust_damage(26, pierce), imodbits_sword_high ],
    ["gg_outlanders_great_sword", "Outlanders Great Sword", [("gg_outlanders_great_sword", 0), ("gg_outlanders_great_sword_scabbard", ixmesh_carry)], itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_merchandise, itc_greatsword|itcf_carry_sword_back,
     7000,  weight(3.25) | difficulty(18) | spd_rtng(96) | weapon_length(118) | swing_damage(35, cut) | thrust_damage(27, pierce), imodbits_sword_high ],

    ["gg_nordlander_huscarl_great_sword", "Nordlander Huscarl Great Sword", [("gg_nordlander_huscarl_great_sword", 0)], itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_merchandise, itc_greatsword|itcf_carry_sword_back,
     7050,  weight(3.25) | difficulty(21) | spd_rtng(93) | weapon_length(118) | swing_damage(38, cut) | thrust_damage(25, pierce), imodbits_sword_high ],

    ["gg_flambard", "Flambard", [("gg_flambard", 0)], itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_merchandise, itc_greatsword|itcf_carry_sword_back,
     5900,  weight(3.3) | difficulty(18) | spd_rtng(93) | weapon_length(117) | swing_damage(39, cut) | thrust_damage(22, pierce), imodbits_sword_high ],

    ["m_sword_handandahalf","Hand-And-A-Half_Sword", [("faradon_handandahalf", 0)], itp_type_two_handed_wpn|itp_merchandise|itp_primary, itcf_carry_sword_back|itc_bastardsword,
     4400 , weight(2.5)|difficulty(14)|spd_rtng(98)|weapon_length(106)|swing_damage(35, cut) | thrust_damage(24, pierce), imodbits_sword_high],
    ["gg_outlanders_longsword", "Outlanders Longsword", [("gg_outlanders_longsword", 0), ("gg_outlanders_longsword_scabbard", ixmesh_carry)], itp_type_two_handed_wpn|itp_primary|itp_merchandise, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
     4500 , weight(2.5)|difficulty(14)|spd_rtng(98)|weapon_length(103)|swing_damage(35, cut)|thrust_damage(24, pierce),imodbits_sword_high],
    ["gg_outlanders_bastard_sword", "Outlander Bastard Sword", [("gg_outlanders_bastard_sword", 0), ("gg_outlanders_bastard_sword_scabbard", ixmesh_carry)], itp_type_two_handed_wpn|itp_primary|itp_merchandise, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
     4600 , weight(2.2)|difficulty(14)|spd_rtng(99)|weapon_length(107)|swing_damage(33, cut) | thrust_damage(27, pierce), imodbits_sword_high],

    # ["m_khergit_sword_two_handed_b", "Long Sabre", [("khergit_sword_two_handed_b", 0)], itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_merchandise, itc_nodachi|itcf_carry_sword_back,                                                                                                     2550,  weight(2.75) | difficulty(16) | spd_rtng(95) | weapon_length(114) | swing_damage(35, cut) | thrust_damage(0, pierce),  imodbits_sword_high ],
    ["m_shortened_military_scythe", "Shortened Military Scythe", [("two_handed_battle_scythe_a", 0)], itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_merchandise, itc_nodachi|itcf_carry_sword_back,                                                                                       
    5100,  weight(3.25) | difficulty(17) | spd_rtng(94) | weapon_length(115) | swing_damage(40, cut) | thrust_damage(0, pierce),  imodbits_sword_high ],
    ["m_two_handed_cleaver", "Two Handed Cleaver", [("military_cleaver_a",0)], itp_type_two_handed_wpn|itp_two_handed|itp_cant_use_on_horseback|itp_primary|itp_unbalanced|itp_merchandise, itc_nodachi|itcf_carry_sword_back,                                                                                               
    5500,  weight(3.75) | difficulty(18) | spd_rtng(92) | weapon_length(120) | swing_damage(42, cut) | thrust_damage(0, pierce),  imodbits_sword_high ],
    ["m_khergit_sword_two_handed_a", "Heavy Long Sabre", [("khergit_sword_two_handed_a", 0)], itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_merchandise, itc_nodachi|itcf_carry_sword_back,                                                                                               
    5800,  weight(2.8)  | difficulty(17) | spd_rtng(95) | weapon_length(114) | swing_damage(39, cut) | thrust_damage(0, pierce),  imodbits_sword_high ],

    ["m_great_sword", "Great Sword", [("gg_heavy_greatsword", 0), ("gg_heavy_greatsword_scabbard", ixmesh_carry)], itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_merchandise, itc_greatsword|itcf_carry_sword_back,
     7100,  weight(3.25) | difficulty(21) | spd_rtng(94) | weapon_length(122) | swing_damage(38, cut) | thrust_damage(22, pierce), imodbits_sword_high ],  
    ["m_great_sword_2", "Tapered Long Sword", [("faradon_twohanded1", 0)], itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_merchandise, itc_greatsword|itcf_carry_sword_back,
     7200,  weight(3.0)  | difficulty(18) | spd_rtng(95) | weapon_length(120) | swing_damage(36, cut) | thrust_damage(27, pierce), imodbits_sword_high ],
    ["m_great_sword_3", "Long Sword with Ricasso", [("faradon_twohanded2", 0)], itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_merchandise, itc_greatsword|itcf_carry_sword_back,
     7400,  weight(3.0)  | difficulty(18) | spd_rtng(95) | weapon_length(119) | swing_damage(37, cut) | thrust_damage(25, pierce), imodbits_sword_high ],
    ["gg_sword_of_war", "Sword Of War", [("gg_sword_of_war", 0), ("gg_sword_of_war_scabbard", ixmesh_carry)], itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_merchandise, itc_greatsword|itcf_carry_sword_back,
     7800,  weight(3.8) | difficulty(24) | spd_rtng(90) | weapon_length(121) | swing_damage(41, cut) | thrust_damage(24, pierce), imodbits_sword_high ],
    ["gg_outlanders_claymore", "Outlanders Claymore", [("gg_outlanders_claymore", 0)], itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_merchandise, itc_greatsword|itcf_carry_sword_back,
     7900,  weight(3.3)  | difficulty(21) | spd_rtng(94) | weapon_length(126) | swing_damage(37, cut) | thrust_damage(24, pierce), imodbits_sword_high ],
    ["m_highlander_claymore", "Masterwork Claymore", [("highlander_claymore", 0)], itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_merchandise, itc_greatsword|itcf_carry_sword_back,
     102500,weight(3.2)  | difficulty(18) | spd_rtng(95) | weapon_length(112) | swing_damage(38, cut) | thrust_damage(23, pierce), imodbits_sword_high ],

    ["gg_noble_heavy_great_sword", "Noble Heavy Great Sword", [("gg_noble_heavy_great_sword", 0)], itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_unbalanced|itp_merchandise, itc_m_heavy_greatsword|itcf_carry_sword_back,
     60000,  weight(5.2)  | difficulty(21) | spd_rtng(87) | weapon_length(140) | swing_damage(42, cut) | thrust_damage(25, pierce), imodbits_sword_high ],	
    ["m_butchers_sword", "Barbed Two-Hander", [("spak_2h_sword", 0)], itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_unbalanced|itp_merchandise, itc_m_heavy_greatsword|itcf_carry_sword_back,
     92500, weight(4.6) | difficulty(21) | spd_rtng(89) | weapon_length(130) | swing_damage(42, cut) | thrust_damage(26, pierce), imodbits_sword_high ],
    ["m_flamberge", "Flamberge", [("flamberge", 0)], itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_unbalanced|itp_merchandise, itc_m_heavy_greatsword|itcf_carry_sword_back,
     9100,  weight(5.2)  | difficulty(23) | spd_rtng(85) | weapon_length(139) | swing_damage(44, cut) | thrust_damage(22, pierce), imodbits_sword_high ],	
    ["gg_strange_great_sword", "Strange Heavy Great Sword", [("gg_strange_great_sword", 0)], itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_unbalanced|itp_merchandise, itc_m_heavy_greatsword|itcf_carry_sword_back,
     9000,  weight(5)  | difficulty(23) | spd_rtng(88) | weapon_length(120) | swing_damage(44, cut) | thrust_damage(24, pierce), imodbits_sword_high ],
    ["gg_gothic_flamberge","Gothic Flamberge", [("gg_gothic_flamberge", 0)], itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_unbalanced|itp_merchandise, itc_m_heavy_greatsword|itcf_carry_sword_back,	
     10000,  weight(5.4)  | difficulty(23) | spd_rtng(83) | weapon_length(152) | swing_damage(43, cut) | thrust_damage(22, pierce), imodbits_sword_high ],	


    # Strange 2h swords

    ["gg_estoc","Estoc", [("gg_estoc", 0)], itp_type_two_handed_wpn|itp_primary|itp_merchandise, itc_bastardsword|itcf_carry_sword_left_hip,
     5600,  weight(2.0)  | difficulty(15) | spd_rtng(99) | weapon_length(95)  | swing_damage(26, cut) | thrust_damage(31, pierce), imodbits_sword ],
    ["m_strange_great_sword", "Strange Sword", [("eastern_katana_new",0), ("eastern_katana_new_sheath", ixmesh_carry)], itp_type_two_handed_wpn|itp_primary|itp_merchandise, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
     80000, weight(1.5)  | difficulty(13) | spd_rtng(99) | weapon_length(115) | swing_damage(35, cut) | thrust_damage(23, pierce), imodbits_sword_high ],
    ["gg_executioner_sword", "Heavy Great Outlander Sword", [("executioner", 0)], itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_unbalanced|itp_merchandise, itc_m_heavy_greatsword|itcf_carry_sword_back,
     120000,  weight(5.8)  | difficulty(23) | spd_rtng(86) | weapon_length(118) | swing_damage(46, cut) | thrust_damage(24, blunt), imodbits_sword_high ],


    # 2h axes

    ["m_two_handed_axe", "Two Handed Axe", [("two_handed_battle_axe_a", 0)], itp_type_two_handed_wpn| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced|itp_merchandise, itc_nodachi|itcf_carry_axe_back,
     1300,  weight(2.5) | difficulty(10) | spd_rtng(98) | weapon_length(90)  | swing_damage(34, cut) | thrust_damage(0, pierce), imodbits_axe ], 
    ["m_shortened_voulge", "Shortened Voulge", [("two_handed_battle_axe_c", 0)], itp_type_two_handed_wpn| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced|itp_merchandise, itc_nodachi|itcf_carry_axe_back,
     1700,  weight(2.75)| difficulty(11) | spd_rtng(96) | weapon_length(100) | swing_damage(36, cut) | thrust_damage(0, pierce), imodbits_axe ], 
    ["m_two_handed_battle_axe_2", "Heavy Two Handed Axe", [("two_handed_battle_axe_b", 0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced|itp_merchandise, itc_nodachi|itcf_carry_axe_back,
     2000, weight(3.0) | difficulty(13) | spd_rtng(96) | weapon_length(92)  | swing_damage(41, cut) | thrust_damage(0, pierce), imodbits_axe ], 

    ["m_great_axe", "Great Axe", [("two_handed_battle_axe_e", 0)], itp_type_two_handed_wpn| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced|itp_merchandise, itc_nodachi|itcf_carry_axe_back,
     3400, weight(3.4) | difficulty(15) | spd_rtng(94) | weapon_length(92)  | swing_damage(43, cut) | thrust_damage(0, pierce), imodbits_axe ], 

    ["m_bearded_axe", "Bearded Axe", [("mackie_bearded_axe", 0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced|itp_merchandise, itc_nodachi|itcf_carry_axe_back,
     4300, weight(3)| difficulty(15) | spd_rtng(96) | weapon_length(95)  | swing_damage(42, cut) | thrust_damage(0, pierce), imodbits_axe ],
    ["m_bardiche", "Bardiche", [("two_handed_battle_axe_d", 0)], itp_type_two_handed_wpn|itp_cant_use_on_horseback| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced|itp_merchandise, itc_nodachi|itcf_carry_axe_back,     
     4500, weight(3.5)| difficulty(16) | spd_rtng(92) | weapon_length(102) | swing_damage(43, cut) | thrust_damage(0, pierce), imodbits_axe ],

    ["m_great_bardiche", "Great Bardiche", [("two_handed_battle_axe_f", 0)], itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced|itp_merchandise, itc_nodachi|itcf_carry_axe_back,                
    5600, weight(3.8)| difficulty(17) | spd_rtng(89) | weapon_length(116) | swing_damage(45, cut) | thrust_damage(0, pierce), imodbits_axe ], 

    ["m_sarranid_two_handed_axe_b", "Long Iron Axe", [("two_handed_battle_axe_h", 0)], itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_unbalanced|itp_merchandise, itc_nodachi|itcf_carry_axe_back,
     6100, weight(4.0) | difficulty(17) | spd_rtng(92) | weapon_length(90)  | swing_damage(45, cut) | thrust_damage(0, pierce), imodbits_axe ],
    ["m_sarranid_two_handed_axe_a", "Long Broad Bladed Iron Axe", [("two_handed_battle_axe_g", 0)], itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_unbalanced|itp_merchandise, itc_nodachi|itcf_carry_axe_back,
     6900, weight(4.2) | difficulty(18) | spd_rtng(90) | weapon_length(94)  | swing_damage(47, cut) | thrust_damage(0, pierce), imodbits_axe ],

     ["gg_outlanders_heavy_bastard_axe", "Outlanders Bastard Axe", [("gg_outlanders_heavy_bastard_axe", 0)], itp_type_two_handed_wpn| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced|itp_merchandise, itc_bastardsword|itcf_carry_axe_back,
      0,  weight(3) | difficulty(17) | spd_rtng(85) | weapon_length(88)  | swing_damage(41, cut) | thrust_damage(0, pierce), imodbits_axe ], 

    ["gg_outlanders_two_handed_bardiche", "Outlander Two Handed Bardiche", [("gg_outlanders_two_handed_bardiche", 0)], itp_type_two_handed_wpn|itp_cant_use_on_horseback| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced|itp_merchandise, itc_nodachi|itcf_carry_axe_back,
     5200, weight(3.6)| difficulty(16) | spd_rtng(89) | weapon_length(101) | swing_damage(46, cut) | thrust_damage(0, pierce), imodbits_axe ],
    ["gg_outlanders_heavy_battle_axe", "Outlander Two Handed Axe", [("gg_outlanders_heavy_battle_axe", 0)], itp_type_two_handed_wpn|itp_cant_use_on_horseback| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced|itp_merchandise, itc_nodachi|itcf_carry_axe_back,
     4000, weight(3.5)| difficulty(16) | spd_rtng(93) | weapon_length(90) | swing_damage(44, cut) | thrust_damage(0, pierce), imodbits_axe ],
    ["gg_outlanders_battlaxe", "Outlanders Battle Axe", [("gg_outlanders_battlaxe", 0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced|itp_merchandise, itc_nodachi|itcf_carry_axe_back,
     3100, weight(3.2) | difficulty(13) | spd_rtng(95) | weapon_length(94)  | swing_damage(42, cut) | thrust_damage(0, pierce), imodbits_axe ], 
    ["gg_celtic_axe", "Celtic Axe", [("gg_celtic_axe", 0)], itp_type_two_handed_wpn| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced|itp_merchandise, itc_nodachi|itcf_carry_axe_back,
     7500, weight(3.0) | difficulty(21) | spd_rtng(93) | weapon_length(100)  | swing_damage(44, cut) | thrust_damage(0, pierce), imodbits_axe ], 
  


    # 2h maces

    ["m_spiked_staff", "Spiked Staff", [("mace_e",0)],  itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_can_knock_down|itp_primary|itp_wooden_parry|itp_merchandise, itc_bastardsword|itcf_carry_axe_back,                                                                    
    800,  weight(2.0) | difficulty(12) | spd_rtng(97) | weapon_length(117)| swing_damage(24, blunt) | thrust_damage(26, pierce),imodbits_mace ],
    ["m_large_club", "Large Club", [("faradon_largeclub", 0)], itp_type_two_handed_wpn|itp_can_knock_down|itp_two_handed|itp_primary|itp_wooden_parry|itp_wooden_attack|itp_merchandise, itc_bastardsword|itcf_carry_axe_back,
     0, weight(2.25)| difficulty(14) | spd_rtng(98) | weapon_length(92) | swing_damage(28, blunt) | thrust_damage(17, blunt), imodbits_mace ],
    ["m_sarranid_two_handed_mace_1", "Long Iron Mace", [("mace_long_d", 0)], itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_can_knock_down|itp_two_handed|itp_primary|itp_crush_through|itp_unbalanced|itp_merchandise, itc_m_2h_mace|itcf_carry_axe_back,                   
    7400, weight(5.2) | difficulty(18) | spd_rtng(92) | weapon_length(95) | swing_damage(31, blunt) | thrust_damage(22, blunt), imodbits_mace ],
    ["m_bar_mace", "Bar Mace", [("faradon_ironclub", 0)], itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_can_knock_down|itp_two_handed|itp_primary|itp_crush_through|itp_unbalanced|itp_merchandise, itc_m_2h_mace|itcf_carry_axe_back,                                      
    7700, weight(5.0) | difficulty(18) | spd_rtng(91) | weapon_length(96) | swing_damage(32, blunt) | thrust_damage(22, blunt), imodbits_mace ],
    ["m_morningstar", "Morningstar", [("mace_morningstar_new", 0)], itp_crush_through|itp_type_two_handed_wpn|itp_primary|itp_wooden_parry|itp_unbalanced|itp_merchandise, itc_morningstar|itcf_carry_axe_left_hip,
     7000, weight(4.6)| difficulty(18) | spd_rtng(94) | weapon_length(85) | swing_damage(34, pierce)| thrust_damage(0, pierce), imodbits_mace ], 
    ["m_maul", "Maul", [("maul_b", 0)], itp_crush_through|itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_can_knock_down |itp_primary|itp_two_handed|itp_wooden_parry|itp_wooden_attack|itp_unbalanced|itp_merchandise, itc_nodachi|itcf_carry_spear,
     3000, weight(7.0) | difficulty(18) | spd_rtng(79) | weapon_length(70) | swing_damage(36, blunt) | thrust_damage(0, pierce), imodbits_mace ],

    ["m_sledgehammer", "Sledgehammer", [("maul_c", 0)], itp_crush_through|itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_can_knock_down|itp_primary|itp_two_handed|itp_wooden_parry|itp_wooden_attack|itp_unbalanced|itp_merchandise, itc_nodachi|itcf_carry_spear,          
    2500, weight(7.5) | difficulty(21) | spd_rtng(76) | weapon_length(72) | swing_damage(39, blunt) | thrust_damage(0, pierce), imodbits_mace ],
    ["m_warhammer", "Great Hammer", [("maul_d", 0)], itp_crush_through|itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_can_knock_down|itp_primary|itp_two_handed|itp_wooden_parry|itp_wooden_attack|itp_unbalanced|itp_merchandise, itc_nodachi|itcf_carry_spear,             
    5300, weight(8.5) | difficulty(24) | spd_rtng(73) | weapon_length(68) | swing_damage(42, blunt) | thrust_damage(0, pierce), imodbits_mace ],

    ["gg_two_handed_long_warhammer", "Two Handed Long Warhammer", [("gg_two_handed_long_warhammer", 0)], itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_unbalanced|itp_merchandise, itc_m_heavy_greatsword|itcf_carry_sword_back,
     6400, weight(3.2)| difficulty(21) | spd_rtng(91) | weapon_length(107) | swing_damage(34, blunt) | thrust_damage(26, pierce), imodbits_mace ],	


    # POLEARMS itc_bastardsword
	
    # Staffs
    ["m_iron_staff", "Iron Staff", [("iron_staff", 0)], itp_type_polearm|itp_cant_use_on_horseback|itp_offset_lance|itp_primary|itp_penalty_with_shield|itp_can_knock_down|itp_merchandise,itc_staff|itcf_carry_sword_back,                                         
    950,  weight(2.75)| difficulty(13)| spd_rtng(95) | weapon_length(128) | swing_damage(27, blunt) | thrust_damage(25, blunt), imodbits_polearm ],
    
    # Hafted blades

    ["m_military_scythe_c", "Blunt-Pointed Scythe", [("spear_c_2-5m", 0)], itp_type_polearm|itp_offset_lance|itp_primary|itp_wooden_parry|itp_merchandise, itc_staff|itcf_carry_spear,                                                                              
    2850, weight(2.25)| difficulty(13) | spd_rtng(92) | weapon_length(155) | swing_damage(35, cut) | thrust_damage(20, pierce), imodbits_polearm ], 
    ["m_military_scythe", "Scythe", [("spear_e_2-5m", 0)], itp_type_polearm|itp_offset_lance|itp_primary|itp_wooden_parry|itp_merchandise, itc_staff|itcf_carry_spear,                                                                                              
    3150, weight(2.25)| difficulty(13) | spd_rtng(91) | weapon_length(155) | swing_damage(35, cut) | thrust_damage(24, pierce), imodbits_polearm ], 
    ["m_hafted_blade_b", "Hafted Blade", [("khergit_pike_b", 0)], itp_type_polearm|itp_cant_use_on_horseback|itp_primary|itp_two_handed|itp_wooden_parry|itp_merchandise, itcf_carry_spear|itc_guandao,                                                             
    3900, weight(1.75)| difficulty(13) | spd_rtng(96) | weapon_length(132) | swing_damage(36, cut) | thrust_damage(19, pierce), imodbits_polearm ], 
    ["m_hafted_blade_a", "Long Hafted Blade", [("khergit_pike_a", 0)], itp_type_polearm|itp_cant_use_on_horseback|itp_primary|itp_two_handed|itp_wooden_parry|itp_merchandise, itcf_carry_spear|itc_guandao,                                                        
    4100, weight(2.25)| difficulty(14) | spd_rtng(92) | weapon_length(153) | swing_damage(37, cut) | thrust_damage(20, pierce), imodbits_polearm ],
    ["m_glaive", "Long Glaive", [("glaive_b", 0)], itp_type_polearm|itp_cant_use_on_horseback|itp_offset_lance|itp_primary|itp_two_handed|itp_wooden_parry|itp_merchandise, itc_staff|itcf_carry_spear,                                                             
    4250, weight(2.5) | difficulty(15) | spd_rtng(90) | weapon_length(160) | swing_damage(37, cut) | thrust_damage(23, pierce), imodbits_polearm ],	
   # ["m_glaive_guisarme_1", "Glaive", [("glaive_guisarme_1", 0)], itp_type_polearm|itp_cant_use_on_horseback|itp_offset_lance|itp_primary|itp_two_handed|itp_wooden_parry|itp_merchandise, itc_staff|itcf_carry_spear,
    # 3270, weight(2.5) | difficulty(15) | spd_rtng(90) | weapon_length(160) | swing_damage(36, cut) | thrust_damage(22, pierce), imodbits_polearm ],	

    ["m_bill", "Bill", [("15_english_bill", 0)], itp_type_polearm|itp_cant_use_on_horseback|itp_primary|itp_penalty_with_shield|itp_two_handed|itp_wooden_parry|itp_merchandise, itc_cutting_spear,
     4700, weight(2.5) | difficulty(16) | spd_rtng(88) | weapon_length(184) | swing_damage(29, cut) | thrust_damage(27, pierce), imodbits_polearm ],

    ["gg_ranseur","Ranseur", [("gg_ranseur", 0)], itp_type_polearm|itp_cant_use_on_horseback|itp_primary|itp_two_handed|itp_wooden_parry|itp_merchandise, itc_cutting_spear,
     4700, weight(2.5) | difficulty(17) | spd_rtng(83) | weapon_length(214) | swing_damage(25, cut) | thrust_damage(26, pierce), imodbits_polearm ],

    ["m_glaive_15_2", "Cross Spear", [("glaive2", 0)], itp_type_polearm|itp_offset_lance|itp_primary|itp_wooden_parry|itp_merchandise, itc_staff|itcf_carry_spear,                                                                                                  
    4900, weight(1.75)| difficulty(12) | spd_rtng(95) | weapon_length(157) | swing_damage(28, cut) | thrust_damage(29, pierce), imodbits_polearm ], 
    ["m_swordstaff", "Swordstaff", [("cp_swordstaff", 0)], itp_type_polearm|itp_offset_lance|itp_primary|itp_wooden_parry|itp_merchandise, itc_staff|itcf_carry_spear,                                                                                              
    5200, weight(1.75)| difficulty(13) | spd_rtng(94) | weapon_length(162) | swing_damage(28, cut) | thrust_damage(29, pierce), imodbits_polearm ],

    # Spears

    ["m_pitchfork", "Pitchfork", [("swup_trident", 0)], itp_type_polearm|itp_offset_lance|itp_primary|itp_wooden_parry|itp_merchandise, itc_staff|itcf_carry_spear,                                                                                                 
    240,  weight(1.25)| difficulty(0)  | spd_rtng(95) | weapon_length(150) | swing_damage(18, blunt) | thrust_damage(26, pierce), imodbits_polearm ], 
    ["m_shortened_spear", "Shortened Spear", [("spear_g_1-9m",0)], itp_type_polearm|itp_offset_lance|itp_primary|itp_wooden_parry|itp_merchandise, itc_staff|itcf_carry_spear,                                                                                      
    340,  weight(1.25)| difficulty(0)  | spd_rtng(99) | weapon_length(120) | swing_damage(19, blunt) | thrust_damage(29, pierce), imodbits_polearm ],
    ["m_spear", "Spear", [("spear_h_2-15m", 0)], itp_type_polearm|itp_offset_lance|itp_primary|itp_wooden_parry|itp_merchandise, itc_staff|itcf_carry_spear,                                                                                                        
    1500,  weight(1.5) | difficulty(0)  | spd_rtng(97) | weapon_length(135) | swing_damage(20, blunt) | thrust_damage(30, pierce), imodbits_polearm ],
    ["m_bamboo_spear_short", "Bamboo Spear", [("m_bamboo_spear_190", 0)], itp_type_polearm|itp_cant_use_on_horseback|itp_offset_lance|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_merchandise, itc_cutting_spear,
     1800, weight(1.5) | difficulty(11) | spd_rtng(89) | weapon_length(190) | swing_damage(17, blunt) | thrust_damage(27, pierce), imodbits_polearm ],
    ["m_war_spear", "Heavy Spear", [("spear_i_2-3m", 0)], itp_type_polearm|itp_offset_lance|itp_primary|itp_wooden_parry|itp_merchandise, itc_staff|itcf_carry_spear,
     1950, weight(1.8) | difficulty(11) | spd_rtng(94) | weapon_length(150) | swing_damage(20, blunt) | thrust_damage(32, pierce), imodbits_polearm ], 
    ["gg_ashwood_pike","Ashwood Pike", [("gg_ashwood_pike", 0)], itp_type_polearm|itp_cant_use_on_horseback|itp_offset_lance|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_merchandise, itc_cutting_spear,
      5400, weight(2) | difficulty(15) | spd_rtng(93) | weapon_length(166) | swing_damage(21, blunt) | thrust_damage(29, pierce), imodbits_polearm ],

    # ["m_melitine_lance2", "Bloody Spear", [("melitine_lance2", 0)], itp_type_polearm|itp_offset_lance|itp_primary|itp_wooden_parry|itp_merchandise, itc_staff|itcf_carry_spear,                                                                                     1700, weight(1.5) | difficulty(11) | spd_rtng(95) | weapon_length(150) | swing_damage(19, blunt) | thrust_damage(31, pierce), imodbits_polearm ], #user Den4ik

    ["m_long_spear", "Long Spear", [("m_long_spear", 0)], itp_type_polearm|itp_cant_use_on_horseback|itp_offset_lance|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_merchandise, itc_spear,
     2730, weight(2.0) | difficulty(12) | spd_rtng(85) | weapon_length(200) | swing_damage(0, blunt)  | thrust_damage(27, pierce), imodbits_polearm ], 
     ["gg_outlander_long_spear", "Outlander Long Spear", [("gg_outlander_long_spear", 0)], itp_type_polearm|itp_cant_use_on_horseback|itp_offset_lance|itp_primary|itp_two_handed|itp_wooden_parry|itp_merchandise, itc_spear,
      5500, weight(2.5) | difficulty(16) | spd_rtng(82) | weapon_length(214) | swing_damage(0, blunt)  | thrust_damage(27, pierce), imodbits_polearm ], 




    ["m_pike", "Pike", [("spear_a_3m",0)], itp_type_polearm|itp_no_parry|itp_cant_use_on_horseback|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_two_handed|itp_merchandise, itcf_thrust_polearm,
     3030, weight(2.3)| difficulty(18) | spd_rtng(80) | weapon_length(245) | swing_damage(0, blunt)  | thrust_damage(25, pierce), imodbits_polearm ],
    # ["gg_giant_pike","Giant Pike", [("gg_giant_pike", 0)], itp_type_polearm|itp_no_parry|itp_cant_use_on_horseback|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_two_handed|itp_merchandise, itcf_thrust_polearm,
     # 9000, weight(3)| difficulty(18) | spd_rtng(75) | weapon_length(300) | swing_damage(0, blunt)  | thrust_damage(23, pierce), imodbits_polearm ],

    ["m_awlpike", "Awlpike", [("awl_pike_b", 0)], itp_type_polearm|itp_cant_use_on_horseback|itp_offset_lance|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_merchandise, itc_cutting_spear|itcf_carry_spear,
     5100, weight(1.75)| difficulty(16) | spd_rtng(90) | weapon_length(165) | swing_damage(20, blunt) | thrust_damage(31, pierce), imodbits_polearm ], 

    # ["m_Roman_Late_Spear", "Roman Late Spear", [("Roman_Late_Spear", 0)], itp_type_polearm|itp_cant_use_on_horseback|itp_offset_lance|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_merchandise, itc_cutting_spear|itcf_carry_spear,                     4150, weight(1.75)| difficulty(14) | spd_rtng(91) | weapon_length(165) | swing_damage(20, blunt) | thrust_damage(32, pierce), imodbits_polearm ], #clan RP

    ["m_awlpike_long", "Long Awlpike", [("awl_pike_a", 0)], itp_type_polearm|itp_cant_use_on_horseback|itp_offset_lance|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_merchandise, itc_cutting_spear|itcf_carry_spear,
     5450, weight(2.0) | difficulty(19) | spd_rtng(86) | weapon_length(185) | swing_damage(20, blunt) | thrust_damage(29, pierce), imodbits_polearm ], 
    # ["m_partyzana_a", "Protazan", [("partyzana_a", 0)], itp_type_polearm|itp_cant_use_on_horseback|itp_offset_lance|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_merchandise, itc_cutting_spear|itcf_carry_spear,                                       4500, weight(2.0) | difficulty(16) | spd_rtng(88) | weapon_length(185) | swing_damage(20, blunt) | thrust_damage(31, pierce), imodbits_polearm ], #clan Strelec
    # ["m_pike_long", "Long Pike", [("pike_long",0)], itp_type_polearm|itp_no_parry|itp_cant_use_on_horseback|itp_primary|itp_unbalanced|itp_penalty_with_shield|itp_wooden_parry|itp_two_handed|itp_merchandise, itcf_thrust_polearm,                                7000, weight(2.5) | difficulty(16) | spd_rtng(79) | weapon_length(300) | swing_damage(0, blunt)  | thrust_damage(25, pierce), imodbits_polearm ],
	
    # Lances

    ["m_light_lance", "Light Lance", [("spear_b_2-75m", 0)], itp_type_polearm|itp_offset_lance|itp_primary|itp_couchable|itp_penalty_with_shield|itp_wooden_parry|itp_merchandise, itc_cutting_spear,
     6000, weight(2.0) | difficulty(9)  | spd_rtng(85) | weapon_length(175) | swing_damage(17, blunt) | thrust_damage(28, pierce), imodbits_polearm ], 
    ["m_lance", "Lance", [("spear_d_2-8m", 0)], itp_type_polearm|itp_offset_lance|itp_primary|itp_couchable|itp_penalty_with_shield|itp_wooden_parry|itp_merchandise, itc_cutting_spear,
     6550, weight(2.10) | difficulty(14) | spd_rtng(81) | weapon_length(180) | swing_damage(17, blunt) | thrust_damage(27, pierce), imodbits_polearm ], 
    ["m_heavy_lance", "Heavy Lance", [("spear_f_2-9m", 0)], itp_type_polearm|itp_offset_lance|itp_primary|itp_couchable|itp_penalty_with_shield|itp_wooden_parry|itp_merchandise, itc_cutting_spear,
     6700, weight(2.25)| difficulty(18) | spd_rtng(77) | weapon_length(190) | swing_damage(17, blunt) | thrust_damage(25, pierce), imodbits_polearm ], 
    ["warlords_great_lance_1", "Great Lance", [("warlords_great_lance_1_mesh", 0)], itp_couchable|itp_type_polearm|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_merchandise, 0,
    8340,weight(3.75)|difficulty(20)|spd_rtng(58)|weapon_length(230)|swing_damage(0,blunt)|thrust_damage(24,pierce),imodbits_polearm, ],

    # Polearms: axes

    ["m_long_axe", "Long Axe", [("long_axe_a", 0)], itp_type_polearm|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced|itp_next_item_as_melee|itp_merchandise, itc_staff|itcf_carry_axe_back,           
    2800,  weight(3.0) | difficulty(13) | spd_rtng(93) | weapon_length(120) | swing_damage(37, cut) | thrust_damage(18, blunt), imodbits_axe ], 
    ["m_long_axe_alt", "Long Axe", [("long_axe_a", 0)], itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced, itc_nodachi|itcf_carry_axe_back,                                     
    2800,  weight(3.0) | difficulty(13) | spd_rtng(87) | weapon_length(120) | swing_damage(37, cut) | thrust_damage(0, blunt), imodbits_axe ], 
    ["m_long_axe_b", "Heavy Long Axe", [("long_axe_b", 0)], itp_type_polearm|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced|itp_next_item_as_melee|itp_merchandise, itc_staff|itcf_carry_axe_back,
    4300, weight(3.25)| difficulty(14) | spd_rtng(92) | weapon_length(125) | swing_damage(41, cut) | thrust_damage(18, blunt), imodbits_axe ], 
    ["m_long_axe_b_alt", "Heavy Long Axe", [("long_axe_b", 0)], itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced, itc_nodachi|itcf_carry_axe_back,
    4300, weight(3.25)| difficulty(14) | spd_rtng(86) | weapon_length(125) | swing_damage(41, cut) | thrust_damage(0, blunt), imodbits_axe ],
    ["m_long_axe_c", "Great Long Axe", [("long_axe_c", 0)], itp_type_polearm|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced|itp_next_item_as_melee|itp_merchandise, itc_staff|itcf_carry_axe_back,   
    5050, weight(3.5) | difficulty(15) | spd_rtng(90) | weapon_length(130) | swing_damage(43, cut) | thrust_damage(19, blunt), imodbits_axe ], 
    ["m_long_axe_c_alt", "Great Long Axe", [("long_axe_c", 0)], itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced, itc_nodachi|itcf_carry_axe_back,                             
    5050, weight(3.5) | difficulty(15) | spd_rtng(84) | weapon_length(130) | swing_damage(43, cut) | thrust_damage(0, blunt), imodbits_axe ], 
    ["m_long_axe_dane","Long Axe with Wide Blade", [("bwg_dane_axe", 0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_cant_use_on_horseback|itp_unbalanced, itc_staff|itcf_carry_axe_back,            
    5200, weight(3.75)| difficulty(15) | spd_rtng(89) | weapon_length(135) | swing_damage(43, cut) | thrust_damage(18, blunt), imodbits_axe ],
#    ["m_bardiche_3", "Bardiche", [("bardiche_3", 0)], itp_type_polearm|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced|itp_next_item_as_melee|itp_merchandise, itc_staff|itcf_carry_axe_back,
#     71500,weight(3.5) | difficulty(15) | spd_rtng(90) | weapon_length(130) | swing_damage(43, cut) | thrust_damage(19, blunt), imodbits_axe ], 
 #   ["m_bardiche_3_alt", "Bardiche", [("bardiche_3", 0)], itp_type_two_handed_wpn|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced, itc_nodachi|itcf_carry_axe_back,
  #   71500,weight(3.5) | difficulty(15) | spd_rtng(84) | weapon_length(130) | swing_damage(43, cut) | thrust_damage(0, blunt), imodbits_axe ],
	
    # Poleaxes

    ["m_voulge", "Voulge", [("two_handed_battle_long_axe_a", 0)], itp_type_polearm|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_merchandise, itc_staff|itcf_carry_axe_back,                                                                  
    2400, weight(3.5) | difficulty(18) | spd_rtng(87) | weapon_length(170) | swing_damage(35, cut) | thrust_damage(16, pierce), imodbits_axe ],
    ["m_long_bardiche", "Long Bardiche", [("m_two_handed_battle_long_axe_b", 0)], itp_type_polearm|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced|itp_merchandise, itc_staff|itcf_carry_axe_back,                                   
    5000, weight(3.5) | difficulty(16) | spd_rtng(88) | weapon_length(141) | swing_damage(44, cut) | thrust_damage(20, pierce), imodbits_axe ], 
    ["m_great_long_bardiche", "Great Long Bardiche", [("m_two_handed_battle_long_axe_c", 0)], itp_type_polearm|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced|itp_merchandise, itc_staff|itcf_carry_axe_back,                       
    5900, weight(3.5) | difficulty(17) | spd_rtng(85) | weapon_length(154) | swing_damage(45, cut) | thrust_damage(20, pierce), imodbits_axe ], 
#    ["m_luc_flemish_halberd", "Great Poleaxe", [("luc_flemish_halberd", 0)], itp_type_polearm|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced|itp_merchandise, itc_staff|itcf_carry_spear,
  #  90000,weight(3.5) | difficulty(17) | spd_rtng(85) | weapon_length(154) | swing_damage(45, cut) | thrust_damage(20, pierce), imodbits_axe ],  	
    ["m_german_poleaxe", "Long Poleaxe", [("15_german_poleaxe", 0), ("15_german_poleaxe_carry", ixmesh_carry)], itp_type_polearm|itp_cant_use_on_horseback|itp_primary|itp_wooden_parry|itp_unbalanced|itp_two_handed|itp_bonus_against_shield|itp_merchandise, itc_staff|itcf_carry_spear,
     7300, weight(3.7) | difficulty(21) | spd_rtng(88) | weapon_length(145) | swing_damage(44, cut) | thrust_damage(26, pierce), imodbits_polearm ],
    # ["m_voulge_1", "Heavy Voulge", [("voulge_1", 0)], itp_type_polearm|itp_cant_use_on_horseback|itp_primary|itp_wooden_parry|itp_unbalanced|itp_two_handed|itp_bonus_against_shield|itp_merchandise, itc_staff|itcf_carry_spear,
#    5800, weight(3.75)| difficulty(17) | spd_rtng(86) | weapon_length(145) | swing_damage(43, cut) | thrust_damage(27, pierce), imodbits_polearm ],
#    ["m_poleaxe_no3", "Schwerter's Poleaxe", [("poleaxe_no3", 0)], itp_type_polearm|itp_cant_use_on_horseback|itp_primary|itp_wooden_parry|itp_unbalanced|itp_two_handed|itp_bonus_against_shield|itp_merchandise, itc_staff|itcf_carry_spear,
 #    5900, weight(3.75)| difficulty(17) | spd_rtng(86) | weapon_length(145) | swing_damage(43, cut) | thrust_damage(27, pierce), imodbits_polearm ], #clan XIV

    ["m_elegant_poleaxe", "Elegant Poleaxe", [("15_elegant_poleaxe", 0), ("15_elegant_poleaxe_carry", ixmesh_carry)], itp_type_polearm|itp_cant_use_on_horseback|itp_primary|itp_wooden_parry|itp_two_handed|itp_bonus_against_shield|itp_merchandise, itc_staff|itcf_carry_spear,
     7000, weight(3.25)| difficulty(18) | spd_rtng(91) | weapon_length(135) | swing_damage(42, cut) | thrust_damage(26, pierce), imodbits_polearm ], 
    ["m_bec_de_corbin_a", "Bec de Corbin", [("bec_de_corbin_a", 0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_two_handed|itp_primary|itp_cant_use_on_horseback, itcf_carry_spear|itc_poleaxe|itcf_thrust_onehanded_lance|itcf_thrust_onehanded_lance_horseback,
     6450, weight(2.7)|difficulty(18)|spd_rtng(93)|weapon_length(120)|swing_damage(33, pierce)|thrust_damage(27, pierce),imodbits_polearm    ],
    ["gg_outlanders_bec_the_corbin", "Outlanders Bec de Corbin", [("gg_outlanders_bec_the_corbin", 0)],     itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_two_handed|itp_primary|itp_cant_use_on_horseback, itcf_carry_spear|itc_poleaxe|itcf_thrust_onehanded_lance|itcf_thrust_onehanded_lance_horseback,
     6720, weight(2.7)|difficulty(18)|spd_rtng(90)|weapon_length(163)|swing_damage(28, pierce)|thrust_damage(25, pierce),imodbits_polearm    ],

    ["gg_long_morningstar", "Long Morningstar", [("gg_long_morningstar", 0)],     itp_type_polearm|itp_merchandise|itp_unbalanced|itp_wooden_parry|itp_two_handed|itp_primary|itp_cant_use_on_horseback, itcf_carry_spear|itc_poleaxe|itcf_thrust_onehanded_lance|itcf_thrust_onehanded_lance_horseback,
     0, weight(3)|difficulty(18)|spd_rtng(88)|weapon_length(132)|swing_damage(29, pierce)|thrust_damage(24, pierce),imodbits_polearm    ],

    ["gg_outlanders_long_morningstar", "Outlanders Long Morningstar", [("gg_outlanders_long_morningstar", 0)],     itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_two_handed|itp_primary|itp_cant_use_on_horseback, itcf_carry_spear|itc_poleaxe|itcf_thrust_onehanded_lance|itcf_thrust_onehanded_lance_horseback,
     4650, weight(3.1)|difficulty(18)|spd_rtng(93)|weapon_length(134)|swing_damage(31, pierce)|thrust_damage(24, pierce),imodbits_polearm    ],
    ["gg_great_long_poleaxe", "Heavy Long Poleaxe", [("gg_great_long_poleaxe", 0), ("gg_great_long_poleaxe_carry", ixmesh_carry)], itp_type_polearm|itp_unbalanced|itp_cant_use_on_horseback|itp_primary|itp_wooden_parry|itp_two_handed|itp_bonus_against_shield|itp_merchandise, itc_staff|itcf_carry_spear,
     7500, weight(4.0)| difficulty(21) | spd_rtng(86) | weapon_length(141) | swing_damage(46, cut) | thrust_damage(26, pierce), imodbits_polearm ], 
    ["gg_elder_poleaxe", "Elder Poleaxe", [("gg_elder_poleaxe", 0), ("gg_elder_poleaxe_carry", ixmesh_carry)], itp_type_polearm|itp_unbalanced|itp_cant_use_on_horseback|itp_primary|itp_wooden_parry|itp_two_handed|itp_bonus_against_shield|itp_merchandise, itc_staff|itcf_carry_spear,
     7200, weight(3.5)| difficulty(18) | spd_rtng(89) | weapon_length(144) | swing_damage(42, cut) | thrust_damage(27, pierce), imodbits_polearm ], 
  


	# Polearms: blunt

    ["m_long_spiked_club", "Long Spiked Club", [("mace_long_c", 0)], itp_type_polearm|itp_cant_use_on_horseback|itp_can_knock_down|itp_primary|itp_wooden_parry|itp_merchandise, itc_staff|itcf_carry_axe_back,
     200,  weight(2.0) | difficulty(10) | spd_rtng(96) | weapon_length(126) | swing_damage(23, pierce) | thrust_damage(20, blunt), imodbits_mace ], 
    ["m_long_hafted_knobbed_mace", "Long Hafted Knobbed Mace", [("mace_long_a", 0)], itp_type_polearm|itp_cant_use_on_horseback|itp_can_knock_down|itp_primary|itp_wooden_parry|itp_merchandise, itc_staff|itcf_carry_axe_back,
     3710, weight(2.5) | difficulty(14) | spd_rtng(94) | weapon_length(133) | swing_damage(28, blunt)  | thrust_damage(22, blunt), imodbits_mace ], 
    ["m_long_hafted_spiked_mace", "Long Hafted Spiked Mace", [("mace_long_b", 0)], itp_type_polearm|itp_cant_use_on_horseback|itp_can_knock_down|itp_primary|itp_wooden_parry|itp_merchandise, itc_staff|itcf_carry_axe_back,
     4750, weight(2.75)| difficulty(14) | spd_rtng(92) | weapon_length(138) | swing_damage(29, blunt)  | thrust_damage(23, blunt), imodbits_mace ],
    # ["m_luc_lucerne_hammer", "Spiked Hammer", [("luc_lucerne_hammer", 0)], itp_type_polearm|itp_cant_use_on_horseback|itp_can_knock_down|itp_primary|itp_wooden_parry|itp_merchandise, itc_staff|itcf_carry_axe_back,                                               3850, weight(2.75)| difficulty(14) | spd_rtng(92) | weapon_length(138) | swing_damage(29, blunt)  | thrust_damage(23, pierce), imodbits_mace ], #clan XIV	
    #
    # BU ITEMI KOYMAYIN AMK
    # ["m_luc_polehammer_du_corbin", "German Polehammer", [("luc_polehammer_du_corbin", 0)], itp_type_polearm|itp_cant_use_on_horseback|itp_primary|itp_wooden_parry|itp_two_handed|itp_merchandise, itc_staff|itcf_carry_spear,                                      5450, weight(2.5) | difficulty(14) | spd_rtng(93) | weapon_length(120) | swing_damage(31, blunt)  | thrust_damage(27, pierce),imodbits_polearm ], #clan XIV	
    ["forged_longwarhammer", "Outlander Long Warhammer", [("forged_longwarhammer", 0), ("forged_longwarhammer_carry", ixmesh_carry)], itp_type_polearm|itp_cant_use_on_horseback|itp_can_knock_down|itp_primary|itp_wooden_parry|itp_unbalanced|itp_two_handed|itp_merchandise, itc_staff|itcf_carry_spear,
     100000,  weight(5.5) | difficulty(21) | spd_rtng(92) | weapon_length(130) | swing_damage(34, blunt) | thrust_damage(23, pierce), imodbits_polearm ],
    ["gg_outlanders_polehammer", "Outlanders Polehammer", [("gg_outlanders_polehammer", 0)],   itp_type_polearm|itp_unbalanced|itp_cant_use_on_horseback|itp_can_knock_down|itp_primary|itp_wooden_parry|itp_merchandise, itc_staff|itcf_carry_axe_back,
     6350, weight(5.5)|difficulty(21)|spd_rtng(92)|weapon_length(133)|swing_damage(33, blunt)|thrust_damage(18, blunt), imodbits_polearm ],
    ["gg_rare_heavy_long_maul", "Heavy Long Maul", [("gg_rare_long_maul", 0)],   itp_type_polearm|itp_cant_use_on_horseback|itp_unbalanced|itp_can_knock_down|itp_primary|itp_wooden_parry|itp_merchandise, itc_staff|itcf_carry_axe_back,
     90000, weight(6)|difficulty(23)|spd_rtng(77)|weapon_length(125)|swing_damage(42, blunt)|thrust_damage(25, blunt), imodbits_polearm ],

##    # Colored great lances
##
##    ["m_colored_great_lance_1", "Black Great Lance", [("btwk_lance_1",0)], itp_couchable|itp_type_polearm|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_merchandise, 0,   #### MAIN 
##     6040, weight(3.75) | difficulty(20) | spd_rtng(58) | weapon_length(230) | swing_damage(0, blunt)  | thrust_damage(32, pierce), imodbits_polearm ],
##    ["m_colored_great_lance_2", "Red Great Lance", [("btwk_lance_2",0)], itp_couchable|itp_type_polearm|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_merchandise, 0,   #### EXTRA
##     6040, weight(3.75) | difficulty(20) | spd_rtng(58) | weapon_length(230) | swing_damage(0, blunt)  | thrust_damage(32, pierce), imodbits_polearm ],
##    ["m_colored_great_lance_3", "Yellow Great Lance", [("btwk_lance_4",0)], itp_couchable|itp_type_polearm|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_merchandise, 0,   #### EXTRA
##     6040, weight(3.75) | difficulty(20) | spd_rtng(58) | weapon_length(230) | swing_damage(0, blunt)  | thrust_damage(32, pierce), imodbits_polearm ],
##    ["m_colored_great_lance_4", "Green Great Lance", [("btwk_lance_5",0)], itp_couchable|itp_type_polearm|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_merchandise, 0,   #### EXTRA
##     6040, weight(3.75) | difficulty(20) | spd_rtng(58) | weapon_length(230) | swing_damage(0, blunt)  | thrust_damage(32, pierce), imodbits_polearm ],
##    ["m_colored_great_lance_5", "Blue Great Lance", [("btwk_lance_6",0)], itp_couchable|itp_type_polearm|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_merchandise, 0,   #### EXTRA
##     6040, weight(3.75) | difficulty(20) | spd_rtng(58) | weapon_length(230) | swing_damage(0, blunt)  | thrust_damage(32, pierce), imodbits_polearm ],

#Cakebatter Heraldic start
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# Weapons
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#-------------------------------------------------------------------------------------------------
# Polearms Start
#-------------------------------------------------------------------------------------------------
["warlords_great_lance_1_heraldic_primary_color", "Heraldic Great Lance Primary Color", [("warlords_great_lance_1_heraldic_mesh",0)], itp_couchable|itp_type_polearm|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_merchandise, 0,
 8340,weight(3.75)|difficulty(20)|spd_rtng(58)|weapon_length(230)|swing_damage(0,blunt)|thrust_damage(24,pierce),imodbits_polearm,
  [(ti_on_init_item, [
    (store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_warlords_great_lance_1_heraldic_primary_color", ":agent_no", ":troop_no"),
  ])]
],#Above item is heraldic version of: m_colored_great_lance_1
["warlords_great_lance_1_heraldic_secondary_color", "Heraldic Great Lance Secondary Color", [("warlords_great_lance_1_heraldic_mesh",0)], itp_couchable|itp_type_polearm|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_merchandise, 0,
 8340,weight(3.75)|difficulty(20)|spd_rtng(58)|weapon_length(230)|swing_damage(0,blunt)|thrust_damage(24,pierce),imodbits_polearm,
  [(ti_on_init_item, [
    (store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_warlords_great_lance_1_heraldic_secondary_color", ":agent_no", ":troop_no"),
  ])]
],#Above item is heraldic version of: m_colored_great_lance_1
["warlords_great_lance_1_heraldic_double_color", "Heraldic Great Lance Both Colors", [("warlords_great_lance_1_heraldic_mesh",0)], itp_couchable|itp_type_polearm|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_merchandise, 0,
 8340,weight(3.75)|difficulty(20)|spd_rtng(58)|weapon_length(230)|swing_damage(0,blunt)|thrust_damage(24,pierce),imodbits_polearm,
  [(ti_on_init_item, [
    (store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_warlords_great_lance_1_heraldic_double_color", ":agent_no", ":troop_no"),
  ])]
],#Above item is heraldic version of: m_colored_great_lance_1
["warlords_great_lance_1_heraldic_double_color_inverted", "Heraldic Great Lance Both Colors Inverted", [("warlords_great_lance_1_heraldic_mesh",0)], itp_couchable|itp_type_polearm|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_merchandise, 0,
 8340,weight(3.75)|difficulty(20)|spd_rtng(58)|weapon_length(230)|swing_damage(0,blunt)|thrust_damage(24,pierce),imodbits_polearm,
  [(ti_on_init_item, [
    (store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_warlords_great_lance_1_heraldic_double_color_inverted", ":agent_no", ":troop_no"),
  ])]
],#Above item is heraldic version of: m_colored_great_lance_1
#Cakebatter Heraldic end


    # ["m_heavy_hussar_lance_rw", "Heavy Hussar Lance", [("heavy_hussar_lance_rw",0)], itp_couchable|itp_type_polearm|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_merchandise, 0,5100, weight(3.75) | difficulty(20) | spd_rtng(58) | weapon_length(230) | swing_damage(0, blunt)  | thrust_damage(32, pierce), imodbits_polearm ], #user Commander



	# SHIELDS                
	
 #elim ilen
    ["m_arena_shield_heraldic_1", "Shield", [("m_arena_shield_heraldic_1", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield,  250, weight(2.0) | hit_points(220) | body_armor(14) | spd_rtng(103) | difficulty(0) | shield_width(30) | shield_height(50), imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_m_arena_shield_heraldic_1", ":agent_no", ":troop_no")])]],

    # Small shields

    ["m_tab_shield_round_a","Weak Round Shield", [("tableau_shield_round_5", 0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_round_shield,                            60,   weight(2.5) | hit_points(215) | body_armor(5)  | spd_rtng(93)  | difficulty(0) | shield_width(44), imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_round_shield_5", ":agent_no", ":troop_no")])]], 
    ["m_hide_covered_round_shield", "Hide Covered Round Shield", [("m_shield_round_f",0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_round_shield,                   400,  weight(2.0) | hit_points(235) | body_armor(17) | spd_rtng(103) | difficulty(1) | shield_width(40), imodbits_shield ],
    ["m_shield_heater_c", "Small Shield", [("m_shield_heater_c", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield,                                         500,  weight(2.0) | hit_points(245) | body_armor(17) | spd_rtng(103) | difficulty(1) | shield_width(30) | shield_height(50), imodbits_shield ], 
    ["m_small_board_shield_1", "Light Cavalry Shield", [("btwk_shield_1", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield,                                700,  weight(2.0) | hit_points(255) | body_armor(16) | spd_rtng(105) | difficulty(1) | shield_width(28) | shield_height(54), imodbits_shield ], 
    ["m_tab_shield_small_round_a", "Small Round Shield", [("tableau_shield_small_round_3", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_round_shield,              900,  weight(2.0) | hit_points(225) | body_armor(18) | spd_rtng(105) | difficulty(1) | shield_width(40), imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_small_round_shield_3", ":agent_no", ":troop_no")])]], 
    ["m_small_board_shield_2", "Small Board Shield", [("btwk_shield_1_big", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield,                              1250, weight(3.0) | hit_points(285) | body_armor(18) | spd_rtng(94)  | difficulty(2) | shield_width(34) | shield_height(60), imodbits_shield ], 
    ["m_leather_covered_round_shield", "Leather Covered Round Shield", [("m_shield_round_d", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_round_shield,            1350, weight(2.5) | hit_points(270) | body_armor(19) | spd_rtng(100) | difficulty(2) | shield_width(40), imodbits_shield ], 
    ["m_tab_shield_kite_cav_a", "Small Kite Shield", [("tableau_shield_kite_4", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield,                          1500, weight(2.0) | hit_points(250) | body_armor(19) | spd_rtng(103) | difficulty(2) | shield_width(30) | shield_height(50), imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_kite_shield_4", ":agent_no", ":troop_no")])]], 
    # ["m_steel_buckler1", "Buckler", [("steel_buckler1",0)], itp_type_shield|itp_cant_use_on_horseback|itp_merchandise, itcf_carry_buckler_left,                                         2300, weight(2.0) | hit_points(250) | body_armor(24) | spd_rtng(105) | difficulty(2) | shield_width(10), imodbits_shield ],
    ["m_tab_shield_small_round_b", "Round Cavalry Shield", [("tableau_shield_small_round_1", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_round_shield,            2500, weight(2.5) | hit_points(265) | body_armor(19) | spd_rtng(100) | difficulty(2) | shield_width(40), imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_small_round_shield_1", ":agent_no", ":troop_no")])]], 
    # ["m_sh_oval", "Oval Shield", [("sh_oval", 0)], itp_type_shield|itp_merchandise, itcf_carry_kite_shield,                                                                             4000, weight(2.5) | hit_points(250) | body_armor(26) | spd_rtng(99)  | difficulty(3) | shield_width(30) | shield_height(50), imodbits_shield ], 
#    ["m_shield_heater_d", "Heraldic Tharch", [("shield_heater_d_new", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield,                                    4500, weight(2.5) | hit_points(250) | body_armor(26) | spd_rtng(99)  | difficulty(3) | shield_width(30) | shield_height(50), imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_shield_heater_d", ":agent_no", ":troop_no")])]], #clan XIV
    # ["m_protector_holy_lightd", "White Knight Shield", [("protector_holy_lightd", 0)], itp_type_shield|itp_merchandise, itcf_carry_kite_shield,                                         4500, weight(2.5) | hit_points(250) | body_armor(26) | spd_rtng(99)  | difficulty(3) | shield_width(30) | shield_height(50), imodbits_shield ], #clan Asgard Guard
    ["m_tab_shield_small_round_c", "Elite Cavalry Shield", [("tableau_shield_small_round_2", 0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield,                             4570, weight(3.0) | hit_points(280) | body_armor(22) | spd_rtng(98)  | difficulty(3) | shield_width(40), imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_small_round_shield_2", ":agent_no", ":troop_no")])]], 
    # ["m_sp_shr1", "Iron Cavalry Shield", [("sp_shr1", 0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield,                                                                    4930, weight(5.0) | hit_points(300) | body_armor(30) | spd_rtng(84)  | difficulty(5) | shield_width(40), imodbits_shield ], 
    ["m_plate_covered_round_shield", "Plate Covered Round Shield", [("m_shield_round_e",0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield,                                  5300, weight(6.2) | hit_points(460) | body_armor(33) | spd_rtng(84)  | difficulty(5) | shield_width(40), imodbits_shield ],
    ["m_tab_shield_heater_cav_b", "Knightly Heater Shield",   [("tableau_shield_heater_2" ,0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,                1450, weight(2.5) | hit_points(260) | body_armor(19) | spd_rtng(100) | difficulty(2) | shield_width(30) | shield_height(50), imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_heater_shield_2", ":agent_no", ":troop_no")])]],



    # Large round shields


    ["m_tab_shield_round_b", "Plain Round Shield", [("tableau_shield_round_3", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_round_shield,                          1200, weight(3.5) | hit_points(365) | body_armor(13) | spd_rtng(88)  | difficulty(2) | shield_width(50), imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_round_shield_3", ":agent_no", ":troop_no")])]], 
    # ["m_iron_shield_mongol_2", "Naimans Cavalry Shield", [("iron_shield_mongol_2", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_round_shield,                      1230, weight(3.5) | hit_points(310) | body_armor(16) | spd_rtng(88)  | difficulty(2) | shield_width(50), imodbits_shield ], #clan Naimans
    ["m_tab_shield_round_c", "Round Shield", [("tableau_shield_round_2", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_round_shield,                                1700, weight(4.0) | hit_points(410) | body_armor(14) | spd_rtng(86)  | difficulty(3) | shield_width(50), imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_round_shield_2", ":agent_no", ":troop_no")])]], 
    ["m_tab_shield_round_d", "Heavy Round Shield", [("tableau_shield_round_1", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_round_shield,                          3000, weight(4.8) | hit_points(465) | body_armor(17) | spd_rtng(85)  | difficulty(4) | shield_width(50), imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_round_shield_1", ":agent_no", ":troop_no")])]], 
    # ["m_Roundshield_06", "Heavy Round Shield", [("Roundshield_06", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_round_shield,                                      3050, weight(4.5) | hit_points(360) | body_armor(20) | spd_rtng(84)  | difficulty(4) | shield_width(50), imodbits_shield ],
    # ["m_s_spartan_hoplon_3", "Spare Shield", [("s_spartan_hoplon_3", 0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield,                                                     3070, weight(4.5) | hit_points(360) | body_armor(20) | spd_rtng(84)  | difficulty(4) | shield_width(50), imodbits_shield ],
    # ["m_HeavyOvalSheild", "Heavy Oval Shield", [("HeavyOvalSheild", 0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield,                                                      3100, weight(4.5) | hit_points(360) | body_armor(20) | spd_rtng(84)  | difficulty(4) | shield_width(50), imodbits_shield ], #user Blade
    # ["m_skellige_shild", "Crate Round Shield", [("skellige_shild", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_round_shield,                                      3100, weight(4.5) | hit_points(360) | body_armor(20) | spd_rtng(84)  | difficulty(4) | shield_width(50), imodbits_shield ], #clan Ulf
    # ["m_shields_archer_antioh_a", "Archer Shield", [("shields_archer_antioh_a", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_round_shield,                         3100, weight(4.5) | hit_points(360) | body_armor(20) | spd_rtng(84)  | difficulty(4) | shield_width(50), imodbits_shield ], #clan Kingdom of Gondor and Arnor
    ["m_tab_shield_round_e", "Huscarl's Round Shield", [("tableau_shield_round_4", 0)], itp_type_shield|itp_cant_use_on_horseback|itp_merchandise, itcf_carry_round_shield,             5000, weight(5.2) | hit_points(580) | body_armor(20) | spd_rtng(84)  | difficulty(5) | shield_width(50), imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_round_shield_4", ":agent_no", ":troop_no")])]], 
	
    # Long shields


    ["m_tab_shield_kite_a","Weak Kite Shield", [("tableau_shield_kite_1", 0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_kite_shield,                                50,   weight(2.25)| hit_points(190) | body_armor(5)  | spd_rtng(96)  | difficulty(0) | shield_width(34) | shield_height(70), imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_kite_shield_1", ":agent_no", ":troop_no")])]], 
    ["m_hide_covered_shield", "Hide Covered Shield", [("m_shield_kite_m", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield,                                600,  weight(3.0) | hit_points(310) | body_armor(15) | spd_rtng(92)  | difficulty(2) | shield_width(34) | shield_height(70), imodbits_shield ],
    ["m_triangle_shield", "Blue and White Shield", [("zimke_triangle_shield_b", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield,                          800,  weight(2.75)| hit_points(285) | body_armor(16) | spd_rtng(97)  | difficulty(2) | shield_width(34) | shield_height(65), imodbits_shield],
    ["m_tab_shield_kite_b", "Plain Kite Shield", [("tableau_shield_kite_3", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield,                              1050, weight(3.0) | hit_points(290) | body_armor(16) | spd_rtng(94)  | difficulty(2) | shield_width(34) | shield_height(70), imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_kite_shield_3", ":agent_no", ":troop_no")])]], 
    ["m_shield_kite_k", "Black and White Kite Shield", [("m_shield_kite_k", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield,                              1550, weight(3.5) | hit_points(330) | body_armor(18) | spd_rtng(91)  | difficulty(3) | shield_width(34) | shield_height(65), imodbits_shield ],
    ["m_shield_kite_g", "Blue and Purple Kite Shield", [("m_shield_kite_g", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield,                              1750, weight(3.0) | hit_points(300) | body_armor(19) | spd_rtng(95)  | difficulty(3) | shield_width(34) | shield_height(65), imodbits_shield ],
    ["m_shield_kite_i", "Leather Covered Kite Shield", [("m_shield_kite_i", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield,                              1800, weight(3.0) | hit_points(300) | body_armor(19) | spd_rtng(95)  | difficulty(3) | shield_width(34) | shield_height(65), imodbits_shield ],
    ["m_tab_shield_kite_c", "Kite Shield", [("tableau_shield_kite_2", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield,                                    2100, weight(3.5) | hit_points(330) | body_armor(18) | spd_rtng(91)  | difficulty(3) | shield_width(34) | shield_height(70), imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_kite_shield_2", ":agent_no", ":troop_no")])]], 
    ["m_tab_shield_heater_c", "Heater Shield", [("tableau_shield_heater_1", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield,                              4100, weight(4.2) | hit_points(365) | body_armor(22) | spd_rtng(89)  | difficulty(4) | shield_width(34) | shield_height(70), imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_heater_shield_1", ":agent_no", ":troop_no")])]], 
	
    # Board shields


    ["m_tab_shield_pavise_c", "Board Shield", [("gg_shield_pavise_1", 0)], itp_type_shield|itp_cant_use_on_horseback|itp_wooden_parry|itp_merchandise, itcf_carry_board_shield,    3200, weight(5.0) | hit_points(410) | body_armor(14) | spd_rtng(72)  | difficulty(2) | shield_width(40) | shield_height(80), imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_pavise_shield_1", ":agent_no", ":troop_no")])]], 
	
    # Norman shields

    ["m_shield_kite_h", "Kite Shield", [("m_shield_kite_h", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield,                       1300, weight(3.25)| hit_points(330) | body_armor(17) | spd_rtng(94) | difficulty(3) | shield_width(34) | shield_height(70), imodbits_shield ],
    ["m_norman_shield_8", "Kite Shield", [("norman_shield_8", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield,                     1400, weight(3.25)| hit_points(330) | body_armor(17) | spd_rtng(94) | difficulty(3) | shield_width(34) | shield_height(70), imodbits_shield ],
    ["m_norman_shield_4", "Kite Shield", [("norman_shield_4", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield,                     1410, weight(3.25)| hit_points(330) | body_armor(17) | spd_rtng(94) | difficulty(3) | shield_width(34) | shield_height(70), imodbits_shield ],
    ["m_norman_shield_2", "Kite Shield", [("norman_shield_2", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield,                     1420, weight(3.25)| hit_points(330) | body_armor(17) | spd_rtng(94) | difficulty(3) | shield_width(34) | shield_height(70), imodbits_shield ],
    ["m_norman_shield_heraldic_1", "Kite Shield", [("m_norman_shield_heraldic_1", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield, 1450, weight(3.25)| hit_points(330) | body_armor(17) | spd_rtng(94) | difficulty(3) | shield_width(34) | shield_height(70), imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_m_norman_shield_heraldic_1", ":agent_no", ":troop_no")])]],
    ["m_norman_shield_6", "Kite Shield", [("norman_shield_6", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield,                     1600, weight(3.5) | hit_points(330) | body_armor(18) | spd_rtng(91) | difficulty(3) | shield_width(34) | shield_height(70), imodbits_shield ],
    ["m_norman_shield_7", "Kite Shield", [("norman_shield_7", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield,                     1610, weight(3.5) | hit_points(330) | body_armor(18) | spd_rtng(91) | difficulty(3) | shield_width(34) | shield_height(70), imodbits_shield ],
    ["m_norman_shield_5", "Kite Shield", [("norman_shield_5", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield,                     1620, weight(3.5) | hit_points(330) | body_armor(18) | spd_rtng(91) | difficulty(3) | shield_width(34) | shield_height(70), imodbits_shield ],
    ["m_norman_shield_1", "Kite Shield", [("norman_shield_1", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield,                     1630, weight(3.5) | hit_points(330) | body_armor(18) | spd_rtng(91) | difficulty(3) | shield_width(34) | shield_height(70), imodbits_shield ],
    ["m_norman_shield_3", "Kite Shield", [("norman_shield_3", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield,                     1640, weight(3.5) | hit_points(330) | body_armor(18) | spd_rtng(91) | difficulty(3) | shield_width(34) | shield_height(70), imodbits_shield ],
	
    # Arena shields
    ["m_arena_shield_red", "Red Shield", [("arena_shield_red", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield,              200, weight(2.0) | hit_points(220) | body_armor(14) | spd_rtng(103) | difficulty(0) | shield_width(30) | shield_height(50), imodbits_shield ],
    ["m_arena_shield_blue", "Blue Shield", [("arena_shield_blue", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield,           200, weight(2.0) | hit_points(220) | body_armor(14) | spd_rtng(103) | difficulty(0) | shield_width(30) | shield_height(50), imodbits_shield ],
    ["m_arena_shield_green", "Green Shield", [("arena_shield_green", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield,        200, weight(2.0) | hit_points(220) | body_armor(14) | spd_rtng(103) | difficulty(0) | shield_width(30) | shield_height(50), imodbits_shield ],
    ["m_arena_shield_yellow", "Yellow Shield", [("arena_shield_yellow", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield,     200, weight(2.0) | hit_points(220) | body_armor(14) | spd_rtng(103) | difficulty(0) | shield_width(30) | shield_height(50), imodbits_shield ],
	
    ["m_heater_shield_1", "Black and White Heater Shield", [("cwe_shield_knight_templar_a", 0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_kite_shield,   2300, weight(2.25)| hit_points(260) | body_armor(19) | spd_rtng(102)| difficulty(2) | shield_width(30) | shield_height(50), imodbits_shield ],
    ["m_kite_shield_1", "Black and White Kite Shield", [("cwe_shield_veteran_templar_a", 0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_kite_shield,      1900, weight(3.5) | hit_points(330) | body_armor(18) | spd_rtng(91) | difficulty(3) | shield_width(34) | shield_height(70), imodbits_shield ],
    ["m_kite_shield_2", "Black and White Kite Shield", [("cwe_shield_veteran_templar_g", 0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_kite_shield,      1970, weight(3.5) | hit_points(330) | body_armor(18) | spd_rtng(91) | difficulty(3) | shield_width(34) | shield_height(70), imodbits_shield ],
    ["m_kite_shield_2_blue", "Blue Kite Shield", [("cwe_shield_veteran_templar_g_blue", 0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_kite_shield,       1980, weight(3.5) | hit_points(330) | body_armor(18) | spd_rtng(91) | difficulty(3) | shield_width(34) | shield_height(70), imodbits_shield ],
    ["m_sarranid_round_shield_1", "Round Sarranid Shield", [("cwe_saracen_shield_g", 0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield,                          4250, weight(3.25)| hit_points(320) | body_armor(22) | spd_rtng(98) | difficulty(3) | shield_width(37), imodbits_shield ],
    ["m_sarranid_round_shield_2", "Round Sarranid Shield", [("cwe_saracen_shield_h", 0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield,                          4230, weight(3.25)| hit_points(320) | body_armor(22) | spd_rtng(98) | difficulty(3) | shield_width(37), imodbits_shield ],
    ["m_sarranid_round_shield_3", "Round Sarranid Shield", [("cwe_saracen_shield_k", 0)], itp_type_shield, itcf_carry_round_shield,                                          4270, weight(3.25)| hit_points(320) | body_armor(22) | spd_rtng(98) | difficulty(3) | shield_width(37), imodbits_shield ],
    ["m_sarranid_round_shield_6", "Round Sarranid Shield", [("cwe_saracen_shield_q", 0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield,                          4400, weight(3.25)| hit_points(320) | body_armor(22) | spd_rtng(98) | difficulty(3) | shield_width(37), imodbits_shield ],
    ["m_sarranid_round_shield_4", "Round Sarranid Shield", [("cwe_saracen_shield_l", 0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield,                          4425, weight(3.25)| hit_points(320) | body_armor(22) | spd_rtng(98) | difficulty(3) | shield_width(37), imodbits_shield ],
    ["m_sarranid_round_shield_5", "Round Sarranid Shield", [("cwe_saracen_shield_p", 0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield,                          4450, weight(3.25)| hit_points(320) | body_armor(22) | spd_rtng(98) | difficulty(3) | shield_width(37), imodbits_shield ],

    #nessa
    ["saracin_shield_t", "Rare Shield", [("saracin_shield_t", 0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield,                          450, weight(3.25)| hit_points(320) | body_armor(22) | spd_rtng(99) | difficulty(3) | shield_width(37), imodbits_shield ],
    ["saracin_shield_y", "Golden Shield", [("saracin_shield_y", 0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield,                          35000, weight(3.25)| hit_points(320) | body_armor(22) | spd_rtng(99) | difficulty(3) | shield_width(37), imodbits_shield ],
    # THROWING WEAPON

    ["m_stone", "Stone", [("m_throwing_stone", 0)], itp_type_thrown|itp_primary, itcf_throw_stone,
     10,   weight(1.5) | difficulty(0) | spd_rtng(100) | shoot_speed(23) | thrust_damage(8, blunt)  | max_ammo(5)| weapon_length(8), imodbit_large_bag, [m_missile_init_trigger]],
    ["m_torch", "Torch", [("m_torch", 0), ("m_torch_flying", ixmesh_flying_ammo)], itp_type_thrown|itp_primary|itp_next_item_as_melee|itp_merchandise|custom_kill_info(6), itcf_throw_stone,
     500,  weight(1.0) | difficulty(0) | spd_rtng(104) | shoot_speed(15) | thrust_damage(15, blunt)  | max_ammo(1) | weapon_length(74), imodbits_thrown_minus_heavy, [(ti_on_init_item, [(set_position_delta,0,65,0),(particle_system_add_new, "psys_torch_fire"),(particle_system_add_new, "psys_torch_smoke"),(particle_system_add_new, "psys_torch_fire_sparks"),(set_current_color,150, 130, 70),(add_point_light, 10, 30),(set_position_delta, 0, 68, 0),(particle_system_add_new, "psys_torch_glow"),(particle_system_emit, "psys_torch_glow", 9000000),]),(ti_on_init_missile, [(set_position_delta,0,65,0),(particle_system_add_new, "psys_torch_fire"),(particle_system_add_new, "psys_torch_smoke"),(particle_system_add_new, "psys_torch_fire_sparks"),(set_current_color,150, 130, 70),(add_point_light, 10, 30),(set_position_delta, 0, 68, 0),(particle_system_add_new, "psys_torch_glow"),(particle_system_emit, "psys_torch_glow", 9000000),]), m_missile_init_trigger, m_torch_missile_hit_trigger] ], 
    ["m_torch_melee", "Torch", [("m_torch", 0)], itp_type_one_handed_wpn|itp_primary|itp_wooden_parry|custom_kill_info(6), itc_longsword,
     200,  weight(1.0) | difficulty(0) | spd_rtng(99)  | swing_damage(12, cut) | thrust_damage(12, cut) | weapon_length(74), imodbits_thrown_minus_heavy, []],
    ["m_throwing_knives", "Throwing Knife", [("m_throwing_knife",0)], itp_type_thrown|itp_primary|itp_merchandise, itcf_throw_knife,
     3250,  weight(0.5) | difficulty(0) | spd_rtng(110) | shoot_speed(25) | thrust_damage(25, cut) | max_ammo(6), imodbits_thrown, [m_missile_init_trigger]],
    ["m_light_dart", "Light Dart", [("dart_b",0), ("dart_a_bag", ixmesh_carry)], itp_type_thrown|itp_primary|itp_merchandise, itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn,
     4300,  weight(1.25)| difficulty(0) | spd_rtng(97) | shoot_speed(24) | thrust_damage(30, cut) | max_ammo(4) | weapon_length(32), imodbits_thrown, [m_missile_init_trigger]],
    ["m_dart", "Darts", [("dart_a",0), ("dart_a_bag", ixmesh_carry)], itp_type_thrown|itp_primary|itp_merchandise, itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn,
     4400,  weight(1.5) | difficulty(0) | spd_rtng(96) | shoot_speed(23) | thrust_damage(31, cut) | max_ammo(4) | weapon_length(45), imodbits_thrown, [m_missile_init_trigger]],
    ["m_francisca", "Light Throwing Axe", [("m_francisca", 0), ("gg_francisca_quiver", ixmesh_carry)], itp_type_thrown|itp_primary|itp_next_item_as_melee|itp_bonus_against_shield|itp_merchandise, itcf_throw_axe|itcf_carry_axe_left_hip|itcf_show_holster_when_drawn,
     4350,  weight(1.25)| difficulty(0) | spd_rtng(99) | shoot_speed(20) | thrust_damage(32, cut)    | max_ammo(3) | weapon_length(53), imodbits_thrown_minus_heavy, [m_missile_init_trigger]], 
    ["m_francisca_melee", "Light Throwing Axe", [("m_francisca",0), ("gg_francisca_quiver", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_bonus_against_shield, itc_scimitar,
     4350,  weight(1.25) | difficulty(6) | spd_rtng(103) | swing_damage(25, cut) | thrust_damage(0, pierce) | weapon_length(53), imodbits_thrown_minus_heavy ],
    ["m_light_throwing_axes", "Throwing Axe", [("throwing_axe_a", 0), ("gg_throwing_axe_a_quiver", ixmesh_carry)], itp_type_thrown|itp_primary|itp_next_item_as_melee|itp_bonus_against_shield|itp_merchandise, itcf_throw_axe|itcf_carry_axe_left_hip|itcf_show_holster_when_drawn,
     4550,  weight(1.75)| difficulty(0) | spd_rtng(98) | shoot_speed(20) | thrust_damage(35, cut)    | max_ammo(3) | weapon_length(54), imodbits_thrown_minus_heavy, [m_missile_init_trigger]], 
    ["m_light_throwing_axes_melee", "Throwing Axe", [("throwing_axe_a",0), ("gg_throwing_axe_a_quiver", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_bonus_against_shield, itc_scimitar,
     4550,  weight(1.75) | difficulty(6) | spd_rtng(102) | swing_damage(26, cut) | thrust_damage(0, pierce) | weapon_length(54), imodbits_thrown_minus_heavy ],
    ["m_heavy_throwing_axes", "Heavy Throwing Axe", [("throwing_axe_b", 0), ("gg_throwing_axe_b_quiver", ixmesh_carry)], itp_type_thrown|itp_primary|itp_next_item_as_melee|itp_bonus_against_shield|itp_merchandise, itcf_throw_axe|itcf_carry_axe_left_hip|itcf_show_holster_when_drawn,
     4700,  weight(1.25)| difficulty(0) | spd_rtng(97) | shoot_speed(20) | thrust_damage(37, cut)    | max_ammo(2) | weapon_length(57), imodbits_thrown_minus_heavy, [m_missile_init_trigger]], 
    ["m_heavy_throwing_axes_melee", "Throwing Axe", [("throwing_axe_b",0), ("gg_throwing_axe_b_quiver", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_bonus_against_shield, itc_scimitar,
     4700,  weight(1.0) | difficulty(6) | spd_rtng(101) | swing_damage(27, cut) | thrust_damage(0, pierce) | weapon_length(57), imodbits_thrown_minus_heavy ],
    ["m_light_javelin","Light Javelin", [("javelin", 0),("javelins_quiver_new", ixmesh_carry)], itp_type_thrown|itp_primary|itp_next_item_as_melee|itp_merchandise, itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn,
     5470,  weight(1.75)| difficulty(0) | spd_rtng(95)  | shoot_speed(23) | thrust_damage(24, pierce) | max_ammo(3) | weapon_length(76), imodbits_thrown, [m_missile_init_trigger]],
    ["m_light_javelin_melee","Light Javelin", [("javelin", 0)], itp_type_one_handed_wpn|itp_wooden_parry|itp_primary, itc_longsword,
     5470,  weight(1.0) | difficulty(6) | spd_rtng(97)  | swing_damage(12, blunt) | weapon_length(76) | thrust_damage(21, pierce), imodbits_thrown],
    ["m_javelin", "Javelin", [("jarid_new_b", 0), ("jarid_new_b_bag", ixmesh_carry)], itp_type_thrown|itp_primary|itp_next_item_as_melee|itp_merchandise, itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn,
     6050,  weight(2.0) | difficulty(0) | spd_rtng(95)  | shoot_speed(19) | thrust_damage(30, pierce) | max_ammo(3) | weapon_length(80), imodbits_thrown, [m_missile_init_trigger]], 
    ["m_javelin_melee", "Javelin", [("jarid_new_b", 0), ("jarid_new_b_bag", ixmesh_carry)], itp_type_one_handed_wpn|itp_wooden_parry|itp_primary, itc_longsword,
     6050,  weight(2.0) | difficulty(6) | spd_rtng(97)  | swing_damage(14, blunt) | weapon_length(80) | thrust_damage(22, pierce), imodbits_thrown ],
    ["m_throwing_star_c", "Orion", [("throwing_star_c", 0)], itp_type_thrown|itp_primary|itp_merchandise, itcf_throw_knife,
     4300, weight(0.5) | difficulty(0) | spd_rtng(110) | shoot_speed(25) | thrust_damage(26, cut)    | max_ammo(4) | weapon_length(5), imodbits_thrown, [m_missile_init_trigger]], 
		

    # BOWS


    ["m_short_bow", "Short Bow", [("m_short_bow",0),("m_short_bow_carry",ixmesh_carry)], itp_type_bow|itp_primary|itp_two_handed|itp_merchandise, itcf_shoot_bow|itcf_carry_bow_back,
     920,  weight(3.6) | difficulty(1) | spd_rtng(69) | shoot_speed(61) | thrust_damage(19, pierce) | accuracy(102), imodbits_bow ], 
    ["m_nomad_bow", "Nomad Bow", [("nomad_bow", 0), ("nomad_bow_case", ixmesh_carry)], itp_type_bow|itp_primary|itp_two_handed|itp_merchandise, itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn,
     1300, weight(4.0)| difficulty(2) | spd_rtng(66) | shoot_speed(57) | thrust_damage(20, pierce) | accuracy(100), imodbits_bow ], 
    ["m_bow", "Hunting Bow", [("gg_hunting_bow", 0), ("gg_hunting_bow_carry", ixmesh_carry)], itp_type_bow|itp_primary|itp_two_handed|itp_merchandise, itcf_shoot_bow|itcf_carry_bow_back,
     1500, weight(4.8)| difficulty(3) | spd_rtng(60) | shoot_speed(57) | thrust_damage(21, pierce) | accuracy(99), imodbits_bow ],
    ["m_banded_bow", "Oak Long Bow", [("gg_long_bow", 0), ("gg_long_bow_carry", ixmesh_carry)], itp_type_bow|itp_primary|itp_cant_use_on_horseback|itp_two_handed|itp_merchandise, itcf_shoot_bow|itcf_carry_bow_back,
     4000, weight(5.5) | difficulty(5) | spd_rtng(53) | shoot_speed(54) | thrust_damage(23, pierce) | accuracy(96), imodbits_bow ],
    ["m_khergit_bow", "Khergit Bow", [("khergit_bow", 0), ("khergit_bow_case", ixmesh_carry)], itp_type_bow|itp_primary|itp_two_handed|itp_merchandise, itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn,
     3500, weight(4.8)| difficulty(3) | spd_rtng(62) | shoot_speed(56) | thrust_damage(21, pierce) | accuracy(97), imodbits_bow ], 
    ["m_strong_bow", "Strong Bow", [("strong_bow", 0), ("strong_bow_case", ixmesh_carry)], itp_type_bow|itp_primary|itp_two_handed|itp_merchandise, itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn,
     5950, weight(4.8)| difficulty(3) | spd_rtng(57) | shoot_speed(55) | thrust_damage(23, pierce) | accuracy(96), imodbits_bow ],
    ["m_long_bow", "Long Bow", [("long_bow", 0), ("long_bow_carry", ixmesh_carry)], itp_type_bow|itp_primary|itp_cant_use_on_horseback|itp_two_handed|itp_merchandise, itcf_shoot_bow|itcf_carry_bow_back,    
     3850, weight(5.5) | difficulty(4) | spd_rtng(56) | shoot_speed(54) | thrust_damage(22, pierce) | accuracy(97), imodbits_bow ],                                     
    ["m_war_bow", "War Bow", [("war_bow", 0), ("war_bow_carry", ixmesh_carry)], itp_type_bow|itp_primary|itp_cant_use_on_horseback|itp_two_handed|itp_merchandise, itcf_shoot_bow|itcf_carry_bow_back,
     5350, weight(5.7) | difficulty(6) | spd_rtng(51) | shoot_speed(54) | thrust_damage(24, pierce) | accuracy(95), imodbits_bow ], 
    ["mongol_bow_3", "Rare Strong Bow", [("mongol_bow_3", 0), ("mongol_bow_3_case", ixmesh_carry)], itp_type_bow|itp_primary|itp_two_handed|itp_merchandise, itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn,
     50000, weight(4.8)| difficulty(3) | spd_rtng(57) | shoot_speed(55) | thrust_damage(23, pierce) | accuracy(96), imodbits_bow ],
	

    # CROSSBOWS


    ["m_light_crossbow", "Light Crossbow", [("gg_crossbow_b", 0)], itp_type_crossbow |itp_primary|itp_two_handed|itp_merchandise, itcf_shoot_crossbow|itcf_carry_crossbow_back,
     2800, weight(2.5) | difficulty(1) | spd_rtng(29) | shoot_speed(63) | thrust_damage(45, pierce) | accuracy(97) | max_ammo(1), imodbits_crossbow ], 
    ["m_crossbow", "Crossbow", [("gg_crossbow_a", 0)], itp_type_crossbow |itp_primary|itp_two_handed|itp_cant_reload_on_horseback|itp_merchandise, itcf_shoot_crossbow|itcf_carry_crossbow_back,
     4400, weight(3.0) | difficulty(2) | spd_rtng(29) | shoot_speed(67) | thrust_damage(52, pierce) | accuracy(98) | max_ammo(1), imodbits_crossbow ], 
    ["m_heavy_crossbow", "Heavy Crossbow", [("gg_crossbow_c", 0)], itp_type_crossbow |itp_primary|itp_two_handed|itp_cant_reload_on_horseback|itp_merchandise, itcf_shoot_crossbow|itcf_carry_crossbow_back,
     6700, weight(3.5) | difficulty(3) | spd_rtng(27) | shoot_speed(70) | thrust_damage(58, pierce) | accuracy(97) | max_ammo(1), imodbits_crossbow ], 
    ["m_arbalest", "Arbalest", [("gg_arbalest", 0)], itp_type_crossbow |itp_primary|itp_two_handed|itp_cant_reload_on_horseback|itp_merchandise, itcf_shoot_crossbow|itcf_carry_crossbow_back,    
     10000, weight(4.0) | difficulty(4) | spd_rtng(26) | shoot_speed(75) | thrust_damage(62, pierce) | accuracy(96) | max_ammo(1), imodbits_crossbow ], 

##  ["m_hand_crossbow_a","Hand Crossbow", [("hand_crossbow_a", 0)], itp_type_crossbow|itp_primary|itp_merchandise, itcf_shoot_crossbow|itcf_carry_pistol_front_left|itcf_reload_musket,                                0, weight(1.0) | difficulty(0) | spd_rtng(30) | shoot_speed(58) | thrust_damage(40, pierce) | accuracy(92) | max_ammo(1), imodbits_crossbow ],
##  ["m_hand_crossbow_b","Hand Crossbow", [("hand_crossbow_b", 0)], itp_type_crossbow|itp_primary|itp_merchandise, itcf_shoot_crossbow|itcf_carry_pistol_front_left|itcf_reload_musket,                                0, weight(1.0) | difficulty(0) | spd_rtng(30) | shoot_speed(58) | thrust_damage(40, pierce) | accuracy(92) | max_ammo(1), imodbits_crossbow ],

    ["m_crossbows_end", "Crossbows End", [("invisible",0)], itp_type_one_handed_wpn, 0, 0 , weight(0)|abundance(0)|head_armor(0)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],

	
    # AMMO


    ["m_arrows", "Arrows", [("arrow", 0), ("flying_missile", ixmesh_flying_ammo), ("quiver", ixmesh_carry)], itp_type_arrows|itp_default_ammo|itp_merchandise, itcf_carry_quiver_back,
     1080,  weight(3.0) | abundance(100) | weapon_length(95) | thrust_damage(1, pierce) | max_ammo(25), imodbits_missile, [m_missile_init_trigger]], 
    ["m_barbed_arrows", "Nomad Arrows", [("barbed_arrow", 0), ("flying_missile", ixmesh_flying_ammo), ("quiver_d", ixmesh_carry)], itp_type_arrows|itp_merchandise, itcf_carry_quiver_back_right,
     2300,  weight(3.5) | abundance(100) | weapon_length(95) | thrust_damage(2, pierce) | max_ammo(19), imodbits_missile, [m_missile_init_trigger]], 
    ["m_khergit_arrows", "Khergit Arrows", [("arrow_b", 0), ("flying_missile", ixmesh_flying_ammo), ("quiver_b", ixmesh_carry)], itp_type_arrows|itp_merchandise, itcf_carry_quiver_back_right,
     2650, weight(4.0) | abundance(100) | weapon_length(95) | thrust_damage(3, pierce) | max_ammo(14), imodbits_missile, [m_missile_init_trigger]], 
    ["m_bodkin_arrows", "Bodkin Arrows", [("piercing_arrow", 0), ("flying_missile", ixmesh_flying_ammo), ("quiver_c", ixmesh_carry)], itp_type_arrows|itp_merchandise, itcf_carry_quiver_back_right,
     3120, weight(4.0) | abundance(100) | weapon_length(91) | thrust_damage(4, pierce) | max_ammo(11), imodbits_missile, [m_missile_init_trigger]], 
    # # ["m_spak_bow8_arrow", "Strong Arrows", [("spak_bow8_arrow", 0), ("flying_missile", ixmesh_flying_ammo), ("spak_bow8_quiver", ixmesh_carry)], itp_type_arrows|itp_merchandise, itcf_carry_quiver_back,                                 1900, weight(1.5) | abundance(100) | weapon_length(91) | thrust_damage(2, pierce) | max_ammo(19), imodbits_missile, [m_missile_init_trigger]], #user Rinus
    ["m_bolts", "Bolts", [("bolt", 0), ("flying_missile", ixmesh_flying_ammo), ("bolt_bag", ixmesh_carry)], itp_type_bolts|itp_default_ammo|itp_can_penetrate_shield|itp_merchandise, itcf_carry_quiver_right_vertical,
     1340,  weight(1.0) | abundance(100) | weapon_length(63) | thrust_damage(2, pierce) | max_ammo(15), imodbits_missile, [m_missile_init_trigger]], 
    ["m_steel_bolts", "Steel Bolts", [("bolt", 0), ("flying_missile", ixmesh_flying_ammo), ("bolt_bag_b", ixmesh_carry)], itp_type_bolts|itp_can_penetrate_shield|itp_merchandise, itcf_carry_quiver_right_vertical,
     2780, weight(1.5) | abundance(100) | weapon_length(63) | thrust_damage(3, pierce) | max_ammo(11), imodbits_missile, [m_missile_init_trigger]], 

#Cakebatter AMMO start
  #Projectile meanings:
  #Leaf = No Bonus to opponents
  #Barbed = Bonus against light armoured opponent, minor bonus against medium armoured opponents
  #Broadhead = Bonus against medium armoured opponent, minor bonus against light/heavy armoured opponents
  #Bodkin = Bonus against heavy armoured opponent, minor bonus against medium armoured opponents
  #Flaming = No bonus to opponents, sets fire to flameable objects
    #Arrows
    
     #["m_warlords_leaf_arrows", "Leaf Arrows", [("warlords_arrow_leaf_mesh", 0), ("flying_missile", ixmesh_flying_ammo), ("warlords_arrow_leaf_quiver_mesh", ixmesh_carry)], itp_type_arrows|itp_default_ammo|itp_merchandise, itcf_carry_quiver_back_right,
     #  500, weight(1.5) | abundance(100) | weapon_length(95) | thrust_damage(1, pierce) | max_ammo(25), imodbits_missile, [m_missile_init_trigger]],
     #["m_warlords_sharp_leaf_arrows", "Sharp Leaf Arrows", [("warlords_arrow_sharp_leaf_mesh", 0), ("flying_missile", ixmesh_flying_ammo), ("warlords_arrow_sharp_leaf_quiver_mesh", ixmesh_carry)], itp_type_arrows|itp_merchandise, itcf_carry_quiver_back_right,
     #  700, weight(1.3) | abundance(100) | weapon_length(95) | thrust_damage(2, pierce) | max_ammo(21), imodbits_missile, [m_missile_init_trigger]],

##     ["m_warlords_barbed_arrows", "Barbed Arrows", [("warlords_arrow_barbed_mesh", 0), ("flying_missile", ixmesh_flying_ammo), ("warlords_arrow_barbed_quiver_mesh", ixmesh_carry)], itp_type_arrows|itp_merchandise, itcf_carry_quiver_back_right,
##      1000, weight(1.4) | abundance(100) | weapon_length(95) | thrust_damage(1, pierce) | max_ammo(23), imodbits_missile, [m_missile_init_trigger]],
##     ["m_warlords_wide_barbed_arrows", "Wide Barbed Arrows", [("warlords_arrow_wide_barbed_mesh", 0), ("flying_missile", ixmesh_flying_ammo), ("warlords_arrow_wide_barbed_quiver_mesh", ixmesh_carry)], itp_type_arrows|itp_merchandise, itcf_carry_quiver_back_right,
##      1300, weight(1.2) | abundance(100) | weapon_length(95) | thrust_damage(2, pierce) | max_ammo(19), imodbits_missile, [m_missile_init_trigger]],
##
##     ["m_warlords_broadhead_arrows", "Broadhead Arrows", [("warlords_arrow_broadhead_mesh", 0), ("flying_missile", ixmesh_flying_ammo), ("warlords_arrow_broadhead_quiver_mesh", ixmesh_carry)], itp_type_arrows|itp_merchandise, itcf_carry_quiver_back_right,
##      1500, weight(1.3) | abundance(100) | weapon_length(95) | thrust_damage(1, pierce) | max_ammo(21), imodbits_missile, [m_missile_init_trigger]],
##     ["m_warlords_large_broadhead_arrows", "Large Broadhead Arrows", [("warlords_arrow_large_broadhead_mesh", 0), ("flying_missile", ixmesh_flying_ammo), ("warlords_arrow_large_broadhead_quiver_mesh", ixmesh_carry)], itp_type_arrows|itp_merchandise, itcf_carry_quiver_back_right,
##      1700, weight(1.1) | abundance(100) | weapon_length(95) | thrust_damage(2, pierce) | max_ammo(17), imodbits_missile, [m_missile_init_trigger]],
## 
##     ["m_warlords_bodkin_arrows", "Bodkin Arrows", [("warlords_arrow_bodkin_mesh", 0), ("flying_missile", ixmesh_flying_ammo), ("warlords_arrow_bodkin_quiver_mesh", ixmesh_carry)], itp_type_arrows|itp_merchandise, itcf_carry_quiver_back_right,
##      2000, weight(1.2) | abundance(100) | weapon_length(95) | thrust_damage(1, pierce) | max_ammo(19), imodbits_missile, [m_missile_init_trigger]],
##     
##     ["m_warlords_needle_bodkin_arrows", "Needle Bodkin Arrows", [("warlords_arrow_needle_bodkin_mesh", 0), ("flying_missile", ixmesh_flying_ammo), ("warlords_arrow_needle_bodkin_quiver_mesh", ixmesh_carry)], itp_type_arrows|itp_merchandise, itcf_carry_quiver_back_right,
##      2300, weight(1.0) | abundance(100) | weapon_length(95) | thrust_damage(2, pierce) | max_ammo(15), imodbits_missile, [m_missile_init_trigger]],
  
  #   ["m_warlords_flaming_arrows", "Flaming Arrows", [("warlords_arrow_flaming_mesh", 0), ("m_flying_missile_fire", ixmesh_flying_ammo), ("warlords_arrow_flaming_quiver_mesh", ixmesh_carry)], itp_type_arrows|itp_merchandise, itcf_carry_quiver_back_right,
  #    0, weight(1.5) | abundance(100) | weapon_length(98) | thrust_damage(2, pierce) | max_ammo(4), imodbits_missile, [(ti_on_init_item, [(set_position_delta, 0, 80, 0),(particle_system_add_new, "psys_torch_fire", pos1),]),(ti_on_init_missile, [(set_position_delta, 0, 80, 0),(particle_system_add_new, "psys_torch_fire", pos1),]),m_missile_init_trigger,(ti_on_missile_dive, [(particle_system_remove),]), m_fire_arrow_hit_trigger]],
    
    # #Bolts
   
    #["m_warlords_leaf_bolts", "Leaf Bolts", [("warlords_bolt_leaf_mesh", 0), ("flying_missile", ixmesh_flying_ammo), ("warlords_bolt_leaf_quiver_mesh", ixmesh_carry)], itp_type_bolts|itp_default_ammo|itp_can_penetrate_shield|itp_merchandise, itcf_carry_quiver_right_vertical,
    #  500,  weight(1.6) | abundance(100) | weapon_length(63) | thrust_damage(2, pierce) | max_ammo(16), imodbits_missile, [m_missile_init_trigger]],
    # ["m_warlords_leaf_steel_bolts", "Steel Leaf Bolts", [("warlords_bolt_steel_leaf_mesh", 0), ("flying_missile", ixmesh_flying_ammo), ("warlords_bolt_steel_leaf_quiver_mesh", ixmesh_carry)], itp_type_bolts|itp_can_penetrate_shield|itp_merchandise, itcf_carry_quiver_right_vertical,
    #  700,  weight(1.5) | abundance(100) | weapon_length(63) | thrust_damage(3, pierce) | max_ammo(14), imodbits_missile, [m_missile_init_trigger]],
  
##     ["m_warlords_barbed_bolts", "Barbed Bolts", [("warlords_bolt_barbed_mesh", 0), ("flying_missile", ixmesh_flying_ammo), ("warlords_bolt_barbed_quiver_mesh", ixmesh_carry)], itp_type_bolts|itp_can_penetrate_shield|itp_merchandise, itcf_carry_quiver_right_vertical,
##      1000,  weight(1.5) | abundance(100) | weapon_length(63) | thrust_damage(2, pierce) | max_ammo(15), imodbits_missile, [m_missile_init_trigger]],
##     ["m_warlords_barbed_steel_bolts", "Steel Barbed Bolts", [("warlords_bolt_steel_barbed_mesh", 0), ("flying_missile", ixmesh_flying_ammo), ("warlords_bolt_steel_barbed_quiver_mesh", ixmesh_carry)], itp_type_bolts|itp_can_penetrate_shield|itp_merchandise, itcf_carry_quiver_right_vertical,
##      1300,  weight(1.4) | abundance(100) | weapon_length(63) | thrust_damage(3, pierce) | max_ammo(13), imodbits_missile, [m_missile_init_trigger]],
##
##     ["m_warlords_broadhead_bolts", "Broadhead Bolts", [("warlords_bolt_broadhead_mesh", 0), ("flying_missile", ixmesh_flying_ammo), ("warlords_bolt_broadhead_quiver_mesh", ixmesh_carry)], itp_type_bolts|itp_can_penetrate_shield|itp_merchandise, itcf_carry_quiver_right_vertical,
##      1500,  weight(1.4) | abundance(100) | weapon_length(63) | thrust_damage(2, pierce) | max_ammo(14), imodbits_missile, [m_missile_init_trigger]],
##     ["m_warlords_broadhead_steel_bolts", "Steel Broadhead Bolts", [("warlords_bolt_steel_broadhead_mesh", 0), ("flying_missile", ixmesh_flying_ammo), ("warlords_bolt_steel_broadhead_quiver_mesh", ixmesh_carry)], itp_type_bolts|itp_can_penetrate_shield|itp_merchandise, itcf_carry_quiver_right_vertical,
##      1700,  weight(1.3) | abundance(100) | weapon_length(63) | thrust_damage(3, pierce) | max_ammo(12), imodbits_missile, [m_missile_init_trigger]],
##    
##     ["m_warlords_bodkin_bolts", "Bodkin Bolts", [("warlords_bolt_bodkin_mesh", 0), ("flying_missile", ixmesh_flying_ammo), ("warlords_bolt_bodkin_quiver_mesh", ixmesh_carry)], itp_type_bolts|itp_can_penetrate_shield|itp_merchandise, itcf_carry_quiver_right_vertical,
##      2000,  weight(1.3) | abundance(100) | weapon_length(63) | thrust_damage(2, pierce) | max_ammo(13), imodbits_missile, [m_missile_init_trigger]],
##     ["m_warlords_bodkin_steel_bolts", "Steel Bodkin Bolts", [("warlords_bolt_steel_bodkin_mesh", 0), ("flying_missile", ixmesh_flying_ammo), ("warlords_bolt_steel_bodkin_quiver_mesh", ixmesh_carry)], itp_type_bolts|itp_can_penetrate_shield|itp_merchandise, itcf_carry_quiver_right_vertical,
##      2300,  weight(1.2) | abundance(100) | weapon_length(63) | thrust_damage(3, pierce) | max_ammo(11), imodbits_missile, [m_missile_init_trigger]],

#Cakebatter AMMO end
	
	
    # POTIONS


     ["m_potion_regeneration", "Healing Drink", [("mandible_bottle_red", 0), ("mandible_bottle_red_carry", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_wooden_parry|itp_merchandise, itcf_carry_dagger_front_right,
      3900, weight(0.5) | difficulty(0) | spd_rtng(0) | weapon_length(10) | swing_damage(0, cut) | thrust_damage(0, pierce), imodbits_axe ], 
     ["m_potion_pain_killing", "Pain Killing Drink", [("mandible_bottle_green", 0), ("mandible_bottle_green_carry", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_wooden_parry|itp_merchandise, itcf_carry_dagger_front_right,
      2400, weight(0.5) | difficulty(0) | spd_rtng(0) | weapon_length(10) | swing_damage(0, cut) | thrust_damage(0, pierce), imodbits_axe ], 
     ["m_potion_concentration", "Refreshing Drink", [("mandible_bottle_blue", 0), ("mandible_bottle_blue_carry", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_wooden_parry|itp_merchandise, itcf_carry_dagger_front_right,
      3000, weight(0.5) | difficulty(0) | spd_rtng(0) | weapon_length(10) | swing_damage(0, cut) | thrust_damage(0, pierce), imodbits_axe ], 
     ["m_potion_strength", "Strengthening Drink", [("mandible_bottle_black", 0), ("mandible_bottle_black_carry", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_wooden_parry|itp_merchandise, itcf_carry_dagger_front_right,
      5100, weight(0.5) | difficulty(0) | spd_rtng(0) | weapon_length(10) | swing_damage(0, cut) | thrust_damage(0, pierce), imodbits_axe ], 
     ["m_potion_speed", "Bracing Drink", [("mandible_bottle_white", 0), ("mandible_bottle_white_carry", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_wooden_parry|itp_merchandise, itcf_carry_dagger_front_right,
      4500, weight(0.5) | difficulty(0) | spd_rtng(0) | weapon_length(10) | swing_damage(0, cut) | thrust_damage(0, pierce), imodbits_axe ], 
   # ["m_potion_night_vision", "Night Vision Drink", [("mandible_bottle_yellow", 0), ("mandible_bottle_yellow_carry", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_wooden_parry|itp_merchandise, itcf_carry_dagger_front_right,
   #  1500, weight(0.5) | difficulty(0) | spd_rtng(0) | weapon_length(10) | swing_damage(0, cut) | thrust_damage(0, pierce), imodbits_axe ],
     ["m_potions_end", "Potions End", [("shield_round_a",0)], 0, 0, 1, 0, 0],


    # FIREARMS


    ["m_hand_cannon_1","Handgonne", [("gg_handgonne_a", 0),("gg_handgonne_a_carry", ixmesh_carry)],itp_type_musket|itp_cant_reload_while_moving|itp_cant_use_on_horseback|itp_two_handed|itp_primary|itp_merchandise, itcf_carry_spear|itcf_reload_musket|itcf_shoot_musket,
     100000, weight(3.5) | difficulty(0)| spd_rtng(19) | shoot_speed(65) | thrust_damage(80, pierce) | accuracy(85) | max_ammo(1), imodbits_none],
##  ["m_hand_cannon_1_alt","Handgonne", [("rrr_arquebuse", 0), ("rrr_arquebuse_carry", ixmesh_carry)],itp_type_polearm|itp_two_handed|itp_primary|itp_cant_use_on_horseback|itp_wooden_parry ,itc_staff|itcf_carry_spear,                                                                          100000, weight(3.5) | difficulty(0)| spd_rtng(85) | swing_damage(20, blunt)| thrust_damage(15, blunt) | weapon_length(80),imodbits_polearm ],
    ["m_bullets", "Bullets", [("m_bullets",0), ("bullet_projectile",ixmesh_flying_ammo)], itp_type_bullets|itp_can_penetrate_shield|itp_merchandise|itp_default_ammo, itcf_carry_quiver_right_vertical,
     0,   weight(2.0) | abundance(90)| weapon_length(3) | thrust_damage(1, pierce) | max_ammo(6), imodbits_missile, [m_missile_init_trigger, m_bullet_hit_trigger]],
    #["m_bullets","Bullets", [("m_bullets", 0)], itp_type_bullets|itp_default_ammo|itp_covers_legs|itp_doesnt_cover_hair, 0,2000, weight(2)|abundance(90)|weapon_length(3)|max_ammo(12)|thrust_damage(1, pierce), imodbits_missile, []],


    # SCRIPTED ITEMS
    

    ["m_spike", "Spike", [("m_spike", 0)], itp_type_polearm|itp_cant_use_on_horseback|itp_primary|itp_wooden_parry|itp_two_handed|itp_merchandise, itc_cutting_spear|itcf_carry_spear,
     140, weight(2.0) | difficulty(0) | spd_rtng(95) | weapon_length(116) | swing_damage(15, blunt)  | thrust_damage(21, pierce), imodbits_polearm ],

##	["m_st_mak_standard_flag", "Flag", [("st_mak_standard_flag", 0),], itp_type_two_handed_wpn|itp_two_handed|itp_primary, 0,250, weight(3)|abundance(100)|weapon_length(220)|thrust_damage(0, pierce), imodbits_sword|imodbit_masterwork], #user Dagoth__Ur
    ["m_flag_1", "Flag", [("m_flag_1", 0),("m_flag_1_carry", ixmesh_carry)], itp_type_two_handed_wpn|itp_two_handed|itp_primary, 0,
      0, weight(3)|abundance(100)|weapon_length(245)|thrust_damage(0, pierce), imodbits_sword|imodbit_masterwork, [
        (ti_on_init_item, [
          (store_trigger_param_1, ":agent_no"),
          (store_trigger_param_2, ":troop_no"),
          (call_script, "script_shield_item_set_banner", "tableau_m_flag_1", ":agent_no", ":troop_no")
        ])
    ]],

    ["m_battle_horn", "Battle Horn", [("m_battle_horn", 0), ("m_battle_horn_carry", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_wooden_parry, itcf_carry_mace_left_hip,
     0, weight(1.0) | difficulty(0) | spd_rtng(0) | weapon_length(25) | swing_damage(0, cut) | thrust_damage(0, pierce), imodbits_axe ],

    ["m_warhorn", "Warhorn", [("warhorn_carry", 0), ("warhorn", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_wooden_parry|itp_no_pick_up_from_ground, itcf_carry_dagger_front_left,
     0, weight(1.0) | difficulty(0) | spd_rtng(0) | weapon_length(25) | swing_damage(0, cut) | thrust_damage(0, pierce), imodbits_axe ],

    	["m_snowballs", "Snowballs", [("m_snowball", 0), ("m_snowball_flying", ixmesh_flying_ammo), ("m_snowball_inv", ixmesh_inventory)], itp_type_thrown|itp_primary|itp_cant_use_on_horseback, itcf_throw_stone,
         0, weight(1) | difficulty(0) | spd_rtng(95) | shoot_speed(22) | thrust_damage(14, blunt) | max_ammo(20) | weapon_length(6), imodbit_large_bag, [m_missile_init_trigger, m_snowball_hit_trigger] ],

##	["m_banner", "Banner", [("pw_banner_pole", 0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary, 0,  250, weight(3.0)|weapon_length(250)|thrust_damage(0, pierce), imodbits_sword|imodbit_masterwork,[(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_banner_pole", ":agent_no", ":troop_no")])]],
##    ["m_flags_end","Flags End", [("shield_round_a", 0)], 0, 0, 0, 0, imodbits_none],


############################################################################ GOLD AND GLORY WEAPON END ############################################################################


    ["m_weapons_end", "Weapons End", [("invisible",0)], itp_type_one_handed_wpn, 0, 0 , weight(0)|abundance(0)|head_armor(0)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],


                 ############################### WEAPONS END #############################################33



    # MERCENARIES HEAD ARMORS 

##    ["m_pw_bishop_helm", "Bishop Helm", [("pw_bishop_helm",0)],  itp_type_head_armor|itp_covers_head, 0,                                                                0,    weight(5.75)| abundance(100) | head_armor(54)| body_armor(0)  | leg_armor(0)  | difficulty(0), imodbits_plate ],
    ["m_headcloth", "Headcloth", [("headcloth_a_new",0)],  itp_type_head_armor|itp_civilian|itp_merchandise, 0,                                                         8,    weight(0.0) | abundance(100) | head_armor(10) | body_armor(0) | leg_armor(0) | difficulty(0), imodbits_cloth ],
    ["m_woolen_cap", "Woolen Cap", [("woolen_cap_new",0)], itp_type_head_armor|itp_civilian|itp_merchandise, 0,                                                         10,   weight(0.0) | abundance(100) | head_armor(11) | body_armor(0) | leg_armor(0) | difficulty(0), imodbits_cloth ],
    ["m_felt_hat_1","Felt Hat", [("felt_hat_a_new", 0)], itp_type_head_armor|itp_civilian|itp_merchandise, 0,                                                           14,   weight(0.0) | abundance(100) | head_armor(12) | body_armor(0) | leg_armor(0) | difficulty(0), imodbits_cloth ],
    ["m_felt_hat_2","Felt Hat", [("felt_hat_b_new", 0)], itp_type_head_armor|itp_civilian|itp_merchandise, 0,                                                           15,   weight(0.0) | abundance(100) | head_armor(12) | body_armor(0) | leg_armor(0) | difficulty(0), imodbits_cloth ],
 
    ["m_common_hood", "Hood", [("hood_new", 0)], itp_type_head_armor|itp_civilian|itp_merchandise, 0,  #### MAIN
     30,   weight(0.0) | abundance(100) | head_armor(15) | body_armor(0) | leg_armor(0) | difficulty(0), imodbits_cloth ], 
    ["m_common_hood_dark", "Dark Hood", [("m_hood_dark", 0)], itp_type_head_armor|itp_civilian|itp_merchandise, 0, #### EXTRA
     5,   weight(0.0) | abundance(100) | head_armor(15) | body_armor(0) | leg_armor(0) | difficulty(0), imodbits_cloth ],
    ["m_green_hood_2", "Green Hood", [("zimke_pelt_hood", 0)], itp_type_head_armor|itp_civilian, 0, #### EXTRA
     5,   weight(0.0) | abundance(100) | head_armor(15) | body_armor(0) | leg_armor(0) | difficulty(0), imodbits_cloth ],


    ["m_green_hood", "Green Hood", [("zimke_pelt_hood", 0)], itp_type_head_armor|itp_civilian, 0,                              ####MOD
     0,   weight(0.0) | abundance(100) | head_armor(15) | body_armor(0) | leg_armor(0) | difficulty(0), imodbits_cloth ],

    ["m_arming_cap", "Arming Cap", [("arming_cap_a_new", 0)],  itp_type_head_armor  |itp_civilian|itp_merchandise, 0,                                                   60,   weight(0.0) | abundance(100) | head_armor(15) | body_armor(0) | leg_armor(0) | difficulty(0), imodbits_cloth ],

    ["m_turban", "Turban", [("tuareg_open", 0)],  itp_type_head_armor|itp_merchandise, 0,  #### MAIN
     120,  weight(0.25)| abundance(100) | head_armor(18) | body_armor(0) | leg_armor(0) | difficulty(0), imodbits_cloth ], 
    ["m_turban_black", "Black Turban", [("tuareg_open_black", 0)],  itp_type_head_armor|itp_merchandise, 0,  #### EXTRA
     10,  weight(0.25)| abundance(100) | head_armor(18) | body_armor(0) | leg_armor(0) | difficulty(0), imodbits_cloth ], 

    ["m_desert_turban", "Desert Turban", [("tuareg", 0)],  itp_type_head_armor|itp_covers_beard|itp_merchandise, 0,                                                     150,  weight(0.25)| abundance(100) | head_armor(18) | body_armor(0) | leg_armor(0) | difficulty(0), imodbits_cloth ], 
    ["m_hood_masked_1", "Assassin's Hood", [("hood_masked_1", 0)], itp_type_head_armor|itp_covers_beard|itp_civilian|itp_merchandise, 0,                                190,  weight(0.25)| abundance(100) | head_armor(18) | body_armor(0) | leg_armor(0) | difficulty(0), imodbits_cloth ], 

    ["m_hood_masked_2", "Black Hood with Mask", [("hood_masked_2", 0)], itp_type_head_armor|itp_covers_beard|itp_civilian|itp_merchandise, 0,  ### MAIN
     200,  weight(0.25)| abundance(100) | head_armor(18) | body_armor(0) | leg_armor(0) | difficulty(0), imodbits_cloth ], 
    ["m_hood_masked_2_white", "White Hood with Mask", [("hood_masked_2_white", 0)], itp_type_head_armor|itp_covers_beard|itp_civilian|itp_merchandise, 0, ### EXTRA
     10,  weight(0.25)| abundance(100) | head_armor(18) | body_armor(0) | leg_armor(0) | difficulty(0), imodbits_cloth ], 

    ["m_sarranid_felt_hat","Sarranid Felt Hat", [("sar_helmet3", 0)], itp_type_head_armor|itp_merchandise, 0,                                                           230,  weight(0.25)| abundance(100) | head_armor(18) | body_armor(0) | leg_armor(0) | difficulty(0), imodbits_cloth ],

    ["m_leather_cap", "Leather Cap", [("leather_cap_a_new",0)],  itp_type_head_armor|itp_civilian|itp_merchandise, 0,   #### MAIN
     250,  weight(0.25)| abundance(100) | head_armor(18) | body_armor(0) | leg_armor(0) | difficulty(0), imodbits_cloth ],
    ["gg_leather_cap_a_new", "Leather Cap", [("gg_leather_cap_a_new",0)], itp_merchandise| itp_type_head_armor| itp_civilian ,0,    #### EXTRA
      10, weight(1)|abundance(100)|head_armor(18)|body_armor(0)|leg_armor(0)|difficulty(0),imodbits_cloth],

    ["m_leather_steppe_cap_a", "Steppe Fur Cap", [("leather_steppe_cap_a_new",0)], itp_type_head_armor|itp_merchandise, 0,  #### MAIN
     270,  weight(0.5) | abundance(100) | head_armor(21) | body_armor(0) | leg_armor(0) | difficulty(0), imodbits_cloth ],
    ["gg_leather_steppe_cap_a_new", "Steppe Cap", [("gg_leather_steppe_cap_a_new",0)], itp_merchandise| itp_type_head_armor| itp_civilian ,0,   #### EXTRA
    10, weight(1)|abundance(100)|head_armor(21)|body_armor(0)|leg_armor(0)|difficulty(0),imodbits_cloth],

    ["m_leather_steppe_cap_b", "Steppe Leather Cap ", [("tattered_steppe_cap_b_new", 0)], itp_type_head_armor|itp_merchandise, 0,    290,  weight(0.5) | abundance(100) | head_armor(21) | body_armor(0) | leg_armor(0) | difficulty(0), imodbits_cloth ], 
    ["m_nomad_cap_b", "Nomad Leather Cap", [("nomad_cap_b_new",0)], itp_type_head_armor|itp_civilian|itp_merchandise,0,                                                 300,  weight(0.5) | abundance(100) | head_armor(21) | body_armor(0) | leg_armor(0) | difficulty(0), imodbits_cloth ],
    # ["m_h_h2_1", "Scottish Barret", [("h_h2_1",0)], itp_type_head_armor|itp_merchandise|itp_attach_armature,0,                                                          390,  weight(0.5) | abundance(100) | head_armor(21) | body_armor(0) | leg_armor(0) | difficulty(0), imodbits_plate ],
    ["m_skullcap", "Skullcap", [("skull_cap_new_a", 0)],  itp_type_head_armor|itp_merchandise, 0,                                                                       410,  weight(0.75)| abundance(100) | head_armor(24) | body_armor(0) | leg_armor(0) | difficulty(7), imodbits_plate ], 
    ["m_leather_warrior_cap", "Leather Warrior Cap", [("skull_cap_new_b", 0)], itp_type_head_armor|itp_civilian|itp_merchandise, 0,                                     500,  weight(0.75)| abundance(100) | head_armor(25) | body_armor(0) | leg_armor(0) | difficulty(7), imodbits_cloth ],

    ["m_sarranid_warrior_cap","Desert Warrior Cap", [("tuareg_helmet", 0)], itp_type_head_armor|itp_covers_beard|itp_merchandise, 0, ### MAIN
     600,  weight(1.0) | abundance(100) | head_armor(27) | body_armor(0) | leg_armor(0) | difficulty(7), imodbits_plate ],
    ["m_sarranid_warrior_cap_black", "Black Desert Warrior Cap", [("tuareg_helmet_black", 0)], itp_type_head_armor|itp_covers_beard|itp_merchandise, 0, ### EXTRA
     10,  weight(1.0) | abundance(100) | head_armor(27) | body_armor(0) | leg_armor(0) | difficulty(7), imodbits_plate ],

    ["m_nomad_cap", "Nomad Fur Cap", [("nomad_cap_a_new",0)], itp_type_head_armor|itp_civilian|itp_merchandise, 0,                                                      700,  weight(1.0) | abundance(100) | head_armor(27) | body_armor(0) | leg_armor(0) | difficulty(7), imodbits_cloth ],
    ["m_nordic_archer_helmet", "Nordic Light Leather Helmet", [("Helmet_A_vs2", 0)],  itp_type_head_armor|itp_merchandise, 0,                                           800,  weight(1.0) | abundance(100) | head_armor(27) | body_armor(0) | leg_armor(0) | difficulty(7), imodbits_plate ],
    ["m_steppe_cap", "Steppe Fur Cap", [("steppe_cap_a_new",0)], itp_type_head_armor|itp_civilian|itp_merchandise, 0,                                                   850,  weight(1.25)| abundance(100) | head_armor(30) | body_armor(0) | leg_armor(0) | difficulty(8), imodbits_cloth ],
    ["m_nordic_veteran_archer_helmet", "Nordic Leather Helmet", [("Helmet_A", 0)],  itp_type_head_armor|itp_merchandise, 0,                                             910,  weight(1.25)| abundance(100) | head_armor(30) | body_armor(0) | leg_armor(0) | difficulty(8), imodbits_plate ], 
    ["m_cervelliere", "Cervelliere", [("fred_cervelliere", 0)],  itp_type_head_armor|itp_merchandise, 0,                                                                970,  weight(1.25)| abundance(100) | head_armor(30) | body_armor(0) | leg_armor(0) | difficulty(8), imodbits_plate ], 
    ["m_mail_coif", "Mail Coif", [("mail_coif_new", 0)],  itp_type_head_armor|itp_merchandise, 0,                                                                       1125, weight(1.5) | abundance(100) | head_armor(32) | body_armor(0) | leg_armor(0) | difficulty(8), imodbits_armor ], 
    # ["m_coif", "Mail Coif", [("coif",0)],  itp_type_head_armor|itp_covers_beard|itp_merchandise, 0,                                                                     1200, weight(1.5) | abundance(100) | head_armor(32) | body_armor(0) | leg_armor(0) | difficulty(8), imodbits_plate ],
    ["m_vaegir_fur_cap", "Cap with Fur", [("vaeg_helmet3", 0)],  itp_type_head_armor|itp_merchandise, 0,                                                                1250, weight(1.5) | abundance(100) | head_armor(32) | body_armor(0) | leg_armor(0) | difficulty(9), imodbits_plate ], 

    ["m_sarranid_helmet1", "Keffiyeh Helmet", [("sar_helmet1", 0)],  itp_type_head_armor|itp_merchandise, 0,  #### MAIN
     1350, weight(1.5) | abundance(100) | head_armor(32) | body_armor(0) | leg_armor(0) | difficulty(9), imodbits_plate ], 
    ["m_sarranid_helmet1_black", "Black Keffiyeh Helmet", [("sar_helmet1_black", 0)],  itp_type_head_armor|itp_merchandise, 0,  #### EXTRA
     100, weight(1.5) | abundance(100) | head_armor(32) | body_armor(0) | leg_armor(0) | difficulty(9), imodbits_plate ], 

    # ["m_bascinet_rusty", "Rusty Bascinet", [("bascinet_avt_new1",0)], itp_type_head_armor|itp_merchandise, 0,                                                           1430, weight(1.5) | abundance(100) | head_armor(32) | body_armor(0) | leg_armor(0) | difficulty(9), imodbits_plate ],
    ["m_bascinet_banded", "Bascinet", [("bascinet_avt_new",0)], itp_type_head_armor|itp_merchandise, 0,                                                                 1430, weight(1.5) | abundance(100) | head_armor(32) | body_armor(0) | leg_armor(0) | difficulty(9), imodbits_plate ],
    # ["m_bascinet", "Bascinet", [("bascinet_avt_new2",0)], itp_type_head_armor|itp_merchandise, 0,                                                                       1430, weight(1.5) | abundance(100) | head_armor(32) | body_armor(0) | leg_armor(0) | difficulty(9), imodbits_plate ],
    ["m_segmented_helmet", "Segmented Helmet", [("segmented_helm_new", 0)],  itp_type_head_armor|itp_merchandise, 0,                                                    1500, weight(1.75)| abundance(100) | head_armor(34) | body_armor(0) | leg_armor(0) | difficulty(9), imodbits_plate ], 
    ["m_footman_helmet", "Footman Helmet", [("skull_cap_new", 0)],  itp_type_head_armor|itp_merchandise, 0,                                                             1600, weight(1.75)| abundance(100) | head_armor(34) | body_armor(0) | leg_armor(0) | difficulty(9), imodbits_plate ],

    ["m_keffiyeh_helmet_1", "Purple Keffiyeh Helmet", [("cwe_securiti_crysader_helm_a", 0),("cwe_securiti_crysader_helm_a_marcet", ixmesh_inventory)], itp_type_head_armor|itp_attach_armature|itp_merchandise, 0,  #### MAIN
     1700, weight(1.75) | abundance(100) | head_armor(34) | body_armor(0) | leg_armor(0) | difficulty(9), imodbits_plate],
    ["m_keffiyeh_helmet_2", "Purple Keffiyeh Nasal Helmet", [("cwe_securiti_crysader_helm_b", 0),("cwe_securiti_crysader_helm_b_marcet", ixmesh_inventory)], itp_type_head_armor|itp_attach_armature|itp_merchandise, 0,  #### EXTRA
     200, weight(1.75) | abundance(100) | head_armor(34) | body_armor(0) | leg_armor(0) | difficulty(9), imodbits_plate],
    ["gulam_helm_b_market", "Reinforced Red Keffiyeh Helmet", [("gulam_helm_b_market", 0)],  itp_type_head_armor|itp_merchandise, 0,  ### Extra
     500, weight(1.8)| abundance(100) | head_armor(35) | body_armor(0) | leg_armor(0) | difficulty(9), imodbits_armor ],


    ["m_chapel_de_fer", "Iron Hat", [("chapel_de_fer", 0)],  itp_type_head_armor|itp_merchandise, 0,                                                                    1800, weight(2.0) | abundance(100) | head_armor(35) | body_armor(0) | leg_armor(0) | difficulty(9), imodbits_plate ],
    ["m_helmet_with_neckguard", "Helmet with Neckguard", [("neckguard_helm_new", 0)],  itp_type_head_armor|itp_merchandise, 0,                                          1850, weight(2.0) | abundance(100) | head_armor(36) | body_armor(0) | leg_armor(0) | difficulty(10),imodbits_plate ], 

    ["m_narf_chapel_de_fer_cloth2", "Kettle Hat", [("narf_chapel_de_fer_cloth2",0), ("narf_inv_chapel_de_fer_cloth2",ixmesh_inventory)], itp_merchandise|itp_type_head_armor|itp_attach_armature, 0,   #### MAIN
     1900, weight(2.0) | abundance(100) | head_armor(36) | body_armor(0) | leg_armor(0) | difficulty(10), imodbits_plate ],
    ["m_narf_chapel_de_fer_cloth3", "Kettle Hat", [("narf_chapel_de_fer_cloth3",0), ("narf_inv_chapel_de_fer_cloth3",ixmesh_inventory)], itp_merchandise|itp_type_head_armor|itp_attach_armature, 0,   #### EXTRA
     200, weight(2.0) | abundance(100) | head_armor(36) | body_armor(0) | leg_armor(0) | difficulty(10), imodbits_plate ],
    ["m_narf_chapel_de_fer_cloth1", "Kettle Hat", [("narf_chapel_de_fer_cloth1",0), ("narf_inv_chapel_de_fer_cloth1",ixmesh_inventory)], itp_merchandise|itp_type_head_armor|itp_attach_armature, 0,   #### EXTRA
     200, weight(2.0) | abundance(100) | head_armor(36) | body_armor(0) | leg_armor(0) | difficulty(10), imodbits_plate ],
    ["m_narf_chapel_de_fer_wreath1", "Kettle Hat with Wreath", [("narf_chapel_de_fer_wreath1",0), ("narf_inv_chapel_de_fer_wreath1",ixmesh_inventory)], itp_type_head_armor|itp_attach_armature, 0,   #### EXTRA
     200, weight(2.0) | abundance(100) | head_armor(36) | body_armor(0) | leg_armor(0) | difficulty(10), imodbits_plate ],

    # ["m_saracen_archer_helmet", "Saracen Archer Helmet", [("saracen_archer_helmet", 0)],  itp_type_head_armor|itp_covers_beard|itp_attach_armature|itp_merchandise, 0,  2100, weight(2.0) | abundance(100) | head_armor(36) | body_armor(0) | leg_armor(0) | difficulty(10), imodbits_plate ],
    ["m_nasal_helmet", "Nasal Helmet", [("nasal_helmet_b", 0)],  itp_type_head_armor|itp_covers_beard|itp_merchandise, 0,                                               2150, weight(2.0) | abundance(100) | head_armor(36) | body_armor(0) | leg_armor(0) | difficulty(10), imodbits_plate ],
    ["m_nordic_helmet", "Nordic Helmet", [("helmet_w_eyeguard_new", 0)],  itp_type_head_armor|itp_merchandise, 0,                                                       2400, weight(2.0) | abundance(100) | head_armor(36) | body_armor(0) | leg_armor(0) | difficulty(10), imodbits_plate ],
    ["m_spiked_helmet", "Spiked Helmet", [("spiked_helmet_new", 0)],  itp_type_head_armor|itp_merchandise, 0,                                                           2440, weight(2.25)| abundance(100) | head_armor(37) | body_armor(0) | leg_armor(0) | difficulty(11), imodbits_plate ],
    ["m_khergit_war_helmet", "Khergit War Helmet", [("tattered_steppe_cap_a_new", 0)], itp_type_head_armor|itp_merchandise, 0,                                          2450, weight(2.25)| abundance(100) | head_armor(38) | body_armor(0) | leg_armor(0) | difficulty(12), imodbits_cloth ],
    ["m_nordic_footman_helmet", "Nordic Footman Helmet", [("Helmet_B_vs2", 0)], itp_type_head_armor|itp_fit_to_head|itp_merchandise, 0,                                 2500, weight(2.25)| abundance(100) | head_armor(38) | body_armor(0) | leg_armor(0) | difficulty(12), imodbits_plate ],
    ["m_khergit_cavalry_helmet", "Khergit Cavalry Helmet", [("lamellar_helmet_b",0)], itp_type_head_armor|itp_merchandise, 0,     2700, weight(2.25)| abundance(100) | head_armor(38) | body_armor(0) | leg_armor(0) | difficulty(12), imodbits_cloth ],
    ["m_sarranid_horseman_helmet", "Sarranid Horseman Helmet", [("sar_helmet2", 0)],  itp_type_head_armor|itp_merchandise, 0,                                           2800, weight(2.5) | abundance(100) | head_armor(39) | body_armor(0) | leg_armor(0) | difficulty(13), imodbits_plate ],


    ["m_vaegir_spiked_helmet1", "Spiked Helmet", [("vaeg_helmet1", 0)],  itp_type_head_armor|itp_merchandise, 0,  ##### MAIN
     2850, weight(2.5) | abundance(100) | head_armor(39) | body_armor(0) | leg_armor(0) | difficulty(13), imodbits_plate ],
    ["m_vaegir_spiked_helmet5", "Cupped Helmet", [("vaeg_helmet5", 0)],  itp_type_head_armor|itp_merchandise, 0,  #### EXTRA
     200, weight(2.5) | abundance(100) | head_armor(39) | body_armor(0) | leg_armor(0) | difficulty(13), imodbits_plate ],

    ["m_vaegir_fur_helmet", "Fur Helmet with Mail Guard", [("vaeg_helmet2", 0)],  itp_type_head_armor|itp_merchandise, 0,                                               3000, weight(2.5) | abundance(100) | head_armor(39) | body_armor(0) | leg_armor(0) | difficulty(13), imodbits_plate ],
    ["m_nordic_fighter_helmet", "Nordic Fighter Helmet", [("Helmet_B", 0)],  itp_type_head_armor|itp_fit_to_head|itp_merchandise, 0,                                    3100, weight(2.5) | abundance(100) | head_armor(39) | body_armor(0) | leg_armor(0) | difficulty(13), imodbits_plate ],
    ["m_skutatos_helmet", "Helmet with Scale Guard", [("zimke_skutatos_helmet", 0),("zimke_skutatos_helmet_inv", ixmesh_inventory)],  itp_type_head_armor|itp_attach_armature|itp_merchandise, 0,                         3150, weight(2.75)| abundance(100) | head_armor(40) | body_armor(0) | leg_armor(0) | difficulty(14), imodbits_plate ],
    ["m_vaegir_lamellar_helmet", "Fur Helmet with Lamellar Guard", [("vaeg_helmet4", 0)],  itp_type_head_armor|itp_merchandise, 0,                                      3200, weight(2.75)| abundance(100) | head_armor(40) | body_armor(0) | leg_armor(0) | difficulty(14), imodbits_plate ],
    ["m_khergit_guard_helmet", "Khergit Lamellar Helmet", [("lamellar_helmet_a", 0)], itp_type_head_armor|itp_merchandise, 0,                                           3300, weight(2.75)| abundance(100) | head_armor(40) | body_armor(0) | leg_armor(0) | difficulty(14), imodbits_cloth ],
    ["m_keffiyeh_helmet_3", "Red Keffiyeh Helmet", [("cwe_gulam_helm_d", 0),("cwe_gulam_helm_d_market", ixmesh_inventory)], itp_type_head_armor|itp_attach_armature|itp_merchandise, 0,                                   3350, weight(2.75)| abundance(100) | head_armor(40) | body_armor(0) | leg_armor(0) | difficulty(14), imodbits_plate ],

    ["m_guard_helmet", "Guard Helmet", [("reinf_helmet_new", 0)],  itp_type_head_armor|itp_merchandise, 0,   ### MAIN
     3400, weight(3.0) | abundance(100) | head_armor(41) | body_armor(0) | leg_armor(0) | difficulty(14), imodbits_plate ],
    ["gg_guard_helmet_red", "Guard Helmet Red", [("gg_guard_helmet_red", 0)],  itp_type_head_armor|itp_merchandise, 0,    ### EXTRA
     100, weight(3.0) | abundance(100) | head_armor(41) | body_armor(0) | leg_armor(0) | difficulty(14), imodbits_plate ],
    ["gg_guard_helmet_blue", "Guard Helmet Blue", [("gg_guard_helmet_blue", 0)],  itp_type_head_armor|itp_merchandise, 0,    ### EXTRA
     100, weight(3.0) | abundance(100) | head_armor(41) | body_armor(0) | leg_armor(0) | difficulty(14), imodbits_plate ],
    ["gg_guard_helmet_green", "Guard Helmet Green", [("gg_guard_helmet_green", 0)],  itp_type_head_armor|itp_merchandise, 0,    ### EXTRA
     100, weight(3.0) | abundance(100) | head_armor(41) | body_armor(0) | leg_armor(0) | difficulty(14), imodbits_plate ],

    ["cwe_city_watch_helmet", "City Watch Helmet", [("cwe_city_watch_helmet", 0)],  itp_type_head_armor|itp_merchandise, 0,   
      4000, weight(3.3) | abundance(100) | head_armor(43) | body_armor(0) | leg_armor(0) | difficulty(15), imodbits_plate ],


    ["m_kettle_hat", "Reinforced Kettle Hat", [("kettle_hat_new", 0)],  itp_type_head_armor|itp_merchandise, 0,  #### MAIN
     3500, weight(3.25)| abundance(100) | head_armor(42) | body_armor(0) | leg_armor(0) | difficulty(14), imodbits_plate ],
    ["gg_kettle_red", "Reinforced Kettle Hat Red", [("gg_kettle_red", 0)],  itp_type_head_armor|itp_merchandise, 0,   #### EXTRA
     100, weight(3.25)| abundance(100) | head_armor(42) | body_armor(0) | leg_armor(0) | difficulty(14), imodbits_plate ],
    ["gg_kettle_green", "Reinforced Kettle Hat Green", [("gg_kettle_green", 0)],  itp_type_head_armor|itp_merchandise, 0,  #### EXTRA
     100, weight(3.25)| abundance(100) | head_armor(42) | body_armor(0) | leg_armor(0) | difficulty(14), imodbits_plate ],    
    ["gg_kettle_blue", "Reinforced Kettle Hat Blue", [("gg_kettle_blue", 0)],  itp_type_head_armor|itp_merchandise, 0,  #### EXTRA
     100, weight(3.25)| abundance(100) | head_armor(42) | body_armor(0) | leg_armor(0) | difficulty(14), imodbits_plate ],
    ["gg_kettle_yellow", "Reinforced Kettle Hat Yellow", [("gg_kettle_yellow", 0)],  itp_type_head_armor|itp_merchandise, 0,  #### EXTRA
     100, weight(3.25)| abundance(100) | head_armor(42) | body_armor(0) | leg_armor(0) | difficulty(14), imodbits_plate ],

    ["turbmail", "Turban with Mail", [("turbmail", 0)],  itp_type_head_armor|itp_merchandise, 0,  #### MAIN
     3550, weight(3.25)| abundance(100) | head_armor(42) | body_armor(0) | leg_armor(0) | difficulty(14), imodbits_plate ],   


    ["m_nordic_huscarl_helmet", "Nordic Huscarl's Helmet", [("Helmet_C_vs2", 0)],  itp_type_head_armor|itp_merchandise, 0,                                              3600, weight(3.25)| abundance(100) | head_armor(42) | body_armor(0) | leg_armor(0) | difficulty(14), imodbits_plate ],
    ["m_vaegir_spiked_helmet", "Vaegir Guard Helmet", [("rus_helm", 0)],  itp_type_head_armor|itp_merchandise, 0,                                                       3700, weight(3.25)| abundance(100) | head_armor(42) | body_armor(0) | leg_armor(0) | difficulty(14), imodbits_plate ],
    ["m_byzantion_helmet", "Bell-Shaped Helmet", [("dejawolf_byzantion_2", 0)], itp_type_head_armor|itp_merchandise, 0,                                                 3750, weight(3.25)| abundance(100) | head_armor(42) | body_armor(0) | leg_armor(0) | difficulty(14), imodbits_plate ],
    ["m_mongolian_helmet", "Khergit Elite Helmet", [("zimke_mongolian_helmet", 0),("zimke_mongolian_helmet_inv", ixmesh_inventory)], itp_type_head_armor|itp_attach_armature|itp_merchandise, 0,                          3800, weight(3.25)| abundance(100) | head_armor(42) | body_armor(0) | leg_armor(0) | difficulty(14), imodbits_plate ],
    ["m_vaegir_noble_helmet_e", "Vaegir Open Spiked Helmet", [("tagancha_helm_a", 0)],  itp_type_head_armor|itp_merchandise, 0,                                         3900, weight(3.25)| abundance(100) | head_armor(42) | body_armor(0) | leg_armor(0) | difficulty(14), imodbits_plate ],

    ["m_narf_sallet_cloth", "Short-Tailed Sallet", [("narf_salet_cloth", 0)], itp_type_head_armor|itp_attach_armature|itp_merchandise, 0,
     3950, weight(3.25)| abundance(100) | head_armor(42) | body_armor(0) | leg_armor(0) | difficulty(14), imodbits_plate ],
    ["m_narf_sallet_mask", "Short-Tailed Sallet with Mask", [("narf_salet_mask", 0)], itp_type_head_armor|itp_attach_armature|itp_covers_beard, 0,
     200, weight(3.25)| abundance(100) | head_armor(42) | body_armor(0) | leg_armor(0) | difficulty(14), imodbits_plate ],
    ["m_narf_sallet_mask_black", "Short-Tailed Sallet with Black Mask", [("narf_salet_mask_black", 0)], itp_type_head_armor|itp_attach_armature|itp_covers_beard, 0,
     200, weight(3.25)| abundance(100) | head_armor(42) | body_armor(0) | leg_armor(0) | difficulty(14), imodbits_plate ],
    ["m_narf_sallet_wreath", "Short-Tailed Sallet with Wreath", [("narf_salet_wreath", 0)], itp_type_head_armor|itp_attach_armature, 0,
     200, weight(3.25)| abundance(100) | head_armor(42) | body_armor(0) | leg_armor(0) | difficulty(14), imodbits_plate ],

    # ["m_masked_sallet", "Short-Tailed Sallet with Mask", [("m_masked_sallet", 0)], itp_type_head_armor|itp_covers_beard|itp_merchandise, 0,                             3970, weight(3.25)| abundance(100) | head_armor(42) | body_armor(0) | leg_armor(0) | difficulty(14), imodbits_plate ],

    ["m_flat_topped_helmet", "Flat Topped Helmet", [("m_flattop_helmet", 0)],  itp_type_head_armor|itp_merchandise, 0,  #### MAIN 
     4000, weight(3.5) | abundance(100) | head_armor(43) | body_armor(0) | leg_armor(0) | difficulty(15), imodbits_plate ],
    ["m_flat_topped_helmet_c", "Colored Flat Topped Helmet", [("m_flattop_helmet_c", 0)],  itp_type_head_armor|itp_merchandise, 0,   #### EXTRA
     400, weight(3.5) | abundance(100) | head_armor(43) | body_armor(0) | leg_armor(0) | difficulty(15), imodbits_plate, [ (ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_m_flattop_helmet_c", ":agent_no", ":troop_no")]) ] ],

    ["m_kettle_hat_4", "Round Kettle Hat", [("dejawolf_kettlehat_1", 0)],  itp_type_head_armor|itp_merchandise, 0,                                                      4150, weight(3.5) | abundance(100) | head_armor(43) | body_armor(0) | leg_armor(0) | difficulty(15), imodbits_plate ],
    ["m_kettle_hat_4_c", "Round White Kettle Hat", [("dejawolf_kettlehat_1_c", 0)],  itp_type_head_armor|itp_merchandise, 0,                                            4160, weight(3.5) | abundance(100) | head_armor(43) | body_armor(0) | leg_armor(0) | difficulty(15), imodbits_plate ],
    ["m_kettle_hat_3", "Cylindrical Kettle Hat", [("dejawolf_kettlehat_2", 0)],  itp_type_head_armor|itp_merchandise, 0,                                                4170, weight(3.5) | abundance(100) | head_armor(43) | body_armor(0) | leg_armor(0) | difficulty(15), imodbits_plate ],
    ["m_kettle_hat_3_c", "Cylindrical Blue Kettle Hat", [("dejawolf_kettlehat_2_c", 0)],  itp_type_head_armor|itp_merchandise, 0,                                       4180, weight(3.5) | abundance(100) | head_armor(43) | body_armor(0) | leg_armor(0) | difficulty(15), imodbits_plate ],
    ["m_norman_helmet_3", "Conical Helmet", [("dejanarf_norman_helmet_1", 0),("dejanarf_norman_helmet_1_inv", ixmesh_inventory)],  itp_type_head_armor|itp_attach_armature|itp_merchandise, 0,                            4200, weight(3.5) | abundance(100) | head_armor(43) | body_armor(0) | leg_armor(0) | difficulty(15), imodbits_plate ],

    ["m_clibanarius_helmet", "One-Piece Brimmed Helmet", [("zimke_clibanarius_helmet",0),("zimke_clibanarius_helmet_inv", ixmesh_inventory)],  itp_type_head_armor|itp_attach_armature|itp_merchandise, 0, ### MAIN
     4250, weight(3.5) | abundance(100) | head_armor(43) | body_armor(0) | leg_armor(0) | difficulty(15), imodbits_plate ],
    ["m_byzantine_helmet_a", "Engraved Brimmed Helmet", [("zimke_byzantine_helmet_a",0),("zimke_byzantine_helmet_a_inv", ixmesh_inventory)],  itp_type_head_armor|itp_attach_armature|itp_merchandise, 0,  ### EXTRA
     200, weight(3.5) | abundance(100) | head_armor(43) | body_armor(0) | leg_armor(0) | difficulty(15), imodbits_plate ],
    ["m_byzantine_helmet_a_red", "Red Brimmed Helmet", [("zimke_byzantine_helmet_a_red",0), ("zimke_byzantine_helmet_a_red_inv", ixmesh_inventory)],  itp_type_head_armor|itp_attach_armature|itp_merchandise, 0,  ### EXTRA
     200, weight(3.5) | abundance(100) | head_armor(43) | body_armor(0) | leg_armor(0) | difficulty(15), imodbits_plate ],

    ["m_norman_helmet_1", "Fluted Helmet", [("gg_almansur_fluted_helmet", 0)],  itp_type_head_armor|itp_covers_beard|itp_merchandise, 0,                                   4350, weight(3.75)| abundance(100) | head_armor(44) | body_armor(0) | leg_armor(0) | difficulty(15), imodbits_plate ],
    ["m_norman_helmet_2", "Cylindrical Helmet", [("gg_almansur_flat_helmet", 0)],  itp_type_head_armor|itp_covers_beard|itp_merchandise, 0,
     4400, weight(3.75)| abundance(100) | head_armor(44) | body_armor(0) | leg_armor(0) | difficulty(15), imodbits_plate ],
    ["m_narf_chapel_de_fer_mail2", "Kettle Hat with Long Mail Guard", [("narf_chapel_de_fer_mail2",0), ("narf_inv_chapel_de_fer_mail2",ixmesh_inventory)], itp_merchandise|itp_type_head_armor|itp_attach_armature, 0,    4450, weight(3.75) | abundance(100) | head_armor(44) | body_armor(0) | leg_armor(0) | difficulty(15), imodbits_plate ],
    ["m_narf_chapel_de_fer_mail3", "Kettle Hat with Long Mail Guard", [("narf_chapel_de_fer_mail3",0), ("narf_inv_chapel_de_fer_mail3",ixmesh_inventory)], itp_merchandise|itp_type_head_armor|itp_attach_armature, 0,    4500, weight(3.75) | abundance(100) | head_armor(44) | body_armor(0) | leg_armor(0) | difficulty(15), imodbits_plate ],
    ["m_narf_chapel_de_fer_mail1", "Kettle Hat with Long Mail Guard", [("narf_chapel_de_fer_mail1",0), ("narf_inv_chapel_de_fer_mail1",ixmesh_inventory)], itp_merchandise|itp_type_head_armor|itp_attach_armature, 0,    4550, weight(3.75) | abundance(100) | head_armor(44) | body_armor(0) | leg_armor(0) | difficulty(15), imodbits_plate ],
    ["m_prato_chapel_de_fer", "Kettle Hat with High Top Point", [("prato_chapel_de_fer",0)],  itp_type_head_armor|itp_merchandise, 0,                                   4580, weight(3.75)| abundance(100) | head_armor(44) | body_armor(0) | leg_armor(0) | difficulty(15), imodbits_plate ],
    ["m_brimmed_helmet_a", "Engraved Bell-Shaped Helmet", [("zimke_brimmed_helmet_a",0),("zimke_brimmed_helmet_a_inv", ixmesh_inventory)],  itp_type_head_armor|itp_attach_armature|itp_merchandise, 0,                   4650, weight(3.75)| abundance(100) | head_armor(44) | body_armor(0) | leg_armor(0) | difficulty(15), imodbits_plate ],
    # ["m_brimmed_helmet_b", "Masked Engraved Bell-Shaped Helmet", [("brimmed_helmet_b",0)],  itp_type_head_armor|itp_attach_armature|itp_covers_beard, 0,                                                                  4650, weight(4.25)| abundance(100) | head_armor(46) | body_armor(0) | leg_armor(0) | difficulty(17), imodbits_plate ],
    ["m_eng_varangian_helmet", "Reinforced Brimmed Helmet", [("zimke_eng_varangian_helmet",0), ("zimke_eng_varangian_helmet_inv", ixmesh_inventory)],  itp_type_head_armor|itp_attach_armature|itp_merchandise, 0,    4700, weight(4.0)  | abundance(100) | head_armor(45) | body_armor(0) | leg_armor(0) | difficulty(16), imodbits_plate ],
    ["m_vaegir_war_helmet", "Veiled Helmet", [("vaeg_helmet6", 0)],  itp_type_head_armor|itp_merchandise, 0,                                                            4750, weight(4.0) | abundance(100) | head_armor(45) | body_armor(0) | leg_armor(0) | difficulty(16), imodbits_plate ],
    ["m_sarranid_veiled_helmet", "Sarranid Veiled Helmet", [("sar_helmet4", 0)],  itp_type_head_armor | itp_covers_beard|itp_merchandise, 0,
     6030, weight(4.8) | abundance(100) | head_armor(48) | body_armor(0) | leg_armor(0) | difficulty(18), imodbits_plate ],

    ["m_vaegir_mask1", "Open War Mask", [("vaeg_helmet8", 0)],  itp_type_head_armor|itp_merchandise, 0, 
     4900, weight(4.0) | abundance(100) | head_armor(45) | body_armor(0) | leg_armor(0) | difficulty(16), imodbits_plate ],

    # ["m_fi_nasal_helmet_1", "Nasal Helmet", [("fi_nasal_helmet_1",0)],  itp_type_head_armor|itp_merchandise, 0,                                                         4970, weight(4.0) | abundance(100) | head_armor(45) | body_armor(0) | leg_armor(0) | difficulty(16), imodbits_plate ],
    ["m_vaegir_noble_helmet_c", "Vaegir Veiled Helmet", [("novogrod_helm", 0)],  itp_type_head_armor|itp_covers_beard|itp_merchandise, 0,                               5000, weight(4.0) | abundance(100) | head_armor(45) | body_armor(0) | leg_armor(0) | difficulty(16), imodbits_plate ],
    ["warlords_vaegir_noble_helmet_c_dark1", "Vaegir Veiled Helmet", [("warlords_novogrod_helm_dark1", 0)],  itp_type_head_armor|itp_covers_beard|itp_merchandise, 0,                               500, weight(4.0) | abundance(100) | head_armor(45) | body_armor(0) | leg_armor(0) | difficulty(16), imodbits_plate ],
    ["warlords_vaegir_noble_helmet_c_dark2", "Vaegir Veiled Helmet", [("warlords_novogrod_helm_dark2", 0)],  itp_type_head_armor|itp_covers_beard|itp_merchandise, 0,                               500, weight(4.0) | abundance(100) | head_armor(45) | body_armor(0) | leg_armor(0) | difficulty(16), imodbits_plate ],

    ["m_bascinet_2", "Bascinet with Aventail", [("bascinet_new_a", 0)], itp_type_head_armor|itp_merchandise, 0,   #### MAIN
     5100, weight(4.0) | abundance(100) | head_armor(45) | body_armor(0) | leg_armor(0) | difficulty(16), imodbits_plate ],
    ["m_bascinet_3", "Bascinet with Nose Guard", [("bascinet_new_b", 0)], itp_type_head_armor, 0,    #### EXTRA
     600, weight(4.25)| abundance(100) | head_armor(46) | body_armor(0) | leg_armor(0) | difficulty(17), imodbits_plate ],

    ["m_nordic_warlord_helmet", "Nordic Warlord Helmet", [("Helmet_C", 0)],  itp_type_head_armor|itp_merchandise, 0,                                                    5950, weight(4.8)| abundance(100) | head_armor(48) | body_armor(0) | leg_armor(0) | difficulty(18), imodbits_plate ],
    ["m_vaegir_mask2", "War Mask", [("vaeg_helmet9", 0)],  itp_type_head_armor|itp_covers_beard|itp_merchandise, 0,                                                     5850, weight(4.8)| abundance(100) | head_armor(48) | body_armor(0) | leg_armor(0) | difficulty(18), imodbits_plate ],
    ["m_vaegir_noble_helmet", "Vaegir Round Helmet", [("nikolskoe_helm", 0)],  itp_type_head_armor|itp_covers_beard|itp_merchandise, 0,                                 5250, weight(4.25)| abundance(100) | head_armor(46) | body_armor(0) | leg_armor(0) | difficulty(17), imodbits_plate ],
    ["m_onion_top_bascinet","Onion-Top Bascinet", [("onion_top_bascinet", 0),("onion_top_bascinet_inv", ixmesh_inventory)], itp_type_head_armor|itp_attach_armature|itp_merchandise, 0,                                     5300, weight(4.25)| abundance(100) | head_armor(46) | body_armor(0) | leg_armor(0) | difficulty(17), imodbits_plate],
    ["m_vaegir_noble_helmet_b", "Vaegir Spiked Helmet", [("tagancha_helm_b", 0)],  itp_type_head_armor|itp_covers_beard|itp_merchandise, 0,                             5400, weight(4.5) | abundance(100) | head_armor(47) | body_armor(0) | leg_armor(0) | difficulty(18), imodbits_plate ],
    ["m_narf_zitta_bascinet_novisor", "Bascinet with Long Aventail", [("narf_zitta_bascinet_novisor",0), ("narf_inv_zitta_bascinet_novisor",ixmesh_inventory)], itp_type_head_armor|itp_attach_armature|itp_merchandise, 0, 5500, weight(4.5) | abundance(100) | head_armor(47) | body_armor(0) | leg_armor(0) | difficulty(18), imodbits_plate],
    ["m_narf_sallet_coif", "Short-Tailed Sallet with Mai Guard", [("narf_open_salet_coif", 0)], itp_type_head_armor|itp_merchandise, 0,                                 5600, weight(4.5) | abundance(100) | head_armor(47) | body_armor(0) | leg_armor(0) | difficulty(18), imodbits_plate ],

    ["m_vaegir_noble_helmet_d", "Vaegir Reinforced Helmet", [("gnezdovo_helm_b", 0)], itp_type_head_armor|itp_covers_beard|itp_merchandise, 0,  #### MAIN
     5700, weight(4.75)| abundance(100) | head_armor(48) | body_armor(0) | leg_armor(0) | difficulty(18), imodbits_plate ],
    ["m_vaegir_noble_helmet_d_horsetail", "Vaegir Reinforced Helmet with Horsetail", [("gnezdovo_helm_a", 0)], itp_type_head_armor|itp_covers_beard, 0,  #### EXTRA
     200, weight(4.75)| abundance(100) | head_armor(48) | body_armor(0) | leg_armor(0) | difficulty(18), imodbits_plate ],

    # ["m_west_guardsman_helm", "Guardsman Helm", [("west_guardsman_helm",0)],  itp_type_head_armor|itp_merchandise, 0,                                                   5880, weight(4.75)| abundance(100) | head_armor(48) | body_armor(0) | leg_armor(0) | difficulty(18), imodbits_plate ],
    ["m_barbuta_1", "Barbute", [("dejawolf_barbuta1", 0)], itp_type_head_armor|itp_merchandise, 0,                                                                      5900, weight(5.0) | abundance(100) | head_armor(48) | body_armor(0) | leg_armor(0) | difficulty(18), imodbits_plate ],
    # ["m_west_pikeman_helmet", "West Sallet", [("west_pikeman_helmet",0)],  itp_type_head_armor|itp_covers_beard|itp_merchandise, 0,                                     5920, weight(5.0) | abundance(100) | head_armor(49) | body_armor(0) | leg_armor(0) | difficulty(18), imodbits_plate ],
    ["m_crusader_faceplate","Helmet with Brass Faceplate", [("dejanarf_faceplate", 0),("dejanarf_faceplate_inv", ixmesh_inventory)], itp_type_head_armor|itp_attach_armature|itp_merchandise|itp_covers_beard, 0,                       6000, weight(5.0) | abundance(100) | head_armor(49) | difficulty(18), imodbits_plate ],
    ["m_crusader_helmet_4", "Pot Helm", [("dejanarf_pot_helm_1", 0),("dejanarf_pot_helm_1_inv", ixmesh_inventory)], itp_type_head_armor|itp_covers_beard|itp_attach_armature|itp_merchandise, 0,                                        6050, weight(5.0) | abundance(100) | head_armor(49) | difficulty(18), imodbits_plate ],
    ["m_crusader_helmet_4_round","Round Pot Helm", [("dejanarf_pot_helm_1_round", 0),("dejanarf_pot_helm_1_round_inv", ixmesh_inventory)], itp_type_head_armor|itp_attach_armature|itp_merchandise|itp_covers_beard, 0,                 6100, weight(5.0) | abundance(100) | head_armor(49) | difficulty(18), imodbits_plate ],

    ["m_crusader_helmet_2", "Reinforced Pot Helm", [("dejanarf_pot_helm_2", 0),("dejanarf_pot_helm_2_inv", ixmesh_inventory)], itp_type_head_armor|itp_covers_beard|itp_attach_armature|itp_merchandise, 0, #### MAIN
     6200, weight(5.0) | abundance(100) | head_armor(50) | body_armor(0) | leg_armor(0) | difficulty(19), imodbits_plate ],
    ["m_crusader_helmet_1", "Fluted Pot Helm", [("dejanarf_pot_helm_3", 0),("dejanarf_pot_helm_3_inv", ixmesh_inventory)], itp_type_head_armor|itp_covers_beard|itp_attach_armature|itp_merchandise, 0,  ### EXTRA
     200, weight(5.0) | abundance(100) | head_armor(50) | body_armor(0) | leg_armor(0) | difficulty(19), imodbits_plate ],

    ["m_narf_visored_sallet", "Visored Short-Tailed Sallet", [("visored_salet_coif", 0)], itp_type_head_armor|itp_covers_beard|itp_merchandise, 0,   6300, weight(5.0) | abundance(100) | head_armor(50) | body_armor(0) | leg_armor(0) | difficulty(19), imodbits_plate ],


    ["m_full_helm", "Thick Pot Helm", [("great_helmet_new_b", 0)],  itp_type_head_armor|itp_covers_head|itp_merchandise, 0,    ############ MAIN ############
     6400, weight(5.25)| abundance(100) | head_armor(51) | body_armor(0) | leg_armor(0) | difficulty(19), imodbits_plate ],
    ["gg_new_plate_face_c", "Rhodok Plate Face Long", [("gg_new_plate_face_c",0)], itp_merchandise| itp_type_head_armor| itp_covers_head ,0,  ############ EXTRA  ############
     200 , weight(5.20)|abundance(100)|head_armor(51)|body_armor(0)|leg_armor(0)|difficulty(19) ,imodbits_plate ],


    ["m_crusader_helmet_6", "Black Helm", [("dejanarf_black_helm_2", 0),("dejanarf_black_helm_2_inv", ixmesh_inventory)], itp_type_head_armor|itp_covers_beard|itp_attach_armature|itp_merchandise, 0, ### MAIN
     6450, weight(5.25)| abundance(100) | head_armor(51) | body_armor(0) | leg_armor(0) | difficulty(19), imodbits_plate ],
    ["m_crusader_helmet_3", "Round Black Helm", [("dejanarf_black_helm_1", 0),("dejanarf_black_helm_1_inv", ixmesh_inventory)], itp_type_head_armor|itp_covers_beard|itp_attach_armature|itp_merchandise, 0, ### EXTRA
     200, weight(5.25)| abundance(100) | head_armor(51) | body_armor(0) | leg_armor(0) | difficulty(19), imodbits_plate ],

    ["m_narf_zitta_bascinet", "Visored Bascinet with Long Aventail", [("narf_zitta_bascinet",0), ("narf_inv_zitta_bascinet_closedvisor",ixmesh_inventory)], itp_merchandise|itp_type_head_armor|itp_covers_head|itp_attach_armature, 0,
     6650, weight(5.5) | abundance(100) | head_armor(52) | body_armor(0) | leg_armor(0) | difficulty(20), imodbits_plate ],


    ["m_klappvisor", "Pigface Klappvisor", [("pigface_klappvisor", 0), ("pigface_klappvisor_inv",ixmesh_inventory)], itp_type_head_armor|itp_covers_head|itp_attach_armature|itp_merchandise, 0, ######## MAIN ############
     6750, weight(5.5) | abundance(100) | head_armor(52) | body_armor(0) | leg_armor(0) | difficulty(20), imodbits_plate ],
    ["gg_pigface_klappvisor_open", "Pigface Klappvisor Open", [("gg_pigface_klappvisor_open",0), ("gg_pigface_inv_klappvisor_open",ixmesh_inventory)], itp_merchandise|itp_type_head_armor|itp_attach_armature, 0,   ############ EXTRA  ############
     200, weight(5.5) | abundance(100) | head_armor(50) | body_armor(0) | leg_armor(0) | difficulty(20), imodbits_plate ],


    ["m_klappvisor_2", "Klappvisor", [("dejawolf_klappvisier", 0)], itp_type_head_armor|itp_covers_head|itp_merchandise, 0,     ############ MAIN ############
     6800, weight(5.5) | abundance(100) | head_armor(52) | body_armor(0) | leg_armor(0) | difficulty(20), imodbits_plate ],
    ["gg_klappvisier_open", "Klappvisor Open", [("gg_klappvisier_open",0), ("gg_inv_klappvisier_open",ixmesh_inventory)], itp_merchandise|itp_type_head_armor|itp_attach_armature, 0,   ############ EXTRA  ############
     200, weight(5.5) | abundance(100) | head_armor(50) | body_armor(0) | leg_armor(0) | difficulty(20), imodbits_plate ],


    ["m_hounskull", "Hounskull", [("hounskull", 0)], itp_type_head_armor|itp_covers_head|itp_merchandise, 0,                                         7900, weight(5.75) | abundance(100) | head_armor(54) | body_armor(0) | leg_armor(0) | difficulty(21), imodbits_plate ],
#    ["m_sallet_1", "Visored Sallet", [("dejawolf_sallet", 0)], itp_type_head_armor|itp_covers_head|itp_merchandise, 0,                              8000, weight(5.75)| abundance(100) | head_armor(54) | body_armor(0) | leg_armor(0) | difficulty(21), imodbits_plate ],
    ["m_bolzano_bucket", "Great Helm", [("dejawolf_bolzano_bucket", 0)], itp_type_head_armor |itp_covers_head|itp_merchandise, 0,                    8100, weight(5.75)| abundance(100) | head_armor(54) | body_armor(0) | leg_armor(0) | difficulty(21), imodbits_plate ],
    ["m_madeln_bucket_1", "Great Helm", [("dejawolf_madeln_bucket_1", 0)], itp_type_head_armor|itp_covers_head|itp_merchandise, 0,                   8150, weight(5.75)| abundance(100) | head_armor(54) | body_armor(0) | leg_armor(0) | difficulty(21), imodbits_plate ],
    ["m_great_helmet_1", "Great Helm", [("dejawolf_crusader_bucket_1", 0)],  itp_type_head_armor |itp_covers_head|itp_merchandise, 0,                8200, weight(5.75)| abundance(100) | head_armor(54) | body_armor(0) | leg_armor(0) | difficulty(21), imodbits_plate ],
    ["m_great_helmet_2", "Great Helm", [("dejawolf_crusader_bucket_2", 0)],  itp_type_head_armor |itp_covers_head|itp_merchandise, 0,                8250, weight(5.75)| abundance(100) | head_armor(54) | body_armor(0) | leg_armor(0) | difficulty(21), imodbits_plate ],
    ["m_madeln_bucket_2", "Great Helm", [("dejawolf_madeln_bucket_2", 0)], itp_type_head_armor |itp_covers_head|itp_merchandise, 0,                  8300, weight(5.75)| abundance(100) | head_armor(54) | body_armor(0) | leg_armor(0) | difficulty(21), imodbits_plate ],
    ["m_bolzano_bucket_c", "Colored Great Helm", [("dejawolf_bolzano_bucket_c", 0)], itp_type_head_armor|itp_covers_head|itp_merchandise, 0,         8400, weight(5.75)| abundance(100) | head_armor(54) | body_armor(0) | leg_armor(0) | difficulty(21), imodbits_plate, [ (ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_m_colored_helmet", ":agent_no", ":troop_no")]) ] ],
    ["m_madeln_bucket_1_c", "Colored Great Helm", [("dejawolf_madeln_bucket_1_c", 0)], itp_type_head_armor|itp_covers_head|itp_merchandise, 0,       8450, weight(5.75)| abundance(100) | head_armor(54) | body_armor(0) | leg_armor(0) | difficulty(21), imodbits_plate, [ (ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_m_colored_helmet", ":agent_no", ":troop_no")]) ] ],
    ["m_crusader_bucket_1_c", "Colored Great Helm", [("dejawolf_crusader_bucket_1_c", 0)], itp_type_head_armor|itp_covers_head|itp_merchandise, 0,   8500, weight(5.75)| abundance(100) | head_armor(54) | body_armor(0) | leg_armor(0) | difficulty(21), imodbits_plate, [ (ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_m_colored_helmet", ":agent_no", ":troop_no")]) ] ],
    ["m_crusader_bucket_2_c", "Colored Great Helm", [("dejawolf_crusader_bucket_2_c", 0)], itp_type_head_armor|itp_covers_head|itp_merchandise, 0,   8550, weight(5.75)| abundance(100) | head_armor(54) | body_armor(0) | leg_armor(0) | difficulty(21), imodbits_plate, [ (ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_m_colored_helmet", ":agent_no", ":troop_no")]) ] ],
    ["m_madeln_bucket_2_c", "Colored Great Helm", [("dejawolf_madeln_bucket_2_c", 0)], itp_type_head_armor|itp_covers_head|itp_merchandise, 0,       8600, weight(5.75)| abundance(100) | head_armor(54) | body_armor(0) | leg_armor(0) | difficulty(21), imodbits_plate, [ (ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_m_colored_helmet", ":agent_no", ":troop_no")]) ] ],
##    ["m_great_helmet", "Thick Great Helm", [("great_helmet_new", 0)],  itp_type_head_armor|itp_covers_head|itp_merchandise, 0,                       8700, weight(5.75)| abundance(100) | head_armor(54) | body_armor(0) | leg_armor(0) | difficulty(21), imodbits_plate ],
    ["m_great_helmet_3", "Wide Great Helm", [("dejawolf_great_helm",0)],  itp_type_head_armor|itp_covers_head|itp_merchandise, 0,                    8800, weight(5.75)| abundance(100) | head_armor(54) | body_armor(0) | leg_armor(0) | difficulty(21), imodbits_plate ],
    ["m_sugarloaf", "Sugarloaf Great Helm", [("sugarloaf",0)],  itp_type_head_armor|itp_covers_head|itp_merchandise, 0,                              8900, weight(5.75)| abundance(100) | head_armor(54) | body_armor(0) | leg_armor(0) | difficulty(21), imodbits_plate ],
    ["m_great_bascinet", "Great Bascinet", [("dejawolf_great_bascinet",0),("dejawolf_great_bascinet_inv", ixmesh_inventory)],  itp_type_head_armor|itp_covers_head|itp_attach_armature, 0, 0,weight(6.0) | abundance(100) | head_armor(56) | body_armor(0) | leg_armor(0) | difficulty(21), imodbits_plate ],


    ["m_eyeslot_kettlehat_hood","Eyeslot_Kettlehat", [("narf_eyeslot_kettlehat_hood", 0),("narf_eyeslot_kettlehat_hood", ixmesh_inventory)], itp_type_head_armor|itp_attach_armature|itp_merchandise, 0,
     3850, weight(3.25)|abundance(100)|head_armor(42)|difficulty(14), imodbits_armor|imodbit_cracked, []],


     # Rare head armor
    ["m_nemeruis_chichak","Sarranid Chichak", [("nemeruis_chichak", 0),("nemeruis_chichak_inv", ixmesh_inventory)], itp_type_head_armor|itp_attach_armature|itp_merchandise, 0,
     60000, weight(4.75)| abundance(100) | head_armor(48) | body_armor(0) | leg_armor(0) | difficulty(18), imodbits_plate ],
    ["m_litchina_helm", "Litchina", [("litchina_helm",0), ("litchina_helm_inv",ixmesh_inventory)], itp_type_head_armor|itp_covers_beard|itp_attach_armature|itp_merchandise, 0,
     75000, weight(4.75) | abundance(100) | head_armor(48) | body_armor(0) | leg_armor(0) | difficulty(18), imodbits_plate ],
    ["helm_sultan_saracens_market", "Sultan Helmet", [("helm_sultan_saracens_market",0),("inv_helm_sultan_saracens_market", ixmesh_inventory)], itp_type_head_armor|itp_fit_to_head|itp_attach_armature, 0,
     85000, weight(5.8) | abundance(100) | head_armor(54) | difficulty(21), imodbits_plate],
    ["turban_helmet_new", "Reinforced Sultan Helmet", [("turban_helmet_new",0),("turban_helmet_new_inv", ixmesh_inventory)], itp_type_head_armor|itp_fit_to_head|itp_attach_armature, 0,
     92500, weight(5.8) | abundance(100) | head_armor(54) | difficulty(21), imodbits_plate],
    ["turban_helmet_b", "Reinforced Sultan Helmet Mod", [("turban_helmet_b",0),("turban_helmet_b_inv", ixmesh_inventory)], itp_type_head_armor|itp_fit_to_head|itp_attach_armature, 0,
     500, weight(5.8) | abundance(100) | head_armor(54) | difficulty(21), imodbits_plate],


     # Nessa helmets
    ["new_sugarloaf", "Rare Sugarloaf", [("new_sugarloaf", 0)], itp_type_head_armor|itp_covers_head|itp_attach_armature|itp_merchandise, 0,     ############ MAIN ############
     0, weight(5.5) | abundance(100) | head_armor(52) | body_armor(0) | leg_armor(0) | difficulty(20), imodbits_plate ],
    ["gjermendbu_helmet", "Gjermendbu Helmet", [("gjermendbu_helmet", 0)], itp_type_head_armor|itp_attach_armature|itp_covers_beard|itp_merchandise, 0,     ############ MAIN ############
     5750, weight(5.0) | abundance(100) | head_armor(48) | body_armor(0) | leg_armor(0) | difficulty(18), imodbits_plate ],
    ["battanian_helmet_04", "Battanian Helmet", [("battanian_helmet_04", 0)], itp_type_head_armor|itp_attach_armature|itp_merchandise, 0,     ############ MAIN ############
     5700, weight(4.6) | abundance(100) | head_armor(48) | body_armor(0) | leg_armor(0) | difficulty(18), imodbits_plate ], 
 
    ["sugarloaf_a", "Light Sugarloaf", [("sugarloaf_a", 0)], itp_type_head_armor|itp_covers_head|itp_attach_armature|itp_merchandise, 0,     ############ MOD ############
     400, weight(5.8) | abundance(100) | head_armor(54) | body_armor(0) | leg_armor(0) | difficulty(21), imodbits_plate ],
    ["sugarloaf_b", "Dark Sugarloaf", [("sugarloaf_b", 0)], itp_type_head_armor|itp_covers_head|itp_attach_armature|itp_merchandise, 0,     ############ MOD ############
     400, weight(5.8) | abundance(100) | head_armor(54) | body_armor(0) | leg_armor(0) | difficulty(21), imodbits_plate ],

    ["pop_sugarloaf", "Visored Sugarloaf", [("pop_sugarloaf", 0)], itp_type_head_armor|itp_covers_head|itp_attach_armature|itp_merchandise, 0,     ############ MAIN ############
     9000, weight(5.8) | abundance(100) | head_armor(54) | body_armor(0) | leg_armor(0) | difficulty(21), imodbits_plate ],
    ["pop_sugarloaf_open", "Open Visored Sugarloaf", [("pop_sugarloaf_open", 0)], itp_type_head_armor|itp_attach_armature|itp_merchandise, 0,     ############ MOD ############
     400, weight(5.8) | abundance(100) | head_armor(54) | body_armor(0) | leg_armor(0) | difficulty(21), imodbits_plate ],
    ["pop_sugarloaf2", "Black Visored Sugarloaf", [("pop_sugarloaf2", 0)], itp_type_head_armor|itp_covers_head|itp_attach_armature|itp_merchandise, 0,     ############ MAIN ############
     9100, weight(5.8) | abundance(100) | head_armor(54) | body_armor(0) | leg_armor(0) | difficulty(21), imodbits_plate ],
    ["pop_sugarloaf2_open", "Open Black Visored Sugarloaf", [("pop_sugarloaf2_open", 0)], itp_type_head_armor|itp_attach_armature|itp_merchandise, 0,     ############ MOD ############
     400, weight(5.8) | abundance(100) | head_armor(54) | body_armor(0) | leg_armor(0) | difficulty(21), imodbits_plate ],
    ["pop_sugarloaf3", "Gold Visored Sugarloaf", [("pop_sugarloaf3", 0)], itp_type_head_armor|itp_covers_head|itp_attach_armature|itp_merchandise, 0,     ############ MAIN ############
     9200, weight(5.8) | abundance(100) | head_armor(54) | body_armor(0) | leg_armor(0) | difficulty(21), imodbits_plate ],
    ["pop_sugarloaf3_open", "Open Gold Visored Sugarloaf", [("pop_sugarloaf3_open", 0)], itp_type_head_armor|itp_attach_armature|itp_merchandise, 0,     ############ MOD ############
     400, weight(5.8) | abundance(100) | head_armor(54) | body_armor(0) | leg_armor(0) | difficulty(21), imodbits_plate ],

    ["ivn_viking_helmet", "Warlord Helmet", [("ivn_viking_helmet", 0)], itp_type_head_armor|itp_merchandise, 0,
     200000, weight(5.8) | abundance(100) | head_armor(54) | body_armor(0) | leg_armor(0) | difficulty(21), imodbits_plate ],
    ["gulam_helm_e", "Gulam Helm", [("gulam_helm_e", 0)], itp_type_head_armor|itp_merchandise, 0,
     55000, weight(4.8) | abundance(100) | head_armor(48) | body_armor(0) | leg_armor(0) | difficulty(18), imodbits_plate ],
    ["gulam_helm_f", "Gulam Helm with Turban", [("gulam_helm_f", 0)], itp_type_head_armor|itp_covers_beard|itp_merchandise, 0,
     1000, weight(4.8) | abundance(100) | head_armor(48) | body_armor(0) | leg_armor(0) | difficulty(18), imodbits_plate ],
    ["gulam_helmet2", "Gulam Archer Helm", [("gulam_helmet2", 0)], itp_type_head_armor|itp_covers_beard|itp_merchandise, 0,
     50000, weight(4.8) | abundance(100) | head_armor(48) | body_armor(0) | leg_armor(0) | difficulty(18), imodbits_plate ],

     #SPECIAL
    ["tac", "Queens Crown", [("tac", 0)], itp_type_head_armor|itp_merchandise, 0,
     0, weight(5.5) | abundance(100) | head_armor(52) | body_armor(0) | leg_armor(0) | difficulty(20), imodbits_plate ],    

############################################################################ GOLD AND GLORY HEAD ARMORS ############################################################################

 ["gg_visoredsallet1", "Knightly Visored Sallet", [("gg_visoredsallet1",0)], itp_merchandise| itp_type_head_armor| itp_attach_armature| itp_covers_head ,0,
  8400 , weight(5.8)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(21) ,imodbits_plate ],

  ["gg_elite_face_plate_helmet", "Elite Full Face Plate Helmet", [("gg_elite_face_plate_helmet",0)], itp_merchandise| itp_type_head_armor| itp_covers_head ,0, ############ MAIN  ############
  13000, weight(6)|abundance(100)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(24) ,imodbits_plate ],


  ["weimarhelm","Weimar Helmet", [("weimarhelm", 0),("inv_weimarhelm", ixmesh_inventory)], itp_type_head_armor|itp_attach_armature ,0, 
   16000, weight(6)|abundance(100)|head_armor(57)|difficulty(27), imodbits_plate ],

  ["greatbascinet1", "New Great Bascinet", [("greatbascinet1",0)], itp_merchandise|  itp_type_head_armor|itp_attach_armature ,0,
   11000 , weight(6)|abundance(100)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(24) ,imodbits_plate ],

  ["gg_closed_armet", "Milanes Helmet", [("gg_closed_armet",0)], itp_merchandise| itp_type_head_armor| itp_covers_head ,0, ############ MAIN  ############
   9500 , weight(6)|abundance(100)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(24) ,imodbits_plate ],
  ["gg_closed_armet_with_green_feather", "Milanes Helmet with Green Feather", [("gg_closed_armet_with_green_feather",0)], itp_merchandise| itp_type_head_armor| itp_covers_head ,0, ############ EXTRA  ############
   150 , weight(6)|abundance(100)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(24) ,imodbits_plate ],
  ["gg_closed_armet_with_yellow_feather", "Milanes Helmet with Yellow Feather", [("gg_closed_armet_with_yellow_feather",0)], itp_merchandise| itp_type_head_armor| itp_covers_head ,0, ############ EXTRA  ############
   150 , weight(6)|abundance(100)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(24) ,imodbits_plate ],
  ["gg_closed_armet_with_white_feather", "Milanes Helmet with White Feather", [("gg_closed_armet_with_white_feather",0)], itp_merchandise| itp_type_head_armor| itp_covers_head ,0, ############ EXTRA  ############
   150 , weight(6)|abundance(100)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(24) ,imodbits_plate ],
  ["gg_closed_armet_with_red_feather", "Milanes Helmet with Red Feather", [("gg_closed_armet_with_red_feather",0)], itp_merchandise| itp_type_head_armor| itp_covers_head ,0, ############ EXTRA  ############
   150 , weight(6)|abundance(100)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(24) ,imodbits_plate ],
  ["gg_closed_armet_with_blue_feather", "Milanes Helmet with Blue Feather", [("gg_closed_armet_with_blue_feather",0)], itp_merchandise| itp_type_head_armor| itp_covers_head ,0, ############ EXTRA  ############
   150 , weight(6)|abundance(100)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(24) ,imodbits_plate ],
  ["gg_closed_armet_with_brown_feather", "Milanes Helmet with Brown Feather", [("gg_closed_armet_with_brown_feather",0)], itp_merchandise| itp_type_head_armor| itp_covers_head ,0, ############ EXTRA  ############
   150 , weight(6)|abundance(100)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(24) ,imodbits_plate ],
  ["gg_closed_armet_with_black_feather", "Milanes Helmet with Black Feather", [("gg_closed_armet_with_black_feather",0)], itp_merchandise| itp_type_head_armor| itp_covers_head ,0, ############ EXTRA  ############
   150 , weight(6)|abundance(100)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(24) ,imodbits_plate ],

  ["gg_open_armet", "Open Milanes Helmet", [("gg_open_armet",0)], itp_merchandise| itp_type_head_armor| itp_fit_to_head ,0, ############ EXTRA  ############
   200 , weight(6)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(24) ,imodbits_plate ], 
  ["gg_open_armet_with_green_feather", "Open Milanes with Green Feather", [("gg_open_armet_with_green_feather",0)], itp_merchandise| itp_fit_to_head| itp_type_head_armor ,0, ############ EXTRA  ############
   200 , weight(6)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(24) ,imodbits_plate ],
  ["gg_open_armet_with_yellow_feather", "Open Milanes with Yellow Feather", [("gg_open_armet_with_yellow_feather",0)], itp_merchandise| itp_fit_to_head| itp_type_head_armor ,0, ############ EXTRA  ############
   200 , weight(6)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(24) ,imodbits_plate ],
  ["gg_open_armet_with_white_feather", "Open Milanes with White Feather", [("gg_open_armet_with_white_feather",0)], itp_merchandise| itp_fit_to_head| itp_type_head_armor ,0, ############ EXTRA  ############
   200 , weight(6)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(24) ,imodbits_plate ],
  ["gg_open_armet_with_red_feather", "Open Milanes with Red Feather", [("gg_open_armet_with_red_feather",0)], itp_merchandise| itp_fit_to_head| itp_type_head_armor ,0, ############ EXTRA  ############
   200 , weight(6)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(24) ,imodbits_plate ],
  ["gg_open_armet_with_blue_feather", "Open Milanes with Blue Feather", [("gg_open_armet_with_blue_feather",0)], itp_merchandise| itp_fit_to_head| itp_type_head_armor ,0, ############ EXTRA  ############
   200 , weight(6)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(24) ,imodbits_plate ],
  ["gg_open_armet_with_brown_feather", "Open Milanes with Brown Feather", [("gg_open_armet_with_brown_feather",0)], itp_merchandise| itp_fit_to_head| itp_type_head_armor ,0, ############ EXTRA  ############
   200 , weight(6)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(24) ,imodbits_plate ],
  ["gg_open_armet_with_black_feather", "Open Milanes with Black Feather", [("gg_open_armet_with_black_feather",0)], itp_merchandise| itp_fit_to_head| itp_type_head_armor ,0, ############ EXTRA  ############
   200 , weight(6)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(24) ,imodbits_plate ],


 ["m_sallet_1", "Visored Sallet", [("gg_great_milanes_helmet",0)], itp_merchandise| itp_type_head_armor| itp_covers_head ,0,
  8000, weight(5.75)| abundance(100) | head_armor(54) | body_armor(0) | leg_armor(0) | difficulty(21), imodbits_plate ],

 ["gg_great_jousting_helmet", "Great Jousting Plate Helmet", [("gg_great_jousting_helmet",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard ,0, ############ MAIN  ############
  7500 , weight(5.8)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(20) ,imodbits_plate ],
 ["gg_great_jousting_helmet_black_with_feathers", "Great Jousting Helmet with Black Feather", [("gg_great_jousting_helmet_black_with_feathers",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard ,0, ############ EXTRA ############
  200 , weight(5.8)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(20) ,imodbits_plate ],
 ["gg_great_jousting_helmet_red_with_feathers", "Great Jousting Helmet with Red Feather", [("gg_great_jousting_helmet_red_with_feathers",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard ,0, ############ EXTRA ############
  200 , weight(5.8)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(20) ,imodbits_plate ],
 ["gg_great_jousting_helmet_white_with_feathers", "Great Jousting Helmet with White Feather", [("gg_great_jousting_helmet_white_with_feathers",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard ,0, ############ EXTRA ############
  200 , weight(5.8)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(20) ,imodbits_plate ],

 ["gg_italian_bascinet", "Italian Bascinet Helmet", [("gg_italian_bascinet",0)], itp_merchandise| itp_type_head_armor| itp_attach_armature ,0,
   8350 , weight(5.8)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(21) ,imodbits_plate ],
  ["gg_zitta_bascinet", "Visored Zitta Bascinet", [("gg_zitta_bascinet",0)], itp_merchandise| itp_type_head_armor| itp_attach_armature| itp_covers_head ,0,
   6550 , weight(5.30)|abundance(100)|head_armor(51)|body_armor(0)|leg_armor(0)|difficulty(19) ,imodbits_plate ], 

  ["gg_new_full_sallet", "New Full Sallet", [("gg_new_full_sallet",0)], itp_merchandise| itp_type_head_armor| itp_covers_head ,0, ############ MAIN  ############
   7000 , weight(5.5)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(20) ,imodbits_plate ],
  ["gg_new_full_sallet_redfeather_helmet", "New Full Sallet with Red Feather", [("gg_new_full_sallet_redfeather_helmet",0)], itp_merchandise| itp_covers_head| itp_type_head_armor| itp_covers_beard ,0,    ############ EXTRA  ############
   100 , weight(5.5)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(21) ,imodbits_plate ],
  ["gg_new_full_sallet_yellowfeather_helmet", "New Full Sallet with Yellow Feather", [("gg_new_full_sallet_yellowfeather_helmet",0)], itp_merchandise| itp_covers_head| itp_type_head_armor ,0,    ############ EXTRA  ############
   100 , weight(5.5)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(21) ,imodbits_plate ],
  ["gg_new_full_sallet_bluefeather_helmet", "New Full Sallet with Blue Feather", [("gg_new_full_sallet_bluefeather_helmet",0)], itp_merchandise| itp_covers_head| itp_type_head_armor| itp_covers_beard ,0,    ############ EXTRA  ############
   100 , weight(5.5)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(21) ,imodbits_plate ],
  ["gg_new_full_sallet_blackfeather_helmet", "New Full Sallet with Black Feather", [("gg_new_full_sallet_blackfeather_helmet",0)], itp_merchandise| itp_covers_head| itp_type_head_armor| itp_covers_beard ,0,    ############ EXTRA  ############
   100 , weight(5.5)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(21) ,imodbits_plate ],
  ["gg_new_full_sallet_brownfeather_helmet", "New Full Sallet with Brown Feather", [("gg_new_full_sallet_brownfeather_helmet",0)], itp_merchandise| itp_covers_head| itp_type_head_armor| itp_covers_beard ,0,    ############ EXTRA  ############
   100 , weight(5.5)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(21) ,imodbits_plate ],
  ["gg_new_full_sallet_greenfeather_helmet", "New Full Sallet with Green Feather", [("gg_new_full_sallet_greenfeather_helmet",0)], itp_merchandise| itp_covers_head| itp_type_head_armor| itp_covers_beard ,0,    ############ EXTRA  ############
   100 , weight(5.5)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(21) ,imodbits_plate ],

  ["gg_new_sallet_short", "New Sallet Short", [("gg_new_sallet_short",0)], itp_merchandise| itp_fit_to_head| itp_type_head_armor ,0,    ### MAIN
   5550 , weight(4.3)|abundance(100)|head_armor(47)|body_armor(0)|leg_armor(0)|difficulty(17) ,imodbits_plate ],
  ["gg_new_sallet_short_pointy", "New Pointy Head Short Sallet", [("gg_new_sallet_short_pointy",0)], itp_merchandise| itp_fit_to_head| itp_type_head_armor ,0,    ### EXTRA
   100 , weight(4.3)|abundance(100)|head_armor(47)|body_armor(0)|leg_armor(0)|difficulty(17) ,imodbits_plate ],

  ["gg_new_sallet_with_coif", "New Sallet with Coif", [("gg_new_sallet_with_coif",0)], itp_merchandise| itp_fit_to_head|  itp_type_head_armor  ,0,  ### MAIN
   5950 , weight(5)|abundance(100)|head_armor(48)|body_armor(0)|leg_armor(0)|difficulty(18) ,imodbits_plate ],
  ["gg_new_pointy_sallet_with_coif", "New Pointy Sallet with coif", [("gg_new_pointy_sallet_with_coif",0)], itp_merchandise| itp_fit_to_head|  itp_type_head_armor ,0,  ### EXTRA
   100 , weight(5)|abundance(100)|head_armor(48)|body_armor(0)|leg_armor(0)|difficulty(18) ,imodbits_plate ],


 ["gg_new_crusader_helmet", "Norman Pot Helmet with Face Plate", [("gg_new_crusader_helmet",0)], itp_merchandise| itp_fit_to_head| itp_covers_beard| itp_type_head_armor ,0,  
  6130 , weight(5)|abundance(100)|head_armor(49)|body_armor(0)|leg_armor(0)|difficulty(18) ,imodbits_plate ], 

 ["gg_frenchpepperpot", "Plate Bounty Hunter Helmet", [("gg_frenchpepperpot",0)], itp_merchandise| itp_fit_to_head| itp_covers_beard| itp_type_head_armor ,0, ############ MAIN  ############
  6460 , weight(5)|abundance(100)|head_armor(51)|body_armor(0)|leg_armor(0)|difficulty(19) ,imodbits_plate ],


 ["gg_varangopoulos_bascinet", "Varagopoulos Helmet", [("gg_varangopoulos_bascinet",0)], itp_merchandise| itp_fit_to_head| itp_type_head_armor ,0,  
  5800 , weight(5)|abundance(100)|head_armor(48)|body_armor(0)|leg_armor(0)|difficulty(18) ,imodbits_plate ],
 

 ["gg_flattophelmet", "Flat Topped Face Mail", [("gg_flattophelmet",0)], itp_merchandise| itp_fit_to_head| itp_covers_beard| itp_type_head_armor ,0, ############ MAIN  ############
  4810 , weight(4)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(16) ,imodbits_armor ],
 ["gg_kettlehatfacebyrnie", "Kettle Hat with Face Mail", [("gg_kettlehatfacebyrnie",0)], itp_merchandise| itp_fit_to_head| itp_covers_beard| itp_type_head_armor ,0, ############ EXTRA  ############
  100 , weight(4)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(16) ,imodbits_armor ], 

 ["gg_open_normanhelmcoif", "Norman  Mail Helmet", [("gg_open_normanhelmcoif",0)], itp_merchandise| itp_fit_to_head| itp_covers_beard| itp_type_head_armor ,0, ############ MAIN  ############
  4400 , weight(4)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(15) ,imodbits_armor ],
 ["gg_normanhelmbalaclavacoif", "Norman Reinforced Mail Helmet", [("gg_normanhelmbalaclavacoif",0)], itp_merchandise| itp_fit_to_head| itp_covers_beard| itp_type_head_armor ,0, ############ EXTRA  ############
  200 , weight(4)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(15) ,imodbits_armor ],
 ["gg_normanhelmfullcoif", "Norman Face Mail Helmet", [("gg_normanhelmfullcoif",0)], itp_merchandise| itp_fit_to_head| itp_covers_beard| itp_type_head_armor ,0, ############ EXTRA  ############
  700 , weight(4.50)|abundance(100)|head_armor(46)|body_armor(0)|leg_armor(0)|difficulty(17) ,imodbits_armor ],
 
 ["gg_kiev_helmet_1_facemail_1", "Vaegir Face Mail Helmet", [("gg_kiev_helmet_1_facemail_1",0)], itp_merchandise| itp_fit_to_head| itp_covers_beard| itp_type_head_armor ,0,
  4850 , weight(4)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(16) ,imodbits_armor ],

 ["gg_rhodok_nasal_helmet_b", "Nasal Helmet", [("gg_rhodok_nasal_helmet_b",0)], itp_merchandise| itp_fit_to_head|  itp_type_head_armor ,0, ############ MAIN  ############
  4400 , weight(4)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(15) ,imodbits_armor ],
 ["gg_rhodok_nasal_helmet_c", "Mail Supported Nasal Helmet", [("gg_rhodok_nasal_helmet_c",0)], itp_merchandise| itp_fit_to_head| itp_covers_beard| itp_type_head_armor ,0, ############ EXTRA  ############
  650 , weight(4)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(16) ,imodbits_armor ],

 ["gg_light_sallet_helmet", "Light Open Sallet Helmet", [("gg_light_sallet_helmet",0)], itp_merchandise| itp_fit_to_head|  itp_type_head_armor ,0, ############ MAIN  ############
  4400 , weight(3.5)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(15) ,imodbits_plate ],
 ["m_masked_sallet", "Light Open Sallet with Black Mask", [("m_masked_sallet",0)], itp_merchandise| itp_covers_beard| itp_fit_to_head|  itp_type_head_armor ,0, ############ EXTRA  ############
  200 , weight(3.5)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(15) ,imodbits_plate ],

 ["gg_barbuta2", "Barbutte", [("gg_barbuta2",0)], itp_merchandise| itp_fit_to_head|  itp_type_head_armor ,0,
  5950 , weight(5)|abundance(100)|head_armor(49)|body_armor(0)|leg_armor(0)|difficulty(18) ,imodbits_plate ],

 ["gg_col1_kettlehat1", "Kettle Hat Red", [("gg_col1_kettlehat1",0)], itp_merchandise| itp_fit_to_head| itp_covers_beard| itp_type_head_armor ,0,
  4460 , weight(4)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(15) ,imodbits_armor ],
 ["gg_col1_kettlehat2", "Kettle Hat Blue", [("gg_col1_kettlehat2",0)], itp_merchandise| itp_fit_to_head| itp_covers_beard| itp_type_head_armor ,0,
  4460 , weight(4)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(15) ,imodbits_armor ],
  ["gg_kettlehat1", "Mercenary Chapel Helmet", [("gg_kettlehat1",0)], itp_merchandise| itp_fit_to_head| itp_type_head_armor ,0,
   4460 , weight(4)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(15) ,imodbits_armor ], 
 ["gg_kettlehat2", "Mercenary Chapel Helmet", [("gg_kettlehat2",0)], itp_merchandise| itp_fit_to_head| itp_type_head_armor ,0,
  4450 , weight(4)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(15) ,imodbits_armor ], 
 ["clibanarius_helmet", "One-Piece Brimmed Helmet with Mask", [("clibanarius_helmet",0),("clibanarius_helmet_inv", ixmesh_inventory)], itp_merchandise| itp_fit_to_head| itp_covers_beard| itp_type_head_armor| itp_attach_armature ,0,
  4460 , weight(4)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(15) ,imodbits_armor ],
 ["byzantine_helmet_b", "Engraved Brimmed Helmet with Mask", [("byzantine_helmet_b",0),("byzantine_helmet_b_inv", ixmesh_inventory)], itp_merchandise| itp_fit_to_head| itp_covers_beard| itp_type_head_armor| itp_attach_armature ,0,
  200 , weight(4)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(15) ,imodbits_armor ],
 ["byzantine_helmet_b_red", "Red Brimmed Helmet with Mask", [("byzantine_helmet_b_red",0),("byzantine_helmet_b_red_inv", ixmesh_inventory)], itp_merchandise| itp_fit_to_head| itp_covers_beard| itp_type_head_armor| itp_attach_armature ,0,
  200 , weight(4)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(15) ,imodbits_armor ], #EXTRA
 ["pronoia_helmet", "Pronia Helmet", [("pronoia_helmet",0),("pronoia_helmet_inv", ixmesh_inventory)], itp_merchandise| itp_fit_to_head| itp_covers_beard| itp_type_head_armor| itp_attach_armature ,0,
  4460 , weight(4)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(15) ,imodbits_armor ],

 ["gg_heavy_swad_helmet", "Heavy Swad Helmet", [("gg_heavy_swad_helmet",0)], itp_merchandise| itp_fit_to_head| itp_covers_beard|  itp_type_head_armor ,0, ############ MAIN ############
  6000 , weight(5)|abundance(100)|head_armor(49)|body_armor(0)|leg_armor(0)|difficulty(18) ,imodbits_plate ],
 ["gg_swad_green", "Heavy Green Swad Helmet", [("gg_swad_green",0)], itp_merchandise| itp_fit_to_head| itp_covers_beard|  itp_type_head_armor ,0, ############ EXTRA  ############
  150 , weight(5)|abundance(100)|head_armor(49)|body_armor(0)|leg_armor(0)|difficulty(18) ,imodbits_plate ],
 ["gg_swad_blue", "Heavy Blue Swad Helmet", [("gg_swad_blue",0)], itp_merchandise| itp_fit_to_head| itp_covers_beard|  itp_type_head_armor ,0, ############ EXTRA  ############
  150 , weight(5)|abundance(100)|head_armor(49)|body_armor(0)|leg_armor(0)|difficulty(18) ,imodbits_plate ],
 ["gg_swad_yellow", "Heavy Yellow Swad Helmet", [("gg_swad_yellow",0)], itp_merchandise| itp_fit_to_head| itp_covers_beard|  itp_type_head_armor ,0, ############ EXTRA  ############
  150 , weight(5)|abundance(100)|head_armor(49)|body_armor(0)|leg_armor(0)|difficulty(18) ,imodbits_plate ],
 ["gg_swad_red", "Heavy Red Helmet", [("gg_swad_red",0)], itp_merchandise| itp_fit_to_head| itp_covers_beard|  itp_type_head_armor ,0, ############ EXTRA  ############
  150 , weight(5)|abundance(100)|head_armor(49)|body_armor(0)|leg_armor(0)|difficulty(18) ,imodbits_plate ],

 ["gg_pelt_hood", "Pelt Hood", [("gg_pelt_hood",0)], itp_merchandise| itp_type_head_armor| itp_civilian ,0, ############ MAIN  ############
  40, weight(0.1)|abundance(100)|head_armor(16)|body_armor(0)|leg_armor(0)|difficulty(0),imodbits_cloth],
 ["gg_hooded_nasal_helmet", "Hood with Nasal Helmet", [("gg_hooded_nasal_helmet",0)], itp_merchandise| itp_type_head_armor| itp_civilian ,0, ############ EXTRA  ############
  1500, weight(2)|abundance(100)|head_armor(33)|body_armor(0)|leg_armor(0)|difficulty(15),imodbits_armor], 

 ["gg_straw_hat_new", "Straw Hat", [("gg_straw_hat_new",0)], itp_merchandise| itp_type_head_armor| itp_civilian ,0,
  2, weight(0.1)|abundance(100)|head_armor(1)|body_armor(0)|leg_armor(0)|difficulty(0),imodbits_cloth],


                                                                                        ## GOLD AND GLORY REWARD HELMET BOLUMU ### 




  ["sallet_dark_open_helmet","Open Sallet", [("sallet_dark_open_helmet", 0),("sallet_inv_dark_open_helmet", ixmesh_inventory)], itp_type_head_armor|itp_attach_armature ,0, ############ MAIN  ############
   8500, weight(5.75)|abundance(100)|head_armor(53)|difficulty(21), imodbits_armor|imodbit_cracked, []], 
  ["sallet_dark_closed","Closed Sallet", [("sallet_dark_closed", 0),("sallet_inv_dark_closed", ixmesh_inventory)], itp_type_head_armor|itp_attach_armature|itp_merchandise ,0,    ############ MAIN ############
   8525, weight(5.75)|abundance(100)|head_armor(54)|difficulty(21), imodbits_armor|imodbit_cracked, []],
 
  ["sallet_white_open_helmet","Open White Sallet", [("sallet_white_open_helmet", 0),("sallet_inv_white_open_helmet", ixmesh_inventory)], itp_type_head_armor|itp_attach_armature ,0, ############ EXTRA  ############
   200, weight(5.75)|abundance(100)|head_armor(53)|difficulty(21), imodbits_armor|imodbit_cracked, []], 
  ["sallet_white_closed","Closed White Sallet", [("sallet_white_closed", 0),("sallet_inv_white_closed", ixmesh_inventory)], itp_type_head_armor|itp_attach_armature|itp_merchandise ,0, ############ EXTRA  ############
   300, weight(5.75)|abundance(100)|head_armor(54)|difficulty(21), imodbits_armor|imodbit_cracked, []], 

  ["sallet_black_open_helmet","Open Black Sallet", [("sallet_black_open_helmet", 0),("sallet_inv_black_open_helmet", ixmesh_inventory)], itp_type_head_armor|itp_attach_armature ,0, ############ EXTRA  ############
   200, weight(5.75)|abundance(100)|head_armor(53)|difficulty(21), imodbits_armor|imodbit_cracked, []], 
  ["sallet_black_closed","Closed Black Sallet", [("sallet_black_closed", 0),("sallet_inv_black_closed", ixmesh_inventory)], itp_type_head_armor|itp_attach_armature|itp_merchandise ,0, ############ EXTRA  ############
   300, weight(5.75)|abundance(100)|head_armor(54)|difficulty(21), imodbits_armor|imodbit_cracked, []], 

  ["reward_helmet_open_normal","Reward Open Sallet", [("reward_helmet_open", 0),("reward_inv_helmet_open", ixmesh_inventory)], itp_type_head_armor|itp_attach_armature ,0, ############ EXTRA  ############
   300, weight(5.75)|abundance(100)|head_armor(53)|difficulty(21), imodbits_armor|imodbit_cracked, []], 
  ["reward_helmet_closed","Reward Closed Sallet", [("reward_helmet_closed", 0),("reward_inv_closed", ixmesh_inventory)], itp_type_head_armor|itp_attach_armature|itp_merchandise  ,0, ############ EXTRA  ############
   500, weight(5.75)|abundance(100)|head_armor(54)|difficulty(21), imodbits_armor|imodbit_cracked, []], 

  ["narf_reward_b_closed1","Closed Reward Sallet", [("narf_reward_b_closed1", 0),("narf_inv_reward_b_closed1", ixmesh_inventory)], itp_type_head_armor|itp_attach_armature ,0, ############ MAIN  ############
   200, weight(5.75)|abundance(100)|head_armor(53)|difficulty(21), imodbits_armor|imodbit_cracked, []], 
 
  ["narf_reward_b_closed2","Closed Reward Sallet", [("narf_reward_b_closed2", 0),("narf_inv_reward_b_closed2", ixmesh_inventory)], itp_type_head_armor|itp_attach_armature ,0, ############ EXTRA  ############
   5650, weight(4.6)|abundance(100)|head_armor(48)|difficulty(18), imodbits_armor|imodbit_cracked, []], 

  ["narf_reward_b_open1","Open Reward Sallet", [("narf_reward_b_open1", 0),("narf_inv_reward_b_open1", ixmesh_inventory)], itp_type_head_armor|itp_attach_armature ,0, ############ EXTRA  ############
   200, weight(5.75)|abundance(100)|head_armor(53)|difficulty(21), imodbits_armor|imodbit_cracked, []], 

  ["narf_reward_b_open2","Open Reward Sallet", [("narf_reward_b_open2", 0),("narf_inv_reward_b_open2", ixmesh_inventory)], itp_type_head_armor|itp_attach_armature ,0, ############ EXTRA  ############
   200, weight(4.6)|abundance(100)|head_armor(48)|difficulty(18), imodbits_armor|imodbit_cracked, []],  

  ["crownedhelm", "Warlords Champion", [("crownedhelm",0)], itp_merchandise| itp_fit_to_head| itp_covers_beard|  itp_type_head_armor ,0, ########## TOURNEY CHAMPIONS
  0 , weight(5.5)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(20) ,imodbits_plate ],


################################################ -PK Yeni Eklenenler- #######################################################

 ["helm_saracin_j", "Sarranid Royal Helmet", [("helm_saracin_j", 0), ("inv_helm_saracin_j",ixmesh_inventory)], itp_type_head_armor|itp_attach_armature|itp_merchandise, 0,
  5130, weight(4.0) | abundance(100) | head_armor(45) | body_armor(0) | leg_armor(0) | difficulty(16), imodbits_armor ],

 ["arhelm_norig", "Arsar Helmet", [("arhelm_norig", 0)],  itp_type_head_armor|itp_merchandise, 0,
  5130, weight(4.0) | abundance(100) | head_armor(45) | body_armor(0) | leg_armor(0) | difficulty(16), imodbits_armor ],

 ["gulam_helm_b_market", "Reinforced Red Keffiyeh Helmet", [("gulam_helm_b_market", 0)],  itp_type_head_armor|itp_merchandise, 0,  ### Extra
  400, weight(1.8)| abundance(100) | head_armor(35) | body_armor(0) | leg_armor(0) | difficulty(9), imodbits_armor ],

 ["sar_infantry_helmet1", "Saranid Guard Helmet", [("sar_infantry_helmet1", 0)],  itp_type_head_armor|itp_merchandise, 0,
  3800, weight(3.3)| abundance(100) | head_armor(42) | body_armor(0) | leg_armor(0) | difficulty(14), imodbits_armor ],
 ["helm_saracin_c", "Sarranid Cavalry Helmet", [("helm_saracin_c",0)], itp_type_head_armor|itp_merchandise, 0,
  2750, weight(2.25)| abundance(100) | head_armor(38) | body_armor(0) | leg_armor(0) | difficulty(12), imodbits_armor ],
 ["north_noseguard", "New Bascinet", [("north_noseguard",0)], itp_type_head_armor|itp_merchandise, 0,
  1450, weight(1.6) | abundance(100) | head_armor(33) | body_armor(0) | leg_armor(0) | difficulty(9), imodbits_plate ],

  ["white_assassin_cape","White Assassin Cape", [("white_assassin_cape", 0)], itp_type_head_armor|itp_civilian, 0, ############ Combine ############   -    ############ MAIN  ############
   100, weight(1)|abundance(100)|head_armor(25)|difficulty(0) ,imodbits_armor ],

  ["brown_assassin_cape","Brown Assassin Cape", [("brown_assassin_cape", 0)], itp_type_head_armor|itp_civilian, 0, ############ Combine ############    -    ############ EXTRA  ############
   100, weight(1)|abundance(100)|head_armor(25)|difficulty(0) ,imodbits_armor ],

  ["green_assassin_cape","Green Assassin Cape", [("green_assassin_cape", 0)], itp_type_head_armor|itp_civilian, 0, ############ Combine ############    -    ############ EXTRA  ############
   100, weight(1)|abundance(100)|head_armor(25)|difficulty(0) ,imodbits_armor ],

  ["red_assassin_cape","Red Assassin Cape", [("red_assassin_cape", 0)], itp_type_head_armor|itp_civilian, 0, ############ Combine ############    -    ############ EXTRA  ############
   100, weight(1)|abundance(100)|head_armor(25)|difficulty(0) ,imodbits_armor ],

##  ["crown", "Crown", [("crown", 0)], itp_type_head_armor|itp_doesnt_cover_hair|itp_fit_to_head, 0,
##   70000, weight(1)|head_armor(33)|difficulty(9), imodbits_plate],

 
############################################################################ GOLD AND GLORY HEAD ARMORS END ############################################################################

#Cakebatter Heraldic start
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# Armour Head
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#-------------------------------------------------------------------------------------------------
# Great Helmets Heraldic Start
#-------------------------------------------------------------------------------------------------
["w_great_helmet_1_heraldic_primary_color", "Heraldic Round Winged Great Helmet", [("warlords_great_helmet_1_heraldic_mesh_wings1",0)], itp_type_head_armor|itp_covers_head,
  0,90000,weight(5.75)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(21),imodbits_plate,
  [(ti_on_init_item, [
    (store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_warlords_great_helmet_1_heraldic_primary_color", ":agent_no", ":troop_no"),
    (cur_item_add_mesh, "@warlords_great_helmet_1_heraldic_mesh_helmet"),
  ])]
],#Above item is heraldic version of: maciejowski_helmet_new - Remade wings, turned them 3d with wavy wings
["w_great_helmet_1v2_heraldic_primary_color", "Heraldic Pointy Winged Great Helmet Primary Color", [("warlords_great_helmet_1_heraldic_mesh_wings2",0)], itp_type_head_armor|itp_covers_head,
  0,900,weight(5.75)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(21),imodbits_plate,
  [(ti_on_init_item, [
    (store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_warlords_great_helmet_1_heraldic_primary_color", ":agent_no", ":troop_no"),
    (cur_item_add_mesh, "@warlords_great_helmet_1_heraldic_mesh_helmet"),
  ])]
],#Above item is heraldic version of: maciejowski_helmet_new - Remade wings, turned them 3d with zigzag wings
["w_great_helmet_1_heraldic_secondary_color", "Heraldic Round Winged Great Helmet Seconndary Color", [("warlords_great_helmet_1_heraldic_mesh_wings1",0)], itp_type_head_armor|itp_covers_head,
  0,900,weight(5.75)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(21),imodbits_plate,
  [(ti_on_init_item, [
    (store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_warlords_great_helmet_1_heraldic_secondary_color", ":agent_no", ":troop_no"),
    (cur_item_add_mesh, "@warlords_great_helmet_1_heraldic_mesh_helmet"),
  ])]
],#Above item is heraldic version of: maciejowski_helmet_new - Remade wings, turned them 3d with wavy wings
["w_great_helmet_1v2_heraldic_secondary_color", "Heraldic Pointy Winged Great Helmet Secondary Color", [("warlords_great_helmet_1_heraldic_mesh_wings2",0)], itp_type_head_armor|itp_covers_head,
  0,900,weight(5.75)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(21),imodbits_plate,
  [(ti_on_init_item, [
    (store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_warlords_great_helmet_1_heraldic_secondary_color", ":agent_no", ":troop_no"),
    (cur_item_add_mesh, "@warlords_great_helmet_1_heraldic_mesh_helmet"),
  ])]
],#Above item is heraldic version of: maciejowski_helmet_new - Remade wings, turned them 3d with zigzag wings
["w_great_helmet_1_heraldic_double_color", "Heraldic Round Winged Great Helmet Both Colors", [("warlords_great_helmet_1_heraldic_mesh_wings1",0)], itp_type_head_armor|itp_covers_head,
  0,900,weight(5.75)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(21),imodbits_plate,
  [(ti_on_init_item, [
    (store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_warlords_great_helmet_1_heraldic_double_color", ":agent_no", ":troop_no"),
    (cur_item_add_mesh, "@warlords_great_helmet_1_heraldic_mesh_helmet"),
  ])]
],#Above item is heraldic version of: maciejowski_helmet_new - Remade wings, turned them 3d with wavy wings
["w_great_helmet_1v2_heraldic_double_color", "Heraldic Pointy Winged Great Helmet Both Colors", [("warlords_great_helmet_1_heraldic_mesh_wings2",0)], itp_type_head_armor|itp_covers_head,
  0,900,weight(5.75)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(21),imodbits_plate,
  [(ti_on_init_item, [
    (store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_warlords_great_helmet_1_heraldic_double_color", ":agent_no", ":troop_no"),
    (cur_item_add_mesh, "@warlords_great_helmet_1_heraldic_mesh_helmet"),
  ])]
],#Above item is heraldic version of: maciejowski_helmet_new - Remade wings, turned them 3d with zigzag wings
["w_great_helmet_1_heraldic_double_color_inverted", "Heraldic Round Winged Great Helmet Both Colors Inverted", [("warlords_great_helmet_1_heraldic_mesh_wings1",0)], itp_type_head_armor|itp_covers_head,
  0,900,weight(5.75)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(21),imodbits_plate,
  [(ti_on_init_item, [
    (store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_warlords_great_helmet_1_heraldic_double_color_inverted", ":agent_no", ":troop_no"),
    (cur_item_add_mesh, "@warlords_great_helmet_1_heraldic_mesh_helmet"),
  ])]
],#Above item is heraldic version of: maciejowski_helmet_new - Remade wings, turned them 3d with wavy wings
["w_great_helmet_1v2_heraldic_double_color_inverted", "Heraldic Pointy Winged Great Helmet Both Colors Inverted", [("warlords_great_helmet_1_heraldic_mesh_wings2",0)], itp_type_head_armor|itp_covers_head,
  0,900,weight(5.75)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(21),imodbits_plate,
  [(ti_on_init_item, [
    (store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_warlords_great_helmet_1_heraldic_double_color_inverted", ":agent_no", ":troop_no"),
    (cur_item_add_mesh, "@warlords_great_helmet_1_heraldic_mesh_helmet"),
  ])]
],#Above item is heraldic version of: maciejowski_helmet_new - Remade wings, turned them 3d with zigzag wings

["w_great_helmet_2_heraldic_primary_color", "Heraldic Great Helmet with Mantle", [("warlords_great_helmet_2_heraldic_mesh_mantle",0)], itp_attach_armature|itp_type_head_armor|itp_covers_head,
  0,95000,weight(5.75)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(21) ,imodbits_plate,
  [(ti_on_init_item, [
    (store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_warlords_great_helmet_2_heraldic_primary_color", ":agent_no", ":troop_no"),
    (cur_item_add_mesh, "@warlords_great_helmet_2_heraldic_mesh_helmet1"),
  ])]
],#Above item is heraldic version of: dejawolf_great_helm_hat - New model, new texturing, rigged the mantle so it clips less through the body
["w_great_helmet_2v2_heraldic_primary_color", "Heraldic Great Helmet Mirrored with Mantle Primary Color", [("warlords_great_helmet_2_heraldic_mesh_mantle2",0)], itp_attach_armature|itp_type_head_armor|itp_covers_head,
  0,950,weight(5.75)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(21) ,imodbits_plate,
  [(ti_on_init_item, [
    (store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_warlords_great_helmet_2_heraldic_primary_color", ":agent_no", ":troop_no"),
    (cur_item_add_mesh, "@warlords_great_helmet_2_heraldic_mesh_helmet2"),
  ])]
],#Above item is heraldic version of: dejawolf_great_helm_hat - New model, new texturing, air holes both sids of the cheek, rigged the mantle so it clips less through the body
["w_great_helmet_2_heraldic_secondary_color", "Heraldic Great Helmet with Mantle Secondary Color", [("warlords_great_helmet_2_heraldic_mesh_mantle",0)], itp_attach_armature|itp_type_head_armor|itp_covers_head,
  0,950,weight(5.75)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(21) ,imodbits_plate,
  [(ti_on_init_item, [
    (store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_warlords_great_helmet_2_heraldic_secondary_color", ":agent_no", ":troop_no"),
    (cur_item_add_mesh, "@warlords_great_helmet_2_heraldic_mesh_helmet1"),
  ])]
],#Above item is heraldic version of: dejawolf_great_helm_hat - New model, new texturing, rigged the mantle so it clips less through the body
["w_great_helmet_2v2_heraldic_secondary_color", "Heraldic Great Helmet Mirrored with Mantle Secondary Color", [("warlords_great_helmet_2_heraldic_mesh_mantle2",0)], itp_attach_armature|itp_type_head_armor|itp_covers_head,
  0,950,weight(5.75)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(21) ,imodbits_plate,
  [(ti_on_init_item, [
    (store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_warlords_great_helmet_2_heraldic_secondary_color", ":agent_no", ":troop_no"),
    (cur_item_add_mesh, "@warlords_great_helmet_2_heraldic_mesh_helmet2"),
  ])]
],#Above item is heraldic version of: dejawolf_great_helm_hat - New model, new texturing, air holes both sids of the cheek, rigged the mantle so it clips less through the body
["w_great_helmet_2_heraldic_double_color", "Heraldic Great Helmet with Mantle Both Colors", [("warlords_great_helmet_2_heraldic_mesh_mantle",0)], itp_attach_armature|itp_type_head_armor|itp_covers_head,
  0,950,weight(5.75)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(21) ,imodbits_plate,
  [(ti_on_init_item, [
    (store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_warlords_great_helmet_2_heraldic_double_color", ":agent_no", ":troop_no"),
    (cur_item_add_mesh, "@warlords_great_helmet_2_heraldic_mesh_helmet1"),
  ])]
],#Above item is heraldic version of: dejawolf_great_helm_hat - New model, new texturing, rigged the mantle so it clips less through the body
["w_great_helmet_2v2_heraldic_double_color", "Heraldic Great Helmet Mirrored with Mantle Both Colors", [("warlords_great_helmet_2_heraldic_mesh_mantle2",0)], itp_attach_armature|itp_type_head_armor|itp_covers_head,
  0,950,weight(5.75)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(21) ,imodbits_plate,
  [(ti_on_init_item, [
    (store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_warlords_great_helmet_2_heraldic_double_color", ":agent_no", ":troop_no"),
    (cur_item_add_mesh, "@warlords_great_helmet_2_heraldic_mesh_helmet2"),
  ])]
],#Above item is heraldic version of: dejawolf_great_helm_hat - New model, new texturing, air holes both sids of the cheek, rigged the mantle so it clips less through the body
["w_great_helmet_2_heraldic_double_color_inverted", "Heraldic Great Helmet with Mantle Both Colors Inverted", [("warlords_great_helmet_2_heraldic_mesh_mantle",0)], itp_attach_armature|itp_type_head_armor|itp_covers_head,
  0,950,weight(5.75)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(21) ,imodbits_plate,
  [(ti_on_init_item, [
    (store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_warlords_great_helmet_2_heraldic_double_color_inverted", ":agent_no", ":troop_no"),
    (cur_item_add_mesh, "@warlords_great_helmet_2_heraldic_mesh_helmet1"),
  ])]
],#Above item is heraldic version of: dejawolf_great_helm_hat - New model, new texturing, rigged the mantle so it clips less through the body
["w_great_helmet_2v2_heraldic_double_color_inverted", "Heraldic Great Helmet Mirrored with Mantle Both Colors Inverted", [("warlords_great_helmet_2_heraldic_mesh_mantle2",0)], itp_attach_armature|itp_type_head_armor|itp_covers_head,
  0,950,weight(5.75)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(21) ,imodbits_plate,
  [(ti_on_init_item, [
    (store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_warlords_great_helmet_2_heraldic_double_color_inverted", ":agent_no", ":troop_no"),
    (cur_item_add_mesh, "@warlords_great_helmet_2_heraldic_mesh_helmet2"),
  ])]
],#Above item is heraldic version of: dejawolf_great_helm_hat - New model, new texturing, air holes both sids of the cheek, rigged the mantle so it clips less through the body

["w_great_helmet_3_heraldic_primary_color", "Heraldic Great Helmet Primary Color", [("warlords_great_helmet_3_heraldic_mesh_helmet",0)], itp_type_head_armor|itp_covers_head,
  0,8900,weight(5.75)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(21),imodbits_plate,
  [(ti_on_init_item, [
    (store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_warlords_great_helmet_3_heraldic_primary_color", ":agent_no", ":troop_no"),
  ])]
],#Above item is heraldic version of: great_helmet_new
["w_great_helmet_3_heraldic_secondary_color", "Heraldic Great Helmet Secondary Color", [("warlords_great_helmet_3_heraldic_mesh_helmet",0)], itp_type_head_armor|itp_covers_head,
  0,600,weight(5.75)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(21),imodbits_plate,
  [(ti_on_init_item, [
    (store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_warlords_great_helmet_3_heraldic_secondary_color", ":agent_no", ":troop_no"),
  ])]
],#Above item is heraldic version of: great_helmet_new
#-------------------------------------------------------------------------------------------------
# Great Helmets Heraldic Start
#-------------------------------------------------------------------------------------------------
#Cakebatter Heraldic end

        ["m_noel_helmet", "Red Hat", [("noel_helmet", 0)],  itp_type_head_armor|itp_civilian, 0,
         0, weight(0.0) | abundance(100) | head_armor(14) | body_armor(0) | leg_armor(0) | difficulty(0), imodbits_cloth ],

    ["m_head_end", "Head End", [("invisible",0)], itp_type_head_armor, 0, 0 , weight(0)|abundance(0)|head_armor(0)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],


        ####################################### HEAD ARMOR END ################################################################




 # BODY ARMOR



    # Light armor


    ["m_coarse_tunic", "Tunic with vest", [("coarse_tunic_a", 0)],  itp_type_body_armor |itp_civilian |itp_covers_legs|itp_merchandise, 0,                          50,   weight(1.0) | abundance(100) | head_armor(0) | body_armor(9)  | leg_armor(7)  | difficulty(0), imodbits_cloth ], 
    ["m_linen_tunic", "Linen Tunic", [("shirt_a", 0)],  itp_type_body_armor |itp_civilian |itp_covers_legs|itp_merchandise, 0,                                      90,   weight(1.0) | abundance(100) | head_armor(0) | body_armor(9)  | leg_armor(7)  | difficulty(0), imodbits_cloth ], 
    # ["m_vikingr_tunik_c", "Viking Tunic", [("vikingr_tunik_c", 0)],  itp_type_body_armor |itp_civilian |itp_covers_legs|itp_merchandise, 0,                         110,  weight(1.0) | abundance(100) | head_armor(0) | body_armor(9)  | leg_armor(7)  | difficulty(0), imodbits_cloth ],
    ["m_red_shirt", "Red Shirt", [("rich_tunic_a", 0)],  itp_type_body_armor |itp_civilian |itp_covers_legs|itp_merchandise, 0,                                     130,  weight(1.0) | abundance(100) | head_armor(0) | body_armor(9)  | leg_armor(7)  | difficulty(0), imodbits_cloth ],
    ["m_rawhide_coat", "Rawhide Coat", [("coat_of_plates_b", 0)],  itp_type_body_armor |itp_civilian |itp_covers_legs|itp_merchandise, 0,                           180,  weight(1.5) | abundance(100) | head_armor(0) | body_armor(10) | leg_armor(9)  | difficulty(0), imodbits_cloth ], 
    ["m_pelt_coat", "Pelt Coat", [("thick_coat_a", 0)], itp_type_body_armor|itp_civilian|itp_covers_legs|itp_merchandise, 0,                                        200,  weight(1.5) | abundance(100) | head_armor(0) | body_armor(11) | leg_armor(8)  | difficulty(0), imodbits_cloth ], 

    ["m_tunic_with_green_cape", "Tunic with Green Cowl", [("peasant_man_a", 0)],  itp_type_body_armor  |itp_covers_legs|itp_civilian|itp_merchandise, 0,  ##MAIN
     230,  weight(1.5) | abundance(100) | head_armor(0) | body_armor(11) | leg_armor(8)  | difficulty(0), imodbits_cloth ],
    ["m_tunic_with_green_hood", "Tunic with Green Hood", [("peasant_man_a", 0)],  itp_type_body_armor  |itp_covers_legs|itp_civilian, 0,  ##EXTRA
     10,  weight(1.5) | abundance(100) | head_armor(0) | body_armor(11) | leg_armor(8)  | difficulty(0), imodbits_cloth ],

    ["m_sarranid_cloth_robe", "Worn Robe", [("sar_robe", 0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,                                            250,  weight(1.75)| abundance(100) | head_armor(0) | body_armor(12) | leg_armor(9)  | difficulty(0), imodbits_cloth ], 
    ["m_sarranid_cloth_robe_black", "Black Worn Robe", [("sar_robe_b", 0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,                              260,  weight(1.75)| abundance(100) | head_armor(0) | body_armor(12) | leg_armor(9)  | difficulty(0), imodbits_cloth ], 
    ["m_sarranid_jacket", "Sarranid Jacket", [("zimke_bashibazouk_robe_a", 0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,                          290,  weight(1.75)| abundance(100) | head_armor(0) | body_armor(13) | leg_armor(8)  | difficulty(0), imodbits_cloth ], 
    ["m_tabard", "Tabard", [("tabard_b", 0)],  itp_type_body_armor  |itp_covers_legs |itp_civilian|itp_merchandise, 0,                                              300,  weight(2.0) | abundance(100) | head_armor(0) | body_armor(14) | leg_armor(9)  | difficulty(0), imodbits_cloth ], 
    ["m_steppe_armor", "Steppe Armor", [("lamellar_leather", 0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,                                        350,  weight(2.25)| abundance(100) | head_armor(0) | body_armor(15) | leg_armor(8)  | difficulty(0), imodbits_cloth ], 
    ["m_nobleman_outfit", "Nobleman Outfit", [("nobleman_outfit_b_new", 0)], itp_type_body_armor|itp_covers_legs|itp_civilian|itp_merchandise, 0,                   400,  weight(2.0) | abundance(100) | head_armor(0) | body_armor(14) | leg_armor(9)  | difficulty(0), imodbits_cloth ],
    ["m_fur_coat", "Fur Coat", [("fur_coat", 0)],  itp_type_body_armor  |itp_covers_legs |itp_civilian|itp_merchandise, 0,                                          500,  weight(2.5) | abundance(100) | head_armor(0) | body_armor(15) | leg_armor(10) | difficulty(0), imodbits_armor ], 
    ["m_nomad_vest", "Nomad Vest", [("nomad_vest_new",0)], itp_type_body_armor|itp_covers_legs|itp_civilian|itp_merchandise, 0,                                     550,  weight(2.5) | abundance(100) | head_armor(0) | body_armor(15) | leg_armor(10) | difficulty(0), imodbits_cloth ],
    ["m_archers_vest", "Sarranid Padded Vest", [("archers_vest", 0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,                                    700,  weight(2.5) | abundance(100) | head_armor(0) | body_armor(16) | leg_armor(8)  | difficulty(0), imodbits_cloth ], 
    ["m_nomad_armor", "Nomad Armor", [("nomad_armor_new",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                                               850,  weight(2.5) | abundance(100) | head_armor(0) | body_armor(17) | leg_armor(8)  | difficulty(0), imodbits_cloth ],
    ["m_khergit_armor", "Khergit Armor", [("khergit_armor_new",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                                         900,  weight(2.5) | abundance(100) | head_armor(0) | body_armor(17) | leg_armor(8)  | difficulty(0), imodbits_cloth ],
    ["m_arena_tunic_blue", "Blue Tunic", [("arena_tunicB_new", 0)], itp_type_body_armor |itp_covers_legs|itp_merchandise, 0,  ##MAIN
     1100, weight(3.0) | abundance(100) | head_armor(0) | body_armor(19) | leg_armor(9)  | difficulty(0), imodbits_cloth ], 
    ["m_arena_tunic_red", "Red Tunic", [("arena_tunicR_new", 0)], itp_type_body_armor |itp_covers_legs|itp_merchandise, 0,  ##EXTRA
     100, weight(3.0) | abundance(100) | head_armor(0) | body_armor(19) | leg_armor(9)  | difficulty(0), imodbits_cloth ], 
    ["m_arena_tunic_green", "Green Tunic", [("arena_tunicG_new", 0)], itp_type_body_armor |itp_covers_legs|itp_merchandise, 0,  ##EXTRA
     100, weight(3.0) | abundance(100) | head_armor(0) | body_armor(19) | leg_armor(9)  | difficulty(0), imodbits_cloth ], 
    ["m_arena_tunic_yellow", "Yellow Tunic", [("arena_tunicY_new", 0)], itp_type_body_armor |itp_covers_legs|itp_merchandise, 0,  ##EXTRA
     100, weight(3.0) | abundance(100) | head_armor(0) | body_armor(19) | leg_armor(9)  | difficulty(0), imodbits_cloth ], 
    ["m_arena_tunic_white", "White Tunic ", [("arena_tunicW_new", 0)], itp_type_body_armor |itp_covers_legs|itp_merchandise, 0,  ##EXTRA
     100, weight(3.0) | abundance(100) | head_armor(0) | body_armor(19) | leg_armor(9)  | difficulty(0), imodbits_cloth ], 
    ["m_red_gambeson", "Red Gambeson", [("red_gambeson_a", 0)],  itp_type_body_armor|itp_covers_legs|itp_civilian|itp_merchandise, 0,                               1200, weight(3.0) | abundance(100) | head_armor(0) | body_armor(20) | leg_armor(8)  | difficulty(0), imodbits_cloth ], 
    ["m_padded_cloth", "Aketon", [("padded_cloth_a", 0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,                                                1350, weight(3.5) | abundance(100) | head_armor(0) | body_armor(20) | leg_armor(10) | difficulty(0), imodbits_cloth ],
    ["m_aketon_green", "Padded Cloth", [("padded_cloth_b", 0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,                                          1450, weight(3.5) | abundance(100) | head_armor(0) | body_armor(20) | leg_armor(10) | difficulty(0), imodbits_cloth ], 
    ["m_aketon_heraldic", "Heraldic Padded Cloth", [("m_padded_cloth_heraldic", 0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,                     1500, weight(3.5) | abundance(100) | head_armor(0) | body_armor(20) | leg_armor(10) | difficulty(0), imodbits_cloth, [ (ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_m_padded_cloth_heraldic", ":agent_no", ":troop_no")]) ] ], 
    ["m_gambeson_heraldic", "Heraldic Gambeson", [("narf_gambeson_heraldic", 0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,                        1650, weight(3.25)| abundance(100) | head_armor(0) | body_armor(21) | leg_armor(8)  | difficulty(0), imodbits_cloth, [ (ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_m_gambeson_heraldic", ":agent_no", ":troop_no")]) ] ], 
    ["m_archer_armor_2", "Dark Gambeson with Cape", [("cwe_archer_armor_2", 0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0,                            1700, weight(3.75)| abundance(100) | head_armor(0) | body_armor(21) | leg_armor(10) | difficulty(0), imodbits_cloth ],
    ["m_archer_armor_1", "Black Gambeson with Cape", [("cwe_archer_armor_1", 0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0,                           1720, weight(3.75)| abundance(100) | head_armor(0) | body_armor(21) | leg_armor(10) | difficulty(0), imodbits_cloth ],
    ["m_leather_jacket", "Leather Jacket", [("leather_jacket_new",0)], itp_type_body_armor|itp_covers_legs|itp_civilian|itp_merchandise, 0,                         1800, weight(4.0) | abundance(100) | head_armor(0) | body_armor(22) | leg_armor(9)  | difficulty(7), imodbits_cloth ],
    ["m_light_leather", "Light Leather", [("m_light_leather", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                                          1900, weight(4.0) | abundance(100) | head_armor(0) | body_armor(22) | leg_armor(9)  | difficulty(7), imodbits_armor ], 
    ["m_ragged_outfit", "Ragged Outfit", [("ragged_outfit_a_new", 0)],  itp_type_body_armor |itp_civilian |itp_covers_legs|itp_merchandise, 0,                      2000, weight(4.5) | abundance(100) | head_armor(0) | body_armor(23) | leg_armor(10) | difficulty(7), imodbits_cloth ], 
    ["m_sarranid_leather_armor", "Sarranid Leather Armor", [("sarranid_leather_armor", 0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,              2100, weight(4.5) | abundance(100) | head_armor(0) | body_armor(23) | leg_armor(10) | difficulty(7), imodbits_armor ], 
    ["m_leather_vest", "Long Leather Vest", [("leather_vest_a", 0)],  itp_type_body_armor  |itp_covers_legs|itp_civilian|itp_merchandise, 0,                        2200, weight(4.5) | abundance(100) | head_armor(0) | body_armor(23) | leg_armor(10) | difficulty(7), imodbits_cloth ], 
    ["m_padded_leather", "Padded Leather", [("leather_armor_b", 0)],  itp_type_body_armor  |itp_covers_legs|itp_civilian|itp_merchandise, 0,                        2400, weight(4.5) | abundance(100) | head_armor(0) | body_armor(24) | leg_armor(8)  | difficulty(7), imodbits_cloth ], 
    ["m_leather_jerkin", "Leather Jerkin", [("ragged_leather_jerkin", 0)],  itp_type_body_armor |itp_civilian |itp_covers_legs|itp_merchandise, 0,                  2600, weight(5.0) | abundance(100) | head_armor(0) | body_armor(25) | leg_armor(10) | difficulty(7), imodbits_cloth ], 

    ["m_padded_leather_2", "Heavy Padded Leather", [("fred_padded_leather", 0)],  itp_type_body_armor|itp_covers_legs|itp_civilian|itp_merchandise, 0,    ### MAIN 
     2800, weight(5.5) | abundance(100) | head_armor(0) | body_armor(26) | leg_armor(10) | difficulty(7), imodbits_cloth ], 
    ["m_padded_leather_2_with_cowl", "Heavy Padded Leather with Cowl", [("fred_padded_leather_cowl", 0)],  itp_type_body_armor|itp_covers_legs|itp_civilian, 0, ### EXTRA
     100, weight(5.5) | abundance(100) | head_armor(0) | body_armor(26) | leg_armor(10) | difficulty(7), imodbits_cloth ], 
    ["m_padded_leather_2_with_hood", "Heavy Padded Leather with Hood", [("fred_padded_leather_cowl", 0)],  itp_type_body_armor|itp_covers_legs|itp_civilian, 0, ### EXTRA
     130, weight(5.5) | abundance(100) | head_armor(0) | body_armor(26) | leg_armor(10) | difficulty(7), imodbits_cloth ], 

    ["m_tribal_warrior_outfit", "Tribal Warrior Outfit", [("tribal_warrior_outfit_a_new", 0)], itp_type_body_armor|itp_covers_legs|itp_civilian|itp_merchandise, 0, 3000, weight(6.0) | abundance(100) | head_armor(0) | body_armor(27) | leg_armor(11) | difficulty(7), imodbits_cloth ],

    ["m_light_studded_leather_coat", "Studded Leather Coat", [("rathos_leather_armor_1", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,               3100, weight(5.5) | abundance(100) | head_armor(0) | body_armor(27) | leg_armor(9)  | difficulty(7), imodbits_cloth ], 

    ["m_leather_armor", "Leather Armor", [("tattered_leather_armor_a", 0)],  itp_type_body_armor |itp_covers_legs|itp_merchandise, 0,     ### MAIN 
     3300, weight(6.0) | abundance(100) | head_armor(0) | body_armor(27) | leg_armor(11) | difficulty(7), imodbits_cloth ],
    ["m_leather_armor_pauldrons", "Leather Armor with Pauldrons", [("m_tattered_leather_armor_a_pauldrons", 0)],  itp_type_body_armor |itp_covers_legs, 0,  ### EXTRA
     300, weight(6.25)| abundance(100) | head_armor(0) | body_armor(28) | leg_armor(11) | difficulty(7), imodbits_cloth ],

    ["m_leather_scale_armor", "Leather Scale Armor", [("zimke_archer_armor", 0)],  itp_type_body_armor |itp_covers_legs|itp_merchandise, 0,     ### MAIN 
     3400, weight(6.0) | abundance(100) | head_armor(0) | body_armor(28) | leg_armor(9)  | difficulty(7), imodbits_cloth ],
    ["m_leather_scale_armor_with_hood", "Leather Scale Armor with Hood", [("zimke_archer_armor", 0)],  itp_type_body_armor |itp_covers_legs, 0,  ### EXTRA
     30, weight(6.0) | abundance(100) | head_armor(0) | body_armor(28) | leg_armor(9)  | difficulty(7), imodbits_cloth ],

    ["m_sergeant_armor_3", "Dark Red Gambeson with Mail", [("cwe_sergeant_armor_3", 0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0,      ### MAIN 
     3800, weight(7.2)| abundance(100) | head_armor(0) | body_armor(29) | leg_armor(9) | difficulty(7), imodbits_cloth ],
    ["m_sergeant_armor_2", "Black Gambeson with Mail", [("cwe_sergeant_armor_2", 0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0,  ### EXTRA
     100, weight(7.2)| abundance(100) | head_armor(0) | body_armor(29) | leg_armor(9) | difficulty(7), imodbits_cloth ],
    ["m_sergeant_armor_1", "Blue and Red Gambeson with Mail", [("cwe_sergeant_armor_1", 0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0,   ### EXTRA
     100, weight(7.2)| abundance(100) | head_armor(0) | body_armor(29) | leg_armor(9) | difficulty(7), imodbits_cloth ],

    ["m_lamellar_vest", "White Lamellar Vest", [("lamellar_vest_a", 0)], itp_type_body_armor |itp_civilian |itp_covers_legs|itp_merchandise, 0,      ### MAIN
     3500, weight(7.2) | abundance(100) | head_armor(0) | body_armor(29) | leg_armor(9) | difficulty(8), imodbits_cloth ],
    ["m_lamellar_vest_khergit", "Red Lamellar Vest", [("lamellar_vest_b", 0)], itp_type_body_armor |itp_civilian |itp_covers_legs|itp_merchandise, 0,   ### EXTRA
     100, weight(7.2) | abundance(100) | head_armor(0) | body_armor(29) | leg_armor(9) | difficulty(8), imodbits_cloth ], 
    ["m_lamellar_vest_black", "Black Lamellar Vest", [("lamellar_vest_black", 0)], itp_type_body_armor |itp_civilian |itp_covers_legs|itp_merchandise, 0,   ### EXTRA
     100, weight(7.2) | abundance(100) | head_armor(0) | body_armor(29) | leg_armor(9) | difficulty(8), imodbits_cloth ], 
	



    # Medium armor
    ["mailsar", "Sarranid Mailsar", [("mailsar", 0)], itp_type_body_armor |itp_civilian |itp_covers_legs|itp_merchandise, 0,
     3700, weight(7.2) | abundance(100) | head_armor(0) | body_armor(29) | leg_armor(9) | difficulty(8), imodbits_cloth ],

    ["m_heraldic_mail_with_tunic_b", "Light Heraldic Mail", [("heraldic_armor_new_c", 0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,               3650, weight(7.2)  | abundance(100) | head_armor(0) | body_armor(29) | leg_armor(9) | difficulty(10), imodbits_armor, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_heraldic_armor_c", ":agent_no", ":troop_no")])]], 
    # ["m_gambeson-vip", "Light Brigandine With Cuisses", [("gambeson-vip", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                             3850, weight(7)  | abundance(100) | head_armor(0) | body_armor(32) | leg_armor(8)  | difficulty(10), imodbits_armor ],
    ["m_peasant_mail", "Light Mail", [("fred_peasant_mail", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                                           3900, weight(7.2)  | abundance(100) | head_armor(0) | body_armor(30) | leg_armor(4)  | difficulty(10), imodbits_armor ],
    # ["m_lambert_body", "Lambert Armor", [("lambert_body", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                                             4050, weight(7)  | abundance(100) | head_armor(0) | body_armor(32) | leg_armor(8)  | difficulty(10), imodbits_armor ], #user SLAVA12341
    # ["m_armour_temeria", "Temeria Light Armor", [("armour_temeria", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                                   4050, weight(7)  | abundance(100) | head_armor(0) | body_armor(32) | leg_armor(8)  | difficulty(10), imodbits_armor ], #clan Nilfgaard Empire
    # ["m_leather_guardsman", "Leather Hambeson", [("leather_guardsman", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                                4050, weight(7)  | abundance(100) | head_armor(0) | body_armor(32) | leg_armor(8)  | difficulty(10), imodbits_armor ], #clan Dungeons and Dragons
    ["m_byrnie", "Byrnie", [("byrnie_a_new", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                                                          4100, weight(7.6)  | abundance(100) | head_armor(0) | body_armor(30) | leg_armor(10) | difficulty(11), imodbits_armor ], 
    ["m_byrnie_b", "Byrnie", [("byrnie_b_new", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                                                          100, weight(7.6)  | abundance(100) | head_armor(0) | body_armor(30) | leg_armor(10) | difficulty(11), imodbits_armor ], 
    ["m_byrnie_c", "Byrnie", [("byrnie_c_new", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                                                          100, weight(7.6)  | abundance(100) | head_armor(0) | body_armor(30) | leg_armor(10) | difficulty(11), imodbits_armor ], 
    ["m_byrnie_d", "Byrnie", [("byrnie_d_new", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                                                          100, weight(7.6)  | abundance(100) | head_armor(0) | body_armor(30) | leg_armor(10) | difficulty(11), imodbits_armor ], 
    ["m_byrnie_e", "Byrnie", [("byrnie_e_new", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                                                          100, weight(7.6)  | abundance(100) | head_armor(0) | body_armor(30) | leg_armor(10) | difficulty(11), imodbits_armor ], 
    ["m_byrnie_f", "Byrnie", [("byrnie_f_new", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                                                          100, weight(7.6)  | abundance(100) | head_armor(0) | body_armor(30) | leg_armor(10) | difficulty(11), imodbits_armor ], 



    ["m_arena_armor_red", "Mail with Red Tunic", [("arena_armorR_new", 0)], itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,  ### MAIN 
     4400, weight(8)  | abundance(100) | head_armor(0) | body_armor(32) | leg_armor(8) | difficulty(12), imodbits_armor ], 
    ["m_arena_armor_blue", "Mail with Blue Tunic", [("arena_armorB_new", 0)], itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,  ### EXTRA
     100, weight(8)  | abundance(100) | head_armor(0) | body_armor(32) | leg_armor(8) | difficulty(12), imodbits_armor ], 
    ["m_arena_armor_green", "Mail with Green Tunic", [("arena_armorG_new", 0)], itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,  ### EXTRA
     100, weight(8)  | abundance(100) | head_armor(0) | body_armor(32) | leg_armor(8) | difficulty(12), imodbits_armor ], 
    ["m_arena_armor_yellow", "Mail with Yellow Tunic", [("arena_armorY_new", 0)], itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,  ### EXTRA
     100, weight(8)  | abundance(100) | head_armor(0) | body_armor(32) | leg_armor(8) | difficulty(12), imodbits_armor ], 
    ["m_arena_armor_white", "Mail with White Tunic", [("arena_armorW_new", 0)], itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,  ### EXTRA
     100, weight(8)  | abundance(100) | head_armor(0) | body_armor(32) | leg_armor(8) | difficulty(12), imodbits_armor ], 
    ["m_heraldic_mail_with_tunic", "Heraldic Mail", [("heraldic_armor_new_b", 0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,  ### EXTRA
     400, weight(8)  | abundance(100) | head_armor(0) | body_armor(32) | leg_armor(8) | difficulty(12), imodbits_armor, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_heraldic_armor_b", ":agent_no", ":troop_no")])]], 
    ["arsar2", "Arsar Armor", [("arsar2", 0)], itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,  
     4450, weight(8)  | abundance(100) | head_armor(0) | body_armor(32) | leg_armor(8) | difficulty(12), imodbits_armor ], 

    ["m_khergit_coat_over_lamellar", "Coat over Lamellar Cuirass", [("zimke_mongol_armor", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,            4850, weight(13) | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_cloth ],
    ["m_caravan_guard_armor", "Rich Coat over Lamellar Cuirass", [("cwe_securiti_caravan_crusader", 0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0,    65000,weight(7.2) | abundance(100) | head_armor(0) | body_armor(30) | leg_armor(4) | difficulty(7), imodbits_cloth ],
    ["m_sarranid_cavalry_robe", "Cavalry Robe", [("arabian_armor_a", 0)],  itp_type_body_armor  |itp_covers_legs |itp_civilian|itp_merchandise, 0,                  4900, weight(13) | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_armor ], 
    ["m_mail_hauberk", "Mail Hauberk", [("hauberk_a_new", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                                             5100, weight(13) | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_armor ], 
    ["m_mail_shirt", "Mail Shirt", [("mail_shirt_a", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                                                  5250, weight(13) | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_armor ], 
    ["m_palace_guard_armor", "Blue Gambeson over Mail Shirt", [("zimke_palace_guard", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,
     5400, weight(13) | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_armor ], 
    # ["m_haubergeon", "Haubergeon", [("haubergeon_c", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                                                  5500, weight(12) | abundance(100) | head_armor(0) | body_armor(39) | leg_armor(11) | difficulty(14), imodbits_armor ],

    ["m_studded_leather_coat_2", "Studded Leather Coat over Mail Jr", [("leather_armor_padded1", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,
     5790, weight(13) | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_armor ], 

    ["m_studded_leather_coat", "Studded Leather Coat over Mail", [("leather_armor_a", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,   ##### MAIN
     5800, weight(13) | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_armor ],
    ["gg_studded_blue", "Studded Leather Coat Blue over Mail", [("gg_studded_blue", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,   ##### EXTRA
     100, weight(13) | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_armor ],
    ["gg_studded_red", "Studded Leather Coat Red over Mail", [("gg_studded_red", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,   ##### EXTRA
     100, weight(13) | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_armor ],
    ["gg_studded_black", "Studded Leather Coat Black over Mail", [("gg_studded_black", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,   ##### EXTRA
     100, weight(13) | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_armor ],
    ["gg_studded_white", "Studded Leather Coat White over Mail", [("gg_studded_white", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,   ##### EXTRA
     100, weight(13) | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_armor ],


    ["m_surcoat_over_mail", "Surcoat over Mail", [("m_surcoat_over_mail", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                              6100, weight(13) | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_armor ], 
    ["m_surcoat_over_mail_red", "Red Surcoat over Mail", [("mail_long_surcoat_new",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                     6250, weight(13) | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_armor ],
    ["m_surcoat_over_mail_green", "Green Surcoat over Mail", [("surcoat_over_mail_new",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                 6300, weight(13) | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_armor ],
    ["m_sarranid_mail_shirt", "Sarranid Mail Shirt", [("sarranian_mail_shirt", 0)],  itp_type_body_armor  |itp_covers_legs|itp_civilian|itp_merchandise, 0,         6400, weight(13) | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_armor ], 

    ["m_vaegir_kuyak_a", "Dark Kuyak", [("kuyak_a", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,
     9500, weight(16) | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ], 
    ["m_vaegir_kuyak_b", "Brown Kuyak", [("kuyak_b", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,
     9550, weight(16) | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ],

    ["m_heraldic_mail_with_tabard", "Heraldic Mail with Tabard", [("heraldic_armor_new_d", 0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,          7010, weight(13) | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_armor, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_heraldic_armor_d", ":agent_no", ":troop_no")])]], 
    ["m_heraldic_mail_with_surcoat", "Heraldic Mail with Surcoat", [("heraldic_armor_new_a", 0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,        7130, weight(13) | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_armor, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_heraldic_armor_a", ":agent_no", ":troop_no")])]], 

    # Heavy armor


    ["m_lamellar_armor", "Khergit Guard Armor", [("lamellar_armor_b", 0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,                     ######## 
     7400,  weight(13)   | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_armor ],



    ["m_arabian_armor_b", "Sarranid Guard Armor", [("arabian_armor_b", 0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,                     ######## MAIN
     7800,  weight(13)   | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_armor ],
    ["gg_arabian_armor_purple", "Purple Sarranid Guard Armor", [("gg_arabian_armor_purple", 0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,                    ######## EXTRA
     100,  weight(13)   | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_armor ],
    ["gg_arabian_armor_red", "Red Sarranid Guard Armor", [("gg_arabian_armor_red", 0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,                     ########  EXTRA
     100,  weight(13)   | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_armor ],
    ["gg_arabian_armor_blue", "Blue Sarranid Guard Armor", [("gg_arabian_armor_blue", 0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,                     ########  EXTRA
     100,  weight(13)   | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_armor ],
    ["gg_arabian_armor_yellow", "Yellow Sarranid Guard Armor", [("gg_arabian_armor_yellow", 0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,                     ######## EXTRA 
     100,  weight(13)   | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_armor ],
    ["gg_arabian_armor_pink", "Pink Sarranid Guard Armor", [("gg_arabian_armor_pink", 0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,                     ########  EXTRA
     100,  weight(13)   | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_armor ],
    ["gg_arabian_armor_grey", "Grey Sarranid Guard Armor", [("gg_arabian_armor_grey", 0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,                     ########  EXTRA
     100,  weight(13)   | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_armor ],
    ["gg_arabian_armor_green", "Green Sarranid Guard Armor", [("gg_arabian_armor_green", 0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,                     ########  EXTRA
     100,  weight(13)   | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_armor ],


    ["m_sarranid_mail_with_plates", "Sarranid Armor with Plates", [("cwe_armor_medium_tyrk_d", 0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0,         10300,  weight(16) | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ],
    # ["m_transitional_plate_harness_01_cape", "Transitional Plate Armor", [("transitional_plate_harness_01_cape", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 8270,  weight(14.5) | abundance(100) | head_armor(0) | body_armor(43) | leg_armor(11) | difficulty(15), imodbits_armor ], #clan RKS

    ["m_light_vaegir_lamellar_a", "Vaegir Guard Armor", [("rus_lamellar_a", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                     ######## MAIN ########
     9100,  weight(16)   | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ],                        
    ["m_light_vaegir_lamellar_b", "Vaegir Guard Armor with Green Tunic", [("rus_lamellar_b", 0)], itp_type_body_armor|itp_covers_legs, 0,                     ######## EXTRA ########
     100,  weight(16)   | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ],

    ["m_surcoat_over_mail_with_plates", "Mail with Plated Jacket", [("btwk_armor_24",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                   8900,  weight(16)   | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ],
    # ["m_vaegir_scale_armor", "Vaegir Scale Armor", [("rus_scale", 0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,                                   9220,  weight(16)   | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(14) | difficulty(16), imodbits_armor ],
    # ["m_rough_ring_leather", "Byrnie", [("rough_ring_leather", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                                        9700,  weight(16)   | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(14) | difficulty(16), imodbits_armor ],
    ["m_khergit_guard_armor", "Khergit Lamellar Armor", [("lamellar_armor_a", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                          10170, weight(16)   | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ],

    ["m_scale_armor", "Scale Armor", [("lamellar_armor_e", 0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,                    ######## MAIN ########
     11160, weight(16)   | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ],
    ["m_scale_armor_kk", "Scale Armor with Kneecops", [("m_lamellar_armor_e_kk", 0)], itp_type_body_armor|itp_covers_legs, 0,                    ######## EXTRA ########   
     600, weight(16) | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ],
    ["m_scale_armor_cuisses", "Scale Armor with Plate Cuisses", [("m_lamellar_armor_e_cuisses", 0)], itp_type_body_armor|itp_covers_legs, 0,                     ######## EXTRA ########  
     1000, weight(16)   | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ],

    # ["m_sellsword_plate_armor_3", "Guardians Winged Armor", [("sellsword_plate_armor_3", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,              11700, weight(17)   | abundance(100) | head_armor(0) | body_armor(47) | leg_armor(10) | difficulty(16), imodbits_armor ], #clan Guardians
    # ["m_highlander_spearman_sash", "Scotich Pituch Light Armour", [("highlander_spearman_sash", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,       11700, weight(17)   | abundance(100) | head_armor(0) | body_armor(47) | leg_armor(10) | difficulty(16), imodbits_armor ], #clan Kingdom of Scotland
    # ["m_thoniara_armor", "Guardian Innos Armor", [("thoniara_armor", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                                  11700, weight(17)   | abundance(100) | head_armor(0) | body_armor(47) | leg_armor(10) | difficulty(16), imodbits_armor ], #clan Gothic
    # ["m_brigandine_black", "Black Canvas Brigandine", [("m_brigandine_black", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                         12100, weight(18)   | abundance(100) | head_armor(0) | body_armor(46) | leg_armor(14) | difficulty(17), imodbits_armor ],
    # ["m_brigandine_red", "Red Leather Brigandine", [("brigandine_b", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                                  12550, weight(18)   | abundance(100) | head_armor(0) | body_armor(46) | leg_armor(14) | difficulty(17), imodbits_armor ],
    # ["m_brigandine_c", "Blue Brigandine", [("brigandine_c", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                                           12600, weight(18)   | abundance(100) | head_armor(0) | body_armor(46) | leg_armor(14) | difficulty(17), imodbits_armor ], 
    # ["m_brigandine_f", "Yellow Brigandine", [("brigandine_f", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                                         12700, weight(18)   | abundance(100) | head_armor(0) | body_armor(46) | leg_armor(14) | difficulty(17), imodbits_armor ], 
    # ["m_brigandine_g", "Green Brigandine", [("brigandine_g", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                                          12800, weight(18)   | abundance(100) | head_armor(0) | body_armor(46) | leg_armor(14) | difficulty(17), imodbits_armor ], 
    # ["m_brigandine_h", "White Brigandine", [("brigandine_h", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                                          12900, weight(18)   | abundance(100) | head_armor(0) | body_armor(46) | leg_armor(14) | difficulty(17), imodbits_armor ], 
    # ["m_scale_mail", "Scaly Armor With Chain Mail", [("scale_mail", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                                   13850, weight(18)   | abundance(100) | head_armor(0) | body_armor(46) | leg_armor(14) | difficulty(17), imodbits_armor ], 
    ["m_drz_lamellar_armor", "Vaegir Lamellar Armor", [("drz_lamellar_armor", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                         14210, weight(16) | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ],
    ["m_banded_armor", "Banded Armor", [("banded_armor_a", 0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,                                          15030, weight(23)   | abundance(100) | head_armor(0) | body_armor(48) | leg_armor(16) | difficulty(21), imodbits_armor ],
    ["m_serbian_lamellar", "Heavy Scale Armor", [("zimke_serbian_lamellar", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                           15700, weight(23)   | abundance(100) | head_armor(0) | body_armor(48) | leg_armor(16) | difficulty(21), imodbits_armor ],
    ["m_mamluke_mail", "Mamluke Mail", [("sarranid_elite_cavalary", 0)],  itp_type_body_armor |itp_covers_legs|itp_civilian|itp_merchandise, 0,                     16150, weight(23)   | abundance(100) | head_armor(0) | body_armor(48) | leg_armor(16) | difficulty(21), imodbits_armor ],
    ["m_cuir_bouilli", "Cuir Bouilli", [("cuir_bouilli_a", 0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,
     17050, weight(23)   | abundance(100) | head_armor(0) | body_armor(48) | leg_armor(16) | difficulty(21), imodbits_plate ],
    # ["m_churburg_gambeson", "Churburg Gambeson", [("churburg_gambeson", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                               17200, weight(21)   | abundance(100) | head_armor(0) | body_armor(48) | leg_armor(16) | difficulty(18), imodbits_armor ], 

  ["m_early_transitional_heraldic","Heraldic Mail and Plate", [("early_transitional_heraldic", 0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_doesnt_cover_hair, 0,19700, weight(23)|abundance(100)|body_armor(48)|leg_armor(16)|difficulty(21), imodbits_armor, [
    (ti_on_init_item, [
      (store_trigger_param_1, ":var0"),
      (store_trigger_param_2, ":var1"),
      (call_script, "script_shield_item_set_banner", "tableau_m_early_transitional_heraldic", ":var0", ":var1"),
    ]),
   ]],
  ["m_early_transitional_ailettes","Mail and Plate with Ailettes", [("early_transitional_ailettes", 0)], itp_type_body_armor|itp_covers_legs|itp_doesnt_cover_hair, 0,300, weight(23)|abundance(100)|body_armor(48)|leg_armor(16)|difficulty(21), imodbits_armor, [
    (ti_on_init_item, [
      (store_trigger_param_1, ":var0"),
      (store_trigger_param_2, ":var1"),
      (call_script, "script_shield_item_set_banner", "tableau_m_early_transitional_ailettes", ":var0", ":var1"),
    ]),
   ]],

    # ["m_milanese_armour", "Milanese Armor", [("milanese_armour_new", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                                  20200, weight(23)   | abundance(100) | head_armor(0) | body_armor(50) | leg_armor(16) | difficulty(20), imodbits_armor ], #user R1ke
    # ["m_armor_19", "Elite Metal Lamellar Armor", [("armor_19", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                                        20200, weight(23)   | abundance(100) | head_armor(0) | body_armor(50) | leg_armor(16) | difficulty(20), imodbits_armor ], #user Commander
    # ["m_Mail_and_cuirass", "Cuirass", [("Mail_and_cuirass", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                                           20200, weight(23)   | abundance(100) | head_armor(0) | body_armor(50) | leg_armor(16) | difficulty(20), imodbits_armor ], #clan EA
    ["m_sarranid_elite_armor", "Sarranid Elite Armor", [("tunic_armor_a", 0)],  itp_type_body_armor|itp_covers_legs|itp_civilian|itp_merchandise, 0,
     20700, weight(23)   | abundance(100) | head_armor(0) | body_armor(48) | leg_armor(16) | difficulty(21), imodbits_plate ],
    ["m_vaegir_elite_armor", "Vaegir Decorated Armor", [("lamellar_armor_c", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,
     20950, weight(23)   | abundance(100) | head_armor(0) | body_armor(48) | leg_armor(16) | difficulty(21), imodbits_plate ],
    ["m_drz_elite_lamellar_armor", "Vaegir Elite Armor", [("drz_elite_lamellar_armor", 0)], itp_type_body_armor|itp_covers_legs|itp_civilian|itp_merchandise, 0,
     21550, weight(23)   | abundance(100) | head_armor(0) | body_armor(48) | leg_armor(16) | difficulty(21), imodbits_plate ],

    ["m_corrazina_red", "Red Corazzina", [("corrazina_red",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,         ########## MAIN ##########
     22650, weight(26.5)   | abundance(100) | head_armor(0) | body_armor(50) | leg_armor(17) | difficulty(24), imodbits_plate ],
    ["m_corrazina_green", "Green Corazzina", [("corrazina_green",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,     ########## EXTRA ##########
     100, weight(26.5)   | abundance(100) | head_armor(0) | body_armor(50) | leg_armor(17) | difficulty(24), imodbits_plate ],
    ["m_corrazina_black", "Black Corazzina", [("corrazina_black",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,     ########## EXTRA ##########
     100, weight(26.5)   | abundance(100) | head_armor(0) | body_armor(50) | leg_armor(17) | difficulty(24), imodbits_plate ],

    # ["m_coat_of_plates_red", "Long Red Coat of Plates", [("coat_of_plates_red", 0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,                     19300, weight(24)   | abundance(100) | head_armor(0) | body_armor(50) | leg_armor(18) | difficulty(21), imodbits_armor ],
    # ["m_coat_of_plates", "Long Black Coat of Plates", [("coat_of_plates_a", 0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,                         19350, weight(24)   | abundance(100) | head_armor(0) | body_armor(50) | leg_armor(18) | difficulty(21), imodbits_armor ],
    # ["m_ned_stark_armor", "Black Armor", [("ned_stark_armor", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                                         105000,weight(18)   | abundance(100) | head_armor(0) | body_armor(46) | leg_armor(14) | difficulty(17), imodbits_armor ],
	
	
    # Plate armor
    # T9 - TIER 9 T9
    ["gg_heavy_dread_plate", "Heavy Thick Dread Plate Armor", [("heavy_plate_1_mesh",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,
     200000, weight(34) | abundance(100) | head_armor(1) | body_armor(55) | leg_armor(23) | difficulty(24), imodbits_plate ],

##    ["m_churburg_13", "Plate Armor", [("churburg_13",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,
##     25550, weight(28) | abundance(100) | head_armor(0) | body_armor(53) | leg_armor(19) | difficulty(23), imodbits_plate ],

##    ["gothic_heavy_plate_blue", "New Area Heavy Plate Blue", [("gothic_heavy_plate_blue",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,  ###MAIN
##     24550, weight(28) | abundance(100) | head_armor(0) | body_armor(53) | leg_armor(20) | difficulty(23), imodbits_plate ],
##    ["gothic_heavy_plate_yellow", "New Area Heavy Plate Yellow", [("gothic_heavy_plate_yellow",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, ### EXTRA
##     100, weight(28) | abundance(100) | head_armor(0) | body_armor(53) | leg_armor(20) | difficulty(23), imodbits_plate ],
##    ["gothic_heavy_plate_red", "New Area Heavy Plate Red", [("gothic_heavy_plate_red",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, ### EXTRA
##     100, weight(28) | abundance(100) | head_armor(0) | body_armor(53) | leg_armor(20) | difficulty(23), imodbits_plate ],
##    ["gothic_heavy_plate_green", "New Area Heavy Plate Green", [("gothic_heavy_plate_green",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, ### EXTRA
##     100, weight(28) | abundance(100) | head_armor(0) | body_armor(53) | leg_armor(20) | difficulty(23), imodbits_plate ],
##
##    ["gothic_heavy_plate_blue_with_shoulders", "New Area Heavy Plate Blue with Shoulders", [("gothic_heavy_plate_blue_with_shoulders",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, ### EXTRA
##     1000, weight(30) | abundance(100) | head_armor(0) | body_armor(54) | leg_armor(20) | difficulty(23), imodbits_plate ],
##    ["gothic_heavy_plate_green_with_shoulders", "New Area Heavy Plate Green with Shoulders", [("gothic_heavy_plate_green_with_shoulders",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, ### EXTRA
##     1000, weight(30) | abundance(100) | head_armor(0) | body_armor(54) | leg_armor(20) | difficulty(23), imodbits_plate ],
##    ["gothic_heavy_plate_red_with_shoulders", "New Area Heavy Plate Red with Shoulders", [("gothic_heavy_plate_red_with_shoulders",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, ### EXTRA
##     1000, weight(30) | abundance(100) | head_armor(0) | body_armor(54) | leg_armor(20) | difficulty(23), imodbits_plate ],
##    ["gothic_heavy_plate_yellow_with_shoulders", "New Area Heavy Plate Yellow with Shoulders", [("gothic_heavy_plate_yellow_with_shoulders",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, ### EXTRA
##     1000, weight(30) | abundance(100) | head_armor(0) | body_armor(54) | leg_armor(20) | difficulty(23), imodbits_plate ],


    # ["gg_outlander_noble_plate_armor", "Outlander Noble Plate Armor", [("gg_outlander_noble_plate_armor",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,
      # 28000, weight(28) | abundance(100) | head_armor(0) | body_armor(54) | leg_armor(19) | difficulty(23), imodbits_plate ],

    # ["outlander_fine_plate1", "Outlander Noble Plate Armor", [("outlander_fine_plate1",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,  ### MAIN
      # 26000, weight(28) | abundance(100) | head_armor(0) | body_armor(53) | leg_armor(19) | difficulty(23), imodbits_plate ],
    # ["outlander_fine_plate2", "Outlander Noble Plate Armor", [("outlander_fine_plate2",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,  ### EXTRA
      # 200, weight(28) | abundance(100) | head_armor(0) | body_armor(53) | leg_armor(19) | difficulty(23), imodbits_plate ],
    # ["outlander_fine_plate3", "Outlander Noble Plate Armor", [("outlander_fine_plate3",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,  ### EXTRA
      # 200, weight(28) | abundance(100) | head_armor(0) | body_armor(53) | leg_armor(19) | difficulty(23), imodbits_plate ],


    ["m_plate_armor", "Thick Plate Armor", [("gg_full_plate_armor", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,  ### MAIN
     33000, weight(28) | abundance(100) | head_armor(0) | body_armor(52) | leg_armor(21) | difficulty(24), imodbits_plate ],
    ["gg_full_plate_with_shoulders", "Thick Plate Armor with Shoulders", [("gg_full_plate_with_shoulders", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,  ### EXTRA
     3200, weight(28) | abundance(100) | head_armor(0) | body_armor(52) | leg_armor(21) | difficulty(24), imodbits_plate ],

    ["m_churburg_13_mail", "Noble Plate Armor", [("churburg_13_mail",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, ########## MAIN ##########
     140000,weight(28) | abundance(100) | head_armor(0) | body_armor(52) | leg_armor(21) | difficulty(24), imodbits_plate ],
##    ["m_churburg_13_brass", "Noble Plate with Red Gambeson", [("churburg_13_brass",0)], itp_type_body_armor|itp_covers_legs, 0,    ########## EXTRA ##########
##     100,weight(28) | abundance(100) | head_armor(0) | body_armor(54) | leg_armor(22) | difficulty(24), imodbits_plate ],

    ["m_plate_armor_1", "Masterwork Plate Armor", [("milanese_armour", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,  ########## MAIN ##########
     160000,weight(28) | abundance(100) | head_armor(0) | body_armor(52) | leg_armor(21) | difficulty(24), imodbits_plate ], 
    ["m_plate_armor_1_with_besagew", "Masterwork Plate with Besagew", [("milanese_armour_besagew", 0)],  itp_type_body_armor|itp_covers_legs, 0, ########## EXTRA ##########
     500,weight(28) | abundance(100) | head_armor(0) | body_armor(52) | leg_armor(21) | difficulty(24), imodbits_plate ], 
    ["m_plate_armor_1_with_bascinet", "Masterwork Plate with Great Bascinet", [("milanese_armour_besagew", 0)],  itp_type_body_armor|itp_covers_legs, 0, ########## EXTRA ##########
     4000,weight(28) | abundance(100) | head_armor(0) | body_armor(52) | leg_armor(21) | difficulty(24), imodbits_plate ],


    # Armor sets

    ["m_narf_aketon", "Aketon with Woolen Hose", [("narf_aketon",0), ("narf_aketon_inv",ixmesh_inventory)], itp_merchandise|itp_type_body_armor|itp_covers_legs|itp_civilian, 0, ##### MAIN
     1550, weight(3.25)| abundance(100) | head_armor(0) | body_armor(21) | leg_armor(8)  | difficulty(0), imodbits_cloth ],
    ["m_narf_aketon_kk", "Aketon with Kneecops", [("narf_aketon_kk",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0,   ##### EXTRA
     500, weight(3.75)| abundance(100) | head_armor(0) | body_armor(21) | leg_armor(11) | difficulty(7), imodbits_cloth ],
    ["m_narf_aketon_cuisses_black", "Aketon with Black Cuisses", [("narf_aketon_cuisses_black",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0,   ##### EXTRA
     900, weight(4.25)| abundance(100) | head_armor(0) | body_armor(21) | leg_armor(14) | difficulty(7), imodbits_cloth ],
    ["m_narf_aketon_cuisses", "Aketon with Plate Cuisses", [("narf_aketon_cuisses",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0,   ##### EXTRA
     1250, weight(4.75)| abundance(100) | head_armor(0) | body_armor(21) | leg_armor(16) | difficulty(7), imodbits_cloth ],

    # FOTO VAR BUNLARDA # ["m_kau_mail_shirt_a", "Padded Armor", [("kau_mail_shirt_a", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                                                                                  3700, weight(7)   | abundance(100) | head_armor(0) | body_armor(31) | leg_armor(8)  | difficulty(10), imodbits_armor ], 
    # ["m_kau_mail_shirt_d", "Blue Padded Armor", [("kau_mail_shirt_d", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                                                                             3720, weight(7)   | abundance(100) | head_armor(0) | body_armor(31) | leg_armor(8)  | difficulty(10), imodbits_armor ], 
    # ["m_kau_haubergeon_a", "Red Padded Armor", [("kau_haubergeon_a", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,                                                                              3740, weight(7)   | abundance(100) | head_armor(0) | body_armor(31) | leg_armor(8)  | difficulty(10), imodbits_armor ],

    ["m_narf_brigandine_green", "Light Green Brigandine", [("narf_brigandine_green",0), ("narf_brigandine_green_inv",ixmesh_inventory)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, ### MAIN
     3850, weight(7.2)   | abundance(100) | head_armor(0) | body_armor(29) | leg_armor(9)  | difficulty(10), imodbits_armor ],
    ["m_narf_brigandine_green_with_kneecops", "Light Green Brigandine with Kneecops", [("narf_brigandine_green",0), ("narf_brigandine_green_inv",ixmesh_inventory)], itp_type_body_armor|itp_covers_legs, 0, ### EXTRA
     500, weight(7.2)   | abundance(100) | head_armor(0) | body_armor(29) | leg_armor(9)  | difficulty(10), imodbits_armor ],
    ["m_narf_brigandine_green_cuisses", "Light Green Brigandine with Cuisses", [("narf_brigandine_green_cuisse",0), ("narf_brigandine_green_inv",ixmesh_inventory)], itp_type_body_armor|itp_covers_legs, 0, ### EXTRA
     900, weight(7.2)   | abundance(100) | head_armor(0) | body_armor(29) | leg_armor(9) | difficulty(10), imodbits_armor ],

    ["m_narf_brigandine_red", "Light Red Brigandine", [("narf_brigandine_red",0), ("narf_brigandine_red_inv",ixmesh_inventory)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, ### EXTRA
     100, weight(7.2)   | abundance(100) | head_armor(0) | body_armor(29) | leg_armor(9)  | difficulty(10), imodbits_armor ],
    ["m_narf_brigandine_red_with_kneecops", "Light Red Brigandine with Kneecops", [("narf_brigandine_red",0), ("narf_brigandine_red_inv",ixmesh_inventory)], itp_type_body_armor|itp_covers_legs, 0, ### EXTRA
     500, weight(7.2)   | abundance(100) | head_armor(0) | body_armor(29) | leg_armor(9)  | difficulty(10), imodbits_armor ],
    ["m_narf_brigandine_red_cuisses", "Light Red Brigandine with Cuisses", [("narf_brigandine_red_cuisse",0), ("narf_brigandine_red_inv",ixmesh_inventory)], itp_type_body_armor|itp_covers_legs, 0, ### EXTRA
     900, weight(7.2)   | abundance(100) | head_armor(0) | body_armor(29) | leg_armor(9) | difficulty(10), imodbits_armor ],

    ["m_narf_brigandine_blue", "Light Blue Brigandine", [("narf_brigandine_blue",0), ("narf_brigandine_blue_inv",ixmesh_inventory)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0,  ### EXTRA
     100, weight(7.2)   | abundance(100) | head_armor(0) | body_armor(29) | leg_armor(9)  | difficulty(10), imodbits_armor ],
    ["m_narf_brigandine_blue_with_kneecops", "Light Blue Brigandine with Kneecops", [("narf_brigandine_blue",0), ("narf_brigandine_blue_inv",ixmesh_inventory)], itp_type_body_armor|itp_covers_legs, 0, ### EXTRA
     500, weight(7.2)   | abundance(100) | head_armor(0) | body_armor(29) | leg_armor(9)  | difficulty(10), imodbits_armor ],
    ["m_narf_brigandine_blue_cuisses", "Light Blue Brigandine with Cuisses", [("narf_brigandine_blue_cuisse",0), ("narf_brigandine_blue_inv",ixmesh_inventory)], itp_type_body_armor|itp_covers_legs, 0, ### EXTRA
     900, weight(7.2)   | abundance(100) | head_armor(0) | body_armor(29) | leg_armor(9) | difficulty(10), imodbits_armor ],



    ["m_narf_brigandine_green_mail", "Green Brigandine", [("narf_brigandine_green_mail",0), ("narf_brigandine_green_mail_inv",ixmesh_inventory)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0,   ### MAIN
     8700, weight(15)  | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(8) | difficulty(15), imodbits_armor ],
    ["m_narf_brigandine_green_mail_cuisses", "Green Brigandine with Cuisses", [("narf_brigandine_green_mail_cuisse",0), ("narf_brigandine_green_mail_inv",ixmesh_inventory)], itp_type_body_armor|itp_covers_legs, 0, ### EXTRA
     900, weight(15)  | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(8) | difficulty(15), imodbits_armor ],

    ["m_narf_brigandine_red_mail", "Red Brigandine", [("narf_brigandine_red_mail",0), ("narf_brigandine_red_mail_inv",ixmesh_inventory)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, ### EXTRA
     100, weight(15)  | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(8) | difficulty(15), imodbits_armor ],
    ["m_narf_brigandine_red_mail_cuisses", "Red Brigandine with Cuisses", [("narf_brigandine_red_mail_cuisse",0), ("narf_brigandine_red_mail_inv",ixmesh_inventory)], itp_type_body_armor|itp_covers_legs, 0, ### EXTRA
     900, weight(15)  | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(8) | difficulty(15), imodbits_armor ],

    ["m_narf_brigandine_blue_mail", "Blue Brigandine", [("narf_brigandine_blue_mail",0), ("narf_brigandine_blue_mail_inv",ixmesh_inventory)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, ### EXTRA
     100, weight(15)  | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(8) | difficulty(15), imodbits_armor ],
    ["m_narf_brigandine_blue_mail_cuisses", "Blue Brigandine with Cuisses", [("narf_brigandine_blue_mail_cuisse",0), ("narf_brigandine_blue_mail_inv",ixmesh_inventory)], itp_type_body_armor|itp_covers_legs, 0, ### EXTRA
     900, weight(15)  | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(8) | difficulty(15), imodbits_armor ],

    # ["m_pw_bishop_armor","Bishop Armor", [("pw_bishop_armor", 0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0,                                                                                      100000,weight(17) | abundance(100) | head_armor(0) | body_armor(47) | leg_armor(10) | difficulty(21), imodbits_armor ],



################################################ GOLD AND GLORY BODY ARMORS ################################################


 # ["heavy_gothic_plate_with_mail", "Heavy Thick Steel Plate Armor With Mail", [("heavy_gothic_plate_with_mail",0)], itp_type_body_armor  |itp_covers_legs ,0,
  # 400000 , weight(35)|abundance(100)|head_armor(3)|body_armor(63)|leg_armor(33)|difficulty(27) ,imodbits_plate ], 
#  ["heavy_gothic_with_neck_guard", "Heavy Thick Plate with Neck Guard", [("heavy_gothic_with_neck_guard",0)], itp_type_body_armor  |itp_covers_legs ,0,
#   0 , weight(27)|abundance(100)|head_armor(2)|body_armor(58)|leg_armor(21)|difficulty(24) ,imodbits_plate ], 
 # ["variantarmor", "Variant Plate Armor", [("variantarmor",0)], itp_type_body_armor  |itp_covers_legs ,0,
  # 50200 , weight(27)|abundance(100)|head_armor(1)|body_armor(58)|leg_armor(21)|difficulty(24) ,imodbits_plate ],

 ["plate_armor_g", "Customized Plate Armor", [("plate_armor_g",0)], itp_type_body_armor  |itp_covers_legs ,0,
  120000 , weight(28)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(21)|difficulty(24) ,imodbits_plate ], 

 # ["gg_new_horde_plate", "Horde Plate", [("gg_new_horde_plate",0)], itp_type_body_armor  |itp_covers_legs ,0,
  # 51000 , weight(27)|abundance(100)|head_armor(0)|body_armor(58)|leg_armor(21)|difficulty(24) ,imodbits_plate ],

 ["elite_gothic_armor", "Elite Gothic Plate Armor", [("elite_gothic_armor",0)], itp_type_body_armor  |itp_covers_legs ,0,
  120000 , weight(28)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(21)|difficulty(24) ,imodbits_plate ],

 # ["elite_joan_armor", "Masterwork Joan Plate Armor", [("elite_joan_armor",0)], itp_type_body_armor  |itp_covers_legs ,0,
  # 48800 , weight(25)|abundance(100)|head_armor(0)|body_armor(57)|leg_armor(21)|difficulty(24) ,imodbits_plate ],
 
 # ["milanese_armour", "Milanese Plate Armor", [("milanese_armour",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ MAIN  ############
  # 48700 , weight(25)|abundance(100)|head_armor(0)|body_armor(57)|leg_armor(21)|difficulty(24) ,imodbits_plate ],
 # ["milanese_armour_besagew", "Milanese Plate Armor with Plate Circles", [("milanese_armour_besagew",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  # 48900 , weight(25.7)|abundance(100)|head_armor(0)|body_armor(57)|leg_armor(21)|difficulty(24) ,imodbits_plate ],

 # ["a_plate_harness_1", "Masterworkd Plate Armor", [("a_plate_harness_1",0)], itp_type_body_armor  |itp_covers_legs ,0,
  # 48500 , weight(25)|abundance(100)|head_armor(0)|body_armor(57)|leg_armor(21)|difficulty(24) ,imodbits_plate ],
 # ["a_plate_harness_2", "Masterwork Plate Armor", [("a_plate_harness_2",0)], itp_type_body_armor  |itp_covers_legs ,0,
  # 48300 , weight(25)|abundance(100)|head_armor(0)|body_armor(57)|leg_armor(21)|difficulty(24) ,imodbits_plate ],
 # ["a_plate_harness_3", "Masterwork Plate Armor", [("a_plate_harness_3",0)], itp_type_body_armor  |itp_covers_legs ,0,
  # 48000 , weight(25)|abundance(100)|head_armor(0)|body_armor(57)|leg_armor(21)|difficulty(24) ,imodbits_plate ],

 # ["ar_swa_t7_fullplate_a", "Calradian Plate Armor", [("ar_swa_t7_fullplate_a",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ MAIN  ############
  # 47800 , weight(25)|abundance(100)|head_armor(0)|body_armor(56)|leg_armor(21)|difficulty(24) ,imodbits_plate ],
 # ["ar_swa_t7_fullplate_c", "Calradian Plate Armor with Plate Shoulders", [("ar_swa_t7_fullplate_c",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  # 48200 , weight(25)|abundance(100)|head_armor(1)|body_armor(57)|leg_armor(21)|difficulty(24) ,imodbits_plate ],
 
 # ["churburg_13_mail", "Churburg Plate Armor", [("churburg_13_mail",0)], itp_type_body_armor  |itp_covers_legs ,0,
  # 47700 , weight(24)|abundance(100)|head_armor(0)|body_armor(56)|leg_armor(21)|difficulty(24) ,imodbits_plate ],
 # ["churburg_13", "Blue Churburg Plate Armor", [("churburg_13",0)], itp_type_body_armor  |itp_covers_legs ,0,
  # 47600 , weight(24)|abundance(100)|head_armor(0)|body_armor(56)|leg_armor(21)|difficulty(24) ,imodbits_plate ],
 # ["churburg_13_brass", "Red Churburg Plate Armor", [("churburg_13_brass",0)], itp_type_body_armor  |itp_covers_legs ,0,
  # 47500 , weight(24)|abundance(100)|head_armor(0)|body_armor(56)|leg_armor(21)|difficulty(24) ,imodbits_plate ],


 # ["licht_pikenier_blue", "Red Churburg Plate Armor", [("licht_pikenier_blue",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ MAIN  ############
  # 46000 , weight(24)|abundance(100)|head_armor(1)|body_armor(55)|leg_armor(21)|difficulty(24) ,imodbits_plate ],
 # ["licht_pikenier_blue_with_shoulders", "Red Churburg Plate Armor", [("licht_pikenier_blue_with_shoulders",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  # 50000 , weight(24)|abundance(100)|head_armor(2)|body_armor(56)|leg_armor(21)|difficulty(24) ,imodbits_plate ],
 # ["licht_pikenier_yellow", "Red Churburg Plate Armor", [("licht_pikenier_yellow",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  # 46150 , weight(24)|abundance(100)|head_armor(1)|body_armor(55)|leg_armor(21)|difficulty(24) ,imodbits_plate ],
 # ["licht_pikenier_yellow_with_shoulders", "Red Churburg Plate Armor", [("licht_pikenier_yellow_with_shoulders",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  # 50100 , weight(24)|abundance(100)|head_armor(2)|body_armor(56)|leg_armor(21)|difficulty(24) ,imodbits_plate ],
 # ["licht_pikenier_red", "Red Churburg Plate Armor", [("licht_pikenier_red",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  # 46250 , weight(24)|abundance(100)|head_armor(1)|body_armor(55)|leg_armor(21)|difficulty(24) ,imodbits_plate ],
 # ["licht_pikenier_red_with_shoulders", "Red Churburg Plate Armor", [("licht_pikenier_red_with_shoulders",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  # 50200 , weight(24)|abundance(100)|head_armor(2)|body_armor(56)|leg_armor(21)|difficulty(24) ,imodbits_plate ],
 # ["licht_pikenier_green", "Red Churburg Plate Armor", [("licht_pikenier_green",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  # 46350 , weight(24)|abundance(100)|head_armor(1)|body_armor(55)|leg_armor(21)|difficulty(24) ,imodbits_plate ], 
 # ["licht_pikenier_green_with_shoulders", "Red Churburg Plate Armor", [("licht_pikenier_green_with_shoulders",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  # 50300 , weight(24)|abundance(100)|head_armor(2)|body_armor(56)|leg_armor(21)|difficulty(24) ,imodbits_plate ], 

 ["varangopoulos_armor", "Varangopoulos", [("varangopoulos_armor",0)], itp_type_body_armor  |itp_covers_legs ,0,
  24400 , weight(26.5)|abundance(100)|head_armor(0)|body_armor(50)|leg_armor(17)|difficulty(24) ,imodbits_plate ],

 # ["corrazina_red", "Corrazina", [("corrazina_red",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ MAIN  ############
  # 40000 , weight(24)|abundance(100)|head_armor(0)|body_armor(54)|leg_armor(21)|difficulty(24) ,imodbits_plate ],
 # ["corrazina_green", "Green Corrazina", [("corrazina_green",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  # 40100 , weight(24)|abundance(100)|head_armor(0)|body_armor(54)|leg_armor(21)|difficulty(24) ,imodbits_plate ],
 # ["corrazina_black", "Black Corrazina", [("corrazina_black",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  # 40200 , weight(24)|abundance(100)|head_armor(0)|body_armor(54)|leg_armor(21)|difficulty(24) ,imodbits_plate ],

 ["vaegir_breastplate", "Breast Plate Armor", [("vaegir_breastplate",0)], itp_type_body_armor  |itp_covers_legs ,0,   ### MAIN
  24800 , weight(26.5)|abundance(100)|head_armor(0)|body_armor(50)|leg_armor(17)|difficulty(24) ,imodbits_plate ],
 ["mercenary_heavy_plate_armor_a", "Mercenary Breast Plate Armor", [("mercenary_heavy_plate_armor_a",0)], itp_type_body_armor  |itp_covers_legs ,0, ### EXTRA
  300 , weight(26.5)|abundance(100)|head_armor(0)|body_armor(50)|leg_armor(17)|difficulty(24) ,imodbits_plate ],

 ["plated_tunic_new_red", "Plated Tunic", [("plated_tunic_new_red",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ MAIN  ############
  22000 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_plate ],
 ["plated_tunic_new_blue", "Plated Tunic Blue", [("plated_tunic_new_blue",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  100 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_plate ],
 ["plated_tunic_new_green", "Plated Tunic Green", [("plated_tunic_new_green",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  100 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_plate ], 
 ["plated_tunic_new_purple", "Plated Tunic Purple", [("plated_tunic_new_purple",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  100 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_plate ],
 ["plated_tunic_new_brown", "Plated Tunic Brown", [("plated_tunic_new_brown",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  100 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_plate ],


 # ["zimke_strzelczy", "Strzelczy Plate Armor", [("zimke_strzelczy",0)], itp_type_body_armor  |itp_covers_legs ,0,
  # 30300 , weight(24)|abundance(100)|head_armor(0)|body_armor(53)|leg_armor(18)|difficulty(24) ,imodbits_plate ],
 ["voulgier", "Voulgier Elite Armor", [("voulgier",0)], itp_type_body_armor  |itp_covers_legs ,0,
  15800 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_plate ],


 ["newcoatofplates", "Plated Coat with Mail", [("newcoatofplates",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ MAIN  ############
  26500 , weight(26.5)|abundance(100)|head_armor(0)|body_armor(50)|leg_armor(17)|difficulty(24) ,imodbits_plate ],
 ["newcoatofplates2", "Blue Plated Coat with Mail", [("newcoatofplates2",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  100 , weight(26.5)|abundance(100)|head_armor(0)|body_armor(50)|leg_armor(17)|difficulty(24) ,imodbits_plate ],
 ["newcoatofplates3", "Black Plated Coat with Mail", [("newcoatofplates3",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  100 , weight(26.5)|abundance(100)|head_armor(0)|body_armor(50)|leg_armor(17)|difficulty(24) ,imodbits_plate ],
 ["huscarl_armour", "Red Plated Coat with Mail", [("newcoatofplates4",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  100 , weight(26.5)|abundance(100)|head_armor(0)|body_armor(50)|leg_armor(17)|difficulty(24) ,imodbits_plate ],


 ["m_mail_and_plate_alt", "Blue Mail and PLate", [("mail_and_plate_alt",0)], itp_type_body_armor  |itp_covers_legs ,0,
  27000 , weight(24)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(18)|difficulty(21) ,imodbits_plate ],
 ["m_light_mail_and_plate_alt", "Red Mail and Plate", [("light_mail_and_plate_alt",0)], itp_type_body_armor  |itp_covers_legs ,0,
  27100 , weight(24)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(18)|difficulty(21) ,imodbits_plate ],

 # ["gg_lamellar_armor_c", "Vaegir Elite Armor", [("gg_lamellar_armor_c",0)], itp_type_body_armor  |itp_covers_legs ,0,
  # 25450 , weight(24)|abundance(100)|head_armor(0)|body_armor(51)|leg_armor(17)|difficulty(21) ,imodbits_plate ], 
 # ["drz_elite_lamellar_armor", "Elite Armor", [("drz_elite_lamellar_armor",0)], itp_type_body_armor  |itp_covers_legs ,0,
  # 25350 , weight(24)|abundance(100)|head_armor(0)|body_armor(51)|leg_armor(17)|difficulty(21) ,imodbits_plate ],

 ["black_elite_plate_armor", "Black Elite Armor", [("black_elite_plate_armor",0)], itp_type_body_armor  |itp_covers_legs ,0,
  21650 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_plate ],



 ["lamellar_armor_d", "Khergit Elite Armor", [("old_lamellar_armor_d",0)], itp_type_body_armor  |itp_covers_legs ,0,  ############ MAIN  ############
  20800 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_plate ],
 ["gg_khergit_elite_blue", "Khergit Elite Armor Blue", [("gg_khergit_elite_blue",0)], itp_type_body_armor  |itp_covers_legs ,0,   ############ EXTRA  ############
  100 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_plate ],
 ["gg_khergit_elite_pink", "Khergit Elite Armor Pink", [("gg_khergit_elite_pink",0)], itp_type_body_armor  |itp_covers_legs ,0,   ############ EXTRA  ############
  100 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_plate ],
 ["gg_khergit_elite_purple", "Khergit Elite Armor Purple", [("gg_khergit_elite_purple",0)], itp_type_body_armor  |itp_covers_legs ,0,   ############ EXTRA  ############
  100 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_plate ],
 ["gg_khergit_elite_yellow", "Khergit Elite Armor Yellow", [("gg_khergit_elite_yellow",0)], itp_type_body_armor  |itp_covers_legs ,0,   ############ EXTRA  ############
  100 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_plate ],
 ["new_lamellar_armor", "New Khergit Elite Armor", [("new_lamellar_armor",0)], itp_type_body_armor  |itp_covers_legs ,0,     ############ EXTRA  ############
  300 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_plate ],
 



##  ["khergit_elite_armor", "Khergit Heraldic Elite Armor", [("heraldic_lamellar_armor_d",0)], itp_type_body_armor|itp_covers_legs, 0, ############ EXTRA  ############
##   200 , weight(25)|abundance(100)|head_armor(0)|body_armor(51)|leg_armor(17)|difficulty(21) ,imodbits_plate ],
##     (ti_on_init_item, [
##       (store_trigger_param_1, ":var0"),
##       (store_trigger_param_2, ":var1"),
##       (call_script, "script_shield_item_set_banner", "tableau_heraldic_lamellar_armor_d", ":var0", ":var1"),
##     ]),
##    ]],
 

 ["gg_coat_of_plates_red", "Coat of Plate", [("gg_coat_of_plates_red",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ MAIN  ############
  19300 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_plate ],
 ["gg_coat_of_plates_white", "White Coat of Plate", [("gg_coat_of_plates_white",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  100 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_plate ],
 ["gg_coat_of_plates_brown", "Brown Coat of Plate", [("gg_coat_of_plates_brown",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  100 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_plate ],
 ["gg_coat_of_plates_purple", "Purple Coat of Plate", [("gg_coat_of_plates_purple",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  100 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_plate ],
 ["gg_coat_of_plates_yellow", "Yellow Coat of Plate", [("gg_coat_of_plates_yellow",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  100 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_plate ],
 ["gg_coat_of_plates_black", "Black Coat of Plate", [("gg_coat_of_plates_black",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  100 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_plate ],
 ["gg_coat_of_plates_blue", "Blue Coat of Plate", [("gg_coat_of_plates_blue",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  100 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_plate ],
 ["gg_coat_of_plates_green", "Green Coat of Plate", [("gg_coat_of_plates_green",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  100 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_plate ],


 ["nord_plate_mail", "Nordland Armor", [("nord_plate_mail",0)], itp_type_body_armor  |itp_covers_legs ,0,   
  10000 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_plate ],


  ["frenchplate", "Blue Outlander Armor", [("frenchplate",0)], itp_type_body_armor  |itp_covers_legs ,0,   ############ MAIN  ############
   18000 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_plate ],
  ["frenchplate_red", "Red Outlander Armor", [("frenchplate_red",0)], itp_type_body_armor  |itp_covers_legs ,0,   ############ EXTRA  ############
   100 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_plate ],
  ["frenchplate_black", "Black Outlander Armor", [("frenchplate_black",0)], itp_type_body_armor  |itp_covers_legs ,0,   ############ EXTRA  ############
   100 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_plate ],


 # ["polishplate", "Red Polish Plate Armor", [("polishplate",0)], itp_type_body_armor  |itp_covers_legs ,0,  ############ MAIN  ############
  # 19800 , weight(20)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_plate ],
 # ["epic_plate", "Blue Polish Plate Armor", [("epic_plate",0)], itp_type_body_armor  |itp_covers_legs ,0,  ############ EXTRA  ############
  # 19990 , weight(20)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_plate ],

 # ["gg_cuir_bouilli_a", "Cuir Bouilli Armor", [("gg_cuir_bouilli_a",0)], itp_type_body_armor  |itp_covers_legs ,0,  
  # 19100 , weight(18)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(15)|difficulty(21) ,imodbits_plate ],
 # ["gg_banded_armor_a", "Banded Armor", [("gg_banded_armor_a",0)], itp_type_body_armor  |itp_covers_legs ,0,  
  # 19000 , weight(18)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(15)|difficulty(21) ,imodbits_plate ],

 # ["gg_red_scale_armor_f", "Red Scale Armor with Mail", [("gg_red_scale_armor_f",0)], itp_type_body_armor  |itp_covers_legs ,0,   ############ MAIN  ############
  # 18990 , weight(18)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(15)|difficulty(21) ,imodbits_plate ],
 # ["gg_red_scale_armor_f_with_plate", "Red Scale Armor with Mail and Plate", [("gg_red_scale_armor_f_with_plate",0)], itp_type_body_armor  |itp_covers_legs ,0,   ############ EXTRA  ############
  # 19600 , weight(22)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(21)|difficulty(21) ,imodbits_plate ],

 
 # ["gg_blue_scale_armor", "Scale Armor", [("gg_blue_scale_armor",0)], itp_type_body_armor  |itp_covers_legs ,0,  ############ MAIN  ############
  # 18000 , weight(18)|abundance(100)|head_armor(0)|body_armor(47)|leg_armor(15)|difficulty(21) ,imodbits_plate ],
 # ["gg_blue_scale_armor", "Scale Armor with Plate", [("gg_blue_scale_armor",0)], itp_type_body_armor  |itp_covers_legs ,0,  ############ EXTRA  ############
  # 19500 , weight(22)|abundance(100)|head_armor(0)|body_armor(47)|leg_armor(21)|difficulty(21) ,imodbits_plate ],


 
 ["old_brigandine_red", "Brigandine", [("old_brigandine_red",0)], itp_type_body_armor  |itp_covers_legs ,0,   ############ MAIN  ############
  12550 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_plate ],
 ["old_leg_plated_brigandine_red", "Red Brigandine with Leg Plate", [("old_leg_plated_brigandine_red",0)], itp_type_body_armor  |itp_covers_legs ,0,  ############ EXTRA  ############
  750 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_plate ],

 ["old_brigandine_yellow", "Yellow Brigandine", [("old_brigandine_yellow",0)], itp_type_body_armor  |itp_covers_legs ,0,  ############ EXTRA  ############
  100 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_plate ],
 ["old_leg_plated_brigandine_yellow", "Yellow Brigandine with Leg Plate", [("old_leg_plated_brigandine_yellow",0)], itp_type_body_armor  |itp_covers_legs ,0,  ############ EXTRA  ############
  750 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_plate ],

 ["old_brigandine_blue", "Blue Brigandine", [("old_brigandine_blue",0)], itp_type_body_armor  |itp_covers_legs ,0,  ############ EXTRA  ############
  100 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_plate ],
 ["old_leg_plated_brigandine_blue", "Blue Brigandine with Leg Plate", [("old_leg_plated_brigandine_blue",0)], itp_type_body_armor  |itp_covers_legs ,0,  ############ EXTRA  ############
  750 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_plate ],

 ["old_brigandine_green", "Green Brigandine", [("old_brigandine_green",0)], itp_type_body_armor  |itp_covers_legs ,0,  ############ EXTRA  ############
  100 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_plate ],
 ["old_leg_plated_brigandine_green", "Green Brigandine with Leg Plate", [("old_leg_plated_brigandine_green",0)], itp_type_body_armor  |itp_covers_legs ,0,  ############ EXTRA  ############
  750 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_plate ],

 ["old_brigandine_black", "Black Brigandine", [("m_brigandine_black",0)], itp_type_body_armor  |itp_covers_legs ,0,  ############ EXTRA  ############
  100 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_plate ],
 ["old_leg_plated_brigandine_black", "Black Brigandine with Leg Plate", [("old_leg_plated_brigandine_black",0)], itp_type_body_armor  |itp_covers_legs ,0,  ############ EXTRA  ############
  750 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_plate ],


 ["pronoia_armor", "Pronia Armor", [("pronoia_armor",0)], itp_type_body_armor  |itp_covers_legs ,0,  
  14160 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_plate ], 
 # ["drz_lamellar_armor", "Lamellar Surcoat Armor", [("drz_lamellar_armor",0)], itp_type_body_armor  |itp_covers_legs ,0,  
  # 18000 , weight(20)|abundance(100)|head_armor(0)|body_armor(47)|leg_armor(17)|difficulty(21) ,imodbits_plate ], 
 # ["grey_plate", "Grey Plate", [("grey_plate",0)], itp_type_body_armor  |itp_covers_legs ,0,  
  # 17000 , weight(18)|abundance(100)|head_armor(0)|body_armor(47)|leg_armor(15)|difficulty(21) ,imodbits_plate ],
 # ["dull_brown", "Brown Plate", [("dull_brown",0)], itp_type_body_armor  |itp_covers_legs ,0,  
  # 16800 , weight(18)|abundance(100)|head_armor(0)|body_armor(47)|leg_armor(15)|difficulty(21) ,imodbits_plate ],

 ["clibanarius_armor", "Clibanarius Armor", [("clibanarius_armor",0)], itp_type_body_armor  |itp_covers_legs ,0,   ############ MAIN  ############
  14000 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_armor ],
 ["clibanarius_armor_purple", "Purple Clibanarius Armor", [("clibanarius_armor_purple",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  100 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_armor ],
 ["clibanarius_armor_green", "Green Clibanarius Armor", [("clibanarius_armor_green",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  100 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_armor ],

 # ["leather_armor_padded1", "Long Leathe Surcoat", [("leather_armor_padded1",0)], itp_type_body_armor  |itp_covers_legs ,0,
  # 14000 , weight(18)|abundance(100)|head_armor(0)|body_armor(46)|leg_armor(16)|difficulty(21) ,imodbits_armor ],

 ["katafraktoi_armor", "Katafraktoi Armor", [("katafraktoi_armor",0)], itp_type_body_armor  |itp_covers_legs ,0,  
  90000 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_armor ],
 ["armor_sultan_saracens", "Sultan Armor", [("armor_sultan_saracens", 0)], itp_type_body_armor  |itp_covers_legs ,0,  
  130000 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_armor ],
 ["armor_sultan_saracens_inf", "Sultan Armor", [("armor_sultan_saracens_inf", 0)], itp_type_body_armor  |itp_covers_legs ,0,  ##SULTAN INF
  500 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_armor ],
 ["armor_king_Jerusalem", "Holy Armor", [("armor_king_Jerusalem", 0)], itp_type_body_armor  |itp_covers_legs ,0,  
  135000 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_armor ],  
 ["armor_king_Jerusalem_inf", "Holy Armor", [("armor_king_Jerusalem_inf", 0)], itp_type_body_armor  |itp_covers_legs ,0,  ##jeru INF
  500 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_armor ],  
 ["archons_armor", "Archons Armor", [("archons_armor",0)], itp_type_body_armor  |itp_covers_legs ,0,  
  12000 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_armor ],
 ["tyrk_armor_heavi_c", "Heavy Tyrk Armor", [("tyrk_armor_heavi_c",0)], itp_type_body_armor  |itp_covers_legs ,0,  
  15500 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_armor ],
 ["heavy_yawshan", "Heavy Yawshan", [("heavy_yawshan",0)], itp_type_body_armor  |itp_covers_legs ,0,  
  17950 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_armor ],
 ["sipahi_jawshan", "Heavy Cavarlry Yawshan", [("sipahi_jawshan",0)], itp_type_body_armor  |itp_covers_legs ,0,  
  22250 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_armor ],
 ["zercalo_armor", "Reinforced Kuyak", [("zercalo_armor", 0)], itp_type_body_armor  |itp_covers_legs ,0,  
  75000 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_armor ],

 # ["ar_pla_t5_mailsurcoat_b", "Mail Surcoat", [("ar_pla_t5_mailsurcoat_b",0)], itp_type_body_armor  |itp_covers_legs ,0,  
  #13000 , weight(16)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(18) ,imodbits_armor ],

 ["new_kuyak_a", "New Dark Kuyak", [("new_kuyak_a",0)], itp_type_body_armor  |itp_covers_legs ,0,  
  9400 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_armor ],
 ["new_kuyak_b", "New Brown Kuyak", [("new_kuyak_b",0)], itp_type_body_armor  |itp_covers_legs ,0,  
  9450 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_armor ], 

 # ["kuyak_a", "Black Kuyak", [("kuyak_a",0)], itp_type_body_armor  |itp_covers_legs ,0,  
  # 12950 , weight(16)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(18) ,imodbits_armor ],
 # ["kuyak_b", "Brown Kuyak", [("kuyak_b",0)], itp_type_body_armor  |itp_covers_legs ,0,  
  # 12950 , weight(16)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(18) ,imodbits_armor ],


 # ["rus_lamellar_b", "Rus Lamellar Armor", [("rus_lamellar_b",0)], itp_type_body_armor  |itp_covers_legs ,0,   ############ MAIN  ############
  # 12850 , weight(16)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(21) ,imodbits_armor ],
 # ["kuyak_b", "Brown Kuyak", [("kuyak_b",0)], itp_type_body_armor  |itp_covers_legs ,0,   ############ EXTRA  ############
  # 12900 , weight(16)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(21) ,imodbits_armor ],


 ["new_plated_som_black", "Surcoat over Mail and Plate", [("new_plated_som_black",0)], itp_type_body_armor  |itp_covers_legs ,0,   ############ MAIN  ############
  9300 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_armor ],
 ["new_plated_som_blue", "Blue Surcoat over Mail and Plate", [("new_plated_som_blue",0)], itp_type_body_armor  |itp_covers_legs ,0,  ############ EXTRA  ############
  100 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_armor ],
 ["new_plated_som_brown", "Brown Surcoat over Mail and Plate", [("new_plated_som_brown",0)], itp_type_body_armor  |itp_covers_legs ,0,  ############ EXTRA  ############
  100 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_armor ],
 ["new_plated_som_green", "Green Surcoat over Mail and Plate", [("new_plated_som_green",0)], itp_type_body_armor  |itp_covers_legs ,0,  ############ EXTRA  ############
  100 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_armor ],
 ["new_plated_som_purple", "Purple Surcoat over Mail and Plate", [("new_plated_som_purple",0)], itp_type_body_armor  |itp_covers_legs ,0,  ############ EXTRA  ############
  100 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_armor ],
 ["new_plated_som_red", "Red Surcoat over Mail and Plate", [("new_plated_som_red",0)], itp_type_body_armor  |itp_covers_legs ,0,  ############ EXTRA  ############
  100 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_armor ],
 ["new_plated_som_white", "White Surcoat over Mail and Plate", [("new_plated_som_white",0)], itp_type_body_armor  |itp_covers_legs ,0,  ############ EXTRA  ############
  100 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_armor ],
 ["new_plated_som_yellow", "Yellow Surcoat over Mail and Plate", [("new_plated_som_yellow",0)], itp_type_body_armor  |itp_covers_legs ,0,  ############ EXTRA  ############
  100 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_armor ],


 ["rus_scale", "Rus Scale Armor", [("rus_scale",0)], itp_type_body_armor  |itp_covers_legs ,0,  ############ MAIN  ############
  9220 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_armor ],
 ["rus_scale_bright_black", "Bright-Black Rus Scale Armor", [("rus_scale_bright_black",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  100 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_armor ],
 ["rus_scale_bright_blue", "Bright-Blue Rus Scale Armor", [("rus_scale_bright_blue",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  100 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_armor ],
 ["rus_scale_bright_white", "Bright-White Rus Scale Armor", [("rus_scale_bright_white",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  100 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_armor ],
 ["rus_scale_dark_white", "Dark-White Rus Scale Armor", [("rus_scale_dark_white",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  150 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_armor ],
 ["rus_scale_green", "Dark-Green Rus Scale Armor", [("rus_scale_green",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  150 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_armor ],
 ["rus_scale_blue", "Dark-Blue Rus Scale Armor", [("rus_scale_blue",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  150 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_armor ],
 ["rus_scale_red", "Dark-Red Rus Scale Armor", [("rus_scale_red",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  150 , weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18) ,imodbits_armor ],


 # ["leather_armor_padded1", "Haubergeon Armor", [("leather_armor_padded1",0)], itp_type_body_armor  |itp_covers_legs ,0,
  # 8000 , weight(18)|abundance(100)|head_armor(0)|body_armor(42)|leg_armor(11)|difficulty(18) ,imodbits_armor ],

 ["palace_guard", "Palace Guard Armor", [("palace_guard",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ MAIN  ############
  5450 , weight(13)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(14)|difficulty(15) ,imodbits_armor ], 
 ["palace_guard_purple", "Purple Palace Guard Armor", [("palace_guard_purple",0)], itp_type_body_armor  |itp_covers_legs ,0,  ############ EXTRA  ############
  100 , weight(13)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(14)|difficulty(15) ,imodbits_armor ],
 ["palace_guard_green", "Green Palace Guard Armor", [("palace_guard_green",0)], itp_type_body_armor  |itp_covers_legs ,0,  ############ EXTRA  ############
  100 , weight(13)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(14)|difficulty(15) ,imodbits_armor ],
 ["palace_guard_red", "Red Palace Guard Armor", [("palace_guard_red",0)], itp_type_body_armor  |itp_covers_legs ,0,  ############ EXTRA  ############
  100 , weight(13)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(14)|difficulty(15) ,imodbits_armor ],


 ["haubergeon_red", "Haubergeon Armor", [("haubergeon_red",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ MAIN  ############
  5500 , weight(13)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(14)|difficulty(15) ,imodbits_armor ],
 ["haubergeon_yellow", "Yellow Haubergeon Armor", [("haubergeon_yellow",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  100 , weight(13)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(14)|difficulty(15) ,imodbits_armor ],
 ["haubergeon_purple", "Purple Haubergeon Armor", [("haubergeon_purple",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  100 , weight(13)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(14)|difficulty(15) ,imodbits_armor ],
 ["haubergeon_black", "Black Haubergeon Armor", [("haubergeon_black",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  100 , weight(13)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(14)|difficulty(15) ,imodbits_armor ],
 ["haubergeon_green", "Green Haubergeon Armor", [("haubergeon_green",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  100 , weight(13)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(14)|difficulty(15) ,imodbits_armor ],
 ["haubergeon_blue", "Blue Haubergeon Armor", [("haubergeon_blue",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  100 , weight(13)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(14)|difficulty(15) ,imodbits_armor ],

 ["forest_bandit_arm", "Forest Bandit Armor", [("forest_bandit_arm",0)], itp_type_body_armor  |itp_covers_legs ,0,
  5450 , weight(13)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(14)|difficulty(15) ,imodbits_armor ],
 # ["m_surcoat_over_mail", "Brown Surcoat Over Mail", [("m_surcoat_over_mail",0)], itp_type_body_armor  |itp_covers_legs ,0,
  # 8000 , weight(16)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(13)|difficulty(18) ,imodbits_armor ],
 ["long_padded_surcoat_with_scale_armor", "Long Padded Scale Surcoat", [("long_padded_surcoat_with_scale_armor",0)], itp_type_body_armor  |itp_covers_legs ,0,
  6200 , weight(13)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(14)|difficulty(15) ,imodbits_armor ],
 ["vaegir_mail_shirt", "Vaegir Mail Shirt", [("vaegir_mail_shirt",0)], itp_type_body_armor  |itp_covers_legs ,0,
  5540 , weight(13)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(14)|difficulty(15) ,imodbits_armor ],
 # ["padded_merc_armor_black", "New Black Padded Armor", [("padded_merc_armor_black",0)], itp_type_body_armor  |itp_covers_legs ,0,
  # 7300 , weight(13)|abundance(100)|head_armor(0)|body_armor(39)|leg_armor(9)|difficulty(15) ,imodbits_armor ],
 ["merc_mail_shirt", "White Mail Shirt", [("merc_mail_shirt",0)], itp_type_body_armor  |itp_covers_legs ,0,
  5450 , weight(13)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(14)|difficulty(15) ,imodbits_armor ],
 ["mail_shirt_with_fur", "Mail Shirt with Fur", [("mail_shirt_with_fur",0)], itp_type_body_armor  |itp_covers_legs ,0,
  5000 , weight(13)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(14)|difficulty(15) ,imodbits_armor ],


 ["dethertir_armor_f", "Brown Dethertir Armor", [("dethertir_armor_f",0)], itp_type_body_armor  |itp_covers_legs ,0,   ############ MAIN  ############
  3420 , weight(6.3)|abundance(100)|head_armor(0)|body_armor(28)|leg_armor(11)|difficulty(7) ,imodbits_armor ],
 ["dethertir_armor_h", "Black Dethertir Armor", [("dethertir_armor_h",0)], itp_type_body_armor  |itp_covers_legs ,0,   ############ EXTRA  ############
  100 , weight(6.3)|abundance(100)|head_armor(0)|body_armor(28)|leg_armor(11)|difficulty(7) ,imodbits_armor ],

 # ["m_hauberk_a_new", "Hauberk Mail Armor", [("m_hauberk_a_new",0)], itp_type_body_armor  |itp_covers_legs ,0,
  # 6400 , weight(15)|abundance(100)|head_armor(0)|body_armor(38)|leg_armor(9)|difficulty(15) ,imodbits_armor ],
 # ["gg_mail_shirt_a", "Nordland Mail Shirt", [("gg_mail_shirt_a",0)], itp_type_body_armor  |itp_covers_legs ,0, 
  # 6100 , weight(12)|abundance(100)|head_armor(0)|body_armor(37)|leg_armor(9)|difficulty(15) ,imodbits_armor ],
 
 ["peltastos_armor", "Peltastor Armor", [("peltastos_armor",0)], itp_type_body_armor  |itp_covers_legs ,0, 
   4050 , weight(7.2)|abundance(100)|head_armor(0)|body_armor(30)|leg_armor(4)|difficulty(10) ,imodbits_armor ],

 ["skutatos_armor", "Skutatos Armor", [("skutatos_armor",0)], itp_type_body_armor  |itp_covers_legs ,0,  
  8350 , weight(13)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(14)|difficulty(15) ,imodbits_armor ],


 # ["cwe_archer_armor_1", "Black Padded Armor", [("cwe_archer_armor_1",0)], itp_type_body_armor  |itp_covers_legs ,0,  ############ MAIN  ############
  # 5800 , weight(16)|abundance(100)|head_armor(0)|body_armor(36)|leg_armor(8)|difficulty(12) ,imodbits_armor ],
 # ["cwe_archer_armor_2", "Brown Padded Armor", [("cwe_archer_armor_2",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  # 5900 , weight(16)|abundance(100)|head_armor(0)|body_armor(36)|leg_armor(8)|difficulty(12) ,imodbits_armor ],
 # ["cwe_sergeant_armor_1", "Blue and Red Padded Armor with Mail", [("cwe_sergeant_armor_1",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  # 8350 , weight(16)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(13)|difficulty(18) ,imodbits_armor ],
 # ["cwe_sergeant_armor_2", "Black Padded Armor with Mail", [("cwe_sergeant_armor_2",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  # 8300 , weight(16)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(13)|difficulty(18) ,imodbits_armor ],
 # ["cwe_sergeant_armor_3", "Red Padded Armor with Mail", [("cwe_sergeant_armor_3",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  # 8300 , weight(16)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(13)|difficulty(18) ,imodbits_armor ],

 # ["gg_lamellar_vest_pruple", "Lamellar Vest", [("gg_lamellar_vest_pruple",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ MAIN  ############
  # 5300 , weight(12)|abundance(100)|head_armor(0)|body_armor(35)|leg_armor(8)|difficulty(12) ,imodbits_armor ],
 # ["gg_lamellar_vest_white", "White Lamellar Vest", [("gg_lamellar_vest_white",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  # 5350 , weight(12)|abundance(100)|head_armor(0)|body_armor(35)|leg_armor(8)|difficulty(12) ,imodbits_armor ],
 # ["gg_lamellar_vest_black", "Black Lamellar Vest", [("gg_lamellar_vest_black",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  # 5400 , weight(12)|abundance(100)|head_armor(0)|body_armor(35)|leg_armor(8)|difficulty(12) ,imodbits_armor ],

 # ["gg_mongol_armor", "Khergit Armor", [("gg_mongol_armor",0)], itp_type_body_armor  |itp_covers_legs ,0,
  # 5300 , weight(12)|abundance(100)|head_armor(0)|body_armor(35)|leg_armor(8)|difficulty(12) ,imodbits_armor ],
 # ["rathos_leather_armor_1", "Rathos Leather Armor", [("rathos_leather_armor_1",0)], itp_type_body_armor  |itp_covers_legs ,0,
  # 5100 , weight(12)|abundance(100)|head_armor(0)|body_armor(35)|leg_armor(8)|difficulty(12) ,imodbits_armor ],
 # ["archer_armor", "Archer Armor", [("archer_armor",0)], itp_type_body_armor  |itp_covers_legs ,0,
#  5000 , weight(12)|abundance(100)|head_armor(0)|body_armor(35)|leg_armor(8)|difficulty(12) ,imodbits_armor ],

 ["gg_aketon", "Aketon", [("gg_aketon",0)], itp_type_body_armor  |itp_covers_legs ,0, 
  1660 , weight(3.30)|abundance(100)|head_armor(0)|body_armor(21)|leg_armor(8)|difficulty(0) ,imodbits_cloth ],

 # ["gg_ragged_leather_jerkin", "Leather Jerkin", [("gg_ragged_leather_jerkin",0)], itp_type_body_armor  |itp_covers_legs ,0, 
  # 4300 , weight(1)|abundance(100)|head_armor(0)|body_armor(33)|leg_armor(0)|difficulty(12) ,imodbits_cloth ],
 # ["gg_leather_armor_b", "Padded Armor", [("gg_leather_armor_b",0)], itp_type_body_armor  |itp_covers_legs ,0, 
  # 3700 , weight(1)|abundance(100)|head_armor(0)|body_armor(32)|leg_armor(0)|difficulty(12) ,imodbits_cloth ],

 # ["gg_leather_armor", "Leather Armor", [("gg_leather_armor",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ MAIN  ############
  # 3400 , weight(1)|abundance(100)|head_armor(0)|body_armor(30)|leg_armor(0)|difficulty(12) ,imodbits_cloth ],
 # ["gg_leather_armor_with_shoulder", "Leather Armor with Shoulders", [("gg_leather_armor_with_shoulder",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  # 3600 , weight(1)|abundance(100)|head_armor(0)|body_armor(31)|leg_armor(0)|difficulty(12) ,imodbits_cloth ],

 ["red_gambeson_c", "New Gambeson", [("red_gambeson_c",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ MAIN  ############
  1300 , weight(3)|abundance(100)|head_armor(0)|body_armor(20)|leg_armor(8)|difficulty(0) ,imodbits_cloth ],
 ["green_gambeson_c", "New Green Gambeson", [("green_gambeson_c",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  100 , weight(3)|abundance(100)|head_armor(0)|body_armor(20)|leg_armor(8)|difficulty(0) ,imodbits_cloth ],
 ["yellow_gambeson_z", "New Yellow Gambeson", [("yellow_gambeson_z",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  100 , weight(3)|abundance(100)|head_armor(0)|body_armor(20)|leg_armor(8)|difficulty(0) ,imodbits_cloth ],

 # ["gg_padded_leather", "Padded Vest", [("gg_padded_leather",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ MAIN  ############
  # 2800 , weight(1)|abundance(100)|head_armor(0)|body_armor(28)|leg_armor(0)|difficulty(9) ,imodbits_cloth ],
 # ["gg_padded_leather_cowl", "Padded Vest with Green Cowl", [("gg_padded_leather_cowl",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  # 2800 , weight(1)|abundance(100)|head_armor(0)|body_armor(28)|leg_armor(0)|difficulty(9) ,imodbits_cloth ],
 # ["gg_padded_leather_c", "Dark Green Padded Leather", [("gg_padded_leather_c",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
  # 2900 , weight(1)|abundance(100)|head_armor(0)|body_armor(28)|leg_armor(0)|difficulty(9) ,imodbits_cloth ],
 # ["gg_padded_cloth_b", "Rhodok Padded Cloth", [("gg_padded_cloth_b",0)], itp_type_body_armor  |itp_covers_legs ,0,
  # 2600 , weight(1)|abundance(100)|head_armor(0)|body_armor(24)|leg_armor(0)|difficulty(7) ,imodbits_cloth ],
 # ["gg_padded_cloth_a", "Swadian Aketon", [("gg_padded_cloth_a",0)], itp_type_body_armor  |itp_covers_legs ,0,
  # 2450 , weight(1)|abundance(100)|head_armor(0)|body_armor(23)|leg_armor(0)|difficulty(7) ,imodbits_cloth ],
 # ["gg_leather_vest_a", "Leatver Vest", [("gg_leather_vest_a",0)], itp_type_body_armor  |itp_covers_legs ,0,
  # 2200 , weight(1)|abundance(100)|head_armor(0)|body_armor(22)|leg_armor(0)|difficulty(7) ,imodbits_cloth ],




 ["gg_pilgrim_hood","Pilgrim Hood", [("gg_pilgrim_hood", 0)], itp_type_head_armor|itp_civilian, 0, ############ Combine  ############
  35, weight(1.25)|abundance(100)|head_armor(14)|difficulty(0) ,imodbits_cloth ],
 ["gg_pilgrim_outfit", "Pilgrim Robe", [("gg_pilgrim_outfit",0)], itp_type_body_armor  |itp_covers_legs ,0,  ############ Combine  ############
  1000 , weight(3)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(8)|difficulty(0) ,imodbits_cloth ],



 # ["gg_light_leather", "Light Leather", [("gg_light_leather",0)], itp_type_body_armor  |itp_covers_legs ,0,
  # 1200 , weight(1)|abundance(100)|head_armor(0)|body_armor(15)|leg_armor(1)|difficulty(0) ,imodbits_cloth ],
 # ["gg_thick_coat_a", "Thick Coat", [("gg_thick_coat_a",0)], itp_type_body_armor  |itp_covers_legs ,0,
  # 1000 , weight(1)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],

 # ["gg_green_tunic", "Green Tunic", [("gg_green_tunic",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ MAIN  ############
  # 800 , weight(1)|abundance(100)|head_armor(0)|body_armor(13)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],

# ["gg_leather_armored_green_tunic", "Green Tunic with Leather Armor", [("gg_leather_armored_green_tunic",0)], itp_type_body_armor  |itp_covers_legs ,0, 
#  3540 , weight(6.5)|abundance(100)|head_armor(0)|body_armor(29)|leg_armor(10)|difficulty(7) ,imodbits_cloth ],

 # ["gg_coat_of_plates_b", "Vaegir Fur Coat", [("gg_coat_of_plates_b",0)], itp_type_body_armor  |itp_covers_legs ,0,
  # 500 , weight(1)|abundance(100)|head_armor(0)|body_armor(12)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
 # ["gg_turkish_robe", "Kaftan", [("gg_turkish_robe",0)], itp_type_body_armor  |itp_covers_legs ,0,
  # 400 , weight(1)|abundance(100)|head_armor(0)|body_armor(12)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
 # ["gg_robe", "Black Robe", [("gg_robe",0)], itp_type_body_armor  |itp_covers_legs ,0,
  # 200 , weight(1)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
 # ["gg_shirt", "Shirt", [("gg_shirt",0)], itp_type_body_armor  |itp_covers_legs ,0,
 # 150 , weight(1)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],



################################################ -PK Yeni Eklenenler- #######################################################

  #T4 Tier 4
  ["hauberk_light", "Hauberk Armor", [("hauberk_light",0)], itp_type_body_armor  |itp_covers_legs ,0,   ############ MAIN  ############
   4750 , weight(13)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(14)|difficulty(15) ,imodbits_armor ],
  ["reinforced_hauberk", "Reinforced Hauberk Armor", [("reinforced_hauberk",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
   7250 , weight(13)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(14)|difficulty(15) ,imodbits_armor ],
  ["heavy_hauberk", "Heavy Hauberk Armor", [("heavy_hauberk",0)], itp_type_body_armor  |itp_covers_legs ,0, ############ EXTRA  ############
   16000 , weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21) ,imodbits_plate ],

##  ["white_assassin_cape","White Assassin Cape", [("white_assassin_cape", 0)], itp_type_head_armor|itp_civilian, 0, ############ Combine ############   -    ############ MAIN  ############
##   100, weight(1)|abundance(100)|head_armor(25)|difficulty(0) ,imodbits_armor ],
  ["white_assassin_armor", "White Assassin Armor", [("white_assassin_armor",0)], itp_type_body_armor  |itp_covers_legs ,0,   ############ Combine  ############    -    ############ MAIN  ############
   200 , weight(6)|abundance(100)|head_armor(0)|body_armor(27)|leg_armor(12)|difficulty(7) ,imodbits_armor ],    

##  ["brown_assassin_cape","Brown Assassin Cape", [("brown_assassin_cape", 0)], itp_type_head_armor|itp_civilian, 0, ############ Combine ############    -    ############ EXTRA  ############
##   100, weight(1)|abundance(100)|head_armor(25)|difficulty(0) ,imodbits_armor ],
  ["brown_assassin_armor", "Brown Assassin Armor", [("brown_assassin_armor",0)], itp_type_body_armor  |itp_covers_legs ,0,   ############ Combine  ############    -    ############ EXTRA  ############
   3000 , weight(6)|abundance(100)|head_armor(0)|body_armor(27)|leg_armor(12)|difficulty(7) ,imodbits_armor ],

##  ["green_assassin_cape","Green Assassin Cape", [("green_assassin_cape", 0)], itp_type_head_armor|itp_civilian, 0, ############ Combine ############    -    ############ EXTRA  ############
##   100, weight(1)|abundance(100)|head_armor(25)|difficulty(0) ,imodbits_armor ],
  ["green_assassin_armor", "Green Assassin Armor", [("green_assassin_armor",0)], itp_type_body_armor  |itp_covers_legs ,0,   ############ Combine  ############    -    ############ EXTRA  ############
   200 , weight(6)|abundance(100)|head_armor(0)|body_armor(27)|leg_armor(12)|difficulty(7) ,imodbits_armor ],

##  ["green_assassin_cape","Green Assassin Cape", [("green_assassin_cape", 0)], itp_type_head_armor|itp_civilian, 0, ############ Combine ############    -    ############ EXTRA  ############
##   100, weight(1)|abundance(100)|head_armor(25)|difficulty(0) ,imodbits_armor ],
  ["armor8_g", "Red Assassin Armor", [("armor8_g",0)], itp_type_body_armor  |itp_covers_legs ,0,   ############ Combine  ############    -    ############ EXTRA  ############
   200 , weight(6)|abundance(100)|head_armor(0)|body_armor(27)|leg_armor(12)|difficulty(7) ,imodbits_armor ],

 ["ghulam_heavy_cavalryman_3", "Ghulam Elite Armor", [("ghulam_heavy_cavalryman_3", 0)], itp_type_body_armor|itp_covers_legs|itp_civilian|itp_merchandise, 0,
  21530, weight(23)   | abundance(100) | head_armor(0) | body_armor(48) | leg_armor(16) | difficulty(21), imodbits_plate ],
 ["turk_bandit_b", "Bandit Scale Armor", [("turk_bandit_b",0)], itp_type_body_armor  |itp_covers_legs ,0,
  5470 , weight(13)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(14)|difficulty(15) ,imodbits_armor ],
 ["armor_medium_tyrk_f", "Tyrk Armor", [("armor_medium_tyrk_f", 0)],  itp_type_body_armor  |itp_covers_legs|itp_civilian|itp_merchandise, 0,
  6450, weight(13) | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_armor ], 
 ["sar_infantry_armor", "Sarranid Scale Guard Armor", [("sar_infantry_armor", 0)],  itp_type_body_armor  |itp_covers_legs|itp_civilian|itp_merchandise, 0,
  6460, weight(13) | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_armor ], 
 ["turk_bandit_c", "Yere Varan Armor", [("turk_bandit_c", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,
  5860, weight(13) | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_armor ], 
 ["sar_lamellar_armor", "Sarranid Scale Armor", [("sar_lamellar_armor", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,
  14310, weight(16) | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ],
 ["studded_coat_mail_a", "Studded Coat Mail", [("studded_coat_mail_a", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,
  5300, weight(13) | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_armor ],
 ["ragged_armour_a", "Ragged Armour", [("ragged_armour_a", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,
  4000, weight(7.2)  | abundance(100) | head_armor(0) | body_armor(30) | leg_armor(4)  | difficulty(10), imodbits_armor ],
 ["gambeson_brown", "Gambeson Brown", [("gambeson_brown", 0)], itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,  
  4500, weight(9)  | abundance(100) | head_armor(0) | body_armor(33) | leg_armor(6) | difficulty(12), imodbits_armor ], 


################################################ -YENI NARF ITEMLERI VE VARYASYONLARI- #######################################################


  ["gg_new_brigandine_light_green", "New Light Green Brigandine", [("gg_new_brigandine_light_green",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, ### MAIN
    3750, weight(7.2)   | abundance(100) | head_armor(0) | body_armor(30) | leg_armor(4)  | difficulty(10), imodbits_armor ],
  ["gg_new_brigandine_light_red", "New Light Red Brigandine", [("gg_new_brigandine_light_red",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, ### COLOUR
    100, weight(7.2)   | abundance(100) | head_armor(0) | body_armor(30) | leg_armor(4)  | difficulty(10), imodbits_armor ],
  ["gg_new_brigandine_light_blue", "New Light Blue Brigandine", [("gg_new_brigandine_light_blue",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, ### COLOUR
    100, weight(7.2)   | abundance(100) | head_armor(0) | body_armor(30) | leg_armor(4)  | difficulty(10), imodbits_armor ],
  ["gg_new_brigandine_light_black", "New Light Black Brigandine", [("gg_new_brigandine_light_black",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, ### COLOUR
    100, weight(7.2)   | abundance(100) | head_armor(0) | body_armor(30) | leg_armor(4)  | difficulty(10), imodbits_armor ],
  ["gg_new_brigandine_light_brown", "New Light Brown Brigandine", [("gg_new_brigandine_light_brown",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, ### COLOUR
    100, weight(7.2)   | abundance(100) | head_armor(0) | body_armor(30) | leg_armor(4)  | difficulty(10), imodbits_armor ],
  ["gg_new_brigandine_light_purple", "New Light Purple Brigandine", [("gg_new_brigandine_light_purple",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, ### COLOUR
    100, weight(7.2)   | abundance(100) | head_armor(0) | body_armor(30) | leg_armor(4)  | difficulty(10), imodbits_armor ],
  ["gg_new_brigandine_light_yellow", "New Light Yellow Brigandine", [("gg_new_brigandine_light_yellow",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, ### COLOUR
    100, weight(7.2)   | abundance(100) | head_armor(0) | body_armor(30) | leg_armor(4)  | difficulty(10), imodbits_armor ],
  ["gg_new_brigandine_light_white", "New Light White Brigandine", [("gg_new_brigandine_light_white",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, ### COLOUR
    100, weight(7.2)   | abundance(100) | head_armor(0) | body_armor(30) | leg_armor(4)  | difficulty(10), imodbits_armor ],

  ["gg_new_medium_brigandine_green", "New Medium Green Brigandine", [("gg_new_medium_brigandine_green",0)], itp_type_body_armor|itp_covers_legs, 0, ### MAIN
    5200, weight(13)   | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14)  | difficulty(15), imodbits_armor ],
  ["gg_new_medium_brigandine_red", "New Medium Red Brigandine", [("gg_new_medium_brigandine_red",0)], itp_type_body_armor|itp_covers_legs, 0, ### COLOUR
    100, weight(13)   | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14)  | difficulty(15), imodbits_armor ],
  ["gg_new_medium_brigandine_blue", "New Medium Blue Brigandine", [("gg_new_medium_brigandine_blue",0)], itp_type_body_armor|itp_covers_legs, 0, ### COLOUR
    100, weight(13)   | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14)  | difficulty(15), imodbits_armor ],
  ["gg_new_medium_brigandine_black", "New Medium Black Brigandine", [("gg_new_medium_brigandine_black",0)], itp_type_body_armor|itp_covers_legs, 0, ### COLOUR
    100, weight(13)   | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14)  | difficulty(15), imodbits_armor ],
  ["gg_new_medium_brigandine_brown", "New Medium Brown Brigandine", [("gg_new_medium_brigandine_brown",0)], itp_type_body_armor|itp_covers_legs, 0, ### COLOUR
    100, weight(13)   | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14)  | difficulty(15), imodbits_armor ],
  ["gg_new_medium_brigandine_purple", "New Medium Purple Brigandine", [("gg_new_medium_brigandine_purple",0)], itp_type_body_armor|itp_covers_legs, 0, ### COLOUR
    100, weight(13)   | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14)  | difficulty(15), imodbits_armor ],
  ["gg_new_medium_brigandine_yellow", "New Medium Yellow Brigandine", [("gg_new_medium_brigandine_yellow",0)], itp_type_body_armor|itp_covers_legs, 0, ### COLOUR
    100, weight(13)   | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14)  | difficulty(15), imodbits_armor ],
  ["gg_new_medium_brigandine_white", "New Medium White Brigandine", [("gg_new_medium_brigandine_white",0)], itp_type_body_armor|itp_covers_legs, 0, ### COLOUR
    100, weight(13)   | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14)  | difficulty(15), imodbits_armor ],


  ["gg_new_reinforced_brigandine_green", "New Reinforced Green Brigandine", [("gg_new_reinforced_brigandine_green",0)], itp_type_body_armor|itp_covers_legs, 0, ### MAIN
    11000, weight(16)   | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ],
  ["gg_new_reinforced_brigandine_red", "New Reinforced Red Brigandine", [("gg_new_reinforced_brigandine_red",0)], itp_type_body_armor|itp_covers_legs, 0, ### COLOUR
    100, weight(16)   | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ],
  ["gg_new_reinforced_brigandine_blue", "New Reinforced Blue Brigandine", [("gg_new_reinforced_brigandine_blue",0)], itp_type_body_armor|itp_covers_legs, 0, ### COLOUR
    100, weight(16)   | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ],
  ["gg_new_reinforced_brigandine_black", "New Reinforced Black Brigandine", [("gg_new_reinforced_brigandine_black",0)], itp_type_body_armor|itp_covers_legs, 0, ### COLOUR
    100, weight(16)   | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ],
  ["gg_new_reinforced_brigandine_brown", "New Reinforced Brown Brigandine", [("gg_new_reinforced_brigandine_brown",0)], itp_type_body_armor|itp_covers_legs, 0, ### COLOUR
    100, weight(16)   | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ],
  ["gg_new_reinforced_brigandine_purple", "New Reinforced Purple Brigandine", [("gg_new_reinforced_brigandine_purple",0)], itp_type_body_armor|itp_covers_legs, 0, ### COLOUR
    100, weight(16)   | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ],
  ["gg_new_reinforced_brigandine_yellow", "New Reinforced Yellow Brigandine", [("gg_new_reinforced_brigandine_yellow",0)], itp_type_body_armor|itp_covers_legs, 0, ### COLOUR
    100, weight(16)   | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ],
  ["gg_new_reinforced_brigandine_white", "New Reinforced White Brigandine", [("gg_new_reinforced_brigandine_white",0)], itp_type_body_armor|itp_covers_legs, 0, ### COLOUR
    100, weight(16)   | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ],


  ["gg_new_heavy_plate_mail_brigandine_green", "New Heavy Brigandine Green", [("gg_new_heavy_plate_mail_brigandine_green",0)], itp_type_body_armor|itp_covers_legs, 0, ### MAIN
    18000, weight(23)   | abundance(100) | head_armor(0) | body_armor(48) | leg_armor(16) | difficulty(21), imodbits_plate ],
  ["gg_new_heavy_plate_mail_brigandine_red", "New Heavy Brigandine Red", [("gg_new_heavy_plate_mail_brigandine_red",0)], itp_type_body_armor|itp_covers_legs, 0, ### COLOUR
    100, weight(23)   | abundance(100) | head_armor(0) | body_armor(48) | leg_armor(16) | difficulty(21), imodbits_plate ],
  ["gg_new_heavy_plate_mail_brigandine_blue", "New Heavy Brigandine Blue", [("gg_new_heavy_plate_mail_brigandine_blue",0)], itp_type_body_armor|itp_covers_legs, 0, ### COLOUR
    100, weight(23)   | abundance(100) | head_armor(0) | body_armor(48) | leg_armor(16) | difficulty(21), imodbits_plate ],
  ["gg_new_heavy_plate_mail_brigandine_black", "New Heavy Brigandine Black", [("gg_new_heavy_plate_mail_brigandine_black",0)], itp_type_body_armor|itp_covers_legs, 0, ### COLOUR
    100, weight(23)   | abundance(100) | head_armor(0) | body_armor(48) | leg_armor(16) | difficulty(21), imodbits_plate ],
  ["gg_new_heavy_plate_mail_brigandine_brown", "New Heavy Brigandine Brown", [("gg_new_heavy_plate_mail_brigandine_brown",0)], itp_type_body_armor|itp_covers_legs, 0, ### COLOUR
    100, weight(23)   | abundance(100) | head_armor(0) | body_armor(48) | leg_armor(16) | difficulty(21), imodbits_plate ],
  ["gg_new_heavy_plate_mail_brigandine_purple", "New Heavy Brigandine Purple", [("gg_new_heavy_plate_mail_brigandine_purple",0)], itp_type_body_armor|itp_covers_legs, 0, ### COLOUR
    100, weight(23)   | abundance(100) | head_armor(0) | body_armor(48) | leg_armor(16) | difficulty(21), imodbits_plate ],
  ["gg_new_heavy_plate_mail_brigandine_yellow", "New Heavy Brigandine Yellow", [("gg_new_heavy_plate_mail_brigandine_yellow",0)], itp_type_body_armor|itp_covers_legs, 0, ### COLOUR
    100, weight(23)   | abundance(100) | head_armor(0) | body_armor(48) | leg_armor(16) | difficulty(21), imodbits_plate ],
  ["gg_new_heavy_plate_mail_brigandine_white", "New Heavy Brigandine White", [("gg_new_heavy_plate_mail_brigandine_white",0)], itp_type_body_armor|itp_covers_legs, 0, ### COLOUR
    100, weight(23)   | abundance(100) | head_armor(0) | body_armor(48) | leg_armor(16) | difficulty(21), imodbits_plate ],



################################################ GOLD AND GLORY BODY ARMORS END ################################################

#Cakebatter Heraldic start
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# Armour Body
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#-------------------------------------------------------------------------------------------------
# Plates Heraldic Start
#-------------------------------------------------------------------------------------------------
["gothic_plate_1_heraldic", "Heraldic New Area Gothic Plate", [("gothic_plate_1_heraldic_mesh",0)], itp_type_body_armor|itp_covers_legs,0,
  24550,weight(28)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(21)|difficulty(24),imodbits_plate, 
  [(ti_on_init_item,
    [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_gothic_plate_1_heraldic", ":agent_no", ":troop_no"),
    ])]
],#Above item is heraldic version of: gothic_heavy_plate_blue
["gothic_plate_1_shoulders_heraldic", "Heraldic New Area Gothic Plate with Shoulderplates", [("gothic_plate_1_shoulders_heraldic_mesh",0)], itp_type_body_armor|itp_covers_legs,0,
  2455,weight(28)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(21)|difficulty(24),imodbits_plate, 
  [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_gothic_plate_1_heraldic", ":agent_no", ":troop_no")])]
],#Above item is heraldic version of: gothic_heavy_plate_blue_with_shoulders

["gothic_plate_2_heraldic", "Heraldic Masterwork Plate Armor", [("gothic_plate_2_heraldic_mesh",0)], itp_type_body_armor|itp_covers_legs,0,
  1500,weight(28)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(21)|difficulty(24),imodbits_plate, 
  [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_gothic_plate_2_heraldic", ":agent_no", ":troop_no")])]
],#Above item is heraldic version of: milanese_armour - new model

["heavy_plate_1_heraldic", "Heraldic Dread Plate Armor", [("heavy_plate_1_heraldic_mesh",0)], itp_type_body_armor|itp_covers_legs,0,
  1500, weight(34) | abundance(100) | head_armor(1) | body_armor(55) | leg_armor(23) | difficulty(24), imodbits_plate,
  [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_heavy_plate_1_heraldic", ":agent_no", ":troop_no")])]
],#Above item is heraldic version of: heavy_dread_plate - Remodelled, re-rigged, retextured
#-------------------------------------------------------------------------------------------------
# Churburgs Heraldic Start
#-------------------------------------------------------------------------------------------------
["churburg_plate_padded_heraldic", "Heraldic Churburg Plate Armor", [("churburg_plate_padded_heraldic_mesh",0)], itp_type_body_armor|itp_covers_legs,0,
  25550,weight(28)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(21)|difficulty(24),imodbits_plate, 
  [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_churburg_plate_padded_heraldic", ":agent_no", ":troop_no")])]
],#Above item is heraldic version of: churburg_13
["churburg_gilded_plate_padded_heraldic", "Heraldic Gilded Churburg Plate Armor", [("churburg_gilded_plate_padded_heraldic_mesh",0)], itp_type_body_armor|itp_covers_legs,0,
  1400,weight(28)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(21)|difficulty(24),imodbits_plate, 
  [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_churburg_gilded_plate_padded_heraldic", ":agent_no", ":troop_no")])]
],#Above item is heraldic version of: churburg_13_brass
#-------------------------------------------------------------------------------------------------
# Brigandines Heraldic Start
#-------------------------------------------------------------------------------------------------
["brigandine_1_light_padded_heraldic", "Heraldic Light Padded Brigandine", [("brigandine_1_light_padded_heraldic_mesh",0)], itp_type_body_armor|itp_covers_legs,0,
  3750,weight(7.2)|abundance(100)|head_armor(0)|body_armor(30)|leg_armor(4)|difficulty(10),imodbits_armor,
  [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_brigandine_1_padded_heraldic", ":agent_no", ":troop_no")])]
],#Above item is heraldic version of: gg_new_brigandine_light_green - gg_new_brigandine_light_green and narf_brigandine_green had almost the same model & texture. Only made one heraldic

["brigandine_1_medium_padded_heraldic", "Heraldic Medium Padded Brigandine", [("brigandine_1_medium_padded_heraldic_mesh",0)], itp_type_body_armor|itp_covers_legs,0,
  375,weight(8.2)|abundance(100)|head_armor(0)|body_armor(31)|leg_armor(10)|difficulty(11),imodbits_armor,
  [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_brigandine_1_padded_heraldic", ":agent_no", ":troop_no")])]
],#Above item is heraldic version of: gg_new_brigandine_light_green - Added kneecops - Changed to medium

["brigandine_1_reinforced_padded_heraldic", "Heraldic Reinforced Padded Brigandine", [("brigandine_1_reinforced_padded_heraldic_mesh",0)], itp_type_body_armor|itp_covers_legs,0,
  5200,weight(13)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(14)|difficulty(15),imodbits_armor,
  [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_brigandine_1_padded_heraldic", ":agent_no", ":troop_no")])]
],#Above item is heraldic version of: gg_new_medium_brigandine_green - Changed to reinforced

["brigandine_1_heavy_padded_heraldic", "Heraldic Heavy Padded Brigandine", [("brigandine_1_heavy_padded_heraldic_mesh",0)],itp_type_body_armor|itp_covers_legs,0,
  11000,weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18),imodbits_armor,
  [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_brigandine_1_padded_heraldic", ":agent_no", ":troop_no")])]
],#Above item is heraldic version of: gg_new_reinforced_brigandine_green - Changed to heavy

["brigandine_1_light_chainmail_heraldic", "Heraldic Light Chainmail Brigandine", [("brigandine_1_light_chainmail_heraldic_mesh",0)], itp_type_body_armor|itp_covers_legs,0,
  9050,weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18),imodbits_armor,
  [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_brigandine_1_chainmail_heraldic", ":agent_no", ":troop_no")])]
],#Above item is heraldic version of: m_narf_brigandine_green_mail - Remade to use same model & texture as brigandine 1

["brigandine_1_medium_chainmail_heraldic", "Heraldic Medium Chainmail Brigandine", [("brigandine_1_medium_chainmail_heraldic_mesh",0)], itp_type_body_armor|itp_covers_legs,0,
  870,weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18),imodbits_armor,
  [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_brigandine_1_chainmail_heraldic", ":agent_no", ":troop_no")])]
],#Above item is heraldic version of: m_narf_brigandine_green_mail_cuisses - Remade to use same model & texture as brigandine 1

["brigandine_1_medium_chainmail_long_heraldic", "Heraldic Medium Long Chainmail Brigandine", [("brigandine_1_medium_chainmail_long_heraldic_mesh",0)], itp_type_body_armor|itp_covers_legs,0,
  870,weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18),imodbits_armor,
  [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_brigandine_1_chainmail_heraldic", ":agent_no", ":troop_no")])]
],#Above item is heraldic NEW VERSION of: m_narf_brigandine_green_mail_cuisses - Remade to use same model & texture as brigandine 1 - Added longer chainmail at legs & arms

["brigandine_1_heavy_chainmail_heraldic", "Heraldic Heavy Chainmail Brigandine", [("brigandine_1_heavy_chainmail_heraldic_mesh",0)],itp_type_body_armor|itp_covers_legs,0,
  18000,weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21),imodbits_plate,
  [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_brigandine_1_chainmail_heraldic", ":agent_no", ":troop_no")])]
],#Above item is heraldic version of: gg_new_heavy_plate_mail_brigandine_green

["brigandine_1_heavy_chainmail_long_heraldic", "Heraldic Heavy Long Chainmail Brigandine", [("brigandine_1_heavy_chainmail_long_heraldic_mesh",0)],itp_type_body_armor|itp_covers_legs,0,
  1800,weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21),imodbits_plate,
  [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_brigandine_1_chainmail_heraldic", ":agent_no", ":troop_no")])]
],#Above item is heraldic NEW VERSION of: gg_new_heavy_plate_mail_brigandine_green - Added longer chainmail at legs
#-------------------------------------------------------------------------------------------------
# Lamellar Heraldic Start
#-------------------------------------------------------------------------------------------------
["lamellar_armor_1_heraldic", "Heraldic Khergit Elite Armor", [("lamellar_armor_1_heraldic_mesh",0)], itp_type_body_armor|itp_covers_legs,0,
  500,weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21),imodbits_plate,
  [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_lamellar_armor_1_heraldic", ":agent_no", ":troop_no")])]
],#Above item is heraldic version of: old_lamellar_armor_d

["lamellar_armor_1v2_heraldic", "Heraldic Khergit Elite Armor", [("lamellar_armor_1v2_heraldic_mesh",0)], itp_type_body_armor|itp_covers_legs,0,
  750,weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21),imodbits_plate,
  [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_lamellar_armor_1v2_heraldic", ":agent_no", ":troop_no")])]
],#Above item is heraldic version of: new_lamellar_armor

["lamellar_armor_2_heraldic", "Heraldic Khergit Guard Armor", [("lamellar_armor_2_heraldic_mesh",0)], itp_type_body_armor|itp_covers_legs,0,
  250,weight(13)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(14)|difficulty(15),imodbits_armor,
  [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_lamellar_armor_2_heraldic", ":agent_no", ":troop_no")])]
],#Above item is heraldic version of: lamellar_armor_b

["lamellar_armor_3_heraldic", "Heraldic Vaegir Decorated Armor", [("lamellar_armor_3_heraldic_mesh",0)], itp_type_body_armor|itp_covers_legs,0,
  750,weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21),imodbits_plate,
  [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_lamellar_armor_3_heraldic", ":agent_no", ":troop_no")])]
],#Above item is heraldic version of: lamellar_armor_c

["lamellar_armor_4_heraldic", "Heraldic Lamellar Vest", [("lamellar_armor_4_heraldic_mesh",0)], itp_type_body_armor|itp_covers_legs,0,
  200,weight(6.5)|abundance(100)|head_armor(0)|body_armor(29)|leg_armor(10)|difficulty(8),imodbits_cloth,
  [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_lamellar_armor_4_heraldic", ":agent_no", ":troop_no")])]
],#Above item is heraldic version of: lamellar_vest_a

["lamellar_armor_5_heraldic", "Heraldic Steppe Armor", [("lamellar_armor_5_heraldic_mesh",0)], itp_type_body_armor|itp_covers_legs,0,
  350,weight(2.25)|abundance(100)|head_armor(0)|body_armor(15)|leg_armor(8)|difficulty(0),imodbits_cloth,
  [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_lamellar_armor_5_heraldic", ":agent_no", ":troop_no")])]
],#Above item is heraldic version of: lamellar_leather

["lamellar_armor_6_heraldic", "Heraldic Vaegir Elite Armor", [("lamellar_armor_6_heraldic_mesh",0)], itp_type_body_armor|itp_covers_legs,0,
  375,weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21),imodbits_plate,
  [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_lamellar_armor_6_heraldic", ":agent_no", ":troop_no")])]
],#Above item is heraldic version of: drz_elite_lamellar_armor

["lamellar_armor_7_heraldic", "Heraldic Vaegir Lamellar Armor", [("lamellar_armor_7_heraldic_mesh",0)], itp_type_body_armor|itp_covers_legs,0,
  350,weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18),imodbits_armor,
  [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_lamellar_armor_7_heraldic", ":agent_no", ":troop_no")])]
],#Above item is heraldic version of: drz_lamellar_armor

["lamellar_armor_8_heraldic", "Heraldic Vaegir Guard Armor", [("lamellar_armor_8_heraldic_mesh",0)], itp_type_body_armor|itp_covers_legs,0,
  200,weight(15)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18),imodbits_armor,
  [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_lamellar_armor_8_heraldic", ":agent_no", ":troop_no")])]
],#Above item is heraldic version of: rus_lamellar_a & rus_lamellar_b
["lamellar_armor_9_heraldic", "Heraldic Sarranid Guard Armor", [("lamellar_armor_9_heraldic_mesh",0)], itp_type_body_armor|itp_covers_legs,0,
  100,weight(15)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(15)|difficulty(15),imodbits_armor,
  [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_lamellar_armor_9_heraldic", ":agent_no", ":troop_no")])]
],#Above item is heraldic version of: *unknown*
#Cakebatter Heraldic end

#Sartiye/Nessa Heraldic start
["lamellar_armor_10_heraldic", "Heraldic Brigandine", [("brigandine_b",0)], itp_type_body_armor|itp_covers_legs,0,
  100,weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(18),imodbits_armor,
  [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_lamellar_armor_10_heraldic", ":agent_no", ":troop_no")])]
],#Above item is heraldic version of: brigandine_b
["lamellar_armor_11_heraldic", "Heraldic Coat of Plates", [("coat_of_plates_red",0)], itp_type_body_armor|itp_covers_legs,0,
  100,weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(21),imodbits_armor,
  [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_lamellar_armor_11_heraldic", ":agent_no", ":troop_no")])]
],#Above item is heraldic version of: coat_of_plates_red
#Sartiye/Nessa Heraldic end

#Nessa armors start 2025
["borov_brigandine_a", "Borovod Purple Brigandine", [("borov_brigandine_a",0)], itp_type_body_armor|itp_covers_legs, 0, ### MAIN
    18100, weight(23)   | abundance(100) | head_armor(0) | body_armor(48) | leg_armor(16) | difficulty(21), imodbits_armor ],
["borov_brigandine_a2", "Borovod Dark Brigandine", [("borov_brigandine_a2",0)], itp_type_body_armor|itp_covers_legs, 0, ### MOD
    100, weight(23)   | abundance(100) | head_armor(0) | body_armor(48) | leg_armor(16) | difficulty(21), imodbits_armor ],

["borovod_coat_of_plates_a", "Plated Dark Kuyak", [("borovod_coat_of_plates_a",0)], itp_type_body_armor|itp_covers_legs, 0, ### MAIN
    17500, weight(23)   | abundance(100) | head_armor(0) | body_armor(48) | leg_armor(16) | difficulty(21), imodbits_armor ],
["borovod_coat_of_plates_a2", "Plated Light Kuyak", [("borovod_coat_of_plates_a2",0)], itp_type_body_armor|itp_covers_legs, 0, ### MOD
    400, weight(23)   | abundance(100) | head_armor(0) | body_armor(48) | leg_armor(16) | difficulty(21), imodbits_armor ],
["borovod_coat_of_plates_b", "Armoured Light Kuyak", [("borovod_coat_of_plates_b",0)], itp_type_body_armor|itp_covers_legs, 0, ### MAIN
    10500, weight(16)   | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ],
["borovod_coat_of_plates_b2", "Armoured Dark Kuyak", [("borovod_coat_of_plates_b2",0)], itp_type_body_armor|itp_covers_legs, 0, ### MOD
    300, weight(16)   | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ],
["borovod_coat_of_plates_c", "Borovod Light Kuyak", [("borovod_coat_of_plates_c",0)], itp_type_body_armor|itp_covers_legs, 0, ### MAIN
    6800, weight(13)   | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_armor ],
["borovod_coat_of_plates_c2", "Borovod Dark Kuyak", [("borovod_coat_of_plates_c2",0)], itp_type_body_armor|itp_covers_legs, 0, ### MOD
    200, weight(13)   | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_armor ],

["new_churburg", "Golden Churburg", [("new_churburg",0)], itp_type_body_armor|itp_covers_legs, 0, ### RARE MAIN
    180000, weight(28)   | abundance(100) | head_armor(0) | body_armor(52) | leg_armor(21) | difficulty(24), imodbits_armor ],
["new_churburg_full", "Golden Churburg", [("new_churburg",0)], itp_type_body_armor|itp_covers_legs, 0, ### RARE MOD
    50000, weight(28)   | abundance(100) | head_armor(0) | body_armor(52) | leg_armor(21) | difficulty(24), imodbits_armor ],


["khergit_fur_lam", "Khergit Fur Lamellar", [("khergit_fur_lam",0)], itp_type_body_armor|itp_covers_legs, 0, ### MAIN
    4050, weight(7.6)   | abundance(100) | head_armor(0) | body_armor(31) | leg_armor(4) | difficulty(10), imodbits_armor ],
["khan_coat", "Archer Coat", [("khan_coat",0)], itp_type_body_armor|itp_covers_legs, 0, ### MAIN
    3600, weight(7.2)   | abundance(100) | head_armor(0) | body_armor(29) | leg_armor(9) | difficulty(8), imodbits_armor ],
["lamellar_armor_e1", "Lamellar Scale Armor", [("lamellar_armor_e1",0)], itp_type_body_armor|itp_covers_legs, 0, ### HATALI
    0, weight(15)   | abundance(100) | head_armor(0) | body_armor(42) | leg_armor(14) | difficulty(15), imodbits_armor ],
["lamellar_armor_e_leather1", "Lamellar Leather Armor", [("lamellar_armor_e_leather1",0)], itp_type_body_armor|itp_covers_legs, 0, ### MAIN
    8250, weight(15)   | abundance(100) | head_armor(0) | body_armor(42) | leg_armor(14) | difficulty(15), imodbits_armor ],

["arab_bandit_b", "Gulam Armor", [("arab_bandit_b",0)], itp_type_body_armor|itp_covers_legs, 0, ### MAIN
    60000, weight(13)   | abundance(100) | head_armor(0) | body_armor(40) | leg_armor(14) | difficulty(15), imodbits_armor ],
["brigandine_black_plate", "Black Plated Brigandine", [("brigandine_black_plate",0)], itp_type_body_armor|itp_covers_legs, 0, ### MAIN
    22500, weight(23)   | abundance(100) | head_armor(0) | body_armor(48) | leg_armor(16) | difficulty(21), imodbits_armor ],

["gg_red_scale_armor_red", "Red Scale Armor", [("gg_red_scale_armor_red", 0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise, 0,                    ######## MAIN ########
    300, weight(16)   | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ],
["gg_red_scale_armor_f", "Red Scale Armor with Kneecops", [("gg_red_scale_armor_f", 0)], itp_type_body_armor|itp_covers_legs, 0,                    ######## EXTRA ########   
    600, weight(16) | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ],
["gg_red_scale_armor_f_with_plate", "Red Scale Armor with Plate Cuisses", [("gg_red_scale_armor_f_with_plate", 0)], itp_type_body_armor|itp_covers_legs, 0,                     ######## EXTRA ########  
    1000, weight(16)   | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ],

["arabian_light_armor_a", "White Arabian Armor", [("arabian_light_armor_a",0)], itp_type_body_armor|itp_covers_legs, 0, ### MAIN
    3800, weight(7.2)   | abundance(100) | head_armor(0) | body_armor(29) | leg_armor(9) | difficulty(7), imodbits_armor ],
["arabian_light_armor_b", "Orange Arabian Armor", [("arabian_light_armor_b",0)], itp_type_body_armor|itp_covers_legs, 0, ### MOD
    100, weight(7.2)   | abundance(100) | head_armor(0) | body_armor(29) | leg_armor(9) | difficulty(7), imodbits_armor ],
["arabian_light_armor_c", "Red Arabian Armor", [("arabian_light_armor_c",0)], itp_type_body_armor|itp_covers_legs, 0, ### MOD
    100, weight(7.2)   | abundance(100) | head_armor(0) | body_armor(29) | leg_armor(9) | difficulty(7), imodbits_armor ],
["arabian_light_armor_d", "Blue Arabian Armor", [("arabian_light_armor_d",0)], itp_type_body_armor|itp_covers_legs, 0, ### MOD
    100, weight(7.2)   | abundance(100) | head_armor(0) | body_armor(29) | leg_armor(9) | difficulty(7), imodbits_armor ],

["armor_archer_saracin_1", "Saracen Archer Armor", [("armor_archer_saracin_1",0)], itp_type_body_armor|itp_covers_legs, 0, ### MAIN
    4350, weight(7.2)   | abundance(100) | head_armor(0) | body_armor(30) | leg_armor(4) | difficulty(7), imodbits_armor ],
["armor_archer_saracin_2", "Saracen Archer Armor", [("armor_archer_saracin_2",0)], itp_type_body_armor|itp_covers_legs, 0, ### MOD
    100, weight(7.2)   | abundance(100) | head_armor(0) | body_armor(30) | leg_armor(4) | difficulty(7), imodbits_armor ],
["armor_archer_saracin_3", "Saracen Archer Armor", [("armor_archer_saracin_3",0)], itp_type_body_armor|itp_covers_legs, 0, ### MOD
    100, weight(7.2)   | abundance(100) | head_armor(0) | body_armor(30) | leg_armor(4) | difficulty(7), imodbits_armor ],
["armor_archer_saracin_4", "Saracen Archer Armor", [("armor_archer_saracin_4",0)], itp_type_body_armor|itp_covers_legs, 0, ### MOD
    100, weight(7.2)   | abundance(100) | head_armor(0) | body_armor(30) | leg_armor(4) | difficulty(7), imodbits_armor ],
["armor_archer_saracin_5", "Saracen Archer Armor", [("armor_archer_saracin_5",0)], itp_type_body_armor|itp_covers_legs, 0, ### MOD
    100, weight(7.2)   | abundance(100) | head_armor(0) | body_armor(30) | leg_armor(4) | difficulty(7), imodbits_armor ],
["armor_archer_saracin_6", "Saracen Archer Armor", [("armor_archer_saracin_6",0)], itp_type_body_armor|itp_covers_legs, 0, ### MOD
    100, weight(7.2)   | abundance(100) | head_armor(0) | body_armor(30) | leg_armor(4) | difficulty(7), imodbits_armor ],

["heavy_armor_arabs_a", "Saracen Infantry Armor", [("heavy_armor_arabs_a",0)], itp_type_body_armor|itp_covers_legs, 0, ### MAIN
    11000, weight(16)   | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ],
["heavy_armor_arabs_b", "Saracen Infantry Armor", [("heavy_armor_arabs_b",0)], itp_type_body_armor|itp_covers_legs, 0, ### MOD
    100, weight(16)   | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ],
["heavy_armor_arabs_c_1", "Saracen Infantry Armor", [("heavy_armor_arabs_c_1",0)], itp_type_body_armor|itp_covers_legs, 0, ### MOD
    100, weight(16)   | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ],
["heavy_armor_arabs_d", "Saracen Infantry Armor", [("heavy_armor_arabs_d",0)], itp_type_body_armor|itp_covers_legs, 0, ### MOD
    100, weight(16)   | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ],
["heavy_armor_arabs_e", "Saracen Infantry Armor", [("heavy_armor_arabs_e",0)], itp_type_body_armor|itp_covers_legs, 0, ### MOD
    100, weight(16)   | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ],
["heavy_armor_arabs_f_1", "Saracen Infantry Armor", [("heavy_armor_arabs_f_1",0)], itp_type_body_armor|itp_covers_legs, 0, ### MOD
    100, weight(16)   | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ],

["heavy_armor_arabs_c", "Saracen Cavalry Armor", [("heavy_armor_arabs_c",0)], itp_type_body_armor|itp_covers_legs, 0, ### MAIN
    10500, weight(16)   | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ],
["heavy_armor_arabs_f", "Saracen Cavalry Armor", [("heavy_armor_arabs_f",0)], itp_type_body_armor|itp_covers_legs, 0, ### MOD
    100, weight(16)   | abundance(100) | head_armor(0) | body_armor(44) | leg_armor(15) | difficulty(18), imodbits_armor ],


    ["m_body_end", "Body End", [("invisible",0)], itp_type_body_armor, 0, 0 , weight(0)|abundance(0)|head_armor(0)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
    




################################################ BODY ARMORS END ################################################




    # LEG ARMORS

#    ["m_wrapping_boots", "Wrapping Boots", [("wrapping_boots_a",0)], itp_type_foot_armor|itp_civilian | itp_attach_armature|itp_merchandise, 0,
#   30,   weight(0.5) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(8)  | difficulty(0), imodbits_cloth, [m_stirrups_item_trigger]],




#    # ["m_Nobelman_hose", "Nobleman Hose", [("Nobelman_hose", 0)],  itp_type_foot_armor, 0,
#    0,    weight(4.0) | abundance(100) | head_armor(0) | body_armor(0)  | leg_armor(28) | difficulty(0), imodbits_armor, [m_stirrups_item_trigger]],
#    # ["m_Eldar_Boots", "Eldar Boots", [("Eldar_Boots", 0)],  itp_type_foot_armor, 0,
#    0,    weight(4.0) | abundance(100) | head_armor(0) | body_armor(0)  | leg_armor(28) | difficulty(0), imodbits_armor, [m_stirrups_item_trigger]],
#    # ["m_Noldor_Guard_Boots", "Noldor Guard Boots", [("Noldor_Guard_Boots", 0)],  itp_type_foot_armor, 0,
#    0,    weight(4.0) | abundance(100) | head_armor(0) | body_armor(0)  | leg_armor(28) | difficulty(0), imodbits_armor, [m_stirrups_item_trigger]],
#    # ["m_schwarzburg_gauntlets_L", "Schwarzburg Gauntlets", [("schwarzburg_gauntlets_L", 0)], itp_type_hand_armor, 0,
#    0,    weight(2.0) | abundance(100) | body_armor(6) | difficulty(0), imodbits_armor],
#    # ["m_pw_bishop_helm", "Bishop Helm", [("pw_bishop_helm",0)],  itp_type_head_armor|itp_covers_head, 0,
#    0,    weight(5.75)| abundance(100) | head_armor(54)| body_armor(0)  | leg_armor(0)  | difficulty(0), imodbits_plate ],

###################BUNU SILENIN AMINA KORUM###################
    ["m_ankle_boots", "Ankle Boots", [("ankle_boots_a_new", 0)],  itp_type_foot_armor |itp_civilian  | itp_attach_armature|itp_merchandise, 0,
     0,   weight(0.5) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(8)  | difficulty(0), imodbits_cloth, [m_stirrups_item_trigger]],
#    ["m_blue_hose", "Blue Hose", [("blue_hose_a", 0)],  itp_type_foot_armor |itp_civilian | itp_attach_armature|itp_merchandise, 0,
#     80,   weight(0.5) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(9)  | difficulty(0), imodbits_cloth, [m_stirrups_item_trigger]],
#    ["m_woolen_hose", "Woolen Hose", [("woolen_hose_a", 0)],  itp_type_foot_armor |itp_civilian | itp_attach_armature|itp_merchandise, 0,
#     100,  weight(0.5) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(9)  | difficulty(0), imodbits_cloth, [m_stirrups_item_trigger]],
#    ["m_sarranid_boots_a", "Sarranid Shoes", [("sarranid_shoes", 0)], itp_type_foot_armor |itp_civilian | itp_attach_armature|itp_merchandise, 0,
#     120,  weight(0.5) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(9)  | difficulty(0), imodbits_cloth, [m_stirrups_item_trigger]],
#    ["m_hunter_boots", "Hunter Boots", [("hunter_boots_a",0)], itp_type_foot_armor|itp_civilian|itp_attach_armature|itp_merchandise, 0,
#     130,  weight(0.5) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(10) | difficulty(0), imodbits_cloth, [m_stirrups_item_trigger]],
#    ["m_hide_boots", "Hide Boots", [("hide_boots_a", 0)],  itp_type_foot_armor |itp_civilian  | itp_attach_armature|itp_merchandise, 0,
#     170,  weight(0.75)| abundance(100) | head_armor(0) | body_armor(0) | leg_armor(12) | difficulty(0), imodbits_cloth, [m_stirrups_item_trigger]],
#    ["m_nomad_boots", "Nomad Boots", [("nomad_boots_a", 0)],  itp_type_foot_armor  |itp_civilian | itp_attach_armature|itp_merchandise, 0,
#     290,  weight(1.0) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(14) | difficulty(0), imodbits_cloth, [m_stirrups_item_trigger]],
#    ["m_khergit_leather_boots", "Black Boots", [("khergit_leather_boots", 0)],  itp_type_foot_armor |itp_civilian | itp_attach_armature|itp_merchandise, 0,
#     400,  weight(1.25)| abundance(100) | head_armor(0) | body_armor(0) | leg_armor(15) | difficulty(0), imodbits_cloth, [m_stirrups_item_trigger]],
#    ["m_sarranid_boots_black", "Black Boots with Buttons", [("cwe_civil_rich_boots_b", 0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise|itp_civilian, 0,
#     450,  weight(1.25)| abundance(100) | head_armor(0) | body_armor(0) | leg_armor(15) | difficulty(0), imodbits_cloth, [m_stirrups_item_trigger]],
#    ["m_sarranid_boots_red", "Red Boots with Buttons", [("cwe_civil_rich_boots_a", 0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise|itp_civilian, 0,
#     460,  weight(1.25)| abundance(100) | head_armor(0) | body_armor(0) | leg_armor(15) | difficulty(0), imodbits_cloth, [m_stirrups_item_trigger]],
#    ["m_light_leather_boots", "Light Leather Boots", [("m_light_leather_boots", 0)], itp_type_foot_armor | itp_attach_armature|itp_merchandise, 0,
#     500,  weight(1.25)| abundance(100) | head_armor(0) | body_armor(0) | leg_armor(15) | difficulty(0), imodbits_cloth, [m_stirrups_item_trigger]],
#    ["m_vaegir_leather_boots_2", "Dark Leather Boots", [("rus_cav_boots_2", 0)],  itp_type_foot_armor  |itp_civilian | itp_attach_armature|itp_merchandise, 0,
#     700,  weight(1.75)| abundance(100) | head_armor(0) | body_armor(0) | leg_armor(18) | difficulty(0), imodbits_cloth, [m_stirrups_item_trigger]], 
#   ["m_vaegir_leather_boots", "Red Leather Boots", [("rus_cav_boots", 0)],  itp_type_foot_armor  |itp_civilian | itp_attach_armature|itp_merchandise, 0,
#     730,  weight(1.75)| abundance(100) | head_armor(0) | body_armor(0) | leg_armor(18) | difficulty(0), imodbits_cloth, [m_stirrups_item_trigger]],
#    ["m_sarranid_boots_b", "Sarranid Leather Boots", [("sarranid_boots", 0)],  itp_type_foot_armor |itp_civilian | itp_attach_armature|itp_merchandise, 0,
#     800,  weight(1.75)| abundance(100) | head_armor(0) | body_armor(0) | leg_armor(18) | difficulty(0), imodbits_cloth, [m_stirrups_item_trigger]],
#    ["m_sarranid_boots_c", "Plated Boots", [("sarranid_camel_boots", 0)],  itp_type_foot_armor |itp_civilian | itp_attach_armature|itp_merchandise, 0,
#     1000, weight(2.5) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(21) | difficulty(7), imodbits_plate, [m_stirrups_item_trigger]], 
#    ["m_splinted_greaves", "Splinted Greaves", [("splinted_greaves_a", 0)],  itp_type_foot_armor | itp_attach_armature|itp_merchandise, 0,
#     1200, weight(2.75)| abundance(100) | head_armor(0) | body_armor(0) | leg_armor(22) | difficulty(7), imodbits_armor, [m_stirrups_item_trigger]],
#    ["m_mail_chausses", "Mail Chausses", [("mail_chausses_a", 0)],  itp_type_foot_armor | itp_attach_armature|itp_merchandise, 0,
#     1500, weight(3.0) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(23) | difficulty(8), imodbits_armor, [m_stirrups_item_trigger]],
#    ["m_sarranid_boots_d", "Sarranid Mail Boots", [("sarranid_mail_chausses", 0)],  itp_type_foot_armor |itp_civilian | itp_attach_armature|itp_merchandise, 0,
#     1800, weight(3.25)| abundance(100) | head_armor(0) | body_armor(0) | leg_armor(24) | difficulty(9), imodbits_armor, [m_stirrups_item_trigger]],
#    ["m_vaegir_splinted_greaves", "Vaegir Splinted Greaves", [("rus_splint_greaves",0)], itp_type_foot_armor | itp_attach_armature|itp_merchandise,0,
#     2150, weight(3.5) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(26) | difficulty(10), imodbits_armor, [m_stirrups_item_trigger]],
#    ["m_heavy_splinted_greaves", "Heavy Splinted Greaves", [("splinted_greaves_nospurs", 0)],  itp_type_foot_armor | itp_attach_armature|itp_merchandise, 0,
#     2500, weight(3.5) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(26) | difficulty(10), imodbits_armor, [m_stirrups_item_trigger]],
#    ["m_heavy_splinted_greaves_spurs", "Heavy Splinted Greaves with Spurs", [("splinted_greaves_spurs", 0)],  itp_type_foot_armor | itp_attach_armature, 0,
#     2500, weight(3.5) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(26) | difficulty(10), imodbits_armor, [m_stirrups_item_trigger]],
#    ["m_khergit_guard_boots", "Khergit Guard Boots", [("lamellar_boots_a", 0)], itp_type_foot_armor | itp_attach_armature|itp_merchandise, 0,
#     2850, weight(3.75)| abundance(100) | head_armor(0) | body_armor(0) | leg_armor(27) | difficulty(11), imodbits_cloth, [m_stirrups_item_trigger]], 
#    ["m_splinted_leather_greaves", "Splinted Leather Greaves", [("leather_greaves_a", 0)],  itp_type_foot_armor | itp_attach_armature|itp_merchandise, 0,
#     3200, weight(4.0) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(28) | difficulty(12), imodbits_armor, [m_stirrups_item_trigger]], 
#    ["m_steel_greaves_leather", "Plate Greaves", [("steel_greaves_leather", 0)],  itp_type_foot_armor | itp_attach_armature|itp_merchandise, 0,
#     3500, weight(4.25)| abundance(100) | head_armor(0) | body_armor(0) | leg_armor(29) | difficulty(14), imodbits_armor, [m_stirrups_item_trigger]],
#    ["m_steel_greaves_leather_spurs", "Plate Greaves with Spurs", [("steel_greaves_leather_spurs", 0)],  itp_type_foot_armor | itp_attach_armature, 0,
#     3500, weight(4.25)| abundance(100) | head_armor(0) | body_armor(0) | leg_armor(29) | difficulty(14), imodbits_armor, [m_stirrups_item_trigger]],
#    ["m_mail_boots_for_tableau", "Mail Boots", [("mail_boots_a", 0)], itp_type_foot_armor | itp_attach_armature|itp_merchandise, 0,
#     3650, weight(4.5) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(30) | difficulty(15), imodbits_armor, [m_stirrups_item_trigger]],
#    ["m_iron_greaves", "Iron Greaves", [("iron_greaves_a", 0)],  itp_type_foot_armor | itp_attach_armature|itp_merchandise, 0,
#     4100, weight(5.0) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(32) | difficulty(18), imodbits_armor, [m_stirrups_item_trigger]],
#    ["m_shynbaulds", "Mail and Plate Boots", [("shynbaulds",0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise,0,
#     4450, weight(5.0) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(32) | difficulty(18), imodbits_plate, [m_stirrups_item_trigger]],
#    ["m_steel_greaves", "Plate Boots", [("steel_greaves",0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise,0,
#     4800, weight(5.5) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(34) | difficulty(20), imodbits_plate, [m_stirrups_item_trigger]],


    

  ["m_narf_hose","Woolen_Hose", [("narf_hose", 0),("narf_hose_inv", ixmesh_inventory)], itp_type_foot_armor|itp_attach_armature|itp_civilian, 0,
   0, weight(0.5)|abundance(100)|leg_armor(10), imodbits_cloth, []],
  ["m_narf_hose_kneecops_red","Woolen_Hose_with_Kneecops", [("narf_hose_kneecops_red", 0),("narf_hose_kneecops_red_inv", ixmesh_inventory)], itp_type_foot_armor|itp_attach_armature|itp_civilian, 0,
   0, weight(3)|abundance(100)|leg_armor(22), imodbits_cloth, []],
  ["m_narf_hose_kneecops_green","Woolen_Hose_with_Kneecops", [("narf_hose_kneecops_green", 0),("narf_hose_kneecops_green_inv", ixmesh_inventory)], itp_type_foot_armor|itp_attach_armature|itp_civilian, 0,
   0, weight(3)|abundance(100)|leg_armor(22), imodbits_cloth, []],





######################################## GG LEG ARMORS ##################################################################################

   ["gg_shoes_yellow", "Yellow Shoes", [("gg_shoes_yellow",0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature ,0, ############ MAIN  ############
    150 , weight(0.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
   ["gg_shoes_brown", "Brown Shoes", [("gg_shoes_brown",0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature ,0, ############ EXTRA  ############
    10 , weight(0.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
   ["gg_shoes_green", "Green Shoes", [("gg_shoes_green",0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature ,0, ############ EXTRA  ############
    10 , weight(0.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(10)|difficulty(0) ,imodbits_cloth ], 
   ["gg_shoes_grey", "Grey Shoes", [("gg_shoes_grey",0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature ,0, ############ EXTRA  ############
    10 , weight(0.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
   ["gg_shoes_red", "Red Shoes", [("gg_shoes_red",0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature ,0, ############ EXTRA  ############
    10 , weight(0.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(10)|difficulty(0) ,imodbits_cloth ], 
   ["gg_shoes_blue", "Blue Shoes", [("gg_shoes_blue",0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature ,0, ############ EXTRA  ############
    10 , weight(0.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],

   ["gg_hide_boots_a", "Hide Boots", [("gg_hide_boots_a",0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature ,0,
    170 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(12)|difficulty(0) ,imodbits_cloth ],

   ["gg_hunter_boots_a", "Hunter Boots", [("gg_hunter_boots_a",0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature ,0, ############ MAIN  ############
    130, weight(0.5)|abundance(100)|leg_armor(10), imodbits_cloth, []],
   ["gg_bear_boots", "Bear Boots", [("gg_bear_boots",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0,  ############ EXTRA  ############
    670 , weight(2.50)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(18)|difficulty(0) ,imodbits_armor ],


   ["gg_ankle_boots_a_new", "Ankle Boots", [("gg_ankle_boots_a_new",0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature ,0,
    50, weight(0.5)|abundance(100)|leg_armor(8), imodbits_cloth, []],
   ["gg_sarranid_shoes", "Sarranid Shoes", [("gg_sarranid_shoes",0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature ,0,
    120, weight(0.5)|abundance(100)|leg_armor(9), imodbits_cloth, []],
   ["gg_sarranid_boots", "Sarranid Boots", [("gg_sarranid_boots",0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature ,0,
    800 , weight(1.8)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(18)|difficulty(0) ,imodbits_cloth ],
   ["gg_nomad_boots_a", "Nomad Boots", [("gg_nomad_boots_a",0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature ,0,
    290	, weight(1)|abundance(100)|leg_armor(14), imodbits_cloth, []],
   ["gg_leather_boots_a", "Leather Boots", [("gg_leather_boots_a",0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature ,0,
    600, weight(1.5)|abundance(100)|leg_armor(17), imodbits_cloth, []],
   ["gg_boot_light_blackr_d", "Nordland Shoes", [("gg_boot_light_blackr_d",0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature ,0,
    150, weight(0.75)|abundance(100)|leg_armor(12), imodbits_cloth, []],
   ["gg_rus_shoes", "Rus Shoes", [("gg_rus_shoes",0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature ,0,
     160, weight(0.75)|abundance(100)|leg_armor(12), imodbits_cloth, []],
   ["gg_leather_boots", "Fine Leather Boots", [("gg_leather_boots",0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature ,0,
    600 , weight(1.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(17)|difficulty(0) ,imodbits_cloth ],

   ["gg_boots_99_b", "Long Noble Boots", [("gg_boots_99_b",0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature ,0, ############ MAIN  ############
    450,  weight(1.25)| abundance(100) | head_armor(0) | body_armor(0) | leg_armor(15) | difficulty(0), imodbits_cloth, [m_stirrups_item_trigger]],
    ["gg_boots_99_a", "Long Red Noble Boots", [("gg_boots_99_a",0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature ,0, ############ MAIN  ############
    10,  weight(1.25)| abundance(100) | head_armor(0) | body_armor(0) | leg_armor(15) | difficulty(0), imodbits_cloth, [m_stirrups_item_trigger]],  

   ["gg_turk_shoes", "Turk_shoes", [("gg_turk_shoes",0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature ,0, 
    160, weight(0.75)|abundance(100)|leg_armor(12), imodbits_cloth, []],

   ["gg_raylin_cav_boots_black", "Black Cavalry Boots", [("gg_raylin_cav_boots_black",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0,  ############ MAIN  ############
    800 , weight(1.75)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(18)|difficulty(0) ,imodbits_armor ],
   ["gg_raylin_cav_boots_brown", "Brown Cavalry Boots", [("gg_raylin_cav_boots_brown",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0, ############ EXTRA  ############
    100 , weight(1.75)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(18)|difficulty(0) ,imodbits_armor ],
   ["gg_rus_cav_boots", "Red Infantry Boots", [("gg_rus_cav_boots",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0,   ############ EXTRA  ############
    100,  weight(1.75)| abundance(100) | head_armor(0) | body_armor(0) | leg_armor(18) | difficulty(0), imodbits_cloth, [m_stirrups_item_trigger]],
   ["gg_rus_cav_boots_2", "Brown Infantry Boots", [("gg_rus_cav_boots_2",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0,  ############ EXTRA  ############
    100,  weight(1.75)| abundance(100) | head_armor(0) | body_armor(0) | leg_armor(18) | difficulty(0), imodbits_cloth, [m_stirrups_item_trigger]], 

   ["gg_black_boots", "Leather Black Boots", [("gg_black_boots",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0,  
    700 , weight(1.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(17)|difficulty(0) ,imodbits_armor ],
   ["gg_red_boots", "Vanguard Red Boots", [("gg_red_boots",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0,  
    750 , weight(1.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(17)|difficulty(0) ,imodbits_armor ],
   ["gg_splinted_greaves_a", "Splinted Boots", [("gg_splinted_greaves_a",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0,  
    1200, weight(3)| abundance(100) | head_armor(0) | body_armor(0) | leg_armor(23) | difficulty(9), imodbits_armor, [m_stirrups_item_trigger]],
   ["gg_rus_splint_greaves", "Rus Splinted Boots", [("gg_rus_splint_greaves",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0,  
    2150, weight(3.7) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(26) | difficulty(15), imodbits_armor, [m_stirrups_item_trigger]],
   ["gg_mail_chausses_a", "Mail Chausses", [("gg_mail_chausses_a",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0,  
    1500, weight(3.0) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(23) | difficulty(9), imodbits_armor, [m_stirrups_item_trigger]],
   ["gg_boot16", "Staufen Chausses", [("gg_boot16",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0,  
    1700 , weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(23)|difficulty(9) ,imodbits_armor ],
   ["gg_leather_greaves_a", "Splinted Greaves", [("gg_leather_greaves_a",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0,  
    3200, weight(3.5) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(26) | difficulty(15), imodbits_armor, [m_stirrups_item_trigger]], 
   ["gg_boot11", "Mail Splinted Boots with Leather", [("gg_boot11",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0,  
    3300 , weight(3.7)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(26)|difficulty(15) ,imodbits_armor ], 
   ["gg_shynbaulds", "Shynbaulds", [("gg_shynbaulds",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0,  
    4450, weight(4.5) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(29) | difficulty(21), imodbits_plate, [m_stirrups_item_trigger]],
   ["gg_shynbaulds_black", "Black Shynbaulds", [("gg_shynbaulds_black",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0,  
    4450, weight(4.5) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(29) | difficulty(21), imodbits_plate, [m_stirrups_item_trigger]],
   ["gg_mail_boots_a", "Mail Greaves", [("gg_mail_boots_a",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0,  
    3650, weight(4.5) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(29) | difficulty(21), imodbits_armor, [m_stirrups_item_trigger]],
   ["gg_plate_mail_boot", "Plate Mail Boots", [("gg_plate_mail_boot",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0,  
   4100 , weight(4.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(29)|difficulty(21) ,imodbits_plate ],

   ["gg_splinted_greaves_nospurs", "Steel Splinted Greaves", [("gg_splinted_greaves_nospurs",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0,  ############ MAIN  ############
    2500, weight(3.7) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(26) | difficulty(15), imodbits_armor, [m_stirrups_item_trigger]],
   ["gg_splinted_greaves_spurs", "Steel Splinted Greaves with Spurs", [("gg_splinted_greaves_spurs",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0,  ############ EXTRA  ############
    100, weight(3.7) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(26) | difficulty(15), imodbits_armor, [m_stirrups_item_trigger]],

   ["gg_narf_steel_shoes2", "Steel Plate with Shoes", [("gg_narf_steel_shoes2",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0,  
    4100 , weight(4.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(29)|difficulty(21) ,imodbits_plate ],
   ["gg_steel_greaves_leather", "Steel Plate with Fine Shoes", [("gg_steel_greaves_leather",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0,  
    4200 , weight(4.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(29)|difficulty(21) ,imodbits_plate ],
   ["gg_boot12", "Scale Plate Boots", [("gg_boot12",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0,  
    4100, weight(4.5) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(29) | difficulty(21), imodbits_armor, [m_stirrups_item_trigger]],
   ["gg_plate_boot", "Thick Plated Greaves with Mail", [("gg_plate_boot",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0,  
    4500, weight(5.3) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(34) | difficulty(24), imodbits_armor, [m_stirrups_item_trigger]],

   ["gg_narf_steel_greaves", "Steel Greaves", [("gg_narf_steel_greaves",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0,   ############ MAIN  ############
    5200, weight(4.5) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(29) | difficulty(21), imodbits_plate, [m_stirrups_item_trigger]], 
   ["gg_narf_greaves", "Dark Steel Greaves", [("gg_narf_greaves",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0,  ############ EXTRA  ############
    100, weight(4.5) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(29) | difficulty(21), imodbits_plate, [m_stirrups_item_trigger]], 

   ["gg_iron_greaves_a", "Iron Greaves", [("gg_iron_greaves_a",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0,  
    4100, weight(4.5) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(29) | difficulty(21), imodbits_armor, [m_stirrups_item_trigger]],

   ["gg_boot3", "Fine Steel Plate with Mail", [("gg_boot3",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0,   
    5500, weight(4.5) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(29) | difficulty(21), imodbits_plate, [m_stirrups_item_trigger]], 
   ["gg_steel_greaves", "Masterwork Steel Greaves", [("gg_steel_greaves",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0,   
    4800, weight(5.3) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(34) | difficulty(24), imodbits_plate, [m_stirrups_item_trigger]],

   ["m_plate_boots", "Thick Plate Boots", [("plate_boots", 0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise, 0,
    5000, weight(5.3) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(34) | difficulty(24), imodbits_plate, [m_stirrups_item_trigger]],

################################################ -PK Yeni Eklenenler- #######################################################

 ["sarranid_camel_boots1", "New Sarranid Boots", [("sarranid_camel_boots1",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0,
  780 , weight(1.75)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(18)|difficulty(0) ,imodbits_armor ],
 ["sarranid_camel_boots2", "Reinforced Sarranid Boots", [("sarranid_camel_boots2",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0,
  1000 , weight(1.75)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(18)|difficulty(0) ,imodbits_armor ],      
 ["sarranid_royal_boots", "Royal Sarranid Boots", [("sarranid_royal_boots",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0,
  3400 , weight(3.7)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(26)|difficulty(15) ,imodbits_armor ],  

############################################### GOLD AND GLORY LEG ARMORS END ######################################################################
   ["new_steel_greaves", "Rare Steel Greaves", [("new_steel_greaves", 0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise, 0,
    5000, weight(5.5) | abundance(100) | head_armor(0) | body_armor(0) | leg_armor(34) | difficulty(24), imodbits_plate, [m_stirrups_item_trigger]],



    ["m_feet_end", "Feet End", [("invisible",0)], itp_type_foot_armor, 0, 0 , weight(0)|abundance(0)|head_armor(0)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],

############################################### LEG ARMORS END ######################################################################


    # HAND ARMOR

#     ["m_leather_gloves", "Leather Gloves", [("leather_gloves_L", 0)], itp_type_hand_armor|itp_merchandise, 0,
 #     0,  weight(0.0) | abundance(100) | body_armor(1) | difficulty(0), imodbits_cloth], 
  #   ["m_mail_mittens", "Mail Mittens", [("mail_mittens_L", 0)], itp_type_hand_armor|itp_merchandise, 0,
   #   0,  weight(0.25)| abundance(100) | body_armor(2) | difficulty(6), imodbits_armor],
#
    #
    ##["m_mail_gauntlets", "Mail Gauntlets", [("mail_gauntlets_L", 0)], itp_type_hand_armor|itp_merchandise, 0,
      #0,  weight(0.5) | abundance(100) | body_armor(3) | difficulty(7), imodbits_armor],
#     ["m_lamellar_gauntlets", "Lamellar Gauntlets", [("scale_gauntlets_a_L", 0)], itp_type_hand_armor|itp_merchandise, 0,
#      0, weight(1.0) | abundance(100) | body_armor(4) | difficulty(9), imodbits_armor], 
#     ["m_scale_gauntlets", "Scale Gauntlets", [("scale_gauntlets_b_L", 0)], itp_type_hand_armor|itp_merchandise, 0,
#      0, weight(1.5) | abundance(100) | body_armor(5) | difficulty(12), imodbits_armor],
#     ["m_plate_mittens", "Plate Mittens", [("plate_mittens_L", 0)], itp_type_hand_armor|itp_merchandise, 0,
#      0, weight(2.0) | abundance(100) | body_armor(6) | difficulty(15), imodbits_armor], 
#     ["m_steel_gauntlets", "Plate Gauntlets", [("hourglass_gauntlets_L", 0)], itp_type_hand_armor|itp_merchandise, 0,
#      0, weight(2.0) | abundance(100) | body_armor(6) | difficulty(15), imodbits_armor],
#     ["m_gauntlets", "Thick Gauntlets", [("gauntlets_L", 0), ("gauntlets_L", imodbit_reinforced)], itp_type_hand_armor|itp_merchandise, 0,
##      0, weight(2.0) | abundance(100) | body_armor(6) | difficulty(15), imodbits_armor],
#     ["m_full_glove1_L", "Gothic Gloves", [("full_glove1_L", 0)], itp_type_hand_armor|itp_merchandise, 0,
#      0, weight(2.0) | abundance(100) | body_armor(6) | difficulty(15), imodbits_armor],
#     ["m_golden_fists", "Golden Fists", [("hourglass_gauntlets_ornate_L", 0)], itp_type_hand_armor|itp_merchandise, 0,
#      0,weight(2.0) | abundance(100) | body_armor(6) | difficulty(15), imodbits_armor], 






########################################## GG MOD GAUNTLETS ###########################################################

  ["gg_leather_gloves","Leather Gloves", [("gg_leather_gloves_L",0)], itp_merchandise|itp_type_hand_armor,0,  ############ MAIN  ############
   150, weight(0.25)|abundance(120)|body_armor(1)|difficulty(0),imodbits_cloth],
  ["gg_black_leather_gloves","Black Leather Gloves", [("gg_black_leather_gloves_L",0)], itp_merchandise|itp_type_hand_armor,0, ############ EXTRA  ############
   10, weight(0.25)|abundance(120)|body_armor(1)|difficulty(0),imodbits_cloth],
  ["gg_ray_leather_gauntlet","Leather Gauntlets", [("gg_ray_leather_gauntlet_L",0)], itp_merchandise|itp_type_hand_armor,0,  ############ EXTRA  ############
   350, weight(0.25)|abundance(120)|body_armor(1)|difficulty(0),imodbits_cloth],
  ["gg_ray_blk_leather_gauntlet","Black Leather Gauntlets", [("gg_ray_blk_leather_gauntlet_L",0)], itp_merchandise|itp_type_hand_armor,0, ############ EXTRA  ############
   350, weight(0.25)|abundance(120)|body_armor(1)|difficulty(0),imodbits_cloth],

  ["gg_mail_mittens","Mail Mittens", [("gg_mail_mittens_L",0)], itp_merchandise|itp_type_hand_armor,0,
   900, weight(0.70)|abundance(100)|body_armor(2)|difficulty(5),imodbits_armor],
  ["gg_mail_gauntlets","Mail Gauntlets", [("gg_mail_gauntlets_L",0)], itp_merchandise|itp_type_hand_armor,0,
   1000, weight(0.70)|abundance(100)|body_armor(2)|difficulty(5),imodbits_armor],

  ["gg_scale_gauntlets","Scale Gauntlets", [("gg_scale_gauntlets_b_L",0)], itp_merchandise|itp_type_hand_armor,0,
   2500, weight(1)|abundance(100)|body_armor(3)|difficulty(5),imodbits_armor],
  ["gg_lamellar_gauntlets","Lamellar Gauntlets", [("gg_lamellar_gauntlets_a_L",0)], itp_merchandise|itp_type_hand_armor,0,
   2400, weight(1)|abundance(100)|body_armor(3)|difficulty(5),imodbits_armor],
  ["gg_glove5","Brown Scale Gauntlets", [("gg_glove5_L",0)], itp_merchandise|itp_type_hand_armor,0,
   2600, weight(1)|abundance(100)|body_armor(3)|difficulty(5),imodbits_armor],
  ["gg_wisby_gauntlets_black","Black Steel Gloves", [("gg_wisby_gauntlets_black_L",0)], itp_merchandise|itp_type_hand_armor,0,
   2800, weight(1)|abundance(100)|body_armor(3)|difficulty(5),imodbits_armor],


  ["gauntlets_arabs_a", "Sarranid Scale Gauntlets", [("gauntlets_arabs_a_L", 0)], itp_merchandise|itp_type_hand_armor,0,
   3300, weight(1.5) | abundance(100) | body_armor(4) | difficulty(12), imodbits_armor],
  ["gauntlets_arabs_b", "Sarranid Royal Scale Gauntlets", [("gauntlets_arabs_b_L", 0)], itp_merchandise|itp_type_hand_armor,0,
   3600, weight(1.5) | abundance(100) | body_armor(4) | difficulty(12), imodbits_armor],


  ["gg_dark_demi_gauntlets","Dark Demi Gauntlets", [("gg_dark_demi_gauntlets_L",0)], itp_merchandise|itp_type_hand_armor,0, ############ MAIN  ############
   3100, weight(1.5)|abundance(100)|body_armor(4)|difficulty(12),imodbits_plate],
  ["gg_shiny_demi_gauntlets","White Demi Gauntlets", [("gg_shiny_demi_gauntlets_L",0)], itp_merchandise|itp_type_hand_armor,0, ############ EXTRA  ############
   100, weight(1.5)|abundance(100)|body_armor(4)|difficulty(12),imodbits_plate],
  ["gg_black_demi_gauntlets","Black Demi Gauntlets", [("gg_black_demi_gauntlets_L",0)], itp_merchandise|itp_type_hand_armor,0, ############ EXTRA  ############
   100, weight(1.5)|abundance(100)|body_armor(4)|difficulty(12),imodbits_plate],
  ["gg_dark_finger_gauntlets","Dark Finger Gauntlets", [("gg_dark_finger_gauntlets_L",0)], itp_merchandise|itp_type_hand_armor,0, ############ EXTRA  ############
   600, weight(2)|abundance(100)|body_armor(4)|difficulty(15),imodbits_plate],
  ["gg_shiny_finger_gauntlets","White Finger Gauntlets", [("gg_shiny_finger_gauntlets_L",0)], itp_merchandise|itp_type_hand_armor,0, ############ EXTRA  ############
   600, weight(2)|abundance(100)|body_armor(4)|difficulty(15),imodbits_plate],
  ["gg_black_gauntlets_black","Black Finger Gauntlets", [("gg_black_gauntlets_black_L",0)], itp_merchandise|itp_type_hand_armor,0, ############ EXTRA  ############
   600, weight(2)|abundance(100)|body_armor(4)|difficulty(15),imodbits_plate],


  ["gg_wisby_gauntlets_brown","Wisby Gauntlets", [("gg_wisby_gauntlets_brown_L",0)], itp_merchandise|itp_type_hand_armor,0,  ############ MAIN  ############
   3500, weight(1.5)|abundance(100)|body_armor(4)|difficulty(12),imodbits_plate],
  ["gg_wisby_gauntlets_yellow","Yellow Wisby Gauntlets", [("gg_wisby_gauntlets_yellow_L",0)], itp_merchandise|itp_type_hand_armor,0, ############ EXTRA  ############
   100, weight(1.5)|abundance(100)|body_armor(4)|difficulty(12),imodbits_plate],
  ["gg_wisby_gauntlets_green","Green Wisby Gauntlets", [("gg_wisby_gauntlets_green_L",0)], itp_merchandise|itp_type_hand_armor,0, ############ EXTRA  ############
   100, weight(1.5)|abundance(100)|body_armor(4)|difficulty(12),imodbits_plate],
  ["gg_wisby_gauntlets_blue","Blue Wisby Gauntlets", [("gg_wisby_gauntlets_blue_L",0)], itp_merchandise|itp_type_hand_armor,0, ############ EXTRA  ############
   100, weight(1.5)|abundance(100)|body_armor(4)|difficulty(12),imodbits_plate],
  ["gg_wisby_gauntlets_white","White Wisby Gauntlets", [("gg_wisby_gauntlets_white_L",0)], itp_merchandise|itp_type_hand_armor,0, ############ EXTRA  ############
   100, weight(1.5)|abundance(100)|body_armor(4)|difficulty(12),imodbits_plate],
  ["gg_wisby_gauntlets_red","Red Wisby Gauntlets", [("gg_wisby_gauntlets_red_L",0)], itp_merchandise|itp_type_hand_armor,0, ############ EXTRA  ############
   100, weight(1.5)|abundance(100)|body_armor(4)|difficulty(12),imodbits_plate],

  ["gg_steel_mittens","Steel Mittens", [("gg_steel_mittens_L",0)], itp_merchandise|itp_type_hand_armor,0,
   3900, weight(2)|abundance(100)|body_armor(5)|difficulty(15),imodbits_plate],
  ["gg_black_mitty","Black Steel Mittens", [("gg_black_mitty_L",0)], itp_merchandise|itp_type_hand_armor,0,
   3950, weight(2)|abundance(100)|body_armor(5)|difficulty(15),imodbits_plate],

  ["gg_steel_gauntlets_L","Mercenary Steel Gauntlets", [("gg_steel_gauntlets_L",0)], itp_merchandise|itp_type_hand_armor,0,
   4000, weight(2)|abundance(100)|body_armor(5)|difficulty(15),imodbits_plate],

  ["gg_hourglass_gauntlets","Steel Hourglass Gauntlets", [("gg_hourglass_gauntlets_L",0)], itp_merchandise|itp_type_hand_armor,0,
   4200, weight(2)|abundance(100)|body_armor(5)|difficulty(15),imodbits_plate],

  ["gg_hourglass_gauntlets_ornate_white","Reinforced Hourglass White Gauntlets", [("gg_hourglass_gauntlets_ornate_white_L",0)], itp_merchandise|itp_type_hand_armor,0,
   4800, weight(2)|abundance(100)|body_armor(5)|difficulty(15),imodbits_plate],

  ["gg_shiny_knighty_glove","Knightly Steel Gauntlets", [("gg_shiny_knighty_glove_L",0)], itp_merchandise|itp_type_hand_armor,0, ############ MAIN  ############
   5000, weight(2)|abundance(100)|body_armor(5)|difficulty(15),imodbits_plate],
  ["gg_black_knightly","Black Knightly Steel Gauntlets", [("gg_black_knightly_L",0)], itp_merchandise|itp_type_hand_armor,0, ############ EXTRA  ############
   100, weight(2)|abundance(100)|body_armor(5)|difficulty(15),imodbits_plate],


  ["gg_gauntlets","Gauntlets", [("gg_gauntlets_L",0)], itp_merchandise|itp_type_hand_armor,0,
   5200, weight(2)|abundance(100)|body_armor(5)|difficulty(15),imodbits_plate],

  # ["gg_gold_hourglass_gauntlets_ornate","Reinforced Hourglass Golden Gauntlets", [("gg_gold_hourglass_gauntlets_ornate_L",0)], itp_merchandise|itp_type_hand_armor,0,
   # 32000, weight(2.0)|abundance(100)|body_armor(10)|difficulty(21),imodbits_plate],
  ["m_golden_fists", "Golden Fists", [("hourglass_gauntlets_ornate_L", 0)], itp_type_hand_armor|itp_merchandise, 0,
   62500,weight(2) | abundance(100) | body_armor(5) | difficulty(15), imodbits_armor], 

# NESSA gloves
  ["new_hourglass_gauntlets", "Ornamented Golden Fists", [("new_hourglass_gauntlets_L", 0)], itp_type_hand_armor|itp_merchandise, 0,
   70000,weight(2) | abundance(100) | body_armor(5) | difficulty(15), imodbits_armor], 
  ["new_hourglass_gauntlets_with_plate", "Sugarloaf Golden Fists", [("new_hourglass_gauntlets_L", 0)], itp_type_hand_armor|itp_merchandise, 0,
   0,weight(2) | abundance(100) | body_armor(5) | difficulty(15), imodbits_armor], 
  ["gloves_king", "Gulam Gloves", [("gloves_king_L", 0)], itp_type_hand_armor|itp_merchandise, 0,
   2900,weight(1) | abundance(100) | body_armor(3) | difficulty(5), imodbits_armor], 




############################################### GOLD AND GLORY HAND ARMOR END ######################################################################

    ["m_glove_end", "Glove End", [("invisible",0)], itp_type_hand_armor, 0, 0 , weight(0)|abundance(0)|head_armor(0)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
    

############################################### HAND ARMOR END ######################################################################



    # HORSES

    ["m_sumpter_horse", "Sumpter Horse", [("sumpter_horse", 0)], itp_type_horse|itp_merchandise, 0,
     3300,  abundance(90) | hit_points(120) | body_armor(15) | difficulty(1) | horse_speed(42) | horse_maneuver(43) | horse_charge(12) | horse_scale(99), imodbits_horse_basic ], 
    ["m_steppe_horse", "Steppe Horse", [("steppe_horse", 0)], itp_type_horse|itp_merchandise, 0,
     6400,  abundance(80) | hit_points(120) | body_armor(18) | difficulty(2) | horse_speed(44) | horse_maneuver(46) | horse_charge(14) | horse_scale(98),  imodbits_horse_basic ], 
    ["m_saddle_horse", "Saddle Horse", [("saddle_horse", 0)], itp_type_horse|itp_merchandise, 0,
     7800,  abundance(90) | hit_points(120) | body_armor(20) | difficulty(2) | horse_speed(45) | horse_maneuver(44) | horse_charge(18) | horse_scale(104), imodbits_horse_basic ], 
    ["m_saddle_horse_2", "Dark Bay Saddle Horse", [("cwe_european_horse_a", 0)], itp_type_horse|itp_merchandise, 0,
     8300,  abundance(90) | hit_points(120) | body_armor(20) | difficulty(2) | horse_speed(45) | horse_maneuver(45) | horse_charge(18) | horse_scale(104), imodbits_horse_basic ],
    ["m_arabian_horse_a", "Desert Horse", [("arabian_horse_a", 0)], itp_type_horse|itp_merchandise, 0,
     9100,  abundance(70) | hit_points(115) | body_armor(15) | difficulty(3) | horse_speed(45) | horse_maneuver(48) | horse_charge(14) | horse_scale(100), imodbits_horse_basic ], 
    ["m_arabian_horse_b", "Sarranid Horse", [("arabian_horse_b", 0)], itp_type_horse|itp_merchandise, 0,
     9200,  abundance(70) | hit_points(115) | body_armor(13) | difficulty(3) | horse_speed(46) | horse_maneuver(47) | horse_charge(15) | horse_scale(100), imodbits_horse_basic ],
    ["m_courser", "Courser", [("courser", 0)], itp_type_horse|itp_merchandise, 0,
     10300, abundance(70) | hit_points(120) | body_armor(15) | difficulty(3) | horse_speed(47) | horse_maneuver(45) | horse_charge(14) | horse_scale(106), imodbits_horse_basic ],  ############ MAIN  ############
    ["m_courser_green", "Courser with Green Saddle", [("m_courser_green", 0)], itp_type_horse, 0,
     150, abundance(70) | hit_points(115) | body_armor(14) | difficulty(3) | horse_speed(48) | horse_maneuver(45) | horse_charge(14) | horse_scale(106), imodbits_horse_basic ],  ############ EXTRA  ############
    ["m_hunter", "Hunter", [("hunting_horse", 0)], itp_type_horse|itp_merchandise, 0,
     11000, abundance(60) | hit_points(130) | body_armor(25) | difficulty(3) | horse_speed(43) | horse_maneuver(44) | horse_charge(24) | horse_scale(108), imodbits_horse_basic ],
    ["m_caparisoned_horse_1", "Horse with Black Caparison", [("cwe_knight_horse_2", 0)], itp_type_horse|itp_merchandise, 0,
     11700, abundance(50) | hit_points(130) | body_armor(27)| difficulty(4) | horse_speed(43) | horse_maneuver(43) | horse_charge(25) | horse_scale(110), imodbits_horse_basic ],
    ["m_barded_horse", "Barded Horse", [("zimke_romeian_barded_warhorse", 0)], itp_type_horse|itp_merchandise, 0,
     13500, abundance(50) | hit_points(135) | body_armor(27) | difficulty(4) | horse_speed(42) | horse_maneuver(43) | horse_charge(27) | horse_scale(110), imodbits_horse_basic ],

    ["m_warhorse", "Mailed Hunter", [("warhorse", 0)], itp_type_horse|itp_merchandise, 0,  ### MAIN
     15000, abundance(50) | hit_points(130) | body_armor(30) | difficulty(4) | horse_speed(42) | horse_maneuver(43) | horse_charge(27) | horse_scale(110), imodbits_horse_basic ],
    ["gg_warhorse_dark_mail", "Dark Mailed Hunter", [("gg_warhorse_dark_mail", 0)], itp_type_horse|itp_merchandise, 0,  ### EXTRA
     200, abundance(50) | hit_points(130) | body_armor(30) | difficulty(4) | horse_speed(42) | horse_maneuver(43) | horse_charge(27) | horse_scale(110), imodbits_horse_basic ],


    ### ["m_ibelin_knight_horse_a", "Noble Hunter", [("ibelin_knight_horse_a", 0)], itp_type_horse|itp_merchandise, 0,
 ###   16000, abundance(50) | hit_points(125) | body_armor(34) | difficulty(4) | horse_speed(42) | horse_maneuver(41) | horse_charge(26) | horse_scale(110), imodbits_horse_basic ], #user Commander

    ["m_warhorse_heavy", "Heavy War Horse", [("warhorse_chain", 0)], itp_type_horse|itp_merchandise, 0,
     18000, abundance(50) | hit_points(140) | body_armor(33) | difficulty(4) | horse_speed(40) | horse_maneuver(41) | horse_charge(30) | horse_scale(110), imodbits_horse_basic ],

    ["m_warhorse_steppe", "Steppe Charger", [("warhorse_steppe", 0)], itp_type_horse|itp_merchandise, 0, ### MAIN
     21000, abundance(40) | hit_points(145) | body_armor(37) | difficulty(5) | horse_speed(40) | horse_maneuver(39) | horse_charge(32) | horse_scale(112), imodbits_horse_basic ],
    ["gg_grey_steppe_warhorse", "Grey Steppe Charger", [("gg_grey_steppe_warhorse", 0)], itp_type_horse|itp_merchandise, 0,  ### EXTRA
     200, abundance(40) | hit_points(145) | body_armor(37) | difficulty(5) | horse_speed(40) | horse_maneuver(39) | horse_charge(32) | horse_scale(112), imodbits_horse_basic ],


    ["m_charger", "Charger", [("charger_new", 0)], itp_type_horse|itp_merchandise, 0,  ### MAIN
     25000, abundance(40) | hit_points(145) | body_armor(42) | difficulty(5) | horse_speed(39) | horse_maneuver(38) | horse_charge(34) | horse_scale(112), imodbits_horse_basic ], 
    ["gg_heavy_strong_black_charger", "Black Charger", [("gg_heavy_strong_black_charger", 0)], itp_type_horse|itp_merchandise, 0, ### EXTRA
     200, abundance(40) | hit_points(145) | body_armor(42) | difficulty(5) | horse_speed(39) | horse_maneuver(38) | horse_charge(34) | horse_scale(112), imodbits_horse_basic ], 
    ["m_warhorse_sarranid", "Sarranian War Horse", [("warhorse_sarranid", 0)], itp_type_horse|itp_merchandise, 0,
     28000, abundance(40) | hit_points(150) | body_armor(48) | difficulty(6) | horse_speed(37) | horse_maneuver(37) | horse_charge(38) | horse_scale(112), imodbits_horse_basic ],

    ["m_sarranid_caparisoned_horse_2", "Sarranid Caparisoned Horse", [("cwe_saracen_hard_horses_c", 0)], itp_type_horse|itp_merchandise, 0,
    12100, abundance(50) | hit_points(130) | body_armor(26)| difficulty(4) | horse_speed(43) | horse_maneuver(43) | horse_charge(25) | horse_scale(110), imodbits_horse_basic ],
    ["m_sarranid_caparisoned_horse_3", "Sarranid Caparisoned Horse", [("cwe_saracen_hard_horses_d", 0)], itp_type_horse|itp_merchandise, 0,
    12300, abundance(50) | hit_points(130) | body_armor(26)| difficulty(4) | horse_speed(43) | horse_maneuver(43) | horse_charge(25) | horse_scale(110), imodbits_horse_basic ],
    ["m_sarranid_caparisoned_horse_1", "Sarranid Caparisoned Horse", [("cwe_saracen_hard_horses_a", 0)], itp_type_horse|itp_merchandise, 0,
    12500, abundance(50) | hit_points(130) | body_armor(26)| difficulty(4) | horse_speed(43) | horse_maneuver(43) | horse_charge(25) | horse_scale(110), imodbits_horse_basic ],

    ["jerusalem_king_horse", "Holy Hunter", [("jerusalem_king_horse", 0)], itp_type_horse, 0, ### JERU
     140000,abundance(50) | hit_points(135) | body_armor(25) | difficulty(4) | horse_speed(43) | horse_maneuver(43) | horse_charge(24) | horse_scale(110), imodbits_horse_basic ],
    ["saracen_horse_sultan", "Sultan Horse", [("saracen_horse_sultan", 0)], itp_type_horse, 0, ### SULTAN
     140000,abundance(50) | hit_points(135) | body_armor(25) | difficulty(4) | horse_speed(43) | horse_maneuver(43) | horse_charge(24) | horse_scale(110), imodbits_horse_basic ],
    ["saracin_hard_horses_d", "Sultan Saracen Horse", [("saracin_hard_horses_d", 0)], itp_type_horse, 0, ### SULTAN EXTRA
     2500,abundance(50) | hit_points(135) | body_armor(25) | difficulty(4) | horse_speed(43) | horse_maneuver(43) | horse_charge(24) | horse_scale(110), imodbits_horse_basic ],
    ["m_noble_hunter_no_mask", "Noble Hunter", [("horse_2_black_yellow_barded", 0)], itp_type_horse, 0, ### MAIN
     150000,abundance(50) | hit_points(135) | body_armor(25) | difficulty(4) | horse_speed(43) | horse_maneuver(43) | horse_charge(24) | horse_scale(110), imodbits_horse_basic ],
    ["m_noble_hunter_armored", "Armoured Noble Hunter", [("horse_2_black_yellow_barded_masked", 0)], itp_type_horse|itp_merchandise, 0, ### EXTRA
     4500,abundance(50) | hit_points(135) | body_armor(25) | difficulty(4) | horse_speed(43) | horse_maneuver(43) | horse_charge(24) | horse_scale(110), imodbits_horse_basic ],
    ["m_noble_hunter_armored_white", "White Armoured Noble Hunter", [("horse_2_white_yellow_barded_masked", 0)], itp_type_horse|itp_merchandise, 0, ### EXTRA
     4500,abundance(50) | hit_points(135) | body_armor(25) | difficulty(4) | horse_speed(43) | horse_maneuver(43) | horse_charge(24) | horse_scale(110), imodbits_horse_basic ],
    ["m_noble_hunter_no_mask_white", "White Noble Hunter", [("horse_2_white_yellow_barded", 0)], itp_type_horse, 0, ### EXTRA
     1500,abundance(50) | hit_points(135) | body_armor(25) | difficulty(4) | horse_speed(43) | horse_maneuver(43) | horse_charge(24) | horse_scale(110), imodbits_horse_basic ],
    ["vaegir_knight_horse", "Noble Hunter with Purple Armor", [("vaegir_knight_horse", 0)], itp_type_horse, 0, ### MAIN
     1500,abundance(50) | hit_points(135) | body_armor(25) | difficulty(4) | horse_speed(43) | horse_maneuver(43) | horse_charge(24) | horse_scale(110), imodbits_horse_basic ],
    ["rus_horse", "Rus Hunter", [("rus_horse", 0)], itp_type_horse|itp_merchandise, 0,
     11500, abundance(60) | hit_points(130) | body_armor(25) | difficulty(3) | horse_speed(43) | horse_maneuver(44) | horse_charge(24) | horse_scale(108), imodbits_horse_basic ],
    ["WCourserMealyBay", "Courser Mealy Bay", [("WCourserMealyBay", 0)], itp_type_horse|itp_merchandise, 0,
     60000, abundance(70) | hit_points(120) | body_armor(15) | difficulty(3) | horse_speed(47) | horse_maneuver(45) | horse_charge(14) | horse_scale(106), imodbits_horse_basic ],
    ["WArabBlack", "Sarranid Black Horse", [("WArabBlack", 0)], itp_type_horse|itp_merchandise, 0,
     9400,  abundance(70) | hit_points(115) | body_armor(15) | difficulty(3) | horse_speed(45) | horse_maneuver(48) | horse_charge(14) | horse_scale(100), imodbits_horse_basic ],
    ["WArabGrey", "Sarranid Silver Horse", [("WArabGrey", 0)], itp_type_horse|itp_merchandise, 0,
     9500,  abundance(70) | hit_points(115) | body_armor(13) | difficulty(3) | horse_speed(46) | horse_maneuver(47) | horse_charge(15) | horse_scale(100), imodbits_horse_basic ],
##    ["m_noble_hunter", "Noble Hunter", [("m_heraldic_warhorse_1", 0)], itp_type_horse, 0, ### MAIN
##     150000,abundance(50) | hit_points(125) | body_armor(30) | difficulty(4) | horse_speed(43) | horse_maneuver(42) | horse_charge(24) | horse_scale(110), imodbits_horse_basic ],

    ["m_heraldic_caparisoned_horse_default", "Horse with Heraldic Caparison", [("horse_heraldic_1_m_banner_4_12", 0)], itp_type_horse|itp_merchandise, 0,
     165000, abundance(60) | hit_points(130) | body_armor(28) | difficulty(4) | horse_speed(43) | horse_maneuver(43) | horse_charge(24) | horse_scale(108), imodbits_horse_basic ],

] + [elem for sublist in [[
    ["m_heraldic_caparisoned_horse_{}".format(merc_banner[0]), "Horse with Heraldic Caparison", [("horse_heraldic_1_{}".format(merc_banner[2]), 0)], itp_type_horse|itp_merchandise, 0,
     0, abundance(60) | hit_points(125) | body_armor(29) | difficulty(4) | horse_speed(43) | horse_maneuver(43) | horse_charge(23) | horse_scale(108), imodbits_horse_basic ],
] for merc_banner in native_banner_meshes + mercenaries_banner_meshes + mercenaries_clan_banner_meshes + native_banner_kingdom_meshes] for elem in sublist] + [

    ["m_horse_end", "Horse End", [("invisible",0)], itp_type_horse, 0, 0 , weight(0)|abundance(0)|head_armor(0)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
    

############################################### HORSE END ######################################################################

    ["m_all_items_end", "All Items End", [("invisible",0)], itp_no_pick_up_from_ground, 0, 0 , weight(0)|abundance(0)|head_armor(0)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
    
############################################### ALL ITEMS ENDS ######################################################################



    # SPECIAL ITEMS
	
	
	["m_small_chest","Chest with Gold", [("m_small_chest", 0),("m_small_chest_carry", ixmesh_carry),("m_small_chest", ixmesh_inventory)], itp_type_thrown|itp_primary, itcf_carry_dagger_front_right, 100, weight(2) | difficulty(0) | spd_rtng(98) | shoot_speed(22) | max_ammo(10) | thrust_damage(1, pierce) | weapon_length(40), imodbits_thrown ],
##	["m_lostik_horn", "Lostik Horn", [("lostik_horn", 0), ("lostik_horn_carry", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_wooden_parry, itcf_carry_mace_left_hip,    10000, weight(1.0) | difficulty(0) | spd_rtng(0) | weapon_length(25) | swing_damage(0, cut) | thrust_damage(0, pierce), imodbits_axe ], #user 4EJIOBE4EK
    ["m_ballista_tools", "Ballista Construction Tools", [("m_ballista_tool",0)], itp_type_polearm|itp_cant_use_on_horseback|itp_primary|itp_wooden_parry|itp_two_handed, 0, 200, weight(5.0) | difficulty(0) | spd_rtng(95) | weapon_length(116) | swing_damage(0, blunt) | thrust_damage(0, pierce), imodbits_polearm ],
    ["m_ballista", "Ballista", [("crossbow_c", 0)], itp_type_crossbow|itp_primary|itp_two_handed|itp_can_penetrate_shield|itp_can_knock_down, itcf_shoot_crossbow, 0, weight(5.0) | difficulty(0) | spd_rtng(50) | shoot_speed(48) | thrust_damage(120, pierce) | accuracy(99) | max_ammo(1), imodbits_crossbow ], 
    ["m_ballista_bolts", "Ballista Bolt", [("m_ballista_bolt", 0)], itp_type_thrown|itp_primary|itp_can_penetrate_shield|itp_cant_use_on_horseback, 0, 950, weight(2.0) | difficulty(0) | spd_rtng(98) | shoot_speed(22) | thrust_damage(1, pierce) | max_ammo(8) | weapon_length(40), imodbits_thrown, [m_ballista_bolt_hit_trigger] ], 
	["m_catapult", "Catapult", [("crossbow_c", 0)], itp_type_crossbow|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_can_knock_down, itcf_shoot_crossbow, 0, weight(5.0) | difficulty(0) | spd_rtng(50) | shoot_speed(50) | thrust_damage(120, blunt)  | accuracy(99) | max_ammo(1), imodbits_crossbow ],
	["m_catapult_stone_balls","Stone Ball", [("m_catapult_missile", 0), ("m_catapult_missile", ixmesh_flying_ammo)], itp_type_thrown|itp_primary|itp_bonus_against_shield|itp_cant_use_on_horseback|itp_can_knock_down, itcf_throw_stone, 100, weight(3) | difficulty(0) | spd_rtng(98) | shoot_speed(22) | max_ammo(10) | thrust_damage(1, blunt) | weapon_length(24), imodbits_thrown, [m_catapult_missile_hit_trigger] ], 
	["m_invisible_head", "Headless", [("invisible",0)], itp_type_head_armor|itp_covers_head   ,0, 0 , weight(0)|abundance(0)|head_armor(0)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
	["m_invisible_legs", "Legsless", [("invisible",0)], itp_type_foot_armor|itp_attach_armature   ,0, 0 , weight(0)|abundance(0)|head_armor(0)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
	["m_invisible_hands", "Handsless", [("invisible",0)], itp_type_hand_armor   ,0, 0 , weight(0)|abundance(0)|head_armor(0)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
	["m_invisible_left_hand", "Left Handsless", [("invisible",0)], itp_type_hand_armor|itp_force_show_right_hand   ,0, 0 , weight(0)|abundance(0)|head_armor(0)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
	["m_invisible_right_hand", "Right Handsless", [("invisible",0)], itp_type_hand_armor|itp_force_show_left_hand   ,0, 0 , weight(0)|abundance(0)|head_armor(0)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
	["m_invisible_body", "Bodyless", [("invisible",0)], itp_covers_legs|itp_type_body_armor   ,0, 0 , weight(0)|abundance(0)|head_armor(0)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
	["m_water_gun", "Water Gun", [("gg_handgonne_a",0)], itp_type_musket |itp_primary|itp_two_handed|custom_kill_info(4),itcf_shoot_musket|itcf_carry_spear, 0 , weight(3.0)|difficulty(0)|spd_rtng(150) | shoot_speed(200) | thrust_damage(200 ,pierce)|max_ammo(1000)|accuracy(99),imodbits_none],
	["m_blood_gun", "Blood Gun", [("gg_handgonne_a",0)], itp_type_musket |itp_primary|itp_two_handed|custom_kill_info(1),itcf_shoot_musket|itcf_carry_spear, 0 , weight(3.0)|difficulty(0)|spd_rtng(150) | shoot_speed(200) | thrust_damage(200 ,pierce)|max_ammo(1000)|accuracy(99),imodbits_none],
	["m_lightning_gun", "Lightning Gun", [("gg_handgonne_a",0)], itp_type_musket |itp_primary|itp_two_handed|custom_kill_info(5),itcf_shoot_musket|itcf_carry_spear, 0 , weight(3.0)|difficulty(0)|spd_rtng(150) | shoot_speed(200) | thrust_damage(200 ,pierce)|max_ammo(1000)|accuracy(99),imodbits_none],
]

count = 0
new_mercenaries_items = list(mercenaries_items)
for index, item in enumerate(mercenaries_items):
  if not item[0] in starter_items:
    continue
  new_item = list(item)
  new_item[5] = 0
  new_item[0] = new_item[0] + "_free"
  count += 1
  new_mercenaries_items.insert(index + count, new_item)

mercenaries_items = new_mercenaries_items




