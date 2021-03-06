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

class WrongFiletypeException(Exception):
	"""A class tried to load from an invalid file."""

class UnsupportedException(Exception):
	"""Unsupported features."""

# Store two- and four-byte unsigned integers in binary files.
shortstruct = struct.Struct("<H")
longstruct = struct.Struct("<L")
signedshortstruct = struct.Struct("<h")

# Fix struct.unpack's ugly syntax.
def Reader(structobj):
	return lambda x: structobj.unpack(x)[0]

readers = {(1, False): ord,
		(2, False): Reader(shortstruct),
		(2, True): Reader(signedshortstruct),
		(4, False): Reader(longstruct)}

# Read an integer num bytes wide from fobj.
def ReadBytes(fobj, num, signed = False):
	if (num, signed) in readers:
		return readers[(num, signed)](fobj.read(num))
	else:
		raise TypeError

# Get bit i of num as a bool.
def GetBit(num, i):
	mask = 0b10000000 >> i
	masked = num & mask
	bit = masked >> (7 - i)
	return bool(bit)

# Set bit i of num to truthiness of val. Returns the new num.
def SetBit(num, i, val):
	if GetBit(num, i) == bool(val):
		return num
	else:
		return num ^ (1 << (7 - i))

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
		elif byte == "":
			print("warning: reached EOF with no terminator while reading C String")
			return myString
		myString += byte

# Write a C string to a file.
def WriteCString(myFile, myString):
	myFile.write(myString + "\0")

# Read an "O String" from a file (1-byte length int followed by data).
def ReadOString(myFile):
	return myFile.read(ReadBytes(myFile, 1))

# Write an "O String" to a file.
def WriteOString(myFile, myString):
	myFile.write(chr(len(myString)) + myString)

# A "new-style" object with an "old-style" string representation.
class _sanebase(type):
	def __str__(self):
		# Chop off stupid Python 3-esque fluff.
		return repr(self)[8:-2]

class saneobject(object):
	__metaclass__ = _sanebase

# Generic class for a file format. Derived classes should define:
# _LoadF(self, fileobj) _SaveF(self, fileobj) _New(self)
class Format(saneobject):
	def _LoadStr(self, filename):
		with open(filename, "rb") as myFile:
			return self._LoadF(myFile)
	
	def Load(self, argument):
		if isinstance(argument, str):
			return self._LoadStr(argument)
		elif isinstance(argument, file):
			return self._LoadF(argument)
		else:
			raise TypeError
	
	def _SaveStr(self, filename):
		with open(filename, "wb") as myFile:
			return self._SaveF(myFile)
	
	def Save(self, argument):
		if isinstance(argument, str):
			return self._SaveStr(argument)
		elif isinstance(argument, file):
			return self._SaveF(argument)
		else:
			raise TypeError
	
	def __init__(self, loadFrom = None):
		self._New()
		if loadFrom:
			self.Load(loadFrom)

# Useful symbols from __main__.
try:
	FindModule = __main__.FindModule
	alert = __main__.alert
	productName = __main__.productName
except:
	pass

