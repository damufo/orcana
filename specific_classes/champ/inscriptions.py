# -*- coding: utf-8 -*-


import os
from operator import itemgetter, attrgetter
# from specific_classes.report_base import ReportBase
#from specific_classes.conversions import Conversions
from specific_classes.champ.inscription import Inscription
# from specific_functions import times
# from specific_functions import files


class Inscriptions(list):

    def __init__(self, **kwargs):
        '''
        Constructor
        '''
        self.event = kwargs['event']
        self.config = self.event.config

        # self.event = None

        # This is for inscriptions form calculation
        self.calc_pool_length = False
        self.calc_licenses_renewed = False

#         self.conversions = Conversions(config=self.config,
#                                        equate_pool_length=self.pool_length,
#                                        equate_chrono_type=self.chrono_type)
        self.sort_reverse = False
        self.sort_last_field = None

        
    @property
    def champ(self):
        return self.event.champ

    @property
    def champ_id(self):
        return self.champ.id

    @property
    def activity_id(self):
        return self.champ.activity_id

    @property
    def estament_id(self):
        return self.champ.estament_id

    @property
    def scope_id(self):
        return self.champ.scope_id

    @property
    def pool_length(self):
        return self.champ.pool_length

    @property
    def chrono_type(self):
        return self.champ.chrono_type

    @property
    def results_from_date(self):
        return self.champ.results_from_date

    @property
    def results_to_date(self):
        return self.champ.results_to_date

    @property
    def item_blank(self):
        return Inscription(
            inscriptions=self,
            id=0,
            pool_length=0,
            chrono_type='',
            mark_hundredth=354000,
            date_time='',
            venue='',
            event_id=0,
            person_id=0,
            )

    @property
    def champs(self):
        return self.champ.champs

    def delete_items(self, idxs):
        for idx in sorted(idxs, reverse=True):
            self.delete_item(idx)

    def delete_item(self, idx):
        inscription = self[idx]
        sql =  ("delete from inscriptions where inscription_id=?")
        values = ((inscription.inscription_id, ), )
        self.config.dbs.exec_sql(sql=sql, values=values)
        sql =  ("delete from inscriptions_members where inscription_id=?")
        values = ((inscription.inscription_id, ), )
        self.config.dbs.exec_sql(sql=sql, values=values)
        self.pop(idx) #remove element from list

    # def get_last_relay_club_id(self, event_id, club_id):
    #     # Get last relay club id
    #     person_id = ""
    #     for i in self:
    #         if i.club_id == club_id and i.event.id == event_id:
    #             if i.person_id > person_id: 
    #                 person_id = i.person_id
    #     if person_id:
    #         last_value = int(person_id[5:])
    #     else:
    #         last_value = 1
    #     return last_value

