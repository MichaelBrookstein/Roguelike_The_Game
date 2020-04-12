import random

import tcod as libtcod

from game_messages import Message
from components.ai import ConfusedMonster, InsaneMonster


def cast_lightning_feat(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    ability_power = kwargs.get('ability_power')
    maximum_range = kwargs.get('maximum_range')


    results = []

    target = None
    closest_distance = maximum_range + 1

    for entity in entities:
        if entity.fighter and entity != caster and libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
            distance = caster.distance_to(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        results.append({'performed': True, 'target': target, 'message': Message('A lighting bolt strikes the {0} with a loud thunder! The damage is {1}'.format(target.name, damage + ability_power))})
        results.extend(target.fighter.take_damage(damage + ability_power))
    else:
        results.append({'performed': False, 'target': None, 'message': Message('No enemy is close enough to strike.', libtcod.red)})

    return results

def cast_shadow_vanish_feat(*args, **kwargs):
    entities = kwargs.get('entities')
    duration = kwargs.get('duration')
    ability_power = kwargs.get('ability_power')

    results = []

    for entity in entities:
        if entity.ai:
            confused_ai = ConfusedMonster(entity.ai, duration + ability_power, fade=True)

            confused_ai.owner = entity
            entity.ai = confused_ai

    results.append({'performed': True, 'message': Message('You fade into the shadows for {0} turns.'.format(duration + ability_power), libtcod.black)})

    return results

def cast_insanity_feat(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    duration = kwargs.get('duration')
    ability_power = kwargs.get('ability_power')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []
    target_list = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'performed': False, 'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
        return results


    for entity in entities:

        if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
            target_list.append(entity)

        if entity.x == target_x and entity.y == target_y and entity.ai:

            target = random.choice(target_list)

            insane_ai = InsaneMonster(entity.ai, duration + ability_power, target)

            insane_ai.owner = entity
            entity.ai = insane_ai

            results.append({'performed': True, 'message': Message('The eyes of the {0} fill with rage!'.format(entity.name), libtcod.light_green)})

            break
    else:
        results.append({'performed': False, 'message': Message('There is no targetable enemy at that location.', libtcod.yellow)})

    return results

def cast_unholy_bolt_feat(*args, **kwargs):
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    ability_power = kwargs.get('ability_power')
    target = kwargs.get('target')

    results = []

    if libtcod.map_is_in_fov(fov_map, target.x, target.y):
        results.append({'performed': True, 'target': target, 'message': Message('Eldritch energy strikes {0}! The damage is {1}'.format(target.name, damage + ability_power))})
        results.extend(target.fighter.take_damage(damage + ability_power))

    return results

def cast_fireball_feat(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    radius = kwargs.get('radius')
    ability_power = kwargs.get('ability_power')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'performed': False, 'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
        return results

    results.append({'performed': True, 'message': Message('The fireball explodes, burning everything within {0} tiles!'.format(radius), libtcod.orange)})

    for entity in entities:
        if entity.distance(target_x, target_y) <= (radius + ability_power) and entity.fighter:
            results.append({'message': Message('The {0} gets burned for {1} hit points.'.format(entity.name, damage + ability_power), libtcod.orange)})
            results.extend(entity.fighter.take_damage(damage + ability_power))

    return results

def cast_confusion_feat(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    duration = kwargs.get('duration')
    ability_power = kwargs.get('ability_power')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'performed': False, 'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            confused_ai = ConfusedMonster(entity.ai, duration + ability_power, fade=False)

            confused_ai.owner = entity
            entity.ai = confused_ai

            results.append({'performed': True, 'message': Message('The eyes of the {0} look vacant, as they start to stumble around!'.format(entity.name), libtcod.light_green)})

            break
    else:
        results.append({'performed': False, 'message': Message('There is no targetable enemy at that location.', libtcod.yellow)})

    return results

def cast_eldritch_blast_feat(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    ability_power = kwargs.get('ability_power')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'performed': False, 'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y:
            results.append({'performed': True, 'message': Message('The {0} gets blasted for {1} hit points.'.format(entity.name, damage + (2*ability_power)), libtcod.orange)})
            results.extend(entity.fighter.take_damage(damage + (2*ability_power)))

    else:
        results.append({'performed': False, 'message': Message('There is no targetable enemy at that location.', libtcod.yellow)})

    return results
