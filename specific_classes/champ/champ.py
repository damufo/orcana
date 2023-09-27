# -*- coding: utf-8 -*- 


import os
import json
from operator import attrgetter
from reportlab.lib.units import cm
from specific_classes.report_base import ReportBase
from specific_classes.champ.params import Params
from specific_classes.champ.entities import Entities
from specific_classes.champ.punctuations import Punctuations
from specific_classes.champ.categories import Categories
from specific_classes.champ.sessions import Sessions
from specific_classes.champ.events import Events
from specific_classes.champ.persons import Persons
from specific_classes.champ.relays import Relays
# from specific_classes.champ.inscriptions import Inscriptions
from specific_classes.champ.phases import Phases
from specific_classes.champ.classifications import Classifications
# from specific_classes.champ.heats import Heats
from specific_functions import files
from specific_functions.files import get_file_content
from specific_functions import utils


class Champ(object):

    def __init__(self, config):
        self.config = config
        self.params = {}
        self.has_champ = None
        # self.champ_id = 0
        # self.name = ''
        # self.pool_length = 0
        # self.pool_lanes = ''
        # self.chrono_type = ''
        # self.estament_id = ''
        # self.date_age_calculation = ''
        # self.venue = ''
        # self.pool_lane_min = 0
        # self.pool_lane_max = 9

    @property
    def file_name(self):
        date = self.sessions[0].date.replace('-', '')
        file_name = '{}_{}_{}'.format(
            date,
            self.params['champ_name'],
            self.params['champ_venue'])
        return utils.get_valid_filename(file_name.lower())

    @property
    def inscriptions_dict_pode_borrarse(self):
        # get all inscriptions for champ
        dict_inscriptions = {}
        for phase in self.phases:
            for i in phase.inscriptions:
                dict_inscriptions[i.inscription_id] = i
        return dict_inscriptions

    @property
    def inscriptions(self):
        # return a tuple with all inscriptions for champ
        list_inscriptions = []
        for phase in self.phases:
            for i in phase.inscriptions:
                list_inscriptions.append(i)
        return tuple(list_inscriptions)

    @property
    def heats(self):
        # return a tuple with all inscriptions for champ
        list_heats = []
        for phase in self.phases:
            for i in phase.heats:
                list_heats.append(i)
        return tuple(list_heats)

    @property
    def results_pode_borrarse(self):
        # get all results for champ
        dict_results = {}
        for phase in self.phases:
            for i in phase.inscriptions:
                if i.result:
                    dict_results[i.result.result_id] = i.result
        return dict_results

    @property
    def clear_champ(self):
        self.params = {}
        # self.champ_id = 0
        # self.name = ''
        # self.pool_length = 0
        # self.pool_lanes = []
        # self.chrono_type = ''
        # self.estament_id = ''
        # self.date_age_calculation = ''
        # self.venue = ''
        self.config.prefs['last_path_dbs'] = ''
        self.config.dbs.dbs_path = None

    def load_dbs(self, dbs_path):
        self.config.dbs.connect(dbs_path=dbs_path)
        # Comproba que sexa unha base de datos correcta
        if self.config.dbs.connection:
            # try:
                self.params = Params(champ=self)
                self.params.load_items_from_dbs()
                self.entities = Entities(champ=self)
                self.entities.load_items_from_dbs()
                self.sessions = Sessions(champ=self)
                self.sessions.load_items_from_dbs()
                self.punctuations = Punctuations(champ=self)
                self.punctuations.load_items_from_dbs()
                self.categories = Categories(champ=self)
                self.categories.load_items_from_dbs()
                self.events = Events(champ=self)
                self.events.load_items_from_dbs()
                self.persons = Persons(champ=self)
                self.persons.load_items_from_dbs()
                self.relays = Relays(champ=self)
                self.relays.load_items_from_dbs()
                self.phases = Phases(champ=self)
                self.phases.load_items_from_dbs()
                self.classifications = Classifications(champ=self)
                self.classifications.load_items_from_dbs()
                self.relays.clear_without_inscription()


                # As series van dentro das phases
                # As inscricións van dentro das fases
                # Os resultados carganse despois de cargar as inscricións e asignanse a cada inscrición

                self.config.prefs['last_path_dbs'] = str(dbs_path)
                self.has_champ = True
            # except:  # Algo fallou durante a carga
            #     self.config.prefs['last_path_dbs'] = ""
            #     self.clear_champ
        else:  # Non foi quen de conectar
            self.clear_champ
            print("Isto non debería pasar nunca. Erro:1134987239847105")
        self.config.prefs.save()

    @property
    def is_manager(self):
        return self.manager.is_manager

    @property
    def relays_events(self):
        # return tuple of tuples ((Relay, Event), )
        relays_events = []
        for inscription in self.inscriptions:
            if inscription.ind_rel == "R":
                relays_events.append((inscription.relay, inscription.event))
        return tuple(relays_events)

    @property
    def league_champ_id(self):
        value = ''
        if self.league_id and self.league_pos:
            value = '{}{}'.format(
                self.league_id, str(self.league_pos).zfill(2))
        return value

    def _set_points_ind_text(self, string_value):
        if string_value:
            if string_value == 'FINA':
                self.points_ind = 'FINA'
            else:
                self.points_ind = [int(i) for i in string_value.split('-')
                                   if i.isdigit()]
        else:
            self.points_ind = ''

    def _get_points_ind_text(self):

        if self.points_ind == 'FINA':
            value = self.points_ind
        else:
            value = '-'.join(["%s" % i for i in self.points_ind])
        return value

#    text format for points
    points_ind_text = property(fget=_get_points_ind_text,
                               fset=_set_points_ind_text)
        
    def _set_points_rel_text(self, string_value):
        if string_value:
            if string_value == 'FINA':
                self.points_rel = 'FINA'
            else:
                self.points_rel = [int(i) for i in string_value.split('-') 
                               if i.isdigit()]
        else:
            self.points_rel = ''

    def _get_points_rel_text(self):
        if self.points_rel == 'FINA':
            value = self.points_rel
        else:
            value = '-'.join(["%s" % i for i in self.points_rel])
        return value
    
