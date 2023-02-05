from datetime import datetime, timedelta, timezone
from io import BytesIO

from django.db.models import Count, QuerySet
from openpyxl.workbook import Workbook

from robots.models import Robot


def get_last_week_range() -> (datetime, datetime):
    now = datetime.now(tz=timezone.utc)

    start_last_week = now - timedelta(days=7 + now.weekday())
    start_last_week = start_last_week.replace(hour=0, minute=0, second=0, microsecond=0)

    end_last_week = start_last_week + timedelta(days=7) - timedelta(microseconds=1)

    return start_last_week, end_last_week


def generate_excel_bytes(robots: QuerySet[dict]):
    wb = Workbook()
    for robot in robots:
        try:
            ws = wb[robot.get('model')]
        except KeyError:
            ws = wb.create_sheet(robot.get('model'))
            ws.append(tuple(robot.keys()))
        ws.append(tuple(robot.values()))
    if robots:
        wb.remove(wb.worksheets[0])

    excel_bytes = BytesIO()
    wb.save(excel_bytes)
    return excel_bytes.getvalue()


def get_weekly_report() -> bytes:
    start_last_week, end_last_week = get_last_week_range()
    robots = Robot.objects \
        .filter(created__gte=start_last_week, created__lte=end_last_week) \
        .values('model', 'version') \
        .annotate(count=Count('model')) \
        .order_by('model')
    return generate_excel_bytes(robots)


def main():
    get_last_week_range()


if __name__ == '__main__':
    main()
