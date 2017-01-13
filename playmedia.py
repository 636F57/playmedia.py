# Copyright (c) 2016 636F57@GitHub
# This software is released under an MIT license.
# See LICENSE for full details.

from ctypes import *
from msgonlywnd import msgOnlyWnd

class playmedia:
	def _init_:
		self.dictAlias = {}

	def mci_cmd(self, msg):
		res = windll.winmm.mciSendStringA(msg, 0, 0, 0)
		if res != 0:
			print("Error:", res, ", Failed in mciSendStringA, msg=", msg)
			return False:

	def closeAll(self):
		mciSend("close all")
		
	def close(self, alias):
		if alias in self.dictAlias:
			mciSend("close "+alias)
			self.dictAlias.pop(alias)
			return True
		else:
			print("alias not found")
			return False
		
	def playAgain(self, alias):
		if alias in self.dictAlias:
			mciSend("play "+ alias + " notify", 0, 0, self.dictAlias[alias])
			return True
		else:
			print("alias not found")
			return False
		
	def openAndPlayMp3(filename, callbackfunc):
		alias = "mp3"+str(len(self.listAlias))
		
		if mciSend("open \" + filaname + "\ type mpegvideo alias "+ alias):
			hwnd = msgOnlyWnd(alias, callbackfunc)
			if hwnd != 0:
				self.listAlias[alias] = hwnd
				mciSend("play "+ alias + " notify", 0, 0, hwnd)
				return alias
			else:
				mciSend("close "+alias)
				return ""
		else:
			print("Failed in opening MCI device.")
			return ""
		
		
	
			

