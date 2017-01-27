# Copyright (c) 2016 636F57@GitHub
# This software is released under an MIT license.
# See LICENSE for full details.

import ctypes
from msgonlywnd import MsgOnlyWnd

class playmedia:
	def __init__(self):
		self.dictAlias = {}

	@classmethod
	def __mciCmd(cls, msg, hwnd=0):
		res = ctypes.windll.winmm.mciSendStringW(msg, 0, 0, hwnd)
		if res != 0:
			print("Error:", res, ", Failed in mciSendStringA, msg=", msg)
			return False
		else:
			return True

	def closeAll(self):
		playmedia.__mciCmd("close all")
		
	def close(self, alias):
		if alias in self.dictAlias:
			playmedia.__mciCmd("close "+alias)
			self.dictAlias.pop(alias)
			return True
		else:
			print("alias not found")
			return False
		
	def playAgain(self, alias):
		if alias in self.dictAlias:
			playmedia.__mciCmd("play "+ alias + " notify", 0, 0, self.dictAlias[alias])
			return True
		else:
			print("alias not found")
			return False
		
	def openAndPlayMp3(self, filename, callbackfunc):
		alias = "mp3"+str(len(self.dictAlias))
		if playmedia.__mciCmd("open " + filename + " type mpegvideo alias "+ alias):
		#if playmedia.__mciCmd("open \"" + filename + "\" type waveaudio alias "+ alias):
			playmedia.__mciCmd("play "+ alias, 0) #for test
			mwnd = MsgOnlyWnd(alias, callbackfunc)
			hwnd = mwnd.getHWND()
			if hwnd != 0:
				print(hwnd)
				self.dictAlias[alias] = hwnd
				playmedia.__mciCmd("play "+ alias + " notify", hwnd)
				return alias
			else:
				print("Failed to create Message only Window.")
				playmedia.__mciCmd("close "+alias)
				return ""
		else:
			print("Failed to open a MCI device.")
			return ""
		
		
	
			

