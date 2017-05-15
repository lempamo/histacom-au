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
# Fonts.py - wrapper for pygame fonts to make them less annoying

import HStruct, HistLib, pygame_sdl2, cStringIO

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