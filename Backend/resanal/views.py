from django.views import generic
from django.db.models import Avg
from django.shortcuts import get_object_or_404, render
from django.db import IntegrityError
from django.http import HttpResponse
from rest_framework.views import APIView
from drf_multiple_model.views import (
    ObjectMultipleModelAPIView,
    FlatMultipleModelAPIView,
)
from rest_framework.response import Response
from rest_framework import status
from .models import Result, Fetch, Analize
from .crawlusn import CrawlResult
from .analizeResult import ResultAnalize
from .serializers import (
    ResultSerializer,
    FetchSerializer,
    AnalizeSerializer,
    SectionFCDSerializer,
    FCDSerializer,
    TotalFCDSerializer,
)
import requests
import bs4
from lxml import html
import re
import os
import xlsxwriter


class MultiAPIView(ObjectMultipleModelAPIView):
    def get_querylist(self):
        qsemester = self.request.query_params.get("sem")
        qbatch = self.request.query_params.get("batch")
        qsection = self.request.query_params.get("sec")
        if qsemester and qbatch and qsection:
            querylist = (
                {
                    "queryset": Result.objects.filter(
                        sem=qsemester, batch=qbatch, section=qsection, gpa__gte=4
                    ),
                    "serializer_class": ResultSerializer,
                    "label": "passCount",
                },
                {
                    "queryset": Result.objects.filter(
                        sem=qsemester, batch=qbatch, section=qsection, gpa__lt=4
                    ),
                    "serializer_class": ResultSerializer,
                    "label": "failCount",
                },
            )

            return querylist
        elif qsemester and qbatch:
            querylist = (
                {
                    "queryset": Result.objects.filter(
                        sem=qsemester, batch=qbatch, gpa__gte=4
                    ),
                    "serializer_class": ResultSerializer,
                    "label": "passCount",
                },
                {
                    "queryset": Result.objects.filter(
                        sem=qsemester, batch=qbatch, gpa__lt=4
                    ),
                    "serializer_class": ResultSerializer,
                    "label": "failCount",
                },
            )

            return querylist

            # filter_backends = [filters.SearchFilter,]
            # search_fields = ('usn',)


class ResultList(APIView):
    def get(self, request):
        # results = Result.objects.all()
        # serializer = ResultSerializer(results, many=True )
        # return Response(.data)
        queryset = Result.objects.order_by("-gpa")
        qsemester = self.request.query_params.get("sem")
        qsection = self.request.query_params.get("sec")
        qbatch = self.request.query_params.get("batch")
        qusn = self.request.query_params.get("usn")
        qscode = self.request.query_params.get("scode")

        if qsemester and qbatch and qsection and qscode is not None:
            # qscode = maping['scode']
            results = Fetch.objects.filter(
                usn__sem=qsemester,
                usn__batch=qbatch,
                usn__section=qsection,
                subcode=qscode,
            ).order_by("-totalmarks")

            # results = queryset.filter(sem = qsemester, batch = qbatch, section = qsection)

            serializer = FetchSerializer(results, many=True)
            return Response(serializer.data)
            # results = queryset.filter(sem = qsemester, batch = qbatch, section = qsection,maping__subcode=qscode)

            # serializer = ResultSerializer(results, many=True )
            # return Response(serializer.data)

        # sectionwise analysis
        if qsemester and qbatch and qsection is not None:
            # qscode = maping['scode']
            results = queryset.filter(sem=qsemester, batch=qbatch, section=qsection)

            serializer = ResultSerializer(results, many=True)
            return Response(serializer.data)

        if qsemester and qusn is not None:
            qusn = qusn + "\\n"

            print(qusn)

            results = queryset.filter(sem=qsemester, usn__iexact=qusn)

            serializer = ResultSerializer(results, many=True)
            return Response(serializer.data)

        if qsemester and qbatch is not None:
            results = queryset.filter(sem=qsemester, batch=qbatch)

            serializer = ResultSerializer(results, many=True)
            return Response(serializer.data)
        if qusn is not None:
            results = queryset.filter(usn=qusn)

            serializer = ResultSerializer(results, many=True)
            return Response(serializer.data)

    # def get_serializer_class(self):
    #     return ResultSerializer

    def post(self):
        pass


