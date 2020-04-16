import tcod as libtcod

from game_functions.death_functions import kill_monster, kill_player
from loader_functions.data_loaders import load_game, save_game
from menus import main_menu, character_select_menu, message_box
from game_functions.render_functions import clear_all, render_all
from entity import get_blocking_entities_at_location
from game_functions.fov_functions import initialize_fov, recompute_fov
from game_messages import Message
from game_states import GameStates
from input_handlers import handle_keys, handle_mouse, handle_main_menu, handle_character_select
from loader_functions.initialize_new_game import get_constants, initialize_game


def main():
    constants = get_constants()

    libtcod.console_set_custom_font('img/Tocky-square-10x10.png', libtcod.FONT_LAYOUT_ASCII_INROW)

    libtcod.console_init_root(constants['screen_width'], constants['screen_height'], constants['window_title'], False)

    con = libtcod.console_new(constants['screen_width'], constants['screen_height'])
    panel = libtcod.console_new(constants['screen_width'], constants['panel_height'])
    panel_bg = libtcod.console_new(constants['screen_width'], constants['panel_height'])
    info = libtcod.console_new(constants['info_width'], constants['screen_height'])
    info_bg = libtcod.console_new(constants['info_width'], constants['screen_height'])
    player_con = libtcod.console_new(constants['player_con_width'], constants['player_con_x'])
    player_con_bg = libtcod.console_new(constants['player_con_width'], constants['player_con_x'])

    player = None
    entities = []
    game_map = None
    message_log = None
    game_state = None
    

    show_main_menu = True
    show_character_select = False

    show_load_error_message = False

    main_menu_background_image = libtcod.image_load('img/castle.png')
    character_select_background_image = libtcod.image_load('img/castle.png')

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if show_main_menu and not show_character_select:

            main_menu(con, main_menu_background_image, constants['screen_width'],
                      constants['screen_height'])

            if show_load_error_message:
                message_box(con, 'No Save Game to Load', 50, constants['screen_width'], constants['screen_height'])

            libtcod.console_flush()

            action = handle_main_menu(key)

            new_game = action.get('new_game')
            load_saved_game = action.get('load_game')
            exit_game = action.get('exit')

            if show_load_error_message and (new_game or load_saved_game or exit_game):
                show_load_error_message = False

            elif new_game:
                show_character_select = True
                show_main_menu = False

            elif load_saved_game:
                try:
                    player, entities, game_map, message_log, game_state, permanent_cooldown_counter = load_game()
                    show_main_menu = False
                except FileNotFoundError:
                    show_load_error_message = True
            elif exit_game:
                break

        elif show_character_select and not show_main_menu:

            character_select_menu(con, character_select_background_image, constants['screen_width'],
                                  constants['screen_height'])

            libtcod.console_flush()

            action = handle_character_select(key)

            thief = action.get('thief')
            brute = action.get('brute')
            occultist = action.get('occultist')

            if thief:
                player, entities, game_map, message_log, game_state, permanent_cooldown_counter = initialize_game(constants, "thief")
                game_state = GameStates.PLAYERS_TURN
                show_character_select = False

            elif brute:
                player, entities, game_map, message_log, game_state, permanent_cooldown_counter = initialize_game(constants, "brute")
                player.fighter.heal(player.inventory.items[0][0].equippable.max_hp_bonus)
                game_state = GameStates.PLAYERS_TURN
                show_character_select = False

            elif occultist:
                player, entities, game_map, message_log, game_state, permanent_cooldown_counter = initialize_game(constants, "occultist")
                game_state = GameStates.PLAYERS_TURN
                show_character_select = False

        elif not (show_main_menu and show_character_select):
            libtcod.console_clear(con)
            play_game(player, entities, game_map, message_log, game_state, con, panel, panel_bg, info, info_bg,
                      player_con, player_con_bg, constants, permanent_cooldown_counter)

            show_main_menu = True


