import json

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
                "message": "成功",
            }
        except Exception as e:
            print(e)
            result = {
                "result": 1,
                "message": str(e),
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


class Patient(MethodView):
    def get(self):
        permissions = Login_Check.login_required()
        if permissions != 4:
            return render_template('patient.html', permissions=permissions)
        else:
            return redirect(url_for('web.login'))


class Database(MethodView):
    def get(self):
        permissions = Login_Check.login_required()
        if permissions != 4:
            return render_template('database.html', permissions=permissions)
        else:
            return redirect(url_for('web.login'))


class Setting(MethodView):
    def get(self):
        permissions = Login_Check.login_required()
        if permissions != 4:
            return render_template('settings.html', permissions=permissions)
        else:
            return redirect(url_for('web.login'))
