# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Student(models.Model):
    name = models.CharField(max_length=40)
    usn = models.CharField(max_length=50)
    section = models.CharField(max_length=1, null=True)
    batch = models.IntegerField(null=True)
    cgpa = models.FloatField(null=True, blank=True)


class Result(models.Model):

    class Meta:
        unique_together = (('usn', 'sem', 'batch'),)

    #name = models.CharField(max_length = 11,unique=True)
    name = models.CharField(max_length=40)
    usn = models.CharField(max_length=50)
    sem = models.IntegerField(null=True)
    section = models.CharField(max_length=1, null=True)
    batch = models.IntegerField(null=True)
    gpa = models.FloatField(null=True, blank=True)
    totalFCD = models.CharField(max_length=3, blank=True)

    #volume = models.IntegerField

    def __str__(self):
        return (self.name)


class Fetch(models.Model):

    class Meta:
        unique_together = (('usn', 'subcode', 'subname'),)

    usn = models.ForeignKey(
        Result, related_name='maping', on_delete=models.CASCADE)
    subcode = models.CharField(max_length=10)
    subname = models.CharField(max_length=100)
    intmarks = models.IntegerField()
    extmarks = models.IntegerField()
    totalmarks = models.IntegerField()
    grade = models.IntegerField(null=True, blank=True)
    FCD = models.CharField(max_length=3, blank=True)

    def __str__(self):
        return self.usn.name


class Analize(models.Model):

    class Meta:
        unique_together = (('batch', 'sem', 'sec', 'subcode'),)

    batch = models.IntegerField()
    sem = models.IntegerField()
    sec = models.CharField(max_length=1)
    subcode = models.CharField(max_length=8)
    passCount = models.FloatField()
    failCount = models.FloatField()
    totalCount = models.FloatField()
    average = models.FloatField()

    def __str__(self):
        return str(self.batch) + " " + str(self.sem) + " " + str(self.sec) + " " + str(self.subcode)


class Data(models.Model):

    usn = models.CharField(max_length=10)
    batch = models.IntegerField()
    section = models.CharField(max_length=1)
    sem = models.IntegerField()
    done = models.BooleanField()

    class Meta:
        db_table = "Data"
