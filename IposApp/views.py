import os
import tempfile
from datetime import datetime
from this import s
from xmlrpc.client import DateTime
from.models import Register
from .forms import ProfileForm
from django.conf import settings
from django.db.backends import mysql
from django.shortcuts import render
import pyodbc
from django.contrib import messages
from django.contrib.sites import requests
from django.db import connections
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.shortcuts import render, redirect
from datetime import datetime

from django.template.loader import get_template
# from easy_pdf.rendering import render_to_pdf_response
# from xhtml2pdf import pisa
from fpdf import FPDF, fpdf
# import PyPDF2
# from easy_pdf.views import PDFTemplateView

# import reportlab
import io
from django.http import FileResponse
# from reportlab.pdfgen import canvas


from IposApp.utils import render_to_pdf

conn = pyodbc.connect(
    'Driver={SQL Server Native Client 10.0};'
    f'Server=SUMMIT-6\SQLEXPRESS;'
    f'Database=SummitIPOSNEW;'
    f'UID=sa;'
    f'PWD=123;'
    'Mars_Connection=Yes;'
)
def Reg(request):
    if request.method == "POST":
        CustomerName=request.POST['CustomerName']
        MobileNumber = request.POST['MobileNumber']
        NoOfPerson = request.POST['NoOfPerson']
        SelectTable = request.POST['SelectTable']
        TokenTime = request.POST['TokenTime']
        cursor = conn.cursor()
        TokenTime = datetime.now()
        query = "INSERT INTO Register(CustomerName,MobileNumber,NoOfPerson,SelectTable,TokenTime) VALUES(?,?,?,?,?)"
        cursor.execute(query, (CustomerName, MobileNumber, NoOfPerson,SelectTable,TokenTime))
        conn.commit()

        cursor = conn.cursor()
        user = "SELECT * FROM Register WHERE id = (SELECT MAX(id)FROM Register);"
        cursor.execute(user)
        user = cursor.fetchall()
        cursor.commit()
        pdf = FPDF('P', 'mm', 'A5')
        pdf.add_page()
        pdf.set_font('Arial', '', 18)
        pdf.cell(40, 10, "Company Name", 0, 1)
        pdf.line(1, 20, 85, 20)
        pdf.line(1, 70, 85, 70)
        # pdf.cell(40, 10, '', 0, 1)
        pdf.set_font('Arial', '', 10)

        for line in user:
            pdf.cell(20, 8, 'CustomerName :    ' + line.CustomerName, 0, 1, '\t')
            pdf.cell(20, 8, 'MobileNumber :    ' + line.MobileNumber, 0, 1)
            pdf.cell(20, 8, 'NoOfPerson   :      ' + str(line.NoOfPerson), 0, 1)
            pdf.cell(20, 8, 'Table        :           ' + line.SelectTable, 0, 1)
            pdf.cell(20, 8, 'TokenTime    :       ' + str(line.TokenTime), 0, 1)
            pdf.cell(20, 8, 'TokenNumber      :         ' + str(line.id), 0, 1)

        filename = tempfile.mktemp('.pdf')
        open(filename, "w").readable()
        pdf.output('report.pdf', 'F')
        return FileResponse(open('report.pdf', 'rb'))
        # return redirect('/Reg',(open,'report.pdf','rb'))
    tb = conn.execute("select * from R_Table")
    return render(request, 'Registration.html',{'tb':tb})





def Display(request):
    cursor = conn.cursor()
    cursor.execute("select * from Register order by id ASC ")
    result = cursor.fetchall()
    return render(request, 'product.html', {'result': result})
k=''
def update(request,id):
    global k
    key = request.POST.getlist("arr[]")
    num = request.GET.dict()
    print(num)
    for k in num.values():
        print("ans:", k)
    cursor=conn.cursor()
    time="'"+str(datetime.now())+"'"
    # res="UPDATE Register SET TokenIn=CONVERT(DATETIME,getdate()) WHERE id = "+str(id)
    cursor.execute("UPDATE Register SET TokenIn=CONVERT(DATETIME,getdate()),SelectTable = ? WHERE id ="+str(id),k)
    cursor.commit()
    return redirect('/')

k=''
def updt(request,id):
    global k
    key = request.POST.getlist("arr[]")
    num = request.GET.dict()
    print(num)
    for k in num.values():
        print("ans:",k)
    cursor = conn.cursor()
    cursor.execute("UPDATE Register SET SelectTable = ? WHERE id = ?",k,id)
    cursor.commit()

    return redirect('/')




def show(request,id):
    cursor=conn.cursor()
    user=("Select * from Register where id="+str(id))
    cursor.execute(user)
    user=cursor.fetchone()
    tb = conn.execute("select TableNo from R_Table")
    return render(request,'Edit.html',{'user':user,'tb':tb})


def report(request):
    cursor=conn.cursor()
    user="SELECT * FROM Register WHERE id = (SELECT MAX(id)FROM Register);"
    cursor.execute(user)
    user=cursor.fetchall()
    cursor.commit()
    pdf = FPDF('P', 'mm', 'A5')
    pdf.add_page()
    pdf.set_font('TimesNewRoman', 'B', 18)

    pdf.cell(40, 10,"Company Address", 0, 1)
    pdf.line(1, 20, 80, 20)
    pdf.line(1, 70, 80, 70)
    # pdf.cell(40, 10, '', 0, 1)
    pdf.set_font('TimesNewRoman', 'B', 10)

    for line in user:
        pdf.cell(20, 8,'CustomerName :    ' + line.CustomerName, 0, 1,'\t')
        pdf.cell(20, 8,'MobileNumber :    ' + line.MobileNumber, 0, 1)
        pdf.cell(20, 8,'NoOfPerson   :      ' + str(line.NoOfPerson), 0, 1)
        pdf.cell(20, 8,'Table        :           ' + line.SelectTable, 0, 1)
        pdf.cell(20, 8,'TokenTime    :       ' + str(line.TokenTime), 0, 1)
        pdf.cell(20, 8,'TokenNumber      :         ' + str(line.id), 0, 1)

    filename = tempfile.mktemp('.jpg')

    open(filename, "w").readable()

    pdf.output('report.pdf', 'F')
    return FileResponse(open('report.pdf', 'rb'))




























