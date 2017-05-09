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
# HistPlat.py - wrap system-specific functions

import importlib, os

if HistLib.FindModule("xdg"):
	BaseDirectory = importlib.import_module("xdg.BaseDirectory")
	home = BaseDirectory.xdg_config_home
else:
	home = os.getenv("APPDATA")
	if home == None:
		home = os.path.join(os.getenv("HOME"), ".config")
if not os.path.isdir(home):
	os.makedirs(home)
