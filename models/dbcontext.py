# import psycopg2 as pg
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
from models.config import Config as cfg

class DbContext:
    """
    dynamically constructs connection string
    and returns new psql sessions
    """
    __CONNECTION_STRING = f"postgresql://{cfg.DBUSER}:{cfg.DBPASS}@{cfg.DBHOST}/{cfg.DBNAME}"
    __engine = create_engine(__CONNECTION_STRING)
    Session = sessionmaker(bind=__engine)
    Base = declarative_base()

    @classmethod
    @contextmanager
    def session_scope(cls):
        """provide a session for db transactions;
           ref: https://docs.sqlalchemy.org/en/13/orm/session_basics.html"""
        session = cls.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
