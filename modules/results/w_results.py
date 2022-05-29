# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Jun 11 2020)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

# import gettext
# _ = gettext.gettext

###########################################################################
## Class Results
###########################################################################

class Results ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 832,603 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, _(u"Results"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		bSizer2.Add( self.m_staticText3, 0, wx.ALL, 5 )

		self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer2.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer7 = wx.BoxSizer( wx.VERTICAL )

		bSizer73 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, _(u"Event:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		bSizer73.Add( self.m_staticText4, 0, wx.ALL, 5 )

		cho_event_idChoices = []
		self.cho_event_id = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cho_event_idChoices, 0 )
		self.cho_event_id.SetSelection( 0 )
		bSizer73.Add( self.cho_event_id, 1, wx.ALL, 5 )


		bSizer7.Add( bSizer73, 0, wx.EXPAND, 5 )

		self.lsc_heats = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		bSizer7.Add( self.lsc_heats, 1, wx.ALL|wx.EXPAND, 5 )

		self.lsc_heat = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		bSizer7.Add( self.lsc_heat, 1, wx.ALL|wx.EXPAND, 5 )

		bSizer71 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_year_add = wx.Button( self, wx.ID_ANY, _(u"&+1"), wx.DefaultPosition, wx.Size( -1,-1 ), wx.BU_EXACTFIT )
		self.btn_year_add.SetToolTip( _(u"Add 1 year for all categories") )

		bSizer6.Add( self.btn_year_add, 1, wx.TOP|wx.BOTTOM, 5 )

		self.btn_year_subtract = wx.Button( self, wx.ID_ANY, _(u"&-1"), wx.DefaultPosition, wx.Size( -1,-1 ), wx.BU_EXACTFIT )
		self.btn_year_subtract.SetToolTip( _(u"Substract 1 year for all categories") )

		bSizer6.Add( self.btn_year_subtract, 1, wx.TOP|wx.BOTTOM, 5 )


		bSizer71.Add( bSizer6, 0, wx.RIGHT|wx.LEFT, 5 )

		bSizer72 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_move_down = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		self.btn_move_down.SetToolTip( _(u"Move down") )

		bSizer72.Add( self.btn_move_down, 0, wx.ALL, 5 )

		self.btn_move_up = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		self.btn_move_up.SetToolTip( _(u"Move up") )

		bSizer72.Add( self.btn_move_up, 0, wx.ALL, 5 )


		bSizer71.Add( bSizer72, 0, wx.RIGHT|wx.LEFT, 5 )


		bSizer71.Add( ( 0, 0), 1, 0, 5 )

		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_delete = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		self.btn_delete.SetToolTip( _(u"Delete") )

		bSizer4.Add( self.btn_delete, 0, wx.ALL, 5 )

		self.btn_edit = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		self.btn_edit.SetToolTip( _(u"Edit") )

		bSizer4.Add( self.btn_edit, 0, wx.ALL, 5 )

		self.btn_add = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		self.btn_add.SetToolTip( _(u"Add") )

		bSizer4.Add( self.btn_add, 0, wx.ALL, 5 )

		self.btn_import = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		self.btn_import.SetToolTip( _(u"Import from predefined") )

		bSizer4.Add( self.btn_import, 0, wx.ALL, 5 )


		bSizer71.Add( bSizer4, 0, wx.LEFT, 5 )


		bSizer7.Add( bSizer71, 0, wx.EXPAND, 5 )

		bSizer10 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer10.Add( self.m_staticline1, 0, wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT, 5 )

		self.btn_close = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		self.btn_close.SetToolTip( _(u"Close") )

		bSizer10.Add( self.btn_close, 0, wx.ALIGN_RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT, 5 )


		bSizer7.Add( bSizer10, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5 )


		bSizer2.Add( bSizer7, 1, wx.EXPAND|wx.ALL, 5 )


		self.SetSizer( bSizer2 )
		self.Layout()

	def __del__( self ):
		pass


