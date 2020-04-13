import tcod as libtcod


def menu(con, header, options, width, screen_width, screen_height):
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate total height for the header (after auto-wrap) and one line per option
    header_height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
    height = len(options) + header_height

    # create an off-screen console that represents the menu's window
    window = libtcod.console_new(width, height)

    # print the header, with auto-wrap
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    # print all the options
    y = header_height
    letter_index = ord('1')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        letter_index += 1

    # blit the contents of "window" to the root console
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

def inventory_menu(con, header, player, inventory_width, map_width, map_height):
    if len(player.inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        options = []

        for item_array in player.inventory.items:
            if player.equipment.main_hand == item_array[0]:
                options.append('{0} (on main hand) x{1}'.format(item_array[0].name, len(item_array)))
            elif player.equipment.off_hand == item_array[0]:
                options.append('{0} (on off hand) x{1}'.format(item_array[0].name, len(item_array)))
            elif player.equipment.upper_body == item_array[0]:
                options.append('{0} (on upper body) x{1}'.format(item_array[0].name, len(item_array)))
            elif player.equipment.lower_body == item_array[0]:
                options.append('{0} (on lower body) x{1}'.format(item_array[0].name, len(item_array)))
            elif player.equipment.head == item_array[0]:
                options.append('{0} (on head) x{1}'.format(item_array[0].name, len(item_array)))
            elif player.equipment.feet == item_array[0]:
                options.append('{0} (on feet) x{1}'.format(item_array[0].name, len(item_array)))
            else:
                options.append('{0} x{1}'.format(item_array[0].name, len(item_array)))

    menu(con, header, options, inventory_width, map_width, map_height)

def ability_menu(con, header, player, abilities_width, map_width, map_height):

    if len(player.abilities.feats) == 0:
        options = ['You have no abilities.']
    else:
        options = []

        for feat in player.abilities.feats:
            options.append('{0} ({1})'.format(feat.name, feat.turn_ready))

    menu(con, header, options, abilities_width, map_width, map_height)

def item_menu(con, item_menu_width, offcenter_width, offcenter_height):

    options = ['Use', 'Drop']

    menu(con, '', options, item_menu_width, offcenter_width, offcenter_height)

def main_menu(con, background_image, screen_width, screen_height):
    libtcod.image_blit_2x(background_image, 0, 0, 0)

    libtcod.console_set_default_foreground(0, libtcod.dark_purple)
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER,
                             'Quest of Shadows')

    menu(con, '', ['Play a new game', 'Continue last game', 'Quit'], 24, screen_width, screen_height)

def character_select_menu(con, background_image, screen_width, screen_height):
    libtcod.image_blit_2x(background_image, 0, 0, 0)

    libtcod.console_set_default_foreground(0, libtcod.dark_purple)
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER,
                             'Choose your character...')


    menu(con, '', ['The Thief', 'The Brute', 'The Occultist'], 24, screen_width, screen_height)


def level_up_menu(con, header, player, menu_width, map_width, map_height):
    options = ['Constitution (+20 HP, from {0})'.format(player.fighter.max_hp),
               'Strength (+1 attack, from {0})'.format(player.fighter.strength),
               'Perseverance (+1 defense, from {0})'.format(player.fighter.defense),
               'Agility (+3 dodge, from {0})'.format(player.fighter.dodge),
               'Ability Power (+2 ability power, from {0})'.format(player.fighter.ability_power),
               'Crit Chance (+5 Crit Chance, from {0})'.format(player.fighter.crit_chance)]

    menu(con, header, options, menu_width, map_width, map_height)

def character_screen(player, character_screen_width, character_screen_height, map_width, map_height):
    window = libtcod.console_new(character_screen_width, character_screen_height)

    libtcod.console_set_default_foreground(window, libtcod.white)

    libtcod.console_print_rect_ex(window, 0, 1, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Character Information')
    libtcod.console_print_rect_ex(window, 0, 2, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Level: {0}'.format(player.level.curr_level))
    libtcod.console_print_rect_ex(window, 0, 3, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Experience: {0}'.format(player.level.curr_xp))
    libtcod.console_print_rect_ex(window, 0, 4, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Experience to Level: {0}'.format(player.level.experience_to_next_level))
    libtcod.console_print_rect_ex(window, 0, 6, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Maximum HP: {0}'.format(player.fighter.max_hp))
    libtcod.console_print_rect_ex(window, 0, 7, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Attack: {0}'.format(player.fighter.strength))
    libtcod.console_print_rect_ex(window, 0, 8, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Accuracy: {0}'.format(player.fighter.accuracy))
    libtcod.console_print_rect_ex(window, 0, 9, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Critical Chance: {0}'.format(player.fighter.crit_chance))
    libtcod.console_print_rect_ex(window, 0, 10, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Defense: {0}'.format(player.fighter.defense))
    libtcod.console_print_rect_ex(window, 0, 11, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Dodge: {0}'.format(player.fighter.dodge))
    libtcod.console_print_rect_ex(window, 0, 12, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Ability Power: {0}'.format(player.fighter.ability_power))


    x = map_width // 2 - character_screen_width // 2
    y = map_height // 2 - character_screen_height // 2
    libtcod.console_blit(window, 0, 0, character_screen_width, character_screen_height, 0, x, y, 1.0, 0.7)

def message_box(con, header, width, screen_width, screen_height):
    menu(con, header, [], width, screen_width, screen_height)