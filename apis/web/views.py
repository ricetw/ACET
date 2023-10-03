import datetime
import json
import random
import time

from flask import jsonify, redirect, render_template, request, session, url_for
from flask.views import MethodView
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash
from uuid import uuid4

from configs import SQL_Server, medical_staff, medical_records, medication, patient, ward
from models import *

engine = create_engine(SQL_Server)
Session = sessionmaker(bind=engine)
dbsession = Session()

class Login_Check():
    def login_required():
        if session.get('ms_id') is None:
            return None
        else:
            try:
                sql = text('select * from {medical_staff} where ms_id = :ms_id'.format(medical_staff=medical_staff))
                row = dbsession.execute(sql, [{'ms_id': session.get('ms_id')}]).fetchall()[0]
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
            data = request.get_json()
            ms_id = data.get('username')
            pwd = data.get('password')
            sql = text('select * from {medical_staff} where ms_id = :ms_id'.format(medical_staff=medical_staff))
            row = dbsession.execute(sql, [{'ms_id': ms_id}]).fetchall()
            if row and check_password_hash(row[0].pwd, pwd):
                session['ms_id'] = row[0].ms_id
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
                row = dbsession.execute(
                    text('select ms_id, name, permissions from {medical_staff}'.format(medical_staff=medical_staff))
                ).fetchall()
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
                dbsession.add(Medical_Staff(
                    uid=uuid4(),
                    name=data.get('name'),
                    ms_id=data.get('ms_id'),
                    pwd=generate_password_hash(data.get('password')),
                    permissions=data.get('permissions')
                ))
                dbsession.commit()
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
                    row = db.execute(
                        text(
                            "select ms_id, name, permissions from {medical_staff} where ms_id LIKE '{ms_id}%'".format(
                                medical_staff=medical_staff, 
                                ms_id=data.get('ms_id')
                    ))).fetchall()
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
                row = dbsession.execute(
                    text(
                        "select uid, ms_id, name, permissions from {medical_staff} where ms_id = :ms_id".format(
                            medical_staff=medical_staff
                    )),
                    [{"ms_id": data.get("ms_id")}]
                ).fetchall()[0]
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
            for i in ms_id:
                dbsession.query(Medical_Staff).filter(Medical_Staff.ms_id == i).delete()
                dbsession.commit()
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
            dbsession.query(Medical_Staff).filter(Medical_Staff.uid == data.get('uid')).update({
                "ms_id": data.get('ms_id'),
                "name": data.get('name'),
                "permissions": data.get('permissions')
            })
            dbsession.commit()
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
                sql = text('select * from {table}'.format(table=medication))
                row = dbsession.execute(sql).fetchall()
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
                dbsession.add(Medication(
                    name=data.get('name'),
                    effect=data.get('effect'),
                    side_effect=data.get('side_effect'),
                    drug_class=data.get('class')
                ))
                dbsession.commit()
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
                        row = db.execute(
                            text(
                                "select * from {medication} where name LIKE '{name}%'".format(
                                    medication=medication,
                                    name=data.get('name')
                            ))).fetchall()
                    else:
                        row = db.execute(
                            text(
                                "select * from {medication} where name LIKE '{name}%' and drug_class = {drug_class}".format(
                                    medication=medication,
                                    name=data.get('name'),
                                    drug_class=medical_class.get(data.get('class'))
                            ))).fetchall()
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
                row = dbsession.execute(
                    text(
                        "select * from {medication} where id = :id".format(
                            medication=medication
                    )),
                    [{"id": data.get("id")}]
                ).fetchall()[0]
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
            dbsession.query(Medication).filter(Medication.id == data.get('id')).update({
                "name": data.get('name'),
                "effect": data.get('effect'),
                "side_effect": data.get('side_effect'),
                "drug_class": data.get('class')
            })
            dbsession.commit()
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
            for i in id:
                dbsession.query(Medication).filter(Medication.id == i).delete()
                dbsession.commit()
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
                row = dbsession.query(Patient).all()
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
                    print(row)
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
                medical_record_number = ''.join(random.sample('0123456789', 8))
                health_id = ' '.join([data.get('health_id')[i:i+4] for i in range(0, len(data.get('health_id')), 4)])
                dbsession.add(Patient(
                    health_id = health_id,
                    medical_record_number = 'P-' + medical_record_number,
                    name = data.get('name'),
                    gender = data.get('gender'),
                    birthday = data.get('birthday')
                ))
                dbsession.commit()
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
            dbsession.query(Patient).filter(Patient.medical_record_number == data.get('medical_record_number')).update({
                "health_id": data.get('health_id'),
                "name": data.get('name'),
                "gender": data.get('gender'),
                "birthday": data.get('birthday')
            })
            dbsession.commit()
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
                patient = dbsession.query(Patient).filter(Patient.medical_record_number == id)[0]
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
                medical_records = dbsession.query(Medical_Records).filter(Medical_Records.medical_record_number == id).all()
                medical_records_data = []
                for i in medical_records:
                    doctor = dbsession.query(Medical_Staff).filter(Medical_Staff.ms_id == i.doctor)[0]
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
            dbsession.query(Patient).filter(Patient.medical_record_number == id).update({
                "height": request.get_json().get('height'),
                "weight": request.get_json().get('weight')
            })
            dbsession.commit()
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
                patient = dbsession.query(Patient).filter(Patient.medical_record_number == id)[0]
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
        print(data)
        try:
            cases = ', '.join(data.get('content', []))
            medication = ', '.join(data.get('medicine', []))
            print(data.get('datetime'))
            dbsession.add(Medical_Records(
                medical_record_number = data.get('medical_record_number'),
                cases = cases,
                medication = medication,
                notice = data.get('notice'),
                hospitalization = data.get('hospitalization'),
                doctor = data.get('doctorid'),
                time = data.get('datetime')
            ))
            dbsession.commit()
            if data.get('hospitalization') == True:
                medical_record_id = dbsession.query(Medical_Records).filter(Medical_Records.medical_record_number == data.get('medical_record_number')).order_by(Medical_Records.time.desc())[0].id
                dbsession.add(Ward_Bed(
                    ward_id = data.get('ward'),
                    bed_number = data.get('bed'),
                    medical_record_number = data.get('medical_record_number'),
                    medical_record_id = medical_record_id,
                    time = data.get('datetime')
                ))
                dbsession.commit()
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
                patient = dbsession.query(Patient).filter(Patient.medical_record_number == pid)[0]
                medical_rocord = dbsession.query(Medical_Records).filter(Medical_Records.id == mid)[0]
                cases = medical_rocord.cases.split(', ')
                medication = medical_rocord.medication.split(', ')
                ward = dbsession.query(Ward_Bed).filter(Ward_Bed.medical_record_number == pid, Ward_Bed.medical_record_id == mid).order_by(Ward_Bed.time.desc())[0]
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
                    "hospitalization": medical_rocord.hospitalization,
                    "ward": ward.ward_id,
                    "bed": ward.bed_number
                }
                print(data)
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
                row = dbsession.query(Medical_Records).all()
                print(row)
                data = []
                for i in row:
                    doctor = dbsession.query(Medical_Staff).filter(Medical_Staff.ms_id == i.doctor)[0]
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
                print(data)
                return render_template('MedicalRecord.html', permissions=permissions, data=json.dumps(data))
            except Exception as e:
                print(e)
                return redirect(url_for('web.index'))
            
    def post(self):
        data = request.get_json()
        print(data)
        print(type(data.get('date')))
        with Session.begin() as db:
            try:
                row =db.query(Medical_Records).filter(
                    Medical_Records.medical_record_number.like(
                        data.get('medical_record_number')+'%'),
                    Medical_Records.doctor.like(data.get('ms_id')+'%')
                ).all()
                print(row)
                data = []
                for i in row:
                    doctor = dbsession.query(Medical_Staff).filter(Medical_Staff.ms_id == i.doctor)[0]
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
                print(data)
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
                row = dbsession.query(Ward_Bed).all()
                data = []
                for i in row:
                    patient = dbsession.query(Patient).filter(Patient.medical_record_number == i.medical_record_number)[0]
                    data.append({
                        "id": i.id,
                        "medical_record_id": i.medical_record_id,
                        "medical_record_number": i.medical_record_number,
                        "name": patient.name,
                        "ward_id": i.ward_id,
                        "bed_number": i.bed_number,
                        "time": i.time.strftime("%Y-%m-%d")
                    })
                print(data)
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
        print(data)
        with Session.begin() as db:
            try:
                print( data.get('medical_recode_number'))
                row = db.query(Ward_Bed).filter(
                    Ward_Bed.medical_record_number.like(
                        data.get('medical_recode_number')+'%'
                )).all()
                print(row)
                data = []
                for i in row:
                    patient = dbsession.query(Patient).filter(Patient.medical_record_number == i.medical_record_number)[0]
                    data.append({
                        "id": i.id,
                        "medical_record_id": i.medical_record_id,
                        "medical_record_number": i.medical_record_number,
                        "name": patient.name,
                        "ward_id": i.ward_id,
                        "bed_number": i.bed_number,
                        "time": i.time.strftime("%Y-%m-%d")
                    })
                print(data)
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
