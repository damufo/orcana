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
## Class Inscriptions
###########################################################################

class Inscriptions ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1258,659 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, _(u"Inscriptions"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		bSizer2.Add( self.m_staticText3, 0, wx.ALL, 5 )

		self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer2.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer7 = wx.BoxSizer( wx.VERTICAL )

		bSizer73 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, _(u"Phase:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		bSizer73.Add( self.m_staticText4, 0, wx.ALL, 5 )

		cho_phase_idChoices = []
		self.cho_phase_id = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cho_phase_idChoices, 0 )
		self.cho_phase_id.SetSelection( 0 )
		bSizer73.Add( self.cho_phase_id, 1, wx.ALL, 5 )


		bSizer7.Add( bSizer73, 0, wx.EXPAND, 5 )

		self.lsc = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		bSizer7.Add( self.lsc, 1, wx.ALL|wx.EXPAND, 5 )

		bSizer71 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_import = wx.Button( self, wx.ID_ANY, _(u"Im&port"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_import.SetToolTip( _(u"Import from file") )

		bSizer6.Add( self.btn_import, 0, wx.ALL, 5 )

		self.btn_create_sort = wx.Button( self, wx.ID_ANY, _(u"Create sor&t"), wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.btn_create_sort.SetToolTip( _(u"Sort lanes for inscriptions.") )

		bSizer6.Add( self.btn_create_sort, 0, wx.ALL, 5 )

		self.btn_delete_sort = wx.Button( self, wx.ID_ANY, _(u"Delete so&rt"), wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.btn_delete_sort.SetToolTip( _(u"Delete current sort if exists.") )

		bSizer6.Add( self.btn_delete_sort, 0, wx.ALL, 5 )

		self.btn_report_start_list = wx.Button( self, wx.ID_ANY, _(u"Report &start list"), wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.btn_report_start_list.SetToolTip( _(u"Report of start list") )

		bSizer6.Add( self.btn_report_start_list, 0, wx.ALL, 5 )


		bSizer71.Add( bSizer6, 0, wx.RIGHT|wx.LEFT, 5 )


		bSizer71.Add( ( 0, 0), 1, 0, 5 )

		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_members = wx.Button( self, wx.ID_ANY, _(u"Me&mbers"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.btn_members, 0, wx.ALL, 5 )

		self.btn_delete = wx.Button( self, wx.ID_ANY, _(u"D&elete"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.btn_delete, 1, wx.ALL, 5 )

		self.btn_edit = wx.Button( self, wx.ID_ANY, _(u"Ed&it"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.btn_edit, 1, wx.ALL, 5 )

		self.btn_add = wx.Button( self, wx.ID_ANY, _(u"A&dd"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.btn_add, 1, wx.ALL, 5 )


		bSizer71.Add( bSizer4, 0, 0, 5 )


		bSizer7.Add( bSizer71, 0, wx.EXPAND, 5 )

		bSizer10 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer10.Add( self.m_staticline1, 0, wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT, 5 )

		self.btn_back = wx.Button( self, wx.ID_ANY, _(u"B&ack"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.btn_back, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )


		bSizer7.Add( bSizer10, 0, wx.EXPAND, 5 )


		bSizer2.Add( bSizer7, 1, wx.EXPAND|wx.ALL, 5 )


		self.SetSizer( bSizer2 )
		self.Layout()

	def __del__( self ):
		pass


