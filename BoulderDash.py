from PyQt5.QtWidgets import QWidget
from math import *
from element_deuxieme_partie import *


class Stase(QWidget):
    def __init__(self):
        super(Stase, self).__init__()
        self.is_menu = False
        self.is_jeu = False

    def update_plateau(self):
        return 15

class BoulderDash(QWidget):
    def __init__(self, width, height, premiere_ligne, parent=None):
        super(BoulderDash, self).__init__(parent)
        self.falling_ent = []
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
        self.n = 0

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
                if y + 800 >= self.height * 80:
                    l = 1600 - self.height * 80
                else:
                    l = 1600 - (y + 800)
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

    def verif_temps(self):
        return True if self.temps_imparti == 0 else False

    def update_plateau(self):
        self.n += 1
        if self.n % 8 == 0:
            self.temps_imparti -= 1
            print(self.temps_imparti)
        if isinstance(self.P.player.element, Sortie):
            print("fin de la partie, bravo !")
            print("score", self.P.score)
            return 0

        if self.P.score/10 >= self.score_a_atteindre and not self.P.is_element(Sortie):
            self.P.point_par_diamant = 15
            self.P.remove_element(self.P.itemAtPosition(self.y_sortie - 1, self.x_sortie - 1).widget())
            self.P.add_element_on_grid(Sortie(self.y_sortie - 1, self.x_sortie - 1, self.P.tiles_element))

        self.falling_ent = self.P.get_falling_elements()
        for el in self.falling_ent:
            t = self.P.apply_gravity(el)
            if t or self.verif_temps():
                print("fin des haricots !")
                print("score", self.P.score)
                self.close()
                return 1


class score(QWidget):
    def __init__(self, temps, diamant_recolte):
        super(score, self).__init__()
        self.temps = temps
        self.nbre_diams = diamant_recolte


stylesheet_jeu = """
    LancerBoulderDash {
        background-image: url('./images/background.png'); 
    }
"""
