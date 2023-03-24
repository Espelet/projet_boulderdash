import random
import time

from element import *
import numpy.random as rd
import keyboard

class BoulderDash:
    def __init__(self, width, height, nbr_diams,nbr_pierre, nbr_brick):
        self.P = Plateau(width, height)
        self.grid = self.P.grid
        self.height = height
        self.width = width
        self.nbr_diams = nbr_diams
        self.nbr_pierre = nbr_pierre
        self.nbr_brick = nbr_brick
        self.falling_ent = []

    def __str__(self):
        output = ""
        for j in range(self.height):
            for i in range(self.width):
                if self.grid[i][j] is None:
                    output += " "
                else:
                    output += self.grid[i][j].symbol
            output += "\n"
        return output

    def get(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        return self.grid[x][y]

    def generate(self):
        for j in range(self.height):
            for i in range(self.width):
                if j == 0 or j == self.height - 1 or i == 0 or i == self.width - 1:
                    self.P.add_element(Brick(i, j))
                else:
                    pass
        self.ajt_element(Diamond, self.nbr_diams)
        self.ajt_element(Brick, self.nbr_brick)
        self.ajt_element(Stone, self.nbr_pierre)
        nbr_dirt = ((self.height - 2) * (self.width - 2) - (self.nbr_pierre + self.nbr_brick + self.nbr_diams))//(10/7)
        self.ajt_element(Dirt, nbr_dirt)
        player_pos = (0, 0)
        while self.P.is_used(player_pos[0], player_pos[1]):
            player_pos = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        player = Player(player_pos[0], player_pos[1])
        self.P.add_element(player)
        self.falling_ent = self.P.get_falling_elements()



    def ajt_element(self, element, n):
        if n == 0:
            return True
        else:
            coords = rd.randint(1, self.width), rd.randint(1, self.height)
            if not self.P.is_used(coords[0], coords[1]):
                self.P.add_element(element(coords[0], coords[1]))
                return self.ajt_element(element, n - 1)
            else:
                return self.ajt_element(element, n)
    def move(self):
        while True:
            if keyboard.is_pressed("down arrow"):
                self.P.move_player(0, 1)
                if self.update():
                    print(self)
                    print("Fin des haricots !")
                    break
                print(self)
            if keyboard.is_pressed("up arrow"):
                self.P.move_player(0, -1)
                if self.update():
                    print(self)
                    print("Fin des haricots !")
                    break
                print(self)
            if keyboard.is_pressed("left arrow"):
                self.P.move_player(-1, 0)
                if self.update():
                    print(self)
                    print("Fin des haricots !")
                    break
                print(self)
            if keyboard.is_pressed("right arrow"):
                self.P.move_player(1, 0)
                if self.update():
                    print(self)
                    print("Fin des haricots !")
                    break
                print(self)
            if keyboard.is_pressed("esc"):
                break

            time.sleep(0.1)

    def update(self):
        for el in self.falling_ent:
            t = self.P.apply_gravity(el)
            if t:
                print(self)
                return True



class BoulderDashTest:
    def test_generate(self):
        bd = BoulderDash(self.niveau_a1()[0], self.niveau_a1()[1], self.niveau_a1()[2]
                         , self.niveau_a1()[3], self.niveau_a1()[4])
        bd.generate()
        print(bd)
        bd.move()

    def niveau_a1(self):
        width = 10
        height = 10
        nbr_diams = 5
        nbr_pierre = 15
        nbr_brick = 5
        return width, height, nbr_diams, nbr_pierre, nbr_brick
    def run_tests(self):
        self.test_generate()

if __name__ == "__main__":
    BoulderDashTest().run_tests()
