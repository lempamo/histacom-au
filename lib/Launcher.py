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

import Engine, Element, Events, HistLib, Fonts, HistDoc

parser = HistDoc.HDocParser()

class LauncherHelp(Element.BoxContainer):
	def __init__(self, parent, (title, desc)):
		font = Engine.theme["font"]
		Element.BoxContainer.__init__(self, parent, 179, 93, 299, 200)
		self.title = self.addObj(Element.Text, 16, 12, title, font[(True, False, False)][19], (51, 102, 153))
		self.desc = self.addObj(Element.Text, 16, 37, desc, font[(False, False, False)][13], (0, 0, 0), w = 230)
		self._text = (title, desc)
	def setText(self, (title, desc)):
		self.title.text = title
		self.desc.text = desc
		self._text = (title, desc)
	text = property(lambda self: self._text, setText)

class LauncherOption(Element.BoxContainer):
	out = (166, 202, 240)
	over = (255, 255, 255)
	(width, height) = (179, 24)
	def mouseout(self):
		self.ColouredBox.colour = self.out
		if self.helptx:
			Engine.currlvl.helptext.text = Engine.currlvl.helpdef

	def mouseover(self):
		self.ColouredBox.colour = self.over
		if self.helptx:
			Engine.currlvl.helptext.text = self.helptx

	def __init__(self, parent, x, y, helptx, action):
		font = Engine.theme["font"]
		self.helptx = helptx
		Element.BoxContainer.__init__(self, parent, x, y, self.width, self.height)
		self.ColouredBox = self.addObj(Element.ColouredBox, 0, 0, self.width, self.height, self.out)
		doc = parser.parse("[f font][fs 13][b 1][u 1][c 0 0 0]{0}[u 0]{1}".format(self.helptx[0][0], self.helptx[0][1:]))
		self.Text = self.addObj(Element.RichText, 10, 5, 174, doc)
		self.action = action
		self.events = {Events.MOUSEOUT: self.mouseout,
					Events.MOUSEOVER: self.mouseover,
					Events.MOUSEUP: self.action}

class LauncherOptions(Element.BoxContainer):
	(width, height) = (179, 229)
	def __init__(self, parent, options):
		Element.BoxContainer.__init__(self, parent, 0, 93, self.width, self.height)
		self.options = options
	def setOptions(self, options):
		self._options = options
		self.objs = []
		y = 0
		for option in options:
			self.addObj(LauncherOption, *(0, y) + option)
			y += LauncherOption.height
			self.addObj(Element.ColouredBox, 0, y, self.width, 1, (51, 102, 153))
			y += 1
	options = property(lambda self: self._options, setOptions)

class LauncherButton(Element.BoxContainer):
	bgcolour = (0, 0, 0)
	fgcolour = (128, 128, 128)
	
	def __init__(self, parent, x, y, w, h, label, action):
		Element.BoxContainer.__init__(self, parent, x, y, w, h)
		

def newGame():
	Engine.endLevel(Engine.loadLevel, ["1998.hzh"])

def continueGame():
	pass

def loadGame():
	pass

def startLevel():
	strings = Engine.theme["strings"]
	helpdef = Engine.currlvl.helpdef = strings["gs"]
	launcherwin = Engine.wm.createWindow(478, 322)
	launcherwin.addObj(Element.Sprite, 0, 0, Engine.theme["launcherbg"])
	Engine.currlvl.helptext = launcherwin.addObj(LauncherHelp, helpdef)
	Engine.currlvl.opts = launcherwin.addObj(LauncherOptions, [
	(strings["nghelp"], newGame),
	(strings["cghelp"], continueGame),
	(strings["lghelp"], loadGame)])
	#launcherwin.addObj(LauncherButton, 427, 293, "exitout", "exitover", None, Engine.quitGame)
	launcherwin.events = {Events.KEYDOWNN: newGame, Events.KEYDOWNE: Engine.quitGame}