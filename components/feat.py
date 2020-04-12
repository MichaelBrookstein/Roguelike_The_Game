class Feat:
    def __init__(self, name=None, cooldown=0, turn_performed=None, turn_ready='Ready!', feat_function=None, targeting=False, targeting_message=None, **kwargs):
        self.name = name
        self.cooldown = cooldown
        self.turn_performed = turn_performed
        self.turn_ready = turn_ready
        self.feat_function = feat_function
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.function_kwargs = kwargs