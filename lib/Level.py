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
# Level.py - class for storing level metadata

import HistLib, String, WManager, Engine, importlib

class Level(HistLib.Format):
	def _LoadF(self, fobj):
		if fobj.read(4) != "HILL":
			raise HistLib.WrongFiletypeException("This is not a Histacom.AU level")
		self.year = HistLib.shortstruct.unpack(fobj.read(2))[0] # year 32769 bug!
		self.wm = eval(HistLib.ReadOString(fobj))()
		self.scr = importlib.import_module(HistLib.ReadOString(fobj))
		for x in range(0, HistLib.shortstruct.unpack(fobj.read(2))[0]):
			key = HistLib.ReadOString(fobj)
			fname = HistLib.ReadOString(fobj)
			self.theme[key] = Engine.loadResource(fname)
		for x in range(0, HistLib.shortstruct.unpack(fobj.read(2))[0]):
			persist = bool(ord(fobj.read(1)))
			name = HistLib.ReadOString(fobj)
			self.mutables.append((name, persist))
	def _SaveF(self, fobj):
		fobj.write("HILL")
		fobj.write(HistLib.shortstruct.pack(self.year))
		HistLib.WriteOString(fobj, str(self.wm.__class__))
		HistLib.WriteOString(fobj, str(self.scr.__name__))
		fobj.write(HistLib.shortstruct.pack(len(self.theme)))
		for key, asset in self.theme.iteritems():
			HistLib.WriteOString(fobj, key)
			HistLib.WriteOString(fobj, asset.name)
		fobj.write(HistLib.shortstruct.pack(len(self.mutables)))
		for (name, persist) in self.mutables:
			fobj.write(chr(persist))
			HistLib.WriteOString(fobj, name)
	def _New(self):
		self.year = 0
		self.theme = {}
		self.wm = None
		self.scr = None
		self.mutables = []