from numpy import random as rd
import field_constructor as fld

class jeu(list):
    def __init__(self, niveau):
        self.nom_niveau, self.largeur, self.hauteur, self.nombre_pierre, self.nombre_diamant = self.carac_terrain(niveau)
        for k in range(self.nombre_pierre - 1):
            self.append(fld.Pierre(rd.randint(0, self.largeur),rd.randint(0, self.hauteur)))
        for l in range(self.nombre_diamant - 1):
            self.append(fld.Diamant(rd.randint(0, self.largeur),rd.randint(0, self.hauteur)))


    def __str__(self):
        res = " "
        for i in range(self.largeur - 1):
            for j in range(self.hauteur - 1):
                for k in range(self.nombre_pierre):


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

