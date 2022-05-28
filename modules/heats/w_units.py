# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Jun 11 2020)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid

import gettext
_ = gettext.gettext

###########################################################################
## Class Units
###########################################################################

class Units ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1119,865 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, _(u"Units"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		bSizer2.Add( self.m_staticText3, 0, wx.ALL, 5 )

		self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer2.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer7 = wx.BoxSizer( wx.VERTICAL )

		self.lsc_units = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL )
		bSizer7.Add( self.lsc_units, 1, wx.ALL|wx.EXPAND, 5 )

		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

		self.grd_results = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.grd_results.CreateGrid( 1, 5 )
		self.grd_results.EnableEditing( True )
		self.grd_results.EnableGridLines( True )
		self.grd_results.EnableDragGridSize( False )
		self.grd_results.SetMargins( 0, 0 )

		# Columns
		self.grd_results.EnableDragColMove( False )
		self.grd_results.EnableDragColSize( True )
		self.grd_results.SetColLabelSize( 30 )
		self.grd_results.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.grd_results.EnableDragRowSize( True )
		self.grd_results.SetRowLabelSize( 80 )
		self.grd_results.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.grd_results.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer9.Add( self.grd_results, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer7.Add( bSizer9, 1, wx.EXPAND, 5 )

		bSizer101 = wx.BoxSizer( wx.HORIZONTAL )

		self.lsc_results = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL )
		bSizer101.Add( self.lsc_results, 1, wx.ALL|wx.EXPAND, 5 )

		self.lsc_splits = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		bSizer101.Add( self.lsc_splits, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer7.Add( bSizer101, 1, wx.EXPAND, 5 )

		bSizer71 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_year_add = wx.Button( self, wx.ID_ANY, _(u"&+1"), wx.DefaultPosition, wx.Size( -1,-1 ), wx.BU_EXACTFIT )
		self.btn_year_add.SetToolTip( _(u"Add 1 year for all categories") )

		bSizer6.Add( self.btn_year_add, 1, wx.TOP|wx.BOTTOM, 5 )

		self.btn_year_subtract = wx.Button( self, wx.ID_ANY, _(u"&-1"), wx.DefaultPosition, wx.Size( -1,-1 ), wx.BU_EXACTFIT )
		self.btn_year_subtract.SetToolTip( _(u"Substract 1 year for all categories") )

		bSizer6.Add( self.btn_year_subtract, 1, wx.TOP|wx.BOTTOM, 5 )


		bSizer71.Add( bSizer6, 0, wx.RIGHT|wx.LEFT, 5 )

		bSizer72 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_move_down = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		self.btn_move_down.SetToolTip( _(u"Move down") )

		bSizer72.Add( self.btn_move_down, 0, wx.ALL, 5 )

		self.btn_move_up = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		self.btn_move_up.SetToolTip( _(u"Move up") )

		bSizer72.Add( self.btn_move_up, 0, wx.ALL, 5 )


		bSizer71.Add( bSizer72, 0, wx.RIGHT|wx.LEFT, 5 )


		bSizer71.Add( ( 0, 0), 1, 0, 5 )

		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_delete = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		self.btn_delete.SetToolTip( _(u"Delete") )

		bSizer4.Add( self.btn_delete, 0, wx.ALL, 5 )

		self.btn_edit = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		self.btn_edit.SetToolTip( _(u"Edit") )

		bSizer4.Add( self.btn_edit, 0, wx.ALL, 5 )

		self.btn_add = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		self.btn_add.SetToolTip( _(u"Add") )

		bSizer4.Add( self.btn_add, 0, wx.ALL, 5 )

		self.btn_import = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		self.btn_import.SetToolTip( _(u"Import from predefined") )

		bSizer4.Add( self.btn_import, 0, wx.ALL, 5 )


		bSizer71.Add( bSizer4, 0, wx.LEFT, 5 )


		bSizer7.Add( bSizer71, 0, wx.EXPAND, 5 )

		bSizer10 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer10.Add( self.m_staticline1, 0, wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT, 5 )

		self.btn_close = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		self.btn_close.SetToolTip( _(u"Close") )

		bSizer10.Add( self.btn_close, 0, wx.ALIGN_RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT, 5 )


		bSizer7.Add( bSizer10, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5 )


		bSizer2.Add( bSizer7, 1, wx.EXPAND|wx.ALL, 5 )


		self.SetSizer( bSizer2 )
		self.Layout()

	def __del__( self ):
		pass


