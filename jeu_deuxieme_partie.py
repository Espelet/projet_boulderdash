import sys, os, time
from PyQt5.Qt import Qt
from PyQt5.QtCore import QTime, QMutex
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
from MenuDuJeu import *
from BoulderDash import *


class LancerBoulderDash(QMainWindow):
    """classe principale générant l'IHM"""
    def __init__(self):
        super(LancerBoulderDash, self).__init__()
        self.setWindowTitle('BoulderDash')
        self.widget = self.lancer_menu_du_jeu()
        self.type_widget = "menu"
        self.setCentralWidget(self.widget)
        #
        # lancer le minuteur permettant le mise à jour du plateau
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_fin)
        self.n = 0
        self.vie = 0
        self.s = 0
        self.timer.start(125)
        self.niveau_actuel = None
        self._mutex = QMutex()
        #
        #

    def keyPressEvent(self, event):
        """récupère les entrées clavier du joueur"""
        if self.type_widget == "jeu":
            if event.key() == Qt.Key_S:
                self.widget.bouge('down')
            elif event.key() == Qt.Key_Z:
                self.widget.bouge('up')
            elif event.key() == Qt.Key_Q:
                self.widget.bouge('left')
            elif event.key() == Qt.Key_D:
                self.widget.bouge('right')
            elif event.key() == Qt.Key_Escape:
                self.changement_de_plateau(self.niveau_actuel)
            elif event.key() == Qt.Key_N:
                self.sauvegarde()
            elif event.key() == Qt.Key_L:
                self.load_niveau()
        elif self.type_widget == "menu":
            if event.key() == Qt.Key_Return:
                #
                # on crée l'aire de jeu et on l'affiche
                self.niveau_actuel = self.niveau_1()
                self.vie = 3
                self.changement_de_plateau(self.niveau_actuel)
                #
                #

    def check_fin(self):
        """vérifie l'état actuel de la partie en cours"""
        a, pt = self.widget.update_plateau()
        if a == 1:  # le joueur est mort
            self.vie -= 1
            if self.vie == 0:
                print("NUL NUL NUL !")
                print("score : ", self.s)
                self.close()
            if self.vie > 0:
                print("Vie restante : ", self.vie)
                print("score : ", self.s)
                self.changement_de_plateau(self.niveau_actuel)

        elif a == 0:  # le joueur a complété le niveau
            print("Fini !")
            self.s += pt
            print("score : ", self.s)
            #
            # on génère le niveau suivant
            self.niveau_actuel = self.niveau_2()
            self.changement_de_plateau(self.niveau_actuel)
            #
            #

    def sauvegarde(self):
        """permet de sauvegarder un niveau"""
        list_of_files = os.listdir('./sauv')
        full_path = ["./sauv/{0}".format(x) for x in list_of_files]
        if len(list_of_files) == 5:
            oldest_file = min(full_path, key=os.path.getctime)
            os.remove(oldest_file)

        nom_fichier = "./sauv/sauv_" + time.strftime("%Y%m%d-%H%M%S")+ ".txt"
        res = ""
        res += "niveau : " + str(self.niveau_actuel) + "\n"
        res += "score : " + str(self.s + self.widget.score) + "\n"
        res += "temps restant : " + str(self.widget.temps_imparti) + "\n\n"
        with open(nom_fichier, "w") as f:
            for k in self.widget.P.grid:
                for i in k:
                    if i is None:
                        res += " "
                    elif isinstance(i.element, Diamant):
                        res += "D"
                    elif isinstance(i.element, Pierre):
                        res += "P"
                    elif isinstance(i.element, Terre):
                        res += "T"
                    elif isinstance(i.element, Brique):
                        res += "M"
                    elif isinstance(i.element, Player):
                        res += "J"
                res += "\n"
            f.write(res)
        print("avancement actuel sauvegardé !")

    def changement_de_plateau(self, niveau):
        """permet de changer le niveau de jeu lors d'un passage à un niveay + difficile"""
        self.widget = Stase()
        self.type_widget = "jeu"
        bd = self.genere_niveau(niveau)
        self.widget = bd
        self.setCentralWidget(self.widget)
        self.widget.show()

    def load_niveau(self):
        """charge un niveau à partir d'une sauvegarde"""
        self.widget.close()
        self.widget = Stase()
        self.type_widget = "jeu"
        list_of_files = os.listdir('./sauv')
        full_path = ["./sauv/{0}".format(x) for x in list_of_files]
        oldest_file = min(full_path, key=os.path.getctime)
        with open(oldest_file, "r") as f:
            premiere_ligne = int(f.readlines()[0].strip().split(' : ')[1])
            f.close()
        print('ras')
        self.niveau_actuel = premiere_ligne
        bd = self.genere_niveau(premiere_ligne, is_sauv=True, sauv=oldest_file)
        print('ras')
        self.widget = bd
        self.setCentralWidget(self.widget)
        self.widget.show()
        print("derniere sauvegarde loadée !")

    def genere_niveau(self, premiere_ligne, is_sauv=False, sauv=""):
        """génère le plateau de jeu"""
        #
        # on fixe les dimensions & l'emplacement de la fenêtre
        self.setFixedSize(1600, 800)
        self.setStyleSheet(stylesheet_jeu)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        if is_sauv:
            #
            # on génère le niveau
            with open("./niveau/A.txt", "r") as g:
                ligne_dimension = g.readlines()[premiere_ligne]
                print(ligne_dimension)
                ligne, col = tuple(map(int, ligne_dimension.strip().split(' : ')[1].split(', ')))
                g.close()
            bd = BoulderDash(ligne, col, premiere_ligne)
            bd.generate(sauv)
            return bd
            #
            #
        else:
            with open("./niveau/A.txt", "r") as f:
                ligne_dimension = f.readlines()[premiere_ligne]
                ligne, col = tuple(map(int, ligne_dimension.strip().split(' : ')[1].split(', ')))
                f.close()
            bd = BoulderDash(ligne, col, premiere_ligne)
            bd.generate()
            return bd
            #
            #

    def lancer_menu_du_jeu(self):
        """lance le menu du jeu au démarrage"""
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
        """donne la première ligne du fichier des niveaux à lire pour générer le premier niveau"""
        ligne_a_lire = 0  # premiere ligne du fichier des niveaux à lire correspondant au niveau 1
        return ligne_a_lire

    def niveau_2(self):
        """donne la première ligne du fichier des niveaux à lire pour générer le deuxième niveau"""
        ligne_a_lire = 30  # premiere ligne du fichier des niveaux à lire correspondant au niveau 2
        return ligne_a_lire


if __name__ == "__main__":
    app = QApplication(sys.argv) # crée l'application de base Qt
    jeu = LancerBoulderDash() # génère la fenêtre IHM
    jeu.show() # affiche cette fenêtre
    sys.exit(app.exec_()) # quitte le programme
