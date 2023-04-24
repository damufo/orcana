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
## Class EventCategoriesCategoriesAdd
###########################################################################

class EventCategoriesCategoriesAdd ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Event categories categories add"), pos = wx.DefaultPosition, size = wx.Size( 909,528 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer11 = wx.BoxSizer( wx.VERTICAL )

		self.panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer8 = wx.BoxSizer( wx.VERTICAL )

		bSizer13 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText5 = wx.StaticText( self.panel, wx.ID_ANY, _(u"Event categories categories add"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		bSizer13.Add( self.m_staticText5, 1, wx.ALL, 5 )

		self.btn_add_category = wx.Button( self.panel, wx.ID_ANY, _(u"+"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer13.Add( self.btn_add_category, 0, wx.ALL, 5 )


		bSizer8.Add( bSizer13, 0, wx.EXPAND, 5 )

		self.m_staticline21 = wx.StaticLine( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer8.Add( self.m_staticline21, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText10 = wx.StaticText( self.panel, wx.ID_ANY, _(u"Add categories in selection order."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )

		bSizer8.Add( self.m_staticText10, 0, wx.ALL, 5 )

		bSizer91 = wx.BoxSizer( wx.VERTICAL )

		self.lsc = wx.ListCtrl( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		bSizer91.Add( self.lsc, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer8.Add( bSizer91, 1, wx.EXPAND, 5 )

		bSizer102 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_cancel = wx.Button( self.panel, wx.ID_ANY, _(u"&Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_cancel.SetToolTip( _(u"Cancel") )

		bSizer102.Add( self.btn_cancel, 0, wx.ALL, 5 )


		bSizer102.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.btn_acept = wx.Button( self.panel, wx.ID_ANY, _(u"&Acept"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_acept.SetToolTip( _(u"Acept") )

		bSizer102.Add( self.btn_acept, 0, wx.ALL, 5 )


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


