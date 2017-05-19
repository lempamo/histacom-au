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
# Serial.py - save stuff

import HistLib

class Colour(HistLib.Format):
	def _LoadF(self, fobj):
		self.tup = tuple([HistLib.ReadBytes(fobj, 1) for i in range(0, 4)])
	def _SaveF(self, fobj):
		if len(self.tup) != 4:
			raise HistLib.UnsupportedException
		for val in self.tup:
			fobj.write(chr(val))
	def _New(self):
		self.tup = (0, 0, 0, 0)