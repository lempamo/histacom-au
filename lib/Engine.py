# Copyright 2017 Declan Hoare
# This file is part of Histacom.AU.
#
# Histacom.AU is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Histacom.AU is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Histacom.AU.  If not, see <http://www.gnu.org/licenses/>.
#
# Engine.py - take a wild guess what this is

import pygame_sdl2

pygame_sdl2.init()

assets = {}
entities = []

i = pygame_sdl2.display.Info()
screenWidth = i.current_w
screenHeight = i.current_h
del i

modeWidth = -1
modeHeight = -1
gamewindow = None
updateRects = []

def setResolution(width, height, flags = 0):
	global modeWidth, modeHeight, gamewindow, updateRects
	modeWidth = width
	modeHeight = height
	gamewindow = pygame_sdl2.display.set_mode((screenWidth, screenHeight), flags)
	updateRects = [(0, 0, screenWidth, screenHeight)]

def configureBg(self):
	