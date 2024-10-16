from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models
import schemas

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/image-detection/", response_model=list[schemas.ImageDetection])
def get_image_detections(db: Session = Depends(get_db)):
    return db.query(models.ImageDetection).all()

@router.get("/products-transformed/", response_model=list[schemas.ProductsTransformed])
def get_products_transformed(db: Session = Depends(get_db)):
    return db.query(models.ProductsTransformed).all()

@router.get("/product-prices-transformed/", response_model=list[schemas.ProductPricesTransformed])
def get_product_prices_transformed(db: Session = Depends(get_db)):
    return db.query(models.ProductPricesTransformed).all()

@router.get("/phone-numbers-transformed/", response_model=list[schemas.PhoneNumbersTransformed])
def get_phone_numbers_transformed(db: Session = Depends(get_db)):
    return db.query(models.PhoneNumbersTransformed).all()

@router.get("/messages/", response_model=list[schemas.Message])
def get_messages(db: Session = Depends(get_db)):
    return db.query(models.Message).all()

@router.get("/channels/", response_model=list[schemas.Channel])
def get_channels(db: Session = Depends(get_db)):
    return db.query(models.Channel).all()

@router.get("/phone-numbers/{channel_id}", response_model=list[schemas.PhoneNumbersTransformed])
def get_phone_numbers_by_channel(channel_id: str, db: Session = Depends(get_db)):
    phone_numbers = db.query(models.PhoneNumbersTransformed).filter(models.PhoneNumbersTransformed.channel_id == channel_id).all()
    if not phone_numbers:
        raise HTTPException(status_code=404, detail="Phone numbers not found for this channel ID")
    return phone_numbers

@router.get("/product-prices/{channel_id}", response_model=list[schemas.ProductPricesTransformed])
def get_product_prices_by_channel(channel_id: str, db: Session = Depends(get_db)):
    prices = db.query(models.ProductPricesTransformed).filter(models.ProductPricesTransformed.channel_id == channel_id).all()
    if not prices:
        raise HTTPException(status_code=404, detail="Prices not found for this channel ID")
    return prices

@router.get("/object-detection/{media_path}", response_model=list[schemas.ImageDetection])
def get_object_detection_by_media(media_path: str, db: Session = Depends(get_db)):
    detections = db.query(models.ImageDetection).filter(models.ImageDetection.media_path == media_path).all()
    if not detections:
        raise HTTPException(status_code=404, detail="Object detection results not found for this media path")
    return detections