class FetchList(APIView):
    def get(self, request):

        fetches = Fetch.objects.filter(
            usn__sem=4,
            usn__section="C",
            usn__batch=2016,
            subcode="15CS42",
            totalmarks__gte=40,
        )

        serializer = FetchSerializer(fetches, many=True)
        return Response(serializer.data)

    def post(self):
        pass


def crawl(request):

    resultcrawl = CrawlResult()
    resultcrawl.initiate()

    return HttpResponse("<h1>Crawling Done</h1>")


class ResultsView(generic.ListView):
    template_name = "resanal/index.html"
    context_object_name = "all_student"

    def get_queryset(self):
        return Result.objects.all()


def analysis(request):

    resultanalize = ResultAnalize()
    resultanalize.analizeresult()

    return HttpResponse("<h1> Analysis Done! Check your website</h1>")

class AnalizeApi(APIView):
    def get(self, request):
        qsemester = self.request.query_params.get("sem")
        qsection = self.request.query_params.get("sec")
        qbatch = self.request.query_params.get("batch")
        qsubcode = self.request.query_params.get("scode").rpartition(" ")[0]

        if qsemester and qbatch and qsubcode and qsection:
            reqAnalysis = Analize.objects.filter(
                batch=qbatch, sem=qsemester, sec=qsection, subcode=qsubcode
            )
        elif qsemester and qbatch and qsubcode:
            reqAnalysis = Analize.objects.filter(
                sem=qsemester, batch=qbatch, subcode=qsubcode
            )
        else:
            pass

        serializer = AnalizeSerializer(reqAnalysis, many=True)
        return Response(serializer.data)

    def post(self):
        pass


class FCD_Section(APIView):
    def get(self, request):

        qsection = self.request.query_params.get("sec")
        qusn = self.request.query_params.get("usn")
        qscode = self.request.query_params.get("scode")
        qbatch = self.request.query_params.get("batch")

        results = Fetch.objects.filter(
            usn__section=qsection, subcode=qscode, usn__batch=qbatch
        ).order_by("-totalmarks")
        if len(results) == 0:
            return HttpResponse(status=204)
        serializer = SectionFCDSerializer(results, many=True)
        return Response(serializer.data)

    def post(self):
        pass


class GetFCD(APIView):
    def get(self, request):
        subcode = self.request.query_params.get("sc")
        batch = self.request.query_params.get("batch")
        result = Fetch.objects.filter(subcode=subcode, usn__batch=batch).order_by(
            "-totalmarks"
        )
        if len(result) == 0:
            return HttpResponse(status=204)
        serializer = FCDSerializer(result, many=True)
        return Response(serializer.data)


class TotalFCD(APIView):
    def get(self, request):
        batch = self.request.query_params.get("batch")
        semester = self.request.query_params.get("sem")
        results = Result.objects.filter(batch=batch, sem=semester).order_by("-gpa")
        if len(results) == 0:
            return HttpResponse(status=204)
        serializer = TotalFCDSerializer(results, many=True)
        return Response(serializer.data)


class TotalFCDSection(APIView):
    def get(self, request):
        batch = self.request.query_params.get("batch")
        semester = self.request.query_params.get("sem")
        section = self.request.query_params.get("sec")
        results = Result.objects.filter(
            batch=batch, sem=semester, section=section
        ).order_by("-gpa")
        if len(results) == 0:
            return HttpResponse(status=204)
        serializer = TotalFCDSerializer(results, many=True)
        return Response(serializer.data)


