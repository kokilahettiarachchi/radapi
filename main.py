from fastapi import FastAPI, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
import crud
import models
import schemas
import database
import security
from database import SessionLocal, engine
from fastapi.responses import JSONResponse
from typing import List

app = FastAPI(
    title="My API",
    description="This is an API built with FastAPI for assessment of RAD",
    version="0.1.0"
)

# OAuth2PasswordBearer is used to get the token from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
 

# Create the tables (if they don't exist)
models.Base.metadata.create_all(bind=engine)

# Create an Item
@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item)

# Get All Items
@app.get("/items/", response_model=list[schemas.Item])
def get_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_items(db=db, skip=skip, limit=limit)

# Get Item by ID
@app.get("/items/{item_id}", response_model=schemas.Item)
def get_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# Update an Item
@app.put("/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = crud.update_item(db=db, item_id=item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# Delete an Item
@app.delete("/items/{item_id}", response_model=schemas.Item)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


# Endpoint for creating a new user
@app.post("/users/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = security.hash_password(user.password)
    return crud.create_user(db=db, user=user, hashed_password=hashed_password)

# Endpoint for logging in and obtaining a JWT token
@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=form_data.username)
    if not db_user or not security.verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate JWT token
    access_token = security.create_access_token(data={"sub": db_user.username, "role": db_user.role})
    return {"access_token": access_token, "token_type": "bearer"}

# Protect a route with JWT and Role-based access
@app.get("/items/", response_model=List[schemas.Item])
def read_items(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=security.decode_access_token(token)["sub"])
    
    # Role-based access control
    if user.role != "Admin":
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    items = crud.get_items(db)
    return items