#     def load_items_from_server(self, only_my=True, event_id=0):
#         '''
#         Load items from server
#         '''
#         query = """
#    query($champId: Int!, $onlyMy: Boolean!, $eventId: Int!) {
#   inscriptions (champId: $champId, onlyMy: $onlyMy, eventId: $eventId) {
#     id personId surname name genderId birthDate clubId poolId chronoId
#     markHundredth xdate venue typeId createdAt createdBy updatedAt updatedBy
#     event { id }
#     } } """
#         variables = {
#             "champId": self.champ.id,
#             "onlyMy": only_my,
#             "eventId": event_id,
#         }
#         del self[:]  # borra o que haxa
#         result = self.config.com_api.execute(query, variables)
#         if result:
#             for i in result["data"]["inscriptions"]:
#                 self.append(Inscription(
#                     inscriptions=self,
#                     id=(i["id"]),
#                     person_id=(i["personId"]),
#                     surname=(i["surname"]),
#                     name=(i["name"]),
#                     gender_id=i["genderId"],
#                     birth_date=i["birthDate"],
#                     club_id=i["clubId"],
#                     pool_length=i["poolId"],
#                     chrono_type=i["chronoId"],
#                     mark_hundredth=i["markHundredth"],
#                     xdate=i["xdate"],
#                     venue=i["venue"],
#                     type_id=i["typeId"],
#                     created_at=i["createdAt"],
#                     created_by=i["createdBy"],
#                     updated_at=i["updatedAt"],
#                     updated_by=i["updatedBy"],
#                     event_id=i["event"]["id"],
#                     save_action='U'))

    def load_items_from_dbs(self, event_id):
        del self[:]  # borra os elementos que haxa
        sql = '''
select inscription_id, pool_length, chrono_type, mark_hundredth,
equated_hundredth, date_time, venue, event_id, person_id, relay_id
from inscriptions where event_id={} order by equated_hundredth '''
        sql = sql.format(event_id)

        res = self.config.dbs.exec_sql(sql=sql)
        (INSCRIPTION_ID, POOL_LENGTH, CHRONO_TYPE, MARK_HUNDREDTH,
EQUATED_HUNDREDTH, DATE_TIME, VENUE, EVENT_ID, PERSON_ID, RELAY_ID) = range(10)
        for i in res:
            person = self.champ.persons.get_person(i[PERSON_ID])
            relay = self.champ.relays.get_relay(i[RELAY_ID])
            event = self.champ.events.get_event(i[EVENT_ID])
            self.append(Inscription(
                    inscriptions=self,
                    inscription_id=i[INSCRIPTION_ID],
                    pool_length=i[POOL_LENGTH],
                    chrono_type=i[CHRONO_TYPE],
                    mark_hundredth=i[MARK_HUNDREDTH],
                    equated_hundredth=i[EQUATED_HUNDREDTH],
                    date_time=i[DATE_TIME],
                    venue=i[VENUE],
                    event=event,
                    person=person,
                    relay=relay,
                    ))

    # @property
    # def list_fields(self):
    #     """
    #     list fields for form show
    #     (name as text, align[L:left, C:center, R:right] as text,
    #             width as integer)
    #     """
    #     return ((_('N.'), 'C', 35), (_('Event'), 'C', 70),
    #             (_('Gender'), 'C', 60),
    #             (_('Category'), 'C', 60), (_('Name'), 'L', 240),
    #             (_('Ind/Rel'), 'C', 55),
    #             (_('Inscribed'), 'C', 65))

    # @property
    # def list_values(self):
    #     """
    #     list values for form show
    #     """
    #     values = []
    #     for x, i in enumerate(self, 1):
    #         values.append((
    #                        x,
    #                        i.event_id,
    #                        i.gender_id,
    #                        i.category_id,
    #                        i.name,
    #                        i.ind_rel,
    #                        i.count_inscriptions))
    #     return tuple(values)

    @property
    def list_fields(self):
        """
        list fields for form show
        (name as text, align[L:left, C:center, R:right] as text,
                width as integer)
        """
        return (
                (_('License'), 'C', 80),
                (_('Name'), 'L', 200),
                (_('Gender'), 'C', 40),
                (_('Year'), 'C', 80),
                (_('Club'), 'L', 60),
                (_('Pool'), 'C', 40),
                (_('Chrono'), 'C', 40),
                (_('Mark'), 'R', 65),
                (_('Equated'), 'R', 65),
                (_('Date'), 'C', 75),
                (_('Venue'), 'L', 100),
                )

    @property
    def list_values(self):
        """
        list values for form show
        """
        values = []
        for i in self:
            if i.person:
                values.append((
                    i.person.license,
                    '{}, {}'.format(i.person.surname.upper(), i.person.name),
                    i.person.gender_id,
                    i.person.birth_date[:4],
                    i.person.entity.short_name,
                    i.pool_length,
                    i.chrono_type,
                    i.mark_time,
                    i.equated_time,
                    i.date_time,
                    i.venue,
                    ))
            elif i.relay:
                values.append((
                    # i.relay.license,
                    # '{}, {}'.format(i.relay.surname.upper(), i.person.name),
                    i.person.gender_id,
                    i.person.birth_date[:4],
                    i.person.entity.short_name,
                    i.pool_length,
                    i.chrono_type,
                    i.mark_time,
                    i.equated_time,
                    i.date_time,
                    i.venue,
                    ))
        return tuple(values)

    def list_sort(self, **kwargs):
        '''
        Sort results by column num or column name
        '''
        field = None
        cols = (
            'event.pos',
            'person_id',
            'surname',
            'name',
            'gender_id',
            'birth_date',
            'club_desc',
            'pool_length',
            'chrono_type',
            'mark_hundredth',
            'equated_hundredth',
            'xdate',
            'venue',
            'type_id'
            )
        # cols valid to order
        order_cols = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)


        if 'num_col' in list(kwargs.keys()):
            if kwargs['num_col'] in order_cols:
                field = cols[kwargs['num_col']]

        if self.sort_last_field == field:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_reverse = False
        if field:
            self.sort_by_field(field=field, reverse=self.sort_reverse)
            self.sort_last_field = field

    def sort_by_field(self, field, reverse=False):
        self_sort = sorted(self, key=attrgetter(field), reverse=reverse)
        del self[:]
        self.extend(self_sort)

    def report(self, file_path, only_my):

        d = ReportBase(config=self.config,
                       file_name=file_path,
                       orientation='landscape',
                       title=_("INSCRIPTIONS REPORT"))

        d.insert_title_1(text=_("By club"), alignment=1)

        lines = [
            ["", "", ""],
            [_("Champ. name: {}").format(self.champ.name),
             _("Champ. ID: {}").format(self.champ.id),
             _("Timestamp: {}").format(self.config.timestamp)],
            [_("Entity: {} {}").format(self.config.entity.entity_id,
                                   self.config.entity.long_desc),
             _("Chronometer: {}").format(self.chrono_type),
             _("Pool length: {}").format(self.pool_length)],
            ["", "", ""]]
        style = [
            ('FONTSIZE', (0, 0), (-1, -1), 9)
            ]

        col_widths = ['50%', '25%', '25%']
        d.insert_table(table=lines, colWidths=col_widths,
                       style=style, pagebreak=False)

        entity = self.config.entity

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
            if inscription.type_id == 'S':  # engade compoñentes
                col_widths = ['6%', '9%', '20%', '6%', '5%',
                              '8%', '8%', '7%', '8%', '9%', '15%']
                style = [
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('GRID', (0, 0), (-1, -1), 0.5, d.colors.grey),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                    ('ALIGN', (2, 0), (2, -1), 'LEFT'),
                    ('ALIGN', (10, 0), (10, -1), 'LEFT'),
                ]

                inscription.insc_members.load_items_from_server()
                lines = []
                for i in inscription.insc_members:
                    mark_time = times.int2time(i.mark_hundredth)
                    equated_time = times.int2time(i.equated_hundredth)
                    lines.append([
                        i.event_code, i.person_id,
                        '%s, %s' % (i.surname, i.name),
                        i.birth_date[:4], i.gender_id,
                        mark_time, '%sm' % i.pool_length, i.chrono_type,
                        equated_time, i.xdate, i.venue],)
                table = lines
                d.insert_paragraph(_('Members:'))
                d.insert_table(table=table, colWidths=col_widths, 
                               style=style, pagebreak=False)

        # inscriptions ordena por clube, tipo, apelidos, nome, proba
        inscriptions = sorted(self, key=attrgetter('event.pos'), reverse=False)
        inscriptions = sorted(inscriptions, key=attrgetter('name'), reverse=False)
        inscriptions = sorted(inscriptions, key=attrgetter('surname'), reverse=False)
        inscriptions = sorted(inscriptions, key=attrgetter('type_id_sort'), reverse=False)
        inscriptions = sorted(inscriptions, key=attrgetter('type_id_sort'), reverse=False)
        inscriptions = sorted(inscriptions, key=attrgetter('club_id'), reverse=False)

        lines = []
        person_id = None
        prev_row = None
        last_club_id = None
        for row in inscriptions:
            # if entity.is_federation or row.club_id == entity.entity_id:
            if row.person_id != person_id or prev_row.type_id == 'S':
                if lines:
                    save_table(lines=lines, inscription=prev_row)
                    d.insert_paragraph("")
                person_id = row.person_id
                lines = []
                style = [
                    ('FONT', (0, 0), (-1, -1), 'Open Sans Bold'),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                ]
                col_widths = ['100%', ]

                if last_club_id != row.club_id:  # pagebreak
                    if last_club_id:
                        d.insert_page_break()

                    last_club_id = row.club_id
                    club = self.config.clubs.get_club(row.club_id)

                    style = [
                        ('FONT', (0, 0), (-1, -1), 'Open Sans Bold'),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTSIZE', (0, 0), (-1, -1), 9),
                        ('BACKGROUND', (0, 0), (-1, 0), d.colors.lightgrey)
                    ]
                    col_widths = ['100%', ]

                    table = [["%s %s" % (
                        club.club_id, club.long_desc), ], ]
                    d.insert_table(
                        table=table, colWidths=col_widths,
                        style=style, pagebreak=False)

                style = [
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                ]
                col_widths = ['100%', ]

                if row.type_id == 'I':
                    table = [
                        ["%s %s, %s (%s)" % (
                            row.person_id, row.surname, 
                            row.name, row.birth_date[:4]),],]
                else:
                    table = [
                        ["%s %s" % (
                            row.person_id, row.surname),],]

                d.insert_table(
                    table=table, colWidths=col_widths,
                    style=style, pagebreak=False)
            mark_time = times.int2time(row.mark_hundredth)
            equated_time = times.int2time(row.equated_hundredth)
            lines.append([
                row.event.pos, row.event.name, row.category.code,
                mark_time, '%sm' % row.pool_length, row.chrono_type,
                equated_time, row.xdate, row.venue],)
            prev_row = row

        else:
            if lines:
                save_table(lines=lines, inscription=prev_row)
                print("rematou bucle") 


        d.insert_page_break()
        d.insert_title_1(text=_("By event"), alignment=1)

        lines = [
            ["", "", ""],
            [
                _("Champ. name: {}").format(self.champ.name),
                _("Champ. ID: {}").format(self.champ.id),
                _("Timestamp: {}").format(self.config.timestamp)
            ],
            [
                _("Entity: {} {}").format(self.config.entity.entity_id,
                                      self.config.entity.long_desc),
                _("Chronometer: {}").format(self.chrono_type),
                _("Pool length: {}").format(self.pool_length)
            ],
            ["", "", ""]]
        style = [
            ('FONTSIZE', (0, 0), (-1, -1), 9)]

        col_widths = ['50%', '25%', '25%']

        d.insert_table(table=lines, colWidths=col_widths,
                       style=style, pagebreak=False)

        def save_lines(lines):

            col_widths = ['4%', '8%', '24%', '5%', '10%', '8%', '7%', '7%', '7%', '8%', '12%']
            style = [
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (2, 0), (2, -1), 'LEFT'),
                ('ALIGN', (10, 0), (10, -1), 'LEFT'),
            ]

            table = lines
            d.insert_table(table=table, colWidths=col_widths,
                           style=style, pagebreak=False)

        # inscriptions ordena por proba e por tempo
        inscriptions = sorted(self, key=attrgetter('mark_hundredth'), reverse=False)
        inscriptions = sorted(inscriptions, key=attrgetter('event.pos'), reverse=False)

        lines = []
        last_pos = None
        for row in inscriptions:
            if row.event.pos != last_pos:
                if lines:
                    save_lines(lines=lines)
                    lines = []
                    d.insert_page_break()

                style = [
                    ('FONT', (0, 0), (-1, -1), 'Open Sans Bold'),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                ]
                col_widths = ['100%', ]

                table = [["{}. {}".format(row.event.pos, row.event.name), ], ]
                d.insert_table(table=table, colWidths=col_widths,
                               style=style, pagebreak=False)

            if row.type_id == 'I':
                name = "{}, {}".format(row.surname, row.name)
                birth_date = row.birth_date[:4]
            else:
                name = "{}".format(row.surname)
                birth_date = ''

            mark_time = times.int2time(row.mark_hundredth)
            equated_time = times.int2time(row.equated_hundredth)  

            club = self.config.clubs.get_club(row.club_id)

            lines.append([
                len(lines)+1, row.person_id, name, birth_date,
                club.short_desc,
                mark_time, '{}m'.format(row.pool_length), row.chrono_type,
                equated_time, row.xdate, row.venue])

            last_pos = row.event.pos
        else:
            if lines:
                save_lines(lines=lines)
                print("rematou bucle")


        d.insert_page_break()
        d.insert_title_1(text=_("Reserves and only relay"), alignment=1)

        lines = [
            ["", "", ""],
            [
                _("Champ. name: {}").format(self.champ.name),
                _("Champ. ID: {}").format(self.champ.id),
                _("Timestamp: {}").format(self.config.timestamp)
            ],
            [
                _("Entity: {} {}").format(self.config.entity.entity_id,
                                      self.config.entity.long_desc),
                _("Chronometer: {}").format(self.chrono_type),
                _("Pool length: {}").format(self.pool_length)
            ],
            ["", "", ""]]
        style = [
            ('FONTSIZE', (0, 0), (-1, -1), 9)]

        col_widths = ['50%', '25%', '25%']

        d.insert_table(table=lines, colWidths=col_widths,
                       style=style, pagebreak=False)




        # reserves ordena por apelidos e por nome
        self.champ.reserves.load_items_from_server(only_my=only_my)
        reserves = sorted(self.champ.reserves, key=attrgetter(
            'surname_normalized', 'name_normalized'), reverse=False)
        # reserves = sorted(reserves, key=attrgetter('event.pos'), reverse=False)

        lines = []
        for pos, row in enumerate(reserves, 1):
            name = "%s, %s" % (row.surname, row.name)
            birth_date = row.birth_date[:4]

            lines.append([
                pos, row.person_id, name, row.gender_id, birth_date,
                row.club_id, row.club_desc, ' '])

        col_widths = ['4%', '8%', '24%', '5%', '5%', '5%', '10%', '39%']
        style = [
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (2, 0), (2, -1), 'LEFT'),
        ]

        table = lines
        d.insert_table(
            table=table, colWidths=col_widths, style=style, pagebreak=False)

        d.build_file()
        print("feito")

    def report_old(self, file_path):

        d = ReportBase(config=self.config,
                       file_name=file_path,
                       orientation='landscape',
                       title=_("INSCRIPTIONS REPORT"))

        d.insert_title_1(text=_("By club"), alignment=1)

        lines = [
            ["", "", ""],
            [_("Champ. name: {}").format(self.champ.name),
             _("Champ. ID: {}").format(self.champ.id),
             _("Timestamp: {}").format(self.config.timestamp)],
            [_("Entity: {} {}").format(self.config.entity.entity_id,
                                    self.config.entity.long_desc),
             _("Chronometer: {}").format(self.chrono_type),
             _("Pool length: {}").format(self.pool_length)],
            ["", "", ""]]
        style = [
                     ('FONTSIZE', (0, 0), (-1, -1), 9)]

        col_widths = ['50%', '25%', '25%']
        d.insert_table(table=lines, colWidths=col_widths,
                       style=style, pagebreak=False)

        sql = '''
select ci.type_id, ci.event_id, ci.gender_id, ci.category_id, ci.person_id, ci.club_id, ci.pool_length, ci.chrono_type, 
    ci.mark_hundredth, ci.equated_hundredth, ci.xdate, ci.venue, ci.surname, ci.name, ci.birth_date, ce.name, ce.pos
from champ_inscriptions ci inner join champ_events ce on ci.champ_id=ce.champ_id 
and ci.event_id=ce.event_id and ci.category_id=ce.category_id and case  when ce.gender_id<>"X" then ci.gender_id=ce.gender_id else 1 end
where ci.champ_id="%s" %s  and ci.inscribed=1 and type_id in ("I", "R", "S")
order by ci.club_id, 
  CASE ci.type_id
    WHEN "I" THEN 0
    WHEN "R" THEN 1
    WHEN "S" THEN 1
  END,
    ci.surname, ci.name, ci.person_id, ce.pos '''

        entity = self.config.entity

        if entity.is_federation:
            where_club_id = ''
        else:
            where_club_id = ' and ci.club_id="{}" '.format(entity.entity_id)
        sql = sql % (self.champ_id, where_club_id)

        rows = self.config.dbs.exec_sql(sql=sql)
        (TYPE_ID, EVENT_ID, GENDER_ID, CATEGORY_ID, PERSON_ID, CLUB_ID, pool_length, 
                chrono_type, MARK_HUNDREDTH, EQUATED_HUNDREDTH, XDATE, VENUE, SURNAME, 
                NAME, BIRTH_DATE, E_NAME, E_POS) = list(range(17))


        def save_table(lines, champ_id, event_id, gender_id, category_id, 
                                                person_id, type_id, ):
            col_widths = ['7%', '22%', '10%', '10%', '8%', '7%', '10%', '11%', '15%']
            style = [
                        ('FONTSIZE',(0,0),(-1,-1), 9),
                        ('GRID',(0,0),(-1,-1),0.5, d.colors.grey),
                        ('ALIGN',(0,0),(-1,-1), 'CENTER'),
                        ('ALIGN',(0,0),(0,-1), 'RIGHT'),
                        ('ALIGN',(1,0),(1,-1), 'LEFT'),
                        ('ALIGN',(8,0),(8,-1), 'LEFT'),
#                         ('BACKGROUND', (0, 0), (-1, 0), d.colors.lightgrey)
                        ]

            table = lines
            d.insert_table(table=table, colWidths=col_widths, 
                           style=style, pagebreak=False)
            if type_id == 'S':  # engade compoñentes
                print("integrantes")

                gender_sql = ''
                if gender_id != 'X':
                    gender_sql = 'and gender_id="{}"'.format(gender_id)
                sql = '''
select member_event_id, member_person_id, surname, name, member_gender_id, birth_date,
club_id, pool_length, chrono_type, mark_hundredth, equated_hundredth, xdate, venue from champ_inscriptions 
where champ_id=? and event_id=? %s and category_id=? and person_id=? 
and type_id="M" '''
                sql = sql % gender_sql
                values = ((champ_id, event_id, category_id,person_id),)
                res = self.config.dbs.exec_sql(sql=sql, values=values)

                col_widths = ['6%', '9%', '20%', '6%', '5%', '8%', '8%', '7%', '8%', '9%', '15%']
                style = [
                        ('FONTSIZE',(0,0),(-1,-1), 9),
                        ('GRID',(0,0),(-1,-1),0.5, d.colors.grey),
                        ('ALIGN',(0,0),(-1,-1), 'CENTER'),
                        ('ALIGN',(0,0),(0,-1), 'RIGHT'),
                        ('ALIGN',(2,0),(2,-1), 'LEFT'),
                        ('ALIGN',(10,0),(10,-1), 'LEFT'),
#                         ('BACKGROUND', (0, 0), (-1, 0), d.colors.lightgrey)
                        ]
                (MEMBER_EVENT_ID, MEMBER_PERSON_ID, SURNAME, NAME, MEMBER_GENDER_ID, 
                        BIRTH_DATE, CLUB_ID, pool_length, chrono_type, MARK_HUNDREDTH,
                        EQUATED_HUNDREDTH,
                        XDATE, VENUE) = list(range(13))
                lines = []
                for i in res:
                    mark_time = times.int2time(i[MARK_HUNDREDTH])
                    equated_time = times.int2time(i[EQUATED_HUNDREDTH])
                    lines.append([
                          i[MEMBER_EVENT_ID], i[MEMBER_PERSON_ID], 
                          '{}, {}'.format(i[SURNAME], i[NAME]),
                          i[BIRTH_DATE][:4], i[MEMBER_GENDER_ID],
                          mark_time, '{}m'.format(i[pool_length]), i[chrono_type], 
                          equated_time, i[XDATE], i[VENUE]],)
                table = lines
                d.insert_paragraph(_('Members:'))
                d.insert_table(table=table, colWidths=col_widths, 
                               style=style, pagebreak=False)

        lines = []
        person_id = None
        prev_row = None
        last_club_id = None
        for row in rows:
            if row[PERSON_ID] != person_id:
                if lines:
                    save_table(lines=lines, champ_id = self.champ_id,
                                    event_id = prev_row[EVENT_ID],
                                    gender_id = prev_row[GENDER_ID],
                                    category_id = prev_row[CATEGORY_ID],
                                    person_id = prev_row[PERSON_ID],
                                    type_id = prev_row[TYPE_ID])
                    d.insert_paragraph("")
                person_id = row[PERSON_ID]
                lines = []
                style = [
                            ('FONT',(0,0),(-1,-1), 'Open Sans Bold'), 
                            ('ALIGN',(0,0),(-1,-1), 'LEFT'),
                            ('FONTSIZE',(0,0),(-1,-1), 9),
                        ]
                col_widths = ['100%',]
                
                
                if last_club_id != row[CLUB_ID]:  # pagebreak
                    if last_club_id:
                        d.insert_page_break()

                    last_club_id = row[CLUB_ID]
                    club = self.config.clubs.get_club(row[CLUB_ID])

                    style = [
                                ('FONT',(0,0),(-1,-1), 'Open Sans Bold'), 
                                ('ALIGN',(0,0),(-1,-1), 'LEFT'),
                                ('FONTSIZE',(0,0),(-1,-1), 9),
                                ('BACKGROUND', (0, 0), (-1, 0), d.colors.lightgrey)
                            ]
                    col_widths = ['100%',]

                    table = [[ "{} {}".format(club.club_id, club.long_desc),],]
                    d.insert_table(table=table, colWidths=col_widths, 
                               style=style, pagebreak=False)
                
                style = [
#                             ('FONT',(0,0),(-1,-1), 'Open Sans'), 
                            ('ALIGN',(0,0),(-1,-1), 'LEFT'),
                            ('FONTSIZE',(0,0),(-1,-1), 9),
                        ]
                col_widths = ['100%',]
                
                
                if row[TYPE_ID] == 'I':
                    table = [[ "{} {}, {} ({})".format(row[PERSON_ID], row[SURNAME], 
                                              row[NAME], row[BIRTH_DATE][:4]),],]
                else:
                    table = [[ "{} {}".format(row[PERSON_ID], row[SURNAME]),],]

                d.insert_table(table=table, colWidths=col_widths, 
                               style=style, pagebreak=False)
            mark_time = times.int2time(row[MARK_HUNDREDTH])
            equated_time = times.int2time(row[EQUATED_HUNDREDTH])
            lines.append([
                          row[E_POS]+1, row[E_NAME], row[CATEGORY_ID], 
                          mark_time, '{}m'.format(row[pool_length]), row[chrono_type], 
                          equated_time, row[XDATE], row[VENUE]],)
            prev_row = row

        else:
            if lines:
                save_table(lines=lines, champ_id = self.champ_id,
                                    event_id = prev_row[EVENT_ID],
                                    gender_id = prev_row[GENDER_ID],
                                    category_id = prev_row[CATEGORY_ID],
                                    person_id = prev_row[PERSON_ID],
                                    type_id = prev_row[TYPE_ID])
                print("rematou bucle") 


        d.insert_page_break()
        d.insert_title_1(text=_("By event"), alignment=1)
        
        lines = [
            ["", "", ""],
            [
            _("Champ. name: {}").format(self.champ.name), 
            _("Champ. ID: {}").format(self.champ.id),             
            _("Timestamp: {}").format(self.config.timestamp)
            ],
            [
            _("Entity: {} {}").format(self.config.entity.entity_id, self.config.entity.long_desc),
            _("Chronometer: {}").format(self.chrono_type), 
            _("Pool length: {}").format(self.pool_length)
            ],
            ["", "", ""]]
        style = [
                     ('FONTSIZE',(0,0),(-1,-1), 9)]

        col_widths = ['50%', '25%', '25%']
        
        d.insert_table(table=lines, colWidths=col_widths, 
                       style=style, pagebreak=False)
        
                    
        sql = '''
select ci.type_id, ci.event_id, ci.gender_id, ci.category_id, ci.person_id, ci.club_id, ci.pool_length, ci.chrono_type, 
    ci.mark_hundredth, ci.equated_hundredth, ci.xdate, ci.venue, ci.surname, ci.name, ci.birth_date, ce.name, ce.pos
from champ_inscriptions ci inner join champ_events ce on ci.champ_id=ce.champ_id 
and ci.event_id=ce.event_id and ci.category_id=ce.category_id and case  when ce.gender_id<>"X" then ci.gender_id=ce.gender_id else 1 end
where ci.champ_id="%s" %s and ci.inscribed=1 and type_id in ("I", "R", "S")
order by ce.pos, ci.equated_hundredth '''
        sql = sql % (self.champ_id, where_club_id) 
        rows = self.config.dbs.exec_sql(sql=sql)
        (TYPE_ID, EVENT_ID, GENDER_ID, CATEGORY_ID, PERSON_ID, CLUB_ID, pool_length, 
                chrono_type, MARK_HUNDREDTH, EQUATED_HUNDREDTH, XDATE, VENUE, SURNAME, 
                NAME, BIRTH_DATE, E_NAME, E_POS) = list(range(17))


        def save_lines(lines):
            
            col_widths = ['4%', '8%', '24%', '5%', '10%', '8%', '7%', '7%', '7%', '8%', '12%']
            style = [
                    ('FONTSIZE',(0,0),(-1,-1), 9),
#                     ('GRID',(0,0),(-1,-1),0.5, d.colors.grey),
                    ('ALIGN',(0,0),(-1,-1), 'CENTER'),
                    ('ALIGN',(0,0),(0,-1), 'RIGHT'),
                    ('ALIGN',(2,0),(2,-1), 'LEFT'),
                    ('ALIGN',(10,0),(10,-1), 'LEFT'),
#                    ('BACKGROUND', (0, 0), (-1, 0), d.colors.lightgrey)
                    ]
             
            table = lines
            d.insert_table(table=table, colWidths=col_widths, 
                           style=style, pagebreak=False)

        lines = []
        last_pos = None
        for row in rows:
            if row[E_POS] != last_pos:
                if lines:
                    save_lines(lines=lines)
                    lines = []
