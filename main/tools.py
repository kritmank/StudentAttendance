from django.db.models import Max, Min
from time import time, gmtime, strftime

def http_method_check(method, accepted_methods):
    if method not in accepted_methods:
        res = {
            "detail" : f"Method '{method}' Not Allowed"
        }
        return res
    return False


def getTime():
    now = time() + 3600*7
    now = gmtime(now)
    time_now = int(now.tm_hour*60 + now.tm_min) # MINUTE format
    time_text = strftime("%H:%M", now)
    date_now = strftime("%Y-%m-%d", now)
    today = strftime("%a", now).upper()

    return {"time": time_now, "time_text": time_text, "date": date_now, "today": today}


def normalize_time(time):
    time_h, time_m = time.split(":")
    time = int(time_h) * 60 + int(time_m)
    return time


def get_timetable(tables, time_now):
    # Get timetable
    max_p = tables.aggregate(Max('period'))["period__max"]
    min_p = tables.aggregate(Min('period'))["period__min"]

    if min_p != 1:
        return False
    
    param = {
        "period": None,
        "subj": None,
        "time_start": None,
        "time_end": None,
    }

    for i in range(min_p, max_p+1):
        subj = tables.filter(period=i).first()
        if subj is None:
            return False

        time_start = normalize_time(subj.time_start)
        time_end = normalize_time(subj.time_end)

        if time_now <= time_end:
            param["period"] = i
            param["subj"] = subj.subject_name
            param["time_start"] = time_start
            param["time_end"] = time_end
            break

        if i == max_p:
            param["period"] = i
            param["subj"] = subj.subject_name
            param["time_start"] = time_start
            param["time_end"] = time_end
            break
            
    return param


