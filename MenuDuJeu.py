from PyQt5.QtWidgets import QWidget
from element_deuxieme_partie import *


class MenuDuJeu(QWidget):
    def __init__(self):
        super(MenuDuJeu, self).__init__()
        self.is_jeu = False
        self.is_menu = True
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setHorizontalSpacing(0)
        self.layout.setVerticalSpacing(0)
        self.wrt = alphabet()
        self.write()
        self.layout.setSizeConstraint(QGridLayout.SizeConstraint.SetFixedSize)
        self.setLayout(self.layout)

    def update_plateau(self):
        """Auteur : Tristan
        C'est une fonction fantôme afin d'unifier toutes les sous-classes de la fenêtre principale de Qt"""
        return 15, 0

    def write(self):
        """Auteur : Trsitan
        permet d'écrire HSCORE sur le menu avec le meilleur score enregistré"""
        asci = self.wrt
        liste_txt = [[(1, 7), asci["h"]], [(1, 8), asci["s"]], [(1, 9), asci["c"]], [(1, 10), asci["o"]],
                        [(1, 11), asci["r"]], [(1, 12), asci["e"]]]
        with open("score_board.txt", "r") as f:
            scores = f.readline().split('\n')[0]   # On lit tous les scores existants et on les stocke dans une liste
        for k, i in enumerate(scores):
            liste_txt.append([(1, 14+k), asci[i]])
        liste_txt += [[(13, 5), asci['a']], [(13, 6), asci['p']], [(13, 7), asci['p']], [(13, 8), asci['u']],
                      [(13, 9), asci['y']], [(13, 10), asci['e']], [(13, 11), asci['r']], [(13, 12), asci[' ']],
                      [(13, 13), asci['s']], [(13, 14), asci['u']], [(13, 15), asci['r']], [(13, 16), asci[' ']],
                      [(13, 17), asci['e']], [(13, 18), asci['n']], [(13, 19), asci['t']], [(13, 20), asci['r']],
                      [(13, 21), asci['e']], [(13, 22), asci['e']], [(14, 4), asci['p']], [(14, 5), asci['o']],
                      [(14, 6), asci['u']], [(14, 7), asci['r']], [(14, 8), asci[' ']], [(14, 9), asci['n']],
                      [(14, 10), asci['o']], [(14, 11), asci['u']], [(14, 12), asci['v']], [(14, 13), asci['e']],
                      [(14, 14), asci['l']], [(14, 15), asci['l']], [(14, 16), asci['e']], [(14, 17), asci[' ']],
                      [(14, 18), asci['p']], [(14, 19), asci['a']], [(14, 20), asci['r']], [(14, 21), asci['t']],
                      [(14, 22), asci['i']], [(14, 23), asci['e']], [(17, 5), asci['a']], [(17, 6), asci['p']], 
                      [(17, 7), asci['p']], [(17, 8), asci['u']], [(17, 9), asci['y']], [(17, 10), asci['e']], 
                      [(17, 11), asci['r']], [(17, 12), asci[' ']], [(17, 13), asci['s']], [(17, 14), asci['u']], 
                      [(17, 15), asci['r']], [(17, 16), asci[' ']], [(17, 17), asci['l']], [(17, 18), asci[' ']],
                      [(17, 19), asci['p']], [(17, 20), asci['o']], [(17, 21), asci['u']], [(17, 22), asci['r']],
                      [(18, 5), asci['c']], [(18, 6), asci['h']], [(18, 7), asci['a']], [(18, 8), asci['r']],
                      [(18, 9), asci['g']], [(18, 10), asci['e']], [(18, 11), asci['r']], [(18, 12), asci[' ']],
                      [(18, 13), asci['s']], [(18, 14), asci['a']], [(18, 15), asci['u']], [(18, 16), asci['v']],
                      [(18, 17), asci['e']], [(18, 18), asci['g']], [(18, 19), asci['a']], [(18, 20), asci['r']],
                      [(18, 21), asci['d']], [(18, 22), asci['e']]]
        for k in range(28):
            for n in range(23):
                lbl = QLabel("lbl")
                lbl.setPixmap(asci[" "])
                self.layout.addWidget(lbl, n, k)
        for a in liste_txt:
            lbl = QLabel("lbl")
            lbl.setPixmap(a[1])
            self.layout.addWidget(lbl, a[0][0], a[0][1])


stylesheet_menu = """
    LancerBoulderDash {
        background-image: url('./images/homescreen.png'); 
    }
"""
