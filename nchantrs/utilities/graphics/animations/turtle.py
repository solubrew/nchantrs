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
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from ogma.logma import Logma

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
    t[cnt].right(90)
    if direction == 0:
        direction = 1
    else:
        direction = 0
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
	frame_delay = 0.05
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

		# elif cnt == 2:
		# 	t[cnt].color("purple")
		# elif cnt == 3:
		# 	t[cnt].color("blue")
		# elif cnt == 4:
		# 	t[cnt].color("yellow")
		# elif cnt == 5:
		# 	t[cnt].color("pink")

		else:
			cnt = 0
		direction = 0
		t[cnt].goto(0, 0)
		t[cnt].clear()
		pos = [0, 0]
		for i in range(100):
			if direction == 0:
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
			print(pos)
		t[cnt].hideturtle()
		cnt += 1

# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
