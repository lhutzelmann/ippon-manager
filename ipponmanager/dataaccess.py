from wheezy.core.comp import u
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, Integer, Sequence, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import MetaData

Base = declarative_base()


class DataModelMixin(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @declared_attr
    def id(cls):
        # some dbms need sequence tables for automatic ID generation
        sequence_table_name = cls.__tablename__ + '_id_seq'
        return Column(Integer, Sequence(sequence_table_name), primary_key=True)

    @classmethod
    def max_str_len(cls, property_name):
        """
        Returns the maximum length of the given property as defined in the
        data model.
        :param property_name: key/name of the property
        :return: the maximum length or None if there is no limitation
        """
        metadata = cls.metadata
        property_column = (metadata.tables[cls.__tablename__]
                           .columns[property_name])
        property_type = property_column.type
        if isinstance(property_type, String):
            return property_type.length
        else:
            return None


class DalSqlAlchemy(object):
    """ Data Access Layer class for SQLAlchemy based data objects.
    """

    def __init__(self, connection_string='sqlite:///:memory:'):
        self.engine = create_engine(connection_string, echo=True)
        self._session = None

    def get_session(self):
        if self._session is None:
            session_class = sessionmaker(bind=self.engine)
            self._session = session_class()
        return self._session

    def create_database(self):
        Base.metadata.create_all(self.engine)

    def new(self, klass, **kwargs):
        """ Create new data model instance of type klass.
        :param klass: type of the new instance.
        :param kwargs: keyword arguments for the initializer of the data model
        :return: the new data model instance
        """
        obj = klass(**kwargs)
        self._session.add(obj)
        return obj
