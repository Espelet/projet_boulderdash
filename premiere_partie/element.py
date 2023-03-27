import random


class Element:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Brique(Element):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.is_gravity_affected = False
        self.is_pushable = False
        self.is_consumable = False
        self.is_Falling = False
        self.symbol = "#"


class Sortie(Element):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.is_gravity_affected = False
        self.is_pushable = False
        self.is_consumable = False
        self.is_Falling = False
        self.symbol = "S"


class Player(Element):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.is_gravity_affected = False
        self.is_pushable = False
        self.is_consumable = False
        self.is_Falling = False
        self.symbol = "P"


class Diamant(Element):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.is_gravity_affected = True
        self.is_pushable = False
        self.is_consumable = True
        self.is_Falling = False
        self.symbol = "D"


class Pierre(Element):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.is_gravity_affected = True
        self.is_pushable = True
        self.is_consumable = False
        self.is_Falling = False
        self.symbol = "O"


class Terre(Element):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.is_gravity_affected = False
        self.is_pushable = False
        self.is_consumable = True
        self.is_Falling = False
        self.symbol = "."


class Plateau:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(height)] for _ in range(width)]
        self.player = None
        self.score = 0

    def is_used(self, x, y):
        return self.grid[x][y] is not None

    def add_element(self, element):
        self.grid[element.x][element.y] = element
        if isinstance(element, Player):
            self.player = element

    def remove_element(self, element):
        self.grid[element.x][element.y] = None

    def is_element(self, el):
        for i in range(self.width):
            for j in range(self.height):
                if isinstance(self.grid[i][j], el):
                    return True
        return False

    def move_element(self, element, x, y):
        self.remove_element(element)
        element.x = x
        element.y = y
        self.add_element(element)

    def is_valid_position(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def get_falling_elements(self):
        adjacent_elements = []
        for x in range(self.width):
            for y in range(self.height):
                if self.is_valid_position(x, y) and isinstance(self.grid[x][y], (Diamant, Pierre)):
                    adjacent_elements.append(self.grid[x][y])
        return adjacent_elements

    def move_player(self, x_offset, y_offset):
        x = self.player.x + x_offset
        y = self.player.y + y_offset

        if not self.is_valid_position(x, y):
            return False

        target_element = self.grid[x][y]

        if isinstance(target_element, Brique):
            return False

        elif isinstance(target_element, Diamant):
            self.score += 10
            self.remove_element(target_element)
            self.move_element(self.player, x, y)
            return self.score

        elif isinstance(target_element, Sortie):
            self.remove_element(self.player)
            self.player = None
            return True

        elif isinstance(target_element, Pierre):
            if y_offset == -1 or not self.is_valid_position(target_element.x + x_offset, target_element.y + y) \
                    or self.is_used(target_element.x + x_offset, target_element.y + y_offset):
                return False
            else:
                self.move_element(target_element, target_element.x + x_offset, target_element.y + y_offset)
                self.move_element(self.player, x, y)
                return True
        self.move_element(self.player, x, y)

    def apply_gravity(self, el):
        if isinstance(self.grid[el.x][el.y + 1], Player) and el.is_Falling:
            self.remove_element(self.player)
            self.move_element(el, el.x, el.y + 1)
            self.player = None
            return True
        if isinstance(el, (Diamant, Pierre)):
            if el.y + 1 < self.height:
                if self.grid[el.x][el.y + 1] is None:
                    el.is_Falling = True
                    self.move_element(el, el.x, el.y + 1)
                    self.apply_gravity(el)
                elif isinstance(self.grid[el.x][el.y + 1], (Diamant, Pierre)):
                    if self.grid[el.x + 1][el.y + 1] is None and self.grid[el.x + 1][el.y] is None:
                        el.is_Falling = True
                        self.move_element(el, el.x + 1, el.y)
                        self.apply_gravity(el)
                    elif self.grid[el.x - 1][el.y + 1] is None and self.grid[el.x - 1][el.y] is None:
                        el.is_Falling = True
                        self.move_element(el, el.x - 1, el.y)
                        self.apply_gravity(el)
            else:
                el.is_Falling = False
