from flask import Blueprint, jsonify, request
from api.config import getDatabase

login_api = Blueprint('login_api', __name__)

# สร้าง instance ของ MongoDBConfig
db_config = getDatabase()

@login_api.route('/getlogin', methods=['POST'])
def get_login():
    try:
        # รับข้อมูลจาก request
        data = request.json
        username = data.get('username')
        password = data.get('password')

        # เลือก Collection
        collection = db_config.get_collection('users')
        if collection is not None:  # ตรวจสอบว่ามี Collection
            # ค้นหา user
            user = collection.find_one({'user_email': username, 'password': password}, {'_id': 0})  # ลบ _id ออกจากผลลัพธ์
            if user:
                message = "Login successful!"
                result = "1"
                return jsonify({
                    "message": message,
                    "result":result,
                    "datalist": user,  # ส่งข้อมูล user ที่ค้นพบกลับ
                }), 200
            elif user is None:
                collection = db_config.get_collection('students')
                user = collection.find_one({'std_id': username, 'password': password}, {'_id':0})
                if user:
                    message = "Login successful!"
                    result = "1"
                    user.update({"user_status": "3"})
                    return jsonify({
                        "message": message,
                        "result":result,
                        "datalist": user,  # ส่งข้อมูล user ที่ค้นพบกลับ
                    }), 200
                else:
                    message = "Invalid username or password."
                    result = "2"
                    return jsonify({
                        "message": message,
                        "result": result
                    }), 401
            else:
                message = "Invalid username or password."
                result = "2"
                return jsonify({
                    "message": message,
                    "result": result
                }), 401
        else:
            message = "Collection not found."
            result = "0"
            return jsonify({
                "message": message,
                "result": result
            }), 500
    except Exception as e:
        return jsonify({
            "message": f"Error occurred: {e}"
        }), 500