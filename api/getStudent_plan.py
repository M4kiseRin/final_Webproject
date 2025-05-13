from api.config import getDatabase
from flask import Blueprint, jsonify, request


getstdPlan_bp = Blueprint("getStudent_plan", __name__)

# สร้าง instance ของ MongoDBConfig
db_config = getDatabase()

@getstdPlan_bp.route('/getStudent_plan', methods=['GET'])
def getStudent_plan():
    try:
        collection = db_config.get_collection('studentPlans')
        students = db_config.get_collection('students')
        syllabus = db_config.get_collection('syllabus')

        if collection is not None:
            datalist = list(collection.find())  # ดึงข้อมูลทั้งหมดจาก studentPlans

            if datalist:
                enriched_datalist = []
                for item in datalist:
                    item['_id'] = str(item['_id'])  # แปลง ObjectId เป็น string

                    student_id = item.get('std_id')  # ดึง student_id
                    student_info = students.find_one({"std_id": student_id}) if student_id else None

                    syllabus_info = None
                    if student_info:
                        syllabus_id = student_info.get('syllabus_id')  # syllabus_id ที่อยู่ใน students
                        if syllabus_id:
                              syllabus_data = syllabus.find_one({"_id": syllabus_id})

                    # สร้าง enriched_data
                    enriched_data = {
                        **item,
                        "std_name": student_info.get('std_name') if student_info else None,
                        "std_last": student_info.get('std_last') if student_info else None,
                        "year": student_info.get('year') if student_info else None,
                        "syll_name": student_info.get('syll_name'),
                        "batch_year": student_info.get('batch_year') if student_info else None,
                    }
                    enriched_datalist.append(enriched_data)

                return jsonify({
                    "message": "get data successfully",
                    "result": "1",
                    "datalist": enriched_datalist,  # ส่ง enriched_datalist กลับ
                }), 200
            else:
                return jsonify({
                    "message": "No data found for the given query",
                    "result": "0"
                }), 404
        else:
            return jsonify({
                "message": "Collection not found",
                "result": "0"
            }), 505

    except Exception as e:
        return jsonify({
            "message": f"Error occurred: {str(e)}"
        }), 500