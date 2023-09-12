# -*- coding: utf-8 -*-


from specific_classes.champ.result_members_candidates import PersonsCandidates


class Model(object):

    def __init__(self, members):
        self.members = members
        self.candidates = PersonsCandidates(
            champ=result_members.champ,
            result_members=members)
