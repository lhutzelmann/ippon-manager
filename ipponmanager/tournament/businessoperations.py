class PersistencyMixin(object):
    """
    """

    def __init__(self, repository=None):
        if repository is None:
            raise ValueError("No repository specified.")
        self.repository = repository


class ListTournaments(object, PersistencyMixin):
    """
    """
    pass