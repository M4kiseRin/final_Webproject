from api.config import getDatabase
from flask import Blueprint, jsonify, request
from pymongo import UpdateOne, InsertOne

updateStudentplan_list_bp = Blueprint("updateStudentplan_list", __name__)
db_config = getDatabase()

@updateStudentplan_list_bp.route('/updateStudentplan_list', methods=['POST'])
def updateStudentplan_list():
    try:
        # รับข้อมูลจาก Request
        data = request.get_json()
        std_id = data.get('std_id')
        plans = data.get('plans')
        status = data.get('status')

        # ตรวจสอบค่าที่จำเป็นต้องมี
        if not std_id or not isinstance(plans, list) or not plans:
            return jsonify({"message": "Invalid request data", "result": "0"}), 400

        # เข้าถึง Collection
        collection = db_config.get_collection('studentPlanList')
        studentplan = db_config.get_collection('studentPlans')

        if collection is None:
            return jsonify({"message": "Collection not found", "result": "0"}), 505

        # ดึงข้อมูลเดิมของ std_id
        existing_plans = list(collection.find(
            {"std_id": std_id},
            {"_id": 0, "year": 1, "term": 1, "subject_id": 1, "group_id": 1}
        ))
        
        existing_plans_set = set() # กำหนดค่าเริ่มต้นเป็นเซ็ตว่างของข้อมูลเดิม
        if existing_plans:
            existing_plans_set = {(p['year'], p['term'], p['subject_id']) for p in existing_plans}
        
        new_plans_set = {(p['year'], p['term'], p['subject_id']) for p in plans}

        # หาข้อมูลที่ต้องลบ
        plans_to_delete = existing_plans_set - new_plans_set
        if plans_to_delete:
            for plan in plans_to_delete:
                collection.delete_one({
                    "std_id": std_id,
                    "subject_id": plan[2],
                })

        bulk_operations = []  # ใช้เก็บคำสั่ง bulk insert/update

        for plan in plans:
            filter_query = {
                "std_id": std_id,
                "subject_id": plan['subject_id']
            }
            update_data = {
                "$set": {
                    "year": plan['year'],
                    "term": plan['term'],
                    "group_id": plan['group_id']
                }
            }

            existing_data = collection.find_one(filter_query)
            
            if existing_data:
                bulk_operations.append(UpdateOne(filter_query, update_data))
            else:
                bulk_operations.append(InsertOne({
                    "std_id": std_id,
                    "year": plan['year'],
                    "term": plan['term'],
                    "subject_id": plan['subject_id'],
                    "group_id": plan['group_id']
                }))

        inserted_count = 0
        updated_count = 0

        if bulk_operations:
            result = collection.bulk_write(bulk_operations)
            inserted_count = result.inserted_count
            updated_count = result.modified_count

        # อัปเดต `status` และลบ `reason` ใน studentplan
        studentplan.update_one(
            {"std_id": std_id},
            {"$set": {"status": status}, "$unset": {"reason": ""}}
        )

        return jsonify({
            "message": "Data processed successfully",
            "result": "1",
            "inserted_count": inserted_count,
            "updated_count": updated_count
        }), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"message": f"Error occurred: {str(e)}", "result": "0"}), 500
