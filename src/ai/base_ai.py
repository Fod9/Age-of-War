class AIBot:
    def __init__(self, player):
        self.player = player

    def perform_actions(self):
        raise NotImplementedError("This method should be overridden by subclasses")

    def spawn_unit(self):
        raise NotImplementedError("This method should be overridden by subclasses")

    def can_afford(self, unit):
        return self.player.money >= unit.price

    def get_spawn_position(self):
        return self.player.base.get_spawn_position()
