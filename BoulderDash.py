from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget
from math import *
from element_deuxieme_partie import *


class Stase(QWidget):
    """Auteur : Chloé
    classe de transition entre chaque changement de niveau"""

    def __init__(self):
        super(Stase, self).__init__()
        self.is_menu = False
        self.is_jeu = False

    def update_plateau(self):
        return 15


class BoulderDash(QWidget):
    """Auteur : Tristan
    classe générant un niveau de jeu"""

    def __init__(self, width, height, premiere_ligne, parent=None):
        """crée le niveau en fonction des paramètres d'entrée"""
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
        self.score = 0
        self.timer_mvt_plateau = QTimer()
        self.timer_mvt_plateau.timeout.connect(self.mouvement_plateau)
        self.timer_mvt_plateau.start(10)
        self.setLayout(self.P)
        self.aff = affichage_element(self.P)
        self.n = 0

    def recup_data_niveau(self):
        """Auteur : Chloé
        récupère les informations permettant la bonne mise en place du niveau"""
        with open("./niveau/A.txt", "r") as f:
            lines = f.readlines()[self.premiere_ligne:]
            self.y_sortie, self.x_sortie = tuple(map(int, lines[1].strip().split(' : ')[1].split(', ')))
            self.score_a_atteindre = int(lines[2].strip().split(' : ')[1])
            self.temps_imparti = int(lines[3].strip().split(' : ')[1])
            f.close()

    def generate(self, fichier_a_lire="./niveau/A.txt"):
        """Auteur : Tristan
        génère le terrain de jeu"""
        self.recup_data_niveau()
        if fichier_a_lire != "./niveau/A.txt":
            self.premiere_ligne = 0
        with open(fichier_a_lire, "r") as f:
            lines = f.readlines()[self.premiere_ligne:]
            if fichier_a_lire != "./niveau/A.txt":
                k = 7
                self.score = int(lines[4].strip().split(' : ')[1]) * 10
                self.temps_imparti = int(lines[5].strip().split(' : ')[1])
            else:
                k = 5
            h = 0
            for i, ligne in enumerate(lines[k:]):
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
        """Auteur : Chloé
        assigne à chaque entrée du joueur une action"""
        if dir == 'down':
            self.score += self.P.move_player(1, 0, 'down')
        elif dir == 'up':
            self.score += self.P.move_player(-1, 0, 'up')
        elif dir == 'left':
            self.score += self.P.move_player(0, -1, 'left')
        elif dir == 'right':
            self.score += self.P.move_player(0, 1, 'right')

    def centrer_vue(self):
        """Auteur : Chloé
        calcule les coordonnées que doit avoir le centre du cadre pour que la vue soit centrée"""
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
        """Auteur : Tristan
        permet de fluidifier le mouvement du cadre lorsque celui-ci se déplace pour centrer la vue"""
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
        """Auteur Tristan :
        vérifie que le temps imparti pour finir le niveau ne s'est pas écoulé"""
        return True if self.temps_imparti == 0 else False

    def update_plateau(self):
        """Auteur : Tristan
        met à jour le plateau toutes les 125 ms"""
        self.n += 1
        if self.n % 8 == 0:
            self.temps_imparti -= 1
        if isinstance(self.P.player.element, Sortie):
            print("fin de la partie, bravo !")
            return 0, self.score + self.temps_imparti

        if self.score / 10 >= self.score_a_atteindre and not self.P.is_element(Sortie):
            self.P.remove_element(self.P.itemAtPosition(self.y_sortie - 1, self.x_sortie - 1).widget())
            self.P.add_element_on_grid(Sortie(self.y_sortie - 1, self.x_sortie - 1, self.P.tiles_element))

        self.falling_ent = self.P.get_falling_elements()
        for el in self.falling_ent:
            t = self.P.apply_gravity(el)
            if t or self.verif_temps():
                print("fin des haricots !")
                self.close()
                return 1, self.score
        return None, self.score


stylesheet_jeu = """
    LancerBoulderDash {
        background-image: url('./images/background.png'); 
    }
"""


class InfoAlEcran(QWidget):
    """Auteur : Chloé
    affiche les informations importantes pour le joueur à l'écran"""
    def __init__(self, parent=None):
        super().__init__(parent)
        # Créer le widget de l'overlay
        self.overlay_label = QLabel(self)
        self.overlay_label.setGeometry(25, 25, 218, 158)  # Position et taille de l'overlay
        self.overlay_label.setStyleSheet("""
                    QLabel {
                        background-image: url('./images/t_diams.png');
                    }
                """)
        self.score_lbl = QLabel(self)
        self.score_lbl.setGeometry(655, 10, 293, 79)
        self.score_lbl.setStyleSheet("""
                            QLabel {
                                background-image: url('./images/t_score.png');
                            }
                        """)
        self.info = QLabel(self)
        self.info.setGeometry(1305, 720, 293, 79)
        self.info.setStyleSheet("""
                                    QLabel {
                                        background-image: url('./images/t_score.png');
                                    }
                                """)
        font = QFont('Arial', 24)
        self.info.setFont(font)
        self.info.setAlignment(QtCore.Qt.AlignRight)
        self.info.setIndent(40)
        self.info.setText("<p style= 'line-height:60%'><font color='white'><br>" + "N : Sauvegarde" +
                             "</font></p>")

        self.vie_lbl = QLabel(self)
        self.vie_lbl.setGeometry(25, 183, 218, 79)
        self.vie_lbl.setStyleSheet("""
                                    QLabel {
                                        background-image: url('./images/t_coeur.png');
                                    }
                                """)
        # Rendre l'overlay transparent
        self.setWindowFlags(
            self.windowFlags() | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # Connecter le signal de déplacement de la fenêtre à la mise à jour de la position de l'overlay
        self.parent().windowMoved.connect(self.updateOverlayPosition)
        self.updateScore(0, 0, 0, 0)

    def paintEvent(self, event):
        # Dessiner le fond transparent de l'overlay
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_Clear)
        painter.fillRect(self.rect(), QtGui.QColor(0, 0, 0, 0))

    def updateOverlayPosition(self):
        # Mettre à jour la position de l'overlay en fonction de la position de la fenêtre principale
        parent_position = self.parent().pos()
        self.move(parent_position.x(), parent_position.y() + 25)  # Définir la nouvelle position de l'overlay

    def updateScore(self, score, temps, s, vie):
        """Auteur : Chloé
        met à jour le score, le nombre de vies, le nombre de diamants récupérés et le temps restant"""
        font = QFont('Arial', 24)
        self.overlay_label.setFont(font)
        self.overlay_label.setAlignment(QtCore.Qt.AlignRight)
        self.overlay_label.setIndent(20)
        self.overlay_label.setText("<p style= 'line-height:60%'><font color='white'><br>" + str(int(score / 10)) +
                                   "</font></p><p style='line-height:115%'><font color='white'><br>" + str(
            int(temps)) + "</font></p>")
        self.score_lbl.setFont(font)
        self.score_lbl.setAlignment(QtCore.Qt.AlignRight)
        self.score_lbl.setIndent(20)
        self.score_lbl.setText("<p style= 'line-height:60%'><font color='white'><br>" + str(s + score) +
                               "</font></p>")

        self.vie_lbl.setFont(font)
        self.vie_lbl.setAlignment(QtCore.Qt.AlignRight)
        self.vie_lbl.setIndent(20)
        self.vie_lbl.setText("<p style= 'line-height:60%'><font color='white'><br>" + str(vie) +
                             "</font></p>")
