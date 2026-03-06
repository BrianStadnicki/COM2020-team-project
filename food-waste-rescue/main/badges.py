from .models import Consumer, Reservation
import datetime as dt
from django.utils import timezone

TARGET_BUNDLE_QUANTITY = 3

badges = [{"name":"New Account", "url":"images/badge-award-medal-svgrepo-com.svg", "des":"Create a new account", "x":1, "y":1},
          {"name":"1 Week Streak", "url":"images/badge-award-medal-svgrepo-com.svg", "des":"Hold a streak for a week", "x":0, "y":1},
          {"name":"1 Month Streak", "url":"images/badge-award-medal-svgrepo-com.svg", "des":"Hold a streak for 4 weeks", "x":0, "y":4},
          {"name":"6 Month Streak", "url":"images/badge-award-medal-svgrepo-com.svg", "des":"Hold a streak for 26 weeks", "x":0, "y":26},
          {"name":"1 Year Streak", "url":"images/badge-award-medal-svgrepo-com.svg", "des":"Hold a streak for a 52 weeks", "x":0, "y":52},
          {"name":"1 Bundle", "url":"images/badge-award-medal-svgrepo-com.svg", "des":"Collect 1 bundle", "x":0, "y":1},
          {"name":"5 Bundles", "url":"images/badge-award-medal-svgrepo-com.svg", "des":"Collect 5 bundles", "x":0, "y":5},
          {"name":"10 Bundles", "url":"images/badge-award-medal-svgrepo-com.svg", "des":"Collect 10 bundles", "x":0, "y":10},
          {"name":"20 Bundles", "url":"images/badge-award-medal-svgrepo-com.svg", "des":"Collect 20 bundles", "x":0, "y":20},
          {"name":"Animal Lover", "url":"images/badge-award-medal-svgrepo-com.svg", "des":f"Collect {TARGET_BUNDLE_QUANTITY} pet food bundles", "x":0, "y":TARGET_BUNDLE_QUANTITY},
          {"name":"Very Veggie", "url":"images/badge-award-medal-svgrepo-com.svg", "des":f"Collect {TARGET_BUNDLE_QUANTITY} vegetarian or vegan bundles", "x":0, "y":TARGET_BUNDLE_QUANTITY}]

def week_start(day):
    return day - dt.timedelta(days=day.weekday())

def get_bundles_total(consumer):
    return Reservation.objects.filter(consumer=consumer, is_collected=True).count()

def get_longest_streak(consumer):

    tz = timezone.get_current_timezone()

    res_ts = Reservation.objects.filter(
        consumer=consumer, is_collected=True
    ).values_list("time_stamp", flat=True)

    res_weeks = set()
    for ts in res_ts:
        res_date = timezone.localdate(ts, tz)
        week = week_start(res_date)
        res_weeks.add(week)

    longest_streak = 0
    current_streak = 1

    res_weeks = list(res_weeks)
    res_weeks.sort()

    for i in range(1, len(res_weeks)):

        if res_weeks[i] - res_weeks[i-1] == dt.timedelta(weeks=1):
            current_streak += 1
        else:
            if current_streak > longest_streak:
                longest_streak = current_streak
            current_streak = 1

    if current_streak > longest_streak:
        return current_streak

    return longest_streak


def get_animal_lover(consumer):
    return Reservation.objects.filter(consumer=consumer, is_collected=True, posting__category="PF").count()

def get_very_veggie(consumer):
    return Reservation.objects.filter(consumer=consumer, is_collected=True, posting__category__in=["V", "VE"]).count()


def get_badges(consumer: Consumer):
    
    l_streak = get_longest_streak(consumer)
    for i in range(1, 5):
        badges[i]["x"] = l_streak if l_streak < badges[i]["y"] else badges[i]["y"]

    bund_t = get_bundles_total(consumer)
    for i in range(5, 9):
        badges[i]["x"] = bund_t if bund_t < badges[i]["y"] else badges[i]["y"]

    a_lover = get_animal_lover(consumer)
    badges[9]["x"] = a_lover if a_lover < badges[9]["y"] else badges[9]["y"]

    v_veggie = get_very_veggie(consumer)
    badges[10]["x"] = v_veggie if v_veggie < badges[10]["y"] else badges[10]["y"]

    return badges


def get_new_badges(consumer: Consumer):

    new_badges = []
    
    l_streak = get_longest_streak(consumer)
    match l_streak:
        case 1:
            new_badges.append({**badges[1], "x": 1})
        case 4:
            new_badges.append({**badges[2], "x": 4})
        case 26:
            new_badges.append({**badges[3], "x": 26})
        case 52:
            new_badges.append({**badges[4], "x": 52})

    bund_t = get_bundles_total(consumer)
    match bund_t:
        case 1:
            new_badges.append({**badges[5], "x": 1})
        case 5:
            new_badges.append({**badges[6], "x": 5})
        case 10:
            new_badges.append({**badges[7], "x": 10})
        case 20:
            new_badges.append({**badges[8], "x": 20})

    a_lover = get_animal_lover(consumer)
    if a_lover == TARGET_BUNDLE_QUANTITY:
        new_badges.append({**badges[9], "x": a_lover})

    v_veggie = get_very_veggie(consumer)
    if v_veggie == TARGET_BUNDLE_QUANTITY:
        new_badges.append({**badges[10], "x": v_veggie})

    return new_badges