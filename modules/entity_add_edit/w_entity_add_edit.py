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
## Class EntityAddEdit
###########################################################################

class EntityAddEdit ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Entity Add Edit"), pos = wx.DefaultPosition, size = wx.Size( 703,353 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer11 = wx.BoxSizer( wx.VERTICAL )

		self.panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer8 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText5 = wx.StaticText( self.panel, wx.ID_ANY, _(u"Entity"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		bSizer8.Add( self.m_staticText5, 0, wx.ALL, 5 )

		self.m_staticline21 = wx.StaticLine( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer8.Add( self.m_staticline21, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText2 = wx.StaticText( self.panel, wx.ID_ANY, _(u"Entity code:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		bSizer9.Add( self.m_staticText2, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.txt_entity_code = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txt_entity_code.SetMaxLength( 5 )
		bSizer9.Add( self.txt_entity_code, 2, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer8.Add( bSizer9, 0, wx.EXPAND, 5 )

		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText3 = wx.StaticText( self.panel, wx.ID_ANY, _(u"Short name:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		bSizer10.Add( self.m_staticText3, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.txt_short_name = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txt_short_name.SetMaxLength( 10 )
		bSizer10.Add( self.txt_short_name, 2, wx.ALL, 5 )


		bSizer8.Add( bSizer10, 0, wx.EXPAND, 5 )

		bSizer101 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText31 = wx.StaticText( self.panel, wx.ID_ANY, _(u"Medium name:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )

		bSizer101.Add( self.m_staticText31, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.txt_medium_name = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txt_medium_name.SetMaxLength( 20 )
		bSizer101.Add( self.txt_medium_name, 2, wx.ALL, 5 )


		bSizer8.Add( bSizer101, 0, wx.EXPAND, 5 )

		bSizer1011 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText311 = wx.StaticText( self.panel, wx.ID_ANY, _(u"Long name:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText311.Wrap( -1 )

		bSizer1011.Add( self.m_staticText311, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.txt_long_name = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txt_long_name.SetMaxLength( 40 )
		bSizer1011.Add( self.txt_long_name, 2, wx.ALL, 5 )


		bSizer8.Add( bSizer1011, 0, wx.EXPAND, 5 )


		bSizer8.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_staticline2 = wx.StaticLine( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer8.Add( self.m_staticline2, 0, wx.ALL|wx.EXPAND, 5 )

		bSizer102 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_cancel = wx.Button( self.panel, wx.ID_ANY, _(u"&Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_cancel.SetToolTip( _(u"Cancel") )

		bSizer102.Add( self.btn_cancel, 0, wx.ALL, 5 )


		bSizer102.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.btn_acept = wx.Button( self.panel, wx.ID_ANY, _(u"&Acept"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_acept.SetToolTip( _(u"Acept") )

		bSizer102.Add( self.btn_acept, 0, wx.ALL, 5 )


		bSizer8.Add( bSizer102, 0, wx.EXPAND, 5 )


		bSizer7.Add( bSizer8, 1, wx.ALL|wx.EXPAND, 5 )


		self.panel.SetSizer( bSizer7 )
		self.panel.Layout()
		bSizer7.Fit( self.panel )
		bSizer11.Add( self.panel, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( bSizer11 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


