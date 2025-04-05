from abc import abstractmethod


class Player:

    @abstractmethod
    def select(self, game, row, col):
        pass