#    text format for points    
    points_rel_text = property(fget=_get_points_rel_text, 
                               fset=_set_points_rel_text)

    def choices_categories(self, gender_id=None, add_empty=False):
        '''
        return values for wxchoice with ClientData
        '''
        values = []
        if add_empty:
            values.append(('', ''))
        if not self.categories:
            self.categories.load_items_from_dbs()
        for i in self.categories:
            if gender_id:
                if gender_id == i.gender_id and (i.category_id, i.category_id) not in values:
                    values.append((i.category_id, i.category_id))
            else:
                if (i.category_id, i.category_id) not in values:
                    values.append((i.category_id, i.category_id))
        return values

    def validade_pool_lanes_sort(self, pool_lanes_sort):
        pool_lanes_sort = pool_lanes_sort.replace(' ', '')
        pool_lanes = [int(i) for i in pool_lanes_sort.split(',')
                                if i.isdigit()]
        # remove duplicates preserving order
        pool_lanes_cleaned = sorted(set(pool_lanes), key=lambda x: pool_lanes.index(x))

        if (max(pool_lanes) > 20 or
        min(pool_lanes) < 0 or
        len(pool_lanes) != len(pool_lanes_cleaned) or
        len(pool_lanes) < 3 or
        len(pool_lanes) > 20):  # Invalid value
            pool_lanes_sort = ''
        else:
            pool_lanes_sort = ', '.join(["%s" % i for i in pool_lanes])
        return pool_lanes_sort

    def gen_heats(self):
        '''
        Xera as fases como TIM (forma abreviada de indicar Timed Finals).
        Xera as series
        Xera as liñas de resultados (aquí é onde vai a serie e a pista)
        '''
        print("Generate all heats")
        # heats and results
        for phase in self.phases:
            if phase.progression == 'TIM':
                phase.gen_heats()
            else:
                print('This phase is not TIM')
        print('Fin')

    def init_report(self, file_name):
        file_path = os.path.join(
            self.config.work_folder_path,
            file_name)

        if self.params['champ_chrono_type'] == 'M':
            chrono_text = _('manual')
        else:
            chrono_text = _('electronic')
        subtitle = "{}. Piscina de {} m. Cronometraxe {}.".format(
            self.params['champ_venue'], self.params['champ_pool_length'], chrono_text)
        d =  ReportBase(
                app_path_folder=self.config.app_path_folder,
                app_version=self.config.app_version,
                file_path=file_path, 
                orientation='portrait',
                title= self.params['champ_name'],
                subtitle=subtitle)
        return d

    def report_results(self):
        d =  self.init_report(file_name=_("results_full.pdf"))
        page_break = False
        for phase in self.phases:
            if phase.official:
                if page_break:
                    d.insert_page_break()
                phase.gen_results_pdf(d=d)
                page_break = True

        d.build_file()

    def gen_classifications_pdf(self):
        d =  self.init_report(file_name=_("classifications.pdf"))

        def save_table(lines):
            col_widths = ['5%', '50%', '20%', '20%', '10%']
            style = [
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                # ('GRID', (0, 0), (-1, -1), 0.5, d.colors.grey),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
            ]

            table = lines
            d.insert_table(table=table, colWidths=col_widths, 
                           style=style, pagebreak=False)

        d.insert_title_1(text=_("Classifications"), alignment=1)

        sql_points_club_category = '''
select 
    case when (select person_id from inscriptions i where i.inscription_id=(select r.inscription_id from results r where r.result_id=rpc.result_id))>0 
    then 
        (select entity_id from persons p where p.person_id=(select person_id from inscriptions i where i.inscription_id=(select r.inscription_id from results r where r.result_id=rpc.result_id)))
    else 
        (select entity_id from relays r where r.relay_id=(select relay_id from inscriptions i where i.inscription_id=(select r.inscription_id from results r where r.result_id=rpc.result_id)))
    end as "entity_id",
    
sum(points) as points
from phases_categories_results rpc
where (select category_id  from categories c where c.category_id=(select category_id from phases_categories pc where pc.phase_category_id=rpc.phase_category_id))=?
group by 
    case when (select person_id from inscriptions i where i.inscription_id=(select r.inscription_id from results r where r.result_id=rpc.result_id))>0 
    then 
        (select entity_id from persons p where p.person_id=(select person_id from inscriptions i where i.inscription_id=(select r.inscription_id from results r where r.result_id=rpc.result_id)))
    else 
        (select entity_id from relays r where r.relay_id=(select relay_id from inscriptions i where i.inscription_id=(select r.inscription_id from results r where r.result_id=rpc.result_id)))
    end
order by
sum(points) desc;          '''
        entities_dict = self.entities.dict
        for classification in self.classifications:
            d.insert_title_1(text=classification.name, alignment=0)
            d.insert_spacer(10, 10)
            # Sump points for all classification categories
            entity_points = {}
            # (ENTITY_ID, POINTS) = range(2)
            for category in classification.categories:
                # Determine factor correction
                if not classification.gender_id:
                    factor_correction = 1
                elif classification.gender_id and classification.gender_id == category.gender_id:
                    factor_correction = 1
                elif classification.gender_id != 'X' and category.gender_id == 'X':
                    factor_correction = 0.5  
                else:  # no resto dos casos non puntúa     
                    factor_correction = 0

                res = self.config.dbs.exec_sql(
                        sql=sql_points_club_category,
                        values=((category.category_id,),))
                if res != 'err' and res:
                    for entity_id, points in res:
                        if entity_id in entity_points:
                            entity_points[entity_id] += points * factor_correction
                        else:
                            entity_points[entity_id] = points * factor_correction
            # Print clasification lines
            lines = []
            last_points = -1
            last_pos = -1
            pos = 1
            entity_points_sorted = dict(sorted(entity_points.items(), key=lambda item: item[1], reverse=True))  # Sort by points
            for entity_id, points in entity_points_sorted.items():
                if not entity_id:
                    print('dd')
                entity = entities_dict[entity_id]
                if points == last_points:
                    line_pos = ""
                else:
                    line_pos = pos
                    last_pos = pos
                lines.append((
                    line_pos,
                    entity.long_name,
                    entity.entity_code,
                    points,
                ))
                last_points = points
                pos += 1
            save_table(lines)

        d.build_file()
        print("fin")

#     def gen_classifications_pdf_old(self):
#         categories = {}
#         d =  self.init_report(file_name=_("classifications.pdf"))

#         def save_table(lines):
#             col_widths = ['5%', '50%', '20%', '20%', '10%']
#             style = [
#                 ('FONTSIZE', (0, 0), (-1, -1), 9),
#                 # ('GRID', (0, 0), (-1, -1), 0.5, d.colors.grey),
#                 ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#                 ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
#                 ('ALIGN', (1, 0), (1, -1), 'LEFT'),
#                 ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
#             ]

#             table = lines
#             d.insert_table(table=table, colWidths=col_widths, 
#                            style=style, pagebreak=False)
#         def save_table_total(category, table_total):
#             lines = []
#             sorted_total = sorted(table_total.items(), key=lambda x:x[1], reverse=True)
#             lines = []
#             last_points = -1
#             last_pos = -1
#             pos = 1
#             for entity_id, points in sorted_total:
#                 entity = self.entities.get_entity(entity_id=entity_id)
#                 if points == last_points:
#                     line_pos = ""
#                 else:
#                     line_pos = pos
#                     last_pos = pos
#                 lines.append((
#                     line_pos,
#                     entity.long_name,
#                     entity.entity_code,
#                     points,
#                 ))
#                 last_points = points
#                 pos += 1
#             gender = _("Total")
#             title_category = "{} {}".format(category.name, gender).capitalize()
#             d.insert_title_1(text=title_category, alignment=0)
#             d.insert_spacer(10, 10)
#             save_table(lines)

#         d.insert_title_1(text=_("Classifications by category"), alignment=1)

#         sql = '''
# select 
#     case when (select person_id from inscriptions i where i.inscription_id=(select r.inscription_id from results r where r.result_id=rpc.result_id))>0 
#     then 
#         (select entity_id from persons p where p.person_id=(select person_id from inscriptions i where i.inscription_id=(select r.inscription_id from results r where r.result_id=rpc.result_id)))
#     else 
#         (select entity_id from relays r where r.relay_id=(select relay_id from inscriptions i where i.inscription_id=(select r.inscription_id from results r where r.result_id=rpc.result_id)))
#     end as "entity_id",
    
