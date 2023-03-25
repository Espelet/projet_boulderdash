import sys, os
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QListWidget, QGridLayout, QLabel, QMainWindow
from PyQt5.QtCore import QTimer,QDateTime
import jeu, element


def cut_image_into_tiles(image, rows=12, cols=24) -> dict:
    if isinstance(image, str) and os.path.exists(image):
        image = QPixmap(image)
    elif not isinstance(image, QPixmap):
        raise ValueError("image must be str or QPixmap object")

    # Dim of the tile
    tw = int(image.size().width() / cols)
    th = int(image.size().height() / rows)

    # prepare return value
    tiles = {"width": tw, "height": th}
    for r in range(rows):
        for c in range(cols):
            tile = image.copy(c * tw, r * th, tw, th)
            tiles[(r, c)] = tile

    return tiles


class data_element:
    def __init__(self):
        self.pixmaps = []


class affi_pierre(data_element):
    def __init__(self, tiles):
        super().__init__()
        self.tiles = tiles
        y = 3
        for x in range(4):
            self.pixmaps.append(self.tiles[x, y])


class affi_joueur(data_element):
    def __init__(self, tiles, dir):
        super().__init__()
        self.tiles = tiles
        if dir is None:
            x = 0
            for y in range(2):
                self.pixmaps.append(self.tiles[x, y])
        self.pixmaps += self.pixmaps


class affi_diams(data_element):
    def __init__(self, tiles):
        super().__init__()
        self.tiles = tiles
        y = 4
        for x in range(4):
            self.pixmaps.append(self.tiles[x, y])


class affi_brique(data_element):
    def __init__(self, tiles):
        super().__init__()
        self.tiles = tiles
        y = 0
        for x in range(4):
            self.pixmaps.append(self.tiles[0, y])


class affi_terre(data_element):
    def __init__(self, tiles):
        super().__init__()
        self.tiles = tiles
        y = 1
        for x in range(4):
            self.pixmaps.append(self.tiles[0, y])

class affi_None(data_element):
    def __init__(self, tiles):
        super().__init__()
        self.tiles = tiles
        y = 2
        for x in range(4):
            self.pixmaps.append(self.tiles[0, y])


class affichage_element:
    def __init__(self, lbl):
        self.layout = lbl
        self.current_frame = 0

    def affiche(self):
        for k in range(self.layout.count()):
            item = self.layout.itemAt(k).widget()
            item.setPixmap(item.pixmaps[self.current_frame])
        self.current_frame += 1
        if self.current_frame >= 4:
            self.current_frame = 0

class label_gnr(QLabel):
    def __init__(self, tiles, el):
        super(label_gnr, self).__init__()
        self.pixmaps = []
        self.tiles = tiles

        if isinstance(el, element.Pierre):
            self.pixmaps = affi_pierre(self.tiles).pixmaps
        elif isinstance(el, element.Diamant):
            self.pixmaps = affi_diams(self.tiles).pixmaps
        elif isinstance(el, element.Brique):
            self.pixmaps = affi_brique(self.tiles).pixmaps
        elif isinstance(el, element.Terre):
            self.pixmaps = affi_terre(self.tiles).pixmaps
        elif el is None:
            self.pixmaps = affi_None(self.tiles).pixmaps


class label_joueur(QLabel):
    def __init__(self, tiles, dir):
        super(label_joueur, self).__init__()
        self.tiles = tiles
        self.pixmaps = affi_joueur(self.tiles, dir).pixmaps

class game_zone(QWidget):
    def __init__(self, boulderdash, parent=None):
        super(game_zone, self).__init__(parent)
        self.setWindowTitle('QTimer example')
        self.listFile = QListWidget()
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setHorizontalSpacing(0)
        layout.setVerticalSpacing(0)
        tiles_element = cut_image_into_tiles('./images/Tileset.png', 24, 12)
        tiles_joueur = cut_image_into_tiles('./images/player_new.png', 15, 6)


        self.boulderdash = boulderdash
        for x in range(self.boulderdash.width):
            for y in range(self.boulderdash.height):
                if isinstance(self.boulderdash.grid[x][y], element.Player):
                    lbl = label_joueur(tiles_joueur, None)
                    lbl.setStyleSheet("background-image : url(./images/background.png)")
                else:
                    lbl = label_gnr(tiles_element, self.boulderdash.grid[x][y])
                layout.addWidget(lbl, x, y)


        self.aff = affichage_element(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.display)

        self.setLayout(layout)
        self.resize(self.sizeHint())
        self.timer.start(200)

    def display(self):
        self.aff.affiche()


class MainWindow(QMainWindow):
    def __init__(self, boulderdash):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Boulderdash")
        widget = game_zone(boulderdash)
        self.setCentralWidget(widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    boulderdash = jeu.BoulderDashTest().test_generate()
    jeu = MainWindow(boulderdash)
    jeu.show()
    sys.exit(app.exec_())