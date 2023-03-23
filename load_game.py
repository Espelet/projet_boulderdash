from numpy import random as rd
import field_constructor as fld
from pynput import keyboard


def carac_terrain(niv):
    nom_niv = "A" + str(niv)
    lgr, hauteur, nbr_pierre, nbr_diamant = 0, 0, 0, 0
    if niv == 1:
        lgr = 10
        hauteur = 10
        nbr_pierre = 15
        nbr_diamant = 5
    elif niv == 2:
        lgr = 15
        hauteur = 15
        nbr_pierre = 25
        nbr_diamant = 10
    return nom_niv, lgr, hauteur, nbr_pierre, nbr_diamant


class jeu(list):
    def __init__(self, niv):
        super().__init__()
        self.niv = niv
        self.nom_niv, self.lgr, self.hauteur, self.nbr_pierre, self.nbr_diamant = carac_terrain(self.niv)
        self.coords = []

        for k in range(self.nbr_pierre):
            coords_pierre = self.verif_coords()
            self.append(fld.Pierre(coords_pierre[0], coords_pierre[1], jeu))

        for lr in range(self.nbr_diamant):
            coords_diams = self.verif_coords()
            self.append(fld.Diamant(coords_diams[0], coords_diams[1], jeu))

        for y in range((((self.lgr - 2) * (self.hauteur - 2))) - len(self.coords)):
            coords_terre = self.verif_coords()
            a = rd.randint(0, 10)
            if a >= 8:
                self.append(fld.Terre(coords_terre[0], coords_terre[1], jeu))


    def __str__(self):
        a = ""
        res = "Nivea " + self.nom_niv + "\n"
        for i in range(self.lgr):
            for jl in range(self.hauteur):
                if jl == 0 or jl == self.hauteur - 1 or i == 0 or i == self.lgr - 1:
                    a = fld.Brique(i, jl, jeu).car()
                else:
                    for obj in self:
                        if obj.coords == (i, jl):
                            a = str(obj.car())
                            break
                        else:
                            a = " "
                res += a + " "
            res += "\n"
        return res

    def verif_coords(self):
        coords_obj = (rd.randint(1, self.lgr - 2), rd.randint(1, self.hauteur - 2))
        while coords_obj in self.coords:
            coords_obj = rd.randint(1, self.lgr - 2), rd.randint(1, self.hauteur - 2)
        self.coords.append(coords_obj)
        return coords_obj


if __name__ == "__main__":
    j = jeu(1)
    print(j)
