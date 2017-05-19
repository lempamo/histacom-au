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
# SaveFile.py - handle saving and loading the game

import HistLib, Cluster, Engine, random, string

class SaveFile(HistLib.Format):
	def _LoadF(self, fobj):
		if fobj.read(4) != "Save":
			raise HistLib.WrongFiletypeException("This is not a Histacom.AU save file")
		self.year = HistLib.ReadBytes(fobj, 2)
		self.level = HistLib.ReadOString(fobj)
		self.fobj = fobj # read the cluster later
	def _SaveF(self, fobj):
		fobj.write("Save")
		fobj.write(HistLib.shortstruct.pack(self.year))
		HistLib.WriteOString(fobj, self.level)
		self.cluster.Save(fobj)
	def _New(self):
		self.year = 0
		self.level = ""
		self.cluster = None
		self.fobj = None
	def getcluster(self):
		if not self.cluster
			self.cluster = Cluster.Cluster(self.fobj)
		return self.cluster
	cluster = property(getcluster)

def LoadGame(loadfrom):
	if isinstance(loadfrom, str) or isinstance(loadfrom, file):
		save = SaveFile(loadfrom)
	elif isinstance(loadfrom, SaveFile):
		save = loadfrom
	else:
		raise TypeError
	level = Cluster.Cluster(Engine.getLevel(fname))
	level.Load(save.fobj)
	save.fobj.close()
	Engine.lvlname = save.level
	Engine.loadLevel(level)

def SaveGame(saveto):
	out = SaveFile()
	out.year = Engine.currlvl.header.year
	out.level = Engine.lvlname
	out.cluster = Cluster.Cluster()
	for obj in Engine.currlvl.header.mutables:
		out.cluster.__dict__[obj] = Engine.currlvl.__dict__[obj]
	out.Save(saveto)

def GenCode():
	if hasattr(Engine.currlvl, "playername"):
		code = str(Engine.currlvl.playername)
		b = str(len(code))
		code += "".join([random.choice(string.printable[:-38]) for x in range(0, 10 - len(code))])
		code += b
	else:
		code = "CHOSENONAME"
	code += Engine.lvlname[:-4]
	code = code.encode("rot13")
	new = ""
	for i, char in enumerate(code):
		if char.isdigit():
			char = str((5 - int(char)) % 10)
		elif i & 1:
			char = char.swapcase()
		new += char
	return new

def LoadCode(code):
	new = ""
	for i, char in enumerate(code):
		if char.isdigit():
			char = str((5 - int(char)) % 10)
		elif i & 1:
			char = char.swapcase()
		new += char
	new = new.encode("rot13")
	lvlname = new[11:] + ".hzh"
	level = Cluster.Cluster(lvlname)
	if new[:11] != "CHOSENONAME":
		level.playername = String.OString(new[:int(new[10])])
	Engine.loadLevel(level)