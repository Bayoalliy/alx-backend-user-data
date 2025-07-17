"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound, InvalidRequestError
from sqlalchemy.orm.session import Session
from user import Base, User
import bcrypt
class DB:
    """DB class
    """
    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email, hashed_password) -> User:
        """adds a user to the database
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs):
        """find a user with an attribute
        """
        print(kwargs)
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            print("No result found")
            return
        except InvalidRequestError:
            print("invalid requeat")
            return
        return user

    def update_user(self, id: int, **kwargs) -> None:
        """updates a row in users table
        """
        user = self.find_user_by(id=id)
        if user:
            for attr, val in kwargs.items():
                if attr not in User.__table__.columns:
                    raise ValueError
                user.attr = val
            self._session.commit()
        return None
