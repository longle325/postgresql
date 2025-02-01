import sys
import argparse
from tqdm import tqdm
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from sqlmodel import create_engine, Session, SQLModel,select
from database.schema import Company, User
from settings import setting
SQLMODEL_DATABASE_URL = setting.database_url
engine = create_engine(SQLMODEL_DATABASE_URL,echo=True)
def init_db():
    SQLModel.metadata.create_all(engine)

def insert_to_db():
    companies = [
        Company(name="Tech Corp"),
        Company(name="Global Solutions"),
        Company(name="Digital Innovations"),
        Company(name="Future Systems"),
        Company(name="Data Dynamics"),
        Company(name="Cloud Services"),
        Company(name="Smart Technologies"),
        Company(name="Innovation Labs"),
        Company(name="Cyber Security Inc"),
        Company(name="AI Solutions")
    ]
    users = [
        User(name="John Doe", company_name="Tech Corp"),
        User(name="Jane Smith", company_name="Global Solutions"),
        User(name="Mike Johnson", company_name="Digital Innovations"),
        User(name="Sarah Williams", company_name="Future Systems"),
        User(name="David Brown", company_name="Data Dynamics"),
        User(name="Emily Davis", company_name="Cloud Services"),
        User(name="James Wilson", company_name="Smart Technologies"),
        User(name="Lisa Anderson", company_name="Innovation Labs"),
        User(name="Robert Taylor", company_name="Cyber Security Inc"),
        User(name="Michelle Lee", company_name="AI Solutions")
    ]

    with Session(engine) as session:
        # Add companies
        for company in companies:
            session.add(company)
        session.commit()
        # Add users
        for user in users:
            session.add(user)
        session.commit()
def get_db_context(table_name: str,size: int = 5):
    result = []
    if table_name == "company":
        from database.schema import Company as Default
    elif table_name == "user":    
        from database.schema import User as Default
    with Session(engine) as session:
        stmt = select(Default).limit(size)
        data = session.exec(stmt)
        for row in data:
            result.append(row)

    table_columns = Default.__table__.columns.keys()
    context_str = " | ".join(table_columns)
    for row in result:
        context_str += "\n"
        context_str += " | ".join([str(getattr(row, col)) for col in table_columns])

    return context_str



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Database")
    parser.add_argument(
        "--task",
        choices=["insert", "init"],
        default="insert"
    )
    args = parser.parse_args()

    if args.task == "insert":
        insert_to_db()
    elif args.task == "init":
        init_db()

