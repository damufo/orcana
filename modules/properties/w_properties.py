# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Jun 11 2020)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class Properties
###########################################################################

class Properties ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 800,530 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer8 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, _(u"Properties"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		bSizer8.Add( self.m_staticText5, 0, wx.ALL, 5 )

		self.m_staticline21 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer8.Add( self.m_staticline21, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, _(u"Championship name:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		bSizer9.Add( self.m_staticText2, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.txt_champ_name = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.txt_champ_name, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer8.Add( bSizer9, 0, wx.EXPAND, 5 )

		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, _(u"Pool length:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		bSizer10.Add( self.m_staticText3, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		cho_pool_lengthChoices = [ _(u"25"), _(u"50") ]
		self.cho_pool_length = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cho_pool_lengthChoices, 0 )
		self.cho_pool_length.SetSelection( 0 )
		bSizer10.Add( self.cho_pool_length, 1, wx.ALL, 5 )


		bSizer8.Add( bSizer10, 0, wx.EXPAND, 5 )

		bSizer101 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText31 = wx.StaticText( self, wx.ID_ANY, _(u"Pool lanes:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )

		bSizer101.Add( self.m_staticText31, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		cho_pool_lanesChoices = [ _(u"5"), _(u"6"), _(u"8"), _(u"10") ]
		self.cho_pool_lanes = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cho_pool_lanesChoices, 0 )
		self.cho_pool_lanes.SetSelection( 1 )
		bSizer101.Add( self.cho_pool_lanes, 1, wx.ALL, 5 )


		bSizer8.Add( bSizer101, 0, wx.EXPAND, 5 )

		bSizer1011 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText311 = wx.StaticText( self, wx.ID_ANY, _(u"Chrono type:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText311.Wrap( -1 )

		bSizer1011.Add( self.m_staticText311, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		cho_chrono_typeChoices = [ _(u"Manual"), _(u"Electronic") ]
		self.cho_chrono_type = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cho_chrono_typeChoices, 0 )
		self.cho_chrono_type.SetSelection( 0 )
		bSizer1011.Add( self.cho_chrono_type, 1, wx.ALL, 5 )


		bSizer8.Add( bSizer1011, 0, wx.EXPAND, 5 )

		bSizer10111 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText3111 = wx.StaticText( self, wx.ID_ANY, _(u"Estament:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3111.Wrap( -1 )

		bSizer10111.Add( self.m_staticText3111, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		cho_estament_idChoices = []
		self.cho_estament_id = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cho_estament_idChoices, 0 )
		self.cho_estament_id.SetSelection( 0 )
		bSizer10111.Add( self.cho_estament_id, 1, wx.ALL, 5 )


		bSizer8.Add( bSizer10111, 0, wx.EXPAND, 5 )

		bSizer91 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText21 = wx.StaticText( self, wx.ID_ANY, _(u"Date age calculation:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )

		bSizer91.Add( self.m_staticText21, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.txt_date_age_calculation = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txt_date_age_calculation.SetMaxLength( 12 )
		bSizer91.Add( self.txt_date_age_calculation, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer8.Add( bSizer91, 0, wx.EXPAND, 5 )

		bSizer911 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText211 = wx.StaticText( self, wx.ID_ANY, _(u"Venue:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText211.Wrap( -1 )

		bSizer911.Add( self.m_staticText211, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.txt_venue = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txt_venue.SetMaxLength( 34 )
		bSizer911.Add( self.txt_venue, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer8.Add( bSizer911, 0, wx.EXPAND, 5 )


		bSizer8.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		bSizer103 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_generate_heats = wx.Button( self, wx.ID_ANY, _(u"&G. heats"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_generate_heats.SetToolTip( _(u"Generate heats automatic:\nsessions, phases, heats...") )

		bSizer103.Add( self.btn_generate_heats, 1, wx.ALL, 5 )

		self.btn_report_heats = wx.Button( self, wx.ID_ANY, _(u"&R. heats"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_report_heats.SetToolTip( _(u"Generate PDF report heats") )

		bSizer103.Add( self.btn_report_heats, 1, wx.ALL, 5 )

		self.btn_fiarna = wx.Button( self, wx.ID_ANY, _(u"&Fiarna"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_fiarna.SetToolTip( _(u"Fiarna") )

		bSizer103.Add( self.btn_fiarna, 1, wx.ALL, 5 )


		bSizer8.Add( bSizer103, 0, 0, 5 )

		self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer8.Add( self.m_staticline2, 0, wx.ALL|wx.EXPAND, 5 )

		bSizer102 = wx.BoxSizer( wx.VERTICAL )

		self.btn_back = wx.Button( self, wx.ID_ANY, _(u"B&ack"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer102.Add( self.btn_back, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )


		bSizer8.Add( bSizer102, 0, wx.EXPAND, 5 )


		bSizer7.Add( bSizer8, 1, wx.ALL|wx.EXPAND, 5 )


		self.SetSizer( bSizer7 )
		self.Layout()

	def __del__( self ):
		pass


