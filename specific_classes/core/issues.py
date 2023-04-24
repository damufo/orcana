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
            (_('DSQ'), 1, _('Disqualified')),
            (_('DNF'), 2, _('Did Not Finish')),
            (_('DWD'), 3, _('Withdraw')),
            (_('DNS'), 4, _('Did Not Start')),
            (_('WSK'), 5, _('Wrong Stroke')),
            (_('WTR'), 6, _('Wrong Turn')),
            (_('WST'), 7, _('Wrong Start')),
            (_('WFN'), 8, _('Wrong Finish')),
            (_('DFS'), 9, _('False Start')),
            # ('DES', 1, _('Descualificado/a')),
            # ('RET', 2, _('Retirado/a')),
            # ('BAI', 3, _('Baixa')),
            # ('NPR', 4, _('Non presentado/a')),
            # ('DNI', 5, _('Nado irregular')),
            # ('DVI', 6, _('Viraxe irregular')),
            # ('DSI', 7, _('Saída irregular')),
            # ('DCI', 8, _('Chegada irregular')),
            # ('DSA', 9, _('Saída anticipada')),
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
