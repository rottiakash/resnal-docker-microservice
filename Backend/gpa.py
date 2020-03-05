from resanal.models import Result,Fetch

for i in Result.objects.filter(batch="2016",sem=7):
    print(i.usn)
    totalgrade = 0
    gpa = 0
    roundoff = 0
    for j in i.maping.all():
        if j.subcode=="15CS51":
                totalgrade += j.grade*4
        if j.subcode=="15CS52":
                totalgrade += j.grade*4
        if j.subcode=="15CS53":
                totalgrade += j.grade*4
        if j.subcode=="15CS54":
                totalgrade += j.grade*4
        if j.subcode=="17CSL57":
                totalgrade += j.grade*2
        if j.subcode=="17CSL58":
                totalgrade += j.grade*2
        else:
                totalgrade += j.grade*3
    gpa = (totalgrade/260)*10
    roundoff = round(gpa,2)
    print(roundoff)
    i.gpa = roundoff
    i.save()