from flask import Blueprint, request, send_file, Response
from api.config import getDatabase
import weasyprint
import io
import json
from urllib.parse import quote
from datetime import datetime
from collections import defaultdict

pdf_plan = Blueprint("pdf_summery_plan", __name__)

# สร้าง instance ของ MongoDBConfig
db_config = getDatabase()

def thai_date():
     th_month = ["มกราคม","กุมภาพันธ์","มีนาคม","เมษายน","พฤษภาคม","มิถุนายน",
                 "กรกฎาคม","สิงหาคม","กันยายน","ตุลาคม","พฤศจิกายน","ธันวาคม"]
     today = datetime.now()
     return f"{today.day} {th_month[today.month-1]} {today.year+543}"

@pdf_plan.route("/pdf_summery_plan", methods=["GET"])
def create_pdf():
     pass
     title = request.args.get("title", "ไม่มีข้อมูล")
     year = request.args.get("year", "ไม่มีข้อมูล")
     students_plan = request.args.get("students_plan", "ไม่มีข้อมูล")
     students_plan = json.loads(students_plan)
     group = request.args.get("group", "ไม่มีข้อมูล")
     group = json.loads(group)
     
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
          <h1>สรุปผลแผนการเรียนรายวิชาประจำภาคเรียน (หลังการเทียบโอน)</h1>
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
               <th>รหัสวิชา</th>
               <th>ชื่อวิชา</th>
               <th>หน่วยกิต</th>
               <th>ปีการศึกษา</th>
               <th>เทอม</th>
               <th>จำนวนนักศึกษา</th>
          </tr>
     """
     subject_count = 0  # นับจำนวนวิชาที่แสดงในตาราง
     # วนลูปตาม group ก่อน (กลุ่มหมวดวิชา)
     for g in group:
          group_name = g.get("group_name")
          group_id = g.get("group_id")

          # ตรวจสอบว่ามีวิชาตรงกับ group_id หรือไม่
          has_subjects = any(subject.get("group_id") == group_id for subject in students_plan)
          if not has_subjects:
               continue  # ถ้าไม่มีวิชาในกลุ่มนี้ ข้ามเลย

          html_content += f"""
          <tr>
               <td colspan="6" style="text-align: left; font-weight: bold;">
                    {group_id} {group_name}
               </td>
          </tr>
          """

          # รวมข้อมูลรายวิชาแบบกลุ่ม subject_id
          subjects_grouped = defaultdict(list)
          for subject in students_plan:
               if subject.get("group_id") == group_id:
                    subjects_grouped[subject["subject_id"]].append(subject)

          # แสดงรายวิชาแบบรวม row
          for subject_id, items in subjects_grouped.items():
               subject_info = items[0]
               subject_name = subject_info.get("subject_name", "")
               pcredit = subject_info.get("practical_credits", 0)
               tcredit = subject_info.get("theory_credits", 0)
               credit = int(pcredit) + int(tcredit)

               rowspan = len(items)
               first = True
               for item in items:
                    std_year = item.get("year", "")
                    if std_year == 3:
                         std_year = year
                    else:
                         std_year = int(year) + 1
                    term = item.get("term", "")
                    total_student = item.get("total_student", "")

                    html_content += "<tr>"
                    if first:
                         html_content += f"""
                              <td rowspan="{rowspan}" style="vertical-align: top;">{subject_id}</td>
                              <td rowspan="{rowspan}" style="vertical-align: top; text-align: left;">{subject_name}</td>
                              <td rowspan="{rowspan}" style="vertical-align: top;">{credit}</td>
                         """
                         first = False
                    html_content += f"""
                         <td>{std_year}</td>
                         <td>{term}</td>
                         <td>{total_student}</td>
                    </tr>
                    """
               subject_count += 1  # เพิ่มทุกครั้งที่มีการแสดงวิชา

     html_content += "</table>"
     html_content += f"""
          <p style="font-size: 16px; margin-top: 10px; font-weight: bold;">
               รวมจำนวนรายวิชา {subject_count} รายวิชา
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