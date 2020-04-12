class Item:
    def __init__(self, use_function=None, targeting=False, targeting_message=None, selected=False, **kwargs):
        self.use_function = use_function
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.selected = selected
        self.function_kwargs = kwargs