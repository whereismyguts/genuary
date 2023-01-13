# Something you’ve always wanted to learn

import pyxel
import random
import math
import time
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
CARS_COUNT = random.randint(5, 30)
MEN_COUNT = random.randint(2, 50)
BACKGROUND_COLOR = random.randint(0, 15)
FPS = 60


def sqrdist(point1, point2):
    return (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2


def angle(point1, point2):
    return math.atan2(point2[1] - point1[1], point2[0] - point1[0])


class Man:

    target_car = None
    target_point = None
    prev_car = None
    chaos_mode = False

    def __init__(self, cars, x, y) -> None:
        self.cars = cars
        self.x = x
        self.y = y
        self.speed = 0.5
        self.color = random.choice(list(set(range(16)) - {BACKGROUND_COLOR}))

    def update(self):
        if self.target_car and self.target_car.state == 'entering':

            return
        points = [(p, c) for c in self.cars for p in c.enter_points]
        point, car = self.find_closest(
            points,
            exclude=[self.prev_car] + list(
                filter(
                    lambda c: c.state == 'entering',
                    self.cars,
                )
            )
        )

        self.target_point = point
        self.target_car = car

        if self.target_point:
            a = angle(self.target_point, self.pos) - math.pi
            self.x += math.cos(a) * self.speed
            self.y += math.sin(a) * self.speed

        if (
            self.target_car and
            self.target_car.state != 'entering' and
            self.target_point and
            sqrdist(self.pos, self.target_point) < 2
        ):
            self.target_car.change_state(state='entering', duration=1)
            self.prev_car = self.target_car

    def draw(self):
        # points = [(p, c) for c in self.cars for p in c.enter_points]
        # size depend on time from 1 to 3:
        if self.chaos_mode:
            pyxel.circ(self.x, self.y,
                       0.1 + math.sin(time.time() * 0.5) + 1 / 2,
                       self.color)
        else:
            pyxel.circ(self.x, self.y, 2, self.color)

        # for p, c in points:
        #     pyxel.line(self.x, self.y, p[0], p[1], c.colors[1])

        return
        if self.target_point:
            pyxel.line(self.x, self.y,
                       self.target_point[0], self.target_point[1], 0)

            # pyxel.text(5, y, str(p) + ' ' + str(c), c.colors[0])
            # y += 10

    @ property
    def pos(self):
        return (self.x, self.y)

    def find_closest(self, points, exclude=None):
        mind = 100000
        result_p = None
        result_c = None
        for p, c in points:
            if exclude and c in exclude:
                continue
            d = sqrdist(p, self.pos)
            if d < mind:
                mind = d
                result_p = p
                result_c = c
        return result_p, result_c


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
        self.move_speed = random.random() * 0.8 + 0.2
        self.smokes = []
        self.colors = colors

        self.state = random.choice(['driving', 'rotating', 'stopped'])
        self.next_state_change = 0

    @ property
    def pos(self):
        return (self.x, self.y)

    @ property
    def enter_points(self):
        return [
            self.polar_vector(8, -math.pi / 2),
            self.polar_vector(8, math.pi / 2),
        ]

    def new_angle_speed(self):
        return random.choice([0.05, -0.05])

    def draw(self):
        if self.chaos_mode:
            return
        # pyxel.circ(self.x, self.y, 2, self.color)

        forward_x = math.cos(self.direction)
        forward_y = math.sin(self.direction)

        backward_x = - math.cos(self.direction)
        backward_y = - math.sin(self.direction)

        left_x = math.cos(self.direction - math.pi / 2)
        left_y = math.sin(self.direction - math.pi / 2)

        right_x = -math.cos(self.direction - math.pi / 2)
        right_y = -math.sin(self.direction - math.pi / 2)

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

        # for s in filter(lambda s: s.size < 10, self.smokes):
        #     s.draw()
        self.animate()

        return
        pyxel.text(
            self.x, self.y + 15,
            '{}({})'.format(
                self.state,
                "%.1f" % self.time_until_state_change
            ),
            0
        )

    def polar_vector(self, length, angle):
        return (
            self.x + math.cos(self.direction + angle) * length,
            self.y + math.sin(self.direction + angle) * length,
        )

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

    def animate(self):
        t = int(20 - self.time_until_state_change * 2)
        # pyxel.text(
        #     self.x + 15, self.y, str(t), 0
        # )

    def update(self):
        # self.process_smoke()

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
            if self.time_until_state_change <= 0:
                self.change_state('driving')

        elif self.state == 'entering':
            self.move_speed = 0

            if self.time_until_state_change <= 0:
                self.change_state('driving')

    @ property
    def time_until_state_change(self):
        return self.next_state_change - time.time()

    def change_state(self, state=None, duration=None):

        if self.time_until_state_change <= 0 or state:
            self.state = state or random.choice(
                list({'rotating', 'stopped', 'driving'} - {self.state})
            )

            self.next_state_change = time.time() + (duration or random.random() * 6)

            if self.state == 'rotating':
                self.angle_speed = self.new_angle_speed()
            if self.state == 'driving':
                self.move_speed = random.random() * 0.5 + 0.1


class App:
    cars = []
    men = []
    chaos_mode = True

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

        for i in range(MEN_COUNT):
            self.men.append(
                Man(self.cars, random.randint(0, SCREEN_WIDTH),
                    random.randint(0, SCREEN_HEIGHT),)
            )

        pyxel.init(
            SCREEN_WIDTH, SCREEN_HEIGHT,
            'Something you’ve always wanted to learn', fps=FPS)
        pyxel.cls(BACKGROUND_COLOR)
        pyxel.run(self.update, self.draw)

    def update(self):
        for c in self.cars:
            c.chaos_mode = self.chaos_mode
            c.update()
            if c.x < 0:
                c.x = SCREEN_WIDTH
            if c.x > SCREEN_WIDTH:
                c.x = 0
            if c.y < 0:
                c.y = SCREEN_HEIGHT
            if c.y > SCREEN_HEIGHT:
                c.y = 0

        for m in self.men:
            m.chaos_mode = self.chaos_mode
            m.update()

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_C):
            self.chaos_mode = not self.chaos_mode

    def draw(self):

        if not self.chaos_mode:
            pyxel.cls(BACKGROUND_COLOR)

        for c in self.cars:
            c.draw()

        for m in self.men:
            m.draw()


App()
