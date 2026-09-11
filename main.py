from database import session, engine
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Product
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_methods=['*'])

database_models.Base.metadata.create_all(bind=engine)

products = [
            Product(id=1, name="Phone", description="Budget Phone", price=99, quantity=10, category="Electronics"),
            Product(id=2, name="Laptop", description="Budget Laptop", price=999, quantity=100, category="Electronics"),
            Product(id=3, name="Pen", description="Budget Pen", price=20, quantity=50, category="Stationery"),
            Product(id=4, name="Table", description="Budget Table", price=300, quantity=30, category="Furniture")
            ]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init__db():
    db = session()
    count = db.query(database_models.Product).count()
    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()

init__db()

@app.get('/products')
def get_products(db: Session = Depends(get_db), category: str | None = None):
    if not category:
        return db.query(database_models.Product).all()
    return db.query(database_models.Product).filter(database_models.Product.category == category).all()

@app.get('/products/{id}')
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    return db.query(database_models.Product).filter(database_models.Product.id == id).first()

@app.post('/products')
def add_product(product: Product, db: Session = Depends(get_db)):
    new_product = database_models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=product.quantity
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.put('/products/{id}')
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Producted updated"
    else:
        return "Product not found"


@app.delete('/products/{id}')
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)    
        db.commit()    
        return "Product deleted successfully"
    else:
        return "Product not found"