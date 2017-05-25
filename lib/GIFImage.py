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
# GIFImage.py - load a GIF image into a list of (im, dur) tuples

import Element, InterOp, PIL.Image

def LoadGIF(loadFrom):
	images = []
	dur = 0
	gif = PIL.Image.open(loadFrom)
	for i in range(0, gif.n_frames):
		gif.seek(i)
		if "duration" in gif.info:
			dur = gif.info["duration"]
		images.append((gif.surface, dur))
	return images