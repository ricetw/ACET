import json

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from uuid import uuid4
from werkzeug.security import generate_password_hash

from models import Medical_Staff, Medication
from configs import SQL_Server

engine = create_engine(SQL_Server)
Session = sessionmaker(bind=engine)
session = Session()

try:
    with open("Medical_Staff.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for item in data:
            session.add(Medical_Staff(
                uid=uuid4(),
                name=item["name"],
                ms_id=item["ms_id"],
                pwd=generate_password_hash(item["pwd"]),
                permissions=item["permissions"]
            ))
    session.commit()
except Exception as e:
    print(e)
    session.rollback()

try:
    with open("Medication.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for item in data:
            session.add(Medication(
                name=item["name"],
                effect=item["effect"] if item["effect"] else "None",
                side_effect=item["side_effect"] if item["side_effect"] else "None",
                drug_class=item["drug_class"]
            ))
    session.commit()
except Exception as e:
    print(e)
    session.rollback()