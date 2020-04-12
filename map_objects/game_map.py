import tcod as libtcod
from random import randint

from game_functions.render_functions import RenderOrder

from components.ai import BasicMonster, AbilityMonster
from components.equipment import EquipmentSlots
from components.equippable import Equippable
from components.fighter import Fighter
from components.item import Item
from components.inventory import Inventory
from components.equipment import Equipment
from components.abilities import Abilities
from components.feat import Feat
from components.info import Information
from map_objects.stairs import Stairs

from entity import Entity
from game_messages import Message
from game_functions.item_functions import cast_confuse, cast_fireball, cast_lightning, heal, add_fireball, \
    add_confusion, add_eldritch_blast, add_lightning
from game_functions.ability_functions import cast_unholy_bolt_feat
from map_objects.rectangle import Rect
from map_objects.tile import Tile

from random_utils import from_dungeon_level, random_choice_from_dict


class GameMap:
    def __init__(self, width, height, dungeon_level=1):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        self.dungeon_level = dungeon_level

    def initialize_tiles(self):
        tiles = [[Tile(x, y, True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities):
        rooms = []
        num_rooms = 0

        center_of_last_room_x = None
        center_of_last_room_y = None

        for r in range(max_rooms):
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)

            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            new_room = Rect(x, y, w, h)

            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                self.create_room(new_room)

                (new_x, new_y) = new_room.center()

                center_of_last_room_x = new_x
                center_of_last_room_y = new_y

                if num_rooms == 0:
                    player.x = new_x
                    player.y = new_y

                else:
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    if randint(0, 1) == 1:
                        self.create_horz_hall(prev_x, new_x, prev_y)
                        self.create_vert_hall(prev_y, new_y, new_x)
                    else:
                        self.create_vert_hall(prev_y, new_y, prev_x)
                        self.create_horz_hall(prev_x, new_x, new_y)

                self.place_entities(new_room, entities)

                rooms.append(new_room)
                num_rooms += 1

        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '<', libtcod.white, 'Stairs',
                             render_order=RenderOrder.STAIRS, stairs=stairs_component)
        entities.append(down_stairs)

    def create_room(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False
                self.tiles[x][y].room = True
                self.tiles[x][y].hall = False


    def create_horz_hall(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if self.tiles[x+1][y].room and self.tiles[x-1][y].hall and \
                    (self.tiles[x][y+1].blocked or self.tiles[x][y-1].blocked):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = True
                self.tiles[x][y].hall = False
                self.tiles[x][y].door = True
            else:
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False
                if not self.tiles[x][y].room:
                    self.tiles[x][y].hall = True


    def create_vert_hall(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if self.tiles[x][y+1].room and self.tiles[x][y-1].hall and \
                    (self.tiles[x+1][y].blocked or self.tiles[x-1][y].blocked):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = True
                self.tiles[x][y].hall = False
                self.tiles[x][y].door = True

            else:
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False
                if not self.tiles[x][y].room:
                    self.tiles[x][y].hall = True


    def place_entities(self, room, entities):
        max_monsters_per_room = from_dungeon_level([[2, 1], [4, 3], [6, 6]], self.dungeon_level)
        max_items_per_room = from_dungeon_level([[1, 1], [2, 4]], self.dungeon_level)

        number_of_monsters = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)


        monster_chances = {
            'risen_corpse': 60,
            'cultist': from_dungeon_level([[10, 2], [40, 4], [60, 6]], self.dungeon_level),
            'unholy_priest': from_dungeon_level([[15, 3], [20, 4], [40, 5], [60, 7]], self.dungeon_level),
            'shadowy_horror': from_dungeon_level([[10, 3], [20, 5], [30, 6]], self.dungeon_level),
        }

        item_chances = {
            'healing_potion': 50,
            'dull_sword': from_dungeon_level([[15, 2]], self.dungeon_level),
            'plain_shirt': from_dungeon_level([[5, 1], [10, 2]], self.dungeon_level),
            'sharpened_sword': from_dungeon_level([[7, 3], [10, 5]], self.dungeon_level),
            'battered_shield': from_dungeon_level([[15, 2]], self.dungeon_level),
            'hardened_shield': from_dungeon_level([[7, 3], [10, 5]], self.dungeon_level),
            'lost_pages': from_dungeon_level([[5, 4], [15, 6]], self.dungeon_level),
            'dirty_spectacles': from_dungeon_level([[1, 1], [3, 2], [7, 4]], self.dungeon_level),
            'rough_trousers': from_dungeon_level([[5, 3], [10, 5]], self.dungeon_level),
            'fine_shoes': from_dungeon_level([[1, 1], [3, 5]], self.dungeon_level),
            'lightning_scroll': from_dungeon_level([[25, 4]], self.dungeon_level),
            'fireball_scroll': from_dungeon_level([[25, 6]], self.dungeon_level),
            'confusion_scroll': from_dungeon_level([[10, 2]], self.dungeon_level),
            'fireball_tome': from_dungeon_level([[5, 3], [10, 5]], self.dungeon_level),
            'confusion_tome': from_dungeon_level([[5, 3], [10, 5]], self.dungeon_level),
            'eldritch_blast_tome': from_dungeon_level([[5, 3], [10, 5]], self.dungeon_level),
            'lightning_blast_tome': from_dungeon_level([[5, 3], [10, 5]], self.dungeon_level)
        }

        for i in range(number_of_monsters):
            # Choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                monster_choice = random_choice_from_dict(monster_chances)

                if monster_choice == 'risen_corpse':
                    zombie_equipment = []
                    zombie_fighter_component = Fighter(hp=15, defense=0, strength=3, accuracy=85, dodge=0, ability_power=0, crit_chance=5, xp=35)
                    ai_component = BasicMonster()
                    enemy_inventory_component = Inventory(5)
                    enemy_equipment_component = Equipment()
                    enemy_info_component = Information('risen_corpse')

                    ragged_shoes_component = Equippable(EquipmentSlots.UPPER_BODY, dodge_bonus=5, accuracy_bonus=5)
                    ragged_shoes_info_component = Information('ragged_shoes')
                    ragged_shoes_entity = Entity(0, 0, 's', libtcod.Color(125, 80, 12), 'Ragged Shoes',
                                            equippable=ragged_shoes_component, info=ragged_shoes_info_component)

                    torn_pants_component = Equippable(EquipmentSlots.LOWER_BODY, max_hp_bonus=10)
                    torn_pants_info_component = Information('torn_pants')
                    torn_pants_entity = Entity(0, 0, 'p', libtcod.Color(143, 73, 7), 'Torn Pants',
                                            equippable=torn_pants_component, info=torn_pants_info_component)

                    mystic_hood_component = Equippable(EquipmentSlots.HEAD, ability_power_bonus=1)
                    mystic_hood_info_component = Information('mystic_hood')
                    mystic_hood_entity = Entity(0, 0, '^', libtcod.Color(159, 71, 214), 'Mystic Hood',
                                            equippable=mystic_hood_component, info=mystic_hood_info_component)

                    broken_sword_component = Equippable(EquipmentSlots.HEAD, strength_bonus=1, crit_chance_bonus=3)
                    broken_sword_info_component = Information('broken_sword')
                    broken_sword_entity = Entity(0, 0, '-', libtcod.Color(219, 219, 219), 'Broken Sword',
                                            equippable=broken_sword_component, info=broken_sword_info_component)

                    zombie_equipment.append(ragged_shoes_entity)
                    zombie_equipment.append(torn_pants_entity)
                    zombie_equipment.append(mystic_hood_entity)
                    zombie_equipment.append(broken_sword_entity)

                    monster = Entity(x, y, 'z', libtcod.darkest_green, 'risen corpse', blocks=True,
                                     inventory=enemy_inventory_component, render_order=RenderOrder.ACTOR, fighter=zombie_fighter_component, ai=ai_component,
                                     equipment=enemy_equipment_component, info=enemy_info_component)

                    for equip in zombie_equipment:
                        if randint(1, 4) > 3:
                            monster.inventory.add_item(equip)
                            monster.equipment.toggle_equip(equip)
                    if monster.fighter.hp < monster.fighter.max_hp:
                        monster.fighter.heal(1000000)

                elif monster_choice == 'cultist':
                    fighter_component = Fighter(hp=20, defense=1, strength=5, accuracy=85, dodge=15, ability_power=0, crit_chance=10, xp=100)
                    ai_component = BasicMonster()
                    enemy_inventory_component = Inventory(5)
                    enemy_equipment_component = Equipment()
                    enemy_info_component = Information('cultist')

                    cultist_cloak_component = Equippable(EquipmentSlots.UPPER_BODY, dodge_bonus=5, max_hp_bonus=10)
                    cultist_cloak_info_component = Information('cultist_cloak')
                    cultist_cloak_entity = Entity(0, 0, '&', libtcod.Color(108, 12, 138), 'Cultist Cloak',
                                            equippable=cultist_cloak_component, info=cultist_cloak_info_component)

                    cultist_blade_component = Equippable(EquipmentSlots.MAIN_HAND, crit_chance_bonus=10, strength_bonus=2)
                    cultist_blade_info_component = Information('cultist_blade')
                    cultist_blade_entity = Entity(0, 0, '-', libtcod.Color(179, 179, 179), 'Cultist Blade',
                                            equippable=cultist_blade_component, info=cultist_blade_info_component)

                    monster = Entity(x, y, 'C', libtcod.Color(34, 3, 43), 'cultist', blocks=True, fighter=fighter_component,
                                     inventory=enemy_inventory_component, render_order=RenderOrder.ACTOR, ai=ai_component, equipment=enemy_equipment_component, info=enemy_info_component)

                    monster.inventory.add_item(cultist_cloak_entity)
                    monster.inventory.add_item(cultist_blade_entity)
                    monster.equipment.toggle_equip(cultist_cloak_entity)
                    monster.equipment.toggle_equip(cultist_blade_entity)

                    if monster.fighter.hp < monster.fighter.max_hp:
                        monster.fighter.heal(1000000)

                elif monster_choice == 'unholy_priest':
                    priest_fighter_component = Fighter(hp=40, defense=1, strength=2, accuracy=90, dodge=15, ability_power=0, crit_chance=5, xp=150)
                    ai_component = AbilityMonster()
                    enemy_inventory_component = Inventory(5)
                    enemy_equipment_component = Equipment()
                    enemey_abilities_component = Abilities(2)
                    enemy_info_component = Information('unholy_priest')

                    tattered_robe_component = Equippable(EquipmentSlots.UPPER_BODY, max_hp_bonus=10, dodge_bonus=10, defense_bonus=1)
                    tattered_robe_info_component = Information('tattered_robe')
                    tattered_robe_entity = Entity(0, 0, 'C', libtcod.Color(232, 216, 125), 'Tattered Robe',
                                            equippable=tattered_robe_component, info=tattered_robe_info_component)

                    corrupted_scripture_component = Equippable(EquipmentSlots.MAIN_HAND, max_hp_bonus=-10, ability_power_bonus=5)
                    corrupted_scripture_info_component = Information('corrupted_scripture')
                    corrupted_scripture_entity = Entity(0, 0, '#', libtcod.Color(110, 0, 0), 'Corrupted Scripture',
                                            equippable=corrupted_scripture_component, info=corrupted_scripture_info_component)

                    monster = Entity(x, y, 'P', libtcod.Color(189, 169, 53), 'unholy priest', blocks=True, fighter=priest_fighter_component,
                                     inventory=enemy_inventory_component, abilities=enemey_abilities_component, render_order=RenderOrder.ACTOR,
                                     ai=ai_component, equipment=enemy_equipment_component, info=enemy_info_component)

                    eldritch_bolt = Feat(name="Eldritch Bolt", cooldown=3, damage=10, feat_function=cast_unholy_bolt_feat)

                    monster.abilities.add_feat([eldritch_bolt])
                    monster.inventory.add_item(corrupted_scripture_entity)
                    monster.inventory.add_item(tattered_robe_entity)
                    monster.equipment.toggle_equip(corrupted_scripture_entity)
                    monster.equipment.toggle_equip(tattered_robe_entity)

                elif monster_choice == 'shadowy_horror':
                    horror_fighter_component = Fighter(hp=60, defense=0, strength=2, accuracy=100, dodge=25, ability_power=0, crit_chance=10, xp=200)
                    ai_component = BasicMonster()
                    enemy_inventory_component = Inventory(5)
                    enemy_equipment_component = Equipment()
                    enemy_info_component = Information('shadowy_horror')

                    shadowy_hide_component = Equippable(EquipmentSlots.UPPER_BODY, dodge_bonus=15, defense_bonus=3)
                    shadowy_hide_info_component = Information('shadowy_hide')
                    shadowy_hide_entity = Entity(0, 0, 'h', libtcod.Color(0, 0, 0), 'shadowy hide',
                                            equippable=shadowy_hide_component, info=shadowy_hide_info_component)

                    shadowy_appendage_component = Equippable(EquipmentSlots.MAIN_HAND, strength_bonus=5, crit_chance_bonus=15)
                    shadowy_appendage_info_component = Information('shadowy_appendage')
                    shadowy_appendage_entity = Entity(0, 0, '|', libtcod.Color(0, 0, 0), 'shadowy appendage',
                                            equippable=shadowy_appendage_component, info=shadowy_appendage_info_component)

                    shadowy_mask_component = Equippable(EquipmentSlots.HEAD, accuracy_bonus=25, ability_power_bonus=10)
                    shadowy_mask_info_component = Information('shadowy_mask')
                    shadowy_mask_entity = Entity(0, 0, '|', libtcod.Color(0, 0, 0), 'shadowy mask',
                                            equippable=shadowy_mask_component, info=shadowy_mask_info_component)

                    monster = Entity(x, y, 'H', libtcod.Color(0, 0, 0), 'shadowy horror', blocks=True, fighter=horror_fighter_component,
                                     inventory=enemy_inventory_component, render_order=RenderOrder.ACTOR, ai=ai_component, equipment=enemy_equipment_component, info=enemy_info_component)

                    monster.inventory.add_item(shadowy_hide_entity)
                    monster.inventory.add_item(shadowy_appendage_entity)
                    monster.inventory.add_item(shadowy_mask_entity)
                    monster.equipment.toggle_equip(shadowy_hide_entity)
                    monster.equipment.toggle_equip(shadowy_appendage_entity)
                    monster.equipment.toggle_equip(shadowy_mask_entity)


                entities.append(monster)

        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_choice = random_choice_from_dict(item_chances)

                if item_choice == 'healing_potion':
                    hp_potion_item_component = Item(use_function=heal, amount=40)
                    hp_potion_info_component = Information('healing_potion')
                    item = Entity(x, y, '!', libtcod.violet, 'Healing Potion', render_order=RenderOrder.ITEM,
                                  item=hp_potion_item_component, info=hp_potion_info_component)
                elif item_choice == 'plain_shirt':
                    pshirt_equippable_component = Equippable(EquipmentSlots.UPPER_BODY, max_hp_bonus=15)
                    pshirt_info_component = Information('plain_shirt')
                    item = Entity(x, y, 'v', libtcod.white, 'Plain Shirt', render_order=RenderOrder.ITEM, equippable=pshirt_equippable_component,
                                  info=pshirt_info_component)
                elif item_choice == 'dull_sword':
                    dsword_equippable_component = Equippable(EquipmentSlots.MAIN_HAND, strength_bonus=2, crit_chance_bonus=5)
                    dsword_info_component = Information('dull_sword')
                    item = Entity(x, y, '/', libtcod.darkest_gray, 'Dull Sword', render_order=RenderOrder.ITEM, equippable=dsword_equippable_component,
                                  info=dsword_info_component)
                elif item_choice == 'sharpened_sword':
                    ssword_equippable_component = Equippable(EquipmentSlots.MAIN_HAND, strength_bonus=4, crit_chance_bonus=7)
                    ssword_info_component = Information('sharpened_sword')
                    item = Entity(x, y, '/', libtcod.lightest_gray, 'Sharpened Sword', render_order=RenderOrder.ITEM, equippable=ssword_equippable_component,
                                  info=ssword_info_component)
                elif item_choice == 'battered_shield':
                    bshield_equippable_component = Equippable(EquipmentSlots.OFF_HAND, max_hp_bonus=10, defense_bonus=1)
                    bshield_info_component = Information('broken_shield')
                    item = Entity(x, y, '[', libtcod.orange, 'Shield', render_order=RenderOrder.ITEM, equippable=bshield_equippable_component,
                                  info=bshield_info_component)
                elif item_choice == 'hardened_shield':
                    hshield_equippable_component = Equippable(EquipmentSlots.OFF_HAND, max_hp_bonus=15, defense_bonus=2)
                    hshield_info_component = Information('hardened_shield')
                    item = Entity(x, y, '[', libtcod.darker_orange, 'Shield', render_order=RenderOrder.ITEM, equippable=hshield_equippable_component,
                                  info=hshield_info_component)
                elif item_choice == 'lost_pages':
                    lpages_equippable_component = Equippable(EquipmentSlots.OFF_HAND, ability_power_bonus=2, dodge_bonus=5)
                    lpages_info_component = Information('lost_pages')
                    item = Entity(x, y, '#', libtcod.light_sepia, 'Lost Pages', render_order=RenderOrder.ITEM, equippable=lpages_equippable_component,
                                  info=lpages_info_component)
                elif item_choice == 'dirty_spectacles':
                    dspecs_equippable_component = Equippable(EquipmentSlots.HEAD, accuracy_bonus=10, crit_chance_bonus=10, ability_power_bonus=-1)
                    dspecs_info_component = Information('dirty_spectacles')
                    item = Entity(x, y, '8', libtcod.lightest_blue, 'Dirty Spectacles', render_order=RenderOrder.ITEM, equippable=dspecs_equippable_component,
                                  info=dspecs_info_component)
                elif item_choice == 'fine_shoes':
                    fshoes_equippable_component = Equippable(EquipmentSlots.FEET, dodge_bonus=10, accuracy_bonus=10)
                    fshoes_info_component = Information('fine_shoes')
                    item = Entity(x, y, 's', libtcod.Color(235, 190, 66), 'Fine Shoes', render_order=RenderOrder.ITEM, equippable=fshoes_equippable_component,
                                  info=fshoes_info_component)
                elif item_choice == 'rough_trousers':
                    rpants_equippable_component = Equippable(EquipmentSlots.FEET, max_hp_bonus=15, defense_bonus=2, dodge_bonus=-10)
                    rpants_info_component = Information('rough_trousers')
                    item = Entity(x, y, 'p', libtcod.Color(237, 114, 19), 'Rough Trousers', render_order=RenderOrder.ITEM, equippable=rpants_equippable_component,
                                  info=rpants_info_component)
                elif item_choice == 'fireball_scroll':
                    item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message(
                        'Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan),
                                          damage=25, radius=3)
                    fireballsc_info_component = Information('fireball_scroll')
                    item = Entity(x, y, '#', libtcod.red, 'Fireball Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component, info=fireballsc_info_component)
                elif item_choice == 'confusion_scroll':
                    item_component = Item(use_function=cast_confuse, targeting=True, targeting_message=Message(
                        'Left-click an enemy to confuse it, or right-click to cancel.', libtcod.light_cyan))
                    confusionsc_info_component = Information('confusion_scroll')
                    item = Entity(x, y, '#', libtcod.light_pink, 'Confusion Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component, info=confusionsc_info_component)
                elif item_choice == 'lightning_scroll':
                    item_component = Item(use_function=cast_lightning, damage=40, maximum_range=5)
                    lightningsc_info_component = Information('lightning_scroll')
                    item = Entity(x, y, '#', libtcod.yellow, 'Lightning Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component, info=lightningsc_info_component)
                elif item_choice == 'fireball_tome':
                    item_component = Item(use_function=add_fireball)
                    firetome_info_component = Information('fireball_tome')
                    item = Entity(x, y, 't', libtcod.red, 'Fireball Tome', render_order=RenderOrder.ITEM,
                                  item=item_component, info=firetome_info_component)
                elif item_choice == 'confusion_tome':
                    item_component = Item(use_function=add_confusion)
                    confusiontome_info_component = Information('confusion_tome')
                    item = Entity(x, y, 't', libtcod.lighter_pink, 'Confusion Tome', render_order=RenderOrder.ITEM,
                                  item=item_component, info=confusiontome_info_component)
                elif item_choice == 'eldritch_blast_tome':
                    item_component = Item(use_function=add_eldritch_blast)
                    ebtome_info_component = Information('eldritch_blast_tome')
                    item = Entity(x, y, 't', libtcod.Color(148, 103, 245), 'Eldritch Blast Tome', render_order=RenderOrder.ITEM,
                                  item=item_component, info=ebtome_info_component)
                elif item_choice == 'lightning_tome':
                    item_component = Item(use_function=add_lightning)
                    lighttome_info_component = Information('lightning_tome')
                    item = Entity(x, y, 't', libtcod.light_yellow, 'Lightning Bolt Tome', render_order=RenderOrder.ITEM,
                                  item=item_component, info=lighttome_info_component)

                entities.append(item)

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False

    def is_door(self, x, y):
        if self.tiles[x][y].door:
            return True

        return False

    def next_floor(self, player, message_log, constants):
        self.dungeon_level += 1
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player, entities)

        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message('You tend to your wounds and push onwards.', libtcod.light_violet))

        return entities