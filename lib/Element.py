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

# Checks if two Pygame Rects have the same position and size.
# The equality operator doesn't seem to work for this.
def sameRect(r1, r2):
	for attr in ["x", "y", "width", "height"]:
		if getattr(r1, attr) != getattr(r2, attr):
			return False
	return True

# Derivatives should define update().
class Element(HistLib.saneobject):
	def __init__(self):
		self.events = {}
	
	def event(self, event):
		if event in self.events:
			self.events[event]()

# An element that has a rectangle.
class Box(Element):
	def __init__(self, parent, x, y, w, h):
		Element.__init__(self)
		self.parent = parent
		for prop in ["x", "y", "w", "h"]:
			self.__dict__["_" + prop] = eval(prop)
		
	def setRect(self, x, y, w, h):
		oldRect = self.rect
		self._x = x
		self._y = y
		self._w = w
		self._h = h
		newRect = self.rect
		if not sameRect(oldRect, newRect):
			for rect in [oldRect, newRect]:
				self.parent.updateRect(rect)
	
	def setPos(self, x, y):
		self.setRect(x, y, self.w, self.h)
	
	rect = property(lambda self: pygame_sdl2.Rect(self.x, self.y, self.w, self.h), lambda self, rect: self.setRect(rect.x, rect.y, rect.width, rect.height))
	pos = property(lambda self: (self.x, self.y), lambda self, pos: self.setPos(*pos))
	x = property(lambda self: self._x, lambda self, val: self.setRect(val, self.y, self.w, self.h))
	y = property(lambda self: self._y, lambda self, val: self.setRect(self.x, val, self.w, self.h))
	w = property(lambda self: self._w, lambda self, val: self.setRect(self.x, self.y, val, self.h))
	h = property(lambda self: self._h, lambda self, val: self.setRect(self.x, self.y, self.w, val))

# An element containing a list of elements that update at the same time
# as itself. Derivatives should usually define blit().
class Container(Element):
	def __init__(self, parent = None):
		Element.__init__(self)
		self.parent = parent
		self.objs = []
	
	def addObj(self, cls, *args, **kwargs):
		obj = cls(*(self,) + args, **kwargs)
		self.objs.append(obj)
		return obj
	
	def update(self):
		for obj in self.objs:
			obj.update()

# Fusion of Box and Container. Multiple inheritance!
class BoxContainer(Box, Container):
	def __init__(self, parent, x, y, w, h):
		Box.__init__(self, parent, x, y, w, h)
		Container.__init__(self, parent)
	
	def convertRect(self, rect):
		newRect = pygame_sdl2.Rect(rect) # copy
		newRect.x += self.x
		newRect.y += self.y
		newRect.width = min(self.rect.right, newRect.right) - newRect.x
		newRect.height = min(self.rect.bottom, newRect.bottom) - newRect.y
		return newRect
	
	def fill(self, colour, dest):
		self.parent.fill(colour, self.convertRect(dest))
	
	def blit(self, image, dest):
		self.parent.blit(image, self.convertRect(dest))
	
	def updateRect(self, rect):
		self.parent.updateRect(self.convertRect(rect))

# Box filled in with a colour.
class ColouredBox(Box):
	def __init__(self, parent, x, y, w, h, colour):
		Box.__init__(self, parent, x, y, w, h)
		self.colour = colour
	def update(self):
		self.parent.fill(self.colour, self.rect)
	def setColour(self, colour):
		self._colour = colour
		self.parent.updateRect(self.rect)
	colour = property(lambda self: self._colour, setColour)

# Image that can be moved around.
class Sprite(Box):
	def __init__(self, parent, x, y, im):
		Box.__init__(self, parent, x, y, im.get_width(), im.get_height())
		self.image = im
	
	def setimage(self, im):
		self._image = im
		(self._w, self._h) = im.get_size()
		self.parent.updateRect(self.rect)

	def update(self):
		self.parent.blit(self.image, self.rect)
	
	image = property(lambda self: self._image, setimage)

