# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Jun  1 2020)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

# import gettext
# _ = gettext.gettext

###########################################################################
## Class Resize
###########################################################################

class Resize ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Resize"), pos = wx.DefaultPosition, size = wx.Size( 435,257 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer4 = wx.BoxSizer( wx.VERTICAL )

		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		bSizer41 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText1 = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"Width:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		bSizer41.Add( self.m_staticText1, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.spn_width_px = wx.SpinCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 1, 9999, 1 )
		bSizer41.Add( self.spn_width_px, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.spn_width_percent = wx.SpinCtrlDouble( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 1, 400, 100, 1 )
		self.spn_width_percent.SetDigits( 2 )
		self.spn_width_percent.Hide()

		bSizer41.Add( self.spn_width_percent, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer3.Add( bSizer41, 0, wx.EXPAND, 5 )

		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText2 = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"Height:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		bSizer5.Add( self.m_staticText2, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.spn_height_px = wx.SpinCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 1, 9999, 1 )
		bSizer5.Add( self.spn_height_px, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.spn_height_percent = wx.SpinCtrlDouble( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 1, 400, 100, 1 )
		self.spn_height_percent.SetDigits( 2 )
		self.spn_height_percent.Hide()

		bSizer5.Add( self.spn_height_percent, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer3.Add( bSizer5, 0, wx.EXPAND, 5 )

		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText4 = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"Units:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		bSizer7.Add( self.m_staticText4, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		cho_unitsChoices = [ _(u"pixels"), _(u"percentages") ]
		self.cho_units = wx.Choice( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cho_unitsChoices, 0 )
		self.cho_units.SetSelection( 0 )
		bSizer7.Add( self.cho_units, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer3.Add( bSizer7, 0, wx.EXPAND, 5 )

		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText3 = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"Preserve aspect ratio:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		bSizer6.Add( self.m_staticText3, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.chb_preserve_aspect_ratio = wx.CheckBox( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.chb_preserve_aspect_ratio.SetValue(True)
		bSizer6.Add( self.chb_preserve_aspect_ratio, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer3.Add( bSizer6, 0, wx.EXPAND, 5 )

		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_cancel = wx.Button( self.m_panel1, wx.ID_ANY, _(u"&Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.btn_cancel, 0, wx.ALL|wx.ALIGN_BOTTOM, 5 )


		bSizer8.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.btn_acept = wx.Button( self.m_panel1, wx.ID_ANY, _(u"&Acept"), wx.DefaultPosition, wx.DefaultSize, 0 )

		self.btn_acept.SetDefault()
		bSizer8.Add( self.btn_acept, 0, wx.ALL|wx.ALIGN_BOTTOM, 5 )


		bSizer3.Add( bSizer8, 1, wx.EXPAND, 5 )


		self.m_panel1.SetSizer( bSizer3 )
		self.m_panel1.Layout()
		bSizer3.Fit( self.m_panel1 )
		bSizer4.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 10 )


		self.SetSizer( bSizer4 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


