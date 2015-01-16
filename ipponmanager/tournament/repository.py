from .datamodel import Tournament


class Repository(object):
    """ Class implementing the repository pattern. A repository lies between
        business layer and data layer and separates them from each other.
    """

    def __init__(self, dal_object):
        """
        :param dal_object: DAL object used for accessing the persistent data
        :return:
        """
        self.dal = dal_object

    def list_tournaments(self):
        """
        :return: a list of all tournament objects
        """
        return self.dal.get_slice(Tournament, 0, 10)

    def add_tournament(self, tournament):
        """
        :param tournament:
        :return:
        """
        self.dal.add(tournament)
