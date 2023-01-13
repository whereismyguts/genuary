# Something you’ve always wanted to learn

import pyxel
import random
import math
import time
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
CARS_COUNT = 15
BACKGROUND_COLOR = 7
FPS = 60


class Smoke:

    def __init__(self, x, y, direction) -> None:

        self.x = x
        self.y = y
        self.direction = direction + random.random() * 0.5 - 0.25
        self.size = 1

    def update(self):
        self.x += math.cos(self.direction) * 0.1
        self.y += math.sin(self.direction) * 0.1
        self.size += random.random() * 0.1

    def draw(self):
        pyxel.circ(self.x, self.y, self.size, 1)


class Car:

    def __init__(self, x, y, colors):
        self.x = x
        self.y = y
        self.direction = random.random() * 2 * math.pi
        self.angle_speed = self.new_angle_speed()
        self.move_speed = random.random() * 0.5 + 0.1
        self.smokes = []
        self.colors = colors

        self.state = random.choice(['driving', 'rotating', 'stopped'])
        self.next_state_change = 0

    def new_angle_speed(self):
        return random.choice([0.05, -0.05])

    def draw(self):
        # pyxel.circ(self.x, self.y, 2, self.color)

        forward_x = math.cos(self.direction)
        forward_y = math.sin(self.direction)

        backward_x = - math.cos(self.direction)
        backward_y = - math.sin(self.direction)

        left_x = math.cos(self.direction - math.pi / 2)
        left_y = math.sin(self.direction - math.pi / 2)

        right_x = -math.cos(self.direction - math.pi / 2)
        right_y = -math.sin(self.direction - math.pi / 2)

        car_len = 20
        car_wide = 10

        pyxel.line(
            # forward left:
            self.x + forward_x * 10 + left_x * 5,
            self.y + forward_y * 10 + left_y * 5,

            self.x + backward_x * 10 + left_x * 5,
            self.y + backward_y * 10 + left_y * 5,
            0,
        )
        pyxel.line(
            # forward right:
            self.x + forward_x * 10 + right_x * 5,
            self.y + forward_y * 10 + right_y * 5,

            self.x + backward_x * 10 + right_x * 5,
            self.y + backward_y * 10 + right_y * 5,
            0,
        )

        for h in [4, 10]:
            pyxel.line(

                self.x + forward_x * h + right_x * 4,
                self.y + forward_y * h + right_y * 4,

                self.x + forward_x * h + left_x * 5,
                self.y + forward_y * h + left_y * 5,
                0,
            )
            pyxel.line(

                self.x + backward_x * h + right_x * 5,
                self.y + backward_y * h + right_y * 5,

                self.x + backward_x * h + left_x * 5,
                self.y + backward_y * h + left_y * 5,
                0,
            )
        pyxel.fill(
            self.x + forward_x * 8,
            self.y + forward_y * 8,
            self.colors[0]
        )
        pyxel.fill(
            self.x + backward_x * 8,
            self.y + backward_y * 8,
            self.colors[0]
        )
        pyxel.fill(
            self.x,
            self.y,
            self.colors[1],
        )

        # pyxel.line(
        #     self.x,
        #     self.y,
        #     self.x - math.cos(self.direction) * 10,
        #     self.y - math.sin(self.direction) * 10,
        #     self.color + 1
        # )

        for s in filter(lambda s: s.size < 10, self.smokes):
            s.draw()

        # pyxel.text(self.x, self.y, self.state, 0)
        # pyxel.text(self.x, self.y + 10, "%.2f" % self.direction, 0)
        # pyxel.text(self.x, self.y + 20, "%.2f" %
        #            self.time_until_state_change, 0)

    def spawn_smoke(self):
        return
        if len(list(filter(lambda s: s.size < 10, self.smokes))) > 10:
            return

        if random.random() > 0.9:
            self.smokes.append(Smoke(
                self.x - math.cos(self.direction) * 10,
                self.y - math.sin(self.direction) * 10,
                self.direction + math.pi,
            ))

    def process_smoke(self):
        if self.state in ['driving', 'rotating']:
            self.spawn_smoke()
        for s in filter(lambda s: s.size < 10, self.smokes):
            s.update()

    def update(self):
        self.process_smoke()

        if self.state == 'rotating':
            self.direction += self.angle_speed
            if self.direction > math.pi * 2:
                self.direction = 0
            if self.direction < 0:
                self.direction = math.pi * 2
            if self.time_until_state_change <= 5:
                for a in [0, math.pi / 2, math.pi, math.pi * 3 / 2]:
                    if self.direction > a - 0.05 and self.direction < a + 0.05:
                        self.direction = a
                        self.change_state(state='driving')
                        break

            self.x += math.cos(self.direction) * self.move_speed
            self.y += math.sin(self.direction) * self.move_speed

        elif self.state == 'driving':

            self.x += math.cos(self.direction) * self.move_speed
            self.y += math.sin(self.direction) * self.move_speed
            self.change_state()

        elif self.state == 'stopped':
            self.move_speed *= 0.9
            self.change_state()

    @property
    def time_until_state_change(self):
        return self.next_state_change - time.time()

    def change_state(self, state=None):

        if self.time_until_state_change <= 0 or state:
            self.state = state or random.choice(
                list({'rotating', 'stopped', 'driving'} - {self.state})
            )

            self.next_state_change = time.time() + random.random() * 6

            if self.state == 'rotating':
                self.angle_speed = self.new_angle_speed()
            if self.state == 'driving':
                self.move_speed = random.random() * 0.5 + 0.1


class App:
    cars = []

    def __init__(self) -> None:

        for i in range(CARS_COUNT):
            self.cars.append(Car(
                random.randint(0, SCREEN_WIDTH),
                random.randint(0, SCREEN_HEIGHT),
                random.choice([
                    (4, 14),
                    (1, 5),
                    (12, 6),
                    (9, 10),
                    (3, 11),
                    (13, 15)
                ])
            ))

        pyxel.init(
            SCREEN_WIDTH, SCREEN_HEIGHT,
            'Something you’ve always wanted to learn', fps=FPS)
        pyxel.run(self.update, self.draw)

    def update(self):
        for c in self.cars:
            c.update()
            if c.x < 0:
                c.x = SCREEN_WIDTH
            if c.x > SCREEN_WIDTH:
                c.x = 0
            if c.y < 0:
                c.y = SCREEN_HEIGHT
            if c.y > SCREEN_HEIGHT:
                c.y = 0

    def draw(self):

        pyxel.cls(BACKGROUND_COLOR)
        for c in self.cars:

            c.draw()


App()
