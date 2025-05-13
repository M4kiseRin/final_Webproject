from api.config import getDatabase
from flask import Blueprint, jsonify, request

getAdjust_list_bp = Blueprint("getAdjust_list", __name__)  # สร้าง Blueprint

# สร้าง instance ของ MongoDBConfig
db_config = getDatabase()

@getAdjust_list_bp.route('/getAdjust_list', methods=['GET', 'POST'])
def getAdjust_list():
     try:
          collection = db_config.get_collection('adjustPlans')
          students = db_config.get_collection('students')
          syllabus = db_config.get_collection('syllabus')

          if collection is not None:
               if request.method == 'GET':
                    # ดึงข้อมูลทั้งหมดจาก Collection
                    datalist = list(collection.find())  # แปลง Cursor เป็น List
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
                              "syll_name": student_info.get('syll_name') if student_info else None,
                              "batch_year": student_info.get('batch_year') if student_info else None,
                              }
                              enriched_datalist.append(enriched_data)

                         return jsonify({
                              "message": "get data successfully",
                              "result": "1",
                              "datalist": enriched_datalist,  # ส่งข้อมูลที่ค้นพบ
                         }), 200
                    else:
                         return jsonify({
                              "message": "can't get data",
                              "result": "0"
                         }), 200
               else:
                    data = request.get_json()
                    std_id = data.get('std_id')
                    query = {
                         "std_id": std_id,
                    }
                    datalist = list(collection.find(query))
                    if datalist:
                         enriched_datalist = []
                         for item in datalist:
                              item['_id'] = str(item['_id'])
                              student_id = item.get('std_id')
                              student_info = students.find_one({"std_id":
                              student_id}) if student_id else None
                              syllabus_info = None
                              if student_info:
                                   syllabus_id = student_info.get('syllabus_id')
                              if syllabus_id:
                                   syllabus_data = syllabus.find_one({"_id":
                                   syllabus_id})
                              enriched_data = {
                                   **item,
                                   "std_name": student_info.get('std_name') if student_info else None,
                                   "std_last": student_info.get('std_last') if student_info else None,
                                   "year": student_info.get('year') if student_info else None,
                                   "syll_name": student_info.get('syll_name') if student_info else None,
                                   "batch_year": student_info.get('batch_year') if student_info else None,
                              }
                              enriched_datalist.append(enriched_data)
                         return jsonify({
                              "message": "get data successfully",
                              "result": "1",
                              "datalist": enriched_datalist,
                         }), 200
          else:
               return jsonify({
                    "message": "Collection not found.",
                    "result": "0"
               }), 500

     except Exception as e:
          return jsonify({
               "message": f"Error occurred: {e}"
          }), 500