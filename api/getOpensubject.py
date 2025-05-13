from api.config import getDatabase
from flask import Blueprint, jsonify, request

get_opensubject_bp = Blueprint("gopensubject", __name__)  # สร้าง Blueprint

# สร้าง instance ของ MongoDBConfig
db_config = getDatabase()

@get_opensubject_bp.route('/getopensubject', methods=['POST'])
def getOpensubject():
    try:
        # เข้าถึง Collections
        collection = db_config.get_collection('open_detail')
        subject_collection = db_config.get_collection('subject')
        data_list = []
        data = request.get_json()
        term = data.get('term')
        
         # ตรวจสอบ Method ของคำร้อง
        if term != None:
            if collection is not None:
            # ค้นหาเอกสารจาก open_detail
                query = {"term": term}
                datalist = list(collection.find(query))

                if datalist:
                    # ดึงข้อมูล subject_name จาก Collection subject
                    for item in datalist:
                        item['_id'] = str(item['_id'])  # แปลง ObjectId เป็น String
                        subject_id = item.get('subject_id')  # ดึง subject_id

                        # ดึงข้อมูลจาก subject collection ที่เกี่ยวข้อง
                        subject_data = subject_collection.find_one({"subject_id": subject_id}) if subject_id else None

                        # รวมข้อมูลจากทั้งสองคอลเล็กชันในรายการเดียว
                        combined_data = {
                            **item,  # ข้อมูลจาก open_detail
                            "subject_name": subject_data.get('subject_nameTh'),
                            "theory_credits": subject_data.get('theory_credits'),
                            "practical_credits": subject_data.get('practical_credits'),
                            "group_id": subject_data.get('group_id'),
                        }
                        data_list.append(combined_data)

                    return jsonify({
                        "message": "get data successfully",
                        "result": "1",
                        "datalist": data_list,  # ส่งข้อมูลที่ค้นพบพร้อม subject_name
                    }), 200
                else:
                    return jsonify({
                        "message": "can't get data",
                        "result": "2"
                    }), 200
            else:
                return jsonify({
                    "message": "Collection not found.",
                    "result": "0"
                }), 500  
                
        elif term == None:
            if collection is not None:
                
                datalist = list(collection.find())

                if datalist:
                    # ดึงข้อมูล subject_name จาก Collection subject
                    for item in datalist:
                        item['_id'] = str(item['_id'])  # แปลง ObjectId เป็น String
                        subject_id = item.get('subject_id')  # ดึง subject_id

                        # ดึงข้อมูลจาก subject collection ที่เกี่ยวข้อง
                        subject_data = subject_collection.find_one({"subject_id": subject_id}) if subject_id else None

                        # รวมข้อมูลจากทั้งสองคอลเล็กชันในรายการเดียว
                        combined_data = {
                            **item,  # ข้อมูลจาก open_detail
                            "subject_name": subject_data.get('subject_nameTh') if subject_data else None,
                            "theory_credits": subject_data.get('theory_credits') if subject_data else None,
                            "practical_credits": subject_data.get('practical_credits') if subject_data else None,
                            "group_id": subject_data.get('group_id') if subject_data else None,
                        }
                        data_list.append(combined_data)

                    return jsonify({
                        "message": "get data successfully",
                        "result": "1",
                        "datalist": data_list,
                    }), 200
                else:
                    return jsonify({
                        "message": "can't get data",
                        "result": "2"
                    }), 200
            else:
                return jsonify({
                    "message": "Collection not found.",
                    "result": "0"
                }), 500
        # **เพิ่ม return ในกรณีที่ทั้ง term และ group_id เป็น None**
        return jsonify({
            "message": "Invalid request, missing term or group_id",
            "result": "0"
        }), 400  # HTTP 400: Bad Request

    except Exception as e:
        return jsonify({
            "message": f"Error occurred: {e}"
        }), 500
