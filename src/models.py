from sqlalchemy import Column, String, Numeric, Integer, Date
from database import Base

class ImageDetection(Base):
    __tablename__ = "image_detection"

    media_path = Column(String, primary_key=True, index=True)
    confidence = Column(Numeric)
    x1 = Column(Numeric)
    x2 = Column(Numeric)
    y1 = Column(Numeric)
    y2 = Column(Numeric)

class ProductsTransformed(Base):
    __tablename__ = "products_transformed"

    id = Column(String, primary_key=True, index=True)
    channel_id = Column(String)
    name = Column(String)
    media_path = Column(String)

class ProductPricesTransformed(Base):
    __tablename__ = "product_prices_transformed"

    id = Column(String, primary_key=True, index=True)
    channel_id = Column(String)
    price = Column(Numeric)

class PhoneNumbersTransformed(Base):
    __tablename__ = "phone_numbers_transformed"

    id = Column(String, primary_key=True, index=True)
    channel_id = Column(String)
    price = Column(String)

class Message(Base):
    __tablename__ = "message"

    id = Column(String, primary_key=True, index=True)
    channel_id = Column(String)
    telegram_id = Column(Integer)
    message = Column(String)
    media_path = Column(String)
    date = Column(Date)

class Channel(Base):
    __tablename__ = "channel"

    id = Column(String, primary_key=True, index=True)
    username = Column(String)
    title = Column(String)
