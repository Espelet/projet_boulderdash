import random
import sys
from PyQt5.Qt import Qt
from PyQt5.QtCore import QTimer, QTime, QRect
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDesktopWidget
from element_deuxieme_partie import *
import numpy.random as rd
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
    def __init__(self, width, height, nbr_diams, nbr_pierre, nbr_brick, parent=None):
        super(BoulderDash, self).__init__(parent)
        self.setStyleSheet(stylesheet_jeu)
        self.setGeometry(QRect(0, 0, 80 * width, 80 * height))
        self.setFixedSize(80 * width, 80 * height)
        self.P = Plateau(width, height)
        self.P.setContentsMargins(0, 0, 0, 0)
        self.P.setSpacing(0)
        self.P.setHorizontalSpacing(0)
        self.P.setVerticalSpacing(0)
        self.is_jeu = True
        self.is_menu = False
        self.height = height
        self.width = width
        self.nbr_diams = nbr_diams
        self.nbr_pierre = nbr_pierre
        self.nbr_brick = nbr_brick

        self.l_sv, self.t_sv = 0, 0
        self.l, self.t = 0, 0
        self.mvt_plateau = False
        self.timer_mvt_plateau = QTimer()
        self.timer_mvt_plateau.timeout.connect(self.mouvement_plateau)
        self.timer_mvt_plateau.start(10)

        self.setLayout(self.P)
        self.aff = affichage_element(self.P)

    def generate(self):
        for j in range(self.height):
            for i in range(self.width):
                if j == 0 or j == self.height - 1 or i == 0 or i == self.width - 1:
                    self.P.add_element_on_grid(Brique(i, j, self.P.tiles_element))
                else:
                    pass

        self.ajt_element(Diamant, self.nbr_diams)
        self.ajt_element(Brique, self.nbr_brick)
        self.ajt_element(Pierre, self.nbr_pierre)

        nbr_dirt = int(
            ((self.height - 2) * (self.width - 2) - (self.nbr_pierre + self.nbr_brick + self.nbr_diams)) * 0.7)
        self.ajt_element(Terre, nbr_dirt)
        player_pos = (0, 0)
        while self.P.is_used(player_pos[0], player_pos[1]):
            player_pos = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        player = Player(player_pos[0], player_pos[1], self.P.tiles_joueur, None)
        self.P.add_element_on_grid(player)
        self.falling_ent = self.P.get_falling_elements()

    def ajt_element(self, element, n):
        if n == 0:
            return True
        else:
            coords = rd.randint(1, self.width), rd.randint(1, self.height)
            if not self.P.is_used(coords[0], coords[1]):
                self.P.add_element_on_grid(element(coords[0], coords[1], self.P.tiles_element))
                return self.ajt_element(element, n - 1)
            else:
                return self.ajt_element(element, n)

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
            if y > 500:
                if y + 400 >= self.height * 80:
                    l = 800 - self.height * 80
                else:
                    l = 800 - (y + 400)
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

        if not any(isinstance(x.element, Diamant) for x in self.falling_ent) and not self.P.is_element(Sortie):
            self.ajt_element(Sortie, 1)

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
        # self.widget = self.test_generate()
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
                bd = self.test_generate()
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
            print(self.widget)
            #
            # on génère le niveau suivant
            bd = BoulderDash(self.niveau_a2()[0], self.niveau_a2()[1], self.niveau_a2()[2],
                             self.niveau_a2()[3], self.niveau_a2()[4])
            bd.generate()
            self.widget = bd
            self.setCentralWidget(self.widget)
            self.widget.show()
            #
            #
        elif a == 1:  # le joueur est mort et n'a plus de vie à disposition
            print("NUL NUL NUL !")
            self.widget.hide()
            self.widget = None
            self.close()

    def test_generate(self):
        #
        # on fixe les dimensions & l'emplacement de la fenêtre
        self.setFixedSize(800, 800)
        self.setStyleSheet(stylesheet_jeu)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        #
        # on génère le premier niveau
        sys.setrecursionlimit(15000)
        bd = BoulderDash(self.niveau_a1()[0], self.niveau_a1()[1], self.niveau_a1()[2],
                         self.niveau_a1()[3], self.niveau_a1()[4])
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

    def niveau_a1(self):
        width = 10
        height = 10
        nbr_diams = 1
        nbr_pierre = 0
        nbr_brick = 3
        return width, height, nbr_diams, nbr_pierre, nbr_brick

    def niveau_a2(self):
        width = 20
        height = 20
        nbr_diams = 25
        nbr_pierre = 25
        nbr_brick = 10
        return width, height, nbr_diams, nbr_pierre, nbr_brick


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
