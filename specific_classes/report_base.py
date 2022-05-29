#!/usr/bin/env python
# -*- coding: utf-8 -*-


from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus import Table
from reportlab.platypus import PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from PIL import Image
import os
import copy

from specific_functions import datetimes


class ReportBase(object):

    def __init__(self, config, file_name, orientation='portrait', title='',
                 subtitle=''):
        '''
        Constructor
        orientation= [portrait|landscape] (vertical|horizontal)
        '''
        self.config = config

        self.colors = colors
        if orientation == 'portrait': #vertical
            self.page_height = 29.7*cm
            self.page_width = 21*cm
            pagesize = portrait(A4)
        elif orientation == 'landscape': #landscape
            self.page_height = 21*cm
            self.page_width = 29.7*cm
            pagesize = landscape(A4)
        self.app_path_folder = config.app_path_folder
        images_path = '%s%s%s%s' % (self.app_path_folder, os.sep, 
                                    'images', os.sep)
        self.title = title
        self.subtitle = subtitle
        self.logo = Image.open('%s%s' % (images_path, 'logo_left.png'))

        l1 = (1*cm, self.page_height-2.3*cm, self.page_width-1.5*cm, self.page_height-2.3*cm)
        l2 = (1*cm, 1.5*cm, self.page_width-1.5*cm, 1.5*cm)
#        self.lineas = [l1,l2]
#        self.lineas = [l2] #só liña de embaixo
        self.lineas = []  # ningunha
        self.estiloencabezado = ParagraphStyle('',
                                      fontName='Open Sans Bold',
                                      fontSize=8,
                                      #FIXME: fontStyle='small-cups', isto non funciona
                                      alignment=TA_CENTER,
                                      spaceBefore=0.5*cm,
                                      spaceAfter=0*cm,
                                      leftIndent=-1*cm,
                                      rightIndent=-0.7*cm)
        self.estiloencabezado2 = ParagraphStyle('',
                                      fontName='Open Sans Bold',
                                      fontSize=6,
                                      #FIXME: fontStyle='small-cups', isto non funciona
                                      alignment=TA_CENTER,
                                      spaceBefore=0.5*cm,
                                      spaceAfter=0*cm,
                                      leftIndent=-1*cm,
                                      rightIndent=-0.7*cm)         
        self.style_normal = ParagraphStyle('normal',
                                           fontName='Open Sans Regular',
                                           fontSize=10,
                                           alignment=TA_JUSTIFY,
                                           spaceBefore=0*cm,
                                           spaceAfter=0.2*cm,
                                           firstLineIndent=0*cm,
#                                         topIndent =-1*cm,
#                                         leftIndent=-1*cm,
#                                         rightIndent=-0.7*cm
                                           )
        self.style_normal_right = ParagraphStyle('normal_right',
                                      parent=self.style_normal,
                                      alignment=TA_RIGHT
                                      )
        self.style_normal_left = ParagraphStyle('normal_left',
                                      parent=self.style_normal,
                                      alignment=TA_LEFT
                                      )
        self.style_normal_center = ParagraphStyle('normal_center',
                                      parent=self.style_normal,
                                      alignment=TA_CENTER
                                      )
        self.style_normal_justify = ParagraphStyle('normal_justify',
                                      parent=self.style_normal,
                                      alignment=TA_JUSTIFY
                                      )
        self.contido_taboa = ParagraphStyle('normal',
                                            fontName='Open Sans Regular',
#                                            fontSize=9,
#                                            alignment=TA_JUSTIFY,
#                                            spaceBefore=0*cm,
#                                            spaceAfter=0.2*cm,
#                                            firstLineIndent=0*cm,
#                                         topIndent =-1*cm,
#                                         leftIndent=-1*cm,
#                                         rightIndent=-0.7*cm
                                           )
        self.titulo1 = ParagraphStyle('',
                                      fontName='Open Sans Regular',
                                      fontSize=12,
                                      alignment=TA_CENTER,
                                      spaceBefore=0.5*cm,
                                      spaceAfter=0*cm,
        #                              leftIndent=-1*cm,
        #                              rightIndent=-0.7*cm
                                      )

        self.t1_table = ParagraphStyle('',
                                      fontName='Open Sans Regular',
                                      fontSize=12,
                                      alignment=TA_CENTER,
                                      spaceBefore=1.5*cm,
                                      spaceAfter=0.5*cm,
        #                              leftIndent=-1*cm,
        #                              rightIndent=-0.7*cm
                                      )

        self.titulo2 = ParagraphStyle('',
                                      fontName='Open Sans Regular',
                                      fontSize=10,
                                      alignment=TA_CENTER,
                                      spaceBefore=0.5*cm,
                                      spaceAfter=0*cm,
        #                              leftIndent=-1*cm,
        #                              rightIndent=-0.7*cm
                                      )
        self.titulo1_center = copy.copy(self.titulo1)
        self.titulo1_center.alignment = 1

        self.titulo1_left = copy.copy(self.titulo1)
        self.titulo1_left.alignment = 0

        self.t2_table = ParagraphStyle('',
                                      fontName='Open Sans Regular',
                                      fontSize=10,
                                      alignment=TA_CENTER,
                                      spaceBefore=5.5*cm,
                                      spaceAfter=0.5*cm,
                                      topIndent=3*cm,
        #                              leftIndent=-1*cm,
        #                              rightIndent=-0.7*cm
                                      )
        self.titulo3 = ParagraphStyle('',
                                      fontName='Open Sans Bold',
                                      fontSize=10,
                                      alignment=TA_CENTER,
                                      spaceBefore=0.5*cm,
                                      spaceAfter=0*cm,
                                      leftIndent=-1*cm,
                                      rightIndent=-0.7*cm)
        #import TT font
        fonts_path = '%s%s%s%s' % (self.app_path_folder, os.sep, 
                                    'fonts', os.sep)
        pdfmetrics.registerFont(TTFont('Open Sans Regular', '%s%s%s%s' % (
                fonts_path,"open-sans", os.sep, "OpenSans-Regular.ttf")))
        pdfmetrics.registerFont(TTFont('Open Sans Bold', '%s%s%s%s' % (
                fonts_path,"open-sans", os.sep, 'OpenSans-Bold.ttf')))
        pdfmetrics.registerFont(TTFont('Open Sans Italic', '%s%s%s%s' % (
                fonts_path,"open-sans", os.sep, 'OpenSans-Italic.ttf')))
        pdfmetrics.registerFont(TTFont('Open Sans Bold Italic', '%s%s%s%s' % (
                fonts_path,"open-sans", os.sep, 'OpenSans-BoldItalic.ttf')))
        registerFontFamily('Open Sans', normal='Open Sans Regular', 
                           bold='Open Sans Bold', 
                           italic='Open Sans Italic', 
                           boldItalic='Open Sans Bold Italic')

        self.doc = SimpleDocTemplate(file_name, pagesize=pagesize,
                        rightMargin=30, leftMargin=30,
                        topMargin=72, bottomMargin=52)
