import json
import random
import time

from flask import jsonify, redirect, render_template, request, session, url_for
from flask.views import MethodView
from paho.mqtt import client as MQTT
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash
from uuid import uuid4

from configs import SQL_Server, MQTT_IP, MQTT_PORT
from models import Medication, Medical_Records, Medical_Staff, Patient, Ward_Bed

engine = create_engine(SQL_Server)
Session = sessionmaker(bind=engine)
client = MQTT.Client()

class Login_Check():
    def login_required():
        if session.get('ms_id') is None:
            return None
        else:
            with Session.begin() as db:
                try:
                    row = db.query(Medical_Staff).filter(Medical_Staff.ms_id == session.get('ms_id')).first()
                    return row.permissions
                except Exception as e:
                    print(e)
                    return None


class Login(MethodView):
    def get(self):
        session.clear()
        return render_template('login.html')

    def post(self):
        try:
            with Session.begin() as db:
                data = request.get_json()
                row = db.query(Medical_Staff).filter(Medical_Staff.ms_id == data.get('username')).first()
                if row and check_password_hash(row.pwd, data.get('password')):
                    session['ms_id'] = row.ms_id
                    result = {
                        "result": 0,
                        "message": "成功"
                    }
                else:
                    result = {
                        "result": 1,
                        "message": "帳號或密碼錯誤",
                    }
        except Exception as e:
            print(e)
            result = {
                "result": 1,
                "message": str(e),
            }
        return jsonify(result)


class Index(MethodView):
    def get(self):
        permissions = Login_Check.login_required()
        if permissions == None:
            return redirect(url_for('web.login'))
        else:
            return render_template('index.html', permissions=permissions)


class Personnel(MethodView):
    def get(self):
        permissions = Login_Check.login_required()
        if permissions == None:
            return redirect(url_for('web.login'))
        else:
            try:
                with Session.begin() as db:
                    row = db.query(Medical_Staff).order_by(Medical_Staff.ms_id).all()
                    data = []
                    for i in row:
                        if i.permissions != 0:
                            data.append({
                                "ms_id": i.ms_id,
                                "name": i.name,
                                "permissions": i.permissions
                            })
                    return render_template('personnel.html', permissions=permissions, personnel_data=json.dumps(data))
            except Exception as e:
                print(e)
                return redirect(url_for('web.index'))

    def post(self):
        data = request.get_json()
        if data.get('action') == 'add':
            try:
                with Session.begin() as db:
                    db.add(Medical_Staff(
                        uid=uuid4(),
                        name=data.get('name'),
                        ms_id=data.get('ms_id'),
                        pwd=generate_password_hash(data.get('password')),
                        permissions=data.get('permissions')
                    ))
                    db.commit()
                    result = {
                        "result": 0,
                        "message": "成功",
                    }
            except Exception as e:
                print(e)
                result = {
                    "result": 1,
                    "message": str(e),
                }
        elif data.get('action') == 'search':
            with Session.begin() as db:
                try:
                    row = db.query(Medical_Staff).filter(Medical_Staff.ms_id.like(data.get('ms_id')+'%')).all()
                    data = []
                    for i in row:
                        if i.permissions != 0:
                            data.append({
                                "ms_id": i.ms_id,
                                "name": i.name,
                                "permissions": i.permissions
                            })
                    result = {
                        "result": 0,
                        "message": "成功",
                        "data": data
                    }
                except Exception as e:
                    print(e)
                    result = {
                        "result": 1,
                        "message": "失敗" + str(e),
                    }
        elif data.get('action') == 'detail':
            try:
                with Session.begin() as db:
                    row = db.query(Medical_Staff).filter(Medical_Staff.ms_id==data.get('ms_id')).first()
                    result = {
                        "result": 0,
                        "message": "成功",
                        "data": {
                            "uid": row.uid,
                            "ms_id": row.ms_id,
                            "name": row.name,
                            "permissions": row.permissions
                    }}
            except Exception as e:
                print(e)
                result = {
                    "result": 1,
                    "message": "失敗" + str(e),
                }
        return jsonify(result)

    def delete(self):
        ms_id = request.get_json().get('ms_id')
        try:
            with Session.begin() as db:
                for i in ms_id:
                    db.query(Medical_Staff).filter(Medical_Staff.ms_id == i).delete()
                    db.commit()
                result = {
                    "result": 0,
                    "message": "成功",
                }
        except Exception as e:
            print(e)
            result = {
                "result": 1,
                "message": "失敗" + str(e),
            }
        return jsonify(result)

    def put(self):
        data = request.get_json()
        try:
            with Session.begin() as db:
                db.query(Medical_Staff).filter(Medical_Staff.uid == data.get('uid')).update({
                    "ms_id": data.get('ms_id'),
                    "name": data.get('name'),
                    "permissions": data.get('permissions')
                })
                db.commit()
                result = {
                    "result": 0,
                    "message": "成功",
                }
        except Exception as e:
            print(e)
            result = {
                "result": 1,
                "message": "失敗" + str(e),
            }
        return jsonify(result)


