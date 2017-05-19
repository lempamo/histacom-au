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

import Engine, HistLib, WordWrap, HStruct
import pygame_sdl2

# Derivatives should define update().
class Element(HistLib.saneobject):
	def __init__(self):
		self.events = {}
	
	def event(self, event):
		if event in self.events:
			self.events[event]()

# An element that has a rectangle.
class Box(Element):
	properties = ["x", "y", "w", "h"]
	
	def __init__(self, parent, x, y, w, h):
		Element.__init__(self)
		self.parent = parent
		for prop in self.properties:
			self.__dict__["_" + prop] = eval(prop)
		
	def setRect(self, x, y, w, h):
		oldRect = self.rect
		self._x = x
		self._y = y
		self._w = w
		self._h = h
		newRect = self.rect
		if oldRect != newRect:
			for rect in [oldRect, newRect]:
				self.parent.updateRect(rect)
	
	rect = property(lambda self: pygame_sdl2.Rect(self.x, self.y, self.w, self.h), lambda self, rect: self.setRect(rect.x, rect.y, rect.width, rect.height))
	x = property(lambda self: self._x, lambda self, val: self.setRect(val, self.y, self.w, self.h))
	y = property(lambda self: self._y, lambda self, val: self.setRect(self.x, val, self.w, self.h))
	w = property(lambda self: self._w, lambda self, val: self.setRect(self.x, self.y, val, self.h))
	h = property(lambda self: self._h, lambda self, val: self.setRect(self.x, self.y, self.w, val))

# An element containing a list of elements that update at the same time
# as itself. Derivatives should usually define blit().
class Container(Element):
	def __init__(self):
		Element.__init__(self)
		self.objs = []
	
	def addObj(self, cls, *args):
		obj = cls(*(self,) + args)
		self.objs.append(obj)
		return obj
	
	def update(self):
		for obj in self.objs:
			obj.update()

# Fusion of Box and Container. Multiple inheritance!
class BoxContainer(Box, Container):
	def __init__(self, parent, x, y, w, h):
		Box.__init__(self, parent, x, y, w, h)
		Container.__init__(self)
	
	def convertRect(self, rect):
		newRect = pygame_sdl2.Rect(rect) # copy
		newRect.x += self.x
		newRect.y += self.y
		newRect.width = min(self.rect.right, newRect.right) - newRect.x
		newRect.height = min(self.rect.bottom, newRect.bottom) - newRect.y
		return newRect
	
	def blit(self, image, dest):
		self.parent.blit(image, self.convertRect(dest))
	
	def updateRect(self, rect):
		self.parent.updateRect(self.convertRect(rect))

# Image that can be moved around.
class Sprite(Box):
	def __init__(self, parent, x, y, image):
		im = Engine.theme[image]
		Box.__init__(self, parent, x, y, im.get_width(), im.get_height())
		self.image = im
	
	def setimage(self, im):
		self._image = im
		(self._w, self._h) = im.get_size()
		self.parent.updateRect(self.rect)

	def update(self):
		self.parent.blit(self.image, self.rect)
	
	image = property(lambda self: self._image, setimage)

# Text that can be moved around and changed.
# Probably doesn't work at the moment - not updated for the new refactor
class Text(Sprite):
	properties = ["text", "font", "size", "colour", "aa", "w"]
	def __init__(self, win, x, y, text, font, size, colour, aa = False, w = -1):
		Element.__init__(self)
		self.win = win
		# This dict comprehension loops on every argument except "win" and
		# creates a dictionary mapping the argument name with "_" prepended
		# to the passed argument value.
		self.modify(**{"_" + x: eval(x) for x in ["x", "y"] + self.properties})
	
	def modify(self, *args, **kwargs):
		try:
			oldRect = self.rect
		except AttributeError:
			oldRect = None
		for setting, val in kwargs.iteritems():
			self.__dict__[setting] = val
		# only redraw if non-positional attributes were modified
		for setting in kwargs:
			if setting != "x" and setting != "y":
				self._image = WordWrap.wrap(self.font[self.size], self.text, self.aa, self.colour, self.w)
				break
		newRect = self.rect
		if oldRect and oldRect != newRect:
			if oldRect not in Engine.updateRects:
				Engine.updateRects.append(oldRect)
		if newRect not in Engine.updateRects:
			Engine.updateRects.append(newRect)
	
	def setpos(self, x, y):
		self.modify(x = x, y = y)
	
	for setting in properties:
		exec("{0} = property(lambda self: self._{0}, lambda self, val: self.modify(_{0} = val))".format(setting))
	
	# disable modification of the image
	image = property(lambda self: self._image)
	def setimage(self, val):
		raise TypeError