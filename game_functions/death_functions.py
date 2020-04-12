import tcod as libtcod

from game_messages import Message

from game_functions.render_functions import RenderOrder
from game_states import GameStates
from random import randint, choice

def kill_player(player):
    player.char = '%'
    player.color = libtcod.dark_red

    return Message('You died!', libtcod.red), GameStates.PLAYER_DEAD


def kill_monster(monster):
    loot = None
    death_message = Message('{0} is dead!'.format(monster.name.capitalize()), libtcod.red)

    if len(monster.inventory.items) != 0:
        randdrop = randint(0, 100)
        if randdrop <= 20:
            loot = choice(monster.inventory.items)

    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = ('{0} remains'.format(monster.name))
    monster.render_order = RenderOrder.CORPSE



    return death_message, loot