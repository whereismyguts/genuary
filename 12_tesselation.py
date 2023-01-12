from turtle import color
import pyxel
import random
import time

# The size of the screen
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
BACKGROUND_COLOR = 2


A = 20
H = (3**0.5) * A / 2

H /= 1.5


def dark_color(color):
    return {
        6: 5,
        10: 9,
        11: 3,
        14: 8,
    }[color]


class App():
    offset_x = 0
    offset_y = 0

    _cells = dict()

    def cells(self, x, y):
        index = (int(x), int(y))
        if self._cells.get(index) is None:
            self._cells[index] = dict(
                color=random.choice([6, 10, 11, 14]),
                bevel=random.randint(5, 30),
                up=random.randint(0, 1),
                # speed=random.randint(1, 3),
                max_up=random.randint(10, 100),
            )
        else:
            bevel = self._cells[index]['bevel']
            up = self._cells[index]['up']
            speed = bevel / 50
            if up:
                if bevel < self._cells[index]['max_up']:
                    bevel += speed
                else:
                    up = False
            else:
                if bevel > 1:
                    bevel -= speed
                else:
                    up = True

            self._cells[index]['bevel'] = bevel
            self._cells[index]['up'] = up

        return self._cells[index]

    def __init__(self) -> None:

        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
        pyxel.run(self.update, self.draw)

    def update(self):
        # self.offset_x += 0.5 - random.random()
        # self.offset_y += 0.5 - random.random()
        # self.offset_h = random.randint(0, 10)
        pass

    def draw(self):

        pyxel.cls(BACKGROUND_COLOR)
        # for i in range(0, SCREEN_WIDTH, 1.5*a):

        j = self.offset_y
        j_is_odd = False
        while j < SCREEN_HEIGHT:
            i = self.offset_x
            i_is_odd = False
            while i < SCREEN_WIDTH:
                # for j in range(10, SCREEN_HEIGHT, 2*h):

                if i_is_odd != j_is_odd:
                    # pyxel.circ(i, j, 2, 8)
                    # drawing a hexagon around the point:
                    chaos = 0  # random.randint(2, 10)
                    a = A - chaos
                    h = H - chaos
                    relative_points = [

                        (-a, 0, -a / 2, h),  # bottom left
                        (-a / 2, h, a / 2, h),  # bottom
                        (a / 2, h, a, 0),  # bottom right

                        # (a, 0, a / 2, -h), # top right
                        # (a / 2, -h, -a / 2, -h), # top
                        # (-a / 2, -h, -a, 0)  # top left

                    ]

                    c = self.cells(i, j)['color']
                    dark_c = dark_color(c)

                    relative_points = [

                        (-a, 0, -a / 2, h),
                        (-a / 2, h, a / 2, h),
                        (a / 2, h, a, 0),

                        (a, 0, a / 2, -h),
                        (a / 2, -h, -a / 2, -h),
                        (-a / 2, -h, -a, 0)

                    ]

                    bevel = self.cells(i, j)['bevel']
                    for p in relative_points:
                        pyxel.tri(
                            i + p[0], j + p[1] - bevel,
                            i + p[2], j + p[3] - bevel,
                            i, j, c
                        )

                    pyxel.rect(
                        i - a / 2, j + h - bevel, a, bevel, dark_c
                    )

                    for p in [
                        (-a, 0, -a / 2, h),  # bottom left
                        (-a / 2, h, a / 2, h),  # bottom
                        (a / 2, h, a, 0),  # bottom right
                    ]:
                        for dy in range(1, int(bevel)):
                            pyxel.line(
                                i + p[0], j + p[1] - dy,
                                i + p[2], j + p[3] - dy,
                                dark_c
                            )

                    for p in relative_points:
                        pass
                        # pyxel.trib(
                        #     i + p[0], j + p[1] - bevel,
                        #     i + p[2], j + p[3] - bevel,
                        #     i, j - bevel, 0
                        # )
                        # pyxel.line(
                        #     i + p[0], j + p[1] - bevel,
                        #     i + p[2], j + p[3] - bevel,
                        #     0
                        # )
                        # else:
                        #     pyxel.circ(i, j, 2, 7)
                i_is_odd = not i_is_odd
                i += A * 1.5
            j += H
            j_is_odd = not j_is_odd


App()
