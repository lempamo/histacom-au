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

import HistLib, String, WManager

class Level(HistLib.Format):
	def _LoadF(self, fobj):
		if fobj.read(4) != "HILL":
			raise HistLib.WrongFiletypeException("This is not a Histacom.AU level")
		self.year = HistLib.shortstruct.unpack(fobj.read(2))[0] # year 32769 bug!
		self.wm = eval(HistLib.ReadOString(fobj))()
		for x in range(0, HistLib.shortstruct.unpack(fobj.read(2))[0]):
			self.deps.append(HistLib.ReadOString(fobj))
	def _SaveF(self, fobj):
		fobj.write("HILL")
		fobj.write(HistLib.shortstruct.pack(self.year))
		fobj.write(HistLib.shortstruct.pack(len(self.deps)))
		HistLib.WriteOString(fobj, str(self.wm.__class__))
		for dep in self.deps:
			HistLib.WriteOString(fobj, dep)
	def _New(self):
		self.year = 0
		self.deps = []
		self.wm = None