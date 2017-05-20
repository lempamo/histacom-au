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
# Fonts.py - font-related classes

import HStruct, HistLib, InterOp, PIL.Image, pygame_sdl2, cStringIO

# A bitmap font format which behaves similarly to pygame.font.Font.
# This is not a HistLib.Format and cannot be saved by the game engine.
class HFont(HistLib.saneobject):
	# default character (for height calculations and missing characters)
	_dchar = property(lambda self: self._characters[" "])
	
	def _getchar(self, char):
		if char in self._characters:
			return self._characters[char]
		else:
			return self._dchar
	
	def _getcolour(self, colour):
		if colour in self._colours:
			return self._colours[colour]
		im = self._image
		if len(colour) != 3:
			raise TypeError
		entry = "".join(chr(x) for x in colour) # stringify RGB tuple
		im.palette = im.palette[:3] + entry # replace index 1
		surf = im.surface
		self._colours[colour] = surf
		return surf
	
	def size(self, text):
		h = self._dchar.height # HFonts should be fixed height
		w = 0
		for char in text:
			w += self._getchar(char).width
		return (w, h)
	
	def render(self, text, aa, colour, bg = None): # aa is ignored
		src = self._getcolour(colour)
		dest = pygame_sdl2.Surface(self.size(text))
		if bg:
			dest.fill(bg)
		p = 0
		for char in text:
			rect = self._getchar(char)
			dest.blit(src, (p, 0), rect)
			p += rect.width
		return dest
	
	def _LoadF(self, fobj):
		if fobj.read(4) != "Font":
			raise HistLib.WrongFiletypeException("This is not a Histacom.AU Bitmap Font")
		
		self._characters = {}
		
		# Read image file
		imsize = HistLib.ReadBytes(fobj, 4)
		image = cStringIO.StringIO(HistLib.read(imsize))
		self._image = PIL.Image.open(image)
		self._image.load()
		image.close()
		self._colours = {}
		
		# Read spritesheet table
		startentry = HistLib.ReadBytes(fobj, 2)
		endentry = HistLib.ReadBytes(fobj, 2)
		for i in range(startentry, endentry):
			for t in ["x", "y", "w", "h"]:
				locals()[t] = HistLib.ReadBytes(fobj, 2)
			self._characters[chr(i + 1)] = pygame_sdl2.Rect(x, y, w, h)
	
	def _LoadStr(self, fname):
		with open(fname, "rb") as f:
			self._LoadF(f)
	
	def __init__(self, loadFrom, size = None): # size is ignored
		if isinstance(loadFrom, str):
			return self._LoadStr(loadFrom)
		elif isinstance(loadFrom, file):
			return self._LoadF(loadFrom)
		else:
			raise TypeError

# A dynamic dictionary of pygame vector fonts. The key is the size.
# You can load a font file once and then get multiple sizes of it.
class Font(HistLib.saneobject):
	def __init__(self, fname):
		with open(fname) as f:
			data = f.read()
		self.stream = cStringIO.StringIO(data)
		self._pyfonts = {}
	def initSize(self, size):
		if size not in self._pyfonts:
			self._pyfonts[size] = pygame_sdl2.font.Font(self.stream, size)
			self.stream.seek(0)
	def __getitem__(self, size):
		self.initSize(size)
		return self._pyfonts[size]