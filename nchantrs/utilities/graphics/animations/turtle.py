# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name:
	description: >
	version: 0.0.0.0.0.0
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import dirname, join
from random import randint

import logging
# ======================================3rd Party Library Modules=====================================================||

logger = logging.getLogger(__name__)

# ======================================Solutions Brewer Library Modules==============================================||
from ogma.logma import Logma

# ====================================================================================================================||
# Constants for magic number replacement
DEFAULT_ANIMATION_FRAMES = 100
DEFAULT_FRAME_DELAY = 0.05
DIRECTION_HORIZONTAL = 0
DIRECTION_VERTICAL = 1
TURTLE_COLOR_MODES = {
    0: "background",
    1: "accent",
}

# ====================================================================================================================||
here = join(dirname(__file__), '')  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, '_data_', '.yaml')

def get_number(max_n):
    """"""
    while True:
        n = randint(int(max_n*0.05), max_n)
        yield n

def turn(t, cnt, direction):
    """Turn the turtle and return new direction"""
    t[cnt].right(90)
    if direction == DIRECTION_HORIZONTAL:
        direction = DIRECTION_VERTICAL
    else:
        direction = DIRECTION_HORIZONTAL
    return direction

def animation_panel(background, accent):
    """"""
    # Set up the screen
    win = turtle.Screen()
    win.bgcolor("black")
    bounds = [100, 100]

    # Create a turtle object
    t = {}
    # This will control speed of animation
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
            logger.debug("Turtle position: %s", pos)
        t[cnt].hideturtle()
        cnt += 1

# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
