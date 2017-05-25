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

import HStruct, HistLib, InterOp, Paths
import PIL.Image, pygame_sdl2, cStringIO, os

# BMFont is a bitmap font format created by AngelCode. This
# implementation reads version 3 of the file format and provides
# methods similar to those of pygame.font.Font.
# This is not a HistLib.Format and cannot be saved by the game engine.
# It also cannot be easily embedded because it needs to read until the
# EOF.
exec(HStruct.Gen("bmchar", "x", "y", "width", "height", "xoffset", "yoffset", "xadvance", "page", "chnl"))
def _toRect(self):
	return pygame_sdl2.Rect(self.x, self.y, self.width, self.height)
bmchar.rect = property(_toRect)
class BMFont(HistLib.saneobject):
	version = 3
	
	# default character (for height calculations and missing characters)
	_dchar = property(lambda self: self.char[ord(" ")])
	
	def _getchar(self, char):
		if ord(char) in self.char:
			return self.char[ord(char)]
		else:
			return self._dchar
	
	def _getcolour(self, colour, page):
		if colour in self._colours:
			return self._colours[colour]
		al = self.page[page]
		if len(colour) != 3:
			raise TypeError
		im = PIL.Image.new("RGB", al.size, colour)
		im.putalpha(al)
		surf = im.surface
		self._colours[colour] = surf
		return surf
	
	def _getxadvance(self, text, pos):
		xadvance = self._getchar(text[pos]).xadvance
		if pos < len(text) - 1:
			pair = (ord(text[pos]), ord(text[pos + 1]))
			if pair in self.pair:
				xadvance += self.pair[pair]
		return xadvance
	
	def size(self, text):
		w = 0
		for pos in range(0, len(text)):
			w += self._getxadvance(text, pos)
		return (w, self.lineHeight)
	
	def set_underline(self, state):
		self.ul = state
	
	def get_underline(self):
		return self.ul
	
	def render(self, text, aa, colour, bg = None):
		if aa == (self.aa == 1): # (self.aa == 1) is True if the font is aliased and False if anti-aliased
			print("warning: BMFont was called with non-matching aa parameter")
		currpage = -1
		dest = pygame_sdl2.Surface(self.size(text), pygame_sdl2.SRCALPHA)
		if bg:
			dest.fill(bg)
		p = 0
		for pos, char in enumerate(text):
			bchar = self._getchar(char)
			if currpage != bchar.page:
				src = self._getcolour(colour[:3], currpage)
			dest.blit(src, (p + bchar.xoffset, bchar.yoffset), bchar.rect)
			p += self._getxadvance(text, pos)
		ulpos = self.base + 1
		if self.ul:
			pygame_sdl2.draw.line(dest, colour[:3], (0, ulpos), (p, ulpos), self.ul)
		return dest
	
	def _LoadF(self, fobj):
		if fobj.read(3) != "BMF": # yeah, 3-byte magic number :/
			raise HistLib.WrongFiletypeException("This is not a BMFont")
		version = HistLib.ReadBytes(fobj, 1)
		if version != self.version:
			raise HistLib.UnsupportedException("This file is version {0}, expected {1}".format(version, self.version))
		fsize = os.fstat(fobj.fileno()).st_size
		
		self._colours = {}
		self.ul = False
		
		self.page = []
		self.char = {}
		self.pair = {}
		
		while fobj.tell() != fsize: # while not at EOF
			ident = HistLib.ReadBytes(fobj, 1)
			size = HistLib.ReadBytes(fobj, 4)
			
			if ident == 1: # Info Block
				self.fontSize = HistLib.ReadBytes(fobj, 2, signed = True) # why is the font size signed? who knows?
				
				bitField = HistLib.ReadBytes(fobj, 1)
				self.smooth = HistLib.GetBit(bitField, 0)
				self.unicode = HistLib.GetBit(bitField, 1)
				self.italic = HistLib.GetBit(bitField, 2)
				self.bold = HistLib.GetBit(bitField, 3)
				self.fixedHeight = HistLib.GetBit(bitField, 4)
				
				self.charSet = HistLib.ReadBytes(fobj, 1)
				self.stretchH = HistLib.ReadBytes(fobj, 2)
				self.aa = HistLib.ReadBytes(fobj, 1)
				
				self.paddingUp = HistLib.ReadBytes(fobj, 1)
				self.paddingRight = HistLib.ReadBytes(fobj, 1)
				self.paddingDown = HistLib.ReadBytes(fobj, 1)
				self.paddingLeft = HistLib.ReadBytes(fobj, 1)
				
				self.spacingHoriz = HistLib.ReadBytes(fobj, 1)
				self.spacingVert = HistLib.ReadBytes(fobj, 1)
				
				self.outline = HistLib.ReadBytes(fobj, 1)
				self.fontName = HistLib.ReadCString(fobj)
			
			elif ident == 2: # Common Block
				self.lineHeight = HistLib.ReadBytes(fobj, 2)
				self.base = HistLib.ReadBytes(fobj, 2)
				
				self.scaleW = HistLib.ReadBytes(fobj, 2)
				self.scaleH = HistLib.ReadBytes(fobj, 2)
				
				self.pages = HistLib.ReadBytes(fobj, 2)
				bitField = HistLib.ReadBytes(fobj, 1)
				self.packed = HistLib.GetBit(bitField, 7)
				
				self.alphaChnl = HistLib.ReadBytes(fobj, 1)
				self.redChnl = HistLib.ReadBytes(fobj, 1)
				self.greenChnl = HistLib.ReadBytes(fobj, 1)
				self.blueChnl = HistLib.ReadBytes(fobj, 1)
			
			elif ident == 3: # Pages Block
				for i in range(0, self.pages):
					pagename = HistLib.ReadCString(fobj)
					self.page.append(PIL.Image.open(os.path.join(Paths.assets, "bmfonts", pagename)))
			
			elif ident == 4: # Chars Block
				num = size / 20
				for x in range(0, num):
					Id = HistLib.ReadBytes(fobj, 4)
					x = HistLib.ReadBytes(fobj, 2)
					y = HistLib.ReadBytes(fobj, 2)
					width = HistLib.ReadBytes(fobj, 2)
					height = HistLib.ReadBytes(fobj, 2)
					xoffset = HistLib.ReadBytes(fobj, 2, signed = True)
					yoffset = HistLib.ReadBytes(fobj, 2, signed = True)
					xadvance = HistLib.ReadBytes(fobj, 2, signed = True)
					page = HistLib.ReadBytes(fobj, 1)
					chnl = HistLib.ReadBytes(fobj, 1)
					self.char[Id] = bmchar(x, y, width, height, xoffset, yoffset, xadvance, page, chnl)
					
			elif ident == 5: # Kerning Pairs Block
				num = size / 10
				for i in range(0, num):
					first = HistLib.ReadBytes(fobj, 4)
					second = HistLib.ReadBytes(fobj, 4)
					amount = HistLib.ReadBytes(fobj, 2, signed = True)
					self.pair[(first, second)] = amount
			
			else: # Unknown block type - seek past it
				fobj.seek(size, os.SEEK_CUR)
			
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
class PFont(HistLib.saneobject):
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

