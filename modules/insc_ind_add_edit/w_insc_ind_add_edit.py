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
## Class InscIndAddEdit
###########################################################################

class InscIndAddEdit ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Inscriptions Individual Add Edit"), pos = wx.DefaultPosition, size = wx.Size( 708,655 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer11 = wx.BoxSizer( wx.VERTICAL )

		self.panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer8 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText5 = wx.StaticText( self.panel, wx.ID_ANY, _(u"Inscription individual"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		bSizer8.Add( self.m_staticText5, 0, wx.ALL, 5 )

		self.m_staticline21 = wx.StaticLine( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer8.Add( self.m_staticline21, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText2 = wx.StaticText( self.panel, wx.ID_ANY, _(u"Event:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		bSizer9.Add( self.m_staticText2, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		cho_phase_idChoices = []
		self.cho_phase_id = wx.Choice( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cho_phase_idChoices, 0 )
		self.cho_phase_id.SetSelection( 0 )
		bSizer9.Add( self.cho_phase_id, 2, wx.ALL, 5 )

		self.lbl_phase_name = wx.StaticText( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_phase_name.Wrap( -1 )

		bSizer9.Add( self.lbl_phase_name, 2, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer8.Add( bSizer9, 0, wx.EXPAND, 5 )

		bSizer91 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText21 = wx.StaticText( self.panel, wx.ID_ANY, _(u"Person:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )

		bSizer91.Add( self.m_staticText21, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.lbl_person_full_name = wx.StaticText( self.panel, wx.ID_ANY, _(u"Person full name"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_person_full_name.Wrap( -1 )

		bSizer91.Add( self.lbl_person_full_name, 2, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizer111 = wx.BoxSizer( wx.HORIZONTAL )

		self.txt_person_full_name = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txt_person_full_name.SetToolTip( _(u"Person full name (surname, name)") )

		bSizer111.Add( self.txt_person_full_name, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.btn_add_person = wx.Button( self.panel, wx.ID_ANY, _(u"+"), wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		bSizer111.Add( self.btn_add_person, 0, wx.ALL, 5 )


		bSizer91.Add( bSizer111, 2, wx.EXPAND, 5 )


		bSizer8.Add( bSizer91, 0, wx.EXPAND, 5 )

		bSizer103 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText32 = wx.StaticText( self.panel, wx.ID_ANY, _(u"License:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText32.Wrap( -1 )

		bSizer103.Add( self.m_staticText32, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.lbl_license = wx.StaticText( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_license.Wrap( -1 )

		bSizer103.Add( self.lbl_license, 2, wx.ALL, 5 )


		bSizer8.Add( bSizer103, 0, wx.EXPAND, 5 )

		bSizer104 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText33 = wx.StaticText( self.panel, wx.ID_ANY, _(u"Entity:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText33.Wrap( -1 )

		bSizer104.Add( self.m_staticText33, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.lbl_entity_short_name = wx.StaticText( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_entity_short_name.Wrap( -1 )

		bSizer104.Add( self.lbl_entity_short_name, 1, wx.ALL, 5 )

		self.lbl_entity_code = wx.StaticText( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_entity_code.Wrap( -1 )

		bSizer104.Add( self.lbl_entity_code, 1, wx.ALL, 5 )


		bSizer8.Add( bSizer104, 0, wx.EXPAND, 5 )

		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText3 = wx.StaticText( self.panel, wx.ID_ANY, _(u"Mark:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		bSizer10.Add( self.m_staticText3, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.txt_mark = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.txt_mark, 2, wx.ALL, 5 )


		bSizer8.Add( bSizer10, 0, wx.EXPAND, 5 )

		bSizer1011 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText311 = wx.StaticText( self.panel, wx.ID_ANY, _(u"Pool:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText311.Wrap( -1 )

		bSizer1011.Add( self.m_staticText311, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		cho_pool_lengthChoices = []
		self.cho_pool_length = wx.Choice( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cho_pool_lengthChoices, 0 )
		self.cho_pool_length.SetSelection( 0 )
		bSizer1011.Add( self.cho_pool_length, 2, wx.ALL, 5 )


		bSizer8.Add( bSizer1011, 0, wx.EXPAND, 5 )

		bSizer10112 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText3112 = wx.StaticText( self.panel, wx.ID_ANY, _(u"Chrono:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3112.Wrap( -1 )

		bSizer10112.Add( self.m_staticText3112, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		cho_chrono_typeChoices = []
		self.cho_chrono_type = wx.Choice( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cho_chrono_typeChoices, 0 )
		self.cho_chrono_type.SetSelection( 0 )
		bSizer10112.Add( self.cho_chrono_type, 2, wx.ALL, 5 )


		bSizer8.Add( bSizer10112, 0, wx.EXPAND, 5 )

		bSizer101 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText31 = wx.StaticText( self.panel, wx.ID_ANY, _(u"Date:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )

		bSizer101.Add( self.m_staticText31, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.txt_date = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer101.Add( self.txt_date, 2, wx.ALL, 5 )


		bSizer8.Add( bSizer101, 0, wx.EXPAND, 5 )

		bSizer1012 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText312 = wx.StaticText( self.panel, wx.ID_ANY, _(u"Venue:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText312.Wrap( -1 )

		bSizer1012.Add( self.m_staticText312, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.txt_venue = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1012.Add( self.txt_venue, 2, wx.ALL, 5 )


		bSizer8.Add( bSizer1012, 0, wx.EXPAND, 5 )

		bSizer101111 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText31111 = wx.StaticText( self.panel, wx.ID_ANY, _(u"Rejected:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31111.Wrap( -1 )

		bSizer101111.Add( self.m_staticText31111, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.chb_rejected = wx.CheckBox( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer101111.Add( self.chb_rejected, 2, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer8.Add( bSizer101111, 0, wx.EXPAND, 5 )

		bSizer101112 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText31112 = wx.StaticText( self.panel, wx.ID_ANY, _(u"Exchanged:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31112.Wrap( -1 )

		bSizer101112.Add( self.m_staticText31112, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.chb_exchanged = wx.CheckBox( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer101112.Add( self.chb_exchanged, 2, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer8.Add( bSizer101112, 0, wx.EXPAND, 5 )

		bSizer101113 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText31113 = wx.StaticText( self.panel, wx.ID_ANY, _(u"Score:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31113.Wrap( -1 )

		bSizer101113.Add( self.m_staticText31113, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.chb_score = wx.CheckBox( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer101113.Add( self.chb_score, 2, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer8.Add( bSizer101113, 0, wx.EXPAND, 5 )

		bSizer101114 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText31114 = wx.StaticText( self.panel, wx.ID_ANY, _(u"Classify:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31114.Wrap( -1 )

		bSizer101114.Add( self.m_staticText31114, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.chb_classify = wx.CheckBox( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer101114.Add( self.chb_classify, 2, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer8.Add( bSizer101114, 0, wx.EXPAND, 5 )


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


