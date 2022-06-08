# -*- coding: utf-8 -*- 


from ctypes import alignment
from reportlab.lib.units import cm
from operator import attrgetter
from specific_functions import marks
from specific_functions import conversion
# from specific_functions import normalize


class Phase(object):

    def __init__(self, **kwargs):
        self.phases = kwargs['phases']
        self.config = self.phases.config
        self.phase_id = kwargs['phase_id']
        self.pos = kwargs['pos']
        self.event = kwargs['event']
        self.pool_lanes = kwargs['pool_lanes']
        self.progression = kwargs['progression']
        self.session = kwargs['session']
        # self.heats = []  # non sei para que se usa isto?

    @property
    def champ(self):
        return self.phases.champ

    @property
    def official(self):
        official = True
        for i in self.heats:
            print(i.heat_id)
            if not i.official:
                official = False
                break
        return official

    @property
    def date_time(self):
        return '{} {}'.format(self.session.xdate, self.session.xtime)

    @property
    def file_name(self):
        return '{}_{}'.format(self.event.file_name, self.progression.lower())

    def gen_results_pdf(self, d=False):
        # Obención de datos
        results = []
        results_issues = []

        for i in self.heats:
            i.results.load_items_from_dbs()
            for j in i.results:
                j.result_splits.load_items_from_dbs()
                results.append(j)


        results_sorted = sorted(results, key=attrgetter('category', 'mark_hundredth'))
        results_sorted = sorted(results_sorted, key=attrgetter('issue_pos'), reverse=False)
        del results[:]
        results.extend(results_sorted)

        # Fin obtención de datos
        import os
        from specific_classes.report_base import ReportBase

        xerar = False
        if not d:
            champ = self.phases.champ
            if champ.chrono_type == 'M':
                chrono_text = _('manual')
            else:
                chrono_text = _('electronic')

            long_name = '{}_{}.pdf'.format(
                self.event.file_name, self.progression.lower())
            file_name = os.path.join(
                self.config.app_path_folder,
                long_name)
            subtitle = "{}. Piscina de {} m. Cronometraxe {}.".format(
                champ.venue, champ.pool_length, chrono_text)
            d =  ReportBase(
                    config= self.config,
                    file_name = file_name, 
                    orientation='portrait',
                    title=champ.name,
                    subtitle=subtitle)
            xerar = True

        style = [
            ('FONT',(0,0),(-1,-1), 'Open Sans Regular'), 
            # ('FONTSIZE',(0,0),(-1,-1), 8),
            ('ALIGN',(0,0),(-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'BOTTOM'), 
            # ('TOPPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING', (0,0), (-1,-1), 3),
            ('RIGHTPADDING', (0,0), (-1,-1), 3),
            # ('BOTTOMPADDING', (0,0), (-1,-1), 3), 
            # ('GRID', [ 0, 0 ], [ -1, -1 ], 0.05, 'grey' ),
            ]
        def add_event_title(lines):
            style_title = [
                ('ALIGN',(0,0),(-1,-1), 'LEFT'),
                ('FONT', (0, 0), (-1, -1), 'Open Sans Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                # ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), 
                ]
            style_title = style + style_title
            col_widths = ['100%']
            d.insert_table(
                table=lines,
                colWidths=col_widths,
                rowHeights=.8*cm,
                style=style_title,
                pagebreak=False)

        def add_result(lines):
            style_result = [
                ('FONTSIZE',(0,0),(-1,-1), 8),
                ('ALIGN',(2,0),(2,-1), 'LEFT'),
                ('ALIGN',(5,0),(5,-1), 'RIGHT'),  #mark
                ('ALIGN',(6,0),(6,-1), 'RIGHT'),  #points
                ('FONT', (2,0),(2,-1), 'Open Sans Bold'),
                ('FONT', (5,0),(5,-1), 'Open Sans Bold'),
                ('FONT', (6,0),(6,-1), 'Open Sans Bold'),
                # ('TOPPADDING', (0,0), (-1,-1), 6),
                # ('BOTTOMPADDING', (0,0), (-1,-1), 0),
                # ('VALIGN', (0,0), (-1,-1), 'BOTTOM'), 
                ]
            style_result = style + style_result

            col_widths = ['4%', '10%', '40%', '6%', '20%', '10%', '10%']
            row_heights = (1.5*cm, 2.5*cm)
            row_heights = [.8*cm] * len(lines)
            d.insert_table(
                table=lines,
                colWidths=col_widths,
                rowHeights=.8*cm,
                style=style_result,
                pagebreak=False)

        def add_member(lines):
            style_result = [
                ('FONTSIZE',(0,0),(-1,-1), 8),
                ('ALIGN',(0,0),(0,-1), 'CENTER'),
                ('ALIGN',(1,0),(2,-1), 'LEFT'),
                ('ALIGN',(2,0),(2,-1), 'CENTER'),
                ('FONT', (1,0),(1,-1), 'Open Sans Bold'),
                ]
            style_result = style + style_result

            col_widths = ['10%', '40%', '6%', '20%', '10%', '14%']
            row_heights = (1.5*cm, 2.5*cm)
            row_heights = [.8*cm] * len(lines)
            d.insert_table(
                table=lines,
                colWidths=col_widths,
                rowHeights=.6*cm,
                style=style_result,
                pagebreak=False,
                alignment='LEFT')

        def add_member_with_splits(member_lines):
            style_result = [
                ('FONTSIZE',(0,0),(-1,-1), 7),
                ('ALIGN',(0,0),(0,-1), 'CENTER'),
                ('ALIGN',(1,0),(2,-1), 'LEFT'),
                ('ALIGN',(2,0),(2,-1), 'CENTER'),
                ('TOPPADDING', (0,0), (-1,-1), -1),
                ('ALIGN', (3, 0), (-1, -1), 'RIGHT'),
                # ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                # ('FONT', (1,0),(1,-1), 'Open Sans Bold'),
                ]
            style_result = style + style_result

            col_widths = ['8%', '25%', '10%', '11%', '7%', '7%', '11%', '7%', '7%']
            # row_heights = (1.5*cm, 2.5*cm)
            # row_heights = [.6*cm] * len(member_line)
                
            d.insert_table(
                table=member_lines,
                colWidths=col_widths,
                rowHeights=.4*cm,
                style=style_result,
                pagebreak=False,
                alignment='RIGHT')
            
        def add_result_split(table):
            style_result = [  # o que queremos mudar respecto do estilo base
                ('FONTSIZE', (0, 0), (-1, -1), 7),
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('TOPPADDING', (0,0), (-1,-1), -1),
                # ('BOTTOMPADDING', (0,0), (-1,-1), 0), 
                ]
            style_result = style  + style_result

            col_widths = ['11%', '7%', '7%', '11%', '7%', '7%', '11%', '7%', '7%', '11%', '7%', '7%']

            d.insert_table(
                table=table,
                colWidths=col_widths,
                rowHeights=.4*cm,
                style=style_result,
                pagebreak=False,
                alignment='LEFT')
        # Xera o informe
        orde = None
        category = None
        lines = []

        position = 1
        last_result_mark_hundredth = None
        for i in results:
            if i.heat.phase.event.pos != orde:  #cambio de evento, xera título
                event_title = '{}.- {}'.format(i.heat.phase.event.pos, i.heat.phase.event.name)
                # d.insert_title_1(text=event_title, alignment=0)
                lines.append(['%s.- %s' % (i.heat.phase.event.pos, i.heat.phase.event.name), ])
                add_event_title(lines)
                orde = i.heat.phase.event.pos

            if i.issue_id:
                line_result = [[
                        i.issue_id, 
                        'X' not in i.heat.phase.event.code.upper() and i.person.license or i.relay.name, 
                        'X' not in i.heat.phase.event.code.upper() and i.person.full_name or "", 
                        'X' not in i.heat.phase.event.code.upper() and i.person.year[2:] or "", 
                        'X' not in i.heat.phase.event.code.upper() and i.person.entity.short_name or i.relay.entity.short_name, 
                        '', '0,0'],]
            else:
                if last_result_mark_hundredth == i.mark_hundredth:
                    position_result = ''
                else:
                    position_result = position
                line_result = [[
                        str(position_result), 
                        'X' not in i.heat.phase.event.code.upper() and i.person.license or i.relay.entity.entity_code, 
                        'X' not in i.heat.phase.event.code.upper() and i.person.full_name or i.relay.name, 
                        'X' not in i.heat.phase.event.code.upper() and i.person.year[2:] or "", 
                        'X' not in i.heat.phase.event.code.upper() and i.person.entity.short_name or i.relay.entity.short_name, 
                        i.mark_time, '0,0'],]
            last_result_mark_hundredth = i.mark_hundredth
            add_result(line_result)

            if i.ind_rel == 'R' and i.result_members.has_set_members:
                table_splits = []
                line_splits = []
                result_split_pos = 0
                last_split_hundredth = 0

                num_members = i.result_members.num_members
                num_splits = len(i.result_splits)
                splits_by_member = 0
                if num_splits % num_members == 0:
                    splits_by_member = num_splits / num_members

                current_member = 0
                has_issue = False
                for num_split, j in enumerate(i.result_splits, start=1):                
                    if not i.issue_split or num_split < i.issue_split:
                        line_splits.append('{} m:'.format(j.distance))
                        line_splits.append(j.mark_time)
                        if j.mark_hundredth:
                            split_time = marks.hun2mark(j.mark_hundredth - last_split_hundredth)
                            last_split_hundredth = j.mark_hundredth
                        else:
                            split_time = ''
                        line_splits.append(split_time)
                        result_split_pos +=1
                        if result_split_pos >= 2:
                            table_splits.append(line_splits)
                            line_splits = []
                            result_split_pos = 0
                    else:
                        has_issue = True
                    
                    if num_split > 0 and num_split % splits_by_member == 0:
                        if line_splits:
                            table_splits.append(line_splits)
                            line_splits = []
                            result_split_pos = 0

                        member = i.result_members[current_member].person
                        member_line = [
                            member.license, 
                            member.long_name, 
                            member.year[2:]]

                        if table_splits:
                            member_split_line = table_splits.pop(0)
                            if len(member_split_line) == 3:
                                member_split_line = member_split_line + ['','','']
                            member_lines = [member_line + member_split_line, ]
                        else:
                            member_lines = [member_line + ['','','','','',''], ]
                        
                        while table_splits:
                            member_split_line = table_splits.pop(0)
                            if len(member_split_line) == 3:
                                member_split_line = member_split_line + ['','','']
                            member_lines.append(['','',''] + member_split_line)

                        add_member_with_splits(member_lines=member_lines)
                        table_splits = []
                        result_split_pos = 0
                        print(i.result_members[current_member].person.name)
                        current_member += 1

                if line_splits and not has_issue:
                    table_splits.append(line_splits)
                if table_splits:
                    add_result_split(table=table_splits)    

            elif len(i.result_splits) > 1:
                table_splits = []
                line_splits = []
                result_split_pos = 0
                last_split_hundredth = 0
                for num_split, j in enumerate(i.result_splits):
                    if not i.issue_split or (num_split < i.issue_split and i.ind_rel == 'R'):
                        line_splits.append('{} m:'.format(j.distance))
                        line_splits.append(j.mark_time)
                        if j.mark_hundredth:
                            split_time = marks.hun2mark(j.mark_hundredth - last_split_hundredth)
                            last_split_hundredth = j.mark_hundredth
                        else:
                            split_time = ''
                        line_splits.append(split_time)
                        result_split_pos +=1
                        if result_split_pos >= 4:
                            table_splits.append(line_splits)
                            line_splits = []
                            result_split_pos = 0
                    else:
                        break
                if line_splits:
                    table_splits.append(line_splits)
                add_result_split(table=table_splits)

            position += 1
        if xerar:
            d.build_file()

        print('fin')


#     def gen_results_pdf_todo_nunha_taboa_os_parciais_quedan_desalinhados(self):

#         splits = []
#         no_splits = []
#         results = []
#         results_issues = []

#         for i in self.heats:
#             i.results.load_items_from_dbs()
#             for j in i.results:
#                 j.result_splits.load_items_from_dbs()
#                 if j.issue_id:
#                     results_issues.append(i)
#                 else:
#                     results.append(j)


#         results_sorted = sorted(results, key=attrgetter('category', 'mark_hundredth'))
#         del results[:]
#         results.extend(results_sorted)

#         # Xera o informe
#         orde = None
#         category = None
#         lines = []

        
#         lines_for_span = []
#         lines_for_span_pos = 0
#         tables = [] # cada un dos eventos para facer salto de páxina
#         position = 1
#         for i in results:
#             if i.heat.phase.event.pos != orde:
#                 if lines:
#                     tables.append((lines, lines_for_span))
#                     lines = [] 
#                     lines_for_span = []
#                     lines_for_span_pos = 0
                                        
#                 orde = i.heat.phase.event.pos
#                 lines.append(['',])
#                 lines_for_span_pos += 1 
#                 lines.append(['%s.- %s' % (i.heat.phase.event.pos, i.heat.phase.event.name), ])
#                 lines_for_span.append(('T', lines_for_span_pos)) # T: title event
#                 lines_for_span_pos += 1 
#                 lines.append(['',])
#                 lines_for_span_pos += 1
#                 category = None
                
#             if i.category != category:
#                 category = i.category
#                 lines.append(['',])
#                 lines_for_span_pos += 1 
#                 lines.append([i.category,])
#                 lines_for_span.append(('C', lines_for_span_pos)) # C: category event
#                 lines_for_span_pos += 1 
#                 position = 1
                
#             lines.append([str(position), 
#                     'X' not in i.heat.phase.event.code.upper() and i.person.license or i.relay.name, 
#                     'X' not in i.heat.phase.event.code.upper() and i.person.full_name or "", 
#                     'X' not in i.heat.phase.event.code.upper() and i.person.year or "", 
#                     'X' not in i.heat.phase.event.code.upper() and i.person.entity.short_name or i.relay.entity.short_name, 
#                     i.mark_time, '0,0'])
#             position += 1

#             if 'X' in i.heat.phase.event.code.upper():
#                 lines_for_span.append(('RN', lines_for_span_pos)) # RN: relay name

                
#             lines_for_span_pos += 1 
#             #splits
#             split_margin = 15
#             result_splits = ''
#             result_split_pos = 0
#             member = None
#             left_margin = ' ' * split_margin
#             if len(i.result_splits) > 1:
#                 for j in i.result_splits:
#                     if result_split_pos == 0:
#                         result_splits = left_margin
                            
#                     result_splits += '%-20s %s' % (
#                                         '%s m: %s' % (j.distance, j.mark_time),
#                                         left_margin)
#                     result_split_pos +=1
                
#                     if 'X' in i.heat.phase.event.code.upper():
                        
#                         member = '%s %s (%s)' % (left_margin, j.name, j.year) 
                        
#                     if result_split_pos > 4:
#                         print('comprobar isto!!!!!!')
#                         lines.append([result_splits,])
#                         lines_for_span.append(('P', lines_for_span_pos)) # P: partial event
#                         lines_for_span_pos += 1 
#                         # result_splits = ''  # ' ' * split_margin
#                         result_split_pos = 0
                    
                    
#             if result_splits:
                
#                 if 'X' in i.heat.phase.event.code.upper():
#                     lines.append([member, "", "", result_splits,])
#                     lines_for_span.append(('PR', lines_for_span_pos)) # PR: partial relay event
#                     lines_for_span_pos += 1 
#                     # add others relayers
#                     for k in i.members:
#                         if k.pos != 1:
#                             lines.append(['%s %s (%s)' % (left_margin, 
#                                                     k.name, k.year),])
#                             lines_for_span.append(('M', lines_for_span_pos)) # M: members relay
#                             lines_for_span_pos += 1                     

                    
#                 else:                         
                    
#                     lines.append([result_splits,])
#                     lines_for_span.append(('P', lines_for_span_pos)) # P: partial event
#                     lines_for_span_pos += 1

#         if lines:
#             tables.append((lines, lines_for_span))





#         import os
#         from specific_classes.report_base import ReportBase

#         champ = self.phases.champ
#         if champ.chrono_type == 'M':
#             chrono_text = _('manual')
#         else:
#             chrono_text = _('electronic')

#         long_name = '{}_{}.pdf'.format(
#             self.event.file_name, self.progression.lower())
#         file_name = os.path.join(
#             self.config.app_path_folder,
#             long_name)
#         subtitle = "{}. Piscina de {} m. Cronometraxe {}.".format(
#             champ.venue, champ.pool_length, chrono_text)
#         d =  ReportBase(
#                 config= self.config,
#                 file_name = file_name, 
#                 orientation='portrait',
#                 title=champ.name,
#                 subtitle=subtitle)
        
# #        colspan = 9
#         col_widths = ['4%', '10%', '40%', '6%', '15%', '10%', '10%']
        
# #         table = lines
#         first_event = True
#         for i in tables:
#             if first_event:
#                 page_break = False
#                 first_event = False
#             else:
#                 page_break = True
#             table, lines_for_span = i
#             style = [('FONT',(0,0),(-1,-1), 'Open Sans Regular'), 
#                         ('FONTSIZE',(0,0),(-1,-1), 8),
#                         ('ALIGN',(0,0),(-1,-1), 'CENTER'),
#                         ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), 
#                         ('TOPPADDING', (0,0), (-1,-1), 1),
#                         ('LEFTPADDING', (0,0), (-1,-1), 3),
#                         ('RIGHTPADDING', (0,0), (-1,-1), 3),
#                         ('BOTTOMPADDING', (0,0), (-1,-1), 3), 
#                         ('GRID', [ 0, 0 ], [ -1, -1 ], 0.05, 'grey' ),
#                         ('SPAN', [ 0, 0 ], [ -1, 0 ]),
#     #                    ('SPAN', [ 0, 20 ], [ -1, 20 ]),
#     #                    ('SPAN', [ 0, 40 ], [ -1, 40 ]),
#     #                    ('SPAN', [ 0, 58 ], [ -1, 58 ]),
#                         ('FONTSIZE',(0,0),(-1, 0), 8),
#                         ('BOTTOMPADDING', (0,0), (-1,0), 4),
#                         ]
#             style2 = [('ALIGN',(2,0),(2,-1), 'LEFT'),
#                          # ('ALIGN',(4,0),(4,-1), 'LEFT'),
#                           ('ALIGN',(5,0),(5,-1), 'RIGHT'),  #mark
#                           ('ALIGN',(6,0),(6,-1), 'RIGHT'),  #points
#                         #   ('ALIGN',(7,0),(7,-1), 'LEFT'),
#                         #   ('ALIGN',(8,0),(8,-1), 'LEFT'),
#                         #   ('ALIGN',(9,0),(9,-1), 'RIGHT'),
#                         #   ('ALIGN',(0, 0),(0, 0), 'CENTER')
#                           ]
#             style.extend(style2)
#     ##                    ('TEXTCOLOR',(0,0),(0,2), colors.blue), 
#     ##                    ('TEXTCOLOR', (1,0), (1,2),colors.green)]
            
            
#             for j in lines_for_span:
#                 type_ = j[0]
#                 line_span = j[1]
#                 if type_ == 'PR':  # Person relay
#                     style.extend((
#                                 ('SPAN', (0, line_span), (2, line_span)),
#                                 ('SPAN', (3, line_span), (-1, line_span)),
#                                 ('ALIGN', (0, line_span), (-1, line_span), 'LEFT'),
#                                 ('FONTSIZE', (0, line_span), (-1, line_span), 7),
#                                 ))                    
#                 elif type_ == 'RN':  # Relay name
#                     style.extend((
#                                 ('SPAN', (1, line_span), (2, line_span)),
#                                 ('ALIGN', (0, line_span), (-1, line_span), 'LEFT'),
#                                 ('ALIGN', (9, line_span), (9, line_span), 'RIGHT'),
#                                 # ('FONTSIZE', (0, line_span), (-1, line_span), 4),
#                                 )) 
#                 elif type_ == 'T':  # Titles
#                     style.extend((
#                             ('SPAN', (0, line_span), (-1, line_span)),
#                             ('ALIGN', (0, line_span), (-1, line_span), 'LEFT'),
#                             ('FONT', (0, line_span), (-1, line_span), 'Open Sans Bold'),
#                             ('FONTSIZE', (0, line_span), (-1, line_span), 10),
#                             ))
#                 elif type_ == 'C':  # Category
#                     style.extend((
#                             ('SPAN', (0, line_span), (-1, line_span)),
#                             ('ALIGN', (0, line_span), (-1, line_span), 'LEFT'),
#                             ('FONT', (0, line_span), (-1, line_span), 'Open Sans Bold'),
#                             # ('FONTSIZE', (0, line_span), (-1, line_span), 8),
#                             ))
#                 else:
#                     style.extend((
#                                 ('SPAN', (0, line_span), (-1, line_span)),
#                                 ('ALIGN', (0, line_span), (-1, line_span), 'LEFT'),
#                                 ('FONTSIZE', (0, line_span), (-1, line_span), 7),
#                                 ))

    
#     #            col_widths=['10%', '15%', '15%', '15%', '15%', '15%', '15%']
            
#             d.insert_table(table=table, colWidths=col_widths, 
#                                style=style, pagebreak=page_break)
            
#         # d.insert_paragraph("Isto é unha proba")
#         d.build_file()
#         print('fin')
