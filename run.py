from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from scheme import Goods, Positions, Orders, Barcodes, Base


engine = create_engine('sqlite:///test.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)