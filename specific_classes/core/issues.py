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
        return pos

    def load_items_from_dbs(self):
        del self[:]  # borra os elementos que haxa
        ISSUES = (
            (_('DSQ'), 1, _('Disqualified')),  # DES - Descualificación
            (_('DNF'), 2, _('Did Not Finish')),  # RET - Retiramento
            (_('DWD'), 3, _('Withdraw')),  # BAI - Baixa
            (_('DNS'), 4, _('Did Not Start')),  # NPR - Non presentación
            (_('WSK'), 5, _('Wrong Stroke')),  # DNI - Nado irregular
            (_('WTR'), 6, _('Wrong Turn')),  # DVI - Viraxe irregular
            (_('WST'), 7, _('Wrong Start')),  # DSI - Saída irregular
            (_('WFN'), 8, _('Wrong Finish')),  # DCI - Chegada irregular
            (_('DFS'), 9, _('False Start')),  # DSA - Saída anticipada
            (_('DIS'), 10, _('Ilegal start')),  # DPA - Posta anticiapda
            (_('>15'), 10, _('>15m immersion')),  # >15m inmersión
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
