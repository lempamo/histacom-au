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
# InterOp.py - a series of tubes

# This is a special module - there is nothing public in its namespace
# and it modifies the namespaces of other modules when you import it.
# The idea is to make third party modules work together in an intuitive
# way even though they don't know anything about one another.

import PIL.Image, pygame_sdl2, cStringIO

# Extension of PIL.Image to enable it to interface with pygame_sdl2
def _ImageToSurface(self):
	o = cStringIO.StringIO()
	self.save(o, "png")
	i = cStringIO.StringIO(o.getvalue())
	o.close()
	s = pygame_sdl2.image.load(i).convert()
	i.close()
	return s

PIL.Image.Image.surface = property(_ImageToSurface)