class Tile:
    """
    A tile on a map. It may or may not be blocked, and may or may not block sight.
    """

    def __init__(self, x, y, blocked, block_sight=None):
        self.x = x;
        self.y = y;
        self.blocked = blocked

        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight

        self.explored = False
        self.room = False
        self.hall = False
        self.door = False
