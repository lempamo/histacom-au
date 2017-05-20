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
# Options.py - command-line options

import __main__, pygame_sdl2, Engine, HistLib

def getMode():
	i = pygame_sdl2.display.Info()
	screenWidth = i.current_w
	screenHeight = i.current_h
	requestedWidth = int(__main__.args.width[0])
	requestedHeight = int(__main__.args.height[0])
	if __main__.args.windowed:
		flags = 0
	else:
		flags = pygame_sdl2.FULLSCREEN
	if requestedWidth > 0:
		width = requestedWidth
	else:
		width = screenWidth
	if requestedHeight > 0:
		height = requestedHeight
	else:
		height = screenHeight
	return (width, height, flags)

