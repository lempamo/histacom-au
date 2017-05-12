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
# HStruct.py - replicates the functionality of a C Struct in Python
# Not to be confused with the inbuilt module "struct"

# Returns a class definition. Usage:
# exec(HStruct.Gen("Window", "w", "h", "x", "y"))
def Gen(clsname, *args):
	return ("""
class {0}:
	def __init__(self, {1}):
""".format(clsname,
	", ".join(args)) +
	"".join(["\t\tself.{0} = {0}\n".format(x) for x in args]))
