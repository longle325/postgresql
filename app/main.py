from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from database import engine, get_session
from models import User, UserBase, Company, CompanyBase
from uuid import UUID

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    from database import create_db_and_tables
    create_db_and_tables()

# User endpoints
@app.post("/users/", response_model=User)
def create_user(user: UserBase, db: Session = Depends(get_session)):
    db_user = User.from_orm(user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    users = db.exec(select(User).offset(skip).limit(limit)).all()
    return users

@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: UUID, db: Session = Depends(get_session)):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: UUID, user: UserBase, db: Session = Depends(get_session)):
    db_user = db.get(User, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: UUID, db: Session = Depends(get_session)):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

# Company endpoints
@app.post("/companies/", response_model=Company)
def create_company(company: CompanyBase, db: Session = Depends(get_session)):
    db_company = Company.from_orm(company)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

@app.get("/companies/", response_model=List[Company])
def read_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    companies = db.exec(select(Company).offset(skip).limit(limit)).all()
    return companies