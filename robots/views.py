from django.http import HttpResponse, HttpResponseBadRequest

from robots.reports import get_weekly_report


def download_last_week_report(request):
    excel_bytes = get_weekly_report()

    response = HttpResponse(excel_bytes, content_type="application/vnd.ms-excel")
    response['Content-Disposition'] = 'inline; filename=last_week_report.xlsx'
    return response