class Medicine(MethodView):
    def get(self):
        permissions = Login_Check.login_required()
        if permissions == None:
            return redirect(url_for('web.login'))
        else:
            try:
                with Session.begin() as db:
                    row = db.query(Medication).all()
                    data = []
                    for i in row:
                        data.append({
                            "id": i.id,
                            "name": i.name,
                            "effect": i.effect,
                            "side_effect": i.side_effect,
                            "drug_class": i.drug_class
                        })
                    return render_template('medications.html', permissions=permissions, medical_data=json.dumps(data))
            except Exception as e:
                print(e)
                return redirect(url_for('web.index'))

    def post(self):
        data = request.get_json()
        if data['action'] == 'add':
            try:
                with Session.begin() as db:
                    db.add(Medication(
                        name=data.get('name'),
                        effect=data.get('effect'),
                        side_effect=data.get('side_effect'),
                        drug_class=data.get('class')
                    ))
                    db.commit()
                    result = {
                        "result": 0,
                        "message": "成功",
                    }
            except Exception as e:
                print(e)
                result = {
                    "result": 1,
                    "message": str(e),
                }
        elif data['action'] == 'search':
            with Session.begin() as db:
                try:
                    medical_class = {
                        "injection": 0,
                        "oral": 1,
                        "external": 2,
                        "other": 3
                    }
                    if data.get('class') == 'all':
                        row = db.query(Medication).filter(Medication.name.like(data.get('name')+'%')).all()
                    else:
                        row = db.query(Medication).filter(
                            Medication.name.like(data.get('name')+'%'), 
                            Medication.drug_class==medical_class.get(data.get('class'))
                        ).all()
                    data = []
                    for i in row:
                        data.append({
                            "id": i.id,
                            "name": i.name,
                            "effect": i.effect,
                            "side_effect": i.side_effect,
                            "drug_class": i.drug_class
                        })
                    result = {
                        "result": 0,
                        "message": "成功",
                        "data": data
                    }
                except Exception as e:
                    print(e)
                    result = {
                        "result": 1,
                        "message": str(e),
                    }
        elif data['action'] == 'detail':
            try:
                with Session.begin() as db:
                    row = db.query(Medication).filter(Medication.id==data.get('id')).first()
                    result = {
                        "result": 0,
                        "message": "成功",
                        "data": {
                            "id": row.id,
                            "name": row.name,
                            "effect": row.effect,
                            "side_effect": row.side_effect,
                            "drug_class": row.drug_class
                    }}
            except Exception as e:
                print(e)
                result = {
                    "result": 1,
                    "message": str(e),
                }
        return jsonify(result)
    
    def put(self):
        data = request.get_json()
        try:
            with Session.begin() as db:
                db.query(Medication).filter(Medication.id == data.get('id')).update({
                    "name": data.get('name'),
                    "effect": data.get('effect'),
                    "side_effect": data.get('side_effect'),
                    "drug_class": data.get('class')
                })
                db.commit()
                result = {
                    "result": 0,
                    "message": "成功"
                }
        except Exception as e:
            print(e)
            result = {
                "result": 1,
                "message": str(e)
            }
        return jsonify(result)
    
    def delete(self):
        id = request.get_json().get('id')
        try:
            with Session.begin() as db:
                for i in id:
                    db.query(Medication).filter(Medication.id == i).delete()
                    db.commit()
                result = {
                    "result": 0,
                    "message": "成功",
                }
        except Exception as e:
            print(e)
            result = {
                "result": 1,
                "message": str(e),
            }
        return jsonify(result)


