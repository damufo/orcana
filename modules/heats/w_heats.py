# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.1.0-0-g733bf3d)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
from .custom_grid import CustomGrid

# import gettext
# _ = gettext.gettext

###########################################################################
## Class Heats
###########################################################################

class Heats ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1388,865 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		self.spl_heats = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_3DBORDER|wx.SP_3DSASH|wx.SP_BORDER|wx.SP_LIVE_UPDATE )
		self.spl_heats.Bind( wx.EVT_IDLE, self.spl_heatsOnIdle )
		self.spl_heats.SetMinimumPaneSize( 100 )

		self.m_panel1 = wx.Panel( self.spl_heats, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer91 = wx.BoxSizer( wx.VERTICAL )

		bSizer102 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText3 = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"Heats"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		bSizer102.Add( self.m_staticText3, 0, wx.ALL, 5 )

		self.m_staticline2 = wx.StaticLine( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer102.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )


		bSizer91.Add( bSizer102, 0, wx.EXPAND, 5 )

		self.lsc_heats = wx.ListCtrl( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL )
		bSizer91.Add( self.lsc_heats, 1, wx.EXPAND|wx.ALL, 5 )

		self.m_staticline4 = wx.StaticLine( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer91.Add( self.m_staticline4, 0, wx.EXPAND, 5 )


		self.m_panel1.SetSizer( bSizer91 )
		self.m_panel1.Layout()
		bSizer91.Fit( self.m_panel1 )
		self.m_panel2 = wx.Panel( self.spl_heats, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer7 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticline3 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer7.Add( self.m_staticline3, 0, wx.EXPAND, 5 )

		bSizer13 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText2 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"Arrival order:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		bSizer8.Add( self.m_staticText2, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.lbl_arrival_order = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"4 , 3 , 2 , 6 , 5 ,1"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self.lbl_arrival_order.Wrap( -1 )

		bSizer8.Add( self.lbl_arrival_order, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer13.Add( bSizer8, 1, wx.EXPAND, 5 )

		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_official = wx.Button( self.m_panel2, wx.ID_ANY, _(u"&Official"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_official.SetToolTip( _(u"Toggle official") )

		bSizer11.Add( self.btn_official, 1, wx.ALL, 5 )

		self.btn_next = wx.Button( self.m_panel2, wx.ID_ANY, _(u"&Next"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_next.SetToolTip( _(u"Next heat") )

		bSizer11.Add( self.btn_next, 1, wx.ALL, 5 )

		self.btn_start_list = wx.Button( self.m_panel2, wx.ID_ANY, _(u"Sta&rt list"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_start_list.SetToolTip( _(u"Generate results report") )

		bSizer11.Add( self.btn_start_list, 1, wx.ALL, 5 )

		self.btn_results_report = wx.Button( self.m_panel2, wx.ID_ANY, _(u"&Results report"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_results_report.SetToolTip( _(u"Generate results report") )

		bSizer11.Add( self.btn_results_report, 1, wx.ALL, 5 )

		self.btn_classifications_report = wx.Button( self.m_panel2, wx.ID_ANY, _(u"Cla&ssif. report"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_classifications_report.SetToolTip( _(u"Generate clasifications report") )

		bSizer11.Add( self.btn_classifications_report, 1, wx.ALL, 5 )

		self.btn_phase_category_results = wx.Button( self.m_panel2, wx.ID_ANY, _(u"Phase r&esults"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_phase_category_results.SetToolTip( _(u"List phase categoríes results.") )

		bSizer11.Add( self.btn_phase_category_results, 1, wx.ALL, 5 )

		self.btn_medals_report = wx.Button( self.m_panel2, wx.ID_ANY, _(u"Me&dals"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.btn_medals_report, 1, wx.ALL, 5 )


		bSizer13.Add( bSizer11, 0, wx.EXPAND, 5 )


		bSizer7.Add( bSizer13, 0, wx.EXPAND, 5 )

		self.grd_results = CustomGrid(self.m_panel2)
		self.grd_results.CreateGrid( 1, 6 )
		bSizer7.Add( self.grd_results, 1, wx.ALL|wx.EXPAND, 5 )

		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

		self.chb_go_to_first = wx.CheckBox( self.m_panel2, wx.ID_ANY, _(u"Go to &first when heat change:"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.chb_go_to_first.SetValue(True)
		self.chb_go_to_first.SetToolTip( _(u"Go to first lane when heat change.") )

		bSizer9.Add( self.chb_go_to_first, 0, wx.ALL, 5 )


		bSizer9.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		bSizer101 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_members = wx.Button( self.m_panel2, wx.ID_ANY, _(u"Me&mbers"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer101.Add( self.btn_members, 1, wx.ALL|wx.EXPAND, 5 )

		self.btn_change_participant = wx.Button( self.m_panel2, wx.ID_ANY, _(u"Chan&ge"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_change_participant.SetToolTip( _(u"Edit participant") )

		bSizer101.Add( self.btn_change_participant, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer9.Add( bSizer101, 0, 0, 5 )


		bSizer7.Add( bSizer9, 0, wx.EXPAND, 5 )

		bSizer10 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticline1 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer10.Add( self.m_staticline1, 0, wx.EXPAND|wx.ALL, 5 )

		self.btn_back = wx.Button( self.m_panel2, wx.ID_ANY, _(u"B&ack"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_back.SetToolTip( _(u"Go back") )

		bSizer10.Add( self.btn_back, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )


		bSizer7.Add( bSizer10, 0, wx.EXPAND, 5 )


		self.m_panel2.SetSizer( bSizer7 )
		self.m_panel2.Layout()
		bSizer7.Fit( self.m_panel2 )
		self.spl_heats.SplitHorizontally( self.m_panel1, self.m_panel2, 400 )
		bSizer2.Add( self.spl_heats, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer2 )
		self.Layout()

	def __del__( self ):
		pass

	def spl_heatsOnIdle( self, event ):
		self.spl_heats.SetSashPosition( 400 )
		self.spl_heats.Unbind( wx.EVT_IDLE )