#                     d.insert_page_break()        
                
                style = [
                            ('FONT',(0,0),(-1,-1), 'Open Sans Bold'), 
                            ('ALIGN',(0,0),(-1,-1), 'LEFT'),
                            ('FONTSIZE',(0,0),(-1,-1), 9),
                        ]
                col_widths = ['100%',]
                                
                table = [[ "{}. {}".format(row[E_POS]+1, self[row[E_POS]].name),],]
                d.insert_table(table=table, colWidths=col_widths, 
                           style=style, pagebreak=False) 
                                    
            
            if row[TYPE_ID] == 'I':
                name =  "{}, {}".format(row[SURNAME], row[NAME])
                birth_date = row[BIRTH_DATE][:4]
            else:
                name =  "{}".format(row[SURNAME])
                birth_date = ''
            
            mark_time = times.int2time(row[MARK_HUNDREDTH])
            equated_time = times.int2time(row[EQUATED_HUNDREDTH])  

            club = self.config.clubs.get_club(row[CLUB_ID])
    
            lines.append([
                        len(lines)+1, row[PERSON_ID], name, birth_date,
                        club.short_desc,
                        mark_time, '%sm' % row[pool_length], row[chrono_type], 
                        equated_time, row[XDATE], row[VENUE]])

            
            
            last_pos = row[E_POS]
        else:
            if lines:
                save_lines(lines=lines)
                print("rematou bucle") 

        d.build_file()
        print("feito")
                
 
    def check_insc_max_person(self):
        
        champ_id = self.champ_id
        insc_max_person = self.champ.insc_max_person
        
        #  Check maximum inscriptions by person
        sql = '''
Select person_id, surname, name, event_id, gender_id, category_id 
from champ_inscriptions where champ_id=? and inscribed=1 and 
person_id in (select person_id from champ_inscriptions where champ_id=? 
    and inscribed=1 and upper(event_id) not like '%X%' 
    group by person_id having count(*)>?)
order by surname, name, birth_date, event_id '''
        values = ((champ_id, champ_id, insc_max_person),)
        rows = self.config.dbs.exec_sql(sql=sql, values=values)
        PERSON_ID, SURNAME, NAME, EVENT_ID, GENDER_ID, CATEGORY_ID = list(range(6))
        message = ''
        person_id = None
        for i in rows:
            if person_id != i[PERSON_ID]:
                if message:
                    message += '\n'
                message += '{}, {}: '.format(i[SURNAME], i[NAME])
                events = None
                person_id = i[PERSON_ID]
            
            if events:
                message += ', {}'.format(i[EVENT_ID])
            else:
                events = True
                message += '{}'.format(i[EVENT_ID])
        if message:
            message=_('People with excess events:\n{}').format(message)
        return message
 
    def check_insc_max_club(self):        
        # Check maximum inscriptions by event and club
        champ_id = self.champ_id
        sql = '''
select ci.club_id, ci.event_id, 
    (select ce.gender_id from champ_events as ce 
                where ce.champ_id=? 
                    and ce.event_id=ci.event_id 
                    and case when ce.gender_id<>'X' then ce.gender_id=ci.gender_id else 1 end 
                    and ce.category_id=ci.category_id) as ce_gender_id, 
    ci.category_id, count(*) as conta, 
    (select insc_max from champ_events as ce 
        where ce.champ_id=? 
            and ce.event_id=ci.event_id 
            and case when ce.gender_id<>'X' then ce.gender_id=ci.gender_id else 1 end 
                and ce.category_id=ci.category_id) as insc_max
from champ_inscriptions as ci where ci.champ_id=? and ci.inscribed=1 and ci.type_id in ("I", "R", "S")
group by ci.club_id, ci.event_id, ce_gender_id, ci.category_id
having
count(*) > (select insc_max from champ_events as ce 
            where ce.champ_id=? 
                and ce.event_id=ci.event_id 
                and case when ce.gender_id<>'X' then ce.gender_id=ci.gender_id else 1 end 
                and ce.category_id=ci.category_id)
order by ci.club_id, ci.event_id '''
        values = ((champ_id, champ_id, champ_id , champ_id),)
        rows = self.config.dbs.exec_sql(sql=sql, values=values)
        CLUB_ID, EVENT_ID, GENDER_ID, CATEGORY_ID, INSC, INSC_MAX = list(range(6))
        message = ''
        for i in rows:
            club = self.config.clubs.get_club(i[CLUB_ID])
            message += _('{} {} {} {} Insc.: {} Max.: {}\n').format(
                    club.short_desc, i[EVENT_ID], i[GENDER_ID], i[CATEGORY_ID], i[INSC], i[INSC_MAX])
        if message:
            message=_('Clubs with excess inscriptions:\n{}').formatmessage
        return message
            
    def export_to_server(self):
        """export inscriptions to_server"""

        # Generate file to publish

        entity = self.config.entity

        prefs = self.config.prefs
        local_file_path = os.path.join(prefs.fol_local_inscriptions,
                                       "{}_{}.insc".format(self.champ_id,
                                                          entity.entity_id))
        remote_file_path = os.path.join(prefs.fol_remote_inscriptions,
                                        "{}_{}.insc".format(self.champ_id,
                                                            entity.entity_id))

        tables = ('champ_inscriptions',)
        if entity.is_federation:
            where_sql = 'where champ_id=?'
            where_values = (self.champ_id, )
        else:
            where_sql = 'where champ_id=? and club_id=? '
            where_values = (self.champ_id, entity.entity_id)
        files.export_table_to_file(dbs=self.config.dbs,
                                   tables=tables,
                                   file_path=local_file_path,
                                   where_sql=where_sql,
                                   where_values=where_values)

        com_server = self.config.com_server
        com_server.send_file(local_file_path=local_file_path,
                             remote_file_path=remote_file_path)

    def import_from_server(self, import_own, entity_id, import_only_own=False):
        """
        import_own = [True|False], if True,  imported overwrite previous
        entity_id = entity owner championship, who is importing
        """
        com_server = self.config.com_server

        fol_local_inscriptions = self.config.prefs.fol_local_inscriptions
        fol_remote_inscriptions = self.config.prefs.fol_remote_inscriptions

        os.chdir(fol_local_inscriptions)
        champ_local_insc = {}
        for i in os.listdir(fol_local_inscriptions):
            if i[:12] == self.champ_id:
                champ_local_insc[i] = os.path.getmtime(i)

        all_remote_insc = com_server.get_list(fol_remote_inscriptions)
        for i in all_remote_insc:
            if i.filename[:12] == self.champ_id:
                insc_club_id = i.filename[13:18]
                local_file_path = os.path.join(fol_local_inscriptions,
                                               i.filename)
                # second if line: compare with local and import if is more new
                if (i.filename not in champ_local_insc or
                        int(i.st_mtime) != int(champ_local_insc[i.filename])):
                    com_server.get_file(
                            remote_file_path=os.path.join(
                                fol_remote_inscriptions,
                                i.filename),
                            local_file_path=local_file_path, optimize=False)
                # as dúas liñas de arriba paseino ás dúas de abaixo para que
                # importe sempre e deste xeito recargue a inscrición do servidor
                if entity_id != insc_club_id and not import_only_own:
                    self.import_club_inscriptions(local_file_path, insc_club_id)
                elif import_own and entity_id == insc_club_id:
                    self.import_club_inscriptions(local_file_path, insc_club_id)

    def import_club_inscriptions(self, local_file_path, insc_club_id):
        champs = self.champs
        msg = ""
        content, main_table, champ_id = champs.get_file_import(
                                                    file_path=local_file_path)
        try:
            self.delete_club_inscriptions(champ_id, insc_club_id)

            champs.import_from_file(content)
        except:
            print(RuntimeError, TypeError, NameError)
            msg = _('Error importing: %s\n') % local_file_path
        return msg

    def delete_club_inscriptions(self, champ_id, club_id):
        '''
        delete current inscriptios for champ_id and club_id
        '''
        sql = '''
delete from champ_inscriptions where champ_id=? and club_id=? '''  #and inscribed=0
        self.config.dbs.exec_sql(sql=sql, values=((champ_id, club_id),))
