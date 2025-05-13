from api.config import getDatabase
from flask import Blueprint, jsonify, request

updatestudent_plan_bp = Blueprint("updateStudent_plan", __name__)
# สร้าง instance ของ MongoDBConfig
db_config = getDatabase()

@updatestudent_plan_bp.route('/updateStudent_plan', methods=['POST'])
def updateStudentplan_list():
    try:
        # รับข้อมูลจากคำร้อง POST
        data = request.get_json()

        std_id = data.get('std_id')
        stdplan_id = data.get('stdplan_id')
        status = data.get('status')
        reason = data.get('reason') if data.get('reason') else None

        # เข้าถึง Collection
        collection = db_config.get_collection('studentPlans')

        if collection is not None:
            # เงื่อนไขในการค้นหา
            query = {
                "std_id": std_id,
                "stdplan_id": stdplan_id,
        
            }

            # อัปเดตข้อมูลโดยใช้คำสั่ง update_one
            update_result = collection.update_one(
                query,  # เงื่อนไข
                {"$set": {"status": status, "reason":reason}}  # ฟิลด์ที่ต้องการเปลี่ยนแปลง
            )

            # ตรวจสอบผลลัพธ์
            if update_result.matched_count > 0:  # มีเอกสารตรงกับเงื่อนไข
                if update_result.modified_count > 0:  # มีการอัปเดตค่าใหม่
                    return jsonify({
                        "message": "Data updated successfully",
                        "result": "1",
                    }), 200
                else:  # ค่าเดิมเหมือนกับค่าที่อัปเดต (ไม่มีการเปลี่ยนแปลง)
                    return jsonify({
                        "message": "No changes made (data is already up to date)",
                        "result": "2",
                    }), 200
            else:  # ไม่มีเอกสารตรงกับเงื่อนไข
                return jsonify({
                    "message": "No matching document found",
                    "result": "0"
                }), 404
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