import datetime
import calendar
from django.utils import timezone
from django.conf import settings

def site_info(request):
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    local_now = timezone.now()

    cal = calendar.HTMLCalendar(calendar.MONDAY)
    html_cal = cal.formatmonth(local_now.year, local_now.month)
    

    return {
        'current_date': local_now,
        'utc_date': utc_now,
        'user_timezone': settings.TIME_ZONE,
        'html_calendar': html_cal,
    }