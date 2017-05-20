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
import Cluster
import HStruct
import Paths
import HistLib
import Fonts
import Options
import os

pygame_sdl2.mixer.pre_init(44100)
pygame_sdl2.init()

assets = {}
entities = []

defaultMode = Options.getMode()
(screenWidth, screenHeight, _flags) = defaultMode # split tuple for easier access
del(_flags) # ... but we don't need that

timer = pygame_sdl2.time.Clock()

modeWidth = -1
modeHeight = -1
gamewindow = None
updateRects = []

currlvl = None
lvlname = None
wm = None

timeDelta = 0
timeTotal = 0

callbacks = {}

def callback(delay, fun, args):
	global callbacks, timeTotal
	callbacks[timeTotal + delay] = (fun, args)

def setResolution(width, height, flags = 0):
	global modeWidth, modeHeight, gamewindow, updateRects
	modeWidth = width
	modeHeight = height
	gamewindow = pygame_sdl2.display.set_mode((width, height), flags)
	updateRects = [(0, 0, width, height)]

loaders = {"graphics": lambda x: pygame_sdl2.image.load(x).convert_alpha(),
		"sounds": pygame_sdl2.mixer.Sound,
		"fonts": Fonts.Font}

def loadResource(fname):
	name = os.path.join(Paths.assets, fname)
	for dirname, loader in loaders.iteritems():
		if fname.startswith(dirname):
			return loader(name)
	with open(name) as f:
		# Fallback: contents of file as string
		return f.read()

def getLevel(fname):
	return os.path.join(Paths.assets, "levels", fname)

def loadLevelCluster(clus):
	global currlvl, wm, theme, updateRects, timeDelta, timeTotal, mousepos, events, modeWidth, modeHeight
	timeTotal = 0
	newlvl = clus
	newlvl.loop = True
	newlvl.tail = None
	newlvl.args = ()
	wm = newlvl.header.wm()
	theme = {key:loadResource(value) for key, value in newlvl.header.theme.iteritems()}
	if currlvl:
		for (name, persist) in currlvl.header.mutables:
			if persist:
				newlvl.__dict__[name] = currlvl.__dict__[name]
	currlvl = newlvl
	
	currlvl.header.scr.startLevel()
	
	while currlvl.loop:
		timeDelta = timer.tick()
		timeTotal += timeDelta
		events = [event for event in pygame_sdl2.event.get()]
		for event in events:
			if event.type == pygame_sdl2.ACTIVEEVENT:
				updateRects = [(0, 0, modeWidth, modeHeight)]
		mousepos = pygame_sdl2.mouse.get_pos()
		for point, (fun, args) in callbacks.iteritems():
			if timeTotal >= point:
				fun(*args)
				callbacks.remove(point) 
		wm.update()
		pygame_sdl2.display.update(updateRects)
		updateRects = []	
			
	if currlvl.tail:
		currlvl.tail(*currlvl.args)

def loadLevelStr(fname):
	global lvlname
	lvlname = fname
	loadLevelCluster(Cluster.Cluster(getLevel(fname)))

def loadLevel(loadFrom):
	if isinstance(loadFrom, str):
		loadLevelStr(loadFrom)
	elif isinstance(loadFrom, Cluster.Cluster):
		loadLevelCluster(loadFrom)
	else:
		raise TypeError

def endLevel(function, arguments = ()):
	global currlvl
	currlvl.loop = False
	currlvl.tail = function
	currlvl.args = arguments
