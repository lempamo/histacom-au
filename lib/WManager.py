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

import Engine, Events, Element, HistLib
import pygame_sdl2

# Window class
class Window(Element.BoxContainer):
	def __init__(self, parent, x, y, w, h):
		Element.BoxContainer.__init__(self, parent, x, y, w, h)
		self.hover = None
	def mouse(self, x, y, event):
		if event in self.events:
			self.events[event]()
		else:
			rel = (x - self.x, y - self.y)
			for obj in reversed(self.objs):
				if hasattr(obj, "rect") and obj.rect.collidepoint(rel):
					if self.hover != obj:
						if self.hover:
							self.hover.event(Events.MOUSEOUT)
						self.hover = obj
						self.hover.event(Events.MOUSEOVER)
					if event:
						obj.event(event)
					break

# Base class for all implementations.
class Man(Element.BoxContainer):
	def __init__(self):
		Element.BoxContainer.__init__(self, Engine.gamewindow, 0, 0, Engine.screenWidth, Engine.screenHeight)
	
	def createWindow(self, w, h, x = -1, y = -1):
		for (c, s) in [("x", "w"), ("y", "h")]:
			exec("""if {0} < 0:
	{0} = int(round(self.{1} / 2 - {1} / 2))""".format(c, s))
		return self.addObj(Window, x, y, w, h)
	
	def getEvent(self): # FIXME, needs a lot of work
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
				tmp += pygame_sdl2.key.name(pyevent.key).upper()
				if tmp in Events.events:
					hevent = eval("Events." + tmp)
				del tmp
		return hevent
	
	def update(self):
		hevent = self.getEvent()
		for obj in self.objs:
			if isinstance(obj, Window):
				if obj.rect.collidepoint(Engine.mousepos):
					obj.mouse(*Engine.mousepos + (hevent,))
			obj.update()
	
	def blit(self, image, dest):
		Engine.gamewindow.blit(image, self.convertRect(dest))
	
	def updateRect(self, rect):
		Engine.updateRects.append(self.convertRect(rect))

# Used for the launcher. Does not actually manage windows.
class Shim(Man):
	def __init__(self):
		Engine.setResolution(478, 322)
		Man.__init__(self)
		pygame_sdl2.display.set_caption("Welcome to " + HistLib.productName)
	
	def createWindow(self, w, h, x = -1, y = -1):
		Engine.setResolution(w, h)
		return Man.createWindow(self, w, h, 0, 0)

# Standard floating window manager. This or a derivative of it will
# probably be used in most levels.
class Floating(Man):
	def __init__(self):
		Engine.setResolution(*Engine.defaultMode)
		Man.__init__(self)
		pygame_sdl2.display.set_caption(HistLib.productName)
		self.bgcolour = None # set by startLevel()
	def update(self):
		if self.bgcolour:
			Engine.gamewindow.fill(self.bgcolour)
		Man.update(self)