def play_game(player, entities, game_map, message_log, game_state, con, panel, panel_bg, info, info_bg, player_con, player_con_bg, constants, permanent_cooldown_counter):
    fov_recompute = True

    fov_map = initialize_fov(game_map)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state

    targeting_item = None
    targeting_feat = None

    game_turn_counter = 0
    cooldown_counter = permanent_cooldown_counter
    
    
    
    

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if fov_recompute:
            fov_map = initialize_fov(game_map)
            recompute_fov(fov_map, player.x, player.y, constants['fov_radius'], constants['fov_light_walls'],
                          constants['fov_algorithm'])

        render_all(con, panel, panel_bg, info, info_bg, player_con, player_con_bg, entities, player, game_map, fov_map, fov_recompute, message_log,
                   constants['screen_width'], constants['screen_height'], constants['map_width'], constants['map_height'], constants['bar_width'],
                   constants['panel_height'], constants['panel_y'], constants['info_width'], constants['info_x'],
                   constants['player_con_width'], constants['player_con_x'], constants['player_con_y'], mouse, constants['colors'], game_state)

        fov_recompute = False

        libtcod.console_flush()

        clear_all(con, entities)

        action = handle_keys(key, game_state)
        mouse_action = handle_mouse(mouse)

        move = action.get('move')
        wait = action.get('wait')
        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        show_abilities = action.get('show_abilities')
        use = action.get('use')
        drop = action.get('drop')
        inventory_index = action.get('inventory_index')
        ability_index = action.get('ability_index')
        take_stairs = action.get('take_stairs')
        level_up = action.get('level_up')
        show_character_screen = action.get('show_character_screen')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        left_click = mouse_action.get('left_click')
        right_click = mouse_action.get('right_click')

        player_turn_results = []

        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)

                else:
                    player.move(dx, dy)
                    fov_recompute = True
                    if game_map.is_door(destination_x, player.y):
                        message_log.add_message(Message('The door creaks open.', libtcod.yellow))

                game_state = GameStates.ENEMY_TURN

        elif wait:
            game_state = GameStates.ENEMY_TURN

        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y:
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)
                    break
            else:
                message_log.add_message(Message('There is nothing here to pick up.', libtcod.yellow))

        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY

        if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(
                player.inventory.items):
            item_index = inventory_index
            item = player.inventory.items[inventory_index][0]

            item.selected = True
            game_state = GameStates.ITEM_MENU

        if use:
            player_turn_results.extend(player.inventory.use(item, item_index, entities=entities, fov_map=fov_map))
            game_state = GameStates.SHOW_INVENTORY
            if game_state != GameStates.TARGETING:
                item.selected = False
            else:
                item.selected = True
        elif drop:
            player_turn_results.extend(player.inventory.drop_item(item, item_index))
            item.selected = False

        if show_abilities:
            previous_game_state = game_state
            game_state = GameStates.SHOW_ABILITIES

        if ability_index is not None and previous_game_state != GameStates.PLAYER_DEAD and ability_index < len(
                player.abilities.feats):
            feat = player.abilities.feats[ability_index]

            if feat.turn_performed is None or (cooldown_counter - feat.turn_performed > feat.cooldown):
                player_turn_results.extend(player.abilities.perform(feat, turn_performed=cooldown_counter, entities=entities, fov_map=fov_map,
                                                                ability_power=player.fighter.ability_power))
            else:
                message_log.add_message(Message('That ability is on cooldown.', libtcod.white))

        if take_stairs and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.stairs and entity.x == player.x and entity.y == player.y:
                    entities = game_map.next_floor(player, message_log, constants)
                    fov_map = initialize_fov(game_map)
                    fov_recompute = True
                    libtcod.console_clear(con)

                    break
            else:
                message_log.add_message(Message('There are no stairs here.', libtcod.yellow))

        if level_up:
            if level_up == 'hp':
                player.fighter.base_max_hp += 20
                player.fighter.hp += 20
            elif level_up == 'str':
                player.fighter.base_strength += 1
            elif level_up == 'def':
                player.fighter.base_defense += 1
            elif level_up == 'dog':
                player.fighter.base_dodge += 3
            elif level_up == 'ap':
                player.fighter.base_ability_power += 2
            elif level_up == 'crit':
                player.fighter.base_crit_chance += 5

            game_state = previous_game_state

        if show_character_screen:
            previous_game_state = game_state
            game_state = GameStates.CHARACTER_SCREEN

        if game_state == GameStates.TARGETING:
            if left_click:
                target_x, target_y = left_click

                if hasattr(targeting, 'item'):
                    item_use_results = player.inventory.use(targeting_item, item_index, entities=entities, fov_map=fov_map,
                                                            target_x=target_x, target_y=target_y)
                    player_turn_results.extend(item_use_results)
                    item.selected = False

                else:
                    if feat.turn_performed is None or game_state == GameStates.TARGETING or (cooldown_counter - feat.turn_performed > feat.cooldown):
                        feat_use_results = player.abilities.perform(targeting_feat, turn_performed=cooldown_counter, entities=entities, fov_map=fov_map,
                                                                    target_x=target_x, target_y=target_y,
                                                                    ability_power=player.fighter.ability_power)
                        player_turn_results.extend(feat_use_results)
                    else:
                        message_log.add_message(Message('That ability is on cooldown.', libtcod.white))

            elif right_click:
                player_turn_results.append({'targeting_cancelled': True})

        if exit:
            if game_state in (
                    GameStates.SHOW_INVENTORY, GameStates.SHOW_ABILITIES,
                    GameStates.CHARACTER_SCREEN):
                game_state = previous_game_state
                for item in player.inventory.items:
                    if hasattr(item[0], 'selected') and item[0].selected:
                        item[0].selected = False
            elif game_state == GameStates.ITEM_MENU:
                for item in player.inventory.items:
                    if hasattr(item[0], 'selected') and item[0].selected:
                        item[0].selected = False
                game_state = GameStates.SHOW_INVENTORY

            elif game_state == GameStates.TARGETING:
                player_turn_results.append({'targeting_cancelled': True})
                for item in player.inventory.items:
                    if hasattr(item[0], 'selected') and item[0].selected:
                        item[0].selected = False
            else:
                save_game(player, entities, game_map, message_log, game_state, cooldown_counter)

                return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')
            item_consumed = player_turn_result.get('consumed')
            feat_performed = player_turn_result.get('performed')
            item_dropped = player_turn_result.get('item_dropped')
            enemy_item_dropped = player_turn_result.get('enemy_item_dropped')
            equip = player_turn_result.get('equip')
            targeting = player_turn_result.get('targeting')
            targeting_cancelled = player_turn_result.get('targeting_cancelled')
            xp = player_turn_result.get('xp')

            if message:
                message_log.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message, loot = kill_monster(dead_entity)
                    if loot is not None:
                        player_turn_results.extend(dead_entity.inventory.drop_item(loot[0], dead_entity.inventory.items.index(loot)))

                message_log.add_message(message)

            if item_added:
                entities.remove(item_added)

                game_state = GameStates.ENEMY_TURN

            if item_consumed:
                game_state = GameStates.ENEMY_TURN

            if feat_performed:
                game_state = GameStates.ENEMY_TURN

            if item_dropped:
                entities.append(item_dropped)

                game_state = GameStates.ENEMY_TURN

            if enemy_item_dropped:
                entities.append(enemy_item_dropped)

            if equip:
                equip_results = player.equipment.toggle_equip(equip)

                for equip_result in equip_results:
                    equipped = equip_result.get('equipped')
                    unequipped = equip_result.get('unequipped')

                    if equipped:
                        message_log.add_message(Message('You equipped the {0}'.format(equipped.name)))

                    if unequipped:
                        message_log.add_message(Message('You unequipped the {0}'.format(unequipped.name)))

                game_state = GameStates.ENEMY_TURN

            if targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING

                if hasattr(targeting, 'item'):
                    targeting_item = targeting

                    message_log.add_message(targeting_item.item.targeting_message)

                else:
                    targeting_feat = targeting

                    message_log.add_message(targeting_feat.targeting_message)

            if targeting_cancelled:
                game_state = previous_game_state

                message_log.add_message(Message('Targeting Cancelled'))

            if xp:
                leveled_up = player.level.add_xp(xp)
                message_log.add_message(Message('You gain {0} experience points.'.format(xp)))

                if leveled_up:
                    message_log.add_message(Message(
                        'You have faced enough horrors and grow stronger, you reach level {0}'.format(
                            player.level.curr_level) + '!', libtcod.yellow))
                    previous_game_state = game_state
                    game_state = GameStates.LEVEL_UP

        if game_state == GameStates.ENEMY_TURN:
            game_turn_counter += 1
            cooldown_counter += 1

            for feat in player.abilities.feats:
                if feat.turn_performed is not None:
                    if ((cooldown_counter - 1) - feat.turn_performed) < feat.cooldown:
                        feat.turn_ready = str(feat.cooldown - (cooldown_counter - feat.turn_performed) + 1)
                    else:
                        feat.turn_ready = "Ready!"

            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities, game_turn_counter)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            message_log.add_message(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message, loot = kill_monster(dead_entity)

                            message_log.add_message(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break

                    if game_state == GameStates.PLAYER_DEAD:
                        break
            else:
                game_state = GameStates.PLAYERS_TURN


if __name__ == '__main__':
    main()
