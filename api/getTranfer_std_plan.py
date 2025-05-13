from api.config import getDatabase
from flask import Blueprint, jsonify, request

getTranferPlan_bp = Blueprint("getTranfer_plan", __name__)

# สร้าง instance ของ MongoDBConfig
db_config = getDatabase()

@getTranferPlan_bp.route('/getTranfer_plan', methods=['POST'])
def getTranfer_plan():
     try:
          # รับข้อมูลจาก Request
          data = request.get_json()
          std_id = data.get('std_id')
          
          # เข้าถึง Collection
          collection = db_config.get_collection('transfer')
          subjects = db_config.get_collection('subject')
          data_list = []
          # ตรวจสอบ Collection ว่ามีหรือไม่
          if collection is not None:
               # ดึงข้อมูลทั้งหมดจาก Collection
               datalist = list(collection.find({"std_id": std_id}))  # แปลง Cursor เป็น List
               if datalist:
                    # แปลงข้อมูลจาก MongoDB ObjectId เป็น String
                    for item in datalist:
                         item['_id'] = str(item['_id'])
                         subject_id = item.get('subject_id')
                         
                         # ดึงข้อมูลจาก subject collection ที่เกี่ยวข้อง
                         subject_data = subjects.find_one({"subject_id": subject_id}) if subject_id else None

                         # ตรวจสอบว่า subject_data ไม่ใช่ None
                         combined_data = {
                         **item,  # ข้อมูลจาก open_detail
                         "subject_name": subject_data.get('subject_nameTh') if subject_data else None,
                         "theory_credits": subject_data.get('theory_credits') if subject_data else None,
                         "practical_credits": subject_data.get('practical_credits') if subject_data else None,
                         "group_id": subject_data.get('group_id') if subject_data else None,
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
            "message": f"Error occurred: {str(e)}"
        }), 500