class GenXL(APIView):
    def get(self, request):
        cFCD = 0
        cFC = 0
        cSC = 0
        cP = 0
        cF = 0
        qsection = self.request.query_params.get("sec")
        qscode = self.request.query_params.get("scode")
        qbatch = self.request.query_params.get("batch")
        if qsection == "undefined":
            results = Fetch.objects.filter(subcode=qscode, usn__batch=qbatch).order_by(
                "usn__usn"
            )
        else:
            results = Fetch.objects.filter(
                usn__section=qsection, subcode=qscode, usn__batch=qbatch
            ).order_by("usn__usn")
        workbook = xlsxwriter.Workbook("Export.xlsx")
        worksheet = workbook.add_worksheet()
        heading = workbook.add_format({"bold": True, "border": 1})
        worksheet.write(0, 0, "Student Name", heading)
        worksheet.write(0, 1, "Student USN", heading)
        merge_format = workbook.add_format(
            {"align": "center", "bold": True, "border": 1}
        )
        border_format = workbook.add_format({"border": 1})
        border_format_fcd_green = workbook.add_format(
            {"border": 1, "bg_color": "green"}
        )
        border_format_fcd_blue = workbook.add_format({"border": 1, "bg_color": "blue"})
        border_format_fcd_yellow = workbook.add_format(
            {"border": 1, "bg_color": "yellow"}
        )
        border_format_fcd_purple = workbook.add_format(
            {"border": 1, "bg_color": "purple"}
        )
        border_format_fcd_red = workbook.add_format({"border": 1, "bg_color": "red"})
        worksheet.merge_range("C1:F1", results[0].subname, merge_format)
        worksheet.write(1, 2, "Internal Marks", heading)
        worksheet.write(1, 3, "External Marks", heading)
        worksheet.write(1, 4, "Total Marks", heading)
        worksheet.write(1, 5, "Class", heading)
        j = 2
        for i in results:
            if i.FCD == "FCD":
                fcd_format = border_format_fcd_green
                cFCD = cFCD + 1
            elif i.FCD == "FC":
                fcd_format = border_format_fcd_blue
                cFC = cFC + 1
            elif i.FCD == "SC":
                fcd_format = border_format_fcd_yellow
                cSC = cSC + 1
            elif i.FCD == "P":
                fcd_format = border_format_fcd_purple
                cP = cP + 1
            elif i.FCD == "F":
                fcd_format = border_format_fcd_red
                cF = cF + 1
            worksheet.write(j, 0, i.usn.name, border_format)
            worksheet.write(j, 1, i.usn.usn, border_format)
            worksheet.write(j, 2, i.intmarks, border_format)
            worksheet.write(j, 3, i.extmarks, border_format)
            worksheet.write(j, 4, i.totalmarks, border_format)
            worksheet.write(j, 5, i.FCD, fcd_format)
            j = j + 1
        worksheet.write("O4", "FCD", heading)
        worksheet.write("P4", "FC", heading)
        worksheet.write("Q4", "SC", heading)
        worksheet.write("R4", "P", heading)
        worksheet.write("S4", "F", heading)
        worksheet.write("O5", cFCD, border_format)
        worksheet.write("P5", cFC, border_format)
        worksheet.write("Q5", cSC, border_format)
        worksheet.write("R5", cP, border_format)
        worksheet.write("S5", cF, border_format)
        chart = workbook.add_chart({"type": "column"})
        data = ["FCD", "FC", "SC", "P", "F"]
        chart.add_series(
            {
                "data_labels": {"value": True, "position": "inside_end"},
                "categories": "=Sheet1!$O$4:$S$4",
                "values": "=Sheet1!$O$5:$S$5",
            }
        )
        chart.set_legend({"none": True})
        worksheet.insert_chart("O9", chart)
        workbook.close()
        with open("/app/Export.xlsx", "rb") as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response["Content-Disposition"] = "inline; filename=" + os.path.basename(
                "/app/Export.xlsx"
            )
            return response


