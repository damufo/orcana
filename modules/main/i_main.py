# -*- coding: utf-8 -*-


import wx
import webbrowser

class Interactor(object):

    def __init__(self):
        self.mouse_ini = None
        self.mouse_ini_scroll = None
        self.mouse_mov = None
        self.mouse_fin = None
        # For scrolling
        self.mouse_fin_scroll = None
        self.porcion_px = None
        self.scroll_x_current = None

    def install(self, presenter, view):
        self.presenter = presenter
        self.view = view
        view.parent.Bind(wx.EVT_CLOSE, self.on_quit)
        view.btn_close.Bind(wx.EVT_BUTTON, self.on_quit)
        view.btn_about.Bind(wx.EVT_BUTTON, self.on_about)
        view.btn_open_db.Bind(wx.EVT_BUTTON, self.on_open_db)
        view.btn_report_results.Bind(wx.EVT_BUTTON, self.on_report_results)
        view.btn_export_results.Bind(wx.EVT_BUTTON, self.on_export_results)

        view.btn_properties.Bind(wx.EVT_BUTTON, self.show_properties)
        view.btn_entities.Bind(wx.EVT_BUTTON, self.show_entities)
        view.btn_categories.Bind(wx.EVT_BUTTON, self.show_categories)
        view.btn_events.Bind(wx.EVT_BUTTON, self.show_events)
        view.btn_phases.Bind(wx.EVT_BUTTON, self.show_phases)
        view.btn_persons.Bind(wx.EVT_BUTTON, self.show_persons)
        view.btn_inscriptions.Bind(wx.EVT_BUTTON, self.show_inscriptions)
        view.btn_heats.Bind(wx.EVT_BUTTON, self.show_heats)
        view.btn_results.Bind(wx.EVT_BUTTON, self.show_results)
        
     



        

        # view.Bind(wx.EVT_MENU, self.show_main, id=view.mnu_main.Id)
        # view.Bind(wx.EVT_MENU, self.show_properties, id=view.mnu_properties.Id)
        # view.Bind(wx.EVT_MENU, self.show_events, id=view.mnu_events.Id)
        # view.Bind(wx.EVT_MENU, self.on_save, id=view.mnu_save.Id)
        # view.Bind(wx.EVT_MENU, self.on_save_as, id=view.mnu_save_as.Id)
        # view.Bind(wx.EVT_MENU, self.on_rename, id=view.mnu_rename.Id)
        # view.Bind(wx.EVT_MENU, self.on_delete, id=view.mnu_delete.Id)
        # view.Bind(wx.EVT_MENU, self.on_quit, id=view.mnu_quit.Id)
        # view.Bind(wx.EVT_MENU, self.on_resize, id=view.mnu_resize.Id)
        # view.Bind(wx.EVT_MENU, self.on_autoresize, id=view.mnu_autoresize.Id)
        # view.Bind(wx.EVT_MENU, self.on_rotate_right, id=view.mnu_rotate_right.Id)
        # view.Bind(wx.EVT_MENU, self.on_rotate_left, id=view.mnu_rotate_left.Id)
        # view.Bind(wx.EVT_MENU, self.on_flip_h, id=view.mnu_flip_h.Id)
        # view.Bind(wx.EVT_MENU, self.on_flip_v, id=view.mnu_flip_v.Id)
        # view.Bind(wx.EVT_MENU, self.on_rotate_custom, id=view.mnu_rotate_custom.Id)
        # view.Bind(wx.EVT_MENU, self.on_preferences, id=view.mnu_preferences.Id)
        # view.Bind(wx.EVT_MENU, self.on_fullscreen, id=view.mnu_fullscreen.Id)
        # view.Bind(wx.EVT_MENU, self.on_go_next, id=view.mnu_go_next.Id)
        # view.Bind(wx.EVT_MENU, self.on_go_prev, id=view.mnu_go_prev.Id)
        # view.Bind(wx.EVT_MENU, self.on_go_first, id=view.mnu_go_first.Id)
        # view.Bind(wx.EVT_MENU, self.on_go_last, id=view.mnu_go_last.Id)
        # view.Bind(wx.EVT_MENU, self.on_zoom_in, id=view.mnu_zoom_in.Id)
        # view.Bind(wx.EVT_MENU, self.on_zoom_out, id=view.mnu_zoom_out.Id)
        # view.Bind(wx.EVT_MENU, self.on_zoom_1, id=view.mnu_zoom_1.Id)
        # view.Bind(wx.EVT_MENU, self.on_zoom_fit, id=view.mnu_zoom_fit.Id)
        # view.Bind(wx.EVT_MENU, self.on_homepage, id=view.mnu_homepage.Id)
        # view.Bind(wx.EVT_MENU, self.on_report_bug, id=view.mnu_report_bug.Id)
        # view.Bind(wx.EVT_MENU, self.on_source, id=view.mnu_source.Id)
        # view.Bind(wx.EVT_MENU, self.on_about, id=view.mnu_about.Id)
        # # Actions without menu
        # on_scroll_left_id = wx.NewId()
        # view.Bind(wx.EVT_MENU, self.on_scroll_left, id=on_scroll_left_id)
        # on_scroll_down_id = wx.NewId()
        # view.Bind(wx.EVT_MENU, self.on_scroll_down, id=on_scroll_down_id)
        # on_scroll_up_id = wx.NewId()
        # view.Bind(wx.EVT_MENU, self.on_scroll_up, id=on_scroll_up_id)
        # on_scroll_right_id = wx.NewId()
        # view.Bind(wx.EVT_MENU, self.on_scroll_right, id=on_scroll_right_id)

        # accel = wx.AcceleratorTable([
        #     (wx.ACCEL_ALT,  ord('M'), view.mnu_main.Id),
        #     (wx.ACCEL_ALT,  ord('P'), view.mnu_properties.Id),
        #     (wx.ACCEL_ALT,  ord('E'), view.mnu_events.Id),
        #     (wx.ACCEL_CTRL,  ord('S'), view.mnu_save.Id),
        #     (wx.ACCEL_CTRL|wx.ACCEL_SHIFT,  ord('S'), view.mnu_save_as.Id),
        #     (wx.ACCEL_NORMAL,  wx.WXK_F2, view.mnu_rename.Id),
        #     (wx.ACCEL_NORMAL,  wx.WXK_DELETE, view.mnu_delete.Id),
        #     (wx.ACCEL_CTRL,  ord('Q'), view.mnu_quit.Id),
        #     (wx.ACCEL_NORMAL,  ord('S'), view.mnu_resize.Id),
        #     (wx.ACCEL_SHIFT,  ord('S'), view.mnu_autoresize.Id),
        #     (wx.ACCEL_NORMAL,  ord('R'), view.mnu_rotate_right.Id),
        #     (wx.ACCEL_SHIFT,  ord('R'), view.mnu_rotate_left.Id),
        #     (wx.ACCEL_NORMAL,  ord('A'), view.mnu_rotate_custom.Id),
        #     (wx.ACCEL_NORMAL,  ord('F'), view.mnu_flip_h.Id),
        #     (wx.ACCEL_SHIFT,  ord('F'), view.mnu_flip_v.Id),
        #     (wx.ACCEL_CTRL,  ord('P'), view.mnu_preferences.Id),
        #     (wx.ACCEL_NORMAL,  wx.WXK_F11, view.mnu_fullscreen.Id),
        #     (wx.ACCEL_NORMAL,  wx.WXK_SPACE, view.mnu_go_next.Id),
        #     (wx.ACCEL_NORMAL,  wx.WXK_PAGEDOWN, view.mnu_go_next.Id),
        #     (wx.ACCEL_NORMAL,  wx.WXK_RIGHT, view.mnu_go_next.Id),
        #     (wx.ACCEL_NORMAL,  wx.WXK_BACK, view.mnu_go_prev.Id),
        #     (wx.ACCEL_NORMAL,  wx.WXK_PAGEUP, view.mnu_go_prev.Id),
        #     (wx.ACCEL_NORMAL,  wx.WXK_LEFT, view.mnu_go_prev.Id),
        #     (wx.ACCEL_NORMAL,  wx.WXK_HOME, view.mnu_go_first.Id),
        #     (wx.ACCEL_NORMAL,  wx.WXK_END, view.mnu_go_last.Id),
        #     (wx.ACCEL_NORMAL,  ord('+'), view.mnu_zoom_in.Id),
        #     (wx.ACCEL_NORMAL,  ord('-'), view.mnu_zoom_out.Id),
        #     (wx.ACCEL_NORMAL,  ord('1'), view.mnu_zoom_1.Id),
        #     (wx.ACCEL_NORMAL,  ord('0'), view.mnu_zoom_fit.Id),
        #     (wx.ACCEL_SHIFT,  ord('H'), view.mnu_homepage.Id),
        #     (wx.ACCEL_CTRL,  ord('B'), view.mnu_report_bug.Id),
        #     (wx.ACCEL_CTRL,  ord('U'), view.mnu_source.Id),
        #     (wx.ACCEL_CTRL,  ord('A'), view.mnu_about.Id),
        #     (wx.ACCEL_NORMAL,  ord('H'), on_scroll_left_id),
        #     (wx.ACCEL_CTRL,  wx.WXK_LEFT, on_scroll_left_id),
        #     (wx.ACCEL_NORMAL,  ord('J'), on_scroll_down_id),
        #     (wx.ACCEL_CTRL,  wx.WXK_DOWN, on_scroll_down_id),
        #     (wx.ACCEL_NORMAL,  ord('K'), on_scroll_up_id),
        #     (wx.ACCEL_CTRL,  wx.WXK_UP, on_scroll_up_id),
        #     (wx.ACCEL_NORMAL,  ord('L'), on_scroll_right_id),
        #     (wx.ACCEL_CTRL,  wx.WXK_RIGHT, on_scroll_right_id),
        #     ])
        # view.SetAcceleratorTable(accel)


    def on_about(self, event):
        self.presenter.about()

    def on_open_db(self, event):
        self.presenter.open_db()

    def on_report_results(self, event):
        self.presenter.report_results()

    def on_export_results(self, event):
        self.presenter.export_results()

    def show_properties(self, event):
        self.presenter.load_properties()

    def show_entities(self, event):
        self.presenter.load_entities()

    def show_categories(self, event):
        self.presenter.load_categories()

    def show_events(self, event):
        self.presenter.load_events()

    def show_phases(self, event):
        self.presenter.load_phases()

    def show_persons(self, event):
        self.presenter.load_persons()

    def show_inscriptions(self, event):
        self.presenter.load_inscriptions()

    def show_heats(self, event):
        self.presenter.load_heats()
        
    def show_results(self, event):
        self.presenter.load_results()

    def on_scroll_down(self, event):
        self.on_scroll(desp='DOWN')

    def on_scroll_up(self, event):
        self.on_scroll(desp='UP')

    def on_scroll_right(self, event):
        self.on_scroll(desp='RIGHT')
    
    def on_scroll(self, desp):
        scroll_win = self.view.scroll_win
        scroll_range = (
            scroll_win.GetScrollRange(wx.HORIZONTAL),
            scroll_win.GetScrollRange(wx.VERTICAL))
        if scroll_range[0] > 1 or scroll_range[1] > 1:
            scroll_current = (
                scroll_win.GetScrollPos(wx.HORIZONTAL),
                scroll_win.GetScrollPos(wx.VERTICAL))                
            if desp == 'LEFT' and scroll_current[0] > 0:
                desp_scroll = (-1, 0)  # Move left
            elif desp == 'DOWN' and scroll_current[1] < scroll_range[1]:
                desp_scroll = (0, 1)  # Move down
            elif desp == 'UP' and scroll_current[1] > 0:
                desp_scroll = (0, -1)  # Move up
            elif desp == 'RIGHT' and scroll_current[0] < scroll_range[0]:
                desp_scroll = (1, 0)  # Move right
            else:
                desp_scroll = (0, 0)
            new_scroll_pos = (
                scroll_current[0] + desp_scroll[0],
                scroll_current[1] + desp_scroll[1])
            self.view.scroll_win.Scroll(new_scroll_pos[0], new_scroll_pos[1])

    def on_size(self, event):
        if self.view.on_size_enabled:
            self.view.Layout()
            self.view.Refresh()
            if self.view.picture and self.view.force_fit:
                self.view.force_fit = False
                self.presenter.set_factor_to_fit()
                self.view.SetTransparent(255)
            self.view.Layout()
            self.view.Refresh()
            if self.view.picture:
                self.view.load_picture()
        else:
            self.view.on_size_enabled = True
            self.view.Layout()
            self.view.Refresh()
        
    def on_fullscreen(self, event):
        self.presenter.show_fullscreen()

    def on_activate_app(self, event):
        self.presenter.go_picture_ini()

    def on_open(self, event):
        self.presenter.open()

    def on_save(self, event):
        self.presenter.save()

    def on_save_as(self, event):
        self.presenter.save_as()

    def on_rename(self, event):
        self.presenter.rename()
        
    def on_delete(self, event):
        self.presenter.delete()
        
    def on_quit(self, event):
        # if self.view.picture and self.view.picture.modified:
        #     result = self.view.msg.question(
        #         message=_("The file has not been saved... continue closing?"))
        #     if not result:
        #         return
        self.view.parent.view_plus.stop()
        # event.Skip()

    def on_resize(self, event):
        self.presenter.resize()
        
    def on_autoresize(self, event):
        self.presenter.autoresize()
        
    def on_rotate_right(self, event):
        self.presenter.rotate(angle=90)
        
    def on_rotate_left(self, event):
        self.presenter.rotate(angle=-90)
        
    def on_rotate_custom(self, event):
        self.presenter.rotate(angle=0)

    def on_flip_h(self, event):
        self.presenter.flip(method='horizontally')
        
    def on_flip_v(self, event):
        self.presenter.flip(method='vertically')
        
    def on_preferences(self, event):
        self.presenter.preferences()
        
    def on_go_next(self, event):
        self.presenter.go_picture(action='next')
        
    def on_go_prev(self, event):
        self.presenter.go_picture(action='prev')
        
    def on_go_first(self, event):
        self.presenter.go_picture(action='first')
        
    def on_go_last(self, event):
        self.presenter.go_picture(action='last')
        
    def on_zoom_in(self, event):
        self.presenter.set_zoom(action='in')
        
    def on_zoom_out(self, event):
        self.presenter.set_zoom(action='out')
        
    def on_zoom_1(self, event):
        self.presenter.set_zoom(action='100')
        
    def on_zoom_fit(self, event):
        self.presenter.set_zoom(action='fit')
        
    def on_homepage(self, event):
        webbrowser.open('https://github.com/damufo/orcana')
        
    def on_report_bug(self, event):
        webbrowser.open('https://github.com/damufo/orcana/issues')
        
        
    def on_source(self, event):
        webbrowser.open('https://github.com/damufo/orcana')
        
    def on_about(self, event):
        self.presenter.about()

    def on_paint(self, event=None):
        dc = wx.PaintDC(self.view.sbx_picture)
        dc.Clear()
        dc.SetPen(wx.Pen(wx.BLACK, 4))
        dc.DrawLine(self.ini_x, self.ini_y, self.fin_x, self.fin_y)

    def mouse_wheel(self, event):
        if event.ControlDown():
            if event.WheelRotation > 0:  # zoom in
                action = 'in'
            else:  # zoom out
                action = 'out'
            self.presenter.set_zoom(action=action)

    def mouse_down(self, event):
        if event.ControlDown():
            self.mouse_ini = (event.Position.x, event.Position.y)
        if not self.mouse_ini_scroll:
            scroll_win = self.view.scroll_win
            scroll_range = (
                scroll_win.GetScrollRange(wx.HORIZONTAL),
                scroll_win.GetScrollRange(wx.VERTICAL))
            hidding_image_size = (
                scroll_win.VirtualSize.Width - scroll_win.Size.Width,
                scroll_win.VirtualSize.Height - scroll_win.Size.Height)
            if hidding_image_size[0] or hidding_image_size[1]:
                self.porcion_px = (
                    scroll_win.VirtualSize.Width / scroll_range[0],
                    scroll_win.VirtualSize.Height / scroll_range[1])
                self.scroll_current = (
                    scroll_win.GetScrollPos(wx.HORIZONTAL),
                    scroll_win.GetScrollPos(wx.VERTICAL))
                self.mouse_ini_scroll = (
                    event.Position.x,
                    event.Position.y)
            else:
                self.mouse_ini_scroll = None

    def mouse_motion(self, event):
        rectangle = None
        if event.ControlDown() and event.LeftIsDown() and self.mouse_ini:
            rectangle = wx.Rect(
                topLeft=(self.mouse_ini[0], self.mouse_ini[1]),
                bottomRight= (event.Position.x, event.Position.y)
                 )
            self.view.draw_rectangle(rectangle=rectangle)
        elif self.mouse_ini:
            self.mouse_ini = None
            self.view.load_picture()

        if event.LeftIsDown() and self.mouse_ini_scroll:
            desprazamento = (
                -(event.Position.x - self.mouse_ini_scroll[0]),
                -(event.Position.y - self.mouse_ini_scroll[1]))
            desp_scroll = (
                int(desprazamento[0] / self.porcion_px[0]),
                int(desprazamento[1] / self.porcion_px[1]))
            new_scroll_pos = (
                self.scroll_current[0] + desp_scroll[0],
                self.scroll_current[1] + desp_scroll[1])
            self.view.scroll_win.Scroll(new_scroll_pos[0], new_scroll_pos[1])
        else:
            self.mouse_ini_scroll = None

    def mouse_up(self, event):
        rectangle = None
        if self.mouse_ini and event.ControlDown():
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
                self.presenter.crop_picture(rectangle=rectangle)
                self.mouse_ini = None
        elif self.mouse_ini:
            self.mouse_ini = None
            self.view.load_picture()
