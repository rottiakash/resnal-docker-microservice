from resanal.models import Result,Fetch

for i in Result.objects.filter(batch="2016",sem=6):
    print(i.usn)
    totalgrade = 0
    gpa = 0
    roundoff = 0
    for j in i.maping.all():
        if j.subcode=="15CS61":
                totalgrade += j.grade*4
        if j.subcode=="15CS62":
                totalgrade += j.grade*4
        if j.subcode=="15CS63":
                totalgrade += j.grade*4
        if j.subcode=="15CS64":
                totalgrade += j.grade*4
        if j.subcode=="15CSL67":
                totalgrade += j.grade*2
        if j.subcode=="15CSL68":
                totalgrade += j.grade*2
        if j.subcode=="15CS651":
                totalgrade += j.grade*3
        if j.subcode=="15CS653":
                totalgrade += j.grade*3
        if j.subcode=="15CS664":
                totalgrade += j.grade*3
        if j.subcode=="15IM663":
                totalgrade += j.grade*3
        if j.subcode=="15MAT661":
                totalgrade += j.grade*3
    gpa = (totalgrade/260)*10
    roundoff = round(gpa,2)
    print(roundoff)
    i.gpa = roundoff
    i.save()