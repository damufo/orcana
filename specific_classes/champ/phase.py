# -*- coding: utf-8 -*- 

import os
from specific_classes.report_base import ReportBase

from ctypes import alignment
from reportlab.lib.units import cm
from operator import attrgetter
# from specific_functions import marks
# from specific_functions import conversion
# from specific_functions import normalize
from specific_classes.champ.phase_categories import PhaseCategories
from specific_classes.champ.inscriptions import Inscriptions
from specific_classes.champ.heats import Heats
# from specific_classes.champ.result import Result

class Phase(object):

    def __init__(self, **kwargs):
        self.phases = kwargs['phases']
        self.config = self.phases.config
        self.phase_id = kwargs['phase_id']
        self.event = kwargs['event']
        self.pool_lanes_sort = kwargs['pool_lanes_sort']
        self.progression = kwargs['progression']
        self.session = kwargs['session']
        self.num_clas_next_phase = kwargs['num_clas_next_phase']
        self.parent = kwargs['parent']
        self.phase_categories = PhaseCategories(phase=self)
        self.phase_categories.load_items_from_dbs()
        self.heats = Heats(phase=self)
        self.heats.load_items_from_dbs()
        self.inscriptions = Inscriptions(phase=self)
        self.inscriptions.load_items_from_dbs()
        # FIXME: poñer a liña de abaixo dentro de inscricións
        # print("poñer a liña de abaixo dentro de inscriptions")
        self.inscriptions.load_results_from_dbs()

    @property
    def pos(self):
        return self.phases.index(self) + 1
    
    @property
    def long_name(self):
        return '{}.- {} ({})'.format(self.event.pos, self.event.name, self.progression)

    @property
    def champ(self):
        return self.phases.champ

    @property
    def gender_id(self):
        return self.event.gender_id

    @property
    def ind_rel(self):
        return self.event.ind_rel

    @property
    def pool_lanes(self):
        # tuple or sorted pool number lanes, ex. (3, 4, 2, 5, 1, 6)
        pool_lanes_sort = self.pool_lanes_sort.replace(' ', '')
        pool_lanes = [int(i) for i in pool_lanes_sort.split(',')
                                   if i.isdigit()]
        return tuple(pool_lanes)

    @property
    def pool_lanes_count(self):
        return len(self.pool_lanes)

    @property
    def pool_lane_min(self):
        return min(self.pool_lanes)

    @property
    def pool_lane_max(self):
        return max(self.pool_lanes)

    # @property
    # def results(self):
    #     # return a list of all results for this phase
    #     results = []
    #     for heat in self.heats:
    #         for result in heat.results:
    #             # result.result_splits.load_items_from_dbs()
    #             results.append(result)
    #     return results

    @property
    def results(self):
        # Return phase results sorted by heat and lane
        list_results = []
        for inscription in self.inscriptions:
            if inscription.result:
                list_results.append(inscription.result)
        list_results = sorted(list_results, key=lambda x: x.lane)
        list_results = sorted(list_results, key=lambda x: x.heat.pos)
        return list_results

    @property
    def results_dict(self):
        # Return phase results sorted by heat and lane
        dict_results = {}
        for inscription in self.inscriptions:
            if inscription.result:
                dict_results[inscription.result.result_id] = inscription.result
        return dict_results

    @property
    def official(self):
        official = False
        if self.heats:
            official = True
            for i in self.heats:
                print(i.heat_id)
                if not i.official:
                    official = False
                    break
        return official

    @property
    def date_time(self):
        # FIXME time debería ter sempre un valor válido e correcto de 8 díxitos
        # tamén podería ser un valor de 5 díxitos ó que sempre se lle engadirían os segundos
        if len(self.session.time) == 8:
            time = self.session.time
        elif len(self.session.time) == 5:
            time = "{}:00".format(self.session.time)
        elif len(self.session.time) < 5:
            time = "00:00:00"
        return '{} {}'.format(self.session.date, time)

    @property
    def file_name(self):
        return '{}_{}'.format(self.event.file_name, self.progression.lower())

    @property
    def categories_text(self):
        categories = []
        for i in self.phase_categories:
            categories.append("{}_{} ({})".format(i.category.code, i.category.gender_id, i.action))
        return ', '.join(categories)

#     def load_results_from_dbs(self):
#         # remove results for all phase inscriptions
#         for i in self.inscriptions:
#             i.result = None
    
