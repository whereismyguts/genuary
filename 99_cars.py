# Something you’ve always wanted to learn
import pyxel
import random
import math
import time
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
CARS_COUNT = 10
MEN_COUNT = 2
ENTER_DURATION = 1
BACKGROUND_COLOR = 7
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
    next_state_change = 10
    car = None

    def __init__(self, cars, x, y, car=None) -> None:
        self.state = 'walking'
        if car:
            self.car = car
            self.state = 'incar'
        self.cars = cars
        self.x = x
        self.y = y
        self.speed = 0.5
        self.color = random.choice(
            [1, 5, 6, 12, 4, 8, 2, 14, 15]
        )

    @property
    def time_until_state_change(self):
        return self.next_state_change - time.time()

    def update(self):
        # if self.target_car and self.target_car.state == 'entering':
        #     return

        if self.state == 'incar':
            self.x = self.car.x
            self.y = self.car.y
            self.target_car = None
            return

        if self.state == 'entering':

            if self.next_state_change < time.time():

                self.target_car.man.car = None
                self.target_car.man.state = 'walking'
                self.target_car.man.prev_car = self.target_car
                self.target_car.man.x = self.target_car.man.x + \
                    math.cos(self.target_car.direction + math.pi / 2) * 10
                self.target_car.man.y = self.target_car.man.y + \
                    math.sin(self.target_car.direction + math.pi / 2) * 10

                self.target_car.robber = None

                self.car = self.target_car
                self.state = 'incar'
                self.prev_car = None
                self.target_car = None

                self.car.man = self
            else:
                # self.target_car.man.x -= (self.x -
                #                           self.target_car.man.x) * 0.1
                # self.target_car.man.y -= (self.y -
                #                           self.target_car.man.y) * 0.1

                self.x += (self.target_car.x - self.x) * 0.1 ** 2
                self.y += (self.target_car.y - self.y) * 0.1 ** 2
            return

        points = [(p, c) for c in self.cars for p in c.enter_points]
        points = [(p, c) for p, c in points if c.state != 'entering']
        point, car = self.find_closest(
            points,
            exclude=[self.prev_car]
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
            self.state = 'entering'
            self.next_state_change = time.time() + ENTER_DURATION
            self.target_car.change_state(
                state='entering', duration=ENTER_DURATION)
            self.target_car.robber = self
            self.prev_car = self.target_car

    def draw(self):
        # points = [(p, c) for c in self.cars for p in c.enter_points]
        # size depend on time from 1 to 3:
        if self.chaos_mode:
            pyxel.circ(self.x, self.y,
                       0.1 + math.sin(time.time() * 0.5) + 1 / 2,
                       self.color)
        else:
            if not self.car:
                pyxel.circ(
                    self.x, self.y, 2, self.color
                )

            # if self.state == 'entering':
            #     pyxel.text(
            #         self.x + 5, self.y + 5,
            #         str(round(self.time_until_state_change, 1)),
            #         0
            #     )
            # pyxel.rect(self.x - 2, self.y - 2, 4, 12, 7)
            # pyxel.text(self.x + 5, self.y, self.state, 0)

            # if self.car:
            #     pyxel.line(self.x, self.y, self.car.x, self.car.y, self.color)

            # if self.target_car:
            #     pyxel.line(
            #         self.x - 4, self.y - 4,
            #         self.target_car.x,
            #         self.target_car.y,
            #         0
            #     )
        # for p, c in points:
        #     pyxel.line(self.x, self.y, p[0], p[1], c.colors[1])

            # if self.target_point:
            #     pyxel.line(self.x, self.y,
            #                self.target_point[0], self.target_point[1], 0)

            # pyxel.text(self.x + 5, self.y + 5, self.state, 0)
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


class Car:

    robber = None

    def __init__(self, x, y, colors):
        self.x = x
        self.y = y
        self.direction = random.random() * 2 * math.pi
        self.angle_speed = self.new_angle_speed()
        self.move_speed = random.random() * 0.8 + 0.2
        self.colors = colors

        self.state = random.choice(['driving', 'rotating', 'stopped'])
        self.next_state_change = 0
        self.trays = []

    @ property
    def pos(self):
        return (self.x, self.y)

    @ property
    def enter_points(self):
        return [
            self.polar_vector(8, -math.pi / 2),
            self.polar_vector(8, math.pi / 2),
        ]

    def polar_vector(self, length, angle):
        return (
            self.x + math.cos(self.direction + angle) * length,
            self.y + math.sin(self.direction + angle) * length,
        )

    def new_angle_speed(self):
        return random.choice([0.05, -0.05])

    def draw_body(self, left_x, left_y, right_x, right_y, forward_x, forward_y, backward_x, backward_y):

        y_offset = 10
        for offset in [(left_x, left_y), (right_x, right_y)]:
            pyxel.line(
                self.x + forward_x * y_offset + offset[0] * 5,
                self.y + forward_y * y_offset + offset[1] * 5,

                self.x + backward_x * y_offset + offset[0] * 5,
                self.y + backward_y * y_offset + offset[1] * 5,
                0,
            )

        for h in [-11, -6, 4, 11.5]:
            pyxel.line(
                self.x + forward_x * h + right_x * 5,
                self.y + forward_y * h + right_y * 5,

                self.x + forward_x * h + left_x * 5,
                self.y + forward_y * h + left_y * 5,
                0,
            )

        # for h in [6, 11]:
        #     pyxel.line(
        #         self.x + backward_x * h + right_x * 5,
        #         self.y + backward_y * h + right_y * 5,

        #         self.x + backward_x * h + left_x * 5,
        #         self.y + backward_y * h + left_y * 5,
        #         0,
        #     )

        for h in list(range(-10, 11)):
            if h in [-11, -6, 4, 11]:
                color = 0
            else:
                color = self.colors[int(h in range(-5, 4))]
            pyxel.line(
                self.x + forward_x * h + right_x * 4,
                self.y + forward_y * h + right_y * 4,

                self.x + forward_x * h + left_x * 4,
                self.y + forward_y * h + left_y * 4,
                color,
            )
            if color:  # not black line
                inbetween_h = (h + 0.5)
                pyxel.line(
                    self.x + forward_x * inbetween_h + right_x * 4,
                    self.y + forward_y * inbetween_h + right_y * 4,

                    self.x + forward_x * inbetween_h + left_x * 4,
                    self.y + forward_y * inbetween_h + left_y * 4,
                    color,
                )

        # pyxel.fill(
        #     self.x + forward_x * 7,
        #     self.y + forward_y * 7,
        #     self.colors[0]
        # )
        # pyxel.fill(
        #     self.x + backward_x * 10,
        #     self.y + backward_y * 10,
        #     self.colors[0]
        # )

    def animate(self, left_x, left_y, right_x, right_y, forward_x, forward_y):
        if self.state == 'entering' and self.robber:

            distances = [sqrdist(p, self.robber.pos)
                         for p in self.enter_points]

            if distances[0] < distances[1]:
                side_x = left_x
                side_y = left_y
            else:
                side_x = right_x
                side_y = right_y

            t = min(
                int((ENTER_DURATION - self.time_until_state_change) * 6),
                5
            )

            # a = math.pi / (2 * t)
            # a = math.pi / (3 / t)
            multipliers = [(1, 13), (-2, 11), (-4, 9)][::-1]
            multipliers = multipliers + multipliers[::-1]
            try:
                fwd, rht = multipliers[t]
            except IndexError:
                print(t, multipliers)
                raise

            pyxel.line(
                self.x + forward_x * 5 + side_x * 4,
                self.y + forward_y * 5 + side_y * 4,

                self.x + forward_x * fwd + side_x * rht,
                self.y + forward_y * fwd + side_y * rht,
                0,
            )

    def draw(self):
        if self.chaos_mode:
            return

        forward_x = math.cos(self.direction)
        forward_y = math.sin(self.direction)

        backward_x = - forward_x
        backward_y = - forward_y

        left_x = math.cos(self.direction - math.pi / 2)
        left_y = math.sin(self.direction - math.pi / 2)

        right_x = -math.cos(self.direction - math.pi / 2)
        right_y = -math.sin(self.direction - math.pi / 2)

        self.draw_body(
            left_x, left_y,
            right_x, right_y,
            forward_x, forward_y,
            backward_x, backward_y
        )

        self.animate(
            left_x, left_y,
            right_x, right_y,
            forward_x, forward_y
        )

        # MUST BE IN UPDATE BUT IT OPTIMIZED
        y_offset = 13
        for side_koefs in [
            # (left_x, left_y),
            (right_x, right_y)
        ]:
            self.trays.append((
                self.x + backward_x * (y_offset + 2) + side_koefs[0] * 1,
                self.y + backward_y * (y_offset + 2) + side_koefs[1] * 1,
                self.x + backward_x * y_offset +
                side_koefs[0] * 1 + random.random() * 4 - 2,
                self.y + backward_y * y_offset +
                side_koefs[1] * 1 + random.random() * 4 - 2,
            ))

        for tray in self.trays:
            pyxel.line(
                *tray, 13,
            )

    def update(self):
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

        if len(self.trays) > 20:
            for i in range(len(self.trays) - 10):
                self.trays.pop(random.randint(0, len(self.trays) - 1))

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
    man = None
    chaos_mode = False

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

        for c in self.cars:
            c.man = Man(self.cars, c.x, c.y, car=c)
            self.men.append(c.man)

        pyxel.init(
            SCREEN_WIDTH, SCREEN_HEIGHT,
            'Something you’ve always wanted to learn', fps=FPS)
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
            pyxel.cls(BACKGROUND_COLOR)

    def draw(self):

        if not self.chaos_mode:
            pyxel.cls(BACKGROUND_COLOR)

        for m in self.men:
            m.draw()

        for c in self.cars:
            c.draw()


App()
