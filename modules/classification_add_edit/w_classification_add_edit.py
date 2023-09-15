# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class ClassificationAddEdit
###########################################################################

class ClassificationAddEdit ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Classification Add Edit"), pos = wx.DefaultPosition, size = wx.Size( 666,478 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer11 = wx.BoxSizer( wx.VERTICAL )

		self.panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer8 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText5 = wx.StaticText( self.panel, wx.ID_ANY, _(u"Classification"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		bSizer8.Add( self.m_staticText5, 0, wx.ALL, 5 )

		self.m_staticline21 = wx.StaticLine( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer8.Add( self.m_staticline21, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText2 = wx.StaticText( self.panel, wx.ID_ANY, _(u"Name:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		bSizer9.Add( self.m_staticText2, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.txt_name = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txt_name.SetMaxLength( 120 )
		bSizer9.Add( self.txt_name, 2, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer8.Add( bSizer9, 0, wx.EXPAND, 5 )

		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText3 = wx.StaticText( self.panel, wx.ID_ANY, _(u"Gender*:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		bSizer10.Add( self.m_staticText3, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		cho_gender_idChoices = []
		self.cho_gender_id = wx.Choice( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cho_gender_idChoices, 0 )
		self.cho_gender_id.SetSelection( 0 )
		bSizer10.Add( self.cho_gender_id, 2, wx.ALL, 5 )


		bSizer8.Add( bSizer10, 0, wx.EXPAND, 5 )

		bSizer103 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText32 = wx.StaticText( self.panel, wx.ID_ANY, _(u"Categories:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText32.Wrap( -1 )

		bSizer103.Add( self.m_staticText32, 1, wx.ALL, 5 )

		clb_categoriesChoices = []
		self.clb_categories = wx.CheckListBox( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, clb_categoriesChoices, 0 )
		bSizer103.Add( self.clb_categories, 2, wx.ALL|wx.EXPAND, 5 )


		bSizer8.Add( bSizer103, 2, wx.EXPAND, 5 )

		bSizer12 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText9 = wx.StaticText( self.panel, wx.ID_ANY, _(u"*If leave gender blank, all categories selected are summed."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )

		bSizer12.Add( self.m_staticText9, 0, wx.ALL, 5 )


		bSizer8.Add( bSizer12, 0, wx.EXPAND, 5 )

		self.m_staticline2 = wx.StaticLine( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer8.Add( self.m_staticline2, 0, wx.ALL|wx.EXPAND, 5 )

		bSizer102 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_cancel = wx.Button( self.panel, wx.ID_ANY, _(u"&Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_cancel.SetToolTip( _(u"Cancel") )

		bSizer102.Add( self.btn_cancel, 0, wx.ALL, 5 )


		bSizer102.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.btn_acept = wx.Button( self.panel, wx.ID_ANY, _(u"&Acept"), wx.DefaultPosition, wx.DefaultSize, 0 )

		self.btn_acept.SetDefault()
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


