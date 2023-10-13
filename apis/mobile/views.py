from flask import jsonify, request
from flask.views import MethodView
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import check_password_hash

from configs import SQL_Server
from models import Medical_Staff, Medical_Records, MedicationTime, Patient, Ward_Bed

engine = create_engine(SQL_Server)
Session = sessionmaker(bind=engine)
dbsession = Session()

class Login(MethodView):
    def post(self):
        try:
            data = request.get_json()
            row = dbsession.query(Medical_Staff).filter_by(ms_id=data["account"]).first()
            if row and check_password_hash(row.pwd, data["password"]):
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
            print(data)
            patient_data = dbsession.query(Patient).filter_by(medical_record_number=data["medicalRecordNumber"]).first()
            ward_data = dbsession.query(Ward_Bed).filter_by(
                medical_record_number=data["medicalRecordNumber"],
                medical_record_id=data["medicalRecordId"]
            ).first()
            medical_records_data = dbsession.query(Medical_Records).filter_by(
                medical_record_number=data["medicalRecordNumber"],
                id=data["medicalRecordId"]
            ).first()
            cases = medical_records_data.cases.split(", ")
            medication = medical_records_data.medication.split(", ")
            notice = medical_records_data.notice.split(", ")
            birthday = patient_data.birthday.strftime("%Y-%m-%d")
            data = {
                "name": patient_data.name,
                "gender": patient_data.gender,
                "medicalRecordNumber": patient_data.medical_record_number,
                "wardNumber": ward_data.ward_id,
                "birthday": birthday,
                "bedNumber": ward_data.bed_number,
                "medication": medication,
                "notice": notice,
                "cases": cases
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


class UploadMedicalRecord(MethodView):
    def post(self):
        try:
            data = request.get_json()
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
                row = db.query(MedicationTime).filter(
                    MedicationTime.medical_record_number == data.get('medicalRecordNumber'),
                    MedicationTime.medical_record_id == data.get('medicalRecordID'),
                    MedicationTime.time.like(data.get('date')+'%')
                ).all()
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
            patient_data = dbsession.query(Patient).filter_by(medical_record_number=input_data["medicalRecordNumber"]).first()
            ward_data = dbsession.query(Ward_Bed).filter_by(
                medical_record_number=input_data["medicalRecordNumber"],
                medical_record_id=input_data['medicalRecordID']
            ).first()
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
