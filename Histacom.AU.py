#!/usr/bin/env python
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
# Histacom.AU.py - start! your! engine!

import sys, os, imp, importlib, traceback, subprocess

# In case this one dies too, and somebody ends up forking it again.
productName = "Histacom.AU"

mypath = os.path.realpath(os.path.abspath(__file__))
alertmethod = None

# Returns True if the module is present on the import path and False
# otherwise.
def FindModule(module):
	try:
		imp.find_module(module)
		return True
	except:
		return False

def alertGtk(message):
	dialog = gtk.MessageDialog(type = MESSAGE_ERROR, buttons = BUTTONS_OK)
	dialog.set_markup(message)
	dialog.set_title(productName)
	dialog.run()
	dialog.hide()
	dialog.destroy()

def alertTkinter(message):
	# Tkinter will automatically show a main window if we use an alert
	# before making one. So we make our own and hide it immediately.
	Tkinter.Tk().withdraw()
	tkMessageBox.showerror(productName, message)

def alertWin32(message):
	win32api.MessageBox(0, message, productName)

def alert(message):
	# Find the best way to get information to the user, then use it.
	global alertmethod, gtk, MESSAGE_ERROR, BUTTONS_OK, Tkinter, tkMessageBox, win32api
	if alertmethod == None:
		if FindModule("win32api"):
			win32api = importlib.import_module("win32api")
			alertmethod = alertWin32
		elif FindModule("gtk"):
			gtk = importlib.import_module("gtk")
			MESSAGE_ERROR = gtk.MESSAGE_ERROR
			BUTTONS_OK = gtk.BUTTONS_OK
			alertmethod = alertGtk
		elif FindModule("gi"):
			gtk = importlib.import_module("gi.repository.Gtk")
			MESSAGE_ERROR = gtk.MessageType.ERROR
			BUTTONS_OK = gtk.ButtonsType.OK
			alertmethod = alertGtk
		elif FindModule("_tkinter"):
			if FindModule("tkMessageBox"):
				Tkinter = importlib.import_module("Tkinter")
				tkMessageBox = importlib.import_module("tkMessageBox")
				alertmethod = alertTkinter
			else:
				Tkinter = importlib.import_module("tkinter")
				tkMessageBox = importlib.import_module("tkinter.messagebox")
				alertmethod = alertTkinter
		else:
			alertmethod = getattr(__builtins__, "print")
	alertmethod(message)

def exception(exctype, value, trace):
	# Most people probably aren't going to have a terminal open to see
	# why the game crashed. Let's give them a hint...
	alert(productName + " has encountered an unhandled exception: \n\n" + "".join(traceback.format_exception(exctype, value, trace)).replace("<", "&lt;").replace(">", "&gt;"))

sys.excepthook = exception

import distutils.spawn

# Make sure we're running Python 2 and not that inferior successor.
# Has the cool side effect of making the game technically compatible
# with Lightning Python, from a certain point of view.
if sys.version_info[0] != 2:
	# Try to find Python 2 using several methods.
	
	# Versioned filenames
	command = distutils.spawn.find_executable("python2")
	if not command:
		command = distutils.spawn.find_executable("python2.7")

	# Interpreter in PATH with desired version
	if not command:
		exepaths = os.environ["PATH"].split(";" if os.name == "nt" else ":")
		for path in exepaths:
			python = os.path.join(path, "python.exe" if os.name == "nt" else "python")
			if os.path.isfile(python) and os.access(python, os.X_OK):
				process = subprocess.Popen([python, "--version"])
				(output, err) = process.communicate()
				if "Python 2" in str(output):
					command = python
					break
	
	# Registry entry (untested)
	if not command:
		if FindModule("winreg"):
			winreg = importlib.import_module("winreg")
			PythonCore = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Python\PythonCore")
			for i in range(0, winreg.QueryInfoKey(PythonCore)[0]):
				try:
					keyname = winreg.EnumKey(PythonCore, i)
					if keyname[0] == "2":
						verkey = winreg.OpenKey(PythonCore, keyname)
						command = winreg.QueryValue(verkey, "InstallPath")
						break
				except WindowsError:
					continue
			
	# Give up
	if not command:
		alert(productName + " requires Python 2 to run.")
		sys.exit(1)
	
	# We found Python 2!
	# Let's use it.
	arguments = [command] + sys.argv
	os.execv(command, arguments)

# We are now guaranteed to be running under Python 2.

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-w", "--windowed", action = "store_const", const = True, default = False)
parser.add_argument("-W", "--width", nargs = 1, default = [-1])
parser.add_argument("-H", "--height", nargs = 1, default = [-1])
args = parser.parse_args()

sys.path.insert(0, "lib")

import Paths

# Check that we have all needed 3rd-party modules. Otherwise, we might
# import a file mid-game and the player loses their progress.
files = os.listdir(Paths.lib)
for fn in files:
	# Skip non-source files.
	if fn.endswith(".py"):
		# Open the source file and split it into lines for iteration.
		for line in open(os.path.join(Paths.lib, fn)).read().splitlines():
			# Remove irrelevant whitespace.
			line = line.strip()
			if line.startswith("import "):
				# Remove "import" and whitespace. Split by ",".
				for mod in " ".join(line.split()[1:]).split(","):
					# Get the actual module imported by "as" imports.
					if " as " in mod:
						mod = mod.split(" as ")[0]
					mod = mod.replace(" ", "")
					# Get base module (FindModule can't find submodules)
					if not FindModule(mod.split(".")[0]):
						alert("The required module '" + mod + "' could not be found.")
						sys.exit(1)

# It's finally time to start the game.

import Engine

# Load launcher window
Engine.loadLevel("launcher.hzh")
