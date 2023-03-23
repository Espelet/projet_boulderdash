from load_game import *

class terrain:
    def __init__(self, x, y, jeu):
        self.jeu = jeu
        self.a = 12
        self.__coords = (x, y)

    @property
    def coords(self):
        return self.__coords

    @property
    def x(self):
        return self.__coords[0]

    @property
    def y(self):
        return self.__coords[1]

    @coords.setter
    def coords(self, val):
        x, y = val
        x = max(min(x, self.jeu.lgr), 0)
        y = max(min(y, self.jeu.hauteur), 0)
        self.__coords = (x, y)


class Joueur(terrain):
    def __init__(self, x, y, jeu):
        super().__init__(x, y, jeu)
        self.SeDeplace = True
        self.score = 0
        self.vie = 3


class Diamant(terrain):
    def __init__(self, x, y, jeu):
        super().__init__(x, y, jeu)
        self.val = 1
        self.EstConso = True
        self.EstImmobile = False

    def car(self):
        return "D"


class Pierre(terrain):
    def __init__(self, x, y, jeu):
        super().__init__(x, y, jeu)
        self.Gravite = True
        self.EstImmobile = False
        self.EstConso = False
        self.damage = 1

    def car(self):
        return "P"


class Brique(terrain):
    def __init__(self, x, y, jeu):
        super().__init__(x, y, jeu)
        self.EstImmobile = True
        self.EstConso = False

    def car(self):
        return "B"


class Terre(terrain):
    def __init__(self, x, y, jeu):
        super().__init__(x, y, jeu)
        self.EstImmobile = True
        self.EstConso = True

    def car(self):
        return "T"
