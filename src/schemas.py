from pydantic import BaseModel
from typing import Optional

class ImageDetectionBase(BaseModel):
    media_path: str
    confidence: float
    x1: float
    x2: float
    y1: float
    y2: float

class ProductsTransformedBase(BaseModel):
    id: str
    channel_id: str
    name: str
    media_path: str

class ProductPricesTransformedBase(BaseModel):
    id: str
    channel_id: str
    price: float

class PhoneNumbersTransformedBase(BaseModel):
    id: str
    channel_id: str
    price: str

class MessageBase(BaseModel):
    id: str
    channel_id: str
    telegram_id: int
    message: str
    media_path: str
    date: str

class ChannelBase(BaseModel):
    id: str
    username: str
    title: str

# Models for responses
class ImageDetection(ImageDetectionBase):
    class Config:
        orm_mode = True

class ProductsTransformed(ProductsTransformedBase):
    class Config:
        orm_mode = True

class ProductPricesTransformed(ProductPricesTransformedBase):
    class Config:
        orm_mode = True

class PhoneNumbersTransformed(PhoneNumbersTransformedBase):
    class Config:
        orm_mode = True

class Message(MessageBase):
    class Config:
        orm_mode = True

class Channel(ChannelBase):
    class Config:
        orm_mode = True
