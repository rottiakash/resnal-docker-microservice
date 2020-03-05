from resanal.models import Fetch
j = 1
for i in Fetch.objects.filter(usn__batch="2016",usn__sem=7):
    if 70 <= i.totalmarks <= 100:
        FCD = "FCD"
    elif 60 <= i.totalmarks <= 69:
        FCD = "FC"
    elif 50 <= i.totalmarks <= 59:
        FCD = "SC"
    elif 40 <= i.totalmarks <= 49:
        FCD = "P"
    else:
        FCD = "F"

    print("Entry "+str(j)+":-FCD="+FCD)
    j += 1
    i.FCD = FCD
    i.save()
