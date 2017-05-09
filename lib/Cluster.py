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
# Cluster.py - implementation of an extremely generic format used for
# save and level files.

import HistLib

# Import every module with a class we need to save.

import CString

class ClusterF(HistLib.Format):
	def _LoadF(self, fileobj):
		if fileobj.read(4) != "Clus":
			raise HistLib.WrongFiletypeException("This is not a Cluster file")
		fileobj.seek(HistLib.longstruct.unpack(fileobj.read(4))[0])
		entrynum = HistLib.longstruct.unpack(fileobj.read(4))[0]
		entries = []
		for x in range(0, entrynum):
			pos = HistLib.longstruct.unpack(fileobj.read(4))[0]
			name = HistLib.ReadCString(fileobj)
			cls = HistLib.ReadCString(fileobj)
			entries.append((pos, name, cls))
		for (pos, name, cls) in entries:
			fileobj.seek(pos)
			self.objs[name] = (eval(cls)(fileobj))
	
	def _SaveF(self, fileobj):
		fileobj.write("Clus")
		header = fileobj.tell()
		fileobj.write("\0" * 4) # reserve room for table pointer
		table = []
		for name, obj in self.objs.iteritems():
			table.append((fileobj.tell(), name, str(obj.__class__)))
			obj.Save(fileobj)
		tablepos = fileobj.tell()
		fileobj.write(HistLib.longstruct.pack(len(table)))
		for (pos, name, cls) in table:
			fileobj.write(HistLib.longstruct.pack(pos))
			fileobj.write(name + "\0")
			fileobj.write(cls + "\0")
		end = fileobj.tell()
		fileobj.seek(header)
		fileobj.write(HistLib.longstruct.pack(tablepos))
		fileobj.seek(end)
	
	def _New(self):
		self.objs = {}