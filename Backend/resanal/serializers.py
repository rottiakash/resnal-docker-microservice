from rest_framework import serializers
# from django_filters.rest_framework import DjangoFilterBackend
from .models import Result, Fetch, Analize
  

class FetchSerializer(serializers.ModelSerializer):
    # abc = serializers.Fo
    class Meta:
        model = Fetch
        fields = '__all__'
        

class ResultSerializer(serializers.ModelSerializer):

    maping = FetchSerializer(many=True)

    class Meta:
        model = Result
        #fields = ('usn','gpa')
        fields = ('name','usn','sem','section','batch','gpa','maping')  


class AnalizeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Analize
        fields = '__all__'

class FCDSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='usn.name')
    usn = serializers.CharField(source='usn.usn')
    gpa = serializers.CharField(source='usn.gpa')
    section = serializers.CharField(source='usn.section')
    class Meta:
        model = Fetch
        fields = ('name','section', 'usn', 'intmarks', 'extmarks', 'totalmarks', 'FCD', 'gpa')


class SectionFCDSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='usn.name')
    usn = serializers.CharField(source='usn.usn')
    section = serializers.CharField(source='usn.section')
    gpa = serializers.CharField(source='usn.gpa')

    class Meta:
        model = Fetch
        fields = ('name', 'usn','section','subcode','intmarks', 'extmarks', 'totalmarks', 'FCD', 'gpa')

class TotalFCDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ('name','usn','sem','gpa','totalFCD','section')

