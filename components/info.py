import entity

class Information:
    def __init__(self, name):
        self.name = name
        self.description = ''

    def display(self, fighter_component=None):

        if fighter_component is not None:
            curr_hp = fighter_component[0].hp
            max_hp = fighter_component[0].max_hp
        else:
            curr_hp = 0
            max_hp = 0

        if self.name == 'thief':
            self.description = 'At home in the shadows, the thief is adept in dodging around attacks while striking back with devestating accuracy.' \
                               'In a pinch, the thief can temporarily dissolve into the shadows to bypass enemies.'
            return self.description
        elif self.name == 'brute':
            self.description = 'Calloused and bruised, The brute brings raw strength where wisdom may fail. Powerful blows and a weathered physique makes up the arsenal of this inured soul.'
            return self.description
        elif self.name == 'occultist':
            self.description = 'Exiled for forbidden insight, the occultist brings unnatural abilities with him into the depths.' \
                               'The occultist can assault both body and mind but may not fare well in conventional combat.'
            return self.description
        elif self.name == 'risen_corpse':
            self.description = 'A macabre caricature of the once-living, animated by dark energies.\n\n{0}/{1}'.format(curr_hp, max_hp)
            return self.description
        elif self.name == 'cultist':
            self.description = 'Consumed by madness, the cultist devotes their lives to the black cause.\n\n{0}/{1}'.format(curr_hp, max_hp)
            return self.description
        elif self.name == 'unholy_priest':
            self.description = 'They are a unhallowed combination of flesh and cloth. Serving a false god and in return, gifted with dark powers.\n\n{0}/{1}'.format(curr_hp, max_hp)
            return self.description
        elif self.name == 'shadowy_horror':
            self.description = 'Twisted shadows and unending madness, living icon of the false god.\n\n{0}/{1}'.format(curr_hp, max_hp)
            return self.description
        elif self.name == 'ragged_shoes':
            self.description = 'A worn sole and leather wraps. It offers minor comfort and a small boost to dodge and accuracy'
            return self.description
        elif self.name == 'torn_pants':
            self.description = 'Pants made with woolen cloth covered in several patched and unpatched holes. It provides minor protection.'
            return self.description
        elif self.name == 'mystic_hood':
            self.description = 'Smooth fabric sewn into the shape of a hood. It has a faint glow of energy.'
            return self.description
        elif self.name == 'broken_sword':
            self.description = "Rust covers what's left of this half weapon. It's jagged points provide a minor boost in offense."
            return self.description
        elif self.name == 'cultist_cloak':
            self.description = "The fabric is course, heavy, and stained with dark splotches. It provides a boost in defense."
            return self.description
        elif self.name == 'cultist_blade':
            self.description = "The handle is cold unlike the blade; warm to the touch. It grants a boost in offense"
            return self.description
        elif self.name == 'tattered_robe':
            self.description = "The cloth used to be white, except for where it began to sink into it's former wearer. It grants a moderate boost in defense."
            return self.description
        elif self.name == 'corrupted_scripture':
            self.description = "It's pages are covered in an unknown language and vibrates slightly as they turn. It has a moderate glow of energy."
            return self.description
        elif self.name == 'shadowy_hide':
            self.description = "Baffling"
            return self.description
        elif self.name == 'shadowy_appendage':
            self.description = "Appalling"
            return self.description
        elif self.name == 'shadowy_mask':
            self.description = "Alluring"
            return self.description
        elif self.name == 'healing_potion':
            self.description = "Purple liquid splashes around inside a small vessel. This will heal you."
            return self.description
        elif self.name == 'dull_sword':
            self.description = "Blunted and abandoned, but it may yet serve a purpose. It provides a boost in offense."
            return self.description
        elif self.name == 'plain_shirt':
            self.description = "An unremarkable garment but will afford some protection if worn. It provides a minor health boost."
            return self.description
        elif self.name == 'sharpened_sword':
            self.description = "A well-balanced weapon with an impressive edge. It provides a moderate boost in offense."
            return self.description
        elif self.name == 'battered_shield':
            self.description = "It has seen better days, and it will see more still. It provides a boost in defense."
            return self.description
        elif self.name == 'hardened_shield':
            self.description = "The metal surface is uneven but unyielding. It provides a moderate boost in defense."
            return self.description
        elif self.name == 'lost_pages':
            self.description = "The parchment is crumpled and torn with the words shifting between pages. It has a faint glow of energy."
            return self.description
        elif self.name == 'dirty_spectacles':
            self.description = "Streaked with seemingly permanent smudges, these glasses focus your attacks but make it harder to read."
            return self.description
        elif self.name == 'fine_shoes':
            self.description = "An odd luxury made with fine fabric. It provides comfort and a moderate boost in dodge and accuracy."
            return self.description
        elif self.name == 'rough_trousers':
            self.description = "The material is tough, stiff and uncomfortable. It provides a moderate bonus in defense at the cost of agility."
            return self.description
        elif self.name == 'fireball_scroll':
            self.description = "The words glow with fiery power."
            return self.description
        elif self.name == 'confusion_scroll':
            self.description = "The words glow with hypnotic power."
            return self.description
        elif self.name == 'lightning_scroll':
            self.description = "The words glow with crackling power."
            return self.description
        elif self.name == 'lightning_tome':
            self.description = "The pages are filled with crackling knowledge. This will teach you to use lightning: A single target damage ability."
            return self.description
        elif self.name == 'fireball_tome':
            self.description = "The pages are filled with fiery knowledge. This will teach you to use fireball: An area-of-effect damage ability."
            return self.description
        elif self.name == 'confusion_tome':
            self.description = "The pages are filled with hypnotic knowledge. This will teach you to use confusion: A mind-altering target ability."
            return self.description
        elif self.name == 'eldritch_blast_tome':
            self.description = "The pages are filled with forbidden knowledge. This will teach you to use eldritch blast: A ability-power dependent target damage ability."
            return self.description
        elif self.name == 'lightning_tome':
            self.description = "The pages are filled with crackling knowledge. This will teach you the lightning ability"
            return self.description
        elif self.name == 'well_used_dagger':
            self.description = "The steel is worn but not dulled. A cut coin-purse, a picked lock, a slit throat: It is a rogue's only ally."
            return self.description
        elif self.name == 'leather_vest':
            self.description = "The rigid material smells of alcohol and sweat. It has witnessed brawls won and lost but never surrendered."
            return self.description
        elif self.name == 'cursed_manuscript':
            self.description = "The sheets smell faintly of incense and wine. It is memories forgotten for powers realized."
            return self.description

        else:
            self.description = ""
            return self.description
