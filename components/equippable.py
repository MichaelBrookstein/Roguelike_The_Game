class Equippable:
    def __init__(self, slot, strength_bonus=0, crit_chance_bonus=0, defense_bonus=0, max_hp_bonus=0, accuracy_bonus=0, dodge_bonus=0, ability_power_bonus=0):
        self.slot = slot
        self.strength_bonus = strength_bonus
        self.crit_chance_bonus = crit_chance_bonus
        self.defense_bonus = defense_bonus
        self.max_hp_bonus = max_hp_bonus
        self.accuracy_bonus = accuracy_bonus
        self.dodge_bonus = dodge_bonus
        self.ability_power_bonus = ability_power_bonus
