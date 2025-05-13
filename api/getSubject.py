from api.config import getDatabase
from flask import Blueprint, jsonify, request

subject_bp = Blueprint("subject", __name__)

# สร้าง instance ของ MongoDBConfig
db_config = getDatabase()

@subject_bp.route('/getSubject', methods=['POST'])
def getSubjects():
    try:
        # รับข้อมูลจากคำร้อง
        data = request.get_json()  # ใช้ .get_json() แทน .json

        # ตรวจสอบว่าได้รับ group_id
        group_id = data.get('group_id')  # รับ group_id
        
        # เชื่อมต่อกับ MongoDB และดึงข้อมูลจาก Collection 'subject'
        collection = db_config.get_collection('subject')
        
        if group_id is  not None:
            if collection is not None:

                # ดึงข้อมูลด้วย find() และแปลง Cursor เป็น List
                datalist = list(collection.find({"group_id": group_id})) #{"group_id": group_id}

                if datalist:
                    # แปลง _id ให้เป็น String
                    for item in datalist:
                        item['_id'] = str(item['_id'])
                        item['theory_credits'] = str(item['theory_credits'])
                        item['total_credits'] = str(item['total_credits'])

                    return jsonify({
                        "message": "get data successfully",
                        "result": "1",
                        "datalist": datalist,  # ส่งข้อมูลรายการทั้งหมดกลับ
                    }), 200
                else:
                    return jsonify({
                        "message": "No data found for the given query",
                        "result": "0"
                    }), 200
            else:
                return jsonify({
                    "message": "Collection not found",
                    "result": "0"
                }), 505
        # else:
        #     if collection is not None:
        #         # ดึงข้อมูลด้วย find() และแปลง Cursor เป็น List
        #         datalist = list(collection.find())
        #         if datalist:
        #             # แปลง _id ให้เป็น String
        #             for item in datalist:
        #                 item['_id'] = str(item['_id'])
        #                 item['theory_credits'] = str(item['theory_credits'])
        #                 item['total_credits'] = str(item['total_credits'])

        #             return jsonify({
        #                 "message": "get data successfully",
        #                 "result": "1",
        #                 "datalist": datalist,  # ส่งข้อมูลรายการทั้งหมดกลับ
        #             }), 200
        #     else:
        #         return jsonify({
        #             "message": "Collection not found",
        #             "result": "0"
        #         }), 505

    except Exception as e:
        return jsonify({
            "message": f"Error occurred: {str(e)}"
        }), 500
