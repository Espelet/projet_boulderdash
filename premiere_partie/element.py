import random


class Element:
    """ auteur : Chloé
        x,y : int
        cette classe permet de définir les coordonnées des éléments
    """
    def __init__(self, x, y):
        self.x = x    #position horizontale
        self.y = y    #position verticale


class Brique(Element):
    """auteur: Chloé
        les briques sont éléments qui comme décrit dans la classe ont des coordonnées,
        ne peuvent pas tomber, ne peuvent pas se pousser, ne peut pas être consommé"""
    def __init__(self, x, y):
        super().__init__(x, y)   #position
        self.is_gravity_affected = False #non affecté gravité
        self.is_pushable = False  #non déplaçable
        self.is_consumable = False  #non consommable
        self.is_Falling = False  #n'est pas en chute
        self.symbol = "#"      # symbole attribué


class Sortie(Element):
    """auteur: Chloé
        les sorties (il n'y en a que 2 dans notre jeu)
        sont repérées par des coordonnées
        ne subissent pas la gravité, ne peuvent pas être poussées, ne peuvent pas être consommées"""
    def __init__(self, x, y):
        super().__init__(x, y) # position
        self.is_gravity_affected = False # non affecté gravité
        self.is_pushable = False # non déplaçable
        self.is_consumable = False  # non consommable
        self.is_Falling = False   # n'est pas en chute
        self.symbol = "S"    # symbole attribué


class Player(Element):
    """auteur: Chloé
            les sorties (il n'y en a que 2 dans notre jeu)
            est repéré par des coordonnées
            ne subit pas la gravité, ne peut pas être poussé, ne peut pas être consommé"""
    def __init__(self, x, y):
        super().__init__(x, y)    # position
        self.is_gravity_affected = False   # non affecté gravité
        self.is_pushable = False # non déplaçable
        self.is_consumable = False   # non consommable
        self.is_Falling = False  # n'est pas en chute
        self.symbol = "P"     # symbole attribué


class Diamant(Element):
    """auteur: Chloé
            les diamants
            sont repérées par des coordonnées (car est un élément)
            subissent la gravité, ne peuvent pas être poussés, consommables"""
    def __init__(self, x, y):
        super().__init__(x, y)    # position
        self.is_gravity_affected = True   # peut-être affecté par la gravité
        self.is_pushable = False # non déplaçable
        self.is_consumable = True   # consommable
        self.is_Falling = False   # n'est pas en chute
        self.symbol = "D"     # symbole attribué


class Pierre(Element):
    """auteur: Chloé
        les diamants
        sont repérées par des coordonnées (car est un élément)
        subissent la gravité, peuvent être poussés, non consommables"""
    def __init__(self, x, y):
        super().__init__(x, y)     # position
        self.is_gravity_affected = True  # peut-être affecté par la gravité
        self.is_pushable = True  # déplaçable
        self.is_consumable = False   # non consommable
        self.is_Falling = False   # n'est pas en chute
        self.symbol = "O"    # symbole attribué


class Terre(Element):
    """auteur: Chloé
        sont repérées par des coordonnées (car est un élément)
        ne subissent pas la gravité, ne peuvent pas être poussés, consommables"""
    def __init__(self, x, y):
        super().__init__(x, y)     # position
        self.is_gravity_affected = False  # non affecté gravité
        self.is_pushable = False  # non déplaçable
        self.is_consumable = True    # consommable
        self.is_Falling = False    # n'est pas en chute
        self.symbol = "."     # symbole attribué


class Plateau:
    """auteur: Tristan
        création du plateau
        définition de la hauteur et de la lareur du plateau
        permet de définir si un élément se trouve dans le plateau ou non
        de définir l'impact de la gravité
        de définir le déplacement du joueur
        """
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
