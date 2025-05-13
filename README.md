# final_Webproject
โปรเจกต์นี้ประกอบด้วย:
- Frontend: Vue.js (build แล้วในโฟลเดอร์ dist)
- Backend: Flask (Python API)
- ใช้ virtual environment (venv) สำหรับแยก dependencies

ขั้นตอนการติดตั้งและใช้งาน 
1. ติดตั้ง Python (แนะนำเวอร์ชัน 3.12.0) ดาวน์โหลดจาก https://www.python.org/downloads/release/python-3120/
2. ติดตั้ง virtual environment (venv) หากไม่มี
- ทำเปิด terminal ที่โฟลเดอร์โปรเจ็คนี้
- ทำการสร้าง venv โดยพิมพ์
  python -m venv venv
- หลังจากทำการติดตั้งแล้วให้ทำการเปิด venv โดยพิมพ์
  venv\Scripts\activate
  แล้วที่หน้า terminal จะขึ้น (venv) D:\your_projec_folder
- หลังจากที่เราทำการเปิด venv เรียบร้อยแล้วให้ทำการติดตั้ง requirements.txt โดยพิมพ์
  pip install -r requirements.txt
3. ทำการรัน project โดยให้พิมพ์ python app.py ถ้าหากรันเรียบร้อยแล้วจะขึ้นว่า Running on http://127.0.0.1:3000/ (Press CTRL+C to quit)
    หลังจากนั้นก็ให้เปิดเว็บที่  http://127.0.0.1:3000/ 