class PatientURL(MethodView):
    def get(self):
        permissions = Login_Check.login_required()
        if permissions == None:
            return redirect(url_for('web.login'))
        else:
            try:
                with Session.begin() as db:
                    row = db.query(Patient).all()
                    data = []
                    for i in row:
                        gender = "男" if i.gender == 1 else "女"
                        data.append({
                            "id": i.id,
                            "medical_record_number": i.medical_record_number,
                            "name": i.name,
                            "gender": gender,
                            "age": time.localtime().tm_year - i.birthday.year,
                            "birthday": i.birthday.strftime("%Y-%m-%d")
                        })
                    return render_template('patients.html', permissions=permissions, patient_data=json.dumps(data))
            except Exception as e:
                print(e)
                return redirect(url_for('web.index'))
            
    def post(self):
        data = request.get_json()
        if data.get('action') == 'search':
            try:
                with Session.begin() as db:                    
                    row = db.query(Patient).filter(
                        Patient.medical_record_number.like(
                            data.get('medical_record_number')+'%'
                    )).all()
                    data = []
                    for i in row:
                        gender = "男" if i.gender == 1 else "女"
                        data.append({
                            "id": i.id,
                            "medical_record_number": i.medical_record_number,
                            "health_id": i.health_id,
                            "name": i.name,
                            "gender": gender,
                            "age": time.localtime().tm_year - i.birthday.year,
                            "birthday": i.birthday.strftime("%Y-%m-%d")
                        })
                    result = {
                        "result": 0,
                        "message": "成功",
                        "data": data
                    }
            except Exception as e:
                print(e)
                result = {
                    "result": 1,
                    "message": str(e),
                }
        elif data.get("action") == 'add':
            try:
                with Session.begin() as db:
                    medical_record_number = ''.join(random.sample('0123456789', 8))
                    health_id = ' '.join([data.get('health_id')[i:i+4] for i in range(0, len(data.get('health_id')), 4)])
                    db.add(Patient(
                        health_id = health_id,
                        medical_record_number = 'P-' + medical_record_number,
                        name = data.get('name'),
                        gender = data.get('gender'),
                        birthday = data.get('birthday')
                    ))
                    db.commit()
                    result = {
                        "result": 0,
                        "message": "成功"
                    }
            except Exception as e:
                print(e)
                result = {
                    "result": 1,
                    "message": str(e)
                }
        return jsonify(result)
    
    def put(self):
        data = request.get_json()
        try:
            with Session.begin() as db:
                db.query(Patient).filter(Patient.medical_record_number == data.get('medical_record_number')).update({
                    "health_id": data.get('health_id'),
                    "name": data.get('name'),
                    "gender": data.get('gender'),
                    "birthday": data.get('birthday')
                })
                db.commit()
                result = {
                    "result": 0,
                    "message": "成功"
                }
        except Exception as e:
            print(e)
            result = {
                "result": 1,
                "message": str(e)
            }
        return jsonify(result)


class PatientMedicalRecord(MethodView):
    def get(self, id):
        permissions = Login_Check.login_required()
        if permissions == None:
            return redirect(url_for('web.login'))
        else:
            try:
                with Session.begin() as db:
                    patient = db.query(Patient).filter(Patient.medical_record_number == id)[0]
                    patient = {
                        "id": patient.id,
                        "medical_record_number": patient.medical_record_number,
                        "health_id": patient.health_id,
                        "name": patient.name,
                        "gender": patient.gender,
                        "birthday": patient.birthday.strftime("%Y-%m-%d"),
                        "age": time.localtime().tm_year - patient.birthday.year,
                        "height": patient.height,
                        "weight": patient.weight
                    }
                    medical_records = db.query(Medical_Records).filter(Medical_Records.medical_record_number == id).all()
                    medical_records_data = []
                    for i in medical_records:
                        doctor = db.query(Medical_Staff).filter(Medical_Staff.ms_id == i.doctor)[0]
                        medical_records_data.append({
                            "id": i.id,
                            "medical_record_number": i.medical_record_number,
                            "cases": i.cases,
                            "medication": i.medication,
                            "notice": i.notice,
                            "hospitalization": i.hospitalization,
                            "doctor": doctor.name,
                            "doctorid": i.doctor,
                            "time": i.time.strftime("%Y-%m-%d")
                        })
                    return render_template(
                        'patient.html', 
                        permissions=permissions,
                        name=patient.get('name'),
                        patient=json.dumps(patient), 
                        medical_records=json.dumps(medical_records_data)
                    )
            except Exception as e:
                print(e)
                return redirect(url_for('web.index'))
            
    def put(self, id):
        try:
            with Session.begin() as db:
                db.query(Patient).filter(Patient.medical_record_number == id).update({
                    "height": request.get_json().get('height'),
                    "weight": request.get_json().get('weight')
                })
                db.commit()
                result = {
                    "result": 0,
                    "message": "成功"
                }
        except Exception as e:
            print(e)
            result = {
                "result": 1,
                "message": str(e)
            }
        return jsonify(result)


