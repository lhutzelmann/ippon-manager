import abc
from functools import lru_cache
from sqlalchemy import create_engine
import sqlalchemy.orm

# from ipponmanager import DAOManager
# from ipponmanager import u
from wheezy.core.comp import u

from ipponmanager.tournament.datamodel import Tournament


class Configuration(object):
    """
    """

    def __init__(self):
        self.__config = {
            "database": {
                "DB1": {
                    "connection_string": 'sqlite:///:memory:'
                }
            }
        }

    def get(self, *path):
        current = self.__config
        for segment in path:
            current = current[segment]
        return current

CONFIGURATION = Configuration()


class SessionFactory(object):
    """
    Fake SessionFactory for testing purposes
    """

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return Session(*args, **kwargs)


class Session(object):
    """
    Fake Session for testing purposes
    """

    def __init__(self, *args, **kwargs):
        pass

    def close(self):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass


class DAOConfig(object):
    """
    """

    def __init__(self):
        # TODO: get real objects
        self.__engine = None
        self.__session_factory = None
        self.__session = None

    def close(self):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass


class DAO(object, metaclass=abc.ABCMeta):
    """

    """

    def __init__(self, klass):
        self.dao_class = klass

    def create(self, **kwargs):
        raise NotImplementedError()

    def read(self, uuid):
        raise NotImplementedError()

    def update(self, data_model):
        raise NotImplementedError()

    def delete(self, data_model):
        raise NotImplementedError()

    def find(self, filter_criteria, start=0, stop=-1):
        raise NotImplementedError()

    def count(self, filter_criteria):
        raise NotImplementedError()


class SqlAlchemyDAO(DAO):
    """

    """
    # TODO: Fully support SQLAlchemy
    engine_pool = {}

    @classmethod
    def get_connection(cls, database):
        engine = cls.engine_pool.get(database)
        if engine is None
            connection_string = CONFIGURATION.get('database', database,
                                                  'connection_string')
            engine = create_engine(connection_string, echo=True)
            cls.engine_pool[database] = engine
        return engine.connect()


    def __init__(self, klass, database=None):
        super(SqlAlchemyDAO, self).__init__(klass)

    def create(self, **kwargs):
        obj = self.dao_class(**kwargs)
        obj.id = 4711
        return obj

    def read(self, uuid):
        pass

    def update(self, data_model):
        pass

    def delete(self, data_model):
        return True

    def find(self, filter_criteria, start=0, stop=-1):
        return []

    def count(self, filter_criteria):
        return 0


class Registry(object):
    """

    """

    def __init__(self):
        self.__registry = {
            'ipponmanager.tournament.datamodel.Tournament': {
                'DAO': SqlAlchemyDAO,
                'DAO.__init__': {'database': 'DB1'},
                'SessionFactory': sqlalchemy.orm.sessionmaker(),
                'SessionFactory.__init__': {}
            }
#            'ipponmanager.tournament.datamodel.Tournament': {
#                'DAO': SqlAlchemyDAO,
#                'DAO.__init__': {},
#                'SessionFactory': SessionFactory,
#                'SessionFactory.__init__': {},
#            }
        }

    def get(self, key):
        return self.__registry[key]


REGISTRY = Registry()


class DAOManager(object):
    """

    """

    def __init__(self):
        self.__dao_contexts = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        no_error = exc_type is None
        if no_error:
            self.commit()
        else:
            self.rollback()
        return no_error

    @staticmethod
    def get_full_class_name(klass):
        # TODO: move to some more generic place
        return klass.__module__ + '.' + klass.__name__

    @lru_cache()
    def __get_cached_session_factory(self, session_factory_class, **kwargs):
        return session_factory_class(**kwargs)

    def get_session_factory(self, key):
        config = REGISTRY.get(key)
        sf_class = config.get('SessionFactory', SessionFactory)
        sf_kwargs = config.get('SessionFactory.__init__', {})
        session_factory = self.__get_cached_session_factory(
            session_factory_class=sf_class,
            **sf_kwargs
        )
        return session_factory

    def dao(self, klass):
        key = self.get_full_class_name(klass)
        # reuse or create new session
        sf = self.get_session_factory(key)
        if sf not in self.__sessions:
            session = sf()
            self.__sessions.add(session)
        # create dao object
        config = REGISTRY.get(key)
        dao_class = config['DAO']
        dao_kwargs = config['DAO.__init__']
        return dao_class(klass, **dao_kwargs)

    def commit(self):
        for dao_context in self.__dao_contexts:
            dao_context.commit()

    def rollback(self):
        for dao_context in self.__dao_contexts:
            dao_context.rollback()


if __name__ == '__main__':
    # TODO: read in configuration etc.

    # TODO: create database schema if necessary

    with DAOManager() as daom:
        dao = daom.dao(Tournament)

        tournament_dict = dict(
            title=u('Vereinsmeisterschaften'),
            organiser=u('JC Ettlingen'),
            description=u('Vereinsmeisterschaften des JC Ettlingen')
        )

        # TODO: validation

        tournament = dao.create(**tournament_dict)
        daom.commit()
        print(tournament.id)
