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
# HistLib.py - common utility functions the other modules might need

import struct, __main__

class InvalidArgumentException(Exception):
	"""Invalid argument passed to function."""

class WrongFiletypeException(Exception):
	"""A class tried to load from an invalid file."""

class UnsupportedException(Exception):
	"""A file contained an unsupported property."""

# Generator to split an iterable into chunks of equal size.
def Chunks(l, n):
	for i in range(0, len(l), n):
		yield l[i:i + n]

# Read a C string from a file.
def ReadCString(myFile):
	myString = ""
	while True:
		byte = myFile.read(1)
		if byte == "\0":
			return myString
		myString += byte

# Read an "O String" from a file (1-byte length int followed by data).
def ReadOString(myFile):
	return myFile.read(ord(myFile.read(1)))

# Generic class for a file format. Derived classes should define:
# _LoadF(self, fileobj) _SaveF(self, fileobj) _New(self)
class Format:
	def _LoadStr(self, filename):
		myFile = open(filename, "rb")
		return self._LoadF(myFile)
	
	def Load(self, argument):
		if argument.__class__ == str:
			return self._LoadStr(argument)
		elif argument.__class__ == file:
			return self._LoadF(argument)
		else:
			raise InvalidArgumentException
	
	def _SaveStr(self, filename):
		myFile = open(filename, "wb")
		return self._SaveF(myFile)
	
	def Save(self, argument):
		if argument.__class__ == str:
			return self._SaveStr(argument)
		elif argument.__class__ == file:
			return self._SaveF(argument)
		else:
			raise InvalidArgumentException
	
	def __init__(self, loadFrom = None):
		self._New()
		if loadFrom:
			self.Load(loadFrom)

# Useful functions from __main__.
try:
	FindModule = __main__.FindModule
	alert = __main__.alert
except:
	pass

longstruct = struct.Struct("<L")
