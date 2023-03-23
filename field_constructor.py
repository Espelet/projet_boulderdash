from load_game import *


class terrain(jeu):
    def __init__(self, x, y):
        self.a = 12
        self.x = x
        self.y = y


class Joueur(terrain):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.SeDeplace = True
        self.score = 0
        self.vie = 3


class Diamant(terrain):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.val = 1
        self.EstConso = True
        self.EstImmobile = True


class Pierre(terrain):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.Gravite = True
        self.EstImmobile = False
        self.EstConso = False
        self.damage = 1


class Brique(terrain):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.EstImmobile = True
        self.EstConso = False


class Terre(terrain):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.EstImmobile = True
        self.EstConso = True