#        Este outro casca co informe historico de records ¿?
#        self.doc = SimpleDocTemplate(file_name, pagesize=pagesize,
#                        rightMargin=1.5*cm,leftMargin=1.5*cm,
#                        topMargin=2.5*cm,bottomMargin=1.8*cm)
        self.story = []
#        for i in range(6):
#            self.insert_title_1(u'Capítulo %s: La formación de las virutas de chocolate.' % i)
#            self.insert_paragraph(u'Un texto muy, muy, muy, pero que muuuuuuuy largo. '*20)
#            self.insert_paragraph(u'Un texto muy, muy, muy, pero que muuuuuuuy largo. '*20)
#            self.story.append(Spacer(1,0.2*cm))
            
    def build_file(self):
#        self.doc.build(self.story, onFirstPage=self.my_first_page, onLaterPages=self.my_later_pages)
        self.doc.build(self.story, onFirstPage=self.my_first_page, onLaterPages=self.my_first_page)

    def insert_title_1(self, text, alignment=TA_JUSTIFY):
        '''
        TA_LEFT, TA_CENTER or TA_CENTRE, TA_RIGHT and TA_JUSTIFY, 
        with values of 0, 1, 2 and 4 respectively
        '''
        if alignment == TA_CENTER:
            title = Paragraph(text, self.titulo1_center)
        elif alignment == TA_LEFT:
            title = Paragraph(text, self.titulo1_left)
        else:
            title = Paragraph(text, self.titulo1)
        self.story.append(title)

    def get_t1_table(self, text):
        t1 = Paragraph(text, self.t1_table)
        return t1

    def insert_title_2(self, text, alignment=TA_LEFT):
        '''
        TA_LEFT, TA_CENTER or TA_CENTRE, TA_RIGHT and TA_JUSTIFY,
        with values of 0, 1, 2 and 4 respectively
        '''
        if alignment == TA_CENTER:
            title = Paragraph(text, self.titulo1_center)
        else:
            title = Paragraph(text, self.titulo1)
        self.story.append(title)

    def insert_page_break(self):
        self.story.append(PageBreak())

    def get_t2_table(self, text):
        t2 = Paragraph(text, self.t2_table)
        return t2

    def insert_spacer(self, width, height):
        spacer = Spacer(width, height)
        self.story.append(spacer)

    def insert_paragraph(self, text, align=None):
        if not align:
            style = self.style_normal
        elif align.upper() == "RIGHT":
            style = self.style_normal_right
        elif align.upper() == "LEFT":
            style = self.style_normal_left
        elif align.upper() == "CENTER":
            style = self.style_normal_center
        elif align.upper() == "JUSTIFY":
            style = self.style_normal_justify

        p = Paragraph(text=text, style=style)
        self.story.append(p)

    def formata_taboa(self, table, col_aligns=[], font_size=9):
        style = ParagraphStyle('normal',
                               fontName='Open Sans Regular',
                               fontSize=font_size,
                               )
        table_formated = []
        for i in table:
            line = []
            for j in i:
                paragraph_formatted = Paragraph(text=j,
                                                style=style)
                line.append(paragraph_formatted)
            table_formated.append(line)
        return table_formated

    def insert_table(self, table, colWidths=None, rowHeights=None, style=None, pagebreak=False, alignment=None):
        """
        aligment = [LEFT|RIGHT|CENTER]
        """
        if table:
