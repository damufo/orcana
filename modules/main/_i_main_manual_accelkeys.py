# -*- coding: utf-8 -*-


import wx


keyMap = {}

def gen_keymap():
    keys = ("BACK", "TAB", "RETURN", "ESCAPE", "SPACE", "DELETE", "START",
        "LBUTTON", "RBUTTON", "CANCEL", "MBUTTON", "CLEAR", "PAUSE",
        "CAPITAL", "PRIOR", "NEXT", "END", "HOME", "LEFT", "UP", "RIGHT",
        "DOWN", "SELECT", "PRINT", "EXECUTE", "SNAPSHOT", "INSERT", "HELP",
        "NUMPAD0", "NUMPAD1", "NUMPAD2", "NUMPAD3", "NUMPAD4", "NUMPAD5",
        "NUMPAD6", "NUMPAD7", "NUMPAD8", "NUMPAD9", "MULTIPLY", "ADD",
        "SEPARATOR", "SUBTRACT", "DECIMAL", "DIVIDE", "F1", "F2", "F3", "F4",
        "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "F13", "F14",
        "F15", "F16", "F17", "F18", "F19", "F20", "F21", "F22", "F23", "F24",
        "NUMLOCK", "SCROLL", "PAGEUP", "PAGEDOWN", "NUMPAD_SPACE",
        "NUMPAD_TAB", "NUMPAD_ENTER", "NUMPAD_F1", "NUMPAD_F2", "NUMPAD_F3",
        "NUMPAD_F4", "NUMPAD_HOME", "NUMPAD_LEFT", "NUMPAD_UP",
        "NUMPAD_RIGHT", "NUMPAD_DOWN", "NUMPAD_PRIOR", "NUMPAD_PAGEUP",
        "NUMPAD_NEXT", "NUMPAD_PAGEDOWN", "NUMPAD_END", "NUMPAD_BEGIN",
        "NUMPAD_INSERT", "NUMPAD_DELETE", "NUMPAD_EQUAL", "NUMPAD_MULTIPLY",
        "NUMPAD_ADD", "NUMPAD_SEPARATOR", "NUMPAD_SUBTRACT", "NUMPAD_DECIMAL",
        "NUMPAD_DIVIDE")
    keys = ("BACK", "TAB", "RETURN", "ESCAPE", "SPACE", "DELETE", "START",
        "LBUTTON", "RBUTTON", "CANCEL", "MBUTTON", "CLEAR", "PAUSE",
        "CAPITAL", "END", "HOME", "LEFT", "UP", "RIGHT",
        "DOWN", "SELECT", "PRINT", "EXECUTE", "SNAPSHOT", "INSERT", "HELP",
        "NUMPAD0", "NUMPAD1", "NUMPAD2", "NUMPAD3", "NUMPAD4", "NUMPAD5",
        "NUMPAD6", "NUMPAD7", "NUMPAD8", "NUMPAD9", "MULTIPLY", "ADD",
        "SEPARATOR", "SUBTRACT", "DECIMAL", "DIVIDE", "F1", "F2", "F3", "F4",
        "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "F13", "F14",
        "F15", "F16", "F17", "F18", "F19", "F20", "F21", "F22", "F23", "F24",
        "NUMLOCK", "SCROLL", "PAGEUP", "PAGEDOWN", "NUMPAD_SPACE",
        "NUMPAD_TAB", "NUMPAD_ENTER", "NUMPAD_F1", "NUMPAD_F2", "NUMPAD_F3",
        "NUMPAD_F4", "NUMPAD_HOME", "NUMPAD_LEFT", "NUMPAD_UP",
        "NUMPAD_RIGHT", "NUMPAD_DOWN", "NUMPAD_PAGEUP",
        "NUMPAD_PAGEDOWN", "NUMPAD_END", "NUMPAD_BEGIN",
        "NUMPAD_INSERT", "NUMPAD_DELETE", "NUMPAD_EQUAL", "NUMPAD_MULTIPLY",
        "NUMPAD_ADD", "NUMPAD_SEPARATOR", "NUMPAD_SUBTRACT", "NUMPAD_DECIMAL",
        "NUMPAD_DIVIDE")
        
    for i in keys:
        keyMap[getattr(wx, "WXK_"+i)] = i
    for i in ("SHIFT", "ALT", "CONTROL", "MENU"):
        keyMap[getattr(wx, "WXK_"+i)] = ''
gen_keymap()

def GetKeyPress(event):
    keycode = event.GetKeyCode()
    keyname = keyMap.get(keycode, None)
    modifiers = ""
    for mod, ch in ((event.ControlDown(), 'Ctrl+'),
                    (event.AltDown(),     'Alt+'),
                    (event.ShiftDown(),   'Shift+'),
                    (event.MetaDown(),    'Meta+')):
        if mod:
            modifiers += ch

    if keyname is None:
        if 27 < keycode < 256:
            keyname = chr(keycode)
        else:
            keyname = "(%s)unknown" % keycode
            # keyname = ''
    return modifiers + keyname