class AddMedicalRecord(MethodView):
    def get(self, id):
        permissions = Login_Check.login_required()
        if permissions == None:
            return redirect(url_for('web.login'))
        else:
            try:
                with Session.begin() as db:
                    patient = db.query(Patient).filter(Patient.medical_record_number == id)[0]
                    patient = {
                        "id": patient.id,
                        "medical_record_number": patient.medical_record_number,
                        "health_id": patient.health_id,
                        "name": patient.name,
                        "gender": patient.gender,
                        "birthday": patient.birthday.strftime("%Y-%m-%d"),
                        "age": time.localtime().tm_year - patient.birthday.year,
                        "height": patient.height,
                        "weight": patient.weight
                    }
                    return render_template(
                        'AddMedicalRecord.html', 
                        permissions=permissions, 
                        name = patient.get('name'),
                        patient=json.dumps(patient))
            except Exception as e:
                print(e)
                return redirect(url_for('web.index'))
        
    def post(self, id):
        data = request.get_json()
        try:
            with Session.begin() as db:
                cases = ', '.join(data.get('content', []))
                medication = ', '.join(data.get('medicine', []))
                db.add(Medical_Records(
                    medical_record_number = data.get('medical_record_number'),
                    cases = cases,
                    medication = medication,
                    notice = data.get('notice'),
                    hospitalization = data.get('hospitalization'),
                    doctor = data.get('doctorid'),
                    time = data.get('datetime')
                ))
                db.commit()
                if data.get('hospitalization') == True:
                    with Session.begin() as db:
                        medical_record_id = db.query(Medical_Records).filter(Medical_Records.medical_record_number == data.get('medical_record_number')).order_by(Medical_Records.time.desc())[0].id
                        db.add(Ward_Bed(
                            ward_id = data.get('ward'),
                            bed_number = data.get('bed'),
                            medical_record_number = data.get('medical_record_number'),
                            medical_record_id = medical_record_id,
                            time = data.get('datetime')
                        ))
                        db.commit()
                    client.connect(MQTT_IP, MQTT_PORT, 60)
                    client.publish("ACET/ward/info", json.dumps({
                        "medical_record_number": data.get('medical_record_number'),
                        "medical_record_id": medical_record_id,
                        "name": data.get('name'),
                        "case": cases,
                        "medication": medication,
                        "notice": data.get('notice'),
                        "ward": data.get('ward'),
                        "bed": data.get('bed'),
                    }))
                result = {
                    "result": 0,
                    "message": "成功"
                }
        except Exception as e:
            print(e)
            result = {
                "result": 1,
                "message": str(e)
            }
        return jsonify(result)


class ViewMedicalRecord(MethodView):
    def get(self, pid, mid):
        permissions = Login_Check.login_required()
        if permissions == None:
            return redirect(url_for('web.login'))
        else:
            try:
                with Session.begin() as db:
                    patient = db.query(Patient).filter(Patient.medical_record_number == pid)[0]
                    medical_rocord = db.query(Medical_Records).filter(Medical_Records.id == mid)[0]
                    cases = medical_rocord.cases.split(', ')
                    medication = medical_rocord.medication.split(', ')
                    data = {
                        "medical_record_number": patient.medical_record_number,
                        "name": patient.name,
                        "gender": patient.gender,
                        "birthday": patient.birthday.strftime("%Y-%m-%d"),
                        "age": time.localtime().tm_year - patient.birthday.year,
                        "height": patient.height,
                        "weight": patient.weight,
                        "datetime": medical_rocord.time.strftime("%Y-%m-%d %H:%M"),
                        "doctorid": medical_rocord.doctor,
                        "cases": cases,
                        "medication": medication,
                        "notice": medical_rocord.notice,
                        "hospitalization": medical_rocord.hospitalization
                    }
                    if medical_rocord.hospitalization == True:
                        ward = db.query(Ward_Bed).filter(Ward_Bed.medical_record_number == pid, Ward_Bed.medical_record_id == mid)[0]
                        data.update({
                            "ward": ward.ward_id,
                            "bed": ward.bed_number
                        })
                    return render_template(
                        'ViewMedicalRecord.html', 
                        permissions=permissions, 
                        name = data.get('name'),
                        data=json.dumps(data))
            except Exception as e:
                print(e)
                return redirect(url_for('web.index'))
            


