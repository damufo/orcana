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
## Class Persons
###########################################################################

class Persons ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1311,937 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, _(u"Persons"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		bSizer2.Add( self.m_staticText3, 0, wx.ALL, 5 )

		self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer2.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer7 = wx.BoxSizer( wx.VERTICAL )

		self.spl_persons = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_3DBORDER|wx.SP_3DSASH|wx.SP_BORDER|wx.SP_LIVE_UPDATE )
		self.spl_persons.Bind( wx.EVT_IDLE, self.spl_personsOnIdle )
		self.spl_persons.SetMinimumPaneSize( 100 )

		self.m_panel1 = wx.Panel( self.spl_persons, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel1.SetMinSize( wx.Size( -1,200 ) )

		bSizer13 = wx.BoxSizer( wx.VERTICAL )

		self.lsc_persons = wx.ListCtrl( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		bSizer13.Add( self.lsc_persons, 1, wx.ALL|wx.EXPAND, 5 )

		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )


		bSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.btn_delete = wx.Button( self.m_panel1, wx.ID_ANY, _(u"D&elete"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_delete.SetToolTip( _(u"Delete") )

		bSizer4.Add( self.btn_delete, 0, wx.ALL, 5 )

		self.btn_edit = wx.Button( self.m_panel1, wx.ID_ANY, _(u"Ed&it"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_edit.SetToolTip( _(u"Edit") )

		bSizer4.Add( self.btn_edit, 0, wx.ALL, 5 )

		self.btn_add = wx.Button( self.m_panel1, wx.ID_ANY, _(u"A&dd"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_add.SetToolTip( _(u"Add") )

		bSizer4.Add( self.btn_add, 0, wx.ALL, 5 )


		bSizer13.Add( bSizer4, 0, wx.EXPAND, 5 )

		self.m_staticline3 = wx.StaticLine( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer13.Add( self.m_staticline3, 0, wx.EXPAND, 5 )


		self.m_panel1.SetSizer( bSizer13 )
		self.m_panel1.Layout()
		bSizer13.Fit( self.m_panel1 )
		self.m_panel2 = wx.Panel( self.spl_persons, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel2.SetMinSize( wx.Size( -1,100 ) )

		bSizer14 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticline4 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer14.Add( self.m_staticline4, 0, wx.EXPAND, 5 )

		self.lsc_inscriptions_ind = wx.ListCtrl( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		bSizer14.Add( self.lsc_inscriptions_ind, 1, wx.ALL|wx.EXPAND, 5 )

		bSizer41 = wx.BoxSizer( wx.HORIZONTAL )


		bSizer41.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.btn_delete_insc = wx.Button( self.m_panel2, wx.ID_ANY, _(u"D&elete"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_delete_insc.SetToolTip( _(u"Delete") )

		bSizer41.Add( self.btn_delete_insc, 0, wx.ALL, 5 )

		self.btn_edit_insc = wx.Button( self.m_panel2, wx.ID_ANY, _(u"Ed&it"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_edit_insc.SetToolTip( _(u"Edit") )

		bSizer41.Add( self.btn_edit_insc, 0, wx.ALL, 5 )

		self.btn_add_insc = wx.Button( self.m_panel2, wx.ID_ANY, _(u"A&dd"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_add_insc.SetToolTip( _(u"Add") )

		bSizer41.Add( self.btn_add_insc, 0, wx.ALL, 5 )


		bSizer14.Add( bSizer41, 0, wx.EXPAND, 5 )


		self.m_panel2.SetSizer( bSizer14 )
		self.m_panel2.Layout()
		bSizer14.Fit( self.m_panel2 )
		self.spl_persons.SplitHorizontally( self.m_panel1, self.m_panel2, 400 )
		bSizer7.Add( self.spl_persons, 1, wx.EXPAND, 5 )

		bSizer10 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer10.Add( self.m_staticline1, 0, wx.EXPAND|wx.ALL, 5 )

		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_import = wx.Button( self, wx.ID_ANY, _(u"Import"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_import.SetToolTip( _(u"Import") )

		bSizer6.Add( self.btn_import, 0, wx.ALL, 5 )


		bSizer6.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.btn_back = wx.Button( self, wx.ID_ANY, _(u"B&ack"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_back.SetToolTip( _(u"Back") )

		bSizer6.Add( self.btn_back, 0, wx.ALL, 5 )


		bSizer10.Add( bSizer6, 0, wx.EXPAND, 5 )


		bSizer7.Add( bSizer10, 0, wx.EXPAND, 5 )


		bSizer2.Add( bSizer7, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer2 )
		self.Layout()

	def __del__( self ):
		pass

	def spl_personsOnIdle( self, event ):
		self.spl_persons.SetSashPosition( 400 )
		self.spl_persons.Unbind( wx.EVT_IDLE )


