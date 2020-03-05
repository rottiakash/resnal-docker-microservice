from resanal.models import Result,Fetch

for i in Result.objects.filter(batch="2017",sem=5):
    print(i.usn)
    totalgrade = 0
    gpa = 0
    roundoff = 0
    for j in i.maping.all():
        if j.subcode=="17CS51":
                totalgrade += j.grade*4
        elif j.subcode=="17CS52":
                totalgrade += j.grade*4
        elif j.subcode=="17CS53":
                totalgrade += j.grade*4
        elif j.subcode=="17CS54":
                totalgrade += j.grade*4
        elif j.subcode=="17CSL57":
                totalgrade += j.grade*2
        elif j.subcode=="17CSL58":
                totalgrade += j.grade*2
        else:
                totalgrade += j.grade*3
    gpa = (totalgrade/260)*10
    roundoff = round(gpa,2)
    print(roundoff)
    i.gpa = roundoff
    i.save()