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
# String.py - serialisable classes for the two binary string types

import HistLib

# Base class for Binary Strings. Derivatives should define _LoadF and
# _SaveF.
class BString(HistLib.Format):
	def _New(self):
		self.pystr = ""
	def Load(self, argument):
		if isinstance(argument, str):
			self.pystr = argument
		elif isinstance(argument, file):
			return self._LoadF(argument)
		else:
			raise TypeError
	def __str__(self):
		return self.pystr

for x in ["C", "O"]:
	exec("""
class {0}String(BString):
	def _LoadF(self, fobj):
		self.pystr = HistLib.Read{0}String(fobj)
	def _SaveF(self, fobj):
		HistLib.Write{0}String(fobj, self.pystr)
""".format(x))