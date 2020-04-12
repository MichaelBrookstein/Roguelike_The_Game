import tcod as libtcod

from game_messages import Message
from random_utils import calculate_hit, calculate_crit

class Fighter:
    def __init__(self, hp, defense, accuracy, dodge, strength, crit_chance, ability_power, xp=0):
        self.base_max_hp = hp
        self.hp = hp
        self.base_defense = defense
        self.base_accuracy = accuracy
        self.base_dodge = dodge
        self.base_strength = strength
        self.base_crit_chance = crit_chance
        self.base_ability_power = ability_power
        self.xp = xp

    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0

        return self.base_max_hp + bonus

    @property
    def strength(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.strength_bonus
        else:
            bonus = 0

        return self.base_strength + bonus

    @property
    def crit_chance(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.crit_chance_bonus
        else:
            bonus = 0

        return self.base_crit_chance + bonus

    @property
    def defense(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defense_bonus
        else:
            bonus = 0

        return self.base_defense + bonus

    @property
    def dodge(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.dodge_bonus
        else:
            bonus = 0

        return self.base_dodge + bonus

    @property
    def accuracy(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.accuracy_bonus
        else:
            bonus = 0

        return self.base_accuracy + bonus

    @property
    def ability_power(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.ability_power_bonus
        else:
            bonus = 0

        return self.base_ability_power + bonus

    def take_damage(self, amount):
        results = []

        self.hp -= amount

        if self.hp <= 0:
            results.append({'dead': self.owner, 'xp': self.xp})

        return results

    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def attack(self, target):
        results = []
        hit = calculate_hit(self.accuracy, target.fighter.dodge)

        if self.owner == target:
            damage = self.strength
            results.append({'message': Message('{0} attacks itself for {1} hit points in its madness!'.format(
                self.owner.name.capitalize(), str(damage)), libtcod.lighter_yellow)})
            results.extend(target.fighter.take_damage(damage))

        elif hit:
            crit = calculate_crit(self.crit_chance)
            if crit:
                crit_damage = (self.strength * 2) - target.fighter.defense

                if crit_damage > 0:
                    results.append({'message': Message('Critical hit! {0} attacks {1} for {2} hit points.'.format(
                        self.owner.name.capitalize(), target.name, str(crit_damage)), libtcod.lighter_yellow)})
                    results.extend(target.fighter.take_damage(crit_damage))
                else:
                    results.append({'message': Message('Critical hit! {0} attacks {1} but does no damage.'.format(
                        self.owner.name.capitalize(), target.name), libtcod.white)})

            else:
                damage = self.strength - target.fighter.defense

                if damage > 0:
                    results.append({'message': Message('{0} attacks {1} for {2} hit points.'.format(
                        self.owner.name.capitalize(), target.name, str(damage)), libtcod.white)})
                    results.extend(target.fighter.take_damage(damage))
                else:
                    results.append({'message': Message('{0} attacks {1} but does no damage.'.format(
                        self.owner.name.capitalize(), target.name), libtcod.white)})
        else:
            results.append({'message': Message('{0} attacks {1} but {1} dodges the attack.'.format(
                self.owner.name.capitalize(), target.name), libtcod.lighter_yellow)})

        return results
