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
## Class Properties
###########################################################################

class Properties ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 920,630 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer8 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, _(u"Properties"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		bSizer8.Add( self.m_staticText5, 0, wx.ALL, 5 )

		self.m_staticline21 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer8.Add( self.m_staticline21, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )


		bSizer8.Add( bSizer9, 0, wx.EXPAND, 5 )

		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, _(u"Championship name:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		fgSizer1.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.txt_champ_name = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.txt_champ_name, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, _(u"Pool length:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		fgSizer1.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		cho_pool_lengthChoices = [ _(u"25"), _(u"50") ]
		self.cho_pool_length = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cho_pool_lengthChoices, 0 )
		self.cho_pool_length.SetSelection( 0 )
		fgSizer1.Add( self.cho_pool_length, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText31 = wx.StaticText( self, wx.ID_ANY, _(u"Pool lanes sort:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )

		fgSizer1.Add( self.m_staticText31, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.txt_pool_lanes_sort = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txt_pool_lanes_sort.SetToolTip( _(u"Pool lane from best to worst separated by hyphen.") )

		fgSizer1.Add( self.txt_pool_lanes_sort, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText311 = wx.StaticText( self, wx.ID_ANY, _(u"Chrono type:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText311.Wrap( -1 )

		fgSizer1.Add( self.m_staticText311, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		cho_chrono_typeChoices = [ _(u"Manual"), _(u"Electronic") ]
		self.cho_chrono_type = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cho_chrono_typeChoices, 0 )
		self.cho_chrono_type.SetSelection( 0 )
		fgSizer1.Add( self.cho_chrono_type, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText3111 = wx.StaticText( self, wx.ID_ANY, _(u"Estament:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3111.Wrap( -1 )

		fgSizer1.Add( self.m_staticText3111, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		cho_estament_idChoices = []
		self.cho_estament_id = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cho_estament_idChoices, 0 )
		self.cho_estament_id.SetSelection( 0 )
		fgSizer1.Add( self.cho_estament_id, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText21 = wx.StaticText( self, wx.ID_ANY, _(u"Date age calculation:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )

		fgSizer1.Add( self.m_staticText21, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.txt_date_age_calculation = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txt_date_age_calculation.SetMaxLength( 12 )
		fgSizer1.Add( self.txt_date_age_calculation, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.m_staticText211 = wx.StaticText( self, wx.ID_ANY, _(u"Venue:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText211.Wrap( -1 )

		fgSizer1.Add( self.m_staticText211, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.txt_venue = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txt_venue.SetMaxLength( 34 )
		fgSizer1.Add( self.txt_venue, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.lbl_dbs_path = wx.StaticText( self, wx.ID_ANY, _(u"Database path:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_dbs_path.Wrap( -1 )

		fgSizer1.Add( self.lbl_dbs_path, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.txt_dbs_path = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		fgSizer1.Add( self.txt_dbs_path, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer8.Add( fgSizer1, 0, wx.EXPAND, 5 )


		bSizer8.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		bSizer12 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_generate_champ = wx.Button( self, wx.ID_ANY, _(u"&Generate champ"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_generate_champ.SetToolTip( _(u"Generate champ automatic:\nsessions, phases, heats...") )

		bSizer12.Add( self.btn_generate_champ, 1, wx.ALL, 5 )

		self.btn_fiarna = wx.Button( self, wx.ID_ANY, _(u"Re&feree tokens"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_fiarna.SetToolTip( _(u"Fiarna") )

		bSizer12.Add( self.btn_fiarna, 1, wx.ALL, 5 )

		self.btn_web_forms_files = wx.Button( self, wx.ID_ANY, _(u"&Web forms files"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_web_forms_files.SetToolTip( _(u"Report inscriptions") )

		bSizer12.Add( self.btn_web_forms_files, 1, wx.ALL, 5 )


		bSizer8.Add( bSizer12, 0, wx.EXPAND, 5 )

		bSizer103 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_report_inscriptions = wx.Button( self, wx.ID_ANY, _(u"Report ins&criptions"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_report_inscriptions.SetToolTip( _(u"Report inscriptions") )

		bSizer103.Add( self.btn_report_inscriptions, 1, wx.ALL, 5 )

		self.btn_report_start_list_pdf = wx.Button( self, wx.ID_ANY, _(u"Report start list &PDF"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_report_start_list_pdf.SetToolTip( _(u"Generate PDF report heats") )

		bSizer103.Add( self.btn_report_start_list_pdf, 1, wx.ALL, 5 )

		self.btn_report_start_list_html = wx.Button( self, wx.ID_ANY, _(u"Report start list &HTML"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer103.Add( self.btn_report_start_list_html, 1, wx.ALL, 5 )


		bSizer8.Add( bSizer103, 0, wx.EXPAND, 5 )

		bSizer1031 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_sessions = wx.Button( self, wx.ID_ANY, _(u"S&essions"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1031.Add( self.btn_sessions, 1, wx.ALL, 5 )

		self.btn_punctuations = wx.Button( self, wx.ID_ANY, _(u"P&unctuations"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1031.Add( self.btn_punctuations, 1, wx.ALL, 5 )

		self.btn_classifications = wx.Button( self, wx.ID_ANY, _(u"Cla&ssifications"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_classifications.SetToolTip( _(u"Generate PDF report heats") )

		bSizer1031.Add( self.btn_classifications, 1, wx.ALL, 5 )


		bSizer8.Add( bSizer1031, 0, wx.EXPAND, 5 )

		self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer8.Add( self.m_staticline2, 0, wx.ALL|wx.EXPAND, 5 )

		bSizer102 = wx.BoxSizer( wx.VERTICAL )

		self.btn_back = wx.Button( self, wx.ID_ANY, _(u"B&ack"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer102.Add( self.btn_back, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )


		bSizer8.Add( bSizer102, 0, wx.EXPAND, 5 )

		gSizer1 = wx.GridSizer( 0, 2, 0, 0 )


		bSizer8.Add( gSizer1, 1, wx.EXPAND, 5 )


		bSizer7.Add( bSizer8, 1, wx.ALL|wx.EXPAND, 5 )


		self.SetSizer( bSizer7 )
		self.Layout()

	def __del__( self ):
		pass


