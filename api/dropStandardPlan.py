from api.config import getDatabase
from flask import Blueprint, jsonify,request

drop_standard_plan_bp = Blueprint("drop_standard", __name__)  # สร้าง Blueprint

# สร้าง instance ของ MongoDBConfig
db_config = getDatabase()

@drop_standard_plan_bp.route('/dropStandard_plan', methods=['POST'])
def dropStandard_plan():
     try:
          data = request.get_json()
          plan_id = data.get('plan_id')
          batch_year = data.get('batch_year')
          # เข้าถึง Collection
          collection = db_config.get_collection('standardPlans')
          col_standard_plan = db_config.get_collection('standardPlansList')
          
          if col_standard_plan is not None:
               query = {
                    "plan_id": plan_id,
               }
               delete  =col_standard_plan.delete_many(query)

               if collection is not None:
                    # ดึงข้อมูลทั้งหมดจาก Collection
                    query ={
                         "plan_id": plan_id,
                         "batch_year": batch_year,
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
          else:
                    return jsonify({
                         "message": "Collection not found.",
                         "result": "0"
                    }), 500
                    
     except Exception as e:
          return jsonify({
               "message": f"Error occurred: {e}"
          }), 500
