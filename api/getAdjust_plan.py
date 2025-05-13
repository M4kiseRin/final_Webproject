from api.config import getDatabase
from flask import Blueprint, jsonify, request

getAdjust_plan_bp = Blueprint("getAdjust_plan", __name__)  # สร้าง Blueprint

# สร้าง instance ของ MongoDBConfig
db_config = getDatabase()

@getAdjust_plan_bp.route('/getAdjust_plan', methods=['POST'])
def getAdjust_plan():
     try:
          data = request.get_json()
          adjust_id = data.get('adjust_id')
          
          collection = db_config.get_collection('adjustPlansList')
          subjects = db_config.get_collection('subject')
          data_list = []


          if collection is not None:
            # ดึงข้อมูลทั้งหมดจาก Collection
            datalist = list(collection.find({"adjust_id": adjust_id}).sort("date_add", -1))  # แปลง Cursor เป็น List
            if datalist:
                # แปลงข้อมูลจาก MongoDB ObjectId เป็น String
                for item in datalist:
                    item['_id'] = str(item['_id'])
                    subject_id = item.get('subject_id')
                    
                    # ดึงข้อมูลจาก subject collection ที่เกี่ยวข้อง
                    subject_data = subjects.find_one({"subject_id": subject_id}) if subject_id else None

                    # ตรวจสอบว่า group_id มีอยู่หรือไม่
                    if 'group_id' not in item:
                        combined_data = {
                            **item,  
                            "subject_name": subject_data.get('subject_nameTh') if subject_data else None,
                            "theory_credits": subject_data.get('theory_credits') if subject_data else None,
                            "practical_credits": subject_data.get('practical_credits') if subject_data else None,
                            "group_id": subject_data.get('group_id') if subject_data else None,
                        }
                    else:
                        combined_data = {
                            **item,  
                            "subject_name": subject_data.get('subject_nameTh') if subject_data else None,
                            "theory_credits": subject_data.get('theory_credits') if subject_data else None,
                            "practical_credits": subject_data.get('practical_credits') if subject_data else None,
                        }
                    data_list.append(combined_data)
            
                return jsonify({
                    "message": "get data successfully",
                    "result": "1",
                    "datalist": data_list,  # ส่งข้อมูลที่ค้นพบ
                }), 200
            else:
                return jsonify({
                    "message": "can't get data",
                    "result": "0"
                }), 200
          else:
               return jsonify({
                    "message": "Collection not found.",
                    "result": "0"
               }), 500

     except Exception as e:
          return jsonify({
               "message": f"Error occurred: {e}"
          }), 500