#         dict_heats = self.heats.dict
#         dict_inscriptions = self.inscriptions.dict
#         # load phase results
#         sql = '''
# select result_id, heat_id, lane, arrival_pos, issue_id,
# issue_split, equated_hundredth, inscription_id
# from results
# where inscription_id in (select inscription_id from inscriptions where phase_id=?)  order by lane; '''
#         values = ((self.phase_id, ), )
#         res = self.config.dbs.exec_sql(sql=sql, values=values)
#         (RESULT_ID, HEAT_ID, LANE, ARRIVAL_POS, 
#         ISSUE_ID, ISSUE_SPLIT, EQUATED_HUNDREDTH, INSCRIPTION_ID
#         ) = range(8)
#         for i in res:
#             inscription = dict_inscriptions[i[INSCRIPTION_ID]]
#             heat = dict_heats[i[HEAT_ID]]
#             result = Result(
#                     inscription=inscription,
#                     result_id=i[RESULT_ID],
#                     heat=heat,
#                     lane=i[LANE],
#                     arrival_pos=i[ARRIVAL_POS],
#                     issue_id=i[ISSUE_ID],
#                     issue_split=i[ISSUE_SPLIT],
#                     equated_hundredth=i[EQUATED_HUNDREDTH],
#                     )
#             inscription.result = result


    def already_exists(self, event_id, progression):
        exists = False
        for i in self.phases:
            if i.event.event_id == event_id and i.progression == progression:
                if i != self:
                    exists = True
                    break
        return exists

    def save(self):
        """
        Save
        """
        if self.phase_id:
            sql = '''
update phases set pos=?, event_id=?, pool_lanes_sort=?, progression=?,
session_id=?, num_clas_next_phase=?, parent_id=?
where phase_id=?'''
            values = ((self.pos, self.event.event_id, self.pool_lanes_sort,
            self.progression, self.session.session_id, self.num_clas_next_phase,
            self.parent and self.parent.phase_id or 0, self.phase_id),)
            self.config.dbs.exec_sql(sql=sql, values=values)
        else:
            sql = '''
INSERT INTO phases (pos, event_id, pool_lanes_sort, progression, session_id,
num_clas_next_phase, parent_id)
VALUES(?, ?, ?, ?, ?, ?, ?) '''
            values = ((self.pos, self.event.event_id, self.pool_lanes_sort,
            self.progression, self.session.session_id,
            self.num_clas_next_phase, self.parent and self.parent.phase_id or 0),)
            self.config.dbs.exec_sql(sql=sql, values=values)
            self.phase_id = self.config.dbs.last_row_id

    def delete(self):
        self.phase_categories.delete_all_items()  
        for heat in self.heats:
            heat.delete()
        sql = ''' delete from phases where phase_id={}'''
        sql = sql.format(self.phase_id)
        self.config.dbs.exec_sql(sql=sql)
        self.phases.remove(self)

    def delete_results_phase_categories(self):
        for phase_category in self.phase_categories:
            phase_category.phase_category_results.delete_all_items()

    def delete_all_heats(self):
        for i in reversed(range(len(self.heats))):
            self.heats[i].delete()
        # for i in self.heats:
        #     i.delete()
        print(len(self.heats))

    def delete_sort_non_se_usa_pode_borrarse(self):
        # Remove current sort
        # clear previous phase results and heats
        # Is not necessary when load, clear all
        # remove phase results_splits, results and heats in dbs
        sql = '''
delete from results_splits where result_id in 
(select result_id from results where inscription_id in 
(select inscription_id from inscriptions where phase_id=?));'''
        values = ((self.phase_id, ), )
        self.config.dbs.exec_sql(sql=sql, values=values)
        sql = '''
delete from results where inscription_id in 
(select inscription_id from inscriptions where phase_id=?)'''
        values = ((self.phase_id, ), )
        self.config.dbs.exec_sql(sql=sql, values=values)
        sql = '''
delete from heats where phase_id=?'''
        values = ((self.phase_id, ), )
        self.config.dbs.exec_sql(sql=sql, values=values)

    def gen_heats(self):
        '''
        Xera as series da fase como TIM (TIM=Timed Finals)
        Xera as series
        Xera as liñas de resultados (aquí é onde vai a serie e a pista)
        '''
        print("Generate phase heats")
        pool_lanes = self.pool_lanes
        pool_lanes_count = self.pool_lanes_count
        
        # Cambiado delete_sort polo de abaixo
        # self.delete_sort()
        self.delete_all_heats()
        # heats and results
        # Get inscriptions, sorted by time asc
        # FIXME get inscriptions from phase
        sql2 = '''
select equated_hundredth, inscription_id
from inscriptions i where phase_id={} and rejected=0 and exchanged=0 order by equated_hundredth; '''
        sql2 = sql2.format(self.phase_id)
        res2 = self.config.dbs.exec_sql(sql=sql2)
        count_inscriptions = len(res2)
        inscriptions = list(res2)
        results = []
        heats = []
        if count_inscriptions:
            tot_heats, first_heat = divmod(count_inscriptions, pool_lanes_count)
            if first_heat != 0:
                tot_heats += 1
            sql_heat = '''
insert into heats (phase_id, pos) values(?, ?)'''
            sql_result = '''
insert into results (heat_id, lane, equated_hundredth, inscription_id)
values(?, ?, ?, ?)'''
#             sql_splits_for_event = '''
# select distance, split_code, official from splits_for_event where 
# event_code=(select event_code from events where event_id=
# (select event_id from phases where phase_id=?))
# order by distance; '''
            sql_result_split = '''
insert into results_splits (result_id, distance, result_split_code, official) 
values( ?, ?, ?, ?)'''
            for heat_pos in range(tot_heats, 0, -1):
                values = ((self.phase_id, heat_pos), )
                self.config.dbs.exec_sql(sql=sql_heat, values=values)
                heat_id = self.config.dbs.last_row_id
                for lane in pool_lanes:
                    inscription = inscriptions.pop(0)
                    EQUATED_HUNDREDTH, INSCRIPTION_ID = range(2) 
                    values = ((
                        heat_id,
                        lane,
                        inscription[EQUATED_HUNDREDTH],
                        inscription[INSCRIPTION_ID],
                        ),)
                    self.config.dbs.exec_sql(sql=sql_result, values=values)
                    result_id = self.config.dbs.last_row_id
                    # Create splits
                    # splits_for_event = self.config.dbs.exec_sql(
                    #     sql=sql_splits_for_event, values=((self.phase_id, ), ))
                    DISTANCE, RESULT_SPLIT_CODE, OFFICIAL = range(3)
                    # if splits_for_event:
                    for event_split in self.event.splits:
                        self.config.dbs.exec_sql(
                            sql=sql_result_split,
                            values=((
                                result_id,
                                event_split[DISTANCE],
                                event_split[RESULT_SPLIT_CODE],
                                event_split[OFFICIAL]), ))
