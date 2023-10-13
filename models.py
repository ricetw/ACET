# -*- coding: UTF-8 -*-
import datetime

from configs import SQL_Server
from sqlalchemy import Boolean, Column, Date, DateTime, Float, Integer, String, TEXT
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


class Patient(Base):  # 病人
    __tablename__ = "Patient"
    id = Column(Integer, nullable=False, primary_key=True)
    health_id = Column(String(255), nullable=False, unique=True)
    medical_record_number = Column(String(255), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    gender = Column(Integer, nullable=False)
    birthday = Column(Date, nullable=False)
    height = Column(Float)
    weight = Column(Float)


class Medical_Records(Base):  # 病歷紀錄
    __tablename__ = "Medical_records"
    id = Column(Integer, nullable=False, primary_key=True)
    medical_record_number = Column(String(255), nullable=False)
    cases = Column(String(2048), nullable=False)
    medication = Column(String(2048), nullable=False)
    notice = Column(String(2048), nullable=False)
    hospitalization = Column(Boolean, nullable=False)
    doctor = Column(String(255), nullable=False)
    time = Column(DateTime(timezone=False), nullable=False)


class Ward_Bed(Base):  # 病床紀錄
    __tablename__ = "Ward"
    id = Column(Integer, nullable=False, primary_key=True)
    ward_id = Column(String(255), nullable=False)
    bed_number = Column(Integer, nullable=False)
    medical_record_number = Column(String(255), nullable=False)
    medical_record_id = Column(Integer, nullable=False)
    time = Column(DateTime(timezone=False), nullable=False)


class MedicationTime(Base):  # 用藥紀錄
    __tablename__ = "MedicationTime"
    id = Column(Integer, nullable=False, primary_key=True)
    medical_record_id = Column(Integer, nullable=False)
    medical_record_number = Column(String(255), nullable=False)
    medication = Column(String(255), nullable=False)
    drug_class = Column(Integer, nullable=False)
    notice = Column(String(255), nullable=False)
    doctor = Column(String(255), nullable=False)
    time = Column(DateTime(timezone=False), nullable=False)


if __name__ == "__main__":
    engine = create_engine(SQL_Server, echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
