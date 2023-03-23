from numpy import random as rd
import field_constructor as fld
from pynput import keyboard


class jeu(list):
    def __init__(self, niveau):
        self.niv = niveau
        self.nom_niveau, self.largeur, self.hauteur, self.nombre_pierre, \
        self.nombre_diamant = self.carac_terrain(self.niv)
        for k in range(self.nombre_pierre - 1):
            self.append(fld.Pierre(rd.randint(1, self.largeur - 2), rd.randint(1, self.hauteur - 2), jeu))
        for l in range(self.nombre_diamant - 1):
            self.append(fld.Diamant(rd.randint(1, self.largeur - 2), rd.randint(1, self.hauteur - 2), jeu))

    def __str__(self):
        a = ""
        res = "Niveau " + self.nom_niveau + "\n"
        for i in range(self.largeur):
            for j in range(self.hauteur):
                if j == 0 or j == self.hauteur - 1 or i == 0 or i == self.largeur - 1:
                    a = fld.Brique(i, j, jeu).car()
                else:
                    for obj in self:
                        if obj.coords == (i, j):
                            a = str(obj.car())
                            break
                        else:
                            a = " "
                res += a + " "
            res += "\n"
        return res

    def carac_terrain(self, niveau):
        nom_niveau = "A" + str(niveau)
        if niveau == 1:
            largeur = 10
            hauteur = 10
            nbre_pierre = 15
            nbre_diamant = 5
        elif niveau == 2:
            largeur = 15
            hauteur = 15
            nbre_pierre = 25
            nbre_diamant = 10
        return nom_niveau, largeur, hauteur, nbre_pierre, nbre_diamant


if __name__ == "__main__":
    j = jeu(1)
    print(j)
