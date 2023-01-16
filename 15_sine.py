from ast import parse
import pyxel
import random
import time
import math


SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256


def sine_wave(x, amplitude, frequency, phase_shift):
    y = amplitude * math.sin(frequency * x + phase_shift)
    return y


def spiral(t, a, b):

    x = a * t * math.cos(t)
    y = b * t * math.sin(t)
    return x, y


def spiral(x, a, b):
    t = x
    x = a * t * math.cos(t)
    y = b * t * math.sin(t)
    return x, y


def loop(t, start, end, step):
    return start + ((t * step) % (2 * (end - start))) if (t * step) % (2 * (end - start)) < end - start else end - ((t * step) % (2 * (end - start)) - (end - start))


def rotate(x, y, angle):
    return (x * math.cos(angle) - y * math.sin(angle), x * math.sin(angle) + y * math.cos(angle))


class App:
    x = 0
    y = 0

    def __init__(self):
        pyxel.init(
            SCREEN_WIDTH, SCREEN_HEIGHT,
            "15 Sine waves",
            fps=60,
            quit_key=pyxel.KEY_Q
        )

        self.amp = 10

        pyxel.run(self.update, self.draw)

    def update(self):
        #  self.x = loop(pyxel.frame_count, -100, 100, 0.01)
        # self.x = pyxel.frame_count / 10
        # self.y = sine_wave(self.x, 100, 30, 0)
        # time.sleep(0.1)
        self.amp = loop(pyxel.frame_count, 0, 16, 0.01)
        pass

    def draw(self):
        pyxel.cls(0)

        fq = 0.1

        # ph = random.random()
        for dx in range(int(-SCREEN_WIDTH * 40), int(SCREEN_WIDTH * 2), 1):
            dx = dx / 100
            x = dx
            y = sine_wave(
                x, self.amp, fq,
                (pyxel.frame_count % 60) / 10
            ) + fq * 2
            x = x + SCREEN_WIDTH / 2
            y = y + 50

            # pyxel.line(x, y, x, y + thickness, 4)
            # pyxel.pset(
            #     x, y, 7
            # )
            # pyxel.pset(x, y + thickness, 8)

            p = rotate(x, y, math.pi / 3 * x % math.pi * 2 - math.pi)

            p = (p[0] + SCREEN_WIDTH / 2, p[1] + SCREEN_HEIGHT / 2)
            pyxel.pset(*p, 9)

        # self.x = loop(pyxel.frame_count, -100, 100, 1)
        # # self.x = pyxel.frame_count / 10
        # self.y = sine_wave(self.x, 10, 0.1, pyxel.frame_count % 10)
        # time.sleep(0.1)
        # pyxel.pset(self.x + SCREEN_WIDTH / 2, self.y + SCREEN_HEIGHT / 2, 7)


App()
