from api.config import getDatabase
from flask import Blueprint, jsonify, request

question_bp = Blueprint("querstion", __name__)
# สร้าง instance ของ MongoDBConfig
db_config = getDatabase()

@question_bp.route('/setQuestion', methods=['POST'])
def setQuestion():
    try:
        # รับข้อมูลจากคำร้อง POST
        data = request.get_json()
        question = data.get('question')

        # เข้าถึง Collection
        collection = db_config.get_collection('question')

        if collection is not None:
            # เพิ่มข้อมูลใหม่ใน Collection

            query = {"question" : question}

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
                    "message": "Failed to insert data",
                    "result": "0"
                }), 500
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