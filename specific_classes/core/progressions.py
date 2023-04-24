# -*- coding: utf-8 -*- 


from specific_classes.core.progression import Progression


class Progressions(list):

    def __init__(self, config):
        self.config = config
        
    def load_items_from_dbs(self):
        '''
        load values
        '''
        del self[:] #borra os elementos que haxa
        res = ((_('TIM'), 'TIM'), (_('FIN'), 'FIN'), (_('PRE'), 'PRE'))
        for i in res:
            self.append(Progression(
                    progressions=self,
                    progression_id = i[1],
                    name = i[0]))
        return self

    def choices(self, add_empty=False):
        '''
        return values for wxchoice with ClientData
        '''
        values = []
        if add_empty:
            values.append(('', '')) 
        for i in self:
            values.append((i.name, i.progression_id))
        return values



