# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Jun 11 2020)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer18 = wx.BoxSizer( wx.VERTICAL )

		buttons = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_properties = wx.Button( self, wx.ID_ANY, u"Properties", wx.DefaultPosition, wx.DefaultSize, 0 )
		buttons.Add( self.btn_properties, 0, wx.ALL, 5 )

		self.btn_events = wx.Button( self, wx.ID_ANY, u"Events", wx.DefaultPosition, wx.DefaultSize, 0 )
		buttons.Add( self.btn_events, 0, wx.ALL, 5 )

		self.btn_persons = wx.Button( self, wx.ID_ANY, u"Persons", wx.DefaultPosition, wx.DefaultSize, 0 )
		buttons.Add( self.btn_persons, 0, wx.ALL, 5 )


		bSizer18.Add( buttons, 1, wx.EXPAND, 5 )

		main_sizer = wx.BoxSizer( wx.VERTICAL )


		bSizer18.Add( main_sizer, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer18 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


