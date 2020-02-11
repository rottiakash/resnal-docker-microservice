from resanal.models import Fetch,Result
import xlrd

book = xlrd.open_workbook('20181st.xlsx')
first_sheet = book.sheet_by_index(0)
#print(first_sheet.cell_value(0,0))
i = 2
while True:
    if first_sheet.cell_value(i,0) == "end":
        break
    print("USN:-"+first_sheet.cell_value(i,0))
    s = Result()
    s.name = first_sheet.cell_value(i,2)
    s.usn = first_sheet.cell_value(i,0)
    s.sem = 1
    s.section = first_sheet.cell_value(i,1)
    s.batch = 2018
    s.save()
    s1 = Fetch()
    s2 = Fetch()
    s3 = Fetch()
    s4 = Fetch()
    s5 = Fetch()
    s6 = Fetch()
    s7 = Fetch()
    s8 = Fetch()
    #sub1
    s1.usn = s
    s1.subcode = "18MAT11"
    s1.subname = "CALCULUS AND LINEAR ALGEBRA"
    s1.intmarks = first_sheet.cell_value(i,3)
    s1.extmarks = first_sheet.cell_value(i,4)
    s1.totalmarks = first_sheet.cell_value(i,5)
    s1.save()
    #sub2
    s2.usn = s
    s2.subcode = "18PHY12"
    s2.subname = "ENGINEERING PHYSICS"
    s2.intmarks = first_sheet.cell_value(i,7)
    s2.extmarks = first_sheet.cell_value(i,8)
    s2.totalmarks = first_sheet.cell_value(i,9)
    s2.save()
    #sub3
    s3.usn = s
    s3.subcode = "18ELE13"
    s3.subname = "BASIC ELECTRICAL ENGINEERING"
    s3.intmarks = first_sheet.cell_value(i,11)
    s3.extmarks = first_sheet.cell_value(i,12)
    s3.totalmarks = first_sheet.cell_value(i,13)
    s3.save()
    #sub4
    s4.usn = s
    s4.subcode = "18CIV14"
    s4.subname = "ELEMENTS OF CIVIL ENGINEERING AND MECHANICS"
    s4.intmarks = first_sheet.cell_value(i,15)
    s4.extmarks = first_sheet.cell_value(i,16)
    s4.totalmarks = first_sheet.cell_value(i,17)
    s4.save()
    #sub5
    s5.usn = s
    s5.subcode = "18EGDL15"
    s5.subname = "ENGINEERING GRAPHICS"
    s5.intmarks = first_sheet.cell_value(i,19)
    s5.extmarks = first_sheet.cell_value(i,20)
    s5.totalmarks = first_sheet.cell_value(i,21)
    s5.save()
    #sub6
    s6.usn = s
    s6.subcode = "18PHYL16"
    s6.subname = "ENGINEERING PHYSICS LABORATORY"
    s6.intmarks = first_sheet.cell_value(i,23)
    s6.extmarks = first_sheet.cell_value(i,24)
    s6.totalmarks = first_sheet.cell_value(i,25)
    s6.save()
    #sub7 
    s7.usn = s
    s7.subcode = "18ELEL17"
    s7.subname = "BASIC ELECTRICAL ENGINEERING LABORATORY"
    s7.intmarks = first_sheet.cell_value(i,27)
    s7.extmarks = first_sheet.cell_value(i,28)
    s7.totalmarks = first_sheet.cell_value(i,29)
    s7.save()
    #sub8
    s8.usn = s
    s8.subcode = "18EGH18"
    s8.subname = "TECHNICAL ENGLISH-I"
    s8.intmarks = first_sheet.cell_value(i,31)
    s8.extmarks = first_sheet.cell_value(i,32)
    s8.totalmarks = first_sheet.cell_value(i,33)
    s8.save()
    i = i+1
print('Done')
