# -*- coding: utf-8 -*-


from specific_classes.core.issue import Issue


class Issues(list):

    def __init__(self, config):
        self.config = config

    def get_pos(self, issue_id):
        pos = 0
        for i in self:
            if i.issue_id == issue_id:
                pos = i.pos
                break
        if pos == 0:  # Issue not found
            #FIXME:
            pos = 999
        return pos

    def load_items_from_dbs(self):
        del self[:]  # borra os elementos que haxa
        ISSUES = (
            # Issues lenex
            ('DSQ', 1, _('Athlete/Relay disqualified')),  # Descualificación (xenérica)
            ('DNS', 2, _('Athlete/Relay did not start \(no reason given or to late withdrawl\)')),  # Non presentación
            ('DNF', 3, _('Athlete/Relay did not finish')),  # Retiramento (por non poder rematar o comezado)
            ('WDR', 5, _('Athlete/Relay was withdrawn (on time)')),  # Baixa 
            ('SICK', 4, _('Athlete is sick.')),  # Baixa por enfermidade

            # Another issues 
            # ('DSQ', 1, _('Disqualified')),  # DES - Descualificación
            # ('DNF', 2, _('Did Not Finish')),  # RET - Retiramento
            # ('DWD', 3, _('Withdraw')),  # BAI - Baixa
            # ('DNS', 4, _('Did Not Start')),  # NPR - Non presentación
            # ('WSK', 5, _('Wrong Stroke')),  # DNI - Nado irregular
            # ('WTR', 6, _('Wrong Turn')),  # DVI - Viraxe irregular
            # ('WST', 7, _('Wrong Start')),  # DSI - Saída irregular
            # ('WFN', 8, _('Wrong Finish')),  # DCI - Chegada irregular
            # ('DFS', 9, _('False Start')),  # DSA - Saída anticipada
            # ('DIS', 10, _('Ilegal start')),  # DPA - Posta anticiapda
            # ('>15', 10, _('>15m immersion')),  # >15m inmersión | Sobrepasar 15 m de inmersión
            )
        (ISSUE_ID, POS, NAME) = range(3) 
        for i in ISSUES:
            self.append(Issue(
                    issues=self,
                    issue_id=i[ISSUE_ID],
                    pos=i[POS],
                    name=i[NAME],
                    ))

    def choices(self):
        '''
        return values for wxchoice with ClientData
        '''
        values = ['',]
        for i in self:
            values.append(i.issue_id)
        return values
