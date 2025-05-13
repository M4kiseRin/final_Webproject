from api.config import getDatabase
from flask import Blueprint, jsonify,request

get_standard_lsit_bp = Blueprint("getStandard_list", __name__)  # สร้าง Blueprint

# สร้าง instance ของ MongoDBConfig
db_config = getDatabase()

@get_standard_lsit_bp.route('/getStandard_list', methods=['POST'])
def getStandard_list():
     try:
          data = request.get_json()
          plan_id = data.get('plan_id')
          
          # เข้าถึง Collection
          collection = db_config.get_collection('standardPlansList')
          subject_collection = db_config.get_collection('subject')
          data_list = []

          if collection is not None:
               
               query = {
                    "plan_id": plan_id,
               }
               # ดึงข้อมูลทั้งหมดจาก Collection
               datalist = list(collection.find(query))
               if datalist:
                    # แปลงข้อมูลจาก MongoDB ObjectId เป็น String
                    for item in datalist:
                         item['_id'] = str(item['_id'])
                         subject_id = item.get('subject_id')  # ดึง subject_id
                         # ดึงข้อมูลจาก subject collection ที่เกี่ยวข้อง
                         subject_data = subject_collection.find_one({"subject_id": subject_id}) if subject_id else None

                         # รวมข้อมูลจากทั้งสองคอลเล็กชันในรายการเดียว
                         if item.get('group_id') is None:
                              combined_data = {
                                   **item,  # ข้อมูลจาก open_detail
                                   "subject_name": subject_data.get('subject_nameTh') if subject_data else None,
                                   "group_id": subject_data.get('group_id') if subject_data else None,
                                   "theory_credits": subject_data.get('theory_credits') if subject_data else None,
                                   "practical_credits": subject_data.get('practical_credits') if subject_data else None,
                              }
                         else:
                              combined_data = {
                                   **item,  # ข้อมูลจาก open_detail
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
                         "result": "2"
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
