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

import Engine, Element, Events, sys, HistLib

class LauncherButton(Element.Sprite):
	def mouseout(self):
		global helptext, helpdef
		self.image = self.out
		if self.helpim:
			helptext.image = helpdef

	def mouseover(self):
		global helptext
		self.image = self.over
		if self.helpim:
			helptext.image = self.helpim

	def __init__(self, win, x, y, out, over, helpim, action):
		self.out = Engine.theme[out].obj
		self.over = Engine.theme[over].obj
		if helpim:
			self.helpim = Engine.theme[helpim].obj
		else:
			self.helpim = None
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
	global helptext, helpdef
	helpdef = Engine.theme["helpgs"].obj
	launcherwin = Engine.wm.createWindow(478, 322)
	launcherwin.addObj(Element.Sprite, 0, 0, "launcherbg")
	helptext = launcherwin.addObj(Element.Sprite, 179, 93, "helpgs")
	launcherwin.addObj(LauncherButton, 0, 93, "newout", "newover", "helpng", newGame)
	launcherwin.addObj(LauncherButton, 0, 118, "contout", "contover", "helpcg", lambda: HistLib.alert("unsupported"))
	launcherwin.addObj(LauncherButton, 0, 143, "loadout", "loadover", "helplg", lambda: HistLib.alert("unsupported"))
	launcherwin.addObj(LauncherButton, 427, 293, "exitout", "exitover", None, quitGame)
	launcherwin.events = {Events.KEYDOWNN: newGame, Events.KEYDOWNE: quitGame}