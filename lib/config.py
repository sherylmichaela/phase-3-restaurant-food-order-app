# Needs engine and sessionmaker

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///data.db")
Session = sessionmaker(bind=engine)
session = Session()