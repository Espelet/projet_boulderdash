import random

class Element:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Brick(Element):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.is_gravity_affected = False
        self.is_pushable = False
        self.is_consumable = False
        self.is_Falling = False
        self.symbol = "#"

class Player(Element):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.is_gravity_affected = False
        self.is_pushable = False
        self.is_consumable = False
        self.is_Falling = False
        self.symbol = "P"

class Diamond(Element):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.is_gravity_affected = True
        self.is_pushable = False
        self.is_consumable = True
        self.is_Falling = False
        self.symbol = "D"

class Stone(Element):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.is_gravity_affected = True
        self.is_pushable = True
        self.is_consumable = False
        self.is_Falling = False
        self.symbol = "O"

class Dirt(Element):
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
                if self.is_valid_position(x, y) and isinstance(self.grid[x][y], (Diamond, Stone)):
                    adjacent_elements.append(self.grid[x][y])
        return adjacent_elements

    def move_player(self, x_offset, y_offset):
        x = self.player.x + x_offset
        y = self.player.y + y_offset
        if not self.is_valid_position(x, y):
            return False
        target_element = self.grid[x][y]
        if isinstance(target_element, Brick):
            return False
        if isinstance(target_element, Diamond):
            self.score += 1
            self.remove_element(target_element)
            self.move_element(self.player, x, y)
            return self.score
        if isinstance(target_element, Stone):
            if y_offset == -1 or not self.move_element(target_element, x, y) \
                    or not self.is_valid_position(target_element.x + x_offset, target_element.y + y):
                return False

        self.move_element(self.player, x, y)
        return True

    def apply_gravity(self, el):
        if isinstance(self.grid[el.x][el.y + 1], Player) and el.is_Falling:
            return True
        if isinstance(el, (Diamond, Stone)):
            if el.y + 1 < self.height:
                if self.grid[el.x][el.y + 1] is None:
                    el.is_Falling = True
                    print(el)
                    self.move_element(el, el.x, el.y + 1)
                    self.apply_gravity(el)
                else:
                    el.is_Falling = False
            else:
                el.is_Falling = False


