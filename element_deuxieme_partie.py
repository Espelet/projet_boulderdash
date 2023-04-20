import os
from PyQt5.QtCore import QTimer, QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGridLayout, QLabel


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


class Element:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.__pixmaps = []

    @property
    def pixmaps(self):
        return self.__pixmaps

    @pixmaps.setter
    def pixmaps(self, val):
        self.__pixmaps = val


class Brique(Element):
    def __init__(self, x, y, tiles):
        super().__init__(x, y)
        self.is_gravity_affected = False
        self.is_pushable = False
        self.is_consumable = False
        self.is_Falling = False
        self.tiles = tiles
        y = 0
        for x in range(4):
            self.pixmaps.append(self.tiles[0, y])


class Sortie(Element):
    def __init__(self, x, y, tiles):
        super().__init__(x, y)
        self.is_gravity_affected = False
        self.is_pushable = False
        self.is_consumable = False
        self.is_Falling = False
        self.tiles = tiles
        y = 6
        for x in range(4):
            self.pixmaps.append(self.tiles[x, y])


class Player(Element):
    def __init__(self, x, y, tiles, dir):
        super().__init__(x, y)
        self.is_gravity_affected = False
        self.is_pushable = False
        self.is_consumable = False
        self.is_Falling = False
        self.tiles = tiles
        self.dir = dir
        self.anim()

    def anim(self):
        self.pixmaps = []
        if self.dir is None:
            x = 0
            for y in range(2):
                self.pixmaps.append(self.tiles[x, y])
                self.pixmaps.append(self.tiles[x, y])
        elif self.dir == "down":
            x = 4
            for y in range(4):
                self.pixmaps.append(self.tiles[x, y])
        elif self.dir == "up":
            x = 2
            for y in range(4):
                self.pixmaps.append(self.tiles[x, y])
        elif self.dir == "left":
            x = 1
            for y in range(3):
                self.pixmaps.append(self.tiles[x, y])
            self.pixmaps.append(self.tiles[5, 3])
        elif self.dir == "right":
            x = 3
            for y in range(3):
                self.pixmaps.append(self.tiles[x, y])
            self.pixmaps.append(self.tiles[5, 1])
        return self.pixmaps


class Diamant(Element):
    def __init__(self, x, y, tiles):
        super().__init__(x, y)
        self.is_gravity_affected = True
        self.is_pushable = False
        self.is_consumable = True
        self.is_Falling = False
        self.tiles = tiles
        y = 4
        for x in range(4):
            self.pixmaps.append(self.tiles[x, y])


class Pierre(Element):
    def __init__(self, x, y, tiles):
        super().__init__(x, y)
        self.is_gravity_affected = True
        self.is_pushable = True
        self.is_consumable = False
        self.is_Falling = False
        self.tiles = tiles
        y = 3
        for x in range(4):
            self.pixmaps.append(self.tiles[x, y])


class Terre(Element):
    def __init__(self, x, y, tiles):
        super().__init__(x, y)
        self.is_gravity_affected = False
        self.is_pushable = False
        self.is_consumable = True
        self.is_Falling = False
        self.tiles = tiles
        y = 1
        for x in range(4):
            self.pixmaps.append(self.tiles[0, y])


class label_gnr(QLabel):
    def __init__(self, tiles, el):
        super(label_gnr, self).__init__()
        self.tiles = tiles
        self.element = el
        self.pixmaps = self.element.pixmaps


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


