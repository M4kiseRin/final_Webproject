from api.config import getDatabase
from flask import Blueprint, jsonify, request

set_standard_bp = Blueprint("setStandardplan", __name__)
# สร้าง instance ของ MongoDBConfig
db_config = getDatabase()

@set_standard_bp.route('/setStandard_plan', methods=['POST'])
def setStandard_plan():
     try:
          # รับข้อมูลจากคำร้อง POST
          data = request.get_json()
          
          plan_id = data.get('plan_id')
          batch_year = data.get('batch_year')

          if plan_id is None or batch_year is None:
               return jsonify({
                    "message": "Invalid request data",
                    "result": "0"
               }), 400

          # เข้าถึง Collection
          collection = db_config.get_collection('standardPlans')

          if collection is not None:
            # เพิ่มข้อมูลใหม่ใน Collection
               query = {
                    "plan_id": plan_id,
                    "batch_year": batch_year, 
                    }
               find_result = collection.find_one(query)
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