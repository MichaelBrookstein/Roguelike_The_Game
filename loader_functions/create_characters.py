import tcod as libtcod
from components.fighter import Fighter
from components.inventory import Inventory
from components.abilities import Abilities
from components.equippable import Equippable
from components.feat import Feat
from components.info import Information
from equipment_slots import EquipmentSlots
from game_functions.ability_functions import cast_shadow_vanish_feat, cast_insanity_feat, cast_eldritch_blast_feat
from game_messages import Message
from entity import Entity


def Character(chosen):
    if chosen == "thief":
        name = chosen
        fighter_component = Fighter(hp=80, defense=1, accuracy=110, dodge=20, strength=2, crit_chance=15, ability_power=2)
        inventory_component = Inventory(15)
        abilities_component = Abilities(5)
        info_component = Information('thief')
        starting_equip_info_component = Information('well_used_dagger')
        starting_equip_component = Equippable(EquipmentSlots.MAIN_HAND, strength_bonus=2, crit_chance_bonus=7)
        starting_equip = Entity(0, 0, '-', libtcod.gray, 'Well Used Dagger', equippable=starting_equip_component, info=starting_equip_info_component)
        starting_feats = [Feat(name="Shadow Vanish", cooldown=20, feat_function=cast_shadow_vanish_feat, duration=5)]

    elif chosen == "brute":
        name = chosen
        fighter_component = Fighter(hp=100, defense=2, accuracy=90, dodge=0, strength=4, crit_chance=0, ability_power=0)
        inventory_component = Inventory(10)
        abilities_component = Abilities(5)
        info_component = Information('brute')
        starting_equip_info_component = Information('leather_vest')
        starting_equip_component = Equippable(EquipmentSlots.UPPER_BODY, max_hp_bonus=20)
        starting_equip = Entity(0, 0, 'v', libtcod.Color(107, 45, 0), 'Leather Vest',
                                equippable=starting_equip_component, info=starting_equip_info_component)
        starting_feats =[]

    elif chosen == "occultist":
        name = chosen
        fighter_component = Fighter(hp=90, defense=1, accuracy=100, dodge=10, strength=2, crit_chance=10, ability_power=3)
        inventory_component = Inventory(10)
        abilities_component = Abilities(10)
        info_component = Information('occultist')
        starting_equip_info_component = Information('cursed_manuscript')
        starting_equip_component = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=-1, strength_bonus=-1, dodge_bonus=10, ability_power_bonus=2)
        starting_equip = Entity(0, 0, '#', libtcod.Color(100, 100, 100), 'Cursed Manuscript',
                                equippable=starting_equip_component, info=starting_equip_info_component)
        starting_feats = [Feat(name="Eldritch Blast", cooldown=10, feat_function=cast_eldritch_blast_feat, damage=5, targeting=True, targeting_message=Message(
                        'Left-click an enemy to blast it, or right-click to cancel.', libtcod.light_cyan)),
                          Feat(name="Insanity", cooldown=10, feat_function=cast_insanity_feat, duration=5, targeting=True, targeting_message=Message(
                        'Left-click an enemy to confuse it, or right-click to cancel.', libtcod.light_cyan))]

    return fighter_component, inventory_component, abilities_component, info_component, starting_equip, starting_feats, name
