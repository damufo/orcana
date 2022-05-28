# -*- coding: utf-8 -*- 


from specific_classes.core.gender import Gender


class Genders(list):

    def __init__(self, config):
        self.config = config
        
    def load_items_from_dbs(self):
        '''
        load values
        '''
        del self[:] #borra os elementos que haxa
        res = ((_('Female'), 'F'), (_('Male'), 'M'), (_('Mixed'), 'X'))
        for i in res:
            self.append(Gender(
                    genders=self,
                    gender_id = i[1],
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
            values.append((i.name, i.gender_id))
        return values



