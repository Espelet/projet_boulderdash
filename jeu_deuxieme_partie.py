import random
import sys
import time
from PyQt5.Qt import Qt
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer, QTime, QRect
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QListWidget, QDesktopWidget
from element_deuxieme_partie import *
import numpy.random as rd
import keyboard


class BoulderDash(QWidget):
    def __init__(self, width, height, nbr_diams, nbr_pierre, nbr_brick, parent=None):
        super(BoulderDash, self).__init__(parent)
        self.setGeometry(QRect(0, 0, 80 * width, 80 * height))
        self.setFixedSize(80 * width, 80 * height)
        self.P = Plateau(width, height)
        self.P.setContentsMargins(0, 0, 0, 0)
        self.P.setSpacing(0)
        self.P.setHorizontalSpacing(0)
        self.P.setVerticalSpacing(0)
        self.is_jeu = True
        self.grid = self.P.grid
        self.layout = self.P
        self.height = height
        self.width = width
        self.nbr_diams = nbr_diams
        self.nbr_pierre = nbr_pierre
        self.nbr_brick = nbr_brick
        self.falling_ent = []
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
            if y > 600:
                if y + 400 >= self.height * 80:
                    l = 800 - self.height * 80
                else:
                    l = 800 - (y + 400)
            if x > 600:
                if x + 400 >= self.width * 80:
                    t = 800 - self.width * 80
                else:
                    t = 800 - (x + 400)
            return l, t

    def update_plateau(self):
        if isinstance(self.P.player.element, Sortie):
            print("fin de la partie, bravo !")
            print("score", self.P.score)
            return 0

        l, t = self.centrer_vue()
        self.setGeometry(QRect(l, t, 80 * self.width, 80 * self.height))

        self.falling_ent = self.P.get_falling_elements()
        if not any(isinstance(x.element, Diamant) for x in self.falling_ent) and not self.P.is_element(Sortie):
            self.ajt_element(Sortie, 1)
        for el in self.falling_ent:
            t = self.P.apply_gravity(el)
            self.aff = affichage_element(self.P)
            if t:
                print("fin des haricots !")
                print("score", self.P.score)
                return 1

class MenuDuJeu(QWidget):
    def __init__(self):
        super(MenuDuJeu, self).__init__()
        # self.is_jeu = False
        # self.is_menu = True
        # self.layout = QGridLayout()
        # self.layout.setContentsMargins(0, 0, 0, 0)
        # self.layout.setSpacing(0)
        # self.layout.setHorizontalSpacing(0)
        # self.layout.setVerticalSpacing(0
        # self.lettres = cut_image_into_tiles('./images/text.png', 12, 16)
        # self.write()
        # self.setLayout(self.layout)

    def write(self):
        liste = [(1, 1), (1, 14), (1, 13), (1, 9), (1, 14), (2, 4), (2, 1)]
        n = 0
        while n <= 6:
            lbl = QLabel("lbl")
            lbl.setPixmap(self.lettres[liste[n]])
            self.layout.addWidget(lbl, 1, n)
            n += 1




class BoulderDashTest(QMainWindow):

    def __init__(self):
        super(BoulderDashTest, self).__init__()
        self.setFixedSize(800, 800)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.setWindowTitle('BoulderDash')
        self.widget = self.test_generate()
        # self.widget = MenuDuJeu()
        self.setCentralWidget(self.widget)
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_fin)
        self.n = 0
        self.timer.start(100)
        self.time_el = QTime(0, 0, 0)


    def incr_temps(self):
        self.time_el = self.time_el.addSecs(1)
        print(self.time_el.toString("hh:mm:ss"))

    def keyPressEvent(self, event):
        if self.widget.is_jeu:
            if event.key() == Qt.Key_S:
                self.widget.bouge('down')

            elif event.key() == Qt.Key_Z:
                self.widget.bouge('up')

            elif event.key() == Qt.Key_Q:
                self.widget.bouge('left')

            elif event.key() == Qt.Key_D:
                self.widget.bouge('right')

    def check_fin(self):
        self.n += 1
        if self.n % 10 == 0:
            self.incr_temps()

        if self.widget.update_plateau() == 0:
            print("Fini !")
            self.widget.hide()
            self.widget = None
            print(self.widget)
            print("ok !")
            bd = BoulderDash(self.niveau_a2()[0], self.niveau_a2()[1], self.niveau_a2()[2]
                             , self.niveau_a2()[3], self.niveau_a2()[4])
            print("Ras")
            bd.generate()
            self.widget = bd
            self.setCentralWidget(self.widget)
            self.widget.show()
        elif self.widget.update_plateau() == 1:
            print("NUL NUL NUL !")
            self.widget.hide()
            self.widget = None
            self.close()


    def test_generate(self):
        sys.setrecursionlimit(15000)
        bd = BoulderDash(self.niveau_a1()[0], self.niveau_a1()[1], self.niveau_a1()[2]
                         , self.niveau_a1()[3], self.niveau_a1()[4])
        bd.generate()
        return bd


    def niveau_a1(self):
        width = 10
        height = 10
        nbr_diams = 10
        nbr_pierre = 5
        nbr_brick = 5
        return width, height, nbr_diams, nbr_pierre, nbr_brick

    def niveau_a2(self):
        width = 20
        height = 20
        nbr_diams = 25
        nbr_pierre = 25
        nbr_brick = 10
        return width, height, nbr_diams, nbr_pierre, nbr_brick


stylesheet = """
    BoulderDashTest {
        background-image: url('./background.png'); 
    }
"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    jeu = BoulderDashTest()
    jeu.show()

    sys.exit(app.exec_())
