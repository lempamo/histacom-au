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
# RTF.py - HistLib.Format for reading and writing RTF

import HistLib, WeakDict, cStringIO, os

# A segment of text with flags.
# RTFParser.parse returns a list of lists (paragraphs) of lists (lines)
# of these. The parser has an internal state which gets copied to each
# text block once it is reached.
class Text(HistLib.saneobject):
	def __init__(self, text, state):
		self.text = text
		self.state = WeakDict.WeakDict(state)
	def __str__(self):
		return self.text
	def __repr__(self): # for testing
		return "{0} ({1})".format(self.text, self.state)

class RTFParser(HistLib.saneobject):
	def __init__(self):
		self.state = WeakDict.WeakDict()
	
	def _bool(self, (cmd, parameter)):
		self.state[cmd] = (parameter != 0)
	
	def _int(self, (cmd, parameter)):
		self.state[cmd] = parameter
	
	def _underline(self, (cmd, parameter)):
		self.state["ul"] = None if cmd == "ulnone" else cmd
	
	cmds = {"b": _bool,
			"i": _bool,
			"f": _int,
			"ul": _underline,
			"ulnone": _underline}
	
	def _readGroup(self, fobj):
		group = []
		obj = ""
		while True:
			byte = fobj.read(1)
			if byte == "{":
				group.append(obj)
				obj = ""
				group.append(self._readGroup(fobj))
			elif byte == "}":
				if obj != "":
					group.append(obj)
				return group
			elif byte == "":
				raise SyntaxError("{ without matching } in RTF data")
			else:
				obj += byte

	def _readControl(self, group):
		out = []
		for obj in group:
			if isinstance(obj, list):
				out.append(self._readControl(obj))
			else: # string
				data = ""
				fobj = cStringIO.StringIO(obj)
				while True:
					char = fobj.read(1)
					if char == "":
						break
					elif char == "\\": # start of command string
						cmd = ""
						parameter = None
						while True:
							char = fobj.read(1)
							if char == "":
								break
							elif char.islower():
								cmd += char
							else:
								if cmd == "":
									if char == "\\":
										data += "\\" # literal backslash
									else:
										cmd = char # command symbol
								elif char.isdigit() or char == "-": # parameter
									parameter = char
									while True:
										char = fobj.read(1)
										if char == "":
											break
										elif char.isdigit():
											parameter += char
										elif not char.isalnum():
											if char != " ":
												fobj.seek(-1, os.SEEK_CUR) # interpret again
											break
									parameter = int(parameter)
								elif char != " ":
									fobj.seek(-1, os.SEEK_CUR)
								break
						if cmd != "":
							if data != "":
								out.append(data)
								data = ""
							out.append((cmd, parameter))
					else: # data
						data += char
				if data != "":
					out.append(data)
		return out

	def _runCommands(self, src):
		control = list(src)
		output = []
		para = []
		line = []
		
		while len(control) > 0:
			self.control = control # update object's reference
			obj = control.pop(0)
			if isinstance(obj, tuple):
				(cmd, parameter) = obj
				if cmd in self.cmds:
					self.cmds[cmd](self, obj)
				elif cmd == "line" or cmd == "par":
					para.append(line)
					line = []
					if cmd == "par":
						output.append(para)
						para = []
			elif isinstance(obj, list):
				self._runCommands(obj)
			elif obj != "\r\n":
				# fragment of text
				line.append(Text(obj.replace("\r\n", ""), self.state))
		
		if len(line) > 0:
			para.append(line)
		
		if len(para) > 0:
			output.append(para)
		
		self.state = WeakDict.WeakDict() # reset
		
		return output
		
	def parse(self, string):
		fobj = cStringIO.StringIO(string)
		if fobj.read(1) != "{":
			raise HistLib.WrongFiletypeException("This is not RTF data")
		group = self._readGroup(fobj)
		control = self._readControl(group)
		return self._runCommands(control)

class RTF(HistLib.Format):
	def _LoadF(self, fobj):
		rawdata = HistLib.ReadCString(fobj)
		parser = RTFParser()
		self.document = parser.parse(rawdata)
	def _SaveF(self, fobj):
		raise HistLib.UnsupportedException("There is no support for saving RTFs yet")
	def _New(self):
		self.document = []