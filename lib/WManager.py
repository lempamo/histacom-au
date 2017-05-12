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
# WManager.py - Window manager implementations

import Engine, HStruct

# Window struct
exec(HStruct.Gen("Window", "w", "h", "x", "y"))	

# Change mode to window size and stick in (0, 0). So, don't do much.
# Used for the launcher. Bad idea to try multiple windows on it.
class Shim:
	def __init__(self):
		self.windows = []
	
	def createWindow(self, w, h, x = -1, y = -1):
		if len(self.freedWindowSlots) > 0:
			entityId = min(freedWindowSlots)
			freedEntitySlots.remove(entityId)
		else:
			entityId = len(entities)
