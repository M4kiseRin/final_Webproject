# final_Webproject
โปรเจกต์นี้ประกอบด้วย:
- Frontend: Vue.js (build แล้วในโฟลเดอร์ dist)
- Backend: Flask (Python API)
- ใช้ virtual environment (venv) สำหรับแยก dependencies
- ฐานข้อมูลที่ใช้ในการจำลองระบบโดยใช้ MongoDB เป็นโปรแกรมฐานข้อมูล (preject_db) 

ขั้นตอนการติดตั้งและใช้งาน 
1. ติดตั้ง Python (แนะนำเวอร์ชัน 3.12.0) ดาวน์โหลดจาก https://www.python.org/downloads/release/python-3120/
2. สร้าง virtual environment
- เปิด terminal ที่โฟลเดอร์โปรเจ็คนี้

  ![image3](https://github.com/user-attachments/assets/38971e20-02ed-4bcd-98a0-1e4d49ac2e69)
- ทำการสร้าง virtual environment โดยพิมพ์
  python -m venv venv
  
   ![image4](https://github.com/user-attachments/assets/70c08be9-193d-4e2b-88cd-eee7de025796)
- หลังจากทำการสร้าง environment แล้วให้ทำการเปิด virtual environment โดยพิมพ์
  venv\Scripts\activate
  แล้วที่หน้า terminal จะขึ้น (venv) D:\final_Webproject-main
  
  ![image5](https://github.com/user-attachments/assets/d8a0ed73-253c-4f07-baef-ad86cedbbc8c)
- หลังจากที่เราทำการเปิด venv เรียบร้อยแล้วให้ทำการติดตั้ง requirements.txt โดยพิมพ์
  pip install -r requirements.txt
  
  ![image6](https://github.com/user-attachments/assets/eee255e1-6d75-4dcc-a275-7b93f23115e3)
3. ทำการรัน project โดยให้พิมพ์ python app.py ถ้าหากรันเรียบร้อยแล้วจะขึ้นว่า Running on http://127.0.0.1:3000/ (Press CTRL+C to quit)
    หลังจากนั้นก็ให้เปิดเว็บที่  http://127.0.0.1:3000/
  
    ![image9](https://github.com/user-attachments/assets/f5f96be7-a12f-43db-bbc0-cec285a30dc2)
