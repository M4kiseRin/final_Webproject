from api.config import getDatabase
from flask import Blueprint, jsonify, request

opensubject_bp = Blueprint("opensubject", __name__)
# สร้าง instance ของ MongoDBConfig
db_config = getDatabase()

@opensubject_bp.route('/setOpensubject', methods=['POST'])
def setOpensubject():
    try:
        # รับข้อมูลจากคำร้อง POST
        data = request.get_json()

        # ตรวจสอบว่ามีข้อมูลสำคัญครบถ้วน
        term = data.get('term')
        subject_id = data.get('subject_id')
        group_id = data.get('group_id')

        # เข้าถึง Collection
        collection = db_config.get_collection('open_detail')

        if collection is not None:
            # เพิ่มข้อมูลใหม่ใน Collection
            new_subject = {
                "term": term,
                "subject_id": subject_id,
                "group_id": group_id
            }
            query = {
                "term" : term,
                "subject_id": subject_id,
            }
            find_data = collection.find_one(new_subject)
            if find_data is None:
                insert_result = collection.insert_one(new_subject)
                # ตรวจสอบว่าเพิ่มสำเร็จหรือไม่
                if insert_result.inserted_id:
                    # ดึงข้อมูลทั้งหมดใน Collection
                    datalist = list(collection.find(query))
                    
                    # แปลง `_id` และข้อมูลเครดิตให้เป็น String
                    for item in datalist:
                        item['_id'] = str(item['_id'])
                        item['term'] = str(item['term'])

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
                        "message": "already has this data",
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