#        Style([('FONT',(0,0),(-1,-1), 'Helvetica'), 
##                    ('FONTSIZE',(0,0),(-1,-1), 8),
##                    ('TEXTCOLOR',(0,0),(0,2), colors.blue), 
##                    ('TEXTCOLOR', (1,0), (1,2),colors.green)]
#        self.story.append(Spacer(0, prev_spacer))

            if pagebreak:
                self.story.append(PageBreak())
            t = Table(table, colWidths=colWidths, rowHeights=rowHeights, style=style)
            if alignment:
                t.hAlign = alignment
            self.story.append(t)
        
    def my_first_page(self, canvas, doc):
        
        canvas.setAuthor('FEGAN')
        canvas.setSubject('')
        canvas.setTitle('')
        
        canvas.saveState()
    ##    linhas
        canvas.setStrokeColor('Grey')
        canvas.setLineWidth(0.01)
        canvas.lines(self.lineas)
    ##    Textos
        canvas.setFont('Open Sans Regular',7)
    ##    cabeceira


        canvas.drawInlineImage(self.logo, 1*cm, self.page_height-(2.2*cm), width = 75, height = 47)

##        titulo da cabeceira
#        canvas.setFont('Copperplate Light', 10)
#        canvas.setFillColorRGB(0,0.176,0.447) #azul escuro
#        string_with_total = canvas.stringWidth(self.title)
#        canvas.drawString((self.page_width/2)-(string_with_total/2)-(1.5*cm), 
#                          self.page_height-(1.8*cm), self.title)


#        titulo da cabeceira
        canvas.setFont('Open Sans Regular', 10)
        canvas.setFillColorRGB(0,0.176,0.447)  # azul escuro
        canvas.setFillColorRGB(0.075, 0.137, 0.357)  # azul escuro
        string_with_total = canvas.stringWidth(self.title)
        canvas.drawString((self.page_width/2)-(string_with_total/2), 
                          self.page_height-(1.5*cm), self.title)
#        subtítulo da cabeceira
        canvas.setFont('Open Sans Regular', 8)
        canvas.setFillColorRGB(0, 0, 0) #black
        string_with_total = canvas.stringWidth(self.subtitle)
        canvas.drawString((self.page_width/2)-(string_with_total/2), 
                          self.page_height-(1.9*cm), self.subtitle)
 
