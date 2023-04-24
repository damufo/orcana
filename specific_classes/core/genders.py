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
        res = (
            ('F', _('Fem.'), _('Female')),
            ('M', _('Mal.'), _('Male')),
            ('X', _('Mix.'), _('Mixed')),
            )
        for i in res:
            self.append(Gender(
                    genders=self,
                    gender_id = i[0],
                    short_name = i[1],  # 4 characters MAS.|FEM.
                    long_name = i[2],  # full name
                    ))
        return self

    def get_long_name(self, gender_id):
        long_name = ''
        for i in self:
            if i.gender_id == gender_id:
                long_name = i.long_name
                break
        return long_name

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



