import xlrd
from resanal.models import Data
book = xlrd.open_workbook('data.xlsx')
first_sheet = book.sheet_by_index(0)
i = 1

while True:
    if first_sheet.cell_value(i, 0) == "end":
        break
    USN = first_sheet.cell_value(i, 0)
    batch = first_sheet.cell_value(i, 1)
    sec = first_sheet.cell_value(i, 2)
    sem = first_sheet.cell_value(i, 3)
    print("USN:-"+first_sheet.cell_value(i, 0))
    student = Data()
    student.usn = USN
    student.batch = batch
    student.section = sec
    student.sem = sem
    student.done = False
    student.save()
    i += 1
print("Done")
