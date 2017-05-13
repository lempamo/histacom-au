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
# Launcher.py - script file for "launcher.hzh"

import Engine, Element, Events, pygame_sdl2, sys

class LauncherButton(Element.Sprite):
	def mouseout(self):
		self.image = self.out

	def mouseover(self):
		self.image = self.over

	def __init__(self, win, x, y, out, over, action):
		self.out = Engine.currlvl.header.theme[out].obj
		self.over = Engine.currlvl.header.theme[over].obj
		Element.Sprite.__init__(self, win, x, y, out)
		self.action = action
		self.events = {Events.MOUSEOUT: self.mouseout,
					Events.MOUSEOVER: self.mouseover,
					Events.MOUSEUP: self.action}
					

def newGame():
	Engine.currlvl.loop = False
	Engine.currlvl.tail = Engine.loadLevel
	Engine.currlvl.args = ["1998.hzh"]

def quitGame():
	Engine.currlvl.loop = False
	Engine.currlvl.tail = sys.exit

def startLevel():
	launcherwin = Engine.wm.createWindow(478, 322)
	launcherwin.addObj(Element.Sprite, 0, 0, "launcherbg")
	launcherwin.addObj(LauncherButton, 0, 93, "newout", "newover", newGame)
	launcherwin.addObj(LauncherButton, 427, 293, "exitout", "exitover", quitGame)