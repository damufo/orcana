# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

# Copyright (C) 2017 Federacion Galega de Natación (FEGAN) http://www.fegan.org
# Author: Daniel Muñiz Fontoira (2017) <dani@damufo.com>

from reportlab.platypus import SimpleDocTemplate
# from reportlab.platypus import Paragraph
from reportlab.platypus import Table
from reportlab.platypus import PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.lib.pagesizes import A4, landscape, portrait
# from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib import colors
import os

from PIL import Image
# from reportlab.lib.utils import ImageReader, getBytesIO
from specific_classes.fiarna import fegan_logo
from reportlab.lib.utils import ImageReader
import io


class ReportBaseRefereeTokens(object):
    '''
    classdocs
    '''

    def __init__(self, config, file_name,
                 orientation='portrait', title='', subtitle=''):
        '''
        Constructor
        orientation= [portrait|landscape] (vertical|horizontal)
        '''
        self.config = config

        self.colors = colors
        if orientation == 'portrait':  # vertical
            self.page_height = 29.7*cm
            self.page_width = 21*cm
            pagesize = portrait(A4)
        elif orientation == 'landscape':  # landscape
            self.page_height = 21*cm
            self.page_width = 29.7*cm
            pagesize = landscape(A4)
        self.app_path_folder = config.app_path_folder
        self.title = title
        self.subtitle = subtitle
        self.lineas = []
        self.estilonormal = ParagraphStyle('normal',
                                           fontName='Open Sans Regular',
                                           fontSize=10,
                                           alignment=TA_JUSTIFY,
                                           spaceBefore=0*cm,
                                           spaceAfter=0.2*cm,
                                           firstLineIndent=0*cm)
        # import TT font
        fonts_path = '{}{}{}{}'.format(self.app_path_folder, os.sep,
                                       'fonts', os.sep)
        pdfmetrics.registerFont(
            TTFont('Open Sans Regular',
                   '{}{}{}{}'.format(fonts_path,
                                     "open-sans",
                                     os.sep,
                                     "OpenSans-Regular.ttf")))

        self.doc = SimpleDocTemplate(file_name, pagesize=pagesize,
                                     rightMargin=5*mm, leftMargin=5*mm,
                                     topMargin=5*mm, bottomMargin=5*mm)
        self.story = []

    def build_file(self):
        self.doc.build(self.story, onFirstPage=self.my_first_page,
                       onLaterPages=self.my_first_page)

    def insert_page_break(self):
        self.story.append(PageBreak())

    def insert_table(self, table, colWidths=None, rowHeights=None,
                     style=None, pagebreak=False):
        if pagebreak:
            self.story.append(PageBreak())
        t = Table(table, colWidths=colWidths,
                  rowHeights=rowHeights, style=style)
        self.story.append(t)

    def my_first_page(self, canvas, doc):
        canvas.setAuthor('FEGAN')
        canvas.setSubject('')
        canvas.setTitle('')
        canvas.saveState()
        # linhas
        canvas.setStrokeColor('Grey')
        canvas.setLineWidth(0.01)
        canvas.lines(self.lineas)
        # Textos
        canvas.setFont('Open Sans Regular', 7)
        #    cabeceira
#         Liñas de corte
#         Horizontais
#         Left
        canvas.line(doc.leftMargin,
                    self.page_height / 2,
                    doc.leftMargin + (5 * mm),
                    self.page_height / 2)
#         Center
        canvas.line((self.page_width / 2) - (5*mm),
                    (self.page_height / 2),
                    (self.page_width / 2) + (5*mm),
                    (self.page_height / 2))
#         Right
        canvas.line(self.page_width - doc.leftMargin - (5*mm),
                    self.page_height / 2,
                    self.page_width - doc.leftMargin,
                    self.page_height/2)
#         Verticais
#         Top
        canvas.line(self.page_width / 2,
                    self.page_height - doc.topMargin,
                    self.page_width / 2,
                    self.page_height - doc.topMargin - (5 * mm))
#         Midle
        canvas.line(self.page_width / 2,
                    (self.page_height / 2) - (5 * mm),
                    self.page_width / 2,
                    (self.page_height / 2) + (5 * mm))
#         Bottom
        canvas.line(self.page_width / 2,
                    doc.bottomMargin,
                    self.page_width / 2,
                    doc.bottomMargin + (5 * mm))


        for i in range(2):
            desp = 10.1  # desprazar
            baix = 14.85 * i  # baixar
#             impar/par
            logo = ImageReader(io.BytesIO(fegan_logo.getData()))
            # logo = Image.open('%s%s' % (images_path, 'logo_left.png'))
            # logo = ImageReader(getBytesIO(fegan_logo.getData()))
            canvas.drawImage(logo, 8*cm, self.page_height-((baix + 2.5)*cm),
                             width=55, height=55)
            canvas.drawImage(logo, (desp + 8)*cm,
                             self.page_height-((baix + 2.5) * cm),
                             width=55, height=55)
        canvas.restoreState()
