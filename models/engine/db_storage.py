#!/usr/bin/python3
"""New engine DBStorage"""

from os import getenv
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User


class DBStorage():
    """A database storage"""
    __engine = None
    __session = None

    def __init__(self):
        """initialzing variables and linking"""
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine(
                'mysql+mysqldb://{}:{}@{}/{}'.format(user, password, host, db),
                pool_pre_ping=True)

        if env == 'test':
            Base.metadata.drop_all(self.engine)

    def all(self, cls=None):
        """query on the current database session depending on class name"""
        all_classes = (User, State, City, Place, Amenity, Review)
        my_objs = dict()

        if cls is None:
            for i in all_classes:
                qury = self.__session.query(i)
                for obj in qury.all():
                    obj_key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                    my_objs[obj_key] = obj
        else:
            qury = self.__session.query(cls)
            for obj in qury.all():
                obj_key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                my_objs[obj_key] = obj
        return my_objs

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """creates all the tables in database"""
        Base.metadata.create_all(self.__engine)

        session_maker = sessionmaker(
                bind=self.__engine, expire_on_commit=False)
        my_session = scoped_session(session_maker)
        self.__session = my_session()

    def close(self):
        """close the session"""
        self.__session.close()
