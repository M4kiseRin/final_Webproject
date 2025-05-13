from api.config import getDatabase
from flask import Blueprint, jsonify,request

dropstudentplan_list_bp = Blueprint("dropStudentplan_list", __name__)  # สร้าง Blueprint

# สร้าง instance ของ MongoDBConfig
db_config = getDatabase()

@dropstudentplan_list_bp.route('/dropStudentplan_list', methods=['POST'])
def dropStandard_plan():
     try:
          data = request.get_json()
          std_id = data.get('std_id')
          subject_id = data.get('subject_id')

          # เข้าถึง Collection
          collection = db_config.get_collection('studentPlanList')

          if collection is not None:
               # ดึงข้อมูลทั้งหมดจาก Collection
               query ={
                    "std_id": std_id,
                    "subject_id": subject_id,
               }
               
               delete = collection.delete_one(query)  # แปลง Cursor เป็น List
               
               if delete.deleted_count > 0:
                    return jsonify({
                         "message": "Data deleted successfully",
                         "result": "1",
                         "deleted_count": delete.deleted_count
                         }), 200
               else:
                    return jsonify({
                         "message": "No matching data found to delete",
                         "result": "2",
                         "deleted_count": 0
                    }), 404
          else:
               return jsonify({
                    "message": "Collection not found.",
                    "result": "0"
               }), 500
               
     except Exception as e:
          return jsonify({
               "message": f"Error occurred: {e}"
          }), 500
