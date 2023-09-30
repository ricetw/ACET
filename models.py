# -*- coding: UTF-8 -*-
import datetime
import os

from configs import SQL_Server
from sqlalchemy import ARRAY, Boolean, Column, DateTime, Float, Integer, String, TEXT
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class BaseTable():
    __table_args__ = {
        "mysql_charset": "utf8mb4"
    }
    count_log = Column(Integer, nullable=False, primary_key=True)
    time_stamp = Column(DateTime(timezone=False), nullable=False,
                        default=datetime.datetime.utcnow)


class Medical_Staff(Base):  # 醫護人員
    __tablename__ = "Medical_Staff"
    uid = Column(String(255), nullable=False, primary_key=True)
    name = Column(String(255), nullable=False)
    ms_id = Column(String(255), nullable=False, unique=True)
    pwd = Column(String(255), nullable=False)
    permissions = Column(Integer, nullable=False)  # 0: admin, 1: manger, 2: staff, 3:deactive


class Medication(Base):  # 藥物
    __tablename__ = "Medication"
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(255), nullable=False)
    effect = Column(TEXT(10000), nullable=False)
    side_effect = Column(TEXT(10000), nullable=False)
    drug_class = Column(Integer, nullable=False)  # 0:injection, 1:oral, 2:external, 3:other


class Patient(Base):
    __tablename__ = "Patient"
    id = Column(Integer, nullable=False, primary_key=True)
    health_id = Column(String(255), nullable=False, unique=True)
    medical_record_number = Column(String(255), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    gender = Column(Integer, nullable=False)
    birthday = Column(DateTime(timezone=False), nullable=False)


class Medical_Records(Base):
    __tablename__ = "Medical_records"
    id = Column(Integer, nullable=False, primary_key=True)
    medical_record_number = Column(String(255), nullable=False)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    cases = Column(String(2048), nullable=False)
    medication = Column(String(2048), nullable=False)
    notice = Column(String(2048), nullable=False)
    time = Column(DateTime(timezone=False), nullable=False)


class Ward_Bed(Base):
    __tablename__ = "Ward"
    id = Column(Integer, nullable=False, primary_key=True)
    ward_id = Column(String(255), nullable=False)
    bed_number = Column(Integer, nullable=False)
    medical_record_number = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)


if __name__ == "__main__":
    engine = create_engine(SQL_Server, echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)