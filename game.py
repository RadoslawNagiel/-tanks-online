from tank import Tank
from random import randrange, uniform
from colorsys import hsv_to_rgb


class Game:
    def __init__(self):
        self.tanks = {}
        self.shots = []

    def add_tank(self, player_id):
        random_pos_x = randrange(50, 750)
        random_pos_y = randrange(50, 550)
        random_color = hsv_to_rgb(uniform(0, 1), 1, 1)
        random_color = (random_color[0] * 255, random_color[1] * 255, random_color[2] * 255)

        new_tank = Tank(random_pos_x, random_pos_y, 50, 80, random_color)
        self.tanks[player_id] = new_tank

        return new_tank

    def remove_tank(self, player_id):
        try:
            self.tanks.pop(player_id, None)
        except KeyError as e:
            print(e)

    def use_command(self, data):
        tank_id, other = data
        command, parameters = other

        if command == "move_tank":
            vel, rot = parameters
            self.tanks[tank_id].move(vel, rot)
        if command == "shoot":
            if self.tanks[tank_id].delay <= 0:
                self.shots.append(self.tanks[tank_id].shot(tank_id))

    def loop(self):
        for shot in self.shots:
            if not shot.move():
                self.shots.remove(shot)

        for tank_id in self.tanks:
            for shot in self.shots:
                if not self.tanks[tank_id].is_hit and shot.did_hit_tank(self.tanks[tank_id]):
                    self.tanks[shot.tank_id].points += 1
                    self.tanks[tank_id].hit()
                    self.shots.remove(shot)
            self.tanks[tank_id].tank_loop()
