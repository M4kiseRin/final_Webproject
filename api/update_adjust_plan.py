from api.config import getDatabase
from flask import Blueprint, jsonify, request
from datetime import datetime


updateadjust_plan_bp = Blueprint("updateAdjust_plan", __name__)
# สร้าง instance ของ MongoDBConfig
db_config = getDatabase()

@updateadjust_plan_bp.route('/updateAdjust_plan', methods=['POST'])
def updateAdjust_plan():
     try:
          # รับข้อมูลจากคำร้อง POST
          data = request.get_json()

          std_id = data.get('std_id')
          adjust_id = data.get('adjust_id')
          plans = data.get('plans')
          status = data.get('status')
          user = data.get('user')
          reason = data.get('reason') if data.get('reason') else None

          # เข้าถึง Collection
          collection = db_config.get_collection('studentPlanList')
          adjust_plan = db_config.get_collection('adjustPlans')
          adjust_list = db_config.get_collection('adjustPlansList')
          
          if collection is None or adjust_plan is None:
               return jsonify({"message": "Collection not found", "result": "0"}), 505
          
                  # **สร้างวันที่ปัจจุบันในรูปแบบ "DD-MM-YYYY (พ.ศ.)"**
          current_date = datetime.now()
          thai_year = current_date.year + 543  # แปลง ค.ศ. -> พ.ศ.
          formatted_date = current_date.strftime(f"%d-%m-{thai_year}")
          
          if int(status) == 1:
               if collection is not None and adjust_plan is not None:
                    for plan in plans:
                         # เงื่อนไขในการค้นหา
                         filter_query = {
                              "std_id": std_id,
                              "subject_id": plan['subject_id']
                         }
                         update_data = {
                              "$set": {  # Corrected the syntax here
                                   "year": plan['year'],
                                   "term": plan['term'],
                              }
                         }
                         collection.update_one(filter_query, update_data)
                                                  
                    adjust_plan.update_one(
                         {"adjust_id": adjust_id},
                         {"$set": {"status": status, "date_updated": formatted_date, "user_ap": user}}
                    )
                    adjust_list.delete_many(
                         {"adjust_id": adjust_id}
                    )
          else:
               if collection is not None and adjust_plan is not None:
                    adjust_plan.update_one(
                         {"adjust_id": adjust_id},
                         {"$set": {"status": status, "reason": reason, "date_updated": formatted_date , "user_ap": user}}
                    )
                    adjust_list.delete_many(
                         {"adjust_id": adjust_id}
                    )
          
          return jsonify({"message": "Adjust plan updated successfully", "result": "1"}), 200
     
     except Exception as e:
          return jsonify({
               "message": f"Error occurred: {str(e)}",
               "result": "0"
          }), 500
