import sys, os
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QListWidget, QGridLayout, QLabel, QMainWindow
from PyQt5.QtCore import QTimer,QDateTime


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



class affi_diams(data_element):
    def __init__(self, tiles):
        super().__init__()
        self.tiles = tiles
        y = 4
        for x in range(4):
            self.pixmaps.append(self.tiles[x, y])



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

        if el == "P":
            self.pixmaps = affi_pierre(self.tiles).pixmaps
        elif el == "D":
            self.pixmaps = affi_diams(self.tiles).pixmaps


class game_zone(QWidget):
    def __init__(self, parent=None):
        super(game_zone, self).__init__(parent)
        self.setWindowTitle('QTimer example')
        self.listFile = QListWidget()
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setHorizontalSpacing(0)
        layout.setVerticalSpacing(0)
        tiles = cut_image_into_tiles('./images/Tileset.png', 24, 12)


        for k in range(40):
            lbl = label_gnr(tiles, "P")
            layout.addWidget(lbl, 0, k)
        for i in range(40):
            lbl = label_gnr(tiles, "D")
            layout.addWidget(lbl, 1, i)

        self.aff = affichage_element(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)

        self.setLayout(layout)
        self.resize(self.sizeHint())
        self.timer.start(333)

    def showTime(self):
        self.aff.affiche()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Boulderdash")
        widget = game_zone()
        self.setCentralWidget(widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    jeu = MainWindow()
    jeu.show()
    sys.exit(app.exec_())