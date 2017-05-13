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

import Engine, HStruct, Events, Element
import pygame_sdl2

# Window class
exec(HStruct.Gwe("Window", "wm", "w", "h", "x", "y", "objs", "hover") + """
	def mouse(self, x, y):
		rel = (x - self.x, y - self.y)
		for obj in self.objs:
			if obj != self.hover:
				if isinstance(obj, Element.Sprite) and obj.rect.collidepoint(rel):
					if self.hover:
						self.hover.event(Events.MOUSEOUT)
					self.hover = obj
					self.hover.event(Events.MOUSEOVER)
	def update(self):
		for obj in self.objs:
			obj.update()
	def blit(self, image, x, y):
		Engine.wm.blit(self, image, x, y)
	def addObj(self, cls, *args):
		self.objs.append(cls(*(self,) + args))
	rect = property(lambda self: pygame_sdl2.Rect(self.x, self.y, self.w, self.h))
""")

# Base class for all implementations.
class Man:
	def __init__(self):
		self.windows = []
	
	def createWindow(self, w, h, x = -1, y = -1):
		win = Window(w, h, x, y, [], None)
		self.windows.append(win)
		return win
	
	exec(HStruct.Sts("w", "h", "x", "y", "objs"))

# Used for the launcher. Does not actually manage windows.
class Shim(Man):
	def __init__(self):
		self.windows = []
		Engine.setResolution(800, 600)
	
	def createWindow(self, w, h, x = -1, y = -1):
		Engine.setResolution(w, h)
		return Man.createWindow(self, w, h, 0, 0)
	
	def blit(self, window, image, x, y):
		Engine.gamewindow.blit(image, (x, y))
	
	def updateGame(self):
		mousepos = pygame_sdl2.mouse.get_pos()
		for win in self.windows:
			if win.rect.collidepoint(mousepos):
				win.mouse(*mousepos)
			win.update()

# Standard floating window manager. This or a derivative of it will
# probably be used in most levels.
class Floating(Man):
	pass
