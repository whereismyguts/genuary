
import pyxel
import random
import time
import math
# The size of the screen
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
BACKGROUND_COLOR = 1
LINE_COLOR = 1

A = 20
H = (3**0.5) * A / 2
H /= 1.5  # sclaing the height to make it look better


def dark_color(color):
    return {
        6: 5,
        10: 9,
        11: 3,
        14: 8,
    }[color]


class App():
    _cells = dict()

    def cells(self, x, y):
        index = (int(x), int(y))
        if self._cells.get(index) is None:
            self._cells[index] = dict(
                color=random.choice([6, 10, 11, 14]),
                bevel=random.randint(5, 30),
                is_up_direction=random.choice([-1, 1]),
                speed=random.random(),  # TODO ease in and out
                max_up=random.randint(10, 20),
                t=random.randint(0, 5),
                chaos=(random.randint(95, 100) / 100)
            )

        return self._cells[index]

    def __init__(self) -> None:

        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, '12 Tesselation', fps=60)
        pyxel.run(self.update, self.draw, )

    def update(self):

        for c in self._cells.values():
            bevel = c['bevel']

            is_up_direction = c['is_up_direction']
            speed = bevel / 10 * c['speed']
            if is_up_direction:
                if bevel < c['max_up']:
                    bevel += speed
                else:
                    is_up_direction = False
            else:
                if bevel > 1:
                    bevel -= speed
                else:
                    is_up_direction = True

            c['bevel'] = bevel
            c['is_up_direction'] = is_up_direction

    def debuga(self):
        return
        pyxel.text(0, 0, str(self.divide), 0)
        pyxel.text(0, 10, '{} -> {}'.format(
            time.time(),
            (math.sin(time.time() * 0.5) + 1) / 2
        ), 0)

    def draw(self):

        pyxel.cls(BACKGROUND_COLOR)
        # for i in range(0, SCREEN_WIDTH, 1.5*a):
        j = 0
        j_is_odd = False
        x_offset = 0
        while j < SCREEN_HEIGHT:

            i = 0

            i_is_odd = False
            while i < SCREEN_WIDTH:
                # for j in range(10, SCREEN_HEIGHT, 2*h):

                if i_is_odd != j_is_odd:
                    # pyxel.circ(i, j, 2, 8)
                    # drawing a hexagon around the point:
                    chaos = self.cells(i, j)['chaos']
                    a = A * chaos
                    h = H * chaos

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

                    # top face:
                    for p in relative_points:
                        pyxel.tri(
                            x_offset + i + p[0], j + p[1] - bevel,
                            x_offset + i + p[2], j + p[3] - bevel,
                            x_offset + i, j, c
                        )

                    # front face:
                    pyxel.rect(
                        x_offset + i - a / 2, j + h - bevel, a, bevel, dark_c
                    )

                    # top face lines:
                    for p in [
                        (-a, 0, -a / 2, h),  # bottom left
                        (-a / 2, h, a / 2, h),  # bottom
                        (a / 2, h, a, 0),  # bottom right

                        (a, 0, a / 2, -h),  # top right
                        (a / 2, -h, -a / 2, -h),  # top
                        (-a / 2, -h, -a, 0)  # top left
                    ]:
                        pyxel.line(
                            x_offset + i + p[0], j + p[1] - bevel,
                            x_offset + i + p[2], j + p[3] - bevel,
                            LINE_COLOR
                        )
                        pyxel.line(
                            x_offset + i + p[0], j + p[1] - bevel + 1,
                            x_offset + i + p[2], j + p[3] - bevel + 1,
                            LINE_COLOR
                        )

                    # left/right side
                    for p in [
                        (-a, 0, -a / 2, h),  # bottom left
                        # (-a / 2, h, a / 2, h),  # bottom
                        (a / 2, h, a, 0),  # bottom right
                    ]:
                        for dy in range(0, math.ceil(bevel) - 1):
                            pyxel.line(
                                x_offset + i + p[0], j + p[1] - dy,
                                x_offset + i + p[2], j + p[3] - dy,
                                dark_c
                            )

                    # vertical lines:
                    for p in [
                        (-a, 0,),
                        (-a / 2, h),  # bottom left
                        (a / 2, h),  # bottom
                        (a, 0),  # bottom right
                    ]:
                        pyxel.line(
                            x_offset + i + p[0], j + p[1],
                            x_offset + i + p[0], j + p[1] - bevel,
                            LINE_COLOR
                        )

                if i_is_odd:
                    i += A * 0.1

                i_is_odd = not i_is_odd
                i += A * 1.5

            # x_offset += 1
            j += H
            j_is_odd = not j_is_odd

        self.debuga()


App()
