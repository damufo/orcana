# -*- coding: utf-8 -*- 


from specific_classes.core.style import Style


class Styles(list):

    def __init__(self, config):
        self.config = config
        
    def load_items_from_dbs(self):
        '''
        load values
        '''
        del self[:] #borra os elementos que haxa
        res = (
            ('L',  _('Fr'), _('Free')), 
            ('M',  _('Bu'), _('Butterfly')),
            ('E',  _('Ba'), _('Backstroke')),
            ('B',  _('Br'), _('Breastroque')),
            ('S',  _('Me'), _('Medley')),               
            ('G',  _('BaBr'), _('Backstroke-Breastroke')),
            ('Z',  _('BuBa'), _('Butterfly-Backstroke')),
            ('T',  _('BaBrCr'), _('Back-Brea-Crol')),
            ('F',  _('FeCrAr'), _('Feet crol arrow')),
            ('N',  _('FeBuAr'), _('Feet butterfly arrow')),
            ('K',  _('FeBrAr'), _('Feet breastroke arrow')),
            ('J',  _('FeBaAr'), _('Feet backstroke arrow')),
            ('H',  _('BrCr'), _('Breastroke-Crol')),
            ('P',  _('CrBa'), _('Crol-Backstroke')),
            ('Q',  _('BrBu'), _('Breastroke-Butterfly')),
            ('V',  _('BuBaBr'), _('Butterfly-Backstroke-Breastroke')),
            )
        # sql = ("SELECT style_id, short_name, long_name "
        #        "from styles order by pos")

        # res = self.config.dbs.exec_sql(sql) 
        for i in res:
            self.append(Style(
                    styles=self,
                    style_id = i[0],
                    short_name = i[1],
                    long_name = i[2]))
        return self

    def get_style(self, style_id):
        style = None
        for i in self:
            if i.style_id == style_id:
                style = i
                break
        return style 
            
    def choices(self, add_empty=False):
        '''
        return values for wxchoice with ClientData
        '''
        values = []
        if add_empty:
            values.append(('',  '')) 
        for i in self:
            values.append((i.style_id, i.long_name))
        return values



