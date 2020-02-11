from resanal.models import Fetch,Result

for  i in Fetch.objects.filter(usn__batch="2016",usn__sem=6):
    if i.totalmarks >= 90:
        i.grade = 10
    elif 80 <= i.totalmarks <= 89:
        i.grade = 9
    elif 70 <= i.totalmarks <= 79:
        i.grade = 8
    elif 60 <= i.totalmarks <= 69:
        i.grade = 7   
    elif 50 <= i.totalmarks <= 59:
        i.grade = 6
    elif 45 <= i.totalmarks <= 49:
        i.grade = 5            
    elif 40 <= i.totalmarks <= 44:
        i.grade = 4
    elif i.totalmarks < 40:
        i.grade = 0
    i.save()