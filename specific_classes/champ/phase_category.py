# -*- coding: utf-8 -*- 


from operator import attrgetter
from reportlab.lib.units import cm
from specific_classes.champ.phase_category_results import PhaseCategoryResults
from specific_functions import marks
# from specific_functions import conversion


class PhaseCategory(object):
    
    def __init__(self, phase_categories, phase_category_id, action, category):
        self.phase_categories = phase_categories
        self.config = self.phase_categories.config  
        self.phase_category_id = phase_category_id
        self.action = action
        self.category = category
        self.phase_category_results = PhaseCategoryResults(self)

    @property
    def champ(self):
        return self.phase_categories.champ

    @property
    def phase(self):
        return self.phase_categories.phase

    @property
    def pos(self):
        return self.phase_categories.index(self) + 1

    def delete(self):
        # delete phases_categories_results
        self.phase_category_results.delete_all_items()
        # delete self
        sql = '''
delete phases_categories where phase_category_id=?'''
        values = ((self.phase_category_id, ),)
        self.config.dbs.exec_sql(sql=sql, values=values)

    def save(self):
        """
        Save
        """
        if self.phase_category_id:
            sql = '''
update phases_categories set pos=?, category_id=?, action=? 
where phase_category_id=?'''
            values = ((self.pos, self.category.category_id, self.action,
            self.phase_category_id),)
            self.config.dbs.exec_sql(sql=sql, values=values)
        else:
            sql = '''
INSERT INTO phases_categories (pos, phase_id, category_id, action)
VALUES(?, ?, ?, ?) '''
            values = ((self.pos, self.phase.phase_id, self.category.category_id,
            self.action),)
            self.config.dbs.exec_sql(sql=sql, values=values)
            self.phase_category_id = self.config.dbs.last_row_id
            # self.champ.phases_categories.append(self) non é boa idea facer 
            # isto aquí, mellor facelo antes xa que neste caso a propiedade 
            # pos casca

    def gen_medals_report(self, d):
        # print('Medals for {} {}'.format(self.category.name, self.action))
        phase_category_results = self.phase_category_results
        phase_category_results.load_items_from_dbs()
        # O fallo da opción de abaixo é que pode devolver 4 resultados
        # results = [i for i in phase_category_results if i.pos in (1, 2, 3)]
        # Xa debería ver ordenado ó cargar os resultados
        # results_sorted = sorted(phase_category_results, key=attrgetter('pos')) 
        
        # Fin obtención de datos
        if phase_category_results:
            # toma os 3 primeiros no caso de habelos
            results = phase_category_results
            '''
            Imprime as medallas por categorías
            '''
            style = [
                ('FONT',(0,0),(-1,-1), 'Open Sans Regular'), 
                ('ALIGN',(0,0),(-1,-1), 'CENTER'),
                ('VALIGN', (0,0), (-1,-1), 'BOTTOM'), 
                ('LEFTPADDING', (0,0), (-1,-1), 3),
                ('RIGHTPADDING', (0,0), (-1,-1), 3),
                ]

            def add_phase_category_title(lines):
                style_title = [
                    ('ALIGN',(0,0),(-1,-1), 'LEFT'),
                    ('FONT', (0, 0), (-1, -1), 'Open Sans Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('ALIGN',(1,0),(-1,-1), 'RIGHT'),
                    # ('FONT', (1, 0), (-1, -1), 'Open Sans Regular'),
                    # ('FONTSIZE', (1, 0), (-1, -1), 8),
                    # ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    # ('TOPPADDING', (0,0), (-1,-1), 20), 
                    ]
                style_title = style + style_title
                col_widths = ['80%', '20%']
                d.insert_table(
                    table=lines,
                    colWidths=col_widths,
                    rowHeights=1.0*cm,
                    style=style_title,
                    pagebreak=False,
                    keepWithNext=True)

            def add_line_medal(lines, keep_with_next):
                style_result = [
                    ('FONTSIZE',(0,0),(-1,-1), 8),
                    ('ALIGN',(1,0),(1,-1), 'LEFT'),
                    ('ALIGN',(3,0),(4,-1), 'LEFT'),
                    ('ALIGN',(4,0),(4,-1), 'RIGHT'),  #mark
                    ('ALIGN',(5,0),(5,-1), 'RIGHT'),  #points
                    # ('FONT', (2,0),(2,-1), 'Open Sans Bold'),
                    # ('FONT', (5,0),(5,-1), 'Open Sans Bold'),
                    # ('FONT', (6,0),(6,-1), 'Open Sans Bold'),
                    # ('TOPPADDING', (0,0), (-1,-1), 0),
                    # ('BOTTOMPADDING', (0,0), (-1,-1), 0), 
                    ]
                style_result = style + style_result
                col_widths = ['4%', '10%', '40%', '6%', '20%', '10%', '10%']
                # row_heights = (1.5*cm, 2.5*cm)
                # row_heights = [.5*cm] * len(lines)
                d.insert_table(
                    table=lines,
                    colWidths=col_widths,
                    rowHeights=.5*cm,
                    style=style_result,
                    pagebreak=False,
                    keepWithNext=keep_with_next)

            add_phase_category_title(((self.phase.long_name, self.category.code_gender), ))

            last_result_category_pos = None
            for pos, phase_category_result in enumerate(results):
                result = phase_category_result.result
                # Isto ten que facerse así porque license pode ser cadea valeira

                if phase_category_result.result.issue_id:
                    print('Non é medallista')
                    break
                elif phase_category_result.pos > 3:
                    print('Non é medallista')
                    break
                elif not phase_category_result.result.inscription.classify:
                    print('isto nunca debería pasar')
                    assert "Isto nunca debería pasar."
                else:
                    if last_result_category_pos == phase_category_result.pos:
                        category_pos = ''
                    else:
                        category_pos = phase_category_result.pos
                    ind_rel = phase_category_result.phase.ind_rel
                    line_result = [[
                            str(category_pos), 
                            ind_rel == 'I' and result.person.full_name or result.relay.name, 
                            ind_rel == 'I' and result.person.year[2:] or "", 
                            ind_rel == 'I' and result.person.entity.short_name or result.relay.entity.short_name, 
                            result.mark_time, phase_category_result.points],]
                last_result_category_pos = phase_category_result.pos
                keep_with_next = True
                if (pos + 1) == len(results):
                    keep_with_next = False    
                add_line_medal(lines=line_result, keep_with_next=keep_with_next)
 
            print('fin phase_category_medals')

    def gen_results_report(self, d):
        # print('{} {}'.format(self.category.name, self.action))
        phase_category_results = self.phase_category_results
        phase_category_results.load_items_from_dbs()
        # FIXME: xa debería vir ordenado ó cargar os resultados
        results_sorted = sorted(phase_category_results, key=attrgetter('pos'))
        results_sorted = sorted(results_sorted, key=attrgetter('result.issue_pos'), reverse=False)  
        results_sorted = sorted(results_sorted, key=attrgetter('result.inscription.classify'), reverse=True)  
        # FIXME: mirar se estas dúas liñas de abaixo son necesarias
        del phase_category_results[:]
        phase_category_results.extend(results_sorted)       
        # Fin obtención de datos
        if results_sorted:
            results = results_sorted
            """ imprime os resultados por categorías"""
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

            def add_phase_category(lines):
                style_title = [
                    ('FONTSIZE',(0,0),(-1,-1), 8),
                    ('ALIGN',(0,0),(-1,-1), 'LEFT'),
                    ('FONT', (0, 0), (-1, -1), 'Open Sans Regular'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('ALIGN',(1,0),(-1,-1), 'RIGHT'),
                    ('FONT', (1, 0), (-1, -1), 'Open Sans Regular'),
                    ('FONTSIZE', (1, 0), (-1, -1), 8),
                    # ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), 
                    ]
                style_title = style + style_title
                col_widths = ['100%', ]
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

            def add_member_without_splits(member_lines):
                style_result = [
                    ('FONTSIZE',(0,0),(-1,-1), 7),
                    ('ALIGN',(0,0),(0,-1), 'CENTER'), #separador
                    ('ALIGN',(1,0),(1,-1), 'RIGHT'),
                    ('ALIGN',(2,0),(2,-1), 'RIGHT'), #separador
                    ('ALIGN',(3,0),(3,-1), 'LEFT'),
                    ('ALIGN',(4,0),(4,-1), 'CENTER'),
                    ('TOPPADDING', (0,0), (-1,-1), -1),
                    # ('GRID', [ 0, 0 ], [ -1, -1 ], 0.05, 'grey' ),
                    ]
                style_result = style + style_result
                col_widths = ['8%', '8%', '1%', '25%', '10%']
                # row_heights = (1.5*cm, 2.5*cm)
                # row_heights = [.6*cm] * len(member_line)
                    
                d.insert_table(
                    table=member_lines,
                    colWidths=col_widths,
                    rowHeights=.4*cm,
                    style=style_result,
                    pagebreak=False,
                    alignment='LEFT')
        
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
            # orde = None
            # category = None
            # FIXME: mellorar este código, seguramente sexa mellor pasar na funcion 
            # o obxecto phase_category  e  sacar de aí os resultados e a categoría 
            category = results[0].category
            add_phase_category(((category.code_gender, ), ))
            lines = []

            position = 1
            last_result_category_pos = None
            for phase_category_result in results:
                i = phase_category_result.result
                # Isto ten que facerse así porque license pode ser cadea valeira
                if 'X' not in i.heat.phase.event.code.upper():
                    license_entity_code = i.person.license
                else:
                    license_entity_code = i.relay.entity.entity_code
                if i.issue_id:
                    line_result = [[
                            i.issue_id, 
                            license_entity_code, 
                            'X' not in i.heat.phase.event.code.upper() and i.person.full_name or "", 
                            'X' not in i.heat.phase.event.code.upper() and i.person.year[2:] or "", 
                            'X' not in i.heat.phase.event.code.upper() and i.person.entity.short_name or i.relay.entity.short_name, 
                            '', '0,0'],]
                elif not i.inscription.classify:
                    line_result = [[
                            _('NC'), 
                            license_entity_code, 
                            'X' not in i.heat.phase.event.code.upper() and i.person.full_name or "", 
                            'X' not in i.heat.phase.event.code.upper() and i.person.year[2:] or "", 
                            'X' not in i.heat.phase.event.code.upper() and i.person.entity.short_name or i.relay.entity.short_name, 
                            i.mark_time, '0,0'],]
                else:
                    if last_result_category_pos == phase_category_result.pos:
                        category_pos = ''
                    else:
                        category_pos = phase_category_result.pos
                    line_result = [[
                            str(category_pos), 
                            license_entity_code, 
                            'X' not in i.heat.phase.event.code.upper() and i.person.full_name or i.relay.name, 
                            'X' not in i.heat.phase.event.code.upper() and i.person.year[2:] or "", 
                            'X' not in i.heat.phase.event.code.upper() and i.person.entity.short_name or i.relay.entity.short_name, 
                            i.mark_time, phase_category_result.points],]
                last_result_category_pos = phase_category_result.pos
                add_result(line_result)

                if i.ind_rel == 'R' and i.relay.relay_members.has_members:
                    num_splits = len(i.result_splits)
                    if num_splits == 1:  # Print line members
                        member_lines = []
                        for i in i.relay.relay_members:
                            person = i.person
                            member_lines.append((
                                ' ',  # separador
                                person.license,
                                ' ',  # separador
                                person.full_name, 
                                person.year[2:],
                                ))
                        add_member_without_splits(member_lines=member_lines)
                    else:
                        table_splits = []
                        line_splits = []
                        result_split_pos = 0
                        last_split_hundredth = 0

                        num_members = i.relay.relay_members.num_members
                        splits_by_member = 0
                        if num_splits % num_members == 0:
                            splits_by_member = int(num_splits / num_members)

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
                            
                            if splits_by_member and splits_by_member <= num_split and num_split % splits_by_member == 0:
                                if line_splits:
                                    table_splits.append(line_splits)
                                    line_splits = []
                                    result_split_pos = 0

                                member = i.relay.relay_members[current_member].person
                                member_line = [
                                    member.license, 
                                    member.full_name, 
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
                                print(i.relay.relay_members[current_member].person.name)
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
            print('fin phase_category_results')