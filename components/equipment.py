from equipment_slots import EquipmentSlots


class Equipment:
    def __init__(self, main_hand=None, off_hand=None, upper_body=None, lower_body=None, head=None, feet=None):
        self.main_hand = main_hand
        self.off_hand = off_hand
        self.upper_body = upper_body
        self.lower_body = lower_body
        self.head = head
        self.feet = feet


    @property
    def max_hp_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.max_hp_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.max_hp_bonus

        if self.upper_body and self.upper_body.equippable:
            bonus += self.upper_body.equippable.max_hp_bonus

        if self.lower_body and self.lower_body.equippable:
            bonus += self.lower_body.equippable.max_hp_bonus

        if self.head and self.head.equippable:
            bonus += self.head.equippable.max_hp_bonus

        if self.feet and self.feet.equippable:
            bonus += self.feet.equippable.max_hp_bonus

        return bonus

    @property
    def strength_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.strength_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.strength_bonus

        if self.upper_body and self.upper_body.equippable:
            bonus += self.upper_body.equippable.strength_bonus

        if self.lower_body and self.lower_body.equippable:
            bonus += self.lower_body.equippable.strength_bonus

        if self.head and self.head.equippable:
            bonus += self.head.equippable.strength_bonus

        if self.feet and self.feet.equippable:
            bonus += self.feet.equippable.strength_bonus

        return bonus

    @property
    def crit_chance_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.crit_chance_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.crit_chance_bonus

        if self.upper_body and self.upper_body.equippable:
            bonus += self.upper_body.equippable.crit_chance_bonus

        if self.lower_body and self.lower_body.equippable:
            bonus += self.lower_body.equippable.crit_chance_bonus

        if self.head and self.head.equippable:
            bonus += self.head.equippable.crit_chance_bonus

        if self.feet and self.feet.equippable:
            bonus += self.feet.equippable.crit_chance_bonus

        return bonus

    @property
    def defense_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.defense_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.defense_bonus

        if self.upper_body and self.upper_body.equippable:
            bonus += self.upper_body.equippable.defense_bonus

        if self.lower_body and self.lower_body.equippable:
            bonus += self.lower_body.equippable.defense_bonus

        if self.head and self.head.equippable:
            bonus += self.head.equippable.defense_bonus

        if self.feet and self.feet.equippable:
            bonus += self.feet.equippable.defense_bonus

        return bonus

    @property
    def accuracy_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.accuracy_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.accuracy_bonus

        if self.upper_body and self.upper_body.equippable:
            bonus += self.upper_body.equippable.accuracy_bonus

        if self.lower_body and self.lower_body.equippable:
            bonus += self.lower_body.equippable.accuracy_bonus

        if self.head and self.head.equippable:
            bonus += self.head.equippable.accuracy_bonus

        if self.feet and self.feet.equippable:
            bonus += self.feet.equippable.accuracy_bonus

        return bonus

    @property
    def dodge_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.dodge_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.dodge_bonus

        if self.upper_body and self.upper_body.equippable:
            bonus += self.upper_body.equippable.dodge_bonus

        if self.lower_body and self.lower_body.equippable:
            bonus += self.lower_body.equippable.dodge_bonus

        if self.head and self.head.equippable:
            bonus += self.head.equippable.dodge_bonus

        if self.feet and self.feet.equippable:
            bonus += self.feet.equippable.dodge_bonus

        return bonus

    @property
    def ability_power_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.ability_power_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.ability_power_bonus

        if self.upper_body and self.upper_body.equippable:
            bonus += self.upper_body.equippable.ability_power_bonus

        if self.lower_body and self.lower_body.equippable:
            bonus += self.lower_body.equippable.ability_power_bonus

        if self.head and self.head.equippable:
            bonus += self.head.equippable.ability_power_bonus

        if self.feet and self.feet.equippable:
            bonus += self.feet.equippable.ability_power_bonus

        return bonus

    def toggle_equip(self, equippable_entity):
        results = []

        slot = equippable_entity.equippable.slot

        if slot == EquipmentSlots.MAIN_HAND:
            if self.main_hand == equippable_entity:
                self.main_hand = None
                results.append({'unequipped': equippable_entity})
            else:
                if self.main_hand:
                    results.append({'unequipped': self.main_hand})

                self.main_hand = equippable_entity
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.OFF_HAND:
            if self.off_hand == equippable_entity:
                self.off_hand = None
                results.append({'unequipped': equippable_entity})
            else:
                if self.off_hand:
                    results.append({'unequipped': self.off_hand})

                self.off_hand = equippable_entity
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.UPPER_BODY:
            if self.upper_body == equippable_entity:
                self.upper_body = None
                results.append({'unequipped': equippable_entity})
            else:
                if self.upper_body:
                    results.append({'unequipped': self.upper_body})

                self.upper_body = equippable_entity
                results.append({'unequipped': equippable_entity})

        elif slot == EquipmentSlots.LOWER_BODY:
            if self.lower_body == equippable_entity:
                self.lower_body = None
                results.append({'unequipped': equippable_entity})
            else:
                if self.lower_body:
                    results.append({'unequipped': self.lower_body})

                self.lower_body = equippable_entity
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.HEAD:
            if self.head == equippable_entity:
                self.head = None
                results.append({'unequipped': equippable_entity})
            else:
                if self.head:
                    results.append({'unequipped': self.head})

                self.head = equippable_entity
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.FEET:
            if self.feet == equippable_entity:
                self.feet = None
                results.append({'unequipped': equippable_entity})
            else:
                if self.feet:
                    results.append({'unequipped': self.feet})

                self.feet = equippable_entity
                results.append({'equipped': equippable_entity})

        return results