class Interactor(object):

    def __init__(self):
        self.mouse_ini = None
        self.mouse_mov = None
        self.mouse_fin = None
        # self.cur = []
        # self.sofar = ""
        # self.lookup = {}

    def install(self, presenter, view):
        self.presenter = presenter
        self.view = view
        # view.btn_close.Bind(wx.EVT_BUTTON, self.on_close)
        # view.btn_generate.Bind(wx.EVT_BUTTON, self.on_generate)
        # view.btn_about.Bind(wx.EVT_BUTTON, self.on_about)
        view.scroll_win.Bind(wx.EVT_KEY_DOWN, self.key_pressed)
        # view.scroll_win.Bind(wx.EVT_KEY_UP, self.key_pressed)
        view.scroll_win.Bind(wx.EVT_MOUSEWHEEL, self.mouse_wheel)
        # view.scroll_win.Bind(wx.EVT_CHAR, self.key_pressed)
        view.sbx_picture.Bind(wx.EVT_LEFT_DOWN, self.mouse_down)
        view.sbx_picture.Bind(wx.EVT_LEFT_UP, self.mouse_up)
        view.sbx_picture.Bind(wx.EVT_MOTION, self.mouse_motion)
        view.scroll_win.SetFocus()
        view.sbx_picture.Bind(wx.EVT_PAINT, self.OnPaint)
        view.Bind(wx.EVT_SHOW, self.on_show)


        randomId = wx.NewId()
        view.Bind(wx.EVT_MENU, self.on_resize, id=randomId)
        accel_tbl = wx.AcceleratorTable(
            [
                # (wx.ACCEL_CTRL,  ord('S'), randomId)
                (wx.ACCEL_NORMAL,  ord('S'), randomId)
            
            ])
        view.SetAcceleratorTable(accel_tbl)

    def on_resize(self, event):
        self.presenter.resize()

    def on_show(self, event):
        self.presenter.go_picture_ini()

    def OnPaint(self, event=None):
        dc = wx.PaintDC(self.view.scroll_win)
        dc.Clear()
        dc.SetPen(wx.Pen(wx.BLACK, 4))
        dc.DrawLine(self.ini_x, self.ini_y, self.fin_x, self.fin_y)

    def mouse_wheel(self, event):
        # if event.ControlDown():
        if event.WheelRotation > 0:  # zoom in
            action = 'in'
        else:  # zoom out
            action = 'out'
        self.view.set_zoom(action=action)
        event.Skip()


    def on_generate(self, event):
        self.presenter.generate()
        event.Skip()

    def on_about(self, event):
        self.presenter.about()
        event.Skip()

    def on_close(self, event):
        self.presenter.close()
        event.Skip()


    # def _reset(self):
    #     self.sofar = ''
    #     self.cur = self.lookup
    #     # self.view.SetStatusText('')
    
    # def _add(self, key):
    #     self.cur = self.cur[key]
    #     self.sofar += ' ' + key
    #     # self.viev.SetStatusText(self.sofar)

    def mouse_down(self, event):
        print("mouse down: ", "x:", event.Position.x, " y", event.Position.y)
        if event.ControlDown():
            self.mouse_ini = (event.Position.x, event.Position.y)

    def mouse_motion(self, event):
        # print(event.LeftIsDown())
        # print("mouse motion: ", "x:", event.Position.x, " y", event.Position.y)
        rectangle = None
        if event.ControlDown() and event.LeftIsDown() and self.mouse_ini:
            print("mouse motion: ", "x:", event.Position.x, " y", event.Position.y)
            # self.mouse_mov =  (event.Position.x, event.Position.y)
            rectangle = wx.Rect(
                topLeft=(self.mouse_ini[0], self.mouse_ini[1]),
                bottomRight= (event.Position.x, event.Position.y)
                 )
            self.view.draw_rectangle(rectangle=rectangle)
        elif self.mouse_ini:
            self.mouse_ini = None
            self.view.load_picture()


    def mouse_up(self, event):
        rectangle = None
        if self.mouse_ini and event.ControlDown():
            print("mouse up: ", "x:", event.Position.x, " y", event.Position.y)
            # self.mouse_mov =  (event.Position.x, event.Position.y)
            '''
            box=(left, upper, right, lower)
            The top left coordinates correspond to (x, y) = (left, upper), and 
            the bottom right coordinates correspond to (x, y) = (right, lower).
            The area to be cropped is left <= x <right and upper <= y <lower,
            and the pixels of x = right andy = lower are not included.
            Be careful not to forget that box requires ().
            '''
            x_ini, y_ini = self.mouse_ini[0], self.mouse_ini[1]
            x_fin, y_fin = event.Position.x, event.Position.y
            if x_ini > x_fin:
                x_ini, x_fin = x_fin, x_ini 
            if y_ini > y_fin:
                y_ini, y_fin = y_fin, y_ini 
            rectangle = (x_ini, y_ini, x_fin, y_fin)
            
            if abs(x_fin - x_ini) > 10 and abs(y_fin - y_ini) > 10:
                self.view.crop_picture(rectangle=rectangle)
        else:
            self.mouse_ini = None
        # self.view.load_picture()

    # def drawRect(self,dc):
    #     dc.SetPen(wx.Pen("FFCE8A", 0))
    #     dc.SetBrush(wx.Brush("C0C0C0"))
    #     dc.DrawRectangle(50,50,50,50)