# Animated list of images.
class Animation(Sprite):
	def __init__(self, parent, x, y, images, startRunning = True):
		(im, dur) = images[0]
		Sprite.__init__(self, parent, x, y, im)
		self.pos = 0	# frame of the image
		self.dur = dur	# time this frame takes
		self.cur = 0	# time this Animation has been on this frame
		self._images = images
		self.running = startRunning
	def update(self):
		if len(self.images) > 1:	# if this actually *is* an animation
			if self.running:
				self.cur += Engine.timeDelta
				if self.cur > self.dur: # if it's time to flick over
					self.pos += 1 # go to the next frame
					if self.pos == len(self.images): # if we're past the end
						self.pos = 0 # go back to the start
					(self.image, self.dur) = self.images[pos]
		Sprite.update(self)
	def setimages(self, images):
		self._images = images
		(self.im, self.dur) = images[0]
		self.pos = 0
		self.cur = 0
	images = property(lambda self: self._images, setimages)

# Text that can be moved around and changed.
class Text(Box):
	properties = ["x", "y", "text", "font", "colour", "aa", "w", "h", "underline"]
	def __init__(self, parent, x, y, text, font, colour, aa = False, w = -1, h = -1, underline = 0):
		Element.__init__(self)
		self.parent = parent
		# This dict comprehension loops on every argument except "win" and
		# creates a dictionary mapping the argument name with "_" prepended
		# to the passed argument value.
		_locals = locals()
		self.modify(**{"_" + i: _locals[i] for i in self.properties})
	
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
				self.image = WordWrap.wrap(self.font, self.text, self.aa, self.colour, self.w, ul = bool(self.underline))
				break
		if self._w == -1:
			self._w = self.image.get_width()
		self._h = self.image.get_height()
		newRect = self.rect
		if oldRect and not sameRect(oldRect, newRect):
			if oldRect not in Engine.updateRects:
				self.parent.updateRect(oldRect)
		if newRect not in Engine.updateRects:
			self.parent.updateRect(newRect)
	
	def setRect(self, x, y, w, h):
		self.modify(_x = _x, _y = y, _w = w, _h = h)
	
	def setPos(self, x, y):
		self.modify(_x = x, _y = y)
	
	def update(self):
		self.parent.blit(self.image, self.rect)
	
	for setting in properties:
		exec("{0} = property(lambda self: self._{0}, lambda self, val: self.modify(_{0} = val))".format(setting))
	
	rect = property(lambda self: pygame_sdl2.Rect(*(self.x, self.y) + self.image.get_size()), setRect)

# A collection of Text items with different formatting. Experimental.
class RichText(BoxContainer):
	def __init__(self, parent, x, y, w, document):
		BoxContainer.__init__(self, parent, x, y, w, 0)
		self.document = document
	
	def addLine(self, line, y):
		x = 0
		h = 0
		fam = None
		fontdict = None
		font = None
		for i in line:
			colour = i.state["c"]
			famname = i.state["f"]
			try:
				fam = Engine.theme[famname]
			except KeyError:
				print("warning: {0} not in theme of {1}".format(famname, Engine.lvlname))
			bold = i.state["b"]
			italic = i.state["i"]
			aa = i.state["aa"]
			size = i.state["fs"]
			underline = i.state["u"]
			try:
				fontdict = fam[(bold, italic, aa)]
			except KeyError:
				print("warning: family {0} does not have an entry for {1}".format(famname, (bold, italic, aa)))
			try:
				font = fontdict[size]
			except KeyError:
				print("warning: font {0}[{1}] is not available in size {2}".format(famname, (bold, italic, aa), size))
			if font:
				text = self.addObj(Text, x, y, i.text, font, colour, aa, underline = underline)
				x += text.w
				if text.h > h:
					h = text.h
		return h
	
	def setDocument(self, document):
		self._document = document
		self.objs = []
		h = 0
		for line in document:
			h += self.addLine(line, h)
		self.setRect(self.x, self.y, self.w, h)
		
	document = property(lambda self: self._document, setDocument)
	