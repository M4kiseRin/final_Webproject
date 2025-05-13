from flask import Blueprint, request, send_file, Response
from api.config import getDatabase
import weasyprint
import io
import json
from urllib.parse import quote
from datetime import datetime

pdf_tranfer = Blueprint("pdf_summery_tranfer", __name__)

# สร้าง instance ของ MongoDBConfig
db_config = getDatabase()

def thai_date():
     th_month = ["มกราคม","กุมภาพันธ์","มีนาคม","เมษายน","พฤษภาคม","มิถุนายน",
                 "กรกฎาคม","สิงหาคม","กันยายน","ตุลาคม","พฤศจิกายน","ธันวาคม"]
     today = datetime.now()
     return f"{today.day} {th_month[today.month-1]} {today.year+543}"

@pdf_tranfer.route("/pdf_summery_tranfer", methods=["GET"])
def create_pdf():
     pass
     title = request.args.get("title", "ไม่มีข้อมูล")
     year = request.args.get("year", "ไม่มีข้อมูล")
     content = request.args.get("content", "ไม่มีข้อมูล")
     content = json.loads(content)
     
     collection = db_config.get_collection('syllabus')
     course_list = list(collection.find())
     course_year = 0
     for item in sorted(course_list, key=lambda x: x["year"], reverse=True):
          if year >= item["year"]:
               course_year = item["year"]
               break

     html_content = f"""
     <html>
          <head>
          <title>{title}</title>
               <meta charset="utf-8">
               <style>
               @page {{
               size: A4;
               margin: 20mm;
               @top-right {{
                    content: "หน้า " counter(page);
                    font-size: 12px;
                    font-family: "TH Sarabun New", sans-serif;
               }}
                    }}
               body {{
                    font-family: 'TH Sarabun New', Arial, sans-serif;
                    text-align: center;
                    margin: 0;
               }}
               h1 {{
                    color: darkblue;
                    margin-bottom: 10px;
                    font-size: 18px; 
               }}
               table {{
                    width: 100%;
                    border-collapse: collapse;
                    page-break-inside: auto;
                    margin-top: 20px;
                    margin-bottom: 20px;
               }}
               th, td {{
                    border: 1px solid black;
                    padding: 5px 10px;  
                    text-align: center;
                    font-size: 10px;  
               }}
               th {{
                    background-color: #f2f2f2;
               }}
               tr{{
                    page-break-inside: avoid;
                    
               }}
               p{{
                    font-size: 14px;
                    margin-bottom: 15px;    
               }}
               .page-break {{
                    page-break-before: always;
               }}
               .term-header {{
                    font-weight: bold;
                    font-size: 14px;
                    margin-top: 10px;
               }}
               </style>
          </head>
     <body>
          <h1>สรุปผลการเทียบโอนรายวิชารายบุคคล (แบบสรุป)</h1>
          <p style="color: darkblue;">หลักสูตรบริหารธุรกิจบัณฑิต</p>
          <p style="color: darkblue;">สาขาวิชาเทคโนโลยีธุรกิจดิจิทัล (หลักสูตร พ.ศ.{course_year})</p>
          <p style="color: darkblue;">คณะบริหารธุรกิจและเทคโนโลยีสารสนเทศ</p>
          <p style="color: darkblue;">มหาวิทยาลัยเทคโนโลยีราชมงคลอีสาน วิทยาเขตขอนแก่น</p>
          <p style="color: darkblue;">รุ่นปีการเรียนศึกษา {year}</p>
          <p style="color: darkblue;">รายงาน ณ วันที่ {thai_date()}</p>
     """

     html_content += """
     <table>
     <tr>
          <th>รหัสนักศึกษา</th>
          <th>ชื่อ-นามสกุล</th>
          <th>หน่วยกิตบังคับ</th>
          <th>เทียบโอนได้</th>
          <th>เรียนเพิ่ม</th>
     </tr>
     """
     student = 0
     
     for students in content:
          std_id = students.get("std_id")
          std_name = students.get("std_name")
          std_last = students.get("std_last")
          total_Tcredits = students.get("total_Tcredits")
          total_Pcredits = students.get("total_Pcredits")
          html_content += f"""
          <tr>
               <td>{ std_id }</td>
               <td style="text-align: left;">{ std_name } { std_last }</td>
               <td>125</td>
               <td>{ total_Tcredits }</td>
               <td>{ total_Pcredits }</td>
          </tr>
          
          """
          student += 1
     html_content += "</table>"
     html_content += f"""
          <pstyle="font-size: 16px; margin-top: 10px; font-weight: bold;>
               รวมจำนวนนักศึกษาที่ขอเทียบโอนทั้งสิ้น {student} คน
          </p>
          """

     html_content += "</body></html>"
     pdf = weasyprint.HTML(string=html_content).write_pdf()
     pdf_io = io.BytesIO(pdf)

     # กำหนดให้เปิดในแท็บใหม่ และให้ชื่อไฟล์เป็น "student_plan.pdf"
     response = Response(pdf_io.getvalue(), mimetype="application/pdf")
     response.headers["Content-Disposition"] = f'inline; filename="{quote(title)}.pdf"'
     response.headers["Content-Type"] = "application/pdf"

     return response