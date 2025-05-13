from api.config import getDatabase
from flask import Blueprint, jsonify, request

setstudentplan_list_bp = Blueprint("setStudentplan_list", __name__)
# สร้าง instance ของ MongoDBConfig
db_config = getDatabase()

@setstudentplan_list_bp.route('/setStudentplan_list', methods=['POST'])
def setStudentplan_list():
     try:
          # รับข้อมูลจากคำร้อง POST
          data = request.get_json()
          
          std_id = data.get('std_id')
          year = data.get('year')
          term = data.get('term')
          subject_id = data.get('subject_id')
          stdplan_id = data.get('stdplan_id')
          group_id = data.get('group_id')

          # เข้าถึง Collection
          collection = db_config.get_collection('studentPlanList')

          if collection is not None:
            # เพิ่มข้อมูลใหม่ใน Collection
               query = {
                    "std_id": std_id,
                    "year": year,
                    "term":term,
                    "subject_id":subject_id,
                    "stdplan_id":stdplan_id,
                    "group_id":group_id
                    }
               find_result = collection.find_one({"subject_id":subject_id,"std_id": std_id,})
               if find_result is None:
                    insert_result = collection.insert_one(query)

                    # ตรวจสอบว่าเพิ่มสำเร็จหรือไม่
                    if insert_result.inserted_id:
                         return jsonify({
                         "message": "Data inserted successfully",
                         "result": "1",
                         "inserted_id": str(insert_result.inserted_id),
                         }), 201
               else:
                    return jsonify({
                    "message": "already have this data",
                    "result": "2"
                    }), 200
          else:
               return jsonify({
                    "message": "Collection not found",
                    "result": "0"
               }), 505
     except Exception as e:
          return jsonify({
               "message": f"Error occurred: {str(e)}",
               "result": "0"
          }), 500