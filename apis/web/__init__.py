from flask import Blueprint
from .views import *

web_bp = Blueprint('web', __name__, template_folder='templates')

web_bp.add_url_rule('/login', view_func=Login.as_view('login'), methods=['GET', 'POST'])
web_bp.add_url_rule('/index', view_func=Index.as_view('admin'), methods=['GET', 'POST'])
web_bp.add_url_rule('/personnel', view_func=Personnel.as_view('personnel'), methods=['GET', 'POST', 'PUT', 'DELETE'])
web_bp.add_url_rule('/medications', view_func=Medicine.as_view('medicine'), methods=['GET', 'POST', 'PUT', 'DELETE'])
web_bp.add_url_rule('/patient', view_func=PatientURL.as_view('patient'), methods=['GET', 'POST', 'PUT', 'DELETE'])
web_bp.add_url_rule('/patient/<string:id>', view_func=PatientMedicalRecord.as_view('patientmedicalrecord'), methods=['GET', 'POST', 'PUT', 'DELETE'])
web_bp.add_url_rule('/medical_records', view_func=MedicalRecord.as_view('medicalrecords'), methods=['GET', 'POST', 'PUT', 'DELETE'])
web_bp.add_url_rule('/medical_record/<string:id>', view_func=ViewMedicalRecord.as_view('viewmedicalrecord'), methods=['GET', 'POST', 'PUT', 'DELETE'])
web_bp.add_url_rule('/medical_record/<string:id>/edit', view_func=EditMedicalRecord.as_view('editmedicalrecord'), methods=['GET', 'POST', 'PUT', 'DELETE'])
web_bp.add_url_rule('/medical_record/<string:id>/add', view_func=AddMedicalRecord.as_view('addmedicalrecord'), methods=['GET', 'POST', 'PUT', 'DELETE'])
# web_bp.add_url_rule('/ward', view_func=Ward.as_view('ward'), methods=['GET', 'POST', 'PUT', 'DELETE'])
web_bp.add_url_rule('/database', view_func=Database.as_view('database'), methods=['GET', 'POST', 'PUT', 'DELETE'])
web_bp.add_url_rule('/settings', view_func=Setting.as_view('setting'), methods=['GET', 'POST', 'PUT', 'DELETE'])
