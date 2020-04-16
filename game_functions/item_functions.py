import tcod as libtcod

from game_functions.ability_functions import cast_fireball_feat, cast_confusion_feat, cast_eldritch_blast_feat, \
    cast_lightning_feat
from game_messages import Message

from components.ai import ConfusedMonster
from components.feat import Feat

def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'consumed': False, 'message': Message('You are already at full health.', libtcod.yellow)})
    else:
        entity.fighter.heal(amount)
        results.append({'consumed': True, 'message': Message('Your wounds start to feel better!', libtcod.green)})

    return results

def junk(*args, **kwargs):
    entity = args[0]

    results = []

    results.append({'consumed': True, 'message': Message('You discard the trash.', libtcod.gray)})

    return results

def cast_lightning(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
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
        results.append({'consumed': True, 'target': target, 'message': Message('A lighting bolt strikes the {0} with a loud thunder! The damage is {1}'.format(target.name, damage))})
        results.extend(target.fighter.take_damage(damage))
    else:
        results.append({'consumed': False, 'target': None, 'message': Message('No enemy is close enough to strike.', libtcod.red)})

    return results

def cast_fireball(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
        return results

    results.append({'consumed': True, 'message': Message('The fireball explodes, burning everything within {0} tiles!'.format(radius), libtcod.orange)})

    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.fighter:
            results.append({'message': Message('The {0} gets burned for {1} hit points.'.format(entity.name, damage), libtcod.orange)})
            results.extend(entity.fighter.take_damage(damage))

    return results

def cast_confuse(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            confused_ai = ConfusedMonster(entity.ai, 10, fade=False)

            confused_ai.owner = entity
            entity.ai = confused_ai

            results.append({'consumed': True, 'message': Message('The eyes of the {0} look vacant, as they start to stumble around!'.format(entity.name), libtcod.light_green)})

            break
    else:
        results.append({'consumed': False, 'message': Message('There is no targetable enemy at that location.', libtcod.yellow)})

    return results

def add_fireball(*args, **kwargs):
    player = args[0]
    results = []
    known = False

    for feat in player.abilities.feats:
        if feat.name == 'Fireball':
            results.append({'consumed': False, 'message': Message('You already know that Ability!')})
            known = True
    if not known:
        add_results = player.abilities.add_feat([Feat(name='Fireball', cooldown=20, feat_function=cast_fireball_feat, targeting=True, targeting_message=Message(
                        'Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan),
                                                      damage=25, radius=3)])

        results.append(add_results[0])

    return results

def add_confusion(*args, **kwargs):
    player = args[0]
    results = []
    known = False

    for feat in player.abilities.feats:
        if feat.name == 'Confusion':
            results.append({'consumed': False, 'message': Message('You already know that Ability!')})
            known = True
    if not known:
        add_results = player.abilities.add_feat([Feat(name="Confusion", cooldown=5, feat_function=cast_confusion_feat, duration=3, targeting=True, targeting_message=Message(
                        'Left-click an enemy to confuse it, or right-click to cancel.', libtcod.light_cyan))])

        results.append(add_results[0])

    return results


def add_eldritch_blast(*args, **kwargs):
    player = args[0]
    results = []
    known = False

    for feat in player.abilities.feats:
        if feat.name == 'Eldritch Blast':
            results.append({'consumed': False, 'message': Message('You already know that Ability!')})
            known = True
    if not known:
        add_results = player.abilities.add_feat([Feat(name="Eldritch Blast", cooldown=10, feat_function=cast_eldritch_blast_feat, damage=5, targeting=True, targeting_message=Message(
                        'Left-click an enemy to blast it, or right-click to cancel.', libtcod.light_cyan))])

        results.append(add_results[0])

    return results

def add_lightning(*args, **kwargs):
    player = args[0]
    results = []
    known = False

    for feat in player.abilities.feats:
        if feat.name == 'Lightning Bolt':
            results.append({'consumed': False, 'message': Message('You already know that Ability!')})
            known = True
    if not known:
        add_results = player.abilities.add_feat([Feat(name="Lightning Bolt", cooldown=10, damage=15, feat_function=cast_lightning_feat)])

        results.append(add_results[0])

    return results



