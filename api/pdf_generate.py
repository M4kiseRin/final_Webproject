from flask import Blueprint, request, send_file, Response
from api.config import getDatabase
import weasyprint
import io
import json
from urllib.parse import quote
from collections import defaultdict

pdf_api = Blueprint("pdf_api", __name__)

# สร้าง instance ของ MongoDBConfig
db_config = getDatabase()

@pdf_api.route("/pdf_generate", methods=["GET"])
def create_pdf():
    title = request.args.get("title", "ไม่มีข้อมูล")
    content = request.args.get("content", "ไม่มีข้อมูล")
    content = json.loads(content)
    std_id = request.args.get("std_id", "ไม่มีข้อมูล")
    std_name = request.args.get("std_name", "ไม่มีข้อมูล")
    std_last = request.args.get("std_last", "ไม่มีข้อมูล")
    batch_year = request.args.get("year", "ไม่มีข้อมูล")
    status = request.args.get("status", "ไม่มีข้อมูล")

    if str(status) == "1":
        html_content = f"""<html>
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
                    tr {{
                        page-break-inside: avoid;
                    }}
                    p {{
                        font-size: 14px;
                        margin-bottom: 15px;    
                    }}
                    .term-header {{
                        font-weight: bold;
                        font-size: 14px;
                        margin-top: 10px;
                    }}
                    .page-break {{
                        page-break-before: always;
                    }}
                </style>
            </head>
            <body>
        """

        for idx, item in enumerate(content):
            if idx > 0:  # ขึ้นหน้าใหม่ถ้าไม่ใช่ชุดแรก
                html_content += '<div class="page-break"></div>'

            std_id = item['std_id']
            std_name = item['std_name']
            std_last = item['std_last']
            batch_year = item['batch_year']
            course_year = 0

            subject_list = []
            student_plan = db_config.get_collection('studentPlanList')
            subjects = db_config.get_collection('subject')
            course = db_config.get_collection('syllabus')

            course_list = list(course.find())
            for c_item in sorted(course_list, key=lambda x: x["year"], reverse=True):
                if batch_year >= int(c_item["year"]):
                    course_year = c_item["year"]
                    break

            plan_list = list(student_plan.find({"std_id": std_id}))
            if plan_list:
                for p_item in plan_list:
                    subject_id = p_item["subject_id"]
                    subject_data = subjects.find_one({"subject_id": subject_id}) if subject_id else None
                    combined_data = {
                        **p_item,
                        "subject_name": subject_data.get('subject_nameTh') if subject_data else None,
                        "theory_credits": subject_data.get('theory_credits') if subject_data else 0,
                        "practical_credits": subject_data.get('practical_credits') if subject_data else 0,
                        "group_id": subject_data.get('group_id') if subject_data else None,
                    }
                    subject_list.append(combined_data)

            grouped_content = defaultdict(lambda: defaultdict(list))
            for s_item in subject_list:
                term = s_item.get("term")
                year = str(int(batch_year) + 1) if s_item.get("year") == 4 else str(int(batch_year))
                grouped_content[year][term].append(s_item)

            html_content += f"""
            <h1>แผนการเรียนตลอดหลักสูตร</h1>
            <p style="color: darkblue;">หลักสูตรบริหารธุรกิจบัณฑิต</p>
            <p style="color: darkblue;">สาขาวิชาเทคโนโลยีธุรกิจดิจิทัล (หลักสูตร พ.ศ.{course_year})</p>
            <p style="color: darkblue;">คณะบริหารธุรกิจและเทคโนโลยีสารสนเทศ</p>
            <p style="color: darkblue;">มหาวิทยาลัยเทคโนโลยีราชมงคลอีสาน วิทยาเขตขอนแก่น</p>
            <p><strong>รหัสนักศึกษา:</strong> {std_id} | <strong>ชื่อ - สกุล:</strong> {std_name} {std_last}</p>
            """

            totalAll_credits = 0
            totalAllT_credits = 0
            totalAllP_credits = 0

            for year in sorted(grouped_content.keys()):
                terms = grouped_content[year]
                for term in sorted(terms.keys(), key=int):
                    subjects = terms[term]
                    html_content += f'<div class="term-header">ภาคเรียนที่: {term} | ปีการศึกษา: {year}</div>'
                    html_content += """
                    <table>
                        <tr>
                            <th>รหัสวิชา</th>
                            <th style="width: 450px;">ชื่อวิชา</th>
                            <th>กลุ่มวิชา</th>
                            <th>ทฤษฎี</th>
                            <th>ปฏิบัติ</th>
                            <th>รวม</th>
                        </tr>
                    """

                    total_credits = 0
                    totalT_credits = 0
                    totalP_credits = 0

                    for subject in subjects:
                        total_sub_credits = subject['theory_credits'] + subject['practical_credits']
                        totalT_credits += subject['theory_credits']
                        totalP_credits += subject['practical_credits']
                        total_credits += total_sub_credits

                        html_content += f"""
                        <tr>
                            <td>{subject['subject_id']}</td>
                            <td style="text-align: left;">{subject['subject_name']}</td>
                            <td>{subject['group_id']}</td>
                            <td>{subject['theory_credits']}</td>
                            <td>{subject['practical_credits']}</td>
                            <td>{total_sub_credits}</td>
                        </tr>
                        """

                    totalAll_credits += total_credits
                    totalAllT_credits += totalT_credits
                    totalAllP_credits += totalP_credits

                    html_content += f"""
                    <tr>
                        <td colspan="3" style="text-align: right;">รวมหน่วยกิต:</td>
                        <td>{totalT_credits}</td>
                        <td>{totalP_credits}</td>
                        <td>{total_credits}</td>
                    </tr>
                    """

                    if str(term) == "2" and str(year) == str(int(batch_year) + 1):
                        html_content += f"""
                        <tr>
                            <td colspan="6" style="border: none"></td>
                        </tr>
                        <tr style="background-color: #f2f2f2;">
                            <td colspan="3">รวมหน่วยกิตตลอดหลักสูตรในแผนการเรียน </td>
                            <td>{totalAllT_credits}</td>
                            <td>{totalAllP_credits}</td>
                            <td>{totalAll_credits}</td>
                        </tr>
                        """

                    html_content += "</table>"
                    if str(term) == "3":
                        html_content += '<div class="page-break"></div>'

        html_content += "</body></html>"

        pdf = weasyprint.HTML(string=html_content).write_pdf()
        pdf_io = io.BytesIO(pdf)

        response = Response(pdf_io.getvalue(), mimetype="application/pdf")
        response.headers["Content-Disposition"] = f'inline; filename="{quote(title)}.pdf"'
        response.headers["Content-Type"] = "application/pdf"

        return response
    
    else:
        collection = db_config.get_collection('syllabus')
        course_list = list(collection.find())
        course_year = 0
        for item in sorted(course_list, key=lambda x: x["year"], reverse=True):
            if batch_year >= item["year"]:
                course_year = item["year"]
                break
            
        
        # สร้าง dictionary สำหรับจัดกลุ่มตาม term และ year
        grouped_content = defaultdict(lambda: defaultdict(list))

        for item in content:
            term = item["term"]
            year = ""
            if item["year"] == 4:
                year = str(int(batch_year) + 1)
            else:
                year = str(int(batch_year))
            grouped_content[year][term].append(item)  

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
            <h1>แผนการเรียนตลอดหลักสูตร</h1>
            <p style="color: darkblue;">หลักสูตรบริหารธุรกิจบัณฑิต</p>
            <p style="color: darkblue;">สาขาวิชาเทคโนโลยีธุรกิจดิจิทัล (หลักสูตร พ.ศ.{course_year})</p>
            <p style="color: darkblue;">คณะบริหารธุรกิจและเทคโนโลยีสารสนเทศ</p>
            <p style="color: darkblue;">มหาวิทยาลัยเทคโนโลยีราชมงคลอีสาน วิทยาเขตขอนแก่น</p>
            <p><strong>รหัสนักศึกษา:</strong> {std_id} | <strong>ชื่อ - สกุล:</strong> {std_name} {std_last}</p>
        """

        # วนลูปตามปีการศึกษา (year) และเทอม (term) ที่จัดกลุ่ม
        totalAll_credits = 0
        totalAllT_credits = 0
        totalAllP_credits = 0
        for year in sorted(grouped_content.keys()):
            terms = grouped_content[year]
            for term in sorted(terms.keys(), key=int):
                subjects = terms[term]

                html_content += f'<div class="term-header">ภาคเรียนที่: {term} | ปีการศึกษา: {year}</div>'
                html_content += """
                <table>
                    <tr>
                        <th>รหัสวิชา</th>
                        <th style="width: 450px;">ชื่อวิชา</th>
                        <th>กลุ่มวิชา</th>
                        <th>ทฤษฎี</th>
                        <th>ปฏิบัติ</th>
                        <th>รวม</th>
                    </tr>
                """
                total_credits = 0
                totalT_credits = 0
                totalP_credits = 0
                for subject in subjects:
                    total_sub_credits = subject['theory_credits'] + subject['practical_credits']
                    totalT_credits += subject['theory_credits']
                    totalP_credits += subject['practical_credits']
                    total_credits += total_sub_credits
                    html_content += f"""
                    <tr>
                        <td>{subject['subject_id']}</td>
                        <td style="text-align: left;">{subject['subject_name']}</td>
                        <td>{subject['group_id']}</td>
                        <td>{subject['theory_credits']}</td>
                        <td>{subject['practical_credits']}</td>
                        <td>{subject['theory_credits'] + subject['practical_credits']}</td>
                    </tr>
                    
                    """
                totalAll_credits += total_credits
                totalAllT_credits += totalT_credits
                totalAllP_credits += totalP_credits
                html_content += f"""
                <tr>
                    <td colspan="3" style="text-align: right;">รวมหน่วยกิต:</td>
                    <td>{totalT_credits}</td>
                    <td>{totalP_credits}</td>
                    <td>{total_credits}</td>
                </tr>
                """
                if str(term) == "2" and str(year) == str(int(batch_year)+1):
                    html_content += f"""
                    <tr>
                        <td colspan="6" style="border: none"></td>
                    </tr>
                    <tr style="background-color: #f2f2f2;">
                        <td colspan="3" >รวมหน่วยกิตตลอดหลักสูตรในแผนการเรียน </td>
                        <td>{totalAllT_credits}</td>
                        <td>{totalAllP_credits}</td>
                        <td>{totalAll_credits}</td>
                    </tr>
                    """
            
                html_content += "</table>"
                if str(term) == "3":
                    html_content += '<div class="page-break"></div>'

        html_content += "</body></html>"
        pdf = weasyprint.HTML(string=html_content).write_pdf()
        pdf_io = io.BytesIO(pdf)

        # กำหนดให้เปิดในแท็บใหม่ และให้ชื่อไฟล์เป็น "student_plan.pdf"
        response = Response(pdf_io.getvalue(), mimetype="application/pdf")
        response.headers["Content-Disposition"] = f'inline; filename="{quote(title)}.pdf"'
        response.headers["Content-Type"] = "application/pdf"

        return response