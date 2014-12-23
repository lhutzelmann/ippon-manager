from wheezy.core.comp import u
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


class DataModelMixin(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


current_session = None


def get_session():
    global current_session
    if current_session is None:
        engine = create_engine('sqlite:///:memory:', echo=True)
        Base.metadata.create_all(engine)
        session_class = sessionmaker(bind=engine)
        current_session = session_class()
    return current_session