#                     else:
#                         # Isto non debería pasar nunca porque engadín un split 
#                         # predeterminado no caso de que non haxa na base de datos
#                         # isto deste else debería poder borrarse


#                         # add one final split
#                         # get event_code
# #                         sql_event_code = """
# # select event_code from events where event_id =
# #     (select event_id from phases where phase_id=
# #         (select phase_id from inscriptions where inscription_id=?)); """
# #                         res_event_code = self.config.dbs.exec_sql(
# #                             sql=sql_event_code,
# #                             values=((inscription[INSCRIPTION_ID], ), ))
                        
# #                         res_event_code = res_event_code[0][0].upper()
#                         res_event_code = self.event.code.upper()
#                         if 'X' in res_event_code:
#                             members = self.event.num_members
#                             distance_per_member = self.event.distance #res_event_code.split('X')[1][:-1]
#                             distance = int(members) * int(distance_per_member)
#                         else:
#                             distance = self.event.distance
#                         self.config.dbs.exec_sql(
#                                 sql=sql_result_split,
#                                 values=((
#                                     result_id,
#                                     distance,
#                                     res_event_code,
#                                     1), ))
                    if heat_pos == 2 and len(inscriptions) == 3:
                        print("Recoloca para gantir 3")
                        break
                    elif len(inscriptions) == 0:
                        break
        print("load heats and results for this phase")
        self.heats.load_items_from_dbs()
        self.inscriptions.load_results_from_dbs()
        print('End phase gen_heats()')

    def init_report(self, file_name):
        file_path = os.path.join(
            self.config.work_folder_path,
            file_name)
        champ = self.phases.champ
        if champ.params['champ_chrono_type'] == 'M':
            chrono_text = _('manual')
        else:
            chrono_text = _('electronic')
        subtitle = "{}. Piscina de {} m. Cronometraxe {}.".format(
            champ.params['champ_venue'], champ.params['champ_pool_length'], chrono_text)
        d =  ReportBase(
                app_path_folder=self.config.app_path_folder,
                app_version=self.config.app_version,
                file_path=file_path, 
                orientation='portrait',
                title=champ.params['champ_name'],
                subtitle=subtitle)
        return d

    def report_start_list_pdf(self, d=False):
        xerar = False
        if not d:
            file_name = _("start_list_{}_{}.pdf").format(
                self.event.file_name, self.progression.lower())
            d =  self.init_report(file_name=file_name)
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

        def add_phase_title(lines):
            style_title = [
                ('ALIGN',(0,0),(-1,-1), 'LEFT'),
                ('FONT', (0, 0), (-1, -1), 'Open Sans Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('ALIGN',(1,0),(-1,-1), 'RIGHT'),
                ('FONT', (1, 0), (-1, -1), 'Open Sans Regular'),
                ('FONTSIZE', (1, 0), (-1, -1), 8),
                # ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), 
                ]
            style_title = style + style_title
            col_widths = ['80%', '20%']
            d.insert_table(
                table=lines,
                colWidths=col_widths,
                rowHeights=.8*cm,
                style=style_title,
                pagebreak=False,
                keepWithNext=True)

        def add_heat_title(lines):
            style_title = [
                ('ALIGN',(0,0),(-1,-1), 'LEFT'),
                ('FONT', (0, 0), (-1, -1), 'Open Sans Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                # ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), 
                ]
            style_title = style + style_title
            col_widths = ['100%']
            d.insert_table(
                table=lines,
                colWidths=col_widths,
                rowHeights=.8*cm,
                style=style_title,
                pagebreak=False,
                keepWithNext=True)

        def add_result(lines, keep_with_next):
            style_result = [
                ('FONTSIZE',(0,0),(-1,-1), 8),
                ('ALIGN',(2,0),(2,-1), 'LEFT'),
                ('ALIGN',(5,0),(5,-1), 'RIGHT'),  #mark
                ('ALIGN',(6,0),(6,-1), 'RIGHT'),  #points
                ('FONT', (2,0),(2,-1), 'Open Sans Bold'),
                # ('FONT', (5,0),(5,-1), 'Open Sans Bold'),
                # ('FONT', (6,0),(6,-1), 'Open Sans Bold'),
                ]
            style_result = style + style_result
            col_widths = ['4%', '10%', '40%', '6%', '20%', '10%', '10%']
            row_heights = (1.5*cm, 2.5*cm)
            row_heights = [.8*cm] * len(lines)
            d.insert_table(
                table=lines,
                colWidths=col_widths,
                rowHeights=.4*cm,
                style=style_result,
                pagebreak=False,
                keepWithNext=keep_with_next)

        def add_relay_members(lines, keep_with_next):
            style_title = [
                ('ALIGN',(0,0),(-1,-1), 'LEFT'),
                # ('FONT', (0, 0), (-1, -1), 'Open Sans Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 7),
                # ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), 
                ]
            style_title = style + style_title
            col_widths = ['86%']
            d.insert_table(
                table=lines,
                colWidths=col_widths,
                rowHeights=.4*cm,
                style=style_title,
                pagebreak=False,
                alignment='RIGHT',
                keepWithNext=keep_with_next)

        phase = self
        add_phase_title(((phase.long_name, phase.date_time[:-3]), ))
        heats = [heat for heat in self.heats if heat.phase == phase]
        count_heats = len(heats)
        inscriptions =  phase.inscriptions
        for heat in heats:
            heat_title = _('Heat {} of {}').format(heat.pos, count_heats)
            add_heat_title([[heat_title], ])
            # heat.results.load_items_from_dbs()
            # FIXME: poñer isto na clase resultados
            # crear unha lista de inscricións con todas as inscricións
            # e poñela en champ
            for result in heat.results:
                time_start_list = '{} {}{}'.format(
                    result.inscription.mark_time,
                    result.inscription.pool_length,
                    result.inscription.chrono_type)
                equated_time = result.equated_time
                ind_rel = result.ind_rel
                if ind_rel == 'I':
                    license_entity_code = result.person.license
                else:
                    license_entity_code = result.relay.entity.entity_code
                
                if ind_rel == 'I':
                    name = result.person.full_name
                    year = result.person.year[2:]
                    entity = result.person.entity.short_name
                else:  # is a relay
                    if self.champ.params['champ_estament_id'] == 'MASTE':
                        name = '{} {}'.format(result.relay.name, result.relay.category.code)
                        year = result.relay.sum_years
                        entity = result.relay.entity.short_name
                    else:
                        name = result.relay.name
                        year = ''
                        entity = result.relay.entity.short_name
                    
                line_result = [[
                        str(result.lane), 
                        license_entity_code, 
                        name, 
                        year, 
                        entity, 
                        time_start_list, equated_time],]
                # line_result = [[
                #         str(result.lane), 
                #         license_entity_code, 
                #         ind_rel == 'I' and result.person.full_name or result.relay.name, 
                #         ind_rel == 'I' and result.person.year[2:] or "", 
                #         ind_rel == 'I' and result.person.entity.short_name or result.relay.entity.short_name, 
                #         time_start_list, equated_time],]

                members = False
                if ind_rel == 'R':
                    # if not result.relay.relay_members:
                    #     result.relay.relay_members.load_items_from_dbs()
                    members = '; '.join(['{}({})'.format(i.person.full_name, i.person.birth_date[2:4]) for i in result.relay.relay_members])

                if result == heat.results[-1]:
                    if not members:
                        add_result(lines=line_result, keep_with_next=False)
                    else:
                        add_result(lines=line_result, keep_with_next=True)
                        add_relay_members([[members], ], keep_with_next=False)
                else:
                    add_result(lines=line_result, keep_with_next=True)
                    if members:
                        add_relay_members([[members], ], keep_with_next=True)
                
                


        if xerar:
            d.build_file()

        print('fin')

    def calculate_results(self):
        categories_results = {}
        for phase_category in self.phase_categories:
            phase_category_results = phase_category.phase_category_results
            phase_category_results.delete_all_items()
            category_results = []
            # print('{} {}'.format(phase_category.category.name, phase_category.action))
            # get all results for this category
            results = []
            # phase.inscriptions.load_items_from_dbs()
            for result in self.results:
                if phase_category.category in result.categories:
                    # result.result_splits.load_items_from_dbs()
                    results.append(result)
            # end get all results for this category
            """
            Unha vez que temos os resultados da categoría:
            - calculamos a posición
            - asignamos puntuación
            gardanse os elementos en phases_categories_results (result_id, phase_category_id, pos, points)
            """
            results_sorted = sorted(results, key=attrgetter('mark_hundredth', 'heat.pos', 'arrival_pos'))
            results_sorted = sorted(results_sorted, key=attrgetter('issue_pos'), reverse=False)
            results_sorted = sorted(results_sorted, key=attrgetter('inscription.classify'), reverse=True)

            # Start set category position
            current_pos = 0
            current_mark_hundredth = None
            swimoffs = []  # list of results swimoff
            swimoff_all = False
            last_heat_pos = None
            last_arrival_pos = None
            pos_adjust = 0
            for i in results_sorted:
                phase_category_result = phase_category_results.item_blank
                phase_category_result.result = i
                if not i.inscription.classify:  # not score go to next
                    phase_category_result.pos = -1
                    phase_category_results.append(phase_category_result)
                    continue
                if current_mark_hundredth != i.mark_hundredth:
                    current_pos += 1 + pos_adjust
                    pos_adjust = 0
                    last_heat_pos = i.heat.pos
                    last_arrival_pos = i.arrival_pos
                    last_swimoffs = []
                    category_pos = current_pos
                    current_mark_hundredth = i.mark_hundredth
                    swimoffs = []
                    swimoff_all = False
                else:  #swimoff
                    pos_adjust += 1 
                    if swimoff_all:  # empatan todos co mesmo tempo
                         category_pos = current_pos
                    elif i.heat.pos == last_heat_pos:  # empate a tempo na mesma serie
                        # determinar se tamen empata a posición
                        if i.arrival_pos == last_arrival_pos:
                            print("outro empate a tempo e posición na mesma serie")
                            print("isto só pode pasar con crono electrónico")
                            category_pos = current_pos
                        else:  # non empata a posición, crono manual
                            swimoffs.append(phase_category_result)  # empatados con distintas posicións
                            category_pos = current_pos + len(swimoffs)
                            last_arrival_pos = i.arrival_pos
                    else:  # empate a tempo nunha nova serie
                        for swimoff in swimoffs:  # empates previos pasan a empatar
                            swimoff.pos = current_pos
                        category_pos = current_pos
                        swimoff_all = True
                text = "Tempo: {0} | Serie: {1} | Chegada: {2} | Orde categoría: {3}"
                values = (i.mark_time, str(i.heat.pos), str(i.arrival_pos), str(category_pos))
                print(text.format(*values))
                phase_category_result.pos = category_pos
                phase_category_results.append(phase_category_result)
            # End set category position

            # Puntua
            # Resort
            results_sorted = sorted(phase_category_results, key=attrgetter('pos'))
            results_sorted = sorted(results_sorted, key=attrgetter('result.issue_pos'), reverse=False)
            # results_sorted = sorted(results_sorted, key=attrgetter('result.inscription.classify'), reverse=True)
            del phase_category_results[:]
            phase_category_results.extend(results_sorted)

            if phase_category_results and phase_category.action == 'PUNC':  # puntuate this category
                print("aquí o código para puntuar os resultados da categoría")
                if phase_category.category.punctuation:
                    pos_cat = 0
                    pos_points = 1
                    entity_punctuated = {} #entity: count punctuated
                    if self.event.ind_rel == 'R':
                        points = phase_category.category.punctuation.points_rel
                        entity_to_point = phase_category.category.punctuation.entity_to_point_rel
                    else:
                        points = phase_category.category.punctuation.points_ind
                        entity_to_point = phase_category.category.punctuation.entity_to_point_ind
                    if points == "FINA":
                        puntuados_club = {} #codclub: numero de puntuado
                        for i in phase_category_results:
                            if i.result.issue_id:  # se ten incidencia non puntúa
                                break
                            if not i.result.inscription.score:
                                i.points = 0.0
                                continue
                            puntua = False
                            if i.result.entity.entity_id in puntuados_club:
                                # ten en conta cantos puntuan por club
                                if  entity_to_point > puntuados_club[i.result.entity.entity_id]:
                                    puntos = self.results.get_fina_points(idx=x)                         
                                    puntuados_club[i.result.entity.entity_id] = puntuados_club[i.result.entity.entity_id] + 1
                            else:
                                if  entity_to_point > 0:
                                    puntos = self.results.get_fina_points(idx=x)                         
                                    puntuados_club[i.result.entity.entity_id] = 1
                    else:
                        points = points.split(',')
                        points = [i.strip() for i in points]
                        points = [int(i) for i in points if i.isdigit()]
                        puntuados_club = {} #codclub: numero de puntuado
                        posicion_puntos = 0
                        repartir = []
                        last_pos = -1
                        for i in phase_category_results:
                            if i.result.issue_id:  # se ten incidencia non puntúa
                                break
                            if not i.result.inscription.score:
                                i.points = 0.0
                                continue
                            puntua = False
                            # ten en conta cantos puntúan por entidade
                            if i.result.entity.entity_id in puntuados_club:
                                if  entity_to_point > puntuados_club[i.result.entity.entity_id]:
                                    puntuados_club[i.result.entity.entity_id] += 1
                                    puntua = True
                            else:
                                if  entity_to_point:  # > 0
                                    puntuados_club[i.result.entity.entity_id] = 1
                                    puntua = True
                            if puntua:
                                # Mira se quedan puntos a repartir
                                if posicion_puntos < len(points):
                                    i.points = float(points[posicion_puntos])
                                    posicion_puntos += 1
                                else:
                                    i.points = 0.0

                            if last_pos != i.pos:
                                # Reparte os anteriores resultados se é o caso
                                if len(repartir) > 1:
                                    puntos_a_repartir = sum([k.points for k in repartir])
                                    for j in repartir:
                                        j.points = round(float(puntos_a_repartir) / len(repartir), 1)
                                # Iso é para o actual resultado
                                if puntua:
                                    repartir = [i, ]
                                    puntua = False
                                else:
                                    repartir = []
                                last_pos = i.pos
                            if last_pos == i.pos and puntua:
                                repartir.append(i)
                        else:
                            if len(repartir) > 1:
                                puntos_a_repartir = sum([k.points for k in repartir])
                                for j in repartir:
                                    j.points = round(float(puntos_a_repartir) / len(repartir), 2)

            elif results and phase_category.action == 'CLAS':  # clasifica para unha seguite phase
                #TODO: Facer este códito
                print('pendene de facer')
                pass
            elif results and phase_category.action == '':  # nin clasifica nin puntua esta categoría da phase
                print('pendene de facer')
                pass
            
            if phase_category.phase_category_results:
                phase_category.phase_category_results.save_all_items()
                categories_results[phase_category.category.name] = phase_category.phase_category_results

    # def gen_phase_category_results_pdf_movido_a_phase_category(self, d, results):
    #     """ imprime os resultados por categorías"""
    #     style = [
    #         ('FONT',(0,0),(-1,-1), 'Open Sans Regular'), 
    #         # ('FONTSIZE',(0,0),(-1,-1), 8),
    #         ('ALIGN',(0,0),(-1,-1), 'CENTER'),
    #         ('VALIGN', (0,0), (-1,-1), 'BOTTOM'), 
    #         # ('TOPPADDING', (0,0), (-1,-1), 0),
    #         ('LEFTPADDING', (0,0), (-1,-1), 3),
    #         ('RIGHTPADDING', (0,0), (-1,-1), 3),
    #         # ('BOTTOMPADDING', (0,0), (-1,-1), 3), 
    #         # ('GRID', [ 0, 0 ], [ -1, -1 ], 0.05, 'grey' ),
    #         ]

    #     def add_phase_category(lines):
    #         style_title = [
    #             ('FONTSIZE',(0,0),(-1,-1), 8),
    #             ('ALIGN',(0,0),(-1,-1), 'LEFT'),
    #             ('FONT', (0, 0), (-1, -1), 'Open Sans Regular'),
    #             ('FONTSIZE', (0, 0), (-1, -1), 10),
    #             ('ALIGN',(1,0),(-1,-1), 'RIGHT'),
    #             ('FONT', (1, 0), (-1, -1), 'Open Sans Regular'),
    #             ('FONTSIZE', (1, 0), (-1, -1), 8),
    #             # ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), 
    #             ]
    #         style_title = style + style_title
    #         col_widths = ['100%', ]
    #         d.insert_table(
    #             table=lines,
    #             colWidths=col_widths,
    #             rowHeights=.8*cm,
    #             style=style_title,
    #             pagebreak=False)

    #     def add_result(lines):
    #         style_result = [
    #             ('FONTSIZE',(0,0),(-1,-1), 8),
    #             ('ALIGN',(2,0),(2,-1), 'LEFT'),
    #             ('ALIGN',(5,0),(5,-1), 'RIGHT'),  #mark
    #             ('ALIGN',(6,0),(6,-1), 'RIGHT'),  #points
    #             ('FONT', (2,0),(2,-1), 'Open Sans Bold'),
    #             ('FONT', (5,0),(5,-1), 'Open Sans Bold'),
    #             ('FONT', (6,0),(6,-1), 'Open Sans Bold'),
    #             # ('TOPPADDING', (0,0), (-1,-1), 6),
    #             # ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    #             # ('VALIGN', (0,0), (-1,-1), 'BOTTOM'), 
    #             ]
    #         style_result = style + style_result

    #         col_widths = ['4%', '10%', '40%', '6%', '20%', '10%', '10%']
    #         row_heights = (1.5*cm, 2.5*cm)
    #         row_heights = [.8*cm] * len(lines)
    #         d.insert_table(
    #             table=lines,
    #             colWidths=col_widths,
    #             rowHeights=.8*cm,
    #             style=style_result,
    #             pagebreak=False)

    #     def add_member(lines):
    #         style_result = [
    #             ('FONTSIZE',(0,0),(-1,-1), 8),
    #             ('ALIGN',(0,0),(0,-1), 'CENTER'),
    #             ('ALIGN',(1,0),(2,-1), 'LEFT'),
    #             ('ALIGN',(2,0),(2,-1), 'CENTER'),
    #             ('FONT', (1,0),(1,-1), 'Open Sans Bold'),
    #             ]
    #         style_result = style + style_result

    #         col_widths = ['10%', '40%', '6%', '20%', '10%', '14%']
    #         row_heights = (1.5*cm, 2.5*cm)
    #         row_heights = [.8*cm] * len(lines)
    #         d.insert_table(
    #             table=lines,
    #             colWidths=col_widths,
    #             rowHeights=.6*cm,
    #             style=style_result,
    #             pagebreak=False,
    #             alignment='LEFT')

    #     def add_member_with_splits(member_lines):
    #         style_result = [
    #             ('FONTSIZE',(0,0),(-1,-1), 7),
    #             ('ALIGN',(0,0),(0,-1), 'CENTER'),
    #             ('ALIGN',(1,0),(2,-1), 'LEFT'),
    #             ('ALIGN',(2,0),(2,-1), 'CENTER'),
    #             ('TOPPADDING', (0,0), (-1,-1), -1),
    #             ('ALIGN', (3, 0), (-1, -1), 'RIGHT'),
    #             # ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    #             # ('FONT', (1,0),(1,-1), 'Open Sans Bold'),
    #             ]
    #         style_result = style + style_result

    #         col_widths = ['8%', '25%', '10%', '11%', '7%', '7%', '11%', '7%', '7%']
    #         # row_heights = (1.5*cm, 2.5*cm)
    #         # row_heights = [.6*cm] * len(member_line)
                
    #         d.insert_table(
    #             table=member_lines,
    #             colWidths=col_widths,
    #             rowHeights=.4*cm,
    #             style=style_result,
    #             pagebreak=False,
    #             alignment='RIGHT')

    #     def add_member_without_splits(member_lines):
    #         style_result = [
    #             ('FONTSIZE',(0,0),(-1,-1), 7),
    #             ('ALIGN',(0,0),(0,-1), 'CENTER'), #separador
    #             ('ALIGN',(1,0),(1,-1), 'RIGHT'),
    #             ('ALIGN',(2,0),(2,-1), 'RIGHT'), #separador
    #             ('ALIGN',(3,0),(3,-1), 'LEFT'),
    #             ('ALIGN',(4,0),(4,-1), 'CENTER'),
    #             ('TOPPADDING', (0,0), (-1,-1), -1),
    #             # ('GRID', [ 0, 0 ], [ -1, -1 ], 0.05, 'grey' ),
    #             ]
    #         style_result = style + style_result
    #         col_widths = ['8%', '8%', '1%', '25%', '10%']
    #         # row_heights = (1.5*cm, 2.5*cm)
    #         # row_heights = [.6*cm] * len(member_line)
                
    #         d.insert_table(
    #             table=member_lines,
    #             colWidths=col_widths,
    #             rowHeights=.4*cm,
    #             style=style_result,
    #             pagebreak=False,
    #             alignment='LEFT')
    
    #     def add_result_split(table):
    #         style_result = [  # o que queremos mudar respecto do estilo base
    #             ('FONTSIZE', (0, 0), (-1, -1), 7),
    #             ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
    #             ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    #             ('TOPPADDING', (0,0), (-1,-1), -1),
    #             # ('BOTTOMPADDING', (0,0), (-1,-1), 0), 
    #             ]
    #         style_result = style  + style_result

    #         col_widths = ['11%', '7%', '7%', '11%', '7%', '7%', '11%', '7%', '7%', '11%', '7%', '7%']

    #         d.insert_table(
    #             table=table,
    #             colWidths=col_widths,
    #             rowHeights=.4*cm,
    #             style=style_result,
    #             pagebreak=False,
    #             alignment='LEFT')
    #     # Xera o informe
    #     # orde = None
    #     # category = None
    #     # FIXME: mellorar este código, seguramente sexa mellor pasar na funcion 
    #     # o obxecto phase_category  e  sacar de aí os resultados e a categoría 
    #     category = results[0].category
    #     add_phase_category(((category.code_gender, ), ))
    #     lines = []

    #     position = 1
    #     last_result_category_pos = None
    #     for phase_category_result in results:
    #         i = phase_category_result.result

    #         if i.issue_id:
    #             line_result = [[
    #                     i.issue_id, 
    #                     'X' not in i.heat.phase.event.code.upper() and i.person.license or i.relay.name, 
    #                     'X' not in i.heat.phase.event.code.upper() and i.person.full_name or "", 
    #                     'X' not in i.heat.phase.event.code.upper() and i.person.year[2:] or "", 
    #                     'X' not in i.heat.phase.event.code.upper() and i.person.entity.short_name or i.relay.entity.short_name, 
    #                     '', '0,0'],]
    #         elif not i.inscription.classify:
    #             line_result = [[
    #                     _('NC'), 
    #                     'X' not in i.heat.phase.event.code.upper() and i.person.license or i.relay.name, 
    #                     'X' not in i.heat.phase.event.code.upper() and i.person.full_name or "", 
    #                     'X' not in i.heat.phase.event.code.upper() and i.person.year[2:] or "", 
    #                     'X' not in i.heat.phase.event.code.upper() and i.person.entity.short_name or i.relay.entity.short_name, 
    #                     '', '0,0'],]

    #         else:
    #             if last_result_category_pos == phase_category_result.pos:
    #                 category_pos = ''
    #             else:
    #                 category_pos = phase_category_result.pos
    #             line_result = [[
    #                     str(category_pos), 
    #                     'X' not in i.heat.phase.event.code.upper() and i.person.license or i.relay.entity.entity_code, 
    #                     'X' not in i.heat.phase.event.code.upper() and i.person.full_name or i.relay.name, 
    #                     'X' not in i.heat.phase.event.code.upper() and i.person.year[2:] or "", 
    #                     'X' not in i.heat.phase.event.code.upper() and i.person.entity.short_name or i.relay.entity.short_name, 
    #                     i.mark_time, phase_category_result.points],]
    #         last_result_category_pos = phase_category_result.pos
    #         add_result(line_result)

    #         if i.ind_rel == 'R' and i.relay.relay_members.has_members:
    #             num_splits = len(i.result_splits)
    #             if num_splits == 1:  # Print line members
    #                 member_lines = []
    #                 for i in i.relay.relay_members:
    #                     person = i.person
    #                     member_lines.append((
    #                         ' ',  # separador
    #                         person.license,
    #                         ' ',  # separador
    #                         person.full_name, 
    #                         person.year[2:],
    #                         ))
    #                 add_member_without_splits(member_lines=member_lines)
    #             else:
    #                 table_splits = []
    #                 line_splits = []
    #                 result_split_pos = 0
    #                 last_split_hundredth = 0

    #                 num_members = i.relay.relay_members.num_members
    #                 splits_by_member = 0
    #                 if num_splits % num_members == 0:
    #                     splits_by_member = int(num_splits / num_members)

    #                 current_member = 0
    #                 has_issue = False
    #                 for num_split, j in enumerate(i.result_splits, start=1):                
    #                     if not i.issue_split or num_split < i.issue_split:
    #                         line_splits.append('{} m:'.format(j.distance))
    #                         line_splits.append(j.mark_time)
    #                         if j.mark_hundredth:
    #                             split_time = marks.hun2mark(j.mark_hundredth - last_split_hundredth)
    #                             last_split_hundredth = j.mark_hundredth
    #                         else:
    #                             split_time = ''
    #                         line_splits.append(split_time)
    #                         result_split_pos +=1
    #                         if result_split_pos >= 2:
    #                             table_splits.append(line_splits)
    #                             line_splits = []
    #                             result_split_pos = 0
    #                     else:
    #                         has_issue = True
                        
    #                     if splits_by_member and splits_by_member <= num_split and num_split % splits_by_member == 0:
    #                         if line_splits:
    #                             table_splits.append(line_splits)
    #                             line_splits = []
    #                             result_split_pos = 0

    #                         member = i.relay.relay_members[current_member].person
    #                         member_line = [
    #                             member.license, 
    #                             member.full_name, 
    #                             member.year[2:]]

    #                         if table_splits:
    #                             member_split_line = table_splits.pop(0)
    #                             if len(member_split_line) == 3:
    #                                 member_split_line = member_split_line + ['','','']
    #                             member_lines = [member_line + member_split_line, ]
    #                         else:
    #                             member_lines = [member_line + ['','','','','',''], ]
                            
    #                         while table_splits:
    #                             member_split_line = table_splits.pop(0)
    #                             if len(member_split_line) == 3:
    #                                 member_split_line = member_split_line + ['','','']
    #                             member_lines.append(['','',''] + member_split_line)

    #                         add_member_with_splits(member_lines=member_lines)
    #                         table_splits = []
    #                         result_split_pos = 0
    #                         print(i.relay.relay_members[current_member].person.name)
    #                         current_member += 1

    #                 if line_splits and not has_issue:
    #                     table_splits.append(line_splits)
    #                 if table_splits:
    #                     add_result_split(table=table_splits)    

    #         elif len(i.result_splits) > 1:
    #             table_splits = []
    #             line_splits = []
    #             result_split_pos = 0
    #             last_split_hundredth = 0
    #             for num_split, j in enumerate(i.result_splits):
    #                 if not i.issue_split or (num_split < i.issue_split and i.ind_rel == 'R'):
    #                     line_splits.append('{} m:'.format(j.distance))
    #                     line_splits.append(j.mark_time)
    #                     if j.mark_hundredth:
    #                         split_time = marks.hun2mark(j.mark_hundredth - last_split_hundredth)
    #                         last_split_hundredth = j.mark_hundredth
    #                     else:
    #                         split_time = ''
    #                     line_splits.append(split_time)
    #                     result_split_pos +=1
    #                     if result_split_pos >= 4:
    #                         table_splits.append(line_splits)
    #                         line_splits = []
    #                         result_split_pos = 0
    #                 else:
    #                     break
    #             if line_splits:
    #                 table_splits.append(line_splits)
    #             add_result_split(table=table_splits)

    #         position += 1
    #     print('fin phase_category_results')


    def gen_results_report(self, d=False):

        xerar = False
        if not d:  # Crea o informe se non existise
            champ = self.phases.champ
            file_name = '{}_{}.pdf'.format(
                self.event.file_name, self.progression.lower())
            d = self.init_report(file_name=file_name)
            xerar = True

        # FIXME: Mellorar este código, quitar función add_phase_title()
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
        def add_phase_title(lines):
            style_title = [
                ('ALIGN',(0,0),(-1,-1), 'LEFT'),
                ('FONT', (0, 0), (-1, -1), 'Open Sans Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('ALIGN',(1,0),(-1,-1), 'RIGHT'),
                ('FONT', (1, 0), (-1, -1), 'Open Sans Regular'),
                ('FONTSIZE', (1, 0), (-1, -1), 8),
                # ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), 
                ]
            style_title = style + style_title
            col_widths = ['80%', '20%']
            d.insert_table(
                table=lines,
                colWidths=col_widths,
                rowHeights=.8*cm,
                style=style_title,
                pagebreak=False)

        add_phase_title(((self.long_name, self.date_time[:-3]), ))

        for phase_category in self.phase_categories:
            phase_category.gen_results_report(d=d)

        if xerar:
            d.build_file()

        print('fin')

    def gen_medals_report(self, d=False):

        xerar = False
        if not d:  # Crea o informe se non existise
            file_name = '{}_{}_medals_by_category.pdf'.format(
                self.event.file_name, self.progression.lower())
            d = self.champ.init_report(file_name=file_name)
            xerar = True

        for phase_category in self.phase_categories:
            phase_category.gen_medals_report(d=d)

        if xerar:
            d.build_file()

        print('fin')

#     def gen_results_report_todo_nunha_taboa_os_parciais_quedan_desalinhados(self):

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
#         if champ.params['champ_chrono_type'] == 'M':
#             chrono_text = _('manual')
#         else:
#             chrono_text = _('electronic')

#         long_name = '{}_{}.pdf'.format(
#             self.event.file_name, self.progression.lower())
#         file_name = os.path.join(
#             self.config.app_path_folder,
#             long_name)
#         subtitle = "{}. Piscina de {} m. Cronometraxe {}.".format(
#             champ.params['champ_venue'], champ.params['champ_pool_length'], chrono_text)
#         d =  ReportBase(
#                 config= self.config,
#                 file_name = file_name, 
#                 orientation='portrait',
#                 title=champ.params['champ_name'],
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
