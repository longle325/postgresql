from sqlmodel import create_engine, SQLModel, Session

DATABASE_URL = "postgresql://longlb:28112005@my-postgres:5432/db"
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