class genXLDash(APIView):
    def get(self, request):
        cFCD = 0
        cFC = 0
        cSC = 0
        cP = 0
        batch = self.request.query_params.get("batch")
        sem = self.request.query_params.get("sem")
        passCount = self.request.query_params.get("pc")
        failCount = self.request.query_params.get("fc")
        results = Result.objects.filter(batch=batch, sem=sem).order_by("-gpa")
        workbook = xlsxwriter.Workbook("Export.xlsx")
        worksheet = workbook.add_worksheet()
        heading = workbook.add_format({"bold": True, "border": 1})
        worksheet.write(0, 0, "Student Name", heading)
        worksheet.write(0, 1, "Student USN", heading)
        worksheet.write(0, 2, "Section", heading)
        worksheet.write(0, 3, "GPA", heading)
        merge_format = workbook.add_format(
            {"align": "center", "bold": True, "border": 1}
        )
        worksheet.merge_range("E1:F1", "Overall Grade", merge_format)
        border_format = workbook.add_format({"border": 1})
        border_format_fcd_green = workbook.add_format(
            {"align": "center", "border": 1, "bg_color": "green"}
        )
        border_format_fcd_blue = workbook.add_format(
            {"align": "center", "border": 1, "bg_color": "blue"}
        )
        border_format_fcd_yellow = workbook.add_format(
            {"align": "center", "border": 1, "bg_color": "yellow"}
        )
        border_format_fcd_purple = workbook.add_format(
            {"align": "center", "border": 1, "bg_color": "purple"}
        )
        border_format_fcd_red = workbook.add_format(
            {"align": "center", "border": 1, "bg_color": "red"}
        )
        j = 1
        for i in results:
            if i.totalFCD == "FCD":
                fcd_format = border_format_fcd_green
                cFCD = cFCD + 1
            elif i.totalFCD == "FC":
                fcd_format = border_format_fcd_blue
                cFC = cFC + 1
            elif i.totalFCD == "SC":
                fcd_format = border_format_fcd_yellow
                cSC = cSC + 1
            elif i.totalFCD == "P":
                fcd_format = border_format_fcd_purple
                cP = cP + 1
            elif i.totalFCD == "F":
                fcd_format = border_format_fcd_red
            worksheet.write(j, 0, i.name, border_format)
            worksheet.write(j, 1, i.usn, border_format)
            worksheet.write(j, 2, i.section, border_format)
            worksheet.write(j, 3, i.gpa, border_format)
            worksheet.merge_range(j, 4, j, 5, i.totalFCD, fcd_format)
            j = j + 1
        worksheet.write("O4", "FCD", heading)
        worksheet.write("P4", "FC", heading)
        worksheet.write("Q4", "SC", heading)
        worksheet.write("R4", "P", heading)
        worksheet.write("O5", cFCD, border_format)
        worksheet.write("P5", cFC, border_format)
        worksheet.write("Q5", cSC, border_format)
        worksheet.write("R5", cP, border_format)
        chart = workbook.add_chart({"type": "column"})
        data = ["FCD", "FC", "SC", "P"]
        chart.add_series(
            {
                "data_labels": {"value": True, "position": "inside_end"},
                "categories": "=Sheet1!$O$4:$R$4",
                "values": "=Sheet1!$O$5:$R$5",
            }
        )
        chart.set_legend({"none": True})
        worksheet.insert_chart("O9", chart)
        worksheet.write("O26", "Pass", heading)
        worksheet.write("P26", "Fail", heading)
        worksheet.write("O27", int(passCount), border_format)
        worksheet.write("P27", int(failCount), border_format)
        Pchart = workbook.add_chart({"type": "pie"})
        Pchart.add_series(
            {
                "data_labels": {
                    "value": True,
                    "category": True,
                    "separator": "\n",
                    "position": "center",
                },
                "categories": "=Sheet1!$O$26:$P$26",
                "values": "=Sheet1!$O$27:$P$27",
                "points": [{"fill": {"color": "green"}}, {"fill": {"color": "red"}},],
            }
        )
        worksheet.insert_chart("O31", Pchart)
        workbook.close()
        with open("/app/Export.xlsx", "rb") as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response["ContentDisposition"] = "inline; filename=" + os.path.basename(
                "/app/Export.xlsx"
            )
            return response


