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
# Element.py - component of a window

import Engine, pygame_sdl2

# Derivatives should define update().
class Element(object):
	def __init__(self):
		self.events = {}
	def event(self, event):
		if event in self.events:
			self.events[event]()

# Image that can be moved around.
class Sprite(Element):
	def __init__(self, win, x, y, image):
		Element.__init__(self)
		self.win = win
		self._x = x
		self._y = y
		self.image = Engine.currlvl.header.theme[image].obj
	
	def setpos(self, x, y):
		oldrect = self.rect
		self._x = x
		self._y = y
		newrect = self.rect
		if oldrect != newrect:
			if not oldRect in Engine.updateRects:
				Engine.updateRects.append(oldRect)
			if not newRect in Engine.updateRects:
				Engine.updateRects.append(newRect)
	
	def setimage(self, im):
		self._image = im
		newRect = self.rect
		if not newRect in Engine.updateRects:
			Engine.updateRects.append(newRect)
	
	def getrect(self):
		return pygame_sdl2.Rect((self.x, self.y) + self.image.get_size())
	
	def update(self):
		self.win.blit(self.image, self.x, self.y)
	
	image = property(lambda self: self._image, setimage)
	rect = property(getrect)
	x = property(lambda self: self._x, lambda self, val: self.setpos(val, self.y))
	y = property(lambda self: self._y, lambda self, val: self.setpos(self.x, val))