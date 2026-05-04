from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

SQLALCHEMY_DATABASE_URL = "sqlite:///./breacherr.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Breach(Base):
    __tablename__ = "breaches"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    name = Column(String)
    title = Column(String)
    domain = Column(String)
    breach_date = Column(String)
    description = Column(Text)
    data_classes = Column(Text) 
    password = Column(String) 

def init_db():
    Base.metadata.create_all(bind=engine)

from core.local_leaks import RAW_DATA

def seed_db():
    db = SessionLocal()

    if db.query(Breach).first():
        db.close()
        return

    for item in RAW_DATA:
        db_breach = Breach(
            email=item["email"],
            name="Local Leak Database",
            title=f"Компрометиран запис: {item['source']}",
            domain=item["source"].lower().replace(" ", "") + ".com",
            breach_date=item["date"],
            password="N/A",
            description=f"Този запис е открит в {item['source']}. Препоръчваме проверка на сигурността.",
            data_classes=json.dumps(["Имейл адрес"])
        )
        db.add(db_breach)

    db.commit()
    db.close()

def search_local_breaches(email=None, name=None):
    db = SessionLocal()
    query = db.query(Breach)

    if email:
        query = query.filter(Breach.email == email)
    if name:
        query = query.filter(Breach.title.contains(name))

    results = query.all()
    db.close()

    formatted = []
    for r in results:

        formatted.append({
            "Name": r.name,
            "Title": r.title,
            "Domain": r.domain,
            "Email": r.email, 
            "BreachDate": r.breach_date,
            "Description": r.description,
            "DataClasses": json.loads(r.data_classes),
            "PasswordSnippet": f"{r.password[:2]}***{r.password[-1:]}" if r.password else "N/A"
        })
    return formatted
