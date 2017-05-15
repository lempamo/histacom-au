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
# HStruct.py - replicates the functionality of a C Struct in Python and
# provides optional setter encapsulation

import HistLib

# Returns a class definition. Usage:
# exec(HStruct.Gen("Window", "w", "h", "x", "y"))
def Gen(clsname, *args):
	return ("""
class {0}(HistLib.saneobject):
	def __init__(self, {1}):
""".format(clsname,
	", ".join(args)) +
	"".join(["\t\tself.{0} = {0}\n".format(x) for x in args]))

# Returns encapsulation functions. Usage:
# exec(HStruct.Enc("Window", "_w", "_h", "_x", "_y") + HStruct.Enc(
#	"wm", "w", "h", "x", "y"))
def Enc(controller, *args):
	return "".join(["""
	def _get{1}(self):
		return self._{1}

	def _set{1}(self, val):
		{0}.set{1}(self, val)
	
	{1} = property(_get{1}, _set{1})

""".format(controller, x) for x in args])

# Combines the above two functions. Usage:
# exec(HStruct.Gwe("Window", "wm", "w", "h", "x", "y"))
def Gwe(clsname, controller, *args):
	gargs = [clsname] + ["_" + x for x in args]
	eargs = [controller] + list(args)
	return Gen(*gargs) + Enc(*eargs)

# Returns setter functions for the base controller class. Usage:
# exec(HStruct.Sts("w", "h", "x", "y"))
def Sts(*args):
	return "".join(["""
def set{0}(self, obj, val):
	obj._{0} = val
""".format(x) for x in args])