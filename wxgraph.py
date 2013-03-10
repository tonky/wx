# -*- coding: utf-8 -*-

from nose.tools import eq_
import math
import wx


class Example(wx.Frame):
    def __init__(self, *args, **kw):
        super(Example, self).__init__(*args, **kw) 

        self.InitUI()

    def InitUI(self):
        self.points = []
        self.current_point = False
        self.selected = False
        self.dragging = False
        self.radius = 10

        wx.StaticText(self, label='x:', pos=(700,10))
        wx.StaticText(self, label='y:', pos=(700,30))
        wx.StaticText(self, label='c:', pos=(700,50))

        self.st1 = wx.StaticText(self, label='', pos=(720, 10))
        self.st2 = wx.StaticText(self, label='', pos=(720, 30))
        self.st3 = wx.StaticText(self, label='', pos=(720, 50))

        pnl = wx.Panel(self, size=(500,50))
        pnl.SetBackgroundColour('#4f5049')

        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        button_clear = wx.Button(pnl, label="Clear")
        button_clear.Bind(wx.EVT_BUTTON, self.OnClearButton)

        vbox = wx.BoxSizer()
        vbox.Add(button_clear, border=5)
        pnl.SetSizer(vbox)
        pnl.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

        self.SetSize((800, 600))
        self.Centre()
        self.Show(True)

    def OnClearButton(self, e):
        self.points = []
        self.Refresh()

    def OnPaint(self, e):
        for point in self.points:
            self.DrawCircle(point)

    def OnMouseMove(self, e):
        x, y = e.GetPosition()
        self.st1.SetLabel(str(x))
        self.st2.SetLabel(str(y))

        if e.LeftIsDown():
            if not self.current_point:
                self.current_point = self.isPointOver(x, y)

            self.points.remove(self.current_point)
            self.points.append((x, y))
            self.current_point = ((x, y))
            return self.Refresh()

    def OnLeftDown(self, e):
        point = self.isPointOver(e.X, e.Y)

        if not point:
            return

        self.current_point = point

    def OnLeftUp(self, e):
        x, y = e.X, e.Y

        if e.ControlDown():
            point = self.isPointOver(e.X, e.Y)

            if point:
                self.selected = point

        if self.current_point:
            self.current_point = False
            return

        self.addPoint((x,y))
        self.Refresh()

    def isPointOver(self, x, y):
        def in_circle(point, x, y):
            center_x, center_y = point

            dist = math.sqrt((center_x - x) ** 2 + (center_y - y) ** 2)

            return dist <= self.radius

        for point in self.points:
            if in_circle(point, x, y):
                self.st3.SetLabel("%d %d" % point)
                return point

        return False

    def addPoint(self, point):
        self.points.append(point)

    def DrawCircle(self, point):
        x, y = point
        dc = wx.ClientDC(self)
        pen=wx.Pen('blue', 2)
        dc.SetPen(pen)
        dc.DrawCircle(x, y, self.radius)

    def OnKeyDown(self, e):
        key = e.GetKeyCode()

        self.st3.SetLabel(str(key))

        if key == wx.WXK_ESCAPE:
            self.Close()

def main():
    ex = wx.App()
    Example(None)
    ex.MainLoop()


from test_client import Client


class TestGraph():
    def setup(self):
        self.app = wx.App()
        self.w = Example(None)
        self.c = Client(self.w)

    def test_clear_button(self):
        self.w.points == [(30, 30)]
        self.c.click_button_by_label('Clear')
        assert self.w.points == []

    def test_drag_point(self):
        self.c.move(20, 30)
        self.c.click()
        self.c.drag(30, 30)
        assert self.w.points == [(30, 30)]

    def test_click_on_point(self):
        self.c.move(10, 10)
        self.c.click()
        self.c.move(12, 12)
        self.c.click()
        assert self.w.points == [(10, 10)]

    def test_add_points(self):
        self.c.move(10, 10)
        self.c.click()
        self.c.move(10, 40)
        self.c.click()
        self.c.move(40, 10)
        self.c.click()
        self.c.move(40, 40)
        self.c.click()

        assert self.w.points == [(10, 10), (10, 40), (40, 10), (40, 40)]

    def test_add_point(self):
        self.c.move(20, 30)
        self.c.click()
        assert self.w.points == [(20, 30)]

    def test_select_point(self):
        self.c.move(20, 30)
        self.c.click()
        self.c.move(22, 33)
        self.c.ctrl_click()
        eq_(self.w.selected, (20, 30))

    def teardown(self):
        self.w.Destroy()




if __name__ == '__main__':
    main()
