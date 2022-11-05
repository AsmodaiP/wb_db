from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DB_URI
from scheme import Barcodes, Base, Goods, Orders, Positions  # noqa

engine = create_engine(DB_URI)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)
