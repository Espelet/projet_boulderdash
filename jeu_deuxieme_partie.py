import sys
from PyQt5.Qt import Qt
from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
from MenuDuJeu import *
from BoulderDash import *


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
        print(int(self.time_el.toString().split(":")[1])*60 + int(self.time_el.toString().split(":")[2]))

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
        print("ok0")
        bd = BoulderDash(ligne, col, premiere_ligne)
        print("ok1")
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    jeu = LancerBoulderDash()
    jeu.show()
    sys.exit(app.exec_())
