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
        # style_id, short_name, long_name, lenex_name
                # if self.event_id.endswith("L"):
        #     style = _("FREE")
        # elif self.event_id.endswith("M"):
        #     style = _("BUTTERFLY")
        # elif self.event_id.endswith("B"):
        #     style = _("BREASTSTROKE")
        # elif self.event_id.endswith("E"):
        #     style = _("BACKSTSTROKE")
        # elif self.event_id.endswith("S"):
        #     style = _("STYLES")
        # elif self.event_id.endswith("Z"):
        #     style = _("BOL-COS")
        # elif self.event_id.endswith("G"):
        #     style = _("COS-BRA")
        # elif self.event_id.endswith("H"):
        #     style = _("BRA-CROL")
        # elif self.event_id.endswith("V"):
        #     style = _("BOL-COS-BRA")
        res = (
            ('L',  _('FREE'), _('Free'), 'FREE'), 
            ('M',  _('FLY'), _('Fly'), 'FLY'),
            ('E',  _('BACK'), _('Back'), 'BACK'),
            ('B',  _('BREAST'), _('Breast'), 'BREAST'),
            ('S',  _('MEDLEY'), _('Medley'), 'MEDLEY'),
            ('G',  _('BA-BR'), _('Back-Breast'), 'BACK-BREAST'),
            ('Z',  _('FL-BA'), _('Fly-Back'), 'FLY-BACK'),
            ('T',  _('BA-BR-CR'), _('Back-Breast-Crawl'), 'BACK-BREAST-CRAWL'),
            ('F',  _('FE CR AR'), _('Feet crawl arrow'), 'FEET CRAWL ARROW'),
            ('N',  _('FE FL AR'), _('Feet fly arrow'), 'FEET FLY ARROW'),
            ('K',  _('FE BR AR'), _('Feet breast arrow'), 'FEET BREAST ARROW'),
            ('J',  _('FE BA AR'), _('Feet back arrow'), 'FEET BACK ARROW'),
            ('H',  _('BR-CR'), _('Breast-Crawl'), 'BREAST-CRAWL'),
            ('P',  _('CR-BA'), _('Crawl-Back'), 'CRAWL-BACK'),
            ('Q',  _('BR-FL'), _('Breast-Fly'), 'BREAST-FLY'),
            ('V',  _('FL-BA-BR'), _('Fly-Back-Breast'), 'FLY-BACK-BREAST'),
            )
        # sql = ("SELECT style_id, short_name, long_name "
        #        "from styles order by pos")

        # res = self.config.dbs.exec_sql(sql) 
        for i in res:
            self.append(Style(
                    styles=self,
                    style_id = i[0],
                    short_name = i[1],
                    long_name = i[2],
                    lenex_name = i[3],
                    ))
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



