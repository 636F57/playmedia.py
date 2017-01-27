# Copyright (c) 2016 636F57@GitHub
# This software is released under an MIT license.
# See LICENSE for full details.

import ctypes
from ctypes.wintypes import *

WNDFUNC = ctypes.WINFUNCTYPE(ctypes.c_int, HWND, ctypes.c_uint, WPARAM, LPARAM)

def DoMsgLoop():
	msg = MSG()
	while windll.user32.GetMessageA(byRef(msg), 0, 0, 0) > 0:
		windll.user32.TranslateMessage(byRef(msg))
		windll.user32.DispatchMessageA(byRef(msg))
			
class ST_WNDCLASS(ctypes.Structure):
	_fields_ = [("style", ctypes.c_uint),
				("lpfnWndProc", WNDFUNC),
				("cbClsExtra", ctypes.c_int),
				("cbWndExtra", ctypes.c_int),
				("hInstance", HANDLE),
				("hIcon", HANDLE),
				("hCursor", HANDLE),
				("hbrBackground", HANDLE),
				("lpszMenuName", LPCWSTR),
				("lpszClassName", LPCWSTR)]

class MsgOnlyWnd:
	
	def __init__(self, alias, callbackfunc):
		self.hWnd = 0		
		self.alias = alias
		self.callbackfunc = callbackfunc
		
		if self.__registerWindow():
			self.hWnd = self.__createWindow()
			
	def	getHWND(self):
		return self.hWnd
		
	def __onMessage(self, hWnd, msg, wParam, lParam):
		if msg == MM_MCINOTIFY:
			self.callbackfunc(self.alias)
			return 0
		else:
			return ctypes.windll.user32.DefWindowProcW(hWnd, Msg, wParam, lParam)
		
	def __registerWindow(self):
		wclassName = u'My Python Win32 Class'
		wname = u'My test window'
		
		wndClass = ST_WNDCLASS()
		wndClass.lpfnWndProc = WNDFUNC(self.__onMessage)
		wndClass.hInstance = ctypes.windll.kernel32.GetModuleHandleW(0)
		wndClass.lpszClassName = self.alias
		
		res = ctypes.windll.user32.RegisterClassW(ctypes.byref(wndClass))
		if res != 0:
			print("Error ",res," in registerWindow. alias =", self.alias)
			return False
		else:
			return True
					
	def __createWindow(self):
		hWnd = ctypes.windll.user32.CreateWindow(self.alias, 
						0, 0, 0, 0, 0, 0, HWND_MESSAGE, 0, 0, 0)
			
		if hWnd == 0:
			print("Error in createWindow. alias =", alias)
			return ""
		else:
			return hWnd
	
	
		
		