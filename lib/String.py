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
# String.py - saveable classes for the two binary string types.

import HistLib

class CString(HistLib.Format):
	def _LoadF(self, fobj):
		self.pystr = HistLib.ReadCString(fobj)
	def _SaveF(self, fobj):
		fobj.write(self.pystr + "\0")
	def _New(self):
		self.pystr = ""

class OString(HistLib.Format):
	def _LoadF(self, fobj):
		self.pystr = HistLib.ReadOString(fobj)
	def _SaveF(self, fobj):
		fobj.write(chr(len(self.pystr)) + self.pystr)
	def _New(self):
		self.pystr = ""