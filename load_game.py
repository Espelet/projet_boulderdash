import field_constructor as fld
import keyboard
from numpy import random as rd

class jeu:
    def __init__(self, nv):
        self.ent = []
        self.coords_pour_verif = []
        self.t = fld.terrain(0, 0, nv)
        self.initialisation_terrain(nv)

    def verif_coords(self):
        coords_obj = (rd.randint(1, self.t.lgr - 1), rd.randint(1, self.t.hauteur - 1))
        while coords_obj in self.coords_pour_verif:
            coords_obj = rd.randint(1, self.t.lgr - 1), rd.randint(1, self.t.hauteur - 1)
        self.coords_pour_verif.append(coords_obj)
        return coords_obj

    def __str__(self):
        a = ""
        res = ""
        for i in range(self.t.lgr):
            for jl in range(self.t.hauteur):
                if jl == 0 or jl == self.t.hauteur - 1 or i == 0 or i == self.t.lgr - 1:
                    a = fld.Brique(i, jl, self.t.nv).car()
                else:
                    for obj in self.ent:
                        if obj.coords == (i, jl):
                            a = str(obj.car())
                            break
                        else:
                            a = " "
                res += a + " "
            res += "\n"
        return res

    def initialisation_terrain(self, nv):
        for k in range(self.t.nbr_pierre):
            coords_pierre = self.verif_coords()
            self.ent.append(fld.Pierre(coords_pierre[0], coords_pierre[1], nv))

        # on place les diamants
        for lr in range(self.t.nbr_diamant):
            coords_diams = self.verif_coords()
            self.ent.append(fld.Diamant(coords_diams[0], coords_diams[1], nv))

        # on place la terre
        a = ((self.t.lgr - 2) * (self.t.hauteur - 2)) - len(self.coords_pour_verif)
        for y in range(a - 1):
            coords_terre = self.verif_coords()
            b = rd.randint(0, 11)
            if b <= 8:
                self.ent.append(fld.Terre(coords_terre[0], coords_terre[1], nv))

        # on place le joueur
        coords_joueur = self.verif_coords()
        self.ent.append(fld.Joueur(coords_joueur[0], coords_joueur[1], nv))
        print("Niveau " + self.t.nom_niv)
        print(self)


def carac_terrain(nv):
    nom_niv = "A" + str(nv)
    lgr, hauteur, nbr_pierre, nbr_diamant = 0, 0, 0, 0
    if nv == 1:
        lgr = 10
        hauteur = 10
        nbr_pierre = 15
        nbr_diamant = 5
    elif nv == 2:
        lgr = 15
        hauteur = 15
        nbr_pierre = 25
        nbr_diamant = 10
    return nom_niv, lgr, hauteur, nbr_pierre, nbr_diamant


def mouvement(j):
    joueur = j.ent[-1]
    print(joueur.x, joueur.y)
    while True:
        if keyboard.is_pressed("down arrow"):
            for obj in j.ent:
                if (obj.x == joueur.x + 1 and obj.y == joueur.y):
                    j.ent.remove(obj)
                    joueur.coords = joueur.x + 1, joueur.y
                    break
                else:
                    joueur.coords = joueur.x + 1, joueur.y
            print(j)
            pass
        if keyboard.is_pressed("esc"):
            break


if __name__ == "__main__":
    nv = 2
    j = jeu(nv)
    mouvement(j)
