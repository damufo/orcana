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
## Class Events
###########################################################################

class Events ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 832,520 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, _(u"Events"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		bSizer2.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.Events = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer2.Add( self.Events, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer61 = wx.BoxSizer( wx.VERTICAL )

		bSizer11 = wx.BoxSizer( wx.VERTICAL )

		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText31 = wx.StaticText( self, wx.ID_ANY, _(u"Champ:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )

		bSizer7.Add( self.m_staticText31, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.lbl_champ_name = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_champ_name.Wrap( -1 )

		bSizer7.Add( self.lbl_champ_name, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


		bSizer11.Add( bSizer7, 0, wx.EXPAND, 5 )

		self.lsc = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		bSizer11.Add( self.lsc, 1, wx.ALL|wx.EXPAND, 5 )

		bsz_events = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_move_down = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		self.btn_move_down.SetToolTip( _(u"Move down") )

		bsz_events.Add( self.btn_move_down, 0, wx.ALL, 5 )

		self.btn_move_up = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		self.btn_move_up.SetToolTip( _(u"Move up") )

		bsz_events.Add( self.btn_move_up, 0, wx.ALL, 5 )

		self.btn_change_event = wx.Button( self, wx.ID_ANY, _(u"&Change event"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_change_event.Hide()

		bsz_events.Add( self.btn_change_event, 0, wx.ALL, 5 )


		bsz_events.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.btn_delete = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		self.btn_delete.SetToolTip( _(u"Delete") )

		bsz_events.Add( self.btn_delete, 0, wx.ALL, 5 )

		self.btn_edit = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		self.btn_edit.SetToolTip( _(u"Edit") )

		bsz_events.Add( self.btn_edit, 0, wx.ALL, 5 )

		self.btn_add = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		self.btn_add.SetToolTip( _(u"Add") )

		bsz_events.Add( self.btn_add, 0, wx.ALL, 5 )


		bSizer11.Add( bsz_events, 0, wx.EXPAND, 5 )

		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer11.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer62 = wx.BoxSizer( wx.VERTICAL )

		self.btn_close = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		self.btn_close.SetToolTip( _(u"Close") )

		bSizer62.Add( self.btn_close, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )


		bSizer11.Add( bSizer62, 0, wx.EXPAND, 5 )


		bSizer61.Add( bSizer11, 1, wx.EXPAND|wx.ALL, 5 )


		bSizer2.Add( bSizer61, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer2 )
		self.Layout()

	def __del__( self ):
		pass