# sum(points) as points
# from phases_categories_results rpc
# where (select category_id  from categories c where c.category_id=(select category_id from phases_categories pc where pc.phase_category_id=rpc.phase_category_id))=?
# group by 
#     case when (select person_id from inscriptions i where i.inscription_id=(select r.inscription_id from results r where r.result_id=rpc.result_id))>0 
#     then 
#         (select entity_id from persons p where p.person_id=(select person_id from inscriptions i where i.inscription_id=(select r.inscription_id from results r where r.result_id=rpc.result_id)))
#     else 
#         (select entity_id from relays r where r.relay_id=(select relay_id from inscriptions i where i.inscription_id=(select r.inscription_id from results r where r.result_id=rpc.result_id)))
#     end
# order by
# sum(points) desc;          '''
#         last_category = None
#         lines = []
#         total = {}
#         (ENTITY_ID, POINTS) = range(2)
#         for category in self.categories:
#             if lines and last_category.show_report:
#                 gender = self.config.genders.get_long_name(gender_id=last_category.gender_id)
#                 title_category = "{} {}".format(last_category.name, gender).capitalize()
#                 d.insert_title_1(text=title_category, alignment=0)
#                 d.insert_spacer(10, 10)
#                 save_table(lines)
#             if last_category and category.code != last_category.code:
#                 # print total
#                 save_table_total(category=last_category, table_total=total)
#                 total = {}
#             res = self.config.dbs.exec_sql(sql=sql, values=((category.category_id,),))
#             lines = []
#             if res != 'err' and res:
#                 # print category puntuation
#                 gender = self.config.genders.get_long_name(gender_id=category.gender_id)
#                 last_points = -1
#                 last_pos = -1
#                 pos = 1
#                 for entity_id, points in res:
#                     entity = self.entities.get_entity(entity_id=entity_id)
#                     if points == last_points:
#                         line_pos = ""
#                     else:
#                         line_pos = pos
#                         last_pos = pos
#                     lines.append((
#                         line_pos,
#                         entity.long_name,
#                         entity.entity_code,
#                         points,
#                     ))
#                     last_points = points
#                     pos += 1
#                     if entity.entity_id in total:
#                         total[entity.entity_id] += points
#                     else:
#                         total[entity.entity_id] = points
#             last_category = category
#         # Isto é para imprimir a última categoría se é que hai que facelo
#         if lines and last_category.show_report:
#             gender = self.config.genders.get_long_name(gender_id=last_category.gender_id)
#             title_category = "{} {}".format(last_category.name, gender).capitalize()
#             d.insert_title_1(text=title_category, alignment=0)
#             d.insert_spacer(10, 10)
#             save_table(lines)
#         if total:
#             # print total
#             save_table_total(category=last_category, table_total=total)


