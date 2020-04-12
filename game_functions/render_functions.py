import tcod as libtcod
from enum import Enum
from game_states import GameStates
import textwrap




from menus import character_screen, inventory_menu, ability_menu, item_menu, level_up_menu


class RenderOrder(Enum):
    STAIRS = 1
    CORPSE = 2
    ITEM = 3
    ACTOR = 4
    PLAYER = 5

def get_names_under_mouse(mouse, player, entities, fov_map, game_state):
    (x, y) = (mouse.cx, mouse.cy)

    if not game_state == game_state.ITEM_MENU:
        names = [entity.name for entity in entities
                 if entity.x == x and entity.y == y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]

        names = ', \n'.join(names)

    else:
        for item in player.inventory.items:
            if hasattr(item[0], 'selected') and item[0].selected:
                names = item[0].name

    return names.title()

def get_info_under_mouse(mouse, player, entities, fov_map, game_state):
    (x, y) = (mouse.cx, mouse.cy)

    if not game_state == game_state.ITEM_MENU:
        info = [entity.info for entity in entities
                 if entity.x == x and entity.y == y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]

        entity_hp = [entity.fighter for entity in entities
                 if entity.x == x and entity.y == y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]

        if len(info) != 0:
            if entity_hp and entity_hp[0] is not None:
                entity_info = info[0].display(entity_hp)
            else:
                entity_info = info[0].display()
        else:
            entity_info = ''
    else:
        for item in player.inventory.items:
            if hasattr(item[0], 'selected') and item[0].selected:
                entity_info = item[0].info.display()

    wrapped_info = textwrap.wrap(entity_info, 23, replace_whitespace=False)

    return wrapped_info

def get_equipment(player, inventory):

    equipment_array = []

    for item_array in inventory.items:
        if player.equipment.main_hand == item_array[0]:
            equipment_array.append('{0}\n (on main hand)'.format(item_array[0].name))
        elif player.equipment.off_hand == item_array[0]:
            equipment_array.append('{0}\n (on off hand)'.format(item_array[0].name))
        elif player.equipment.upper_body == item_array[0]:
            equipment_array.append('{0}\n (on upper body)'.format(item_array[0].name))
        elif player.equipment.lower_body == item_array[0]:
            equipment_array.append('{0}\n (on lower body)'.format(item_array[0].name))
        elif player.equipment.head == item_array[0]:
            equipment_array.append('{0}\n (on head)'.format(item_array[0].name))
        elif player.equipment.feet == item_array[0]:
            equipment_array.append('{0}\n (on feet)'.format(item_array[0].name))


    if len(equipment_array) != 0:
        equipment_sheet = ', \n\n'.join(equipment_array)
    else:
        equipment_sheet = 'Nothing is equipped.'

    return equipment_sheet


def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER,
                             '{0}: {1}/{2}'.format(name, value, maximum))


