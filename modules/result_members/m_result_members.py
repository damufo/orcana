# -*- coding: utf-8 -*-


from specific_classes.champ.result_members_candidates import PersonsCandidates


class Model(object):

    def __init__(self, result_members):
        self.result_members = result_members
        self.candidates = PersonsCandidates(
            champ=result_members.champ,
            result_members=result_members)
