from .config import getDatabase

def test_database_connection():
    try:
        # ดึงฐานข้อมูล
        db = getDatabase()

        # ระบุชื่อคอลเลกชัน (สมมติว่ามีชื่อ 'users')
        users_collection = db["User"]

        # ดึงข้อมูลทั้งหมดจากคอลเลกชัน
        users = list(users_collection.find())

        # แสดงผลข้อมูล
        if users:
            status = "เชื่อมต่อฐานข้อมูลสำเร็จ!"
            massage =  "ข้อมูลที่ได้:"
            datalist = []
            for user in users:
                datalist.append = user
            print(status + massage + datalist)
        else:
            print ("เชื่อมต่อฐานข้อมูลสำเร็จ แต่ยังไม่มีข้อมูลในคอลเลกชัน")

    except Exception as e:
        print ("เกิดข้อผิดพลาด:", e)

# เรียกฟังก์ชันทดสอบ
if __name__ == "__main__":
    test_database_connection()
