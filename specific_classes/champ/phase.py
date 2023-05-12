# -*- coding: utf-8 -*- 

import os
from specific_classes.report_base import ReportBase

from ctypes import alignment
from reportlab.lib.units import cm
from operator import attrgetter
from specific_functions import marks
from specific_functions import conversion
# from specific_functions import normalize
from specific_classes.champ.phase_categories import PhaseCategories

class Phase(object):

    def __init__(self, **kwargs):
        self.phases = kwargs['phases']
        self.config = self.phases.config
        self.phase_id = kwargs['phase_id']
        self.event = kwargs['event']
        self.pool_lanes = kwargs['pool_lanes']
        self.progression = kwargs['progression']
        self.session = kwargs['session']
        # self.heats = []  # non sei para que se usa isto?
        self.phase_categories = PhaseCategories(phase=self)

    @property
    def pos(self):
        return self.phases.index(self) + 1

    @property
    def champ(self):
        return self.phases.champ

    @property
    def heats(self):
        heats = []
        for heat in self.champ.heats:
            if heat.phase == self:
                heats.append(heat)
        return heats

    @property
    def results(self):
        # get all results for this phase
        results = []
        for heat in self.heats:
            heat.results.load_items_from_dbs()
            for result in heat.results:
                result.result_splits.load_items_from_dbs()
                results.append(result)
        return results

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
        # FIXME xtime debería ter sempre un valor válido e correcto de 8 díxitos
        # tamén podería ser un valor de 5 díxitos ó que sempre se lle engadirían os segundos
        if len(self.session.xtime) == 8:
            xtime = self.session.xtime
        elif len(self.session.xtime) == 5:
            xtime = "{}:00".format(self.session.xtime)
        elif len(self.session.xtime) < 5:
            xtime = "00:00:00"
        return '{} {}'.format(self.session.xdate, xtime)

    @property
    def file_name(self):
        return '{}_{}'.format(self.event.file_name, self.progression.lower())

    @property
    def categories_names(self):
        categories = []
        for i in self.phase_categories:
            categories.append("{} ({})".format(i.category.name, i.action))

        return ', '.join(categories)

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
update phases set pos=?, event_id=?, pool_lanes=?, progression=?, session_id=? 
where phase_id=?'''
            values = ((self.pos, self.event.event_id, self.pool_lanes,
            self.progression, self.session.session_id, self.phase_id),)
            self.config.dbs.exec_sql(sql=sql, values=values)
        else:
            sql = '''
INSERT INTO phases (pos, event_id, pool_lanes, progression, session_id)
VALUES(?, ?, ?, ?, ?) '''
            values = ((self.pos, self.event.event_id, self.pool_lanes,
            self.progression, self.session.session_id),)
            self.config.dbs.exec_sql(sql=sql, values=values)
            self.phase_id = self.config.dbs.last_row_id

    def delete(self):
        self.phase_categories.delete_all_items()  # con isto bórranse as phases_categories e results_phases_categories
        # ver reflesion 2022-09-22 en changelog
        for heat in self.heats:  # as heats realmente non son das fases senón que están todas as do campionato baixo heats
            heat.delete()  # borra os results que teña e a propia serie
            heat.heats.remove(heat)  # retira a serie da lista de series
        sql = ''' delete from phases where phase_id={}'''
        sql = sql.format(self.phase_id)
        self.config.dbs.exec_sql(sql=sql)

    def delete_results_phase_categories(self):
        for phase_category in self.phase_categories:
            phase_category.results_phase_category.delete_all_items()

    def delete_all_heats(self):
        for i in self.heats:
            i.delete()

    def gen_heats(self):
        '''
        Xera as series da fase como TIM
        Xera as series
        Xera as liñas de resultados (aquí é onde vai a serie e a pista)
        '''
        print("Generate sphase eries")
        
        # clear previous phase heats
        self.delete_all_heats()

        if self.pool_lanes == 5:
            lanes_sort = (3, 4, 2, 5, 1)
        if self.pool_lanes == 6:
            lanes_sort = (3, 4, 2, 5, 1, 6)
        elif self.pool_lanes == 8:
            lanes_sort = (4, 5, 3, 6, 2, 7, 1, 8)
        # heats and results
        # Get inscriptions, sorted by time asc
        sql2 = '''
