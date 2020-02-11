from resanal.models import Result,Fetch
for i in Result.objects.filter(batch='2015',sem=7):
    i.delete()