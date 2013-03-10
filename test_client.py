import wx


class Client():
    def __init__(self, window):
        self.w = window
        self.x = 0
        self.y = 0
        self.left_is_down = False

    def click_button_by_label(self, label):
        button = self.w.FindWindowByLabel(label)

        e = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, button.GetId())

        self.w.GetEventHandler().ProcessEvent(e)

    def drag(self, x, y):
        self.left_down()
        self.move(x, y)
        self.left_up()

    def move(self, x, y):
        self.x, self.y = x, y

        e = wx.MouseEvent(wx.wxEVT_MOTION)

        e.m_leftDown = self.left_is_down
        e.m_x, e.m_y = self.x, self.y

        self.w.GetEventHandler().ProcessEvent(e)

    def ctrl_click(self):
        self.left_up(meta='control')

    def click(self):
        self.left_down()
        self.left_up()

    def left_up(self, meta=False):
        self.left_is_down = False

        e = wx.MouseEvent(wx.wxEVT_LEFT_UP)

        if meta == 'control':
            e.m_controlDown = True
            print e.ControlDown()

        e.m_x, e.m_y = self.x, self.y

        self.w.GetEventHandler().ProcessEvent(e)

    def left_down(self):
        self.left_is_down = True

        e = wx.MouseEvent(wx.wxEVT_LEFT_DOWN)

        e.m_x, e.m_y = self.x, self.y

        self.w.GetEventHandler().ProcessEvent(e)
