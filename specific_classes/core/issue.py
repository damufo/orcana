# -*- coding: utf-8 -*- 


class Issue(object):

    def __init__(self, **kwargs):
        self.issues = kwargs['issues']
        self.issue_id = kwargs['issue_id']
        self.name = kwargs['name']
        self.pos = kwargs['pos']
