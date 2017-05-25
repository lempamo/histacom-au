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
# HistDoc.py - Histacom.AU Document Format; use this module to read
# other document formats too

import HistLib, WeakDict, cStringIO, os

# A segment of text with flags.
# Parsers should produce a list of lists (lines) of these.
class Text(HistLib.saneobject):
	def __init__(self, text, state):
		self.text = text
		self.state = state
	def __str__(self): # for display
		return self.text
	def __repr__(self): # for testing
		return "Text('{0}', {1})".format(self.text, self.state)

class HDocParser(HistLib.saneobject):
	def _str(self, (cmd, val)):
		self._state[cmd] = val
	def _int(self, (cmd, val)):
		self._state[cmd] = int(val)
	def _bool(self, (cmd, val)):
		self._state[cmd] = bool(int(val))
	def _colour(self, (cmd, r, g, b)):
		self._state[cmd] = (int(r), int(g), int(b))
	cmds = {"aa": _bool,
			"b": _bool,
			"i": _bool,
			"c": _colour,
			"fs": _int,
			"u": _int,
			"f": _str}
	
	def _resetState(self):
		self._state = WeakDict.WeakDict(False)()
		self._state["u"] = 0
		self._state["c"] = (0, 0, 0)
	
	def __init__(self):
		self._resetState()
	
	def _flushText(self):
		if self._text != "":
			self._line.append(self._text)
			self._text = ""
	
	def _flushLine(self):
		self._flushText()
		if len(self._line) > 0:
			self._lines.append(self._line)
			self._line = []
	
	def _readCmd(self, fobj):
		cmdtext = ""
		while fobj.tell() < self._strlength:
			char = fobj.read(1)
			if char == "]":
				break
			else:
				cmdtext += char
		return cmdtext.split(" ")
	
	def _splitCmds(self, fobj):
		text = ""
		out = []
		while fobj.tell() < self._strlength:
			char = fobj.read(1)
			if char == "\\":
				self._text += fobj.read(1)
			elif char == "\n":
				if fobj.read(1) == "\n":
					self._flushLine()
				else:
					self._text += " "
					fobj.seek(-1, os.SEEK_CUR) # reinterpret that
			elif char == "[":
				self._flushText()
				self._line.append(self._readCmd(fobj))
			else:
				self._text += char
		self._flushLine()
	
	def _execute(self):
		output = []
		for inline in self._lines:
			outline = []
			for i in inline:
				if isinstance(i, str):
					outline.append(Text(i, WeakDict.WeakDict(False)(self._state)))
				else:
					cmd = i[0]
					if cmd in self.cmds:
						self.cmds[cmd](self, i)
			output.append(outline)
		self._resetState()
		return output
	
	def parse(self, string):
		self._lines = []
		self._line = []
		self._text = ""
		self._strlength = len(string)
		fobj = cStringIO.StringIO(string)
		self._splitCmds(fobj)
		return self._execute()