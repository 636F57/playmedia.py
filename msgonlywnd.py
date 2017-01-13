
from ctypes import *
from ctypes.wintypes import MSG

def DoMsgLoop():
	msg = MSG()
	while windll.user32.GetMessageA(byRef(msg), 0, 0, 0) > 0:
		windll.user32.TranslateMessage(byRef(msg))
		windll.user32.DispatchMessageA(byRef(msg))
			
class ST_WNDCLASS(ctypes.Structure):
	_fields_ = [("style", c_uint),
				("lpfnWndProc", WNDPROCTYPE),
				("cbClsExtra", c_int),
				("cbWndExtra", c_int),
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
		
		if registerWindow():
			self.hWnd = createWindow()
		
		
	def onMessage(self, hWnd, msg, wParam, lParam):
		if msg == MM_MCINOTIFY:
			self.callbackfunc()
			return 0
		else:
			return windll.user32.DefWindowProcW(hWnd, Msg, wParam, lParam)
		
	def registerWindow(self):
		WNDFUNC = WINFUNCTYPE(c_int, HWND, c_uint, WPARAM, LPARAM)
		wclassName = u'My Python Win32 Class'
		wname = u'My test window'
		
		wndClass = ST_WNDCLASS()
		wndClass.lpfnWndProc = WNDFUNC(onMessage)
		wndClass.hInstance = windll.kernel32.GetModuleHandleW(0)
		wndClass.lpszClassName = self.alias
		
		res = windll.user32.RegisterClass(ctypes.byref(wndClass))
		if res != 0:
			print("Error in registerWindow. alias =", alias)
			return False
		else:
			return True
					
	def createWindow(self):
		hWnd = windll.user32.CreateWindow(self.alias, 
						0, 0, 0, 0, 0, 0, HWND_MESSAGE, 0, 0, 0)
			
		if hWnd == 0:
			print("Error in createWindow. alias =", alias)
			return ""
		else:
			return hWnd
	
	
		
		