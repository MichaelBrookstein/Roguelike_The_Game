from random import randint


def random_choice_index(chances):
    random_chance = randint(1, sum(chances))

    running_sum = 0
    choice = 0
    for w in chances:
        running_sum += w

        if random_chance <= running_sum:
            return choice
        choice += 1


def random_choice_from_dict(choice_dict):
    choices = list(choice_dict.keys())
    chances = list(choice_dict.values())

    return choices[random_choice_index(chances)]


def from_dungeon_level(table, dungeon_level):
    for (value, level) in reversed(table):
        if dungeon_level >= level:
            return value

    return 0


def calculate_hit(accuracy, dodge):
    chance = accuracy - dodge
    if randint(0, 100) <= chance:
        return True
    else:
        return False


def calculate_crit(crit_chance):
    if randint(0, 100) <= crit_chance:
        return True
    else:
        return False
