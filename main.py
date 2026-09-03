from database import session, engine
from fastapi import FastAPI, Depends
from models import Product
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)

@app.get('/')
def greet():
    return "Welcome to telusko trac"

def imp_fn():
    return 100


products = [
            Product(id=1, name="Phone", description="Budget Phone", price=99, quantity=10),
            Product(id=2, name="Laptop", description="Budget Laptop", price=999, quantity=100),
            Product(id=3, name="Pen", description="Budget Pen", price=20, quantity=50),
            Product(id=4, name="Table", description="Budget Table", price=300, quantity=30)
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
    print("Products count: ", count)
    if count == 0:
        for product in products:
            print(product.model_dump())
            db.add(database_models.Product(**product.model_dump()))
        db.commit()

init__db()

@app.get('/products')
def get_products(db: Session = Depends(get_db)):
    return db.query(database_models.Product).all()

@app.get('/product/{id}')
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    for product in products:
        if product.id == id:
            return product
    return "Product not found"

@app.post('/product')
def add_product(product: Product, db: int = Depends(imp_fn)):
    products.append(product)
    return products

@app.put('/product/{id}')
def update_product(id: int, product: Product, db: int = Depends(imp_fn)):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return "Product updated successfully"
    return "Product not found"

@app.delete('/product/{id}')
def delete_product(id: int):
    for i in range(len(products)):
        if products[i].id == id:
            del(products[i])
            return "Product deleted successfully"
    return "Product not found"