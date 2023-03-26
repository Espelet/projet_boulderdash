import os

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


class Element:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pixmaps = []


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
        if dir is None:
            x = 0
            for y in range(2):
                self.pixmaps.append(self.tiles[x, y])
                self.pixmaps.append(self.tiles[x, y])


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


class el_none(Element):
    def __init__(self, x, y, tiles):
        super().__init__(x, y)
        self.tiles = tiles
        y = 2
        for x in range(4):
            self.pixmaps.append(self.tiles[0, y])


class label_gnr(QLabel):
    def __init__(self, tiles, el):
        super(label_gnr, self).__init__()
        self.tiles = tiles
        self.element = el
        self.pixmaps = self.element.pixmaps


class Plateau(QGridLayout):
    def __init__(self, width, height, parent=None):
        super(Plateau, self).__init__(parent)
        self.tiles_element = cut_image_into_tiles('./images/Tileset.png', 24, 12)
        self.tiles_joueur = cut_image_into_tiles('./images/player_new.png', 15, 6)
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(self.height)] for _ in range(self.width)]
        self.player = None
        self.score = 0

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
        self.update()

    def remove_element(self, label_element):
        self.grid[label_element.element.x][label_element.element.y] = None
        if label_element == self.player:
            wid = self.itemAtPosition(label_element.element.x, label_element.element.y).widget()
            self.removeWidget(wid)
        self.removeWidget(label_element)
        self.update()

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

    def move_player(self, x_offset, y_offset):
        x = self.player.element.x + x_offset
        y = self.player.element.y + y_offset

        if not self.is_valid_position(x, y):
            return False

        target_element = self.grid[x][y]
        if target_element is None:
            self.move_element(self.player, x, y)
        elif isinstance(target_element.element, Terre):
            self.remove_element(target_element)
            self.move_element(self.player, x, y)
            self.player = self.player
        elif isinstance(target_element.element, Brique):
            return False
        elif isinstance(target_element.element, Diamant):
            self.score += 10
            self.remove_element(target_element)
            self.move_element(self.player, x, y)
            return self.score

        elif isinstance(target_element.element, Sortie):
            self.remove_element(self.player)
            self.player = None
            return True

        elif isinstance(target_element.element, Pierre):
            if x_offset == -1 or not self.is_valid_position(target_element.element.x + x_offset, target_element.element.y + y_offset) \
                    or self.is_used(target_element.element.x + x_offset, target_element.element.y + y_offset):
                return False
            else:
                self.move_element(target_element, target_element.element.x + x_offset, target_element.element.y + y_offset)
                self.move_element(self.player, x, y)
                return True


    def apply_gravity(self, el):
        if self.is_used(el.element.x + 1, el.element.y):
            if isinstance(self.grid[el.element.x + 1][el.element.y].element, Player) and el.element.is_Falling:
                self.remove_element(self.player)
                self.move_element(el, el.element.x + 1, el.element.y)
                self.player = None
                return True
        if isinstance(el.element, (Diamant, Pierre)):
            if el.element.x + 1 < self.height:
                if self.grid[el.element.x + 1][el.element.y] is None:
                    el.element.is_Falling = True
                    self.move_element(el, el.element.x + 1, el.element.y)
                    self.apply_gravity(el)
                elif isinstance(self.grid[el.element.x + 1][el.element.y].element, (Diamant, Pierre)):
                    if self.grid[el.element.x + 1][el.element.y + 1] is None and self.grid[el.element.x][el.element.y + 1] is None:
                        el.element.is_Falling = True
                        self.move_element(el, el.element.x, el.element.y + 1)
                        self.apply_gravity(el)
                    elif self.grid[el.element.x + 1][el.element.y - 1] is None and self.grid[el.element.x][el.element.y - 1] is None:
                        el.element.is_Falling = True
                        self.move_element(el, el.element.x, el.element.y - 1)
                        self.apply_gravity(el)
                    else:
                        el.element.is_Falling = False
                else:
                    el.element.is_Falling = False
            else:
                el.element.is_Falling = False