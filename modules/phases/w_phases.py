# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

# import gettext
# _ = gettext.gettext

###########################################################################
## Class Phases
###########################################################################

class Phases ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1362,543 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, _(u"Phases"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		bSizer2.Add( self.m_staticText3, 0, wx.ALL, 5 )

		self.Events = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer2.Add( self.Events, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer61 = wx.BoxSizer( wx.VERTICAL )

		bSizer11 = wx.BoxSizer( wx.VERTICAL )

		self.lsc = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		bSizer11.Add( self.lsc, 1, wx.ALL|wx.EXPAND, 5 )

		bsz_events = wx.BoxSizer( wx.HORIZONTAL )

		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_move_down = wx.Button( self, wx.ID_ANY, _(u"D&own"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_move_down.SetToolTip( _(u"Move down") )

		bSizer7.Add( self.btn_move_down, 1, wx.ALL, 5 )

		self.btn_move_up = wx.Button( self, wx.ID_ANY, _(u"&Up"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_move_up.SetToolTip( _(u"Move up") )

		bSizer7.Add( self.btn_move_up, 1, wx.ALL, 5 )

		self.m_staticline3 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer7.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )

		self.btn_copy_cat = wx.Button( self, wx.ID_ANY, _(u"Copy cat."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_copy_cat.SetToolTip( _(u"Copy phase categories.") )

		bSizer7.Add( self.btn_copy_cat, 0, wx.ALL, 5 )

		self.btn_paste_cat = wx.Button( self, wx.ID_ANY, _(u"Paste cat."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_paste_cat.SetToolTip( _(u"Replace phase categories by coped categories.") )

		bSizer7.Add( self.btn_paste_cat, 0, wx.ALL, 5 )


		bsz_events.Add( bSizer7, 0, 0, 5 )


		bsz_events.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.btn_categories = wx.Button( self, wx.ID_ANY, _(u"&Categories"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_categories.SetToolTip( _(u"Set categories for selected phases.") )

		bsz_events.Add( self.btn_categories, 0, wx.ALL, 5 )

		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_delete = wx.Button( self, wx.ID_ANY, _(u"D&elete"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_delete.SetToolTip( _(u"Delete") )

		bSizer8.Add( self.btn_delete, 1, wx.ALL, 5 )

		self.btn_edit = wx.Button( self, wx.ID_ANY, _(u"Ed&it"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_edit.SetToolTip( _(u"Edit") )

		bSizer8.Add( self.btn_edit, 1, wx.ALL, 5 )

		self.btn_add = wx.Button( self, wx.ID_ANY, _(u"A&dd"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_add.SetToolTip( _(u"Add") )

		bSizer8.Add( self.btn_add, 1, wx.ALL, 5 )


		bsz_events.Add( bSizer8, 0, 0, 5 )


		bSizer11.Add( bsz_events, 0, wx.EXPAND, 5 )

		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer11.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer62 = wx.BoxSizer( wx.VERTICAL )

		self.btn_back = wx.Button( self, wx.ID_ANY, _(u"B&ack"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_back.SetToolTip( _(u"Back") )

		bSizer62.Add( self.btn_back, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )


		bSizer11.Add( bSizer62, 0, wx.EXPAND, 5 )


		bSizer61.Add( bSizer11, 1, wx.EXPAND|wx.ALL, 5 )


		bSizer2.Add( bSizer61, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer2 )
		self.Layout()

	def __del__( self ):
		pass


