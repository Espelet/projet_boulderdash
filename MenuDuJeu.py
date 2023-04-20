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
        return 15, 0

    def write(self):
        asci = self.wrt
        liste_hscore = [[(1, 7), asci["h"]], [(1, 8), asci["s"]], [(1, 9), asci["c"]], [(1, 10), asci["o"]], [(1, 11), asci["r"]],
                        [(1, 12), asci["e"]]]
        for k in range(28):
            for n in range(23):
                lbl = QLabel("lbl")
                lbl.setPixmap(asci[" "])
                self.layout.addWidget(lbl, n, k)
        for a in liste_hscore:
            lbl = QLabel("lbl")
            lbl.setPixmap(a[1])
            self.layout.addWidget(lbl, a[0][0], a[0][1])


stylesheet_menu = """
    LancerBoulderDash {
        background-image: url('./images/homescreen.png'); 
    }
"""
