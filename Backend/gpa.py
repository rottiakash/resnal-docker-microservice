from resanal.models import Result,Fetch

for i in Result.objects.filter(batch="2016",sem=7):
    print(i.usn)
    totalgrade = 0
    gpa = 0
    roundoff = 0
    for j in i.maping.all():
        if j.subcode=="15CS71":
                totalgrade += j.grade*4
        if j.subcode=="15CS72":
                totalgrade += j.grade*4
        if j.subcode=="15CS73":
                totalgrade += j.grade*4
        if j.subcode=="15CS744":
                totalgrade += j.grade*3
        if j.subcode=="15CS754":
                totalgrade += j.grade*3
        if j.subcode=="15CSL76":
                totalgrade += j.grade*2
        if j.subcode=="15CSL77":
                totalgrade += j.grade*2
        if j.subcode=="15CSP78":
                totalgrade += j.grade*2
    gpa = (totalgrade/240)*10
    roundoff = round(gpa,2)
    print(roundoff)
    i.gpa = roundoff
    i.save()