class genXLDashSec(APIView):
    def get(self, request):
        cFCD = 0
        cFC = 0
        cSC = 0
        cP = 0
        batch = self.request.query_params.get("batch")
        sem = self.request.query_params.get("sem")
        sec = self.request.query_params.get("sec")
        passCount = self.request.query_params.get("pc")
        failCount = self.request.query_params.get("fc")
        results = Result.objects.filter(batch=batch, sem=sem,section=sec).order_by("-gpa")
        workbook = xlsxwriter.Workbook("Export.xlsx")
        worksheet = workbook.add_worksheet()
        heading = workbook.add_format({"bold": True, "border": 1})
        worksheet.write(0, 0, "Student Name", heading)
        worksheet.write(0, 1, "Student USN", heading)
        worksheet.write(0, 2, "Section", heading)
        worksheet.write(0, 3, "GPA", heading)
        merge_format = workbook.add_format(
            {"align": "center", "bold": True, "border": 1}
        )
        worksheet.merge_range("E1:F1", "Overall Grade", merge_format)
        border_format = workbook.add_format({"border": 1})
        border_format_fcd_green = workbook.add_format(
            {"align": "center", "border": 1, "bg_color": "green"}
        )
        border_format_fcd_blue = workbook.add_format(
            {"align": "center", "border": 1, "bg_color": "blue"}
        )
        border_format_fcd_yellow = workbook.add_format(
            {"align": "center", "border": 1, "bg_color": "yellow"}
        )
        border_format_fcd_purple = workbook.add_format(
            {"align": "center", "border": 1, "bg_color": "purple"}
        )
        border_format_fcd_red = workbook.add_format(
            {"align": "center", "border": 1, "bg_color": "red"}
        )
        j = 1
        for i in results:
            if i.totalFCD == "FCD":
                fcd_format = border_format_fcd_green
                cFCD = cFCD + 1
            elif i.totalFCD == "FC":
                fcd_format = border_format_fcd_blue
                cFC = cFC + 1
            elif i.totalFCD == "SC":
                fcd_format = border_format_fcd_yellow
                cSC = cSC + 1
            elif i.totalFCD == "P":
                fcd_format = border_format_fcd_purple
                cP = cP + 1
            elif i.totalFCD == "F":
                fcd_format = border_format_fcd_red
            worksheet.write(j, 0, i.name, border_format)
            worksheet.write(j, 1, i.usn, border_format)
            worksheet.write(j, 2, i.section, border_format)
            worksheet.write(j, 3, i.gpa, border_format)
            worksheet.merge_range(j, 4, j, 5, i.totalFCD, fcd_format)
            j = j + 1
        worksheet.write("O4", "FCD", heading)
        worksheet.write("P4", "FC", heading)
        worksheet.write("Q4", "SC", heading)
        worksheet.write("R4", "P", heading)
        worksheet.write("O5", cFCD, border_format)
        worksheet.write("P5", cFC, border_format)
        worksheet.write("Q5", cSC, border_format)
        worksheet.write("R5", cP, border_format)
        chart = workbook.add_chart({"type": "column"})
        data = ["FCD", "FC", "SC", "P"]
        chart.add_series(
            {
                "data_labels": {"value": True, "position": "inside_end"},
                "categories": "=Sheet1!$O$4:$R$4",
                "values": "=Sheet1!$O$5:$R$5",
            }
        )
        chart.set_legend({"none": True})
        worksheet.insert_chart("O9", chart)
        worksheet.write("O26", "Pass", heading)
        worksheet.write("P26", "Fail", heading)
        worksheet.write("O27", int(passCount), border_format)
        worksheet.write("P27", int(failCount), border_format)
        Pchart = workbook.add_chart({"type": "pie"})
        Pchart.add_series(
            {
                "data_labels": {
                    "value": True,
                    "category": True,
                    "separator": "\n",
                    "position": "center",
                },
                "categories": "=Sheet1!$O$26:$P$26",
                "values": "=Sheet1!$O$27:$P$27",
                "points": [{"fill": {"color": "green"}}, {"fill": {"color": "red"}},],
            }
        )
        worksheet.insert_chart("O31", Pchart)
        workbook.close()
        with open("/app/Export.xlsx", "rb") as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response["ContentDisposition"] = "inline; filename=" + os.path.basename(
                "/app/Export.xlsx"
            )
            return response