#         d.build_file()
#         print("fin")

    def export_results(self):
        self.gen_lev()

    def gen_lev(self):
        """
        Generate file export lev format
        """
        categorias = (
            ("ABSO", "MENORES OPEN FEMENINO"),
            ("ABSO", "MENORES OPEN MASCULINO"),
            ("ABSO", "ABSOLUTO OPEN FEMENINA"),
            ("ABSO", "ABSOLUTO OPEN MASCULINO"),
            ("INFA", "Infantil Femenino (Invierno)"),
            ("ABSO", "SENIOR-JUNIOR 1 - JUNIOR 2 FEM."),
            ("ABSO", "SENIOR-JUNIOR 1 - JUNIOR 2 MAS."),
            ("JUNI", "JUNIOR 1"),
            ("JUNI", "JUNIOR 2"),
            ("SENI", "SENIOR"),
            ("ABSO", "INFANTIL MASCULINO LD"),
            ("ABSO", "INFANTIL FEMENINO LD"),
            ("ABSO", "INFANTIL-JUNIOR FEMENINO"),
            ("ABSO", "INFANTIL-JUNIOR MASCULINO"),
            ("9 A", "9 años"),
            ("10 A", "10 años"),
            ("11 A", "11 años"),
            ("12 A", "12 años"),
            ("13 A", "13 años"),
            ("14 A", "14 años"),
            ("15 A", "15 años"),
            ("16 A", "16 años"),
            ("17 A", "17 años"),
            ("18 A", "18 años"),
            ("20+", "20+"),
            ("+80", "+80"),
            ("+100", "+100"),
            ("+120", "+120"),
            ("+160", "+160"),
            ("+200", "+200"),
            ("+240", "+240"),
            ("+280", "+280"),
            ("+320", "+320"),
            ("95+", "95+"),
            ("90+", "90+"),
            ("85+", "85+"),
            ("80+", "80+"),
            ("75+", "75+"),
            ("70+", "70+"),
            ("65+", "65+"),
            ("60+", "60+"),
            ("55+", "55+"),
            ("50+", "50+"),
            ("45+", "45+"),
            ("40+", "40+"),
            ("35+", "35+"),
            ("30+", "30+"),
            ("25+", "25+"),
            ("ABSO.mixed", "Absoluto Mixto"),
            ("ABSO.female", "Absoluto Femenino"),
            ("ABSO.male", "Absoluto Masculino"),
            ("ABSJ.mixed", "Absouto Joven Mixto"),
            ("ABSJ.female", "Absoluto Joven Femenino"),
            ("ABSJ.male", "Absoluto Joven Masculino"),
            ("JUNI.", "JUNIOR"),
            ("JUNI.mixed", "Junior Mixto"),
            ("JUNI.female", "Junior Femenino"),
            ("JUNI.male", "Junior Masculino"),
            ("INFA.mixed", "Infantil Mixto"),
            ("INFA.female", "Infantil Femenino"),
            ("INFA.male", "Infantil Masculino"),
            ("ALEV.mixed", "Alevín Mixto"),
            ("ALEV.female", "Alevín Femenino"),
            ("ALEV.male", "Alevín Masculino"),
            ("BENJ.mixed", "Benjamín Mixto"),
            ("BENJ.female", "Benjamín Femenino"),
            ("BENJ.male", "Benjamín Masculino"),
            ("PROM.mixed", "Prebenjamín Mixto"),
            ("PROM.female", "Prebenjamín Femenino"),
            ("PROM.male", "Prebenjamín Masculino"),
        )
        cat_dic = {}
        for i in categorias:
            cat_dic[i[0].lower()] = i[1]
        parent_blank = [''] * 39
        head = [
            "phaseresult.last_name",
            "phaseresult.first_name",
            "phaseresult.resultable.profile_number",
            "phaseresult.resultable.@where:code",
            "phaseresult.resultable.@type",
            "phaseresult.style.code",
            "phaseresult.value",
            "phaseresult.goal",
            "phaseresult.date",
            "phaseresult.custom_fields.result_point",
            "phaseresult.custom_fields.result_lane",
            "phaseresult.custom_fields.result_heat",
            "phaseresult.category.maximum_age",
            "phaseresult.category.minimum_age",
            "phaseresult.category.name",
            "phaseresult.category.@where:categorydisciplines.discipline.id",
            "phaseresult.competition",
            "phaseresult.location",
            "phaseresult.discipline_fields.pool_size",
            "phaseresult.discipline_fields.chronometer",
            "phaseresult.custom_fields.pool_name",
            "phaseresult.custom_fields.pool_lanemin",
            "phaseresult.custom_fields.pool_lanemax",
            "phaseresult.gender",
            "phaseresult.custom_fields.event_number",
            "phaseresult.custom_fields.event_round",
            "phaseresult.official",
            "phaseresult.office.code",
            "phaseresult.participants_amount",
            "phaseresult.participants_names.0",
            "phaseresult.participants_names.1",
            "phaseresult.participants_names.2",
            "phaseresult.participants_names.3",
            "phaseresult.participants_names.4",
            "phaseresult.participants_names.5",
            "phaseresult.participants_names.6",
            "phaseresult.participants_names.7",
            "phaseresult.custom_fields.leveradeid",
            "phaseresult.position",
            "phaseresult.phaseresult.last_name",
            "phaseresult.phaseresult.first_name",
            "phaseresult.phaseresult.resultable.profile_number",
            "phaseresult.phaseresult.resultable.@where:code",
            "phaseresult.phaseresult.resultable.@type",
            "phaseresult.phaseresult.style.code",
            "phaseresult.phaseresult.value",
            "phaseresult.phaseresult.goal",
            "phaseresult.phaseresult.date",
            "phaseresult.phaseresult.custom_fields.result_point",
            "phaseresult.phaseresult.custom_fields.result_lane",
            "phaseresult.phaseresult.custom_fields.result_heat",
            "phaseresult.phaseresult.category.maximum_age",
            "phaseresult.phaseresult.category.minimum_age",
            "phaseresult.phaseresult.category.name",
            "phaseresult.phaseresult.category.@where:categorydisciplines.discipline.id",
            "phaseresult.phaseresult.competition",
            "phaseresult.phaseresult.location",
            "phaseresult.phaseresult.discipline_fields.pool_size",
            "phaseresult.phaseresult.discipline_fields.chronometer",
            "phaseresult.phaseresult.custom_fields.pool_name",
            "phaseresult.phaseresult.custom_fields.pool_lanemin",
            "phaseresult.phaseresult.custom_fields.pool_lanemax",
            "phaseresult.phaseresult.gender",
            "phaseresult.phaseresult.custom_fields.event_number",
            "phaseresult.phaseresult.custom_fields.event_round",
            "phaseresult.phaseresult.official",
            "phaseresult.phaseresult.office.code",
            "phaseresult.phaseresult.participants_amount",
            "phaseresult.phaseresult.participants_names.0",
            "phaseresult.phaseresult.participants_names.1",
            "phaseresult.phaseresult.participants_names.2",
            "phaseresult.phaseresult.participants_names.3",
            "phaseresult.phaseresult.participants_names.4",
            "phaseresult.phaseresult.participants_names.5",
            "phaseresult.phaseresult.participants_names.6",
            "phaseresult.phaseresult.participants_names.7",
            "phaseresult.phaseresult.custom_fields.leveradeid",
            "phaseresult.phaseresult.position"
            ]
        head_str_line = ';'.join(head)
        head_str_line += '\n'
        lines = []
        for phase in self.phases:
            if phase.official:
                for result in phase.results:
                    # result.result_splits.load_items_from_dbs()
                    # Determina se o resultado se ten en conta ou non
                    if result.issue_id:
                        if result.ind_rel == 'I':
                            print(('issue', result.person.name, result.person.surname, result.issue_id))
                            continue
                        elif result.ind_rel == 'R':
                            result.relay.relay_members.load_items_from_dbs()
                            num_members = result.relay.relay_members.num_members
                            num_splits = len(result.result_splits)
                            if result.issue_split<=(num_splits/num_members):
                                print(('issue', result.relay.name, result.issue_id))
                                continue
                    if result.ind_rel == 'R': # non envía remudas sen remudistas
                        result.relay.relay_members.load_items_from_dbs()
                        if result.relay.relay_members.num_members == 0:
                            print('Erro:  remuda sen membros, isto non debería pasar nunca')
                            continue
                    style_names = {
                        'M':'butterfly',
                        'E':'backstroke',
                        'B':'breaststroke',
                        'L':'freestyle',
                        'S':'medley',
                        }
                    genders = {
                        'M':'male',
                        'F':'female',
                        'X':'mixed',
                        }
                    
                    #result final parcial
                    line = []
                    members = {0: '', 1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: ''}
                    members_licenses_str = ''
                    if result.ind_rel == 'I':
                        line.append(result.person.surname)  # phaseresult.last_name
                        line.append(result.person.name)  # phaseresult.first_name
                        line.append(result.person.license)  # phaseresult.resultable.profile_number
                        line.append('')  # phaseresult.resultable.@where:code
                        line.append('license')  # phaseresult.resultable.@type
                    else:
                        line.append('')  # phaseresult.last_name
                        line.append('')  # phaseresult.first_name
                        line.append('')  # phaseresult.resultable.profile_number
                        line.append(result.relay.entity.entity_code)  # phaseresult.resultable.@where:code
                        line.append('club')  # phaseresult.resultable.@type
                        members_licenses = []
                        for pos, member in enumerate(result.relay.relay_members):
                            members[pos] = member.person.full_name
                            members_licenses.append(member.person.license)
                        if members_licenses:
                            members_licenses_str = members_licenses
                        distance_per_member = int(result.distance / result.relay.relay_members.num_members)
                        num_member = result.relay.relay_members.num_members  # for splits calculations

                    line.append(style_names[result.style_id])  # phaseresult.style.code
                    line.append(result.mark_hundredth)  # phaseresult.value
                    line.append(result.distance)  # phaseresult.goal
                    line.append('{}'.format(result.heat.start_time or result.phase.date_time))  # phaseresult.date
                    #FIXME: points
                    line.append('0')  # phaseresult.custom_fields.result_point
                    line.append(str(result.lane))  # phaseresult.custom_fields.result_lane
                    line.append(str(result.heat.pos))  # phaseresult.custom_fields.result_heat
                    line.append(int(result.category.to_age))  # phaseresult.category.maximum_age
                    line.append(int(result.category.from_age))  # phaseresult.category.minimum_age
                    line.append(result.category.name)  # phaseresult.category.name
                    line.append('38')  # phaseresult.category.@where:categorydisciplines.discipline.id
                    line.append(self.params['champ_name'])  # phaseresult.competition
                    line.append(self.params['champ_venue'])  # phaseresult.location
                    line.append(str(self.params['champ_pool_length']))  # phaseresult.discipline_fields.pool_size
                    line.append(self.params['champ_chrono_type'] == 'M' and 'manual' or 'electronic')  # phaseresult.discipline_fields.chronometer
                    line.append(self.params['champ_venue'])  # phaseresult.custom_fields.pool_name
                    line.append(str(phase.pool_lane_min))  # phaseresult.custom_fields.pool_lanemin
                    line.append(str(phase.pool_lane_max))  # phaseresult.custom_fields.pool_lanemax
                    #FIXME: coller o sexo da persoa ou remuda
                    line.append(genders[result.event.gender_id])  # phaseresult.gender
                    line.append(str(result.event.pos))  # phaseresult.custom_fields.event_number
                    line.append(result.phase.progression)  # phaseresult.custom_fields.event_round
                    line.append(1)  # phaseresult.official
                    line.append('athlete')  # phaseresult.office.code
                    line.append(int(result.event.num_members))  # phaseresult.participants_amount
                    line.append(members[0])  # phaseresult.participants_names.0
                    line.append(members[1])  # phaseresult.participants_names.1
                    line.append(members[2])  # phaseresult.participants_names.2
                    line.append(members[3])  # phaseresult.participants_names.3
                    line.append(members[4])  # phaseresult.participants_names.4
                    line.append(members[5])  # phaseresult.participants_names.5
                    line.append(members[6])  # phaseresult.participants_names.6
                    line.append(members[7])  # phaseresult.participants_names.7
                    line.append(members_licenses_str)  # phaseresult.custom_fields.leveradeid
                    line.append(int(result.arrival_pos))  # phaseresult.position (in heat)        
                    lines.append(line + parent_blank)
                    line_parent = line

                    if result.ind_rel == 'I':
                        splits = reversed(result.result_splits[:-1])
                    else:
                        if len(result.result_splits) >= len(members_licenses_str):
                            splits = reversed(result.result_splits)
                        else:
                            # hai menos parciais que remudistas
                            splits = []
                    mark_hundredth_adjust = 0
                    for split in splits:
                        line = []
                        members = {0: '', 1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: ''}
                        members_licenses_str = ''
                        split_distance = 0
                        if result.ind_rel == 'I':
                            line.append(result.person.surname)  # phaseresult.last_name
                            line.append(result.person.name)  # phaseresult.first_name
                            line.append(result.person.license)  # phaseresult.resultable.profile_number
                            line.append('')  # phaseresult.resultable.@where:code
                            line.append('license')  # phaseresult.resultable.@type
                            split_gender = genders[result.person.gender_id]
                            split_mark_hundredth = split.mark_hundredth
                            split_distance = split.distance
                        else:
                            # FIXME: este cálculo seguro que se pode mellorar
                            if int(split.distance % distance_per_member) == 0:
                                num_member -= 1
                                if num_member > 0:
                                    # calcula o tempo de axuste para o membro
                                    for i in result.result_splits:
                                        if i.distance == distance_per_member * num_member:
                                            mark_hundredth_adjust = i.mark_hundredth
                                            break
                                else:
                                    mark_hundredth_adjust = 0
                            split_distance = split.distance - (num_member * distance_per_member)
                            if num_member < len(result.relay.relay_members):
                                member = result.relay.relay_members[num_member]
                                line.append(member.person.surname)  # phaseresult.last_name
                                line.append(member.person.name)  # phaseresult.first_name
                                line.append(member.person.license)  # phaseresult.resultable.profile_number
                                split_gender = genders[member.person.gender_id]
                            else:
                                line.append('')  # phaseresult.last_name
                                line.append('')  # phaseresult.first_name
                                line.append('')  # phaseresult.resultable.profile_number
                                split_gender = ''
                            split_mark_hundredth = split.mark_hundredth - mark_hundredth_adjust
                            line.append('')  # phaseresult.resultable.@where:code
                            line.append('license')  # phaseresult.resultable.@type
                        line.append(style_names[split.style_id])  # phaseresult.style.code
                        line.append(split_mark_hundredth)  # phaseresult.value
                        line.append(split_distance)  # phaseresult.goal
                        line.append('{}'.format(result.heat.start_time or result.phase.date_time))  # phaseresult.date
                        #FIXME: points
                        line.append('0')  # phaseresult.custom_fields.result_point
                        line.append(str(result.lane))  # phaseresult.custom_fields.result_lane
                        line.append(str(result.heat.pos))  # phaseresult.custom_fields.result_heat
                        line.append(int(result.category.to_age))  # phaseresult.category.maximum_age
                        line.append(int(result.category.from_age))  # phaseresult.category.minimum_age
                        line.append(result.category.code)  # phaseresult.category.name
                        line.append('38')  # phaseresult.category.@where:categorydisciplines.discipline.id
                        line.append(self.params['champ_name'])  # phaseresult.competition
                        line.append(self.params['champ_venue'])  # phaseresult.location
                        line.append(str(self.params['champ_pool_length']))  # phaseresult.discipline_fields.pool_size
                        line.append(self.params['champ_chrono_type'] == 'M' and 'manual' or 'electronic')  # phaseresult.discipline_fields.chronometer
                        line.append(self.params['champ_venue'])  # phaseresult.custom_fields.pool_name
                        line.append(str(phase.pool_lane_min))  # phaseresult.custom_fields.pool_lanemin
                        line.append(str(phase.pool_lane_max))  # phaseresult.custom_fields.pool_lanemax
                        #FIXME: coller o sexo da persoa ou remuda
                        line.append(split_gender)  # phaseresult.gender
                        line.append(str(result.event.pos))  # phaseresult.custom_fields.event_number
                        line.append(result.phase.progression)  # phaseresult.custom_fields.event_round
                        line.append(split.official)  # phaseresult.official
                        line.append('athlete')  # phaseresult.office.code
                        line.append(1)  # phaseresult.participants_amount
                        line.append(members[0])  # phaseresult.participants_names.0
                        line.append(members[1])  # phaseresult.participants_names.1
                        line.append(members[2])  # phaseresult.participants_names.2
                        line.append(members[3])  # phaseresult.participants_names.3
                        line.append(members[4])  # phaseresult.participants_names.4
                        line.append(members[5])  # phaseresult.participants_names.5
                        line.append(members[6])  # phaseresult.participants_names.6
                        line.append(members[7])  # phaseresult.participants_names.7
                        line.append(members_licenses_str)  # phaseresult.custom_fields.leveradeid
                        line.append(int(result.arrival_pos))  # phaseresult.position (in heat)

                        last_split_mark_hundredth = split.mark_hundredth  # to calculate relay member time
                        if split.mark_hundredth:
                            lines.append(line + line_parent)
                        else:
                            print("parcial sen tempo")

        lines.append(head)
        lines.reverse()
        for i in lines:
            print(i)

        datos = []
        int_cols = [6, 7, 8, 10, 11]
        for i in lines:
            row = ""
            for col, j in enumerate(i):
                json.dumps(j)
                if isinstance(j, str):
                    value = '"{}"'.format(j)
                elif isinstance(j, int):
                    value = '{}'.format(j)
                elif isinstance(j, list):
                    value = json.dumps(j)
                else:
                    print('Isto non debería pasar.')
                row += ';{}'.format(value)

            datos.append(row[1:])

        datos = "\n".join(datos)
        datos += "\n"
        # datos = head_str_line + datos
        file_name = '{}.csv'.format(
            self.file_name)
        file_path = os.path.join(
            self.config.work_folder_path,
            file_name)
        files.set_file_content(content=datos,
                               file_path=file_path,
                               compress=False,
                               binary=False,
                               encoding='utf-8-sig',
                               end_line="\n")
        print('Fin')

    def report_inscriptions_by_club(self, entity=None):
        if entity:
            entities = [entity, ]
            file_name = _('inscriptions_by_club_{}.pdf').format(entity.entity_code)
        else:
            entities = self.entities
            file_name = _('inscriptions_by_club_full.pdf')
        d =  self.init_report(file_name=file_name)

        def save_table(lines, inscription):
            col_widths = ['7%', '22%', '10%', '10%', '8%', '7%', '10%', '11%', '15%']
            style = [
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, d.colors.grey),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('ALIGN', (8, 0), (8, -1), 'LEFT'),
            ]

            table = lines
            d.insert_table(table=table, colWidths=col_widths, 
                           style=style, pagebreak=False)

        d.insert_title_1(text=_("Inscriptions by entity"), alignment=1)

        last_entity = None
        entities = sorted(entities, key=attrgetter('entity_code'), reverse=False)
        for entity in entities:
            # check has inscriptions
            has_inscriptions =  False
            for i in self.inscriptions:
                if i.ind_rel == 'I' and i.person.entity == entity:
                    has_inscriptions = True
                    break
                elif i.ind_rel == 'R' and i.relay.entity == entity:
                    has_inscriptions = True
                    break
            if not has_inscriptions:
                continue
            # end check has inscriptions
            if last_entity:
                d.insert_page_break()
            d.insert_paragraph("")
            last_entity = entity
            style = [
                ('FONT', (0, 0), (-1, -1), 'Open Sans Bold'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BACKGROUND', (0, 0), (-1, 0), d.colors.lightgrey)
            ]
            col_widths = ['100%', ]

            table = [["%s %s" % (
                entity.entity_code, entity.long_name), ], ]
            d.insert_table(
                table=table, colWidths=col_widths,
                style=style, pagebreak=False)

            inscriptions_ind = [i for i in self.inscriptions if i.ind_rel == 'I']
            inscriptions_ind = [i for i in inscriptions_ind if i.person.entity == entity]
            inscriptions_ind = sorted(inscriptions_ind, key=attrgetter('event.pos'), reverse=False)
            inscriptions_ind = sorted(inscriptions_ind, key=attrgetter('person.name'), reverse=False)
            inscriptions_ind = sorted(inscriptions_ind, key=attrgetter('person.surname'), reverse=False)

            lines = []
            last_person = None
            prev_row = None
            for row in inscriptions_ind:
                if row.person != last_person:
                    if lines:
                        save_table(lines=lines, inscription=prev_row)
                        d.insert_paragraph("")
                        lines = []
                    style = [
                        ('FONT', (0, 0), (-1, -1), 'Open Sans Bold'),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ]
                    col_widths = ['100%', ]  
                    table = [
                        ["%s %s, %s (%s)" % (
                            row.person.license, row.person.surname, 
                            row.person.name, row.person.birth_date[:4]),],]
                    d.insert_table(
                        table=table, colWidths=col_widths,
                        style=style, pagebreak=False)
                    last_person = row.person

                mark_time = row.mark_time
                equated_time = row.equated_time
                lines.append([
                    row.event.pos, row.event.name, row.category.code,
                    mark_time, '%sm' % row.pool_length, row.chrono_type,
                    equated_time, row.date, row.venue],)
                prev_row = row

            else:
                if lines:
                    save_table(lines=lines, inscription=prev_row)
                    print("rematou individual")
                    lines = []

            # #remudas
            inscriptions_rel = [i for i in self.inscriptions if i.ind_rel == 'R']
            inscriptions_rel= [i for i in inscriptions_rel if i.relay.entity == entity]
            inscriptions_rel = sorted(inscriptions_rel, key=attrgetter('relay.name'), reverse=False)
            inscriptions_rel = sorted(inscriptions_rel, key=attrgetter('event.pos'), reverse=False)

            lines = []
            prev_row = None
            for row in inscriptions_rel:
                if lines:
                    save_table(lines=lines, inscription=prev_row)
                    d.insert_paragraph("")
                    lines = []
                style = [
                    ('FONT', (0, 0), (-1, -1), 'Open Sans Bold'),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                ]
                col_widths = ['100%', ]  
                table = [
                    ["{} {}".format(
                        row.relay.entity.entity_code, row.relay.name),],]
                d.insert_table(
                    table=table, colWidths=col_widths,
                    style=style, pagebreak=False)

                mark_time = row.mark_time
                equated_time = row.equated_time
                lines.append([
                    row.event.pos, row.event.name, row.category.code,
                    mark_time, '%sm' % row.pool_length, row.chrono_type,
                    equated_time, row.date, row.venue],)
                prev_row = row

            else:
                if lines:
                    save_table(lines=lines, inscription=prev_row)
                    print("rematou bucle remudas")

        d.build_file()
        print("feito")

    def report_inscriptions_by_event(self, phase=None):
        if phase:
            phases = [phase, ]
            file_path = os.path.join(
                self.config.work_folder_path,
                _('inscriptions_by_event_{}.pdf').format(phase.file_name),
                )
        else:
            phases = self.phases
            file_name = _('inscriptions_by_event_full.pdf')
        d = self.init_report(file_name=file_name)
        def save_lines_ind(lines):
            col_widths = ['4%', '8%', '30%', '4%', '10%', '12%', '8%', '8%', '16%']
            style = [
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (5, 0), (5, -1), 'RIGHT'),
                ('ALIGN', (6, 0), (6, -1), 'RIGHT'),
                ('ALIGN', (2, 0), (2, -1), 'LEFT'),
                ('ALIGN', (8, 0), (8, -1), 'LEFT'),
            ]
            table = lines
            d.insert_table(table=table, colWidths=col_widths,
                           style=style, pagebreak=False)

        def save_lines_rel(lines):
            col_widths = ['4%', '8%', '24%', '14%', '10%', '12%', '8%', '8%', '12%']
            style = [
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (5, 0), (5, -1), 'RIGHT'),
                ('ALIGN', (6, 0), (6, -1), 'RIGHT'),
                ('ALIGN', (2, 0), (2, -1), 'LEFT'),
                ('ALIGN', (8, 0), (8, -1), 'LEFT'),
            ]
            table = lines
            d.insert_table(table=table, colWidths=col_widths,
                           style=style, pagebreak=False)

        d.insert_title_1(text=_("Inscriptions by event"), alignment=1)

        last_event = None
        for event in self.events:
            if last_event:
                d.insert_page_break()
            d.insert_paragraph("")
            last_event = event
            style = [
                ('FONT', (0, 0), (-1, -1), 'Open Sans Bold'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ]
            col_widths = ['100%', ]

            table = [["%s. %s" % (event.pos, event.name), ], ]
            d.insert_table(table=table, colWidths=col_widths,
                               style=style, pagebreak=False)
    
            inscriptions_ind = [i for i in self.inscriptions if i.event == event]
            inscriptions_ind = sorted(inscriptions_ind, key=attrgetter('equated_hundredth'), reverse=False)
            lines = []
            for row in inscriptions_ind:
                if row.ind_rel == 'I':
                    license = row.person.license
                    name = row.person.full_name
                    birth_year = row.person.birth_date[2:4]
                    entity_name = row.person.entity.short_name
                elif row.ind_rel == 'R':
                    license = row.relay.entity.entity_code
                    name = row.relay.name
                    birth_year = row.relay.category.name
                    entity_name = row.relay.entity.short_name
                else:
                    print("Erro")
                    AssertionError("produciuse un erro")

                mark_time = '{} {}{}'.format(
                    row.mark_time,
                    row.pool_length,
                    row.chrono_type)
                    # pool_chrono = '{}{}'.format(
                    #     self.pool_length,
                    #     self.chrono_type)
                equated_time = row.equated_time
                lines.append([
                    len(lines) + 1, license, name, birth_year,
                    entity_name, mark_time, equated_time, row.date, row.venue])
            else:
                if lines:
                    if event.ind_rel == 'I':
                        save_lines_ind(lines=lines)
                    else:
                        save_lines_rel(lines=lines)
                    print("rematou bucle")

        d.build_file()
        print("feito")

    def report_sumary_participants(self, entity=None):
        if entity:
            entities = [entity, ]
            file_name =_('sumary_participants_{}.pdf').format(entity.entity_code)
        else:
            entities = self.entities
            file_name = _('sumary_participants_full.pdf')
        d = self.init_report(file_name=file_name)

        def save_lines(lines):
            # col_widths = ['4%', '8%', '24%', '14%', '10%', '12%', '8%', '8%', '12%']
            col_widths = ['40%', '6%', '6%', '8%', '6%', '6%', '8%', '6%', '6%', '6%', '6%']
            style = [
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                # ('ALIGN', (2, 0), (2, -1), 'LEFT'),
                # ('ALIGN', (10, 0), (10, -1), 'LEFT'),
                ('FONT', (0, 0), (0, -1), 'Open Sans Bold'),
            ]
            table = lines
            d.insert_table(table=table, colWidths=col_widths,
                           style=style, pagebreak=False)

        d.insert_title_1(text=_("Sumary participantes"), alignment=1)
        d.insert_paragraph("")
        d.insert_paragraph("")
        # calculate
        calculations = {}
        for person in self.persons:
            if person.entity.entity_code in calculations:
                entity = calculations[person.entity.entity_code]
            else:
                entity = {
                    'per_fem': 0,
                    'per_mas': 0,
                    'per_tot': 0,
                    'ind_fem': 0,
                    'ind_mas': 0,
                    'ind_tot': 0,
                    'rel_fem': 0,
                    'rel_mas': 0,
                    'rel_mix': 0,
                    'rel_tot': 0,
                    }
                calculations[person.entity.entity_code] = entity
            if person.gender_id == 'F':
                entity['per_fem'] += 1
            elif person.gender_id == 'M':
                entity['per_mas'] += 1
            entity['per_tot'] += 1

        for inscription in self.inscriptions:
            if inscription.ind_rel == 'I':
                person = inscription.person
                entity_code = inscription.person.entity.entity_code
                if entity_code in calculations:
                    entity = calculations[entity_code]
                else:
                    entity = {
                        'per_fem': 0,
                        'per_mas': 0,
                        'per_tot': 0,
                        'ind_fem': 0,
                        'ind_mas': 0,
                        'ind_tot': 0,
                        'rel_fem': 0,
                        'rel_mas': 0,
                        'rel_mix': 0,
                        'rel_tot': 0,
                        }
                    calculations[entity_code] = entity
                if person.gender_id == 'F':
                    entity['ind_fem'] += 1
                elif person.gender_id == 'M':
                    entity['ind_mas'] += 1
                entity['ind_tot'] += 1
            elif inscription.ind_rel == 'R':
                relay = inscription.relay
                entity_code = inscription.relay.entity.entity_code
                if entity_code in calculations:
                    entity = calculations[entity_code]
                else:
                    entity = {
                        'per_fem': 0,
                        'per_mas': 0,
                        'per_tot': 0,
                        'ind_fem': 0,
                        'ind_mas': 0,
                        'ind_tot': 0,
                        'rel_fem': 0,
                        'rel_mas': 0,
                        'rel_mix': 0,
                        'rel_tot': 0,
                        }
                    calculations[entity_code] = entity
                if relay.gender_id == 'F':
                    entity['rel_fem'] += 1
                elif relay.gender_id == 'M':
                    entity['rel_mas'] += 1
                elif relay.gender_id == 'X':
                    entity['rel_mix'] += 1
                entity['rel_tot'] += 1

        last_entity = None
        entities = sorted(entities, key=attrgetter('entity_code'), reverse=False)
        # col headers
        style = [
            ('FONT', (0, 0), (-1, -1), 'Open Sans Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BACKGROUND', (0, 0), (-1, 0), d.colors.lightgrey)
        ]
        # col_widths = ['100%', ]
        col_widths = ['36%', '20%', '20%', '24%']
        table = [[
            _('Entity'),
            _('Participants'),
            _('Insc. individuals'),
            _('Insc. relays'),
             ], ]
        d.insert_table(
            table=table, colWidths=col_widths,
            style=style, pagebreak=False)

        style = [
            ('FONT', (0, 0), (-1, -1), 'Open Sans Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BACKGROUND', (0, 0), (-1, 0), d.colors.lightgrey)
        ]
        # col_widths = ['100%', ]
        col_widths = ['40%', '6%', '6%', '8%', '6%', '6%', '8%', '6%', '6%', '6%', '6%']
        table = [[
            '',
            _('Fem.'),
            _('Mas.'),
            _('Tot.'),
            _('Fem.'),
            _('Mas.'),
            _('Tot.'),
            _('Fem.'),
            _('Mas.'),
            _('Mix.'),
            _('Tot.'),
             ], ]
        d.insert_table(
            table=table, colWidths=col_widths,
            style=style, pagebreak=False)

        lines = []
        totals = {
                'per_fem': 0,
                'per_mas': 0,
                'per_tot': 0,
                'ind_fem': 0,
                'ind_mas': 0,
                'ind_tot': 0,
                'rel_fem': 0,
                'rel_mas': 0,
                'rel_mix': 0,
                'rel_tot': 0,
                }
        for entity_code, values in calculations.items():

            lines.append([
                self.entities.get_entity_by_code(entity_code).long_name,
                values['per_fem'],
                values['per_mas'],
                values['per_tot'],
                values['ind_fem'],
                values['ind_mas'],
                values['ind_tot'],
                values['rel_fem'],
                values['rel_mas'],
                values['rel_mix'],
                values['rel_tot'],
                ])
                
            totals['per_fem'] += values['per_fem']
            totals['per_mas'] += values['per_mas']
            totals['per_tot'] += values['per_tot']
            totals['ind_fem'] += values['ind_fem']
            totals['ind_mas'] += values['ind_mas']
            totals['ind_tot'] += values['ind_tot']
            totals['rel_fem'] += values['rel_fem']
            totals['rel_mas'] += values['rel_mas']
            totals['rel_mix'] += values['rel_mix']
            totals['rel_tot'] += values['rel_tot']
        else:
            if lines:
                save_lines(lines)
                style = [
                    ('FONT', (0, 0), (-1, -1), 'Open Sans Bold'),
                    ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('BACKGROUND', (0, 0), (-1, 0), d.colors.lightgrey)
                ]
                # col_widths = ['100%', ]
                col_widths = ['40%', '6%', '6%', '8%', '6%', '6%', '8%', '6%', '6%', '6%', '6%']
                table = [[
                    '',
                    totals['per_fem'],
                    totals['per_mas'],
                    totals['per_tot'],
                    totals['ind_fem'],
                    totals['ind_mas'],
                    totals['ind_tot'],
                    totals['rel_fem'],
                    totals['rel_mas'],
                    totals['rel_mix'],
                    totals['rel_tot'],
                    ], ]
                d.insert_table(
                    table=table, colWidths=col_widths,
                    style=style, pagebreak=False)

            # if last_event:
            #     d.insert_page_break()
            # d.insert_paragraph("")
            # last_event = event
            # style = [
            #     ('FONT', (0, 0), (-1, -1), 'Open Sans Bold'),
            #     ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            #     ('FONTSIZE', (0, 0), (-1, -1), 9),
            #     ]
            # col_widths = ['100%', ]

            # table = [["%s. %s" % (event.pos, event.name), ], ]
            # d.insert_table(table=table, colWidths=col_widths,
            #                    style=style, pagebreak=False)
    
            # inscriptions_ind = [i for i in self.inscriptions if i.event == event]
            # inscriptions_ind = sorted(inscriptions_ind, key=attrgetter('equated_hundredth'), reverse=False)
            # lines = []
            # for row in inscriptions_ind:
            #     if row.ind_rel == 'I':
            #         license = row.person.license
            #         name = row.person.full_name
            #         birth_year = row.person.birth_date[2:4]
            #         entity_name = row.person.entity.short_name
            #     elif row.ind_rel == 'R':
            #         license = row.relay.entity.entity_code
            #         name = row.relay.name
            #         birth_year = row.relay.category.name
            #         entity_name = row.relay.entity.short_name
            #     else:
            #         print("Erro")
            #         AssertionError("produciuse un erro")

            #     mark_time = '{} {}{}'.format(
            #         row.mark_time,
            #         row.pool_length,
            #         row.chrono_type)
            #         # pool_chrono = '{}{}'.format(
            #         #     self.pool_length,
            #         #     self.chrono_type)
            #     equated_time = row.equated_time
            #     lines.append([
            #         len(lines) + 1, license, name, birth_year,
            #         entity_name, mark_time, equated_time, row.date, row.venue])
            # else:
            #     if lines:
            #         if event.ind_rel == 'I':
            #             save_lines_ind(lines=lines)
            #         else:
            #             save_lines_rel(lines=lines)
            #         print("rematou bucle")

        d.build_file()
        print("feito")

    def gen_web_forms_files(self):

        # Choices person
        file_name = os.path.join(
                self.config.work_folder_path,
                'choices_person.csv',
                )
        file_path = os.path.join(
            self.config.work_folder_path,
            file_name)
        lines = []
        for person in self.persons:
            # F 00071 BUGALLO PÉREZ, Estíbaliz 1084714
            line = "{} {} {} {}".format(
                person.gender_id,
                person.entity.entity_code,
                "{}, {}".format(person.surname.upper(),
                person.name.title()),
                person.license)
            lines.append((
                line,
                "{}#{}#{}".format(
                    person.gender_id,
                    person.entity.entity_code,
                    person.full_name_normalized
                    )
                ))
        sorted_lines = sorted(lines, key=lambda x:x[1], reverse=False)
        for i in sorted_lines:
            print(i[0])
        sorted_lines = [i[0] for i in sorted_lines]         
        files.set_file_content(content=sorted_lines,
                               file_path=file_path,
                               compress=False,
                               binary=False,
                               encoding='utf-8-sig',
                               end_line="\n")

        # Choices club
        file_name = os.path.join(
                self.config.work_folder_path,
                'choices_club.csv',
                )
        file_path = os.path.join(
            self.config.work_folder_path,
            file_name)
        lines = []
        for entity in self.entities:
            # 00071 Real C. Náutico De Vigo
            lines.append(
                "{} {}".format(
                    entity.entity_code,
                    entity.long_name,
                    )
                )
        sorted_lines = sorted(lines)
        for i in sorted_lines:
            print(i)           
        files.set_file_content(content=sorted_lines,
                               file_path=file_path,
                               compress=False,
                               binary=False,
                               encoding='utf-8-sig',
                               end_line="\n")
        # Choices event
        file_name = os.path.join(
                self.config.work_folder_path,
                'choices_event.csv',
                )
        file_path = os.path.join(
            self.config.work_folder_path,
            file_name)
        lines = []
        for event in self.events:
            # 1. Feminino, 400m Libre
            lines.append(event.long_name)
        # sorted_lines = sorted(lines)
        for i in lines:
            print(i)           
        files.set_file_content(content=lines,
                               file_path=file_path,
                               compress=False,
                               binary=False,
                               encoding='utf-8-sig',
                               end_line="\n")
        print('fin')

    def report_start_list_html(self, phase=None):
        if phase:
            phases = [phase, ]
            file_name = os.path.join(
                self.config.work_folder_path,
                _('start_list_{}.html').format(phase.file_name),
                )
        else:
            phases = self.phases
            file_name = os.path.join(
                self.config.work_folder_path,
                _('start_list_full.html'),
                )
        if self.params.get_value('champ_chrono_type') == 'M':
            chrono_text = _('manual')
        else:
            chrono_text = _('electronic')

        file_path = os.path.join(
            self.config.work_folder_path,
            file_name)
        
        subtitle = _("{}. Pool course {} m. Timing system {}.").format(
            self.params.get_value('champ_venue'),
            self.params.get_value('champ_pool_length'),
            self.params.get_value('champ_chrono_type'),
            )
        
        md = """<!DOCTYPE html>
<html>
<head>
<STYLE><!--
body, table, td {font-family: Arial, helvetica; font-style:normal; font-size: 9pt;}
#f7 {font-family: Arial, helvetica; font-style:normal; font-size: 7pt;}
#f8 {font-family: Arial, helvetica; font-style:normal; font-size: 8pt;}
#f9 {font-family: Arial, helvetica; font-style:normal; font-size: 9pt;}
#f10 {font-family: Arial, helvetica; font-style:normal; font-size: 10t;}
#f11 {font-family: Arial, helvetica; font-style:normal; font-size: 11pt;}
#f12 {font-family: Arial, helvetica; font-style:normal; font-size: 12pt;}
#f13 {font-family: Arial, helvetica; font-style:normal; font-size: 13pt;}
#f14 {font-family: Arial, helvetica; font-style:normal; font-size: 14pt;}
--></STYLE>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title></title>
</head>
<body>
<h1 align=center>%s</h1>\n<p align=center>%s</p>\n""" % (
    self.params.get_value('champ_name'),
    subtitle
    )
        
        def add_phase_title(lines):
            nonlocal md
            md +="""<h2>{}</h2>\n""".format(lines[0][0])

        def add_heat_title(lines):
            nonlocal md
            md +="""\n<h3>{}</h3>\n""".format(lines[0][0])

        def add_result(lines):
            nonlocal md
            rows = ""
            for i in lines:
                rows += """
        <tr>
            <td align=right width=3%>{}</td>
            <td align=center width=8%>{}</td>
            <td align=left width=37%><b>{}</b></td>
            <td align=center width=4%>{}</td>
            <td align=left width=16%>{}</td>
            <td align=right width=8%>{}</td>
            <td align=right width=4%>{}</td>
            <td align=right width=10%>{}</td>
        </tr>
        """.format(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])
            md +="""
<table width="100%">
{}
</table>
""".format(rows)

        def add_relay_members(lines):
            print(lines)
            print(lines)

        for phase in phases:
            # FIXME: poñer isto na clase phase
            phase_title = '{}.- {} ({})'.format(phase.event.pos, phase.event.name, phase.progression)
            add_phase_title([[phase_title], ])
            count_heats = len(phase.heats)
            inscriptions =  phase.inscriptions
            for heat in phase.heats:
                heat_title = _('Heat {} of {}').format(heat.pos, count_heats)
                add_heat_title([[heat_title], ])
                for result in heat.results:
                    time_start_list = result.inscription.mark_time
                    insc_properties = '{}{}'.format(
                        result.inscription.pool_length,
                        result.inscription.chrono_type)
                    equated_time = result.equated_time
                    line_result = [[
                            str(result.lane), 
                            'X' not in result.event.code.upper() and result.person.license or result.relay.entity.entity_code, 
                            'X' not in result.event.code.upper() and result.person.full_name or result.relay.name, 
                            'X' not in result.event.code.upper() and result.person.year[2:] or "", 
                            'X' not in result.event.code.upper() and result.person.entity.short_name or result.relay.entity.short_name, 
                            time_start_list, insc_properties, equated_time],]
                    add_result(line_result)
                    if result.ind_rel == 'R':
                        if not result.relay.relay_members:
                            result.relay.relay_members.load_items_from_dbs()
                        members = '; '.join([i.person.full_name for i in result.relay.relay_members])
                        print(members)
                        if members:
                            add_relay_members([[members], ])
        md += """</body>\n</html>"""
        files.set_file_content(content=md,
                               file_path=file_path,
                               compress=False,
                               binary=False,
                               encoding='utf-8-sig',
                               end_line="\n")
        print('fin')

    def report_start_list_pdf(self, phase=None):
        if phase:
            phases = [phase, ]
            file_name = _('start_list_{}.pdf').format(phase.file_name)
        else:
            phases = self.phases
            file_name = _('start_list_full.pdf')
        d = self.init_report(file_name=file_name)

        for phase in phases:
            phase.report_start_list_pdf(d=d)
        d.build_file()
        print('fin')

    def import_insc_from_file(self, file_path):
        print(file_path)
        lines = get_file_content(file_path=file_path,
                                            mode="csv",
                                            compressed=False,
                                            encoding='utf-8-sig')
        if not lines:
            print("O ficheiro está baleiro!!")
            raise ValueError("O ficheiro está baleiro!!")
            

        start_line = 1
        for pos, i in enumerate(lines):
            if i[0]== 'RFEN ID':
                start_line = pos + 1
                break

        (LICENSE, SURNAME, NAME, GENDER_ID, BIRTH_DATE, ENTITY_CODE,
        ENTITY_NAME, EVENT_POS, EVENT_CODE, MARK_TIME, POOLCHRONO) = range(11)
        for i in lines[start_line:]:
            license = i[LICENSE]
            person = self.persons.get_person_by_license(license=i[LICENSE])
            if person:
                print("This person {} already exists.".format(person.full_name))
            else:
                # add person
                entity = self.entities.get_entity_by_code(entity_code=i[ENTITY_CODE])
                if entity:
                    print("This entity {} already exists.".format(entity.code))
                else:
                    # add entity
                    entity = self.entities.item_blank
                    entity.entity_code = i[ENTITY_CODE]
                    entity.short_name = i[ENTITY_NAME]
                    entity.medium_name = i[ENTITY_NAME]
                    entity.long_name = i[ENTITY_NAME]
                    # FIXME: revisar que garde o código da entidade cando se importa de csv
                    entity.save()
                person = self.persons.item_blank
                person.license = i[LICENSE]
                person.surname = i[SURNAME]
                person.name = i[NAME]
                person.gender_id = i[GENDER_ID]
                person.birth_date = i[BIRTH_DATE]
                person.entity = entity
                person.save()
            event = self.events[int(i[EVENT_POS]) - 1]
            if event.code != i[EVENT_CODE]:
                print("This event {}.- {} not exists.".format(i[EVENT_POS], i[EVENT_CODE]))
            else:
                
                inscriptions = event.inscriptions
                inscriptions.load_items_from_dbs()
                # if not self.check_exists(person=person, event=event):
                exists_inscription = False
                for j in inscriptions:
                    if j.person == person and j.event == event:
                        exists_inscription = True
                        break
                if exists_inscription:
                    # add inscription
                    print('Inscription already exists.')
                else:
                    print('add inscription')
                    if len(i[POOLCHRONO]) == 3:
                        pool_length = int(i[POOLCHRONO][:2])
                        chrono_type = i[POOLCHRONO][2].upper()
                    else:
                        pool_length = 0
                        chrono_type = ''
                    inscription = inscriptions.item_blank
                    inscription.person = person
                    inscription.mark_time = i[MARK_TIME]
                    inscription.pool_length = pool_length
                    inscription.chrono_type = chrono_type
                    inscription.date = ''
                    inscription.venue = ''
                    inscription.save()
            print(i)
        return True