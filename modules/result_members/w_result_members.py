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
## Class ResultMembers
###########################################################################

class ResultMembers ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 832,899 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, _(u"Relay members"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		bSizer2.Add( self.m_staticText3, 0, wx.ALL, 5 )

		self.Events = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer2.Add( self.Events, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer61 = wx.BoxSizer( wx.VERTICAL )

		bSizer11 = wx.BoxSizer( wx.VERTICAL )

		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText31 = wx.StaticText( self, wx.ID_ANY, _(u"Relay:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )

		bSizer7.Add( self.m_staticText31, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.lbl_relay = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_relay.Wrap( -1 )

		bSizer7.Add( self.lbl_relay, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


		bSizer11.Add( bSizer7, 0, wx.EXPAND, 5 )

		self.m_staticline4 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer11.Add( self.m_staticline4, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, _(u"Candidates:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		bSizer9.Add( self.m_staticText5, 0, wx.ALL, 5 )


		bSizer11.Add( bSizer9, 0, wx.EXPAND, 5 )

		self.lsc_candidates = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		bSizer11.Add( self.lsc_candidates, 2, wx.ALL|wx.EXPAND, 5 )

		bSizer71 = wx.BoxSizer( wx.HORIZONTAL )


		bSizer71.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.btn_select_candidates = wx.Button( self, wx.ID_ANY, _(u"&Select"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_select_candidates.SetToolTip( _(u"Add selected candidates to members") )

		bSizer71.Add( self.btn_select_candidates, 0, wx.ALL, 5 )


		bSizer11.Add( bSizer71, 0, wx.EXPAND, 5 )

		self.m_staticline3 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer11.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, _(u"Selected members:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		bSizer8.Add( self.m_staticText4, 0, wx.ALL, 5 )


		bSizer11.Add( bSizer8, 0, wx.EXPAND, 5 )

		self.lsc_members = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_NO_HEADER|wx.LC_REPORT )
		bSizer11.Add( self.lsc_members, 1, wx.ALL|wx.EXPAND, 5 )

		bsz_events = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_move_down = wx.Button( self, wx.ID_ANY, _(u"D&own"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_move_down.SetToolTip( _(u"Move down") )

		bsz_events.Add( self.btn_move_down, 0, wx.ALL, 5 )

		self.btn_move_up = wx.Button( self, wx.ID_ANY, _(u"&Up"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_move_up.SetToolTip( _(u"Move up") )

		bsz_events.Add( self.btn_move_up, 0, wx.ALL, 5 )


		bsz_events.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.btn_new_person = wx.Button( self, wx.ID_ANY, _(u"Add new &person"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_new_person.SetToolTip( _(u"Add new person to members") )

		bsz_events.Add( self.btn_new_person, 0, wx.ALL, 5 )

		self.btn_remove_members = wx.Button( self, wx.ID_ANY, _(u"&Remove"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_remove_members.SetToolTip( _(u"Remove person from members") )

		bsz_events.Add( self.btn_remove_members, 0, wx.ALL, 5 )


		bSizer11.Add( bsz_events, 0, wx.EXPAND, 5 )

		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer11.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer62 = wx.BoxSizer( wx.VERTICAL )

		self.btn_back = wx.Button( self, wx.ID_ANY, _(u"B&ack"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_back.SetToolTip( _(u"Go back") )

		bSizer62.Add( self.btn_back, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )


		bSizer11.Add( bSizer62, 0, wx.EXPAND, 5 )


		bSizer61.Add( bSizer11, 1, wx.EXPAND|wx.ALL, 5 )


		bSizer2.Add( bSizer61, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer2 )
		self.Layout()

	def __del__( self ):
		pass


