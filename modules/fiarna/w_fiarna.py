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

class Main ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Fiarna"), pos = wx.DefaultPosition, size = wx.Size( 479,406 ), style = wx.CAPTION|wx.BORDER_NONE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )


		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


###########################################################################
## Class Fiarna
###########################################################################

class Fiarna ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Fiarna"), pos = wx.DefaultPosition, size = wx.Size( 644,337 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer12 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText3 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"Generator of referee's tokens for swimming"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
		self.m_staticText3.Wrap( -1 )

		self.m_staticText3.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		bSizer12.Add( self.m_staticText3, 0, wx.ALL|wx.EXPAND, 15 )

		bSizer82 = wx.BoxSizer( wx.VERTICAL )


		bSizer12.Add( bSizer82, 1, wx.EXPAND, 5 )

		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText7 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"From event:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )

		bSizer8.Add( self.m_staticText7, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.spn_from_event = wx.SpinCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 999, 0 )
		bSizer8.Add( self.spn_from_event, 0, wx.ALL, 5 )


		bSizer12.Add( bSizer8, 0, wx.EXPAND, 5 )

		bSizer81 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText71 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"To event:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText71.Wrap( -1 )

		bSizer81.Add( self.m_staticText71, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.spn_to_event = wx.SpinCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 999, 99 )
		bSizer81.Add( self.spn_to_event, 0, wx.ALL, 5 )


		bSizer12.Add( bSizer81, 0, wx.EXPAND, 5 )

		bSizer811 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText711 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"Phase:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText711.Wrap( -1 )

		bSizer811.Add( self.m_staticText711, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		cho_phaseChoices = [ _(u"All"), _(u"Final"), _(u"Preliminar") ]
		self.cho_phase = wx.Choice( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cho_phaseChoices, 0 )
		self.cho_phase.SetSelection( 0 )
		bSizer811.Add( self.cho_phase, 0, wx.ALL, 5 )


		bSizer12.Add( bSizer811, 0, wx.EXPAND, 5 )

		bSizer101 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText72 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"Sort:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText72.Wrap( -1 )

		bSizer101.Add( self.m_staticText72, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		cho_sortChoices = [ _(u"Por pista"), _(u"Por proba") ]
		self.cho_sort = wx.Choice( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cho_sortChoices, 0 )
		self.cho_sort.SetSelection( 0 )
		bSizer101.Add( self.cho_sort, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer12.Add( bSizer101, 0, wx.EXPAND, 5 )


		bSizer12.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		bSizer13 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_close = wx.Button( self.m_panel2, wx.ID_ANY, _(u"&Close"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer13.Add( self.btn_close, 0, wx.ALL, 5 )


		bSizer13.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.btn_gen_referee_tokens = wx.Button( self.m_panel2, wx.ID_ANY, _(u"Generate re&feree's tokens"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_gen_referee_tokens.SetToolTip( _(u"Generate re&feree's tokens") )

		bSizer13.Add( self.btn_gen_referee_tokens, 0, wx.ALL, 5 )


		bSizer12.Add( bSizer13, 0, wx.EXPAND, 5 )


		self.m_panel2.SetSizer( bSizer12 )
		self.m_panel2.Layout()
		bSizer12.Fit( self.m_panel2 )
		bSizer1.Add( self.m_panel2, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