class getAllXL(APIView):
    def get(self, request):
        batch = self.request.query_params.get("batch")
        sem = self.request.query_params.get("sem")
        results = Result.objects.filter(batch=batch, sem=sem).order_by("usn")
        workbook = xlsxwriter.Workbook("Export.xlsx")
        worksheet = workbook.add_worksheet()
        heading = workbook.add_format({"bold": True, "border": 1})
        worksheet.write(0, 0, "Student Name", heading)
        merge_format = workbook.add_format(
            {"align": "center", "bold": True, "border": 1}
        )
        worksheet.write(0, 1, "Student USN", heading)
        worksheet.write(0, 2, "Section", heading)
        subs = set()
        for i in results:
            for j in i.maping.all():
                subs.add(j.subcode)
        subs = sorted(subs)
        j = 3
        for i in subs:
            worksheet.merge_range(0, j, 0, j + 3, i, merge_format)
            worksheet.write(1, j, "Internal Marks", heading)
            j = j + 1
            worksheet.write(1, j, "External Marks", heading)
            j = j + 1
            worksheet.write(1, j, "Total Marks", heading)
            j = j + 1
            worksheet.write(1, j, "Class", heading)
            j = j + 1

        worksheet.write(0, j, "GPA", heading)
        border_format = workbook.add_format({"border": 1})
        border_format_fcd_green = workbook.add_format(
            {"align": "center", "border": 1, "bg_color": "green"}
        )
        border_format_fcd_blue = workbook.add_format(
            {"align": "center", "border": 1, "bg_color": "blue"}
        )
        border_format_fcd_yellow = workbook.add_format(
            {"align": "center", "border": 1, "bg_color": "yellow"}
        )
        border_format_fcd_purple = workbook.add_format(
            {"align": "center", "border": 1, "bg_color": "purple"}
        )
        border_format_fcd_red = workbook.add_format(
            {"align": "center", "border": 1, "bg_color": "red"}
        )
        row = 2
        col = 3
        for i in results:
            worksheet.write(row, 0, i.name, border_format)
            worksheet.write(row, 1, i.usn, border_format)
            worksheet.write(row, 2, i.section, border_format)
            for j in subs:
                isub = Fetch.objects.filter(subcode=j, usn__batch=batch, usn__usn=i.usn)
                if len(isub) == 1:
                    isub = isub[0]
                    if isub.FCD == "FCD":
                        fcd_format = border_format_fcd_green
                    elif isub.FCD == "FC":
                        fcd_format = border_format_fcd_blue
                    elif isub.FCD == "SC":
                        fcd_format = border_format_fcd_yellow
                    elif isub.FCD == "P":
                        fcd_format = border_format_fcd_purple
                    elif isub.FCD == "F":
                        fcd_format = border_format_fcd_red
                    worksheet.write(row, col, isub.intmarks, border_format)
                    worksheet.write(row, col + 1, isub.extmarks, border_format)
                    worksheet.write(row, col + 2, isub.totalmarks, border_format)
                    worksheet.write(row, col + 3, isub.FCD, fcd_format)
                    col = col + 4
                else:
                    worksheet.write(row, col, "-", border_format)
                    worksheet.write(row, col + 1, "-", border_format)
                    worksheet.write(row, col + 2, "-", border_format)
                    worksheet.write(row, col + 3, "-", border_format)
                    col = col + 4
            worksheet.write(row, col, i.gpa, border_format)
            row = row + 1
            col = 3
        workbook.close()
        with open("/app/Export.xlsx", "rb") as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response["Content-Disposition"] = "inline; filename=" + os.path.basename(
                "/app/Export.xlsx"
            )
            return response

    def post(self, request):
        pass


