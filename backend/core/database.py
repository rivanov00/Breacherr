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

    final_data = []

    lines = RAW_DATA.strip().split('\n')
    header_skipped = False
    for line in lines:
        if not header_skipped:
            header_skipped = True
            continue

        parts = line.split(',')
        if len(parts) >= 5:

            if len(parts) == 6:

                name = parts[1].strip()
                email = parts[3].strip()
                password = parts[4].strip()
                reg_date = parts[5].strip()
            else:

                name = parts[0].strip()
                email = parts[2].strip()
                password = parts[3].strip()
                reg_date = parts[4].strip()

            final_data.append({
                "email": email,
                "name": "Local Leak Database",
                "title": f"Компрометиран запис: {name}",
                "domain": "internal-leak.bg",
                "breach_date": reg_date,
                "password": password,
                "description": "Този запис е открит в локален списък с компрометирани данни. Препоръчваме незабавна смяна на паролата за всички свързани услуги.",
                "data_classes": json.dumps(["Имейл адреси", "Пароли", "Потребителски имена"])
            })

    for item in final_data:
        db_breach = Breach(**item)
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
