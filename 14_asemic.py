import pyxel
import random
import math
import time

WIDTH = 256
HEIGHT = 256
BACKGROUND_COLOR = random.choice([7, 15, 6, 11])
DRAW_COLORS = [0, 1, 5, 4, 8, 2, 3]
DRAW_COLOR = random.choice(DRAW_COLORS)
LETTER_WIDTH = random.randint(10, 30)  # 20
LETTER_COUNT = 6
MARGIN = LETTER_WIDTH / (random.random() * 5 + 2)  # 10


class Shapes:
    def __init__(self):
        self.R = 10

    def circle(self, t, **kwargs):
        r = kwargs.get("a", self.R)
        x = r * math.cos(t)
        y = r * math.sin(t)
        return x, y

    def spiral(self, t, **kwargs):
        a = kwargs.get('a', self.R)
        b = kwargs.get('b', self.R)
        x = a * t * math.cos(t)
        y = b * t * math.sin(t)
        return x, y

    def parabola(self, t, **kwargs):
        a = kwargs.get('a', self.R)
        x = t
        y = a * t**2
        return x, y

    def hyperbola(self, t, **kwargs):
        a = kwargs.get('a', self.R)
        b = kwargs.get('b', self.R)
        x = a * math.cosh(t)
        y = b * math.sinh(t)
        return x, y

    def cardioid(self, t, **kwargs):
        a = kwargs.get('a', self.R)
        x = a * (2 * math.cos(t) - math.cos(2 * t))
        y = a * (2 * math.sin(t) - math.sin(2 * t))
        return x, y

    def limacon(self, t, **kwargs):
        a = kwargs.get('a', self.R)
        x = a * (math.cos(t) + 2 * math.cos(2 * t))
        y = a * (math.sin(t) - 2 * math.sin(2 * t))
        return x, y

    def lemniscate(self, t, **kwargs):
        a = kwargs.get('a', self.R)
        x = a * math.cos(t) * math.sqrt(2 * math.cos(2 * t))
        y = a * math.sin(t) * math.sqrt(2 * math.cos(2 * t))
        return x, y

    def witch_of_agnesi(self, t, **kwargs):
        a = kwargs.get('a', self.R)
        x = a * (2 * math.cos(t) / (1 + math.sin(t)**2))
        y = a * (math.cos(t) * math.sin(t) / (1 + math.sin(t)**2))
        return x, y

    def astroid(self, t, **kwargs):
        a = kwargs.get('a', self.R)
        x = a * (math.cos(t)**3)
        y = a * (math.sin(t)**3)
        return x, y

    def butterfly_curve(self, t, **kwargs):
        a = kwargs.get('a', self.R)
        b = kwargs.get('b', self.R)
        c = kwargs.get('c', self.R)
        x = math.sin(t) * (math.exp(math.cos(t)) - a *
                           math.cos(4 * t) - math.pow(math.sin(t / b), c))
        y = math.cos(t) * (math.exp(math.cos(t)) - a *
                           math.cos(4 * t) - math.pow(math.sin(t / b), c))
        return x, y


def get_random_func():
    shapes = Shapes()
    all_methods = [
        'astroid', 'butterfly_curve',
        'cardioid', 'circle', 'hyperbola',
        'lemniscate', 'limacon',
        'parabola', 'spiral', 'witch_of_agnesi',
    ]

    funcname = random.choice(all_methods)
    func = getattr(shapes, funcname)

    def wrap_func(*a, **k):
        try:

            return func(*a, **k)
        except TypeError as e:
            print("TypeError!!!: ", e, funcname, a, k)
        except ValueError:
            pass

    return wrap_func


class Letter:
    func = None
    DEBUG = False
    play = True
    points = None

    def __init__(self, x, y, color=None) -> None:
        self.x0 = x
        self.y0 = y
        self.x = 0
        self.y = 0
        self.t = random.random() * 100
        self.points = []
        self.color = color or DRAW_COLOR

        self.randomize()

    def randomize(self):
        self.func = get_random_func()
        self.a = random.random() * 60 - 30
        self.b = random.random() * 60 - 30
        self.c = random.random() * 60 - 30

    def update(self):
        if not self.play:
            return

        if pyxel.frame_count % 100 == 0:
            self.randomize()

        res = self.func(self.t, a=self.a, b=self.a, c=self.a)
        if res:
            self.x, self.y = res

        x = self.x + self.x0
        y = self.y + self.y0

        RECT_X = self.x0 - LETTER_WIDTH / 2
        RECT_Y = self.y0 - LETTER_WIDTH / 2

        if (
            x > RECT_X and
            x < RECT_X + LETTER_WIDTH and
            y > RECT_Y and
            y < RECT_Y + LETTER_WIDTH
        ):
            self.points.append((x, y))

        if self.t % 15 < 0.1:
            if len(self.points) < 200:
                self.points = self.points[-100:]
            else:
                self.play = False
                return

        self.t += 0.01

    def draw(self):
        for p in self.points:
            pyxel.pset(*p, self.color)

        if self.DEBUG:  # debug
            RECT_X = self.x0 - LETTER_WIDTH / 2
            RECT_Y = self.y0 - LETTER_WIDTH / 2

            RECT = (
                RECT_X - MARGIN, RECT_Y - MARGIN,
                LETTER_WIDTH + 2 * MARGIN,
                LETTER_WIDTH + 2 * MARGIN
            )

            pyxel.rectb(*RECT, 2)

            # pyxel.text(RECT_X, RECT_Y + LETTER_WIDTH, f'{self.t:.1f}', 3)
            pyxel.text(RECT_X + 1, RECT_Y + LETTER_WIDTH +
                       2, f'{len(self.points)}', 3)


# iterate through a range of values and iterate backward to the start:
def loop(t, start=0, end=4):
    time.sleep(0.1)
    return math.cos(t % math.pi * 2) * (end - start) / 2 + (end - start) / 2 + start


class App:
    chaos_mode = False
    letters = []
    debug = False

    def __init__(self, ):
        pyxel.init(WIDTH, HEIGHT, "14 Asemic", fps=60, quit_key=pyxel.KEY_Q)

        colored_column = -1
        color = random.choice(
            list(set(DRAW_COLORS) - {DRAW_COLOR})
        )
        for j in range(
            int(MARGIN + LETTER_WIDTH / 2),
            HEIGHT,
            int(LETTER_WIDTH + MARGIN)
        ):

            for i in range(
                int(MARGIN + LETTER_WIDTH / 2),
                WIDTH,
                int(LETTER_WIDTH + MARGIN)
            ):
                if colored_column == -1 and random.random() < 0.1:
                    colored_column = i

                self.letters.append(
                    Letter(
                        i, j,
                        color=color if i == colored_column else DRAW_COLOR
                    )
                )

        pyxel.cls(BACKGROUND_COLOR)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_C):
            self.chaos_mode = not self.chaos_mode

        if pyxel.btnp(pyxel.KEY_D):
            self.debug = not self.debug
            for letter in self.letters:
                letter.DEBUG = self.debug
            if not self.debug:
                pyxel.cls(BACKGROUND_COLOR)

        for letter in self.letters:
            letter.update()

    def draw(self):
        if not self.chaos_mode:
            pyxel.cls(BACKGROUND_COLOR)

        for letter in self.letters:
            letter.draw()


App()