select (select person_id from persons p where p.person_id=i.person_id) person_id,
(select relay_id from relays r where r.relay_id=i.relay_id) relay_id,
equated_hundredth, inscription_id
from inscriptions i where event_id={} order by equated_hundredth; '''
        sql2 = sql2.format(self.event.event_id)
        res2 = self.config.dbs.exec_sql(sql=sql2)
        count_inscriptions = len(res2)
        inscriptions = list(res2)
        results = []
        heats = []
        if count_inscriptions:
            tot_heats, first_heat = divmod(count_inscriptions, self.pool_lanes)
            if first_heat != 0:
                tot_heats += 1
            sql_heat = '''
insert into heats (phase_id, pos) values(?, ?)'''
            sql_result = '''
insert into results (heat_id, lane, person_id, relay_id, equated_hundredth, inscription_id)
values(?, ?, ?, ?, ?,?)'''
            sql_splits_for_event = '''
select distance, split_code, official from splits_for_event where 
event_code=(select event_code from events where event_id=
(select event_id from phases where phase_id=?))
order by distance; '''
            sql_result_split = '''
insert into results_splits (result_id, distance, result_split_code, official) 
values( ?, ?, ?, ?)'''
            for heat_pos in range(tot_heats, 0, -1):
                values = ((self.phase_id, heat_pos), )
                self.config.dbs.exec_sql(sql=sql_heat, values=values)
                heat_id = self.config.dbs.last_row_id
                for lane in lanes_sort:
                    inscription = inscriptions.pop(0)
                    PERSON_ID, RELAY_ID, EQUATED_HUNDREDTH, INSCRIPTION_ID = range(4) 
                    values = ((
                        heat_id,
                        lane,
                        inscription[PERSON_ID] or 0,
                        inscription[RELAY_ID] or 0,
                        inscription[EQUATED_HUNDREDTH],
                        inscription[INSCRIPTION_ID],
                        ),)
                    self.config.dbs.exec_sql(sql=sql_result, values=values)
                    result_id = self.config.dbs.last_row_id
                    # Create splits
                    splits_for_event = self.config.dbs.exec_sql(
                        sql=sql_splits_for_event, values=((self.phase_id, ), ))
                    DISTANCE, RESULT_SPLIT_CODE, OFFICIAL = range(3)
                    if splits_for_event:
                        for event_split in splits_for_event:
                            self.config.dbs.exec_sql(
                                sql=sql_result_split,
                                values=((
                                    result_id,
                                    event_split[DISTANCE],
                                    event_split[RESULT_SPLIT_CODE],
                                    event_split[OFFICIAL]), ))
                    else:
                        # add one final split
                        # get event_code
                        sql_event_code = """
select event_code from events where event_id =
(select event_id from inscriptions where inscription_id=?); """
                        res_event_code = self.config.dbs.exec_sql(
                            sql=sql_event_code,
                            values=((inscription[INSCRIPTION_ID], ), ))
                        res_event_code = res_event_code[0][0].upper()
                        if 'X' in res_event_code:
                            members = int(res_event_code.split('X')[0])
                            distance_per_member = res_event_code.split('X')[1][:-1]
                            distance = int(members) * int(distance_per_member)
                        else:
                            distance = res_event_code[:len(res_event_code)-1]
                        self.config.dbs.exec_sql(
                                sql=sql_result_split,
                                values=((
                                    result_id,
                                    distance,
                                    res_event_code,
                                    1), ))
                    if heat_pos == 2 and len(inscriptions) == 3:
                        print("Recoloca para gantir 3")
                        break
                    elif len(inscriptions) == 0:
                        break
        # self.phases.load_items_from_dbs()
        self.champ.heats.load_items_from_dbs()
        print("load heats for this phase")
        print('Fin')

    def init_report(self, file_name):
        file_path = os.path.join(
            self.config.work_folder_path,
            file_name)
        champ = self.phases.champ
        if champ.chrono_type == 'M':
            chrono_text = _('manual')
        else:
            chrono_text = _('electronic')
        subtitle = "{}. Piscina de {} m. Cronometraxe {}.".format(
            champ.venue, champ.pool_length, chrono_text)
        d =  ReportBase(
                app_path_folder=self.config.app_path_folder,
                app_version=self.config.app_version,
                file_path=file_path, 
                orientation='portrait',
                title=champ.name,
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
                pagebreak=False)

        def add_result(lines):
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
                pagebreak=False)

        def add_relay_members(lines):
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
                alignment='RIGHT')

        phase = self
        phase_title = '{}.- {} ({})'.format(phase.event.pos, phase.event.name, phase.progression)
        add_phase_title([[phase_title], ])
        heats = [heat for heat in self.heats if heat.phase == phase]
        count_heats = len(heats)
        inscriptions =  phase.event.inscriptions
        inscriptions.load_items_from_dbs()
        for heat in heats:
            heat_title = _('Heat {} of {}').format(heat.pos, count_heats)
            add_heat_title([[heat_title], ])
            heat.results.load_items_from_dbs()
            # FIXME: poñer isto na clase resultados
            # crear unha lista de inscricións con todas as inscricións
            # e poñela en champ
            for result in heat.results:
                if result.inscription:
                    time_sart_list = '{} {}{}'.format(
                        result.inscription.mark_time,
                        result.inscription.pool_length,
                        result.inscription.chrono_type)
                    equated_time = result.equated_time
                else:
                    time_sart_list = ''
                    equated_time = result.equated_time

                line_result = [[
                        str(result.lane), 
                        'X' not in result.event.code.upper() and result.person.license or result.relay.entity.entity_code, 
                        'X' not in result.event.code.upper() and result.person.full_name or result.relay.name, 
                        'X' not in result.event.code.upper() and result.person.year[2:] or "", 
                        'X' not in result.event.code.upper() and result.person.entity.short_name or result.relay.entity.short_name, 
                        time_sart_list, equated_time],]
                add_result(line_result)
                if result.ind_rel == 'R':
                    if not result.result_members:
                        result.result_members.load_items_from_dbs()
                    members = '; '.join([i.person.full_name for i in result.result_members])
                    print(members)
                    if members:
                        add_relay_members([[members], ])


        if xerar:
            d.build_file()

        print('fin')

    def calculate_results(self):
        categories_results = {}
        for phase_category in self.phase_categories:
            category_results = []
            print('{} {}'.format(phase_category.category.name, phase_category.action))
            # get all results for this category
            results = []
            for heat in self.heats:
                heat.results.load_items_from_dbs()
                for result in heat.results:
                    if phase_category.category.category_id in result.categories:
                        result.result_splits.load_items_from_dbs()
                        results.append(result)
            print("Aquí a ordenación por categoría non debería ter sentido")
            print("ordenar por marca e por serie, se na mesma serie e crono manual, non fai reparto")
            print("se en distintas series repartir puntos, pensar no caso de que dous na mesma serie empaten e non se reparten puntos pero os dous teñen que repartir co empate da seguinte serie")
            """
            O reparto de puntos funciona do seguinte xeito
            Empatan dous a tempo pero como é manual un é primeiroe outro é segundo
            Na seguinte serie empatan outros dous co mesmo tempo

            Como e o reparto?
                os primeiros como están en series distintas reparten tempo por igualar posición
                Os segundos (que serían o posto 3) reparten puntos entre eles.
            """
            results_sorted = sorted(results, key=attrgetter(
                'category', 'mark_hundredth', 'heat.pos', 'arrival_pos'))
            results_sorted = sorted(results_sorted, key=attrgetter('issue_pos'), reverse=False)
            del results[:]
            results.extend(results_sorted)
            # end get all results for this category
            if results and phase_category.action == 'PUNC':  # puntuate this category
                print("aquí o código para puntuar os resultados da categoría")

                # phase_category.results_phase_category.delete_all_items()

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
                    for i in results:
                        result_phase_category = phase_category.results_phase_category.item_blank
                        result_phase_category.result = i
                        if i.entity.entity_id in puntuados_club:
                            # ten en conta cantos puntuan por club
                            if  entity_to_point > puntuados_club[i.entity.entity_id]:
                                puntos = self.results.get_fina_points(idx=x)                         
                                puntuados_club[i.entity.entity_id] = puntuados_club[i.entity.entity_id] + 1
                        else:
                            if  entity_to_point > 0:
                                puntos = self.results.get_fina_points(idx=x)                         
                                puntuados_club[i.entity.entity_id] = 1
                else:
                    points = points.split(',')
                    points = [int(i) for i in points if i.isdigit()]

                    # orde = -1  # event pos?
                    tie_pos = 0  # is for ties (ties=empates)
                    empatados = []
                    heats_empatados = []
                    last_mark = -1
                    last_heat = -1
                    last_order = -1
                    last_cat = -1
                    tot_puntos = 0
                    prev_category_id = None
                    posicion = 0
                    posicion_puntos = 0
                    puntuados_club = {} #codclub: numero de puntuado
                    
                    # o primeiro é calcular a posición
                    results_pos = []
                    empatados = []
                    pendentes = []

                    for i in results:
                        result_phase_category = phase_category.results_phase_category.item_blank
                        result_phase_category.result = i
                        engadir = True
                        
                        if i.issue_id:
                            result_phase_category.pos = i.issue_id
                            phase_category.results_phase_category.append(result_phase_category)
                        elif last_mark == i.mark_time and i.heat.heat_id not in heats_empatados:
                            # mira se o empate é noutra serie, no caso de ser 
                            # outra serie implica que empata a posición
                            # sábese que está en peor posición pola ordenación
                            empatados.append(result_phase_category)
                        elif last_mark == i.mark_time and i.heat.heat_id in heats_empatados:
                            # empate na mesma serie en peor posición, pasa ó final
                            # se houbese aquí outro empate non funcionaría
                            pendentes.append(result_phase_category)
                        else:
                            # engade os empatados coa correspondente posición
                            for empatado in empatados:
                                empatado.pos = posicion
                                phase_category.results_phase_category.append(empatado)
                            empatados = []
                            heats_empatados = []
                            if pendentes:                                
                                # engade os pendentes coa correspondente posición
                                posicion = posicion + 1
                                for pendente in pendentes:
                                    pendente.pos = posicion
                                    phase_category.results_phase_category.append(pendente)
                                pendentes = []
                            posicion = posicion + 1
                            result_phase_category.pos = posicion
                            phase_category.results_phase_category.append(result_phase_category)
                        last_mark = result_phase_category.result.mark_time
                        if i.heat.heat_id not in heats_empatados:
                            heats_empatados.append(i.heat.heat_id)
                    
                    # agora en base á posición establece a puntuación
                    
                    posicion_puntos = 0
                    repartir = []
                    last_pos = -1
                    for i in phase_category.results_phase_category:
                        puntos = 0
                        # ten en conta cantos puntúan por entidade
                        puntua = False
                        if i.result.entity.entity_id in puntuados_club:
                            if  entity_to_point > puntuados_club[i.result.entity.entity_id]:
                                puntuados_club[i.result.entity.entity_id] = puntuados_club[i.result.entity.entity_id] + 1
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
                        if last_pos == i.pos and puntua:
                            repartir.append(i)
                        elif last_pos != i.pos:
                            if len(repartir) > 1:
                                puntos_a_repartir = sum([i.points for i in repartir])
                                for i in repartir:
                                    i.points = round(float(puntos_a_repartir) / len(repartir), 1)
                            repartir = [i, ]
                        last_pos = i.pos
                    else:
                        if len(repartir) > 1:
                            puntos_a_repartir = sum([i.points for i in repartir])
                            for i in repartir:
                                i.points = round(float(puntos_a_repartir) / len(repartir), 2)



                        # # Mira se lle corresponden puntos
                        # if i.entity.entity_id in puntuados_club:
                        #     # ten en conta cantos puntuan por club
                        #     if  entity_to_point_ind > puntuados_club[i.entity.entity_id]:
                        #         if posicion_puntos < len(points):
                        #             puntos = points[posicion_puntos]
                        #             puntuados_club[i.entity.entity_id] = puntuados_club[i.entity.entity_id] + 1
                        #         posicion_puntos = posicion_puntos + 1
                        # else:
                        #     if  entity_to_point_ind > 0:
                        #         if  posicion_puntos < len(points):
                        #             puntos = points[posicion_puntos]
                        #             puntuados_club[i.entity.entity_id] = 1
                        #         posicion_puntos = posicion_puntos + 1
                        
                        # if last_mark == i.mark_time and last_pos == i.pos:
                        #     # é un empate

                        #     if puntos != 0:
                        #         empatados.append(result_phase_category)
                        #         tot_puntos = tot_puntos + puntos
                        #     else:
                        #         # retira o resultado para poñer despois dos empatados
                        #         pendentes.append(result_phase_category)
                        #         engadir = False
                        # else:
                        #     if len(empatados) > 1:
                        #         media_reparto = round(float(tot_puntos) / len(empatados), 2)
                        #         for j in empatados:
                        #             j.points = media_reparto
                        #     empatados = []
                        #     tot_puntos = 0
                        #     if puntos != 0:
                        #         empatados = [result_phase_category, ]
                        #         tot_puntos = puntos

                        # if engadir:
                        #     if i.entity.entity_id in puntuados_club:
                        #         # ten en conta cantos puntuan por club
                        #         if  entity_to_point_ind > puntuados_club[i.entity.entity_id]:
                        #             if posicion_puntos < len(points):
                        #                 puntos = points[posicion_puntos]
                        #                 puntuados_club[i.entity.entity_id] = puntuados_club[i.entity.entity_id] + 1
                        #             posicion_puntos = posicion_puntos + 1
                        #     else:
                        #         if  entity_to_point_ind > 0:
                        #             if  posicion_puntos < len(points):
                        #                 puntos = points[posicion_puntos]
                        #                 puntuados_club[i.entity.entity_id] = 1
                        #             posicion_puntos = posicion_puntos + 1

                        #     posicion = posicion + 1
                        #     result_phase_category.pos = posicion
                        #     result_phase_category.points = puntos
                        #     phase_category.results_phase_category.append(result_phase_category)
                        # elif pendentes:
                        #     # engade pendentes
                        #     for pendente in pedentes:
                        #         posicion = posicion + 1
                        #         pendente.pos = posicion
                        #         pendente.points = puntos
                        #         phase_category.results_phase_category.append(pendente)
                        #     cur_res = pendente
                        #     pendentes = []

                        # last_mark = cur_res.mark_time
                        # last_heat = cur_res.heat.heat_id
                        # tie_pos = tie_pos + 1


            elif results and phase_category.action == 'CLAS':  # clasifica para unha seguite phase
                #TODO: Facer este códito
                pass
            elif results and phase_category.action == '':  # nin clasifica nin puntua esta categoría da phase
                pass
            
            if phase_category.results_phase_category:
                phase_category.results_phase_category.save_all_items()
                categories_results[phase_category.category.name] = phase_category.results_phase_category

    def gen_phase_category_results_pdf(self, d, categories_results):
        """ Non sei quen usa esta función!! pode_borrarse??"""
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

        def add_category_title(lines):
            style_title = [
                ('ALIGN',(0,0),(-1,-1), 'LEFT'),
                ('FONT', (0, 0), (-1, -1), 'Open Sans Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
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
        # Category title
        event_title = '{}.- {}'.format(
            self.event.pos,
            self.event.name
            )
        add_event_title([[event_title, ]])
        # end category title
        for category_name, results_phase_category in categories_results.items():
            add_category_title([[category_name, ]])
            last_pos = None
            for result_phase_category in results_phase_category:
                i = result_phase_category.result
                if i.issue_id:
                    line_result = [[
                            i.issue_id, 
                            'X' not in i.heat.phase.event.code.upper() and i.person.license or i.relay.name, 
                            'X' not in i.heat.phase.event.code.upper() and i.person.full_name or "", 
                            'X' not in i.heat.phase.event.code.upper() and i.person.year[2:] or "", 
                            'X' not in i.heat.phase.event.code.upper() and i.person.entity.short_name or i.relay.entity.short_name, 
                            '', '0,0'],]
                else:
                    if last_pos == result_phase_category.pos:
                        position_result = ''
                    else:
                        position_result = result_phase_category.pos
                    line_result = [[
                            str(position_result), 
                            'X' not in i.heat.phase.event.code.upper() and i.person.license or i.relay.entity.entity_code, 
                            'X' not in i.heat.phase.event.code.upper() and i.person.full_name or i.relay.name, 
                            'X' not in i.heat.phase.event.code.upper() and i.person.year[2:] or "", 
                            'X' not in i.heat.phase.event.code.upper() and i.person.entity.short_name or i.relay.entity.short_name, 
                            i.mark_time, str(result_phase_category.points).replace(".", ",")],]
                last_pos = result_phase_category.pos
                add_result(line_result)
                print(line_result)

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


            print('fin results category {}'.format(category_name))
        print('fin results category {}'.format(category_name))
        d.build_file()

    def gen_results_pdf(self, d=False):
        # Obención de datos
        results = []
        # results_issues = []
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

        xerar = False
        if not d:
            champ = self.phases.champ
            file_name = '{}_{}.pdf'.format(
                self.event.file_name, self.progression.lower())
            d = self.init_report(file_name=file_name)
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
                phase_title = '{}.- {} - {}'.format(
                    i.heat.phase.event.pos,
                    i.heat.phase.event.name,
                    i.heat.phase.progression)
                phase_date_time = '{} {}'.format(
                    i.heat.phase.session.xdate,
                    i.heat.phase.session.xtime)
                # d.insert_title_1(text=event_title, alignment=0)
                lines.append([phase_title, phase_date_time])
                add_phase_title(lines)
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