class Plateau(QGridLayout):
    def __init__(self, width, height, parent=None):
        super(Plateau, self).__init__(parent)
        self.tiles_element = cut_image_into_tiles('./images/Tileset.png', 24, 12)
        self.tiles_joueur = cut_image_into_tiles('./images/player_new.png', 15, 6)
        self.width = width
        self.height = height
        self.setGeometry(QRect(0, 0, 80 * self.height, 80 * self.width))
        self.grid = [[None for _ in range(self.height)] for _ in range(self.width)]
        self.player = None
        self.point_par_diamant = 10
        self.timer = QTimer()
        self.timer.timeout.connect(self.display)
        self.aff = affichage_element(self)
        self.timer.start(100)

    def display(self):
        self.aff.affiche()

    def is_used(self, x, y):
        return self.grid[x][y] is not None

    def add_element_on_grid(self, element):
        if isinstance(element, Player):
            lbl = label_gnr(self.tiles_joueur, element)
            self.player = lbl
        lbl = label_gnr(self.tiles_element, element)
        lbl.setStyleSheet("background-image : url(./images/background.png)")
        self.grid[element.x][element.y] = lbl
        self.addWidget(lbl, element.x, element.y)
        self.update()

    def add_element(self, label_element):
        self.grid[label_element.element.x][label_element.element.y] = label_element
        self.addWidget(label_element, label_element.element.x, label_element.element.y)

    def remove_element(self, label_element):
        self.grid[label_element.element.x][label_element.element.y] = None
        if label_element == self.player:
            wid = self.itemAtPosition(label_element.element.x, label_element.element.y).widget()
            self.removeWidget(wid)
        self.removeWidget(label_element)

    def is_element(self, el):
        for i in range(self.width):
            for j in range(self.height):
                if self.grid[i][j] is not None:
                    if isinstance(self.grid[i][j].element, el):
                        return True
        return False

    def move_element(self, label_element, x, y):
        self.remove_element(label_element)
        label_element.element.x = x
        label_element.element.y = y
        self.add_element(label_element)
        if isinstance(label_element.element, Player):
            self.player = label_element

    def is_valid_position(self, x, y):
        return 0 <= x <= self.width and 0 <= y <= self.height

    def get_falling_elements(self):
        adjacent_elements = []
        for x in range(self.width):
            for y in range(self.height):
                if self.is_valid_position(x, y) and self.is_used(x, y):
                    if isinstance(self.grid[x][y].element, (Diamant, Pierre)):
                        adjacent_elements.append(self.grid[x][y])
        return adjacent_elements

    def move_player(self, x_offset, y_offset, dir=None):
        self.player.element.dir = dir
        self.player.element.pixmaps = self.player.element.anim()
        x = self.player.element.x + x_offset
        y = self.player.element.y + y_offset

        if not self.is_valid_position(x, y):
            return 0

        target_element = self.grid[x][y]
        if target_element is None:
            self.move_element(self.player, x, y)

        elif isinstance(target_element.element, Terre):
            self.remove_element(target_element)
            self.move_element(self.player, x, y)
            self.player = self.player

        elif isinstance(target_element.element, Brique):
            return 0

        elif isinstance(target_element.element, Diamant):
            self.remove_element(target_element)
            self.move_element(self.player, x, y)
            return self.point_par_diamant

        elif isinstance(target_element.element, Sortie):
            self.remove_element(self.player)
            self.player = target_element
            return 0

        elif isinstance(target_element.element, Pierre):
            if x_offset == -1 or not self.is_valid_position(target_element.element.x + x_offset,
                                                            target_element.element.y + y_offset) \
                    or self.is_used(target_element.element.x + x_offset, target_element.element.y + y_offset):
                return 0
            else:
                self.move_element(target_element, target_element.element.x + x_offset,
                                  target_element.element.y + y_offset)
                self.move_element(self.player, x, y)

        return 0

    def apply_gravity(self, el):
        if self.is_used(el.element.x + 1, el.element.y):
            if isinstance(self.grid[el.element.x + 1][el.element.y].element, Player) and el.element.is_Falling:
                self.remove_element(self.player)
                self.move_element(el, el.element.x + 1, el.element.y)
                return True
        if isinstance(el.element, (Diamant, Pierre)):
            if el.element.x + 1 < self.height:
                if self.grid[el.element.x + 1][el.element.y] is None:
                    el.element.is_Falling = True
                    self.move_element(el, el.element.x + 1, el.element.y)
                elif isinstance(self.grid[el.element.x + 1][el.element.y].element, (Diamant, Pierre)) or el.element.is_Falling:
                    if self.grid[el.element.x + 1][el.element.y + 1] is None and self.grid[el.element.x][el.element.y + 1] is None:
                        el.element.is_Falling = True
                        self.move_element(el, el.element.x, el.element.y + 1)
                    elif self.grid[el.element.x + 1][el.element.y - 1] is None and self.grid[el.element.x][
                        el.element.y - 1] is None:
                        el.element.is_Falling = True
                        self.move_element(el, el.element.x, el.element.y - 1)
                    else:
                        el.element.is_Falling = False
                else:
                    el.element.is_Falling = False
            else:
                el.element.is_Falling = False
