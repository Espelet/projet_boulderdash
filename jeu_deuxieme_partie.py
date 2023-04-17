import random
import sys
from PyQt5.Qt import Qt
from PyQt5.QtCore import QTimer, QTime, QRect
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDesktopWidget
from element_deuxieme_partie import *
from math import *


class alphabet(dict):
    def __init__(self):
        super(alphabet, self).__init__()
        self.tiles = cut_image_into_tiles('./images/text.png', 12, 16)
        self.ascii = "0123456789 abcdefghijklmnopqrstuvwxyz"
        self.creer_alphabet()
    def creer_alphabet(self):
        k = self.ascii
        for i in range(11):
            self[k[i]] = self.tiles[0, i]
        for i in range(16):
            self[k[i + 11]] = self.tiles[1, i]
        for i in range(10):
            self[k[i + 27]] = self.tiles[2, i]


class BoulderDash(QWidget):
    def __init__(self, width, height, premiere_ligne, parent=None):
        super(BoulderDash, self).__init__(parent)
        self.setStyleSheet(stylesheet_jeu)
        self.setFixedSize(80 * height, 80 * width)
        self.setGeometry(QRect(0, 0, 80 * height, 80 * width))
        self.P = Plateau(width, height)
        self.P.setContentsMargins(0, 0, 0, 0)
        self.P.setSpacing(0)
        self.P.setHorizontalSpacing(0)
        self.P.setVerticalSpacing(0)
        self.is_jeu = True
        self.is_menu = False
        self.height = height
        self.width = width
        self.premiere_ligne = premiere_ligne
        self.x_sortie, self.y_sortie, self.score_a_atteindre, self.temps_imparti = 0, 0, 0, 0
        self.l_sv, self.t_sv = 0, 0
        self.l, self.t = 0, 0
        self.mvt_plateau = False
        self.timer_mvt_plateau = QTimer()
        self.timer_mvt_plateau.timeout.connect(self.mouvement_plateau)
        self.timer_mvt_plateau.start(10)

        self.setLayout(self.P)
        self.aff = affichage_element(self.P)

    def generate(self):
        with open("./niveau/A.txt", "r") as f:
            lines = f.readlines()[self.premiere_ligne:]
            self.y_sortie, self.x_sortie = tuple(map(int, lines[1].strip().split(' : ')[1].split(', ')))
            self.score_a_atteindre = int(lines[2].strip().split(' : ')[1])
            self.temps_imparti = int(lines[3].strip().split(' : ')[1])
            h = 0
            for i, ligne in enumerate(lines[5:]):
                if i > self.width:
                    break
                for k in ligne.strip():
                    if k == "M":
                        self.P.add_element_on_grid(Brique(i, h, self.P.tiles_element))
                    elif k == "D":
                        self.P.add_element_on_grid(Diamant(i, h, self.P.tiles_element))
                    elif k == "P":
                        self.P.add_element_on_grid(Pierre(i, h, self.P.tiles_element))
                    elif k == "J":
                        self.P.add_element_on_grid(Player(i, h, self.P.tiles_joueur, None))
                    elif k == "T":
                        self.P.add_element_on_grid(Terre(i, h, self.P.tiles_element))
                    h += 1
                h = 0
            self.falling_ent = self.P.get_falling_elements()

    def bouge(self, dir):
        if dir == 'down':
            self.P.move_player(1, 0, 'down')
        elif dir == 'up':
            self.P.move_player(-1, 0, 'up')
        elif dir == 'left':
            self.P.move_player(0, -1, 'left')
        elif dir == 'right':
            self.P.move_player(0, 1, 'right')

    def centrer_vue(self):
        l, t = 0, 0
        if self.P.player is None:
            return
        else:
            x = self.P.player.element.x * 80
            y = self.P.player.element.y * 80
            if y > 1000:
                if y + 900 >= self.height * 80:
                    l = 1600 - self.height * 80
                else:
                    l = 1600 - (y + 900)
            if x > 500:
                if x + 400 >= self.width * 80:
                    t = 800 - self.width * 80
                else:
                    t = 800 - (x + 400)
            return l, t

    def mouvement_plateau(self):
        if self.mvt_plateau:
            if self.l_sv == self.l and self.t_sv == self.t:
                self.l_sv = self.l
                self.t_sv = self.t
                self.mvt_plateau = False
            else:
                a = ceil((self.l - self.l_sv) / 8)
                b = ceil((self.t - self.t_sv) / 8)
                self.l_sv += a
                self.t_sv += b
                if abs(a) == 0:
                    self.l_sv = self.l
                if abs(b) == 0:
                    self.t_sv = self.t
                self.setGeometry(QRect(self.l_sv, self.t_sv, 80 * self.width, 80 * self.height))
        else:
            self.l, self.t = self.centrer_vue()
            if self.t_sv != self.t or self.l_sv != self.l:
                self.mvt_plateau = True
            else:
                self.mvt_plateau = False

    def update_plateau(self):
        if isinstance(self.P.player.element, Sortie):
            print("fin de la partie, bravo !")
            print("score", self.P.score)
            return 0

        if self.P.score >= self.score_a_atteindre and not self.P.is_element(Sortie):
            self.P.remove_element(self.P.itemAtPosition(self.y_sortie-1, self.x_sortie - 1).widget())
            self.P.add_element_on_grid(Sortie(self.y_sortie - 1, self.x_sortie - 1, self.P.tiles_element))

        self.falling_ent = self.P.get_falling_elements()
        for el in self.falling_ent:
            t = self.P.apply_gravity(el)
            if t:
                print("fin des haricots !")
                print("score", self.P.score)
                return 1


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
        return 15

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


