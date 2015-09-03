from wheezy.core.comp import u
from decimal import Decimal as Dec
from sqlalchemy import Column, String

from ipponmanager.dataaccess import Base, DataModelMixin


class Tournament(Base, DataModelMixin):
    """
    data class for tournaments.
    """
    title = Column(
        String(50),
        default=u(''),
        doc=u('Title of the tournament.'))
    organiser = Column(
        String,
        default=u(''),
        doc=u('Organiser of the tournament.'))
    description = Column(
        String,
        default=u(''),
        doc=u('Short description of the tournament.'))

    def __init__(self, id=0, title=u(''), organiser=u(''), description=u('')):
        if id != 0:
            self.id = id
        self.title = title
        self.organiser = organiser
        self.description = description


class SportsAssociation(Base, DataModelMixin):
    """ data class for sports associations.
    """

    def __init__(self, id=0, title=u(''), description=u('')):
        if id != 0:
            self.id = id
        self.title = title
        self.description = description


class SportsClub(Base, DataModelMixin):
    """ data class for sports clubs.
    """

    def __init__(self, id=0, title=u(''), association=None):
        if id != 0:
            self.id = id
        self.title = title
        self.association = association


class Competitor(Base, DataModelMixin):
    """ data class for tournament competitors/participants.
    """

    def __init__(self, id=0, first_name=u(''), middle_name=u(''),
                 last_name=u(''), gender=None, current_weight=Dec(0),
                 age_cohort=2000, sports_club=None, external_id=u('')):
        if id != 0:
            self.id = id
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.gender = gender
        self.current_weight = current_weight
        self.age_cohort = age_cohort
        self.sports_club = sports_club
        self.external_id = external_id


class Registration(Base, DataModelMixin):
    """ data class for registrations of competitors to a tournament.
    """

    def __init__(self, id=0, tournament=None, competitor=None, weight=Dec(0),
                 participation=None):
        if id != 0:
            self.id = id
        self.tournament = tournament
        self.competitor = competitor
        self.weight = weight
        self.participation = participation
