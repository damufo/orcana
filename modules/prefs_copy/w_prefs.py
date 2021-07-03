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
## Class Prefs
###########################################################################

class Prefs ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Preferences"), pos = wx.DefaultPosition, size = wx.Size( 492,390 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer4 = wx.BoxSizer( wx.VERTICAL )

		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel1, wx.ID_ANY, _(u"JPG options:") ), wx.VERTICAL )

		bSizer81 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText5 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, _(u"Quality:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		self.m_staticText5.SetToolTip( _(u"Quality when save") )

		bSizer81.Add( self.m_staticText5, 1, wx.ALL, 5 )

		self.spn_jpg_quality = wx.SpinCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 1, 95, 75 )
		self.spn_jpg_quality.SetToolTip( _(u"The image quality, on a scale from 1 (worst) to 95 (best). The default is 75. Values above 95 should be avoided; 100 disables portions of the JPEG compression algorithm, and results in large files with hardly any gain in image quality.") )

		bSizer81.Add( self.spn_jpg_quality, 0, wx.ALL, 5 )


		sbSizer2.Add( bSizer81, 1, wx.EXPAND, 5 )

		bSizer62 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText32 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, _(u"Optimize:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText32.Wrap( -1 )

		bSizer62.Add( self.m_staticText32, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.chb_jpg_optimize = wx.CheckBox( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.chb_jpg_optimize.SetValue(True)
		self.chb_jpg_optimize.SetToolTip( _(u"If true, indicates that the encoder should make an extra pass over the image in order to select optimal encoder settings.") )

		bSizer62.Add( self.chb_jpg_optimize, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		sbSizer2.Add( bSizer62, 1, wx.EXPAND, 5 )

		bSizer621 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText321 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, _(u"Progressive:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText321.Wrap( -1 )

		bSizer621.Add( self.m_staticText321, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.chb_jpg_progressive = wx.CheckBox( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.chb_jpg_progressive.SetValue(True)
		self.chb_jpg_progressive.SetToolTip( _(u"If true, indicates that this image should be stored as a progressive JPEG file.") )

		bSizer621.Add( self.chb_jpg_progressive, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		sbSizer2.Add( bSizer621, 1, wx.EXPAND, 5 )


		bSizer3.Add( sbSizer2, 0, wx.ALL|wx.EXPAND, 5 )

		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel1, wx.ID_ANY, _(u"Auto-resize (px):") ), wx.VERTICAL )

		bSizer41 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText1 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, _(u"Width:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		bSizer41.Add( self.m_staticText1, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.spn_width_px = wx.SpinCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 0, 9999, 0 )
		self.spn_width_px.SetToolTip( _(u"When 0 is not set.") )

		bSizer41.Add( self.spn_width_px, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		sbSizer1.Add( bSizer41, 0, wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText2 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, _(u"Height:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		bSizer5.Add( self.m_staticText2, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.spn_height_px = wx.SpinCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 0, 9999, 0 )
		self.spn_height_px.SetToolTip( _(u"When 0 is not set.") )

		bSizer5.Add( self.spn_height_px, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		sbSizer1.Add( bSizer5, 0, wx.EXPAND|wx.RIGHT|wx.LEFT, 5 )

		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText3 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, _(u"Preserve aspect ratio:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		bSizer6.Add( self.m_staticText3, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.chb_preserve_aspect_ratio = wx.CheckBox( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.chb_preserve_aspect_ratio.SetValue(True)
		bSizer6.Add( self.chb_preserve_aspect_ratio, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		sbSizer1.Add( bSizer6, 0, wx.EXPAND|wx.RIGHT|wx.LEFT, 5 )

		bSizer61 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText31 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, _(u"Save when auto-resize:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )

		bSizer61.Add( self.m_staticText31, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.chb_save_when_autoresize = wx.CheckBox( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		bSizer61.Add( self.chb_save_when_autoresize, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		sbSizer1.Add( bSizer61, 0, wx.EXPAND|wx.RIGHT|wx.LEFT, 5 )


		sbSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )


		bSizer3.Add( sbSizer1, 0, wx.EXPAND|wx.ALL, 5 )

		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_cancel = wx.Button( self.m_panel1, wx.ID_ANY, _(u"&Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.btn_cancel, 0, wx.ALL|wx.ALIGN_BOTTOM, 5 )


		bSizer8.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.btn_acept = wx.Button( self.m_panel1, wx.ID_ANY, _(u"&Acept"), wx.DefaultPosition, wx.DefaultSize, 0 )

		self.btn_acept.SetDefault()
		bSizer8.Add( self.btn_acept, 0, wx.ALL|wx.ALIGN_BOTTOM, 5 )


		bSizer3.Add( bSizer8, 1, wx.EXPAND|wx.BOTTOM, 5 )


		self.m_panel1.SetSizer( bSizer3 )
		self.m_panel1.Layout()
		bSizer3.Fit( self.m_panel1 )
		bSizer4.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 10 )


		self.SetSizer( bSizer4 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