class getAllXLSec(APIView):
    def get(self, request):
        batch = self.request.query_params.get("batch")
        sem = self.request.query_params.get("sem")
        sec = self.request.query_params.get("sec")
        results = Result.objects.filter(batch=batch, sem=sem,section=sec).order_by("usn")
        workbook = xlsxwriter.Workbook("Export.xlsx")
        worksheet = workbook.add_worksheet()
        heading = workbook.add_format({"bold": True, "border": 1})
        worksheet.write(0, 0, "Student Name", heading)
        merge_format = workbook.add_format(
            {"align": "center", "bold": True, "border": 1}
        )
        worksheet.write(0, 1, "Student USN", heading)
        worksheet.write(0, 2, "Section", heading)
        subs = set()
        for i in results:
            for j in i.maping.all():
                subs.add(j.subcode)
        subs = sorted(subs)
        j = 3
        for i in subs:
            worksheet.merge_range(0, j, 0, j + 3, i, merge_format)
            worksheet.write(1, j, "Internal Marks", heading)
            j = j + 1
            worksheet.write(1, j, "External Marks", heading)
            j = j + 1
            worksheet.write(1, j, "Total Marks", heading)
            j = j + 1
            worksheet.write(1, j, "Class", heading)
            j = j + 1

        worksheet.write(0, j, "GPA", heading)
        border_format = workbook.add_format({"border": 1})
        border_format_fcd_green = workbook.add_format(
            {"align": "center", "border": 1, "bg_color": "green"}
        )
        border_format_fcd_blue = workbook.add_format(
            {"align": "center", "border": 1, "bg_color": "blue"}
        )
        border_format_fcd_yellow = workbook.add_format(
            {"align": "center", "border": 1, "bg_color": "yellow"}
        )
        border_format_fcd_purple = workbook.add_format(
            {"align": "center", "border": 1, "bg_color": "purple"}
        )
        border_format_fcd_red = workbook.add_format(
            {"align": "center", "border": 1, "bg_color": "red"}
        )
        row = 2
        col = 3
        for i in results:
            worksheet.write(row, 0, i.name, border_format)
            worksheet.write(row, 1, i.usn, border_format)
            worksheet.write(row, 2, i.section, border_format)
            for j in subs:
                isub = Fetch.objects.filter(subcode=j, usn__batch=batch, usn__usn=i.usn)
                if len(isub) == 1:
                    isub = isub[0]
                    if isub.FCD == "FCD":
                        fcd_format = border_format_fcd_green
                    elif isub.FCD == "FC":
                        fcd_format = border_format_fcd_blue
                    elif isub.FCD == "SC":
                        fcd_format = border_format_fcd_yellow
                    elif isub.FCD == "P":
                        fcd_format = border_format_fcd_purple
                    elif isub.FCD == "F":
                        fcd_format = border_format_fcd_red
                    worksheet.write(row, col, isub.intmarks, border_format)
                    worksheet.write(row, col + 1, isub.extmarks, border_format)
                    worksheet.write(row, col + 2, isub.totalmarks, border_format)
                    worksheet.write(row, col + 3, isub.FCD, fcd_format)
                    col = col + 4
                else:
                    worksheet.write(row, col, "-", border_format)
                    worksheet.write(row, col + 1, "-", border_format)
                    worksheet.write(row, col + 2, "-", border_format)
                    worksheet.write(row, col + 3, "-", border_format)
                    col = col + 4
            worksheet.write(row, col, i.gpa, border_format)
            row = row + 1
            col = 3
        workbook.close()
        with open("/app/Export.xlsx", "rb") as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response["Content-Disposition"] = "inline; filename=" + os.path.basename(
                "/app/Export.xlsx"
            )
            return response

    def post(self, request):
        pass



class Wake(APIView):
    def get(self, request):
        return HttpResponse(status=200)