# #       cabeceira dereita
# #       todo este hari é para simular a letra versaleta
# #       por iso vai intercalando o tamaño da letra
#         canvas.setFont('Open Sans Bold', 8)
#         canvas.setFillColorRGB(0, 0.176, 0.447)  # azul escuro
#         string_with_total = canvas.stringWidth('Federación Galega De Natación')
#         string_with = canvas.stringWidth('F')
#         canvas.drawRightString(self.page_width-(1.25*cm) - string_with_total + string_with, self.page_height-(0.9*cm), 'F')
# 
#         canvas.setFont('Open Sans Bold', 6)
#         canvas.setFillColorRGB(0, 0.176, 0.447)  # azul escuro
#         string_with += canvas.stringWidth('ederación ')
#         canvas.drawRightString(self.page_width-(1.25*cm) - string_with_total + string_with, self.page_height-(0.9*cm), 'EDERACIÓN ')
# 
#         canvas.setFont('Open Sans Bold', 8)
#         canvas.setFillColorRGB(0, 0.176, 0.447)  # azul escuro
#         string_with += canvas.stringWidth('G')
#         canvas.drawRightString(self.page_width-(1.25*cm) - string_with_total + string_with, self.page_height-(0.9*cm), 'G')
# 
#         canvas.setFont('Open Sans Bold', 6)
#         canvas.setFillColorRGB(0, 0.176, 0.447)  # azul escuro
#         string_with += canvas.stringWidth('alega de ')
#         canvas.drawRightString(self.page_width-(1.25*cm) - string_with_total + string_with, self.page_height-(0.9*cm), 'ALEGA DE ')
# 
#         canvas.setFont('Open Sans Bold', 8)
#         canvas.setFillColorRGB(0, 0.176, 0.447)  # azul escuro
#         string_with += canvas.stringWidth('N')
#         canvas.drawRightString(self.page_width-(1.25*cm) - string_with_total + string_with, self.page_height-(0.9*cm), 'N')
# 
#         canvas.setFont('Open Sans Bold', 6)
#         canvas.setFillColorRGB(0, 0.176, 0.447)  # azul escuro
#         string_with += canvas.stringWidth('atación')
#         canvas.drawRightString(self.page_width-(1.25*cm) - string_with_total + string_with, self.page_height-(0.9*cm), 'ATACIÓN')        
# #       fin da simulación da versaleta

        canvas.setFont('Open Sans Regular', 8)
        canvas.setFillColorRGB(0, 0.176, 0.447)  # azul escuro
        canvas.setFillColorRGB(0.075, 0.137, 0.357)  # azul escuro
        canvas.drawRightString(self.page_width - (1.25 * cm),
                               self.page_height - (0.9 * cm),
                               'Federación Galega de Natación')

        string_with_total = canvas.stringWidth('Federación Galega de Natación')
        canvas.setFont('Open Sans Regular', 6)
        canvas.setFillColorRGB(0, 0, 0)  # black
        string_width = (string_with_total/2) - (canvas.stringWidth('Avenida de Glasgow, 13')/2)
        canvas.drawRightString((self.page_width-(1.25*cm)-string_width), self.page_height-1.3*cm, 'Avenida de Glasgow, 13')
        string_width = (string_with_total/2) - (canvas.stringWidth('CP 15008 - A Coruña')/2)
        canvas.drawRightString((self.page_width-(1.25*cm)-string_width), (self.page_height-1.6*cm), 'CP 15008 - A Coruña')
        string_width = (string_with_total/2) - (canvas.stringWidth('www.fegan.org - info@fegan.org')/2)
        canvas.drawRightString((self.page_width-(1.25*cm)-string_width), self.page_height-1.9*cm, 'www.fegan.org - info@fegan.org')
    ##    pe
        canvas.drawRightString(self.page_width - 1.7 * cm, 1.0 * cm, _('Page %d') % doc.page)
        canvas.drawString(1.7 * cm, 1.0 * cm, _('Timestamp: %s') % datetimes.get_numbers())
        
        canvas.restoreState()
        
    def my_later_pages(self, canvas, doc):
        '''
        xa non o uso, emprego o modelo da primeira páxina para todo.
        '''
        canvas.saveState()
    ##    Lineas
        canvas.setStrokeColor('Grey')
        canvas.setLineWidth(0.01)
        canvas.lines(self.lineas)
    ##    Textos
        canvas.setFont('Open Sans Regular',7)
    ##    Cabecera
        canvas.drawInlineImage(self.logo, 1*cm, self.page_height-(2.2*cm), width = 75, height = 47)
        canvas.setFont('Open Sans Bold', 8)
        canvas.setFillColorRGB(0,0.176,0.447) #azul escuro
        string_with_total = canvas.stringWidth('Federación Galega De Natación')
        canvas.drawRightString(self.page_width-1.7*cm, self.page_height-0.9*cm, 'Federación Galega De Natación')
        canvas.setFont('Open Sans Regular', 6)
        canvas.setFillColorRGB(0,0,0) #black
        string_width = (string_with_total/2) - (canvas.stringWidth('Avenida de Glasgow, 13')/2)
        canvas.drawRightString((self.page_width-1.7*cm-string_width), self.page_height-1.3*cm, 'Avenida de Glasgow, 13')
        string_width = (string_with_total/2) - (canvas.stringWidth('CP 15008 - A Coruóa')/2)
        canvas.drawRightString((self.page_width-1.7*cm-string_width), (self.page_height-1.6*cm), 'CP 15008 - A Coruña')
        string_width = (string_with_total/2) - (canvas.stringWidth('www.fegan.org - info@fegan.org')/2)
        canvas.drawRightString((self.page_width-1.7*cm-string_width), self.page_height-1.9*cm, 'www.fegan.org - info@fegan.org')
    ##    Pie
        canvas.drawRightString(self.page_width - 1.7 * cm, 1.0 * cm, _('page %d') % doc.page)
        
        canvas.restoreState()
                

