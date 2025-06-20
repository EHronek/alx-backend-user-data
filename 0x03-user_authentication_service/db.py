#!/usr/bin/env python3
"""DB Module"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB Class"""
    def __init__(self) -> None:
        """Initialize a new db session
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database"""
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self.__session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """FInds a user based on a set if filters"""
        if not kwargs:
            raise InvalidRequestError("No filter creteria provided")
        try:
            return self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound("No user found matching the creteria")
        except InvalidRequestError as e:
            raise InvalidRequestError(f"Invalid query as arguments: {str(e)}")

    def update_user(self, user_id: int, **kwargs) -> None:
        """updates a user based on id"""
        user = self.find_user_by(id=user_id)
        if not user:
            return
        valid_attrs = ['email', 'hashed_password', 'session_id', 'reset_token']
        for key, value in kwargs.items():
            if key not in valid_attrs:
                raise ValueError(f"Invalid attribute: {key}")
            setattr(user, key, value)
        self._session.commit()