class MedicalRecord(MethodView):
    def get(self):
        permissions = Login_Check.login_required()
        if permissions == None:
            return redirect(url_for('web.login'))
        else:
            try:
                with Session.begin() as db:
                    row = db.query(Medical_Records).all()
                    data = []
                    for i in row:
                        doctor = db.query(Medical_Staff).filter(Medical_Staff.ms_id == i.doctor)[0]
                        data.append({
                            "id": i.id,
                            "medical_record_number": i.medical_record_number,
                            "cases": i.cases,
                            "medication": i.medication,
                            "notice": i.notice,
                            "hospitalization": i.hospitalization,
                            "doctor_id": doctor.ms_id,
                            "doctor": doctor.name,
                            "time": i.time.strftime("%Y-%m-%d")
                        })
                    return render_template('MedicalRecord.html', permissions=permissions, data=json.dumps(data))
            except Exception as e:
                print(e)
                return redirect(url_for('web.index'))
            
    def post(self):
        data = request.get_json()
        with Session.begin() as db:
            try:
                row = db.query(Medical_Records).filter(
                    Medical_Records.medical_record_number.like(
                        data.get('medical_record_number')+'%'),
                    Medical_Records.doctor.like(data.get('ms_id')+'%')
                ).all()
                data = []
                for i in row:
                    doctor = db.query(Medical_Staff).filter(Medical_Staff.ms_id == i.doctor)[0]
                    data.append({
                        "id": i.id,
                        "medical_record_number": i.medical_record_number,
                        "cases": i.cases,
                        "medication": i.medication,
                        "notice": i.notice,
                        "hospitalization": i.hospitalization,
                        "doctor_id": doctor.ms_id,
                        "doctor": doctor.name,
                        "time": i.time.strftime("%Y-%m-%d")
                    })
                result = {
                    "result": 0,
                    "message": "成功",
                    "data": data
                }
            except Exception as e:
                print(e)
                result = {
                    "result": 1,
                    "message": str(e),
                }
        return jsonify(result)


class WardBed(MethodView):
    def get(self):
        permissions = Login_Check.login_required()
        if permissions == None:
            return redirect(url_for('web.login'))
        else:
            try:
                with Session.begin() as db:
                    row = db.query(Ward_Bed).all()
                    data = []
                    for i in row:
                        patient = db.query(Patient).filter(Patient.medical_record_number == i.medical_record_number).first()
                        data.append({
                            "id": i.id,
                            "medical_record_id": i.medical_record_id,
                            "medical_record_number": i.medical_record_number,
                            "name": patient.name,
                            "ward_id": i.ward_id,
                            "bed_number": i.bed_number,
                            "time": i.time.strftime("%Y-%m-%d")
                        })
                    return render_template(
                        'WardBed.html', 
                        permissions=permissions, 
                        data=json.dumps(data)
                    )
            except Exception as e:
                print(e)
                return redirect(url_for('web.index'))

    def post(self):
        data = request.get_json()
        with Session.begin() as db:
            try:
                row = db.query(Ward_Bed).filter(
                    Ward_Bed.medical_record_number.like(
                        data.get('medical_recode_number')+'%'
                )).all()
                data = []
                for i in row:
                    patient = db.query(Patient).filter(Patient.medical_record_number == i.medical_record_number)[0]
                    data.append({
                        "id": i.id,
                        "medical_record_id": i.medical_record_id,
                        "medical_record_number": i.medical_record_number,
                        "name": patient.name,
                        "ward_id": i.ward_id,
                        "bed_number": i.bed_number,
                        "time": i.time.strftime("%Y-%m-%d")
                    })
                result = {
                    "result": 0,
                    "message": "成功",
                    "data": data
                }
            except Exception as e:
                print(e)
                result = {
                    "result": 1,
                    "message": str(e),
                }
        return jsonify(result)


class Database(MethodView):
    def get(self):
        permissions = Login_Check.login_required()
        if permissions == None:
            return redirect(url_for('web.login'))
        else:
            return render_template('database.html', permissions=permissions)


class Setting(MethodView):
    def get(self):
        permissions = Login_Check.login_required()
        if permissions == None:
            return redirect(url_for('web.login'))
        else:
            return render_template('settings.html', permissions=permissions)