class LancerBoulderDash(QMainWindow):
    def __init__(self):
        super(LancerBoulderDash, self).__init__()
        self.setWindowTitle('BoulderDash')
        self.widget = self.lancer_menu_du_jeu()
        self.setCentralWidget(self.widget)
        #
        # lancer le minuteur permettant le mise à jour du plateau
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_fin)
        self.n = 0
        self.timer.start(125)
        self.time_el = QTime(0, 0, 0)  # Décompte du temps que le joueur a à disposition pour finir la partie
        #
        #

    def incr_temps(self):
        self.time_el = self.time_el.addSecs(1)
        print(self.time_el.toString("hh:mm:ss"))

    def keyPressEvent(self, event):  # récupérer les entrées clavier du joueur
        if self.widget.is_jeu:
            if event.key() == Qt.Key_S:
                self.widget.bouge('down')

            elif event.key() == Qt.Key_Z:
                self.widget.bouge('up')

            elif event.key() == Qt.Key_Q:
                self.widget.bouge('left')

            elif event.key() == Qt.Key_D:
                self.widget.bouge('right')
        if self.widget.is_menu:
            if event.key() == Qt.Key_Return:
                #
                # on efface le menu de l'écran
                self.widget.hide()
                self.widget = None
                #
                # on crée l'aire de jeu et on l'affiche
                bd = self.genere_niveau(self.niveau_1())
                self.widget = bd
                self.setCentralWidget(self.widget)
                self.widget.show()
                #
                #

    def check_fin(self):
        self.n += 1
        if self.n % 8 == 0:
            self.incr_temps()

        a = self.widget.update_plateau()

        if a == 0:  # le joueur a complété le niveau
            print("Fini !")
            self.widget.hide()
            self.widget = None
            #
            # on génère le niveau suivant
            bd_new = self.genere_niveau(self.niveau_2())
            self.widget = bd_new
            self.setCentralWidget(self.widget)
            self.widget.show()
            #
            #
        elif a == 1:  # le joueur est mort et n'a plus de vie à disposition
            print("NUL NUL NUL !")
            self.widget.hide()
            self.widget = None
            self.close()

    def genere_niveau(self, premiere_ligne):
        #
        # on fixe les dimensions & l'emplacement de la fenêtre
        self.setFixedSize(1600, 800)
        self.setStyleSheet(stylesheet_jeu)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        #
        # on génère le niveau
        with open("./niveau/A.txt", "r") as f:
            ligne_dimension = f.readlines()[premiere_ligne]
            ligne, col = tuple(map(int, ligne_dimension.strip().split(' : ')[1].split(', ')))
        bd = BoulderDash(ligne, col, premiere_ligne)
        bd.generate()
        return bd
        #
        #

    def lancer_menu_du_jeu(self):
        #
        # on fixe les dimensions & l'emplacement de la fenêtre
        self.setFixedSize(1024, 896)
        self.setStyleSheet(stylesheet_menu)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        #
        # on génère le menu
        menu = MenuDuJeu()
        return menu

    def niveau_1(self):
        ligne_a_lire = 0  # premiere ligne du fichier des niveaux à lire correspondant au niveau 1
        return ligne_a_lire

    def niveau_2(self):
        ligne_a_lire = 30  # premiere ligne du fichier des niveaux à lire correspondant au niveau 2
        return ligne_a_lire


stylesheet_jeu = """
    LancerBoulderDash {
        background-image: url('./images/background.png'); 
    }
"""
stylesheet_menu = """
    LancerBoulderDash {
        background-image: url('./images/homescreen.png'); 
    }
"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    jeu = LancerBoulderDash()
    jeu.show()

    sys.exit(app.exec_())
