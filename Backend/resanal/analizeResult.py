from django.db.models import Avg
from django.db import IntegrityError
from django.http import HttpResponse
from .models import Result, Fetch, Analize

class ResultAnalize:
    def analizeresult(self):
        distinctBatch = Result.objects.order_by('batch').values('batch').distinct()
        for batch in distinctBatch:
            try:

                distinctSem = Fetch.objects.filter(usn__batch=batch['batch']).order_by('usn__sem').values('usn__sem').distinct()
            
                for sem in distinctSem:
                    try:
                        for section in ['A','B','C']:
                            distinctSubject = Fetch.objects.filter(usn__batch=batch['batch'],usn__sem = sem['usn__sem']).order_by('subcode').values('subcode').distinct()
                            try:
                                for subject in distinctSubject:
                                    try:
                                
                                        passC = Fetch.objects.filter(usn__sem = sem['usn__sem'],usn__section = section, usn__batch = batch['batch'],subcode=subject['subcode'],totalmarks__gte= 40).count()
                                        totalC = Fetch.objects.filter(usn__sem = sem['usn__sem'],usn__section = section, usn__batch = batch['batch'],subcode=subject['subcode']).count()
                                        failC = totalC - passC
                                        average = Fetch.objects.filter(usn__sem = sem['usn__sem'],usn__section = section, usn__batch = batch['batch'],subcode=subject['subcode']).aggregate(Avg('grade'))['grade__avg']
                                        Analize.objects.create(batch = batch['batch'],sem = sem['usn__sem'],sec = section,subcode = subject['subcode'],passCount = passC,failCount = failC,totalCount = totalC,average= average)
                                    except IntegrityError:
                                        pass
                            except IntegrityError:
                                pass
                    except IntegrityError:
                        pass
            except IntegrityError:
                    pass
        return