from typing import Any, Iterator
'\n---\n<(META)>:\n        docid:\n        name:\n        description: >\n        version: 0.0.0.0.0.0\n        authority: filesystem\n        security: seclvl2\n        <(WT)>: -32\n'
from os.path import dirname, join
from random import randint
import logging
logger = logging.getLogger(__name__)
from kahndor.logma import Logma
DEFAULT_ANIMATION_FRAMES = 100
DEFAULT_FRAME_DELAY = 0.05
DIRECTION_HORIZONTAL = 0
DIRECTION_VERTICAL = 1
TURTLE_COLOR_MODES = {0: 'background', 1: 'accent'}
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', '.yaml')

def get_number(max_n) -> Iterator[Any]:
    """"""
    while True:
        n = randint(int(max_n * 0.05), max_n)
        yield n

def turn(t, cnt, direction) -> str:
    """Turn the turtle and return new direction"""
    t[cnt].right(90)
    if direction == DIRECTION_HORIZONTAL:
        direction = DIRECTION_VERTICAL
    else:
        direction = DIRECTION_HORIZONTAL
    return direction

def animation_panel(background, accent) -> None:
    """"""
    win = turtle.Screen()
    win.bgcolor('black')
    bounds = [100, 100]
    t = {}
    frame_delay = DEFAULT_FRAME_DELAY
    x = get_number(int(bounds[0] / 3))
    y = get_number(int(bounds[1] / 3))
    cnt = 0
    while True:
        if cnt not in t.keys():
            t[cnt] = turtle.Turtle()
        if cnt == 0:
            t[cnt].color(background)
        elif cnt == 1:
            t[cnt].color(accent)
        else:
            cnt = 0
        direction = DIRECTION_HORIZONTAL
        t[cnt].goto(0, 0)
        t[cnt].clear()
        pos = [0, 0]
        for i in range(DEFAULT_ANIMATION_FRAMES):
            if direction == DIRECTION_HORIZONTAL:
                move = next(x)
            else:
                move = next(y)
            direction = turn(t, cnt, direction)
            if pos[direction] + move >= bounds[direction]:
                move = -move
            pos[direction] += move
            if move > 0:
                t[cnt].forward(move)
            else:
                t[cnt].backward(move)
            logger.debug('Turtle position: %s', pos)
        t[cnt].hideturtle()
        cnt += 1