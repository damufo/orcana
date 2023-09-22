import wx
import wx.grid
import wx.lib.mixins.gridlabelrenderer as glr


COL_H_ALIGNMENTS_IND = {
    0 : wx.ALIGN_LEFT,
    1 : wx.ALIGN_CENTRE,
    2 : wx.ALIGN_CENTRE,
    3 : wx.ALIGN_RIGHT,
    4 : wx.ALIGN_CENTRE,
    5 : wx.ALIGN_CENTRE,
    6 : wx.ALIGN_CENTRE,
}
COL_H_ALIGNMENTS_REL = {
    0 : wx.ALIGN_LEFT,
    1 : wx.ALIGN_CENTRE,
    2 : wx.ALIGN_CENTRE,
    3 : wx.ALIGN_CENTRE,
    4 : wx.ALIGN_RIGHT,
    5 : wx.ALIGN_CENTRE,
    6 : wx.ALIGN_CENTRE,
    7 : wx.ALIGN_CENTRE,
}
class CustomGrid(wx.grid.Grid, glr.GridWithLabelRenderersMixin):
    def __init__(self, parent):
        wx.grid.Grid.__init__(self, parent)
        glr.GridWithLabelRenderersMixin.__init__(self)


# class CustomGrid(wx.grid.Grid, glr.GridWithLabelRenderersMixin):
#     def __init__(self, parent):
#         wx.grid.Grid.__init__(self, parent)
#         glr.GridWithLabelRenderersMixin.__init__(self)


class CustomColLabelRenderer(glr.GridLabelRenderer):
    def __init__(self, color, ind_rel):
        super(CustomColLabelRenderer, self).__init__()
        self.color = color
        if ind_rel == 'I':
            self.col_h_alignments = COL_H_ALIGNMENTS_IND
        else:
            self.col_h_alignments = COL_H_ALIGNMENTS_REL

    def Draw(self, grid, dc, rect, col):
        dc.SetPen(wx.Pen(wx.WHITE))
        dc.SetBrush(wx.Brush(self.color))
        dc.DrawRectangle(rect)
        text = grid.GetColLabelValue(col)
        # hAlign, vAlign = grid.GetColLabelAlignment()
        if col in self.col_h_alignments:
            hAlign = self.col_h_alignments[col]
        else:
            hAlign = wx.ALIGN_RIGHT

        vAlign = wx.ALIGN_CENTRE
        self.DrawText(grid, dc, rect, text, hAlign, vAlign)