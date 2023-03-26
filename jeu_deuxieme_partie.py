import random
import sys
import time

from PyQt5 import QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QListWidget, QDesktopWidget
from element_deuxieme_partie import *
import numpy.random as rd
import keyboard


class affichage_element:
    def __init__(self, lbl):
        self.layout = lbl
        self.current_frame = 0

    def affiche(self):
        for k in range(self.layout.count()):
            item = self.layout.itemAt(k).widget()
            try:
                item.setPixmap(item.element.pixmaps[self.current_frame])
            except:
                a = True

        self.current_frame += 1
        if self.current_frame >= 4:
            self.current_frame = 0


class BoulderDash(QWidget):
    def __init__(self, width, height, nbr_diams, nbr_pierre, nbr_brick, parent=None):
        super(BoulderDash, self).__init__(parent)
        self.listFile = QListWidget()
        self.P = Plateau(width, height)
        self.P.setContentsMargins(0, 0, 0, 0)
        self.P.setSpacing(0)
        self.P.setHorizontalSpacing(0)
        self.P.setVerticalSpacing(0)
        self.grid = self.P.grid
        self.layout = self.P
        self.height = height
        self.width = width
        self.nbr_diams = nbr_diams
        self.nbr_pierre = nbr_pierre
        self.nbr_brick = nbr_brick
        self.falling_ent = []
        self.setLayout(self.P)
        self.timer = QTimer()
        self.timer.timeout.connect(self.display)
        self.aff = affichage_element(self.P)

        self.setGrabbing()
        self.timer.start(100)

    def display(self):
        self.aff.affiche()
        self.update_plateau()

    def move_player(self, event):
        if event.event_type == 'down':
            if event.name == 's':
                self.P.move_player(1, 0)

            elif event.name == 'z':
                self.P.move_player(-1, 0)

            elif event.name == 'q':
                self.P.move_player(0, -1)

            elif event.name == 'd':
                self.P.move_player(0, 1)

    def setGrabbing(self):
        self.hook = keyboard.on_press(self.move_player)
        self.showMinimized()

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
        self.setLayout(self.layout)
        self.resize(self.sizeHint())
        qtRectangle = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(cp)
        self.move(qtRectangle.topLeft())

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

    def update_plateau(self):
        if self.P.player is None:
            print("fin de la partie, bravo !")
            print("score", self.P.score)
            self.timer.stop()
            self.shutdown = True

        self.falling_ent = self.P.get_falling_elements()
        if not any(isinstance(x.element, Diamant) for x in self.falling_ent) and not self.P.is_element(Sortie):
            self.ajt_element(Sortie, 1)
        for el in self.falling_ent:
            t = self.P.apply_gravity(el)
            if t:
                print("fin des haricots !")
                print("score", self.P.score)
                self.timer.timeout.disconnect()
                self.timer.stop()


class BoulderDashTest(QMainWindow):

    def __init__(self):
        super(BoulderDashTest, self).__init__()
        self.resize(800, 800)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.setWindowTitle('BoulderDash')
        widget = self.test_generate()
        self.setCentralWidget(widget)

    def test_generate(self):
        sys.setrecursionlimit(15000)
        bd = BoulderDash(self.niveau_a1()[0], self.niveau_a1()[1], self.niveau_a1()[2]
                         , self.niveau_a1()[3], self.niveau_a1()[4])
        bd.generate()
        return bd


    def niveau_a1(self):
        width = 10
        height = 10
        nbr_diams = 1
        nbr_pierre = 1
        nbr_brick = 5
        return width, height, nbr_diams, nbr_pierre, nbr_brick


stylesheet = """
    BoulderDashTest {
        background-image: url('background.png'); 
    }
"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    jeu = BoulderDashTest()
    jeu.show()

    sys.exit(app.exec_())
