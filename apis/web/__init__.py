from flask import Blueprint
from .views import *

web_bp = Blueprint('web', __name__, template_folder='templates')

web_bp.add_url_rule('/login', view_func=Login.as_view('login'), methods=['GET', 'POST'])
web_bp.add_url_rule('/index', view_func=Index.as_view('admin'), methods=['GET', 'POST'])
web_bp.add_url_rule('/personnel', view_func=Personnel.as_view('personnel'), methods=['GET', 'POST', 'PUT', 'DELETE'])
web_bp.add_url_rule('/medications', view_func=Medicine.as_view('medicine'), methods=['GET', 'POST', 'PUT', 'DELETE'])
web_bp.add_url_rule('/patient', view_func=Patient.as_view('patient'), methods=['GET', 'POST', 'PUT', 'DELETE'])
# web_bp.add_url_rule('/medical_records', view_func=MedicalRecord.as_view('medical_record'), methods=['GET', 'POST', 'PUT', 'DELETE'])
# web_bp.add_url_rule('/ward', view_func=Ward.as_view('ward'), methods=['GET', 'POST', 'PUT', 'DELETE'])
web_bp.add_url_rule('/database', view_func=Database.as_view('database'), methods=['GET', 'POST', 'PUT', 'DELETE'])
web_bp.add_url_rule('/settings', view_func=Setting.as_view('setting'), methods=['GET', 'POST', 'PUT', 'DELETE'])
