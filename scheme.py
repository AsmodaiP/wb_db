
from sqlalchemy import TIMESTAMP, Column, Date, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

    def __repr__(self):
        return '<{0.__class__.__name__}(id={0.id!r})>'.format(self)


class Goods(BaseModel):
    __tablename__ = 'goods'

    sku = Column(Integer, nullable=False, unique=True)
    article = Column(String(255), nullable=False, unique=True)
    category = Column(String(255), nullable=True)
    price = Column(Float, nullable=False)
    price_after_spp = Column(Float, nullable=False)
    brand = Column(String(255), nullable=True)
    owner = Column(String(255), nullable=False)


class Positions(BaseModel):
    __tablename__ = 'positions'

    sku = Column(Integer, nullable=False)
    query = Column(String(255), nullable=False)
    position = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)


class Orders(BaseModel):
    __tablename__ = 'orders'

    sku = Column(Integer, nullable=False, unique=False)
    barcode = Column(String(255), nullable=False, unique=False)
    date = Column(Date, nullable=False)
    fbs_count = Column(Integer, nullable=False, default=0)
    fbo_count = Column(Integer, nullable=False, default=0)


class Barcodes(BaseModel):
    __tablename__ = 'barcodes'

    sku = Column(Integer, nullable=False, unique=True)
    barcode = Column(String(255), nullable=False, unique=True)
    size = Column(String(255), nullable=False)
    color = Column(String(255), nullable=False)
