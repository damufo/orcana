# -*- coding: utf-8 -*-


from specific_classes.champ.relay_members_candidates import RelayMembersCandidates


class Model(object):

    def __init__(self, relay_members):
        self.relay_members = relay_members
        self.candidates = RelayMembersCandidates(
            relay_members=relay_members)
