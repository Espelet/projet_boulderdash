import random
import time

from element import *
import keyboard

class BoulderDash:
    def __init__(self, width, height):
        self.P = Plateau(width, height)
        self.grid = self.P.grid
        self.height = height
        self.width = width
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
                if random.random() < 0.1:
                    self.P.add_element(Brick(i, j))
                    pass
                elif random.random() < 0.1:
                    self.P.add_element(Diamond(i, j))
                    pass
                elif random.random() < 0.05:
                    self.P.add_element(Stone(i, j))
                    pass
                if random.random() < 0.75:
                    self.P.add_element(Dirt(i, j))
        player_pos = (0, 0)
        while self.P.is_used(player_pos[0], player_pos[1]):
            player_pos = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        self.P.add_element(Player(player_pos[0], player_pos[1]))
        self.falling_ent = self.P.get_falling_elements()


    def move(self):
        while True:
            if keyboard.is_pressed("down arrow"):
                self.P.move_player(0, 1)
                print(self)
            if keyboard.is_pressed("up arrow"):
                self.P.move_player(0, -1)
                print(self)
            if keyboard.is_pressed("left arrow"):
                self.P.move_player(-1, 0)
                print(self)
            if keyboard.is_pressed("right arrow"):
                self.P.move_player(1, 0)
                print(self)
            if keyboard.is_pressed("esc"):
                break
            self.P.apply_gravity(self.falling_ent)



class BoulderDashTest:
    def test_generate(self):
        bd = BoulderDash(10, 10)
        bd.generate()
        print(bd)
        bd.move()

    def run_tests(self):
        self.test_generate()

if __name__ == "__main__":
    BoulderDashTest().run_tests()
