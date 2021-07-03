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
## Class Main
###########################################################################

class Main ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 946,601 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer41 = wx.BoxSizer( wx.VERTICAL )

		bSizer61 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

		self.btm_logo = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 250,250 ), 0 )
		bSizer11.Add( self.btm_logo, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 20 )

		bSizer5 = wx.BoxSizer( wx.VERTICAL )

		self.btn_properties = wx.Button( self, wx.ID_ANY, _(u"Pr&operties"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.btn_properties, 0, wx.ALL|wx.EXPAND, 5 )

		self.btn_entities = wx.Button( self, wx.ID_ANY, _(u"En&tities"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.btn_entities, 0, wx.ALL|wx.EXPAND, 5 )

		self.btn_categories = wx.Button( self, wx.ID_ANY, _(u"&Categories"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.btn_categories, 0, wx.ALL|wx.EXPAND, 5 )

		self.btn_events = wx.Button( self, wx.ID_ANY, _(u"&Events"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.btn_events, 0, wx.ALL|wx.EXPAND, 5 )

		self.btn_persons = wx.Button( self, wx.ID_ANY, _(u"&Persons"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.btn_persons, 0, wx.ALL|wx.EXPAND, 5 )

		self.btn_relais = wx.Button( self, wx.ID_ANY, _(u"&Relays"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.btn_relais, 0, wx.ALL|wx.EXPAND, 5 )

		self.btn_per_inscriptions = wx.Button( self, wx.ID_ANY, _(u"&Individual inscriptions"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.btn_per_inscriptions, 0, wx.ALL|wx.EXPAND, 5 )

		self.btn_rel_inscriptions = wx.Button( self, wx.ID_ANY, _(u"Relay in&scriptions"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.btn_rel_inscriptions, 0, wx.ALL|wx.EXPAND, 5 )

		self.btn_heats = wx.Button( self, wx.ID_ANY, _(u"&Heats"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.btn_heats, 0, wx.ALL|wx.EXPAND, 5 )

		self.btn_results = wx.Button( self, wx.ID_ANY, _(u"&Results"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.btn_results, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer11.Add( bSizer5, 1, wx.EXPAND, 5 )


		bSizer61.Add( bSizer11, 1, wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer41.Add( bSizer61, 1, wx.EXPAND, 5 )

		bSizer9 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer9.Add( self.m_staticline1, 0, wx.ALL|wx.EXPAND, 5 )

		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_about = wx.Button( self, wx.ID_ANY, _(u"About"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_about.SetToolTip( _(u"About") )

		bSizer6.Add( self.btn_about, 0, wx.ALL, 5 )

		self.btn_open_db = wx.Button( self, wx.ID_ANY, _(u"&Open DB"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_open_db.SetToolTip( _(u"Open DB") )

		bSizer6.Add( self.btn_open_db, 0, wx.ALL, 5 )


		bSizer6.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.btn_close = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		self.btn_close.SetToolTip( _(u"Close") )

		bSizer6.Add( self.btn_close, 0, wx.ALL, 5 )


		bSizer9.Add( bSizer6, 0, wx.EXPAND, 5 )


		bSizer41.Add( bSizer9, 0, wx.EXPAND|wx.ALL, 5 )


		self.SetSizer( bSizer41 )
		self.Layout()

	def __del__( self ):
		pass