def render_all(con, panel, panel_bg, info, info_bg, player_con, player_con_bg, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height, map_width, map_height,
               bar_width, panel_height, panel_y, info_width, info_x, player_con_width, player_con_x, player_con_y, mouse, colors, game_state):
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):

                libtcod.console_set_char_background(con, x, y, colors.get('background'), libtcod.BKGND_SET)

                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight and game_map.tiles[x][y].blocked
                door = game_map.tiles[x][y].block_sight and not game_map.tiles[x][y].blocked

                if visible:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors.get('light_wall'), libtcod.BKGND_SET)
                    elif door:
                        libtcod.console_set_char_background(con, x, y, colors.get('light_door'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, colors.get('light_ground'), libtcod.BKGND_SET)
                    game_map.tiles[x][y].explored = True

                elif game_map.tiles[x][y].explored:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
                    elif door:
                        libtcod.console_set_char_background(con, x, y, colors.get('dark_door'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)

                if game_map.tiles[x][y].door and player.x == game_map.tiles[x][y].x and player.y == game_map.tiles[x][y].y:
                    game_map.tiles[x][y].block_sight = False
                    game_map.tiles[x][y].door = False


    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map, game_map)


    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

    libtcod.console_set_default_background(info_bg, libtcod.Color(16, 8, 20))
    libtcod.console_set_default_background(info, libtcod.Color(36, 31, 42))
    libtcod.console_set_default_background(panel_bg, libtcod.Color(16, 8, 20))
    libtcod.console_set_default_background(panel, libtcod.Color(36, 31, 42))
    libtcod.console_set_default_background(player_con_bg, libtcod.Color(16, 8, 20))
    libtcod.console_set_default_background(player_con, libtcod.Color(36, 31, 42))

    libtcod.console_clear(panel)
    libtcod.console_clear(info)
    libtcod.console_clear(player_con)
    libtcod.console_clear(panel_bg)
    libtcod.console_clear(info_bg)
    libtcod.console_clear(player_con_bg)

    libtcod.console_print_ex(player_con, 12, 2, libtcod.BKGND_NONE, libtcod.CENTER,
                             'Equipment')
    libtcod.console_print_ex(player_con, 12, 5, libtcod.BKGND_NONE, libtcod.CENTER,
                             get_equipment(player, player.inventory))

    message_y = 1
    for message in message_log.messages:
        libtcod.console_set_default_foreground(panel, message.color)
        libtcod.console_print_ex(panel, message_log.x, message_y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
        message_y += 1

    render_bar(panel, 1, 3, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp,
               libtcod.light_red, libtcod.darker_red)

    libtcod.console_print_ex(panel, 2, 5, libtcod.BKGND_NONE, libtcod.LEFT, 'Level: {0}'.format(player.level.curr_level))

    libtcod.console_print_ex(panel, 2, 7, libtcod.BKGND_NONE, libtcod.LEFT, 'XP: {0}'.format(player.level.curr_xp))

    libtcod.console_print_ex(panel, 2, 9, libtcod.BKGND_NONE, libtcod.LEFT, 'XP to Level: {0}'.format(player.level.experience_to_next_level))

    libtcod.console_print_ex(panel, 2, 11, libtcod.BKGND_NONE, libtcod.LEFT, 'Dungeon level: {0}'.format(game_map.dungeon_level))

    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    libtcod.console_set_alignment(panel, libtcod.CENTER)
    libtcod.console_print_ex(info, 12, 2, libtcod.BKGND_NONE, libtcod.CENTER,
                             get_names_under_mouse(mouse, player, entities, fov_map, game_state))

    info_y = 6
    for info_lines in get_info_under_mouse(mouse, player, entities, fov_map, game_state):
        libtcod.console_print_ex(info, 12, info_y, libtcod.BKGND_NONE, libtcod.CENTER,
                                 info_lines)
        info_y += 1

    libtcod.console_blit(panel_bg, 0, 0, screen_width - info_width, panel_height, 0, 0, panel_y)
    libtcod.console_blit(panel, -1, -1, screen_width - info_width, panel_height - 1, 0, 0, panel_y)
    libtcod.console_blit(info_bg, 0, 0, info_width, int(screen_height / 2), 0, info_x, 0)
    libtcod.console_blit(info, -1, -1, info_width - 1, int(screen_height / 2), 0, info_x, 0)
    libtcod.console_blit(player_con_bg, 0, 0, player_con_width, int(screen_height / 2) + 1, 0, player_con_x, player_con_y)
    libtcod.console_blit(player_con, -1, -1, player_con_width - 1, int(screen_height / 2), 0, player_con_x,
                         player_con_y)

    if game_state == GameStates.SHOW_INVENTORY:
        inventory_title = 'Press the key next to an item to examine it, or Esc to cancel.\n'
        inventory_menu(con, inventory_title, player, 50, map_width, map_height)

    elif game_state == GameStates.SHOW_ABILITIES:
        abilities_title = 'Press the key next to the ability to use it, or Esc to cancel.\n'
        ability_menu(con, abilities_title, player, 50, map_width, map_height)

    elif game_state == GameStates.ITEM_MENU:
        inventory_title = 'Press the key next to what to do with item, or Esc to cancel.\n'
        inventory_menu(con, inventory_title, player, 50, map_width - 15, map_height)

        item_menu(con, 20, map_width + 35, map_height + 3)

    elif game_state == GameStates.LEVEL_UP:
        level_up_menu(con, 'You grow stronger, choose a stat to raise:', player, 60, map_width, map_height)

    elif game_state == GameStates.CHARACTER_SCREEN:
        character_screen(player, 30, 13, map_width, map_height)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, fov_map, game_map):
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y) or \
            (entity.stairs and game_map.tiles[entity.x][entity.y].explored):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)


def clear_entity(con, entity):
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)