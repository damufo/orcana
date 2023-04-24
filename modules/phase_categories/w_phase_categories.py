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
## Class PhaseCategories
###########################################################################

class PhaseCategories ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Phase categories"), pos = wx.DefaultPosition, size = wx.Size( 948,716 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer11 = wx.BoxSizer( wx.VERTICAL )

		self.panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer8 = wx.BoxSizer( wx.VERTICAL )

		bSizer19 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText5 = wx.StaticText( self.panel, wx.ID_ANY, _(u"Phase categories"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		bSizer19.Add( self.m_staticText5, 1, wx.ALL, 5 )

		self.btn_add_category = wx.Button( self.panel, wx.ID_ANY, _(u"+"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_add_category.SetToolTip( _(u"Add new category.") )

		bSizer19.Add( self.btn_add_category, 0, wx.ALL, 5 )


		bSizer8.Add( bSizer19, 0, wx.EXPAND, 5 )

		self.m_staticline21 = wx.StaticLine( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer8.Add( self.m_staticline21, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer13 = wx.BoxSizer( wx.HORIZONTAL )


		bSizer8.Add( bSizer13, 0, wx.EXPAND, 5 )

		self.lsc = wx.ListCtrl( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		bSizer8.Add( self.lsc, 1, wx.ALL|wx.EXPAND, 5 )

		bSizer14 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_move_down = wx.Button( self.panel, wx.ID_ANY, _(u"D&own"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.btn_move_down, 0, wx.ALL, 5 )

		self.btn_move_up = wx.Button( self.panel, wx.ID_ANY, _(u"&Up"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.btn_move_up, 0, wx.ALL, 5 )


		bSizer14.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.btn_delete = wx.Button( self.panel, wx.ID_ANY, _(u"D&elete"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.btn_delete, 0, wx.ALL, 5 )

		self.btn_add = wx.Button( self.panel, wx.ID_ANY, _(u"A&dd"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.btn_add, 0, wx.ALL, 5 )


		bSizer8.Add( bSizer14, 0, wx.EXPAND, 5 )

		self.m_staticline2 = wx.StaticLine( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer8.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer141 = wx.BoxSizer( wx.HORIZONTAL )


		bSizer141.Add( ( 0, 0), 1, wx.EXPAND, 5 )


		bSizer8.Add( bSizer141, 0, wx.EXPAND, 5 )

		bSizer102 = wx.BoxSizer( wx.HORIZONTAL )


		bSizer102.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.btn_back = wx.Button( self.panel, wx.ID_ANY, _(u"B&ack"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_back.SetToolTip( _(u"Acept") )

		bSizer102.Add( self.btn_back, 0, wx.ALL, 5 )


		bSizer8.Add( bSizer102, 0, wx.EXPAND, 5 )


		bSizer7.Add( bSizer8, 1, wx.ALL|wx.EXPAND, 5 )


		self.panel.SetSizer( bSizer7 )
		self.panel.Layout()
		bSizer7.Fit( self.panel )
		bSizer11.Add( self.panel, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( bSizer11 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


