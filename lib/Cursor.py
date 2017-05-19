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
# Cursor.py - do I have to spell it out?

import Engine, Element, pygame_sdl2

class Cursor(Element.Sprite):
	def __init__(self, win):
		Element.Sprite.__init__(self, win, 0, 0, "cursor pointer")
		pygame_sdl2.mouse.set_visible(False)
	def update(self):
		self.pos = Engine.mousepos
		Element.Sprite.update(self)