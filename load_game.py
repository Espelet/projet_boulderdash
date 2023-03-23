class jeu(list):
    def __init__(self, niveau):
        nom_niveau, largeur, hauteur, nombre_pierre, nombre_diamant = self.carac_terrain(niveau)

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
