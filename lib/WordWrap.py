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
# WordWrap.py - wrap text to a certain width; adapted from pygame wiki

import pygame_sdl2

# Returns a Surface with text rendered at the specified colour with
# lines never running past "w".
def wrap(font, text, aa, colour, w, spacing = 0):
	if w < 0:
		# If w is negative, we don't need to wrap. This does not
		# meaningfully affect the result, but should speed things up a
		# bit.
		return font.render(text, aa, colour)
	lh = font.size("Tg")[1] + spacing
	h = 0
	rows = []
	while text:
		i = 1
		while font.size(text[:i])[0] < w and i < len(text):
			i += 1
		if i < len(text): # if wrapped...
			i = text.rfind(" ", 0, i) + 1 # find last space before cursor
		rows.append(font.render(text[:i], aa, colour))
		h += lh
		text = text[i:]
	out = pygame_sdl2.Surface((w, h), pygame_sdl2.SRCALPHA)
	y = 0
	for row in rows:
		out.blit(row, (0, y))
		y += lh
	return out

