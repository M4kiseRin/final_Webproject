from pymongo import MongoClient

class getDatabase:
    def __init__(self):
        try:
            # MongoDB URI
            self.client = MongoClient("mongodb://localhost:27017/")
            # ระบุชื่อ Database ที่จะใช้
            self.db = self.client['project_db']
            print("MongoDB connection established successfully.")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")

    def get_collection(self, collection_name):
        try:
            # คืนค่า collection ที่ต้องการ
            return self.db[collection_name]
        except Exception as e:
            print(f"Error getting collection '{collection_name}': {e}")
            return None
