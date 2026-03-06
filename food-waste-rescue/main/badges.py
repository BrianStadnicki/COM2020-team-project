from .models import Consumer, Reservation, Bundle_posting
import datetime as dt
from django.utils import timezone

TARGET_BUNDLE_QUANTITY = 3

badges = [["New Account", None, "Create a new account", 1, 1],
          ["1 Week Streak", None, "Hold a streak for a week", 0, 1],
          ["1 Month Streak", None, "Hold a streak for 4 weeks", 0, 4],
          ["6 Month Streak", None, "Hold a streak for 26 weeks", 0, 26],
          ["1 Year Streak", None, "Hold a streak for a 52 weeks", 0, 52],
          ["1 Bundle", None, "Collect 1 bundle", 0, 1],
          ["5 Bundles", None, "Collect 5 bundles", 0, 5],
          ["10 Bundles", None, "Collect 10 bundles", 0, 10],
          ["20 Bundles", None, "Collect 20 bundles", 0, 20],
          ["Animal Lover", None, f"Collect {TARGET_BUNDLE_QUANTITY} pet food bundles", 0, TARGET_BUNDLE_QUANTITY],
          ["Very Veggie", None, f"Collect {TARGET_BUNDLE_QUANTITY} vegetarian or vegan bundles", 0, TARGET_BUNDLE_QUANTITY]]

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


def get_badges(consumer: Consumer) -> list[list]:
    
    l_streak = get_longest_streak(consumer)
    for i in range(1, 4):
        badges[i][3] = l_streak if l_streak < badges[i][4] else badges[i][4]

    bund_t = get_bundles_total(consumer)
    for i in range(5, 8):
        badges[i][3] = bund_t if bund_t < badges[i][4] else badges[i][4]

    a_lover = get_animal_lover(consumer)
    badges[9][3] = a_lover if a_lover < badges[9][4] else badges[9][4]

    v_veggie = get_very_veggie(consumer)
    badges[10][3] = v_veggie if v_veggie < badges[10][4] else badges[10][4]

    return badges


def get_new_badges(consumer: Consumer) -> list[list]:

    new_badges = []
    
    l_streak = get_longest_streak(consumer)
    match l_streak:
        case 1:
            new_badges.append(badges[1][:3]+[l_streak]+badges[1][4])
        case 4:
            new_badges.append(badges[2][:3]+[l_streak]+badges[2][4])
        case 26:
            new_badges.append(badges[3][:3]+[l_streak]+badges[3][4])
        case 52:
            new_badges.append(badges[4][:3]+[l_streak]+badges[4][4])

    bund_t = get_bundles_total(consumer)
    match bund_t:
        case 1:
            new_badges.append(badges[5][:3]+[bund_t]+badges[5][4])
        case 5:
            new_badges.append(badges[6][:3]+[bund_t]+badges[6][4])
        case 10:
            new_badges.append(badges[7][:3]+[bund_t]+badges[7][4])
        case 20:
            new_badges.append(badges[8][:3]+[bund_t]+badges[8][4])

    a_lover = get_animal_lover(consumer)
    if a_lover == TARGET_BUNDLE_QUANTITY:
        new_badges.append(badges[9][:3]+[a_lover]+badges[9][4])

    v_veggie = get_very_veggie(consumer)
    if v_veggie == TARGET_BUNDLE_QUANTITY:
        new_badges.append(badges[10][:3]+[v_veggie]+badges[10][4])

    return new_badges