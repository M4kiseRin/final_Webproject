from api.config import getDatabase
from flask import Blueprint, jsonify, request
from datetime import datetime

setAdjustplan_list_bp = Blueprint("setAdjustplan_list", __name__)
# สร้าง instance ของ MongoDBConfig
db_config = getDatabase()

@setAdjustplan_list_bp.route('/setAdjustplan_list', methods=['POST'])
def updateStudentplan_list():
    try:
        # รับข้อมูลจาก Request
        data = request.get_json()
        std_id = data.get('std_id')
        plans = data.get('plans')

        # เช็คว่า plans เป็น array และไม่ว่าง
        if not isinstance(plans, list) or len(plans) == 0:
            return jsonify({
                "message": "Invalid or empty plans array",
                "result": "0"
            }), 400

        # เข้าถึง Collection
        collection = db_config.get_collection('adjustPlansList')
        adjustPlan = db_config.get_collection('adjustPlans')


        if collection is None or adjustPlan is None:
            return jsonify({
                "message": "Collection not found",
                "result": "0"
            }), 505

        inserted_ids = []  # เก็บ id ที่ถูก insert
        # สร้าง key ใหม่
        primary_key_prefix = f"{std_id[:2]}{std_id[-4:]}"
        last_entry = adjustPlan.find_one(
            {"std_id": std_id},
            sort=[("adjust_id", -1)]
        )
        if last_entry and ("status" in last_entry) == 0:
            return jsonify({
            "message": "Data processed successfully",
            "result": "2"
            }), 200
        
        elif last_entry and "adjust_id" in last_entry:
            # ดึงเลข 6 ตัวท้ายจาก adjust_id แล้วเพิ่มค่าทีละ 1
            last_primary_key = int(last_entry["adjust_id"].split("-")[-1])
            new_primary_key = f"{primary_key_prefix}-{str(last_primary_key + 1).zfill(6)}"
        else:
            new_primary_key = f"{primary_key_prefix}-900001"

        # เพิ่ม key ลงใน query
        key = new_primary_key



        # เพิ่ม key ลงใน query
        key = new_primary_key

        # **สร้างวันที่ปัจจุบันในรูปแบบ "DD-MM-YYYY (พ.ศ.)"**
        current_date = datetime.now()
        thai_year = current_date.year + 543  # แปลง ค.ศ. -> พ.ศ.
        formatted_date = current_date.strftime(f"%d-%m-{thai_year}")
        
        for plan in plans:
            # ดึงข้อมูลจาก plans
            year = plan.get('year')
            term = plan.get('term')
            subject_id = plan.get('subject_id')
            group_id = plan.get('group_id')

            query = {
                "adjust_id": key,
                "std_id": std_id,
                "year": year,
                "term": term,
                "subject_id": subject_id,
                "group_id": group_id,
                "date": formatted_date  # **เพิ่มวันที่ลงไปใน Collection**
            }

            insert_result = collection.insert_one(query)
            if insert_result.inserted_id:
                inserted_ids.append(str(insert_result.inserted_id))
                        
        adjustPlan.insert_one(
            {   
                "adjust_id": key,
                "std_id": std_id,
                "status": 0,
                "date_add": formatted_date
            }
        )

        return jsonify({
            "message": "Data processed successfully",
            "result": "1",
            "inserted_ids": inserted_ids
        }), 200

    except Exception as e:
        return jsonify({
            "message": f"Error occurred: {str(e)}",
            "result": "0"
        }), 500