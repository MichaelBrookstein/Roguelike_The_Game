import tcod as libtcod
from random import randint

from game_messages import Message

class BasicMonster:
    def take_turn(self, target, fov_map, game_map, entities, game_turn_counter):
        results = []

        monster = self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

            if monster.distance_to(target) >= 2:
                monster.move_astar(target, entities, game_map)

            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)


        return results

class AbilityMonster:
    def take_turn(self, target, fov_map, game_map, entities, game_turn_counter):
        results = []
        player = target
        monster = self.owner

        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
            target = target
            if monster.distance_to(target) >= 2 and monster.abilities is not None:
                for feat in monster.abilities.feats:
                    if feat.turn_performed is None or (game_turn_counter - feat.turn_performed > feat.cooldown):
                        results.extend(monster.abilities.perform(feat, turn_performed=game_turn_counter, target=target,
                                                        fov_map=fov_map, ability_power=monster.fighter.ability_power))
            else:
                for entity in entities:
                    if entity not in ['thief', 'brute', 'occultist'] and monster.distance_to(entity) < 20:
                        target = entity
                if game_turn_counter % 2 == 0:
                    if monster.distance_to(target) > 2:
                        monster.move_astar(target, entities, game_map)
                    else:
                        target = player
                        attack_results = monster.fighter.attack(target)
                        results.extend(attack_results)

        return results

class ConfusedMonster:
    def __init__(self, previous_ai, number_of_turns, fade):
        self.previous_ai = previous_ai
        self.number_of_turns = number_of_turns
        self.fade = fade

    def take_turn(self, target, fov_map, game_map, entities, game_turn_counter):
        results = []

        if self.number_of_turns > 0:
            if self.fade:
                self.owner.blocks = False

            random_x = self.owner.x + randint(0, 2) - 1
            random_y = self.owner.y + randint(0, 2) - 1

            if random_x != self.owner.x and random_y != self.owner.y:
                self.owner.move_towards(random_x, random_y, game_map, entities)

            self.number_of_turns -= 1
        else:
            self.owner.ai = self.previous_ai
            if self.fade:
                self.owner.blocks = True
            else:
                results.append({'message': Message('The {0} is no longer confused!'.format(self.owner.name), libtcod.red)})

        return results

class InsaneMonster:
    def __init__(self, previous_ai, number_of_turns, target):
        self.previous_ai = previous_ai
        self.number_of_turns = number_of_turns
        self.target = target

    def take_turn(self, target, fov_map, game_map, entities, game_turn_counter):
        results = []
        monster = self.owner

        if self.number_of_turns > 0:

            if self.target.fighter is not None:
                if monster.distance_to(self.target) >= 2:
                    monster.move_astar(self.target, entities, game_map)

                elif self.target.fighter.hp > 0:
                    attack_results = monster.fighter.attack(self.target)
                    results.extend(attack_results)

                self.number_of_turns -= 1
            else:
                self.owner.ai = self.previous_ai
                results.append(
                    {'message': Message("The {0} has killed its prey; their bloodlust subsides.".format(self.owner.name), libtcod.red)})

        else:
            self.owner.ai = self.previous_ai
            results.append({'message': Message('The {0} is no longer in a frenzy.'.format(self.owner.name), libtcod.red)})

        return results