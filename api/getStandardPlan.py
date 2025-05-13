from api.config import getDatabase
from flask import Blueprint, jsonify

get_standard_bp = Blueprint("getStandard_plan", __name__)  # สร้าง Blueprint

# สร้าง instance ของ MongoDBConfig
db_config = getDatabase()

@get_standard_bp.route('/getStandard_plan', methods=['GET'])
def getStandard_plan():
    try:
        # เข้าถึง Collection
        collection = db_config.get_collection('standardPlans')

        if collection is not None:
            # ดึงข้อมูลทั้งหมดจาก Collection
            datalist = list(collection.find().sort("batch_year", -1))  # แปลง Cursor เป็น List
            if datalist:
                # แปลงข้อมูลจาก MongoDB ObjectId เป็น String
                for item in datalist:
                    item['_id'] = str(item['_id'])

                return jsonify({
                    "message": "get data successfully",
                    "result": "1",
                    "datalist": datalist,  # ส่งข้อมูลที่ค้นพบ
                }), 200
            else:
                return jsonify({
                    "message": "can't get data",
                    "result": "0"
                }), 401
        else:
            return jsonify({
                "message": "Collection not found.",
                "result": "0"
            }), 500

    except Exception as e:
        return jsonify({
            "message": f"Error occurred: {e}"
        }), 500
