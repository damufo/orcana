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
            ('RET', 1, _('Retirado')),
            ('BAI', 2, _('Baixa')),
            ('NPR', 3, _('Non presentado/a')),
            ('DNI', 4, _('Nado irregular')),
            ('DVI', 5, _('Viraxe irregular')),
            ('DSI', 6, _('Saída irregular')),
            ('DCI', 7, _('Chegada irregular')),
            ('DSA', 8, _('Saída anticipada')),
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
