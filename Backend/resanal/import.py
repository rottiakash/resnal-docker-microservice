# import csv,sys,os
 
# project_dir = '/home/vikash/resanalDjango/resanalDjango'

# sys.path.append(project_dir)

# os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# import django

# django.setup()

# from resanal.models import Result

# data = csv.reader(open('/home/vikash/resanalDjango/resanal/data.csv'), delimiter=",")

# for row in data:
#     if row[0] != 'name':
#         result = Result()
#         result.name = row[0]
#         result.usn = row[1]
#         result.sem = row[2]
#         result.section = row[3]
#         result.batch = row[4]
#         result.gpa = row[5]
#         result.save()
from models import Result, Fetch

os.environ['DJANGO_SETTINGS_MODULE'] = 'resanal.settings'

with open('/data.csv') as f:
    reader = csv.reader(f)
    result = Result()
    for row in reader:

        create = Result.objects.create(
            name = row[0],
            usn = row[1],
            sem = row[2],
            section = row[3],
            batch = row[4],
            )