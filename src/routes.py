from fastapi import APIRouter, Depends
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
