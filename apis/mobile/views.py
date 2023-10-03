import json

from flask import jsonify, redirect, render_template, request, session, url_for
from flask.views import MethodView
from sqlalchemy import and_, create_engine, text
from sqlalchemy.orm import sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash
from uuid import uuid4

from configs import SQL_Server, medical_staff, medical_records, medication, patient, ward
from models import *

engine = create_engine(SQL_Server)
Session = sessionmaker(bind=engine)
dbsession = Session()

class Login(MethodView):
    def post(self):
        try:
            data = request.get_json()
            data = {
                "ms_id": data["account"],
                "password": data["password"]
            }
            sql = text('select * from {} where ms_id = :ms_id'.format(medical_staff))
            row = dbsession.execute(sql, data).fetchall()
            if row and check_password_hash(row[0].pwd, data["password"]):
                result = {
                    "result": 0,
                    "data": "帳號登入成功",
                    "message": "success"
                }
            else:
                result = {
                    "result": 1,
                    "data": "帳號或密碼錯誤",
                    "message": "fail"
                }
        except Exception as e:
            print(e)
            result = {
                "result": 1,
                "data": "帳號或密碼錯誤",
                "message": "fail"
            }
        return jsonify(result)


class PatientInfo(MethodView):
    def post(self):
        try:
            data = request.get_json()
            patient_data = dbsession.query(Patient).filter_by(medical_record_number=data["medicalRecordNumber"]).first()
            ward_data = dbsession.query(Ward_Bed).filter_by(medical_record_number=data["medicalRecordNumber"]).first()
            medical_records_data = dbsession.query(Medical_Records).filter_by(
                medical_record_number=data["medicalRecordNumber"], time=ward_data.time, hospitalization=True
            ).first()
            cases = medical_records_data.cases.split(", ")
            medication = medical_records_data.medication.split(", ")
            notice = medical_records_data.notice.split(", ")
            birthday = patient_data.birthday.strftime("%Y-%m-%d")
            result = {
                "result": 0,
                "data": {
                    "name": patient_data.name,
                    "gender": patient_data.gender,
                    "medicalRecordNumber": patient_data.medical_record_number,
                    "wardNumber": ward_data.ward_id,
                    "birthday": birthday,
                    "bedNumber": ward_data.bed_number,
                    "medication": medication,
                    "notice": notice,
                    "cases": cases
                },
                "message": "success"
            }
        except Exception as e:
            print(e)
            result = {
                "result": 1,
                "data": "查無資料",
                "message": "fail"
            }
        return jsonify(result)


class UploadMedicalRecord(MethodView):
    def post(self):
        try:
            data = request.get_json()
            print(data)
            dbsession.add(MedicationTime(
                medical_record_id = data.get('medicalRecordID'),
                medical_record_number = data.get('medicalRecordNumber'),
                medication = data.get('medication'),
                drug_class =  data.get("drugClass"),
                notice = data.get('notice'),
                doctor = data.get('ms_id'),
                time = data.get('time')
            ))
            dbsession.commit()
            result = {
                "result": 0,
                "data": "上傳成功",
                "message": "success"
            }
        except Exception as e:
            print(e)
            result = {
                "result": 1,
                "data": "上傳失敗",
                "message": "fail"
            }
        return jsonify(result)


class GetMedicalRecord(MethodView):
    def post(self):
        try:
            with Session.begin() as db:
                data = request.get_json()
                print(data)
                row = db.query(MedicationTime).filter(
                    MedicationTime.medical_record_number == data.get('medicalRecordNumber'),
                    MedicationTime.medical_record_id == data.get('medicalRecordID'),
                    MedicationTime.time.like(data.get('date')+'%')
                ).all()
                print(row)
                data = []
                for i in row:
                    data.append({
                        "id": i.id,
                        "time": i.time.strftime("%H:%M"),
                        "drugName": i.medication,
                        "drugClass": i.drug_class,
                        "note": i.notice
                    })
                result = {
                    "result": 0,
                    "data": data,
                    "message": "sussess"
                }
        except Exception as e:
            print(e)
            result = {
                "result": 1,
                "data": "獲取失敗",
                "message": "fail"
            }
        return jsonify(result)


class Index(MethodView):
    def post(self):
        try:
            input_data = request.get_json()
            data = {}
            patient_data = dbsession.query(Patient).filter_by(medical_record_number=input_data["medicalRecordNumber"])[0]
            ward_data = dbsession.query(Ward_Bed).filter_by(
                medical_record_number=input_data["medicalRecordNumber"],
                medical_record_id=input_data['medicalRecordID']
            )[0]
            data = {
                "medicalRecordNumber": patient_data.medical_record_number,
                "name": patient_data.name,
                "medicalRecordID": ward_data.medical_record_id,
                "wardNumber": ward_data.ward_id,
                "bedNumber": ward_data.bed_number
            }
            result = {
                "result": 0,
                "data": data,
                "message": "success"
            }
        except Exception as e:
            print(e)
            result = {
                "result": 1,
                "data": "查無資料",
                "message": "fail"
            }
        return jsonify(result)
