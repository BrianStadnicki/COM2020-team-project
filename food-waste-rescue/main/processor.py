import datetime as dt
from django.utils import timezone
from datetime import datetime, timedelta, time
from .models import Bundle_posting, Reservation


def week_start(day):
    return day - dt.timedelta(days=day.weekday())

def reservation_streak(request):
    user = getattr(request, "user", None)

    if not getattr(user, "is_authenticated", False):
        return {"reservation_streak": 0}

    try:
        consumer = user.consumer
    except ObjectDoesNotExist:
        return {"reservation_streak": 0}

    # only consumers get streaks

    if getattr(user, "user_type", None) != "consumer":
        return {"reservation_streak": 0}

    tz = timezone.get_current_timezone()

    # Gets all user's reservation time stamps
    res_ts = Reservation.objects.filter(
        consumer=consumer, is_collected=True
    ).values_list("time_stamp", flat=True)

    # Gets start data of each week with a reservation
    res_weeks = set()
    for ts in res_ts:
        res_date = timezone.localdate(ts, tz)
        week = week_start(res_date)
        res_weeks.add(week)

    streak = 0
    week = week_start(timezone.localdate())

    # If current week not completed but previous week has, streak is maintained until week finishes

    if week in res_weeks:
        streak += 1
    week -= dt.timedelta(weeks=1)

    while week in res_weeks:
        streak += 1
        week -= dt.timedelta(weeks=1)

    return {"reservation_streak": streak}


def bundle_pickup_time(request):
    user = getattr(request, "user", None)

    if user is None:
        return {}

    if not getattr(user, "is_authenticated", False):
        return {}

    if getattr(user, "user_type", None) != "consumer":
        return {}

    pickups = []
    for reservation in Reservation.objects.filter(
        consumer=user.consumer,
        posting__creation_time__date=datetime.date(datetime.today()),
        is_collected=False,
    ).all():
        pickups.append(reservation)

    return {"pickups": pickups}