# Organise a set of loose font files into a family for easier loading
# and access. The key is a (bold, italic, aa) tuple.
class Family(HistLib.Format):
	def _New(self):
		self.props = {}
	def _LoadF(self, fobj):
		if fobj.read(4) != "Fam!": # What up, fam squad?
			raise HistLib.WrongFiletypeException("This is not a Histacom.AU font family")
		num = HistLib.ReadBytes(fobj, 4)
		for i in range(0, num):
			bf = HistLib.ReadBytes(fobj, 1)
			vector = HistLib.GetBit(bf, 0)
			bold = HistLib.GetBit(bf, 1)
			italic = HistLib.GetBit(bf, 2)
			aa = HistLib.GetBit(bf, 3) # should always be True for vector fonts
			if vector:
				fname = HistLib.ReadOString(fobj)
				self.props[(bold, italic, aa)] = fname
			else:
				numB = HistLib.ReadBytes(fobj, 1)
				entry = {}
				self.props[(bold, italic, aa)] = entry # by reference
				for j in range(0, numB):
					size = HistLib.ReadBytes(fobj, 2)
					fname = HistLib.ReadOString(fobj)
					entry[size] = fname
	def _SaveF(self, fobj):
		fobj.write("Fam!")
		fobj.write(HistLib.longstruct.pack(len(self.props)))
		for key, val in self.props.iteritems():
			vector = isinstance(val, str)
			(bold, italic, aa) = key
			bf = 0
			bf = HistLib.SetBit(bf, 0, vector)
			bf = HistLib.SetBit(bf, 1, bold)
			bf = HistLib.SetBit(bf, 2, italic)
			bf = HistLib.SetBit(bf, 3, aa)
			fobj.write(chr(bf))
			if vector:
				HistLib.WriteOString(fobj, val)
			else:
				fobj.write(chr(len(val)))
				for size, fname in val.iteritems():
					fobj.write(HistLib.shortstruct.pack(size))
					HistLib.WriteOString(fobj, fname)

# Create the Family object, load the files it references, and return the
# dictionary.
def LoadFamily(fname):
	fam = Family(fname)
	out = {}
	for key, val in fam.props.iteritems():
		if isinstance(val, str): # vector font
			out[key] = PFont(os.path.join(Paths.assets, "fonts", val))
		else: # bitmap font
			outval = {}
			for size, fname in val.iteritems():
				outval[size] = BMFont(os.path.join(Paths.assets, "bmfonts", fname))
			out[key] = outval
	return out
