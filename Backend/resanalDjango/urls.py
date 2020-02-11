from django.conf.urls import url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from resanal import views

urlpatterns = [
    url(r'^api/admin/', admin.site.urls),
    url(r'^api/json/', views.ResultList.as_view()),
    url(r'^api/json1/', views.FetchList.as_view()),
    url(r'^api/json2/', views.MultiAPIView.as_view()),
    url(r'^api/crawl/',views.crawl),
    url(r'^api/analize/',views.analysis),
    url(r'^api/results/',views.ResultsView.as_view()),
    url(r'^api/ranalysis/',views.AnalizeApi.as_view()),
    url(r'^api/getfcd/',views.GetFCD.as_view()),
    url(r'^api/secfcd/',views.FCD_Section.as_view()),
    url(r'^api/totalfcd/',views.TotalFCD.as_view()),
    url(r'^api/genXL/',views.GenXL.as_view()),
    url(r'^api/genXLDash/',views.genXLDash.as_view()),
    url(r'^api/genallXL/',views.getAllXL.as_view()),
    url(r'^api/wake/',views.Wake.as_view())
]

#urlpatterns = format_suffix_patterns(urlpatterns)