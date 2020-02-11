from resanal.models import Fetch,Result
import xlrd

book = xlrd.open_workbook('2017_4th_DIP.xlsx')
first_sheet = book.sheet_by_index(0)
#print(first_sheet.cell_value(0,0))
i = 2

while True:
    if first_sheet.cell_value(i,0) == "end":
        break
    print("USN:-"+first_sheet.cell_value(i,0))
    s = Result.objects.filter(usn=first_sheet.cell_value(i,0),sem=4)[0]
    s1 = Fetch()
    s1.usn = s
    s1.subcode = "17MATDIP41"
    s1.subname = "Additional Mathematics-II"
    s1.intmarks = first_sheet.cell_value(i,39)
    s1.extmarks = first_sheet.cell_value(i,40)
    s1.totalmarks = first_sheet.cell_value(i,41)
    fcd = "F"
    if  first_sheet.cell_value(i,42) == "P":
        fcd = "FCD"
    s1.FCD = fcd
    if  first_sheet.cell_value(i,38) != "-":
        s1.save()
    i = i+1
print('Done')
    
