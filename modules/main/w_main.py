# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.1.0-0-g733bf3d)
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

		sizer_warning = wx.BoxSizer( wx.VERTICAL )

		self.lbl_warning_version = wx.StaticText( self, wx.ID_ANY, _(u"Atention!! It is not working with the latest version,\nplease update your version of Orcana."), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
		self.lbl_warning_version.Wrap( -1 )

		self.lbl_warning_version.SetBackgroundColour( wx.Colour( 255, 0, 0 ) )
		self.lbl_warning_version.Hide()

		sizer_warning.Add( self.lbl_warning_version, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer5.Add( sizer_warning, 1, wx.EXPAND, 5 )

		self.btn_properties = wx.Button( self, wx.ID_ANY, _(u"Pr&operties"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.btn_properties, 0, wx.ALL|wx.EXPAND, 5 )

		self.btn_entities = wx.Button( self, wx.ID_ANY, _(u"E&ntities"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.btn_entities, 0, wx.ALL|wx.EXPAND, 5 )

		self.btn_categories = wx.Button( self, wx.ID_ANY, _(u"Cate&gories"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.btn_categories, 0, wx.ALL|wx.EXPAND, 5 )

		self.btn_events = wx.Button( self, wx.ID_ANY, _(u"&Events"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.btn_events, 0, wx.ALL|wx.EXPAND, 5 )

		self.btn_phases = wx.Button( self, wx.ID_ANY, _(u"Ph&ases"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.btn_phases, 0, wx.ALL|wx.EXPAND, 5 )

		self.btn_persons = wx.Button( self, wx.ID_ANY, _(u"&Persons"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.btn_persons, 0, wx.ALL|wx.EXPAND, 5 )

		self.btn_relays = wx.Button( self, wx.ID_ANY, _(u"&Relays"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_relays.Hide()

		bSizer5.Add( self.btn_relays, 0, wx.ALL|wx.EXPAND, 5 )

		self.btn_inscriptions = wx.Button( self, wx.ID_ANY, _(u"Ins&criptions"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.btn_inscriptions, 0, wx.ALL|wx.EXPAND, 5 )

		self.btn_heats = wx.Button( self, wx.ID_ANY, _(u"Heat&s"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.btn_heats, 0, wx.ALL|wx.EXPAND, 5 )

		self.btn_results = wx.Button( self, wx.ID_ANY, _(u"Resul&ts"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_results.Hide()

		bSizer5.Add( self.btn_results, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer11.Add( bSizer5, 1, wx.EXPAND, 5 )


		bSizer61.Add( bSizer11, 1, wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer41.Add( bSizer61, 1, wx.EXPAND, 5 )

		bSizer9 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer9.Add( self.m_staticline1, 0, wx.ALL|wx.EXPAND, 5 )

		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_about = wx.Button( self, wx.ID_ANY, _(u"A&bout"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_about.SetToolTip( _(u"About") )

		bSizer7.Add( self.btn_about, 0, wx.ALL, 5 )

		self.btn_open_db = wx.Button( self, wx.ID_ANY, _(u"Open &DB"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_open_db.SetToolTip( _(u"Open DB") )

		bSizer7.Add( self.btn_open_db, 0, wx.ALL, 5 )

		self.btn_report_results = wx.Button( self, wx.ID_ANY, _(u"Report res&ults"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_report_results.SetToolTip( _(u"Generate a PDF report with all results") )

		bSizer7.Add( self.btn_report_results, 0, wx.ALL, 5 )

		self.btn_export_results = wx.Button( self, wx.ID_ANY, _(u"E&x. results"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_export_results.Hide()
		self.btn_export_results.SetToolTip( _(u"Export resulta to CSV") )

		bSizer7.Add( self.btn_export_results, 0, wx.ALL, 5 )


		bSizer6.Add( bSizer7, 0, wx.EXPAND, 5 )


		bSizer6.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.btn_close = wx.Button( self, wx.ID_ANY, _(u"Ex&it"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.btn_close, 0, wx.ALL, 5 )


		bSizer9.Add( bSizer6, 0, wx.EXPAND, 5 )


		bSizer41.Add( bSizer9, 0, wx.EXPAND|wx.ALL, 5 )


		self.SetSizer( bSizer41 )
		self.Layout()

	def __del__( self ):
		pass


