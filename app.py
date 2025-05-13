from flask import Flask, send_from_directory
from flask_cors import CORS
import os

# === IMPORT BLUEPRINTS ===
from api.getlogin import login_api
from api.getOpen_id import getopenid_bp
from api.getSubject import subject_bp
from api.getStructure import structure_bp
from api.setOpensubject import opensubject_bp
from api.getOpensubject import get_opensubject_bp
from api.setAnswer import answer_bp
from api.setQuestion import question_bp
from api.dropOpensubject import dropOpen_bp
from api.setStandardPlan import set_standard_bp
from api.getStandardPlan import get_standard_bp
from api.dropStandardPlan import drop_standard_plan_bp
from api.getStandardList import get_standard_lsit_bp
from api.setStandardlist import set_standard_list_bp
from api.getStudent_plan import getstdPlan_bp
from api.getStudentplan_list import getStudentplan_list_bp
from api.setStudentplan_list import setstudentplan_list_bp
from api.dropStudentplan_list import dropstudentplan_list_bp
from api.updateStudentplan import updatestudent_plan_bp
from api.update_stdPlan_list import updateStudentplan_list_bp
from api.getTranfer_std_plan import getTranferPlan_bp
from api.setAdjustplan_list import setAdjustplan_list_bp
from api.getAdjust_list import getAdjust_list_bp
from api.getAdjust_plan import getAdjust_plan_bp
from api.update_adjust_plan import updateadjust_plan_bp
from api.pdf_generate import pdf_api
from api.getSyllabus import syllabus_bp
from api.pdf_summery_tranfer import pdf_tranfer
from api.pdf_summery_plan import pdf_plan

# === FLASK APP ===
app = Flask(__name__, static_folder='dist', static_url_path='')
# app.config['JSON_AS_ASCII'] = False  # แก้ปัญหา json encode ภาษาไทย
CORS(app)

# === REGISTER BLUEPRINTS ===
blueprints = [
    login_api, getopenid_bp, subject_bp, structure_bp, opensubject_bp, get_opensubject_bp,
    answer_bp, question_bp, dropOpen_bp, set_standard_bp, get_standard_bp,
    drop_standard_plan_bp, get_standard_lsit_bp, set_standard_list_bp, getstdPlan_bp,
    getStudentplan_list_bp, setstudentplan_list_bp, dropstudentplan_list_bp,
    updatestudent_plan_bp, updateStudentplan_list_bp, getTranferPlan_bp, setAdjustplan_list_bp,
    getAdjust_list_bp, getAdjust_plan_bp, updateadjust_plan_bp, pdf_api, syllabus_bp,
    pdf_tranfer, pdf_plan
]

for bp in blueprints:
    app.register_blueprint(bp, url_prefix='/api')

# === SERVE FRONTEND (Vue dist) ===
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_vue(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# === MAIN ===
if __name__ == '__main__':
    app.run(port=3000, debug=True)
