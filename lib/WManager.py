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
# WManager.py - Window manager implementations

import Engine, HStruct, Events, Element, HistLib
import pygame_sdl2

# Window class
exec(HStruct.Gwe("Window", "Engine.wm", "w", "h", "x", "y", "objs", "hover", "events") + """
	def mouse(self, x, y, event):
		if event in self.events:
			self.events[event]()
		else:
			rel = (x - self.x, y - self.y)
			for obj in reversed(self.objs):
				if isinstance(obj, Element.Sprite) and obj.rect.collidepoint(rel):
					if self.hover != obj:
						if self.hover:
							self.hover.event(Events.MOUSEOUT)
						self.hover = obj
						self.hover.event(Events.MOUSEOVER)
					if event:
						obj.event(event)
					break
	def update(self):
		for obj in self.objs:
			obj.update()
	def blit(self, image, x, y):
		Engine.wm.blit(self, image, x, y)
	def addObj(self, cls, *args):
		obj = cls(*(self,) + args)
		self.objs.append(obj)
		return obj
	rect = property(lambda self: pygame_sdl2.Rect(self.x, self.y, self.w, self.h))
""")

# Base class for all implementations. Derivatives should define blit()
# and updateGame().
class Man:
	def __init__(self):
		self.windows = []
	
	def createWindow(self, w, h, x = -1, y = -1):
		win = Window(w, h, x, y, [], None, [])
		self.windows.append(win)
		return win
	
	def getEvent(self):
		hevent = None
		for pyevent in Engine.events:
			if pyevent.type == pygame_sdl2.MOUSEBUTTONUP:
				hevent = Events.MOUSEUP
			elif pyevent.type == pygame_sdl2.KEYDOWN or pyevent.type == pygame_sdl2.KEYUP:
				tmp = "KEY"
				if pyevent.type == pygame_sdl2.KEYDOWN:
					tmp += "DOWN"
				else:
					tmp += "UP"
				tmp += pygame_sdl2.key.name(pyevent.key)
				if tmp in Events.events:
					hevent = eval("Events." + tmp)
				del tmp
		return hevent
	
	exec(HStruct.Sts("w", "h", "x", "y", "objs", "hover", "events"))

# Used for the launcher. Does not actually manage windows.
class Shim(Man):
	def __init__(self):
		Man.__init__(self)
		Engine.setResolution(478, 322)
		pygame_sdl2.display.set_caption("Welcome to " + HistLib.productName)
	
	def createWindow(self, w, h, x = -1, y = -1):
		Engine.setResolution(w, h)
		return Man.createWindow(self, w, h, 0, 0)
	
	def blit(self, window, image, x, y):
		Engine.gamewindow.blit(image, (x, y))
	
	def updateGame(self):
		hevent = self.getEvent()
		for win in self.windows:
			if win.rect.collidepoint(Engine.mousepos):
				win.mouse(*Engine.mousepos + (hevent,))
			win.update()

# Standard floating window manager. This or a derivative of it will
# probably be used in most levels.
class Floating(Man):
	pass
