from flask import Blueprint
from .views import *

mobile_bp = Blueprint('mobile', __name__, template_folder='templates')

mobile_bp.add_url_rule('/login', view_func=Login.as_view('login'), methods=['GET', 'POST'])
mobile_bp.add_url_rule('/patientInfo', view_func=PatientInfo.as_view('patientInfo'), methods=['GET', 'POST'])
mobile_bp.add_url_rule('/uploadMedicalRecord', view_func=UploadMedicalRecord.as_view('uploadMedicalRecord'), methods=['GET', 'POST'])
mobile_bp.add_url_rule('/getMedicalRecord', view_func=GetMedicalRecord.as_view('getMedicalRecord'), methods=['GET', 'POST'])
mobile_bp.add_url_rule('/scanQRCode', view_func=Index.as_view('getMedicationTime'), methods=['GET', 'POST'])
