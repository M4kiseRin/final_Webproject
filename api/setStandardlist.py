from api.config import getDatabase
from flask import Blueprint, jsonify, request
from pymongo import UpdateOne, InsertOne

set_standard_list_bp = Blueprint("setStandard_list", __name__)
# สร้าง instance ของ MongoDBConfig
db_config = getDatabase()

@set_standard_list_bp.route('/setStandard_list', methods=['POST'])
def setStandard_list():
    try:
        # รับข้อมูลจากคำร้อง POST
        data = request.get_json()

        plan_id = data.get('plan_id')
        plans = data.get('plans')
        
        # เข้าถึง Collection
        collection = db_config.get_collection('standardPlansList')
        
        if collection is None:
            return jsonify({"message": "Collection not found", "result": "0"}), 505
        
        # ดึงข้อมูลเดิมของ std_id
        existing_plans = list(collection.find(
            {"plan_id": plan_id},
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
                    "plan_id": plan_id,
                    "subject_id": plan[2],
                })

        bulk_operations = []  # ใช้เก็บคำสั่ง bulk insert/update

        for plan in plans:
            filter_query = {
                "plan_id": plan_id,
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
                    "plan_id": plan_id,
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

        return jsonify({
            "message": "Data processed successfully",
            "result": "1",
            "inserted_count": inserted_count,
            "updated_count": updated_count
        }), 200
       

    except Exception as e:
        return jsonify({
            "message": f"Error occurred: {str(e)}",
            "result": "0"
        }), 500