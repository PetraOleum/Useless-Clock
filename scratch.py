# https://stackoverflow.com/questions/7594656/how-to-determine-when-dst-starts-or-ends-in-a-specific-location-in-python
import pytz
import datetime as dt
from math import floor
from random import shuffle, choice, randint

tz

tzname = "Pacific/Auckland"

t1915 = dt.datetime(1915, 1, 1)
td800d = dt.timedelta(days=800)
td0 = dt.timedelta(seconds=0)

tz = pytz.timezone(tzname)

tnowUTC = dt.datetime.now(pytz.utc)

tzchanges = [{
    "start": t[0].astimezone(pytz.utc),
    "fromNow": t[0].astimezone(pytz.utc) - tnowUTC,
    "utcOffset": t[1][0],
    "tzName": t[1][2],
    "dstOffset": t[1][1]
} for t in zip(tz._utc_transition_times,
                tz._transition_info) if t[0] > t1915]

tzchange_near = [t for t in tzchanges
                 if abs(t["fromNow"]) <= td800d]


tzchange_past = [t for t in tzchanges
                 if t["fromNow"] < td0]
tzchange_future = [t for t in tzchanges
                 if t["fromNow"] > td0]

def isLeapYear(date):
    year = date.year
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


def decimalTime(time_now, time_zone=None):
    loc_time = (time_now.astimezone(time_zone) if time_zone is not None else
                time_now)
    secs = loc_time.second + loc_time.minute * 60 + loc_time.hour * 60 * 60
    total_decimal_secs = floor(100000 * secs / (60*60*24))
    decimal_secs = total_decimal_secs % 100
    decimal_mins = (total_decimal_secs // 100) % 100
    decimal_hours = (total_decimal_secs // 10000)
    return (decimal_hours, decimal_mins, decimal_secs)


def textDecimalTime(time_now, tz_options):
    tz_name = choice(tz_options)
    tz_choice = pytz.timezone(tz_name)
    decimal_time = decimalTime(time_now, tz_choice)
    decimal_text = "It's {}h{:02d} decimal time in {}".format(decimal_time[0], decimal_time[1],
                                             tz_name)
    if tz_name in pytz.country_timezones["fr"]:
        decimal_text = decimal_text + ". Vive la révolution!"
    return decimal_text


def timeBeats(time_now):
    utc1_dec = decimalTime(time_now, pytz.FixedOffset(60))
    return "@{}".format(utc1_dec[0] * 100 + utc1_dec[1])


def textBeats(time_now):
    beats_time = timeBeats(time_now)
    beats_text = "Set your watches, it's {} internet time!".format(beats_time)
    return beats_text


def IFCDate(time_now, time_zone=None):
    loc_time = (time_now.astimezone(time_zone) if time_zone is not None else
                time_now)
    year = loc_time.year
    leap_year = isLeapYear(loc_time)
    day_number = int(loc_time.strftime("%j"))
    if leap_year:
        if day_number <= 28 * 6:
            ifc_month = ((day_number - 1) // 28) + 1
            ifc_day = ((day_number - 1) % 28) + 1
            return (year, ifc_month, ifc_day)
        elif day_number == (28 * 6) + 1:
            return (year, 6, 29)
        elif day_number == 366:
            return (year, 13, 29)
        else:
            ifc_month = ((day_number - 2) // 28) + 1
            ifc_day = ((day_number - 2) % 28) + 1
            return (year, ifc_month, ifc_day)
    else:
        if day_number == 365:
            return (year, 13, 29)
        else:
            ifc_month = ((day_number - 1) // 28) + 1
            ifc_day = ((day_number - 1) % 28) + 1
            return (year, ifc_month, ifc_day)


def IFCDayName(ifc_date):
    weekdays_ifc = [
        "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
        "Saturday"
    ]
    if ifc_date[2] == 29:
        if ifc_date[1] == 13:
            return "Year Day"
        else:
            return "Leap Day"
    else:
        return weekdays_ifc[(ifc_date[2] - 1) % 7]


def IFCMonthName(ifc_date):
    months_ifc = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "Sol",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    return months_ifc[(ifc_date[1] - 1)]


def textIFC(time_now, tz_options):
    tz_name = choice(tz_options)
    tz_choice = pytz.timezone(tz_name)
    IFC_date = IFCDate(time_now, tz_choice)
    IFC_text = "It's {} {} {} {} in {} by the IFC calendar".format(
        IFCDayName(IFC_date),
        IFC_date[2],
        IFCMonthName(IFC_date),
        IFC_date[0],
        tz_name
    )
    return (IFC_text)


def fiveOClockSomewhere(time_now, tz_list, tries = 200, tol = 30):
    shuffle(tz_list)
    tz_list_subset = tz_list[:tries]
    for tz_name in tz_list_subset:
        tz = pytz.timezone(tz_name)
        local_time = time_now.astimezone(tz)
        local_1700 = tz.localize(dt.datetime(local_time.year, local_time.month,
                                 local_time.day, 17, 0, 0))
        tdiff_17 = local_time - local_1700
        tdiff_mins = tdiff_17.total_seconds() / 60
        if abs(tdiff_mins) <= tol:
            return (tz_name, tdiff_mins, local_time.strftime("%c %Z"),
                    local_1700.strftime("%c %Z"),
                    tdiff_17.total_seconds())
    return None


def text5OClock(time_now, tz_options):
    found_tz = fiveOClockSomewhere(time_now, tz_options)
    if found_tz is None:
        return None
    if found_tz[1] < 0:
        text = "It's {} minute{} to 5pm in {}"
    else:
        text = "It's {} minute{} past 5pm in {}"
    return text.format(round(abs(found_tz[1])),
                       ("" if round(abs(found_tz[1])) == 1 else "s"),
                       found_tz[0])


def findTZChanges(time_now, tz):
    if ((not hasattr(tz, "_transition_info")) or
        (not hasattr(tz, "_utc_transition_times"))):
        return []
    tzchanges = [{
        "start": pytz.utc.localize(t[0]),
        "fromNow": pytz.utc.localize(t[0]) - time_now,
        "utcOffset": t[1][0],
        "tzName": t[1][2],
        "dstOffset": t[1][1]
    } for t in zip(tz._utc_transition_times,
                    tz._transition_info)]
    if len(tzchanges) == 0:
        return []
    tzchanges_shift = ([tzc["start"] for tzc in tzchanges[1:]] +
                       [pytz.utc.localize(dt.datetime.max)])
    for i in range(len(tzchanges)):
        tzchanges[i].update({"end": tzchanges_shift[i]})
    return tzchanges


def nextTZChange(time_now, tz):
    tzchanges = findTZChanges(time_now, tz)
    tzchanges_future = [t for t in tzchanges
                        if t["fromNow"].total_seconds() > 0]
    tzchanges_past = [t for t in tzchanges
                        if t["fromNow"].total_seconds() <= 0]
    if len(tzchanges_past) == 0 or len(tzchanges_future) == 0:
        return None
    return (tzchanges_future[0]["fromNow"], tzchanges_future[0]["start"],
            tzchanges_past[-1]["tzName"], tzchanges_future[0]["tzName"])


def textNextOffset(time_now, tz_options):
    shuffle(tz_options)
    tries = 200
    tz_list_subset = tz_options[:tries]
    for tz_name in tz_list_subset:
        tz_obj = pytz.timezone(tz_name)
        ntz = nextTZChange(time_now, tz_obj)
        if ntz is not None:
            ntz_text = ("The next time zone change for {} will be from {} to "
                        "{} in about {} days").format(
                            tz_name, ntz[2], ntz[3],
                            round(ntz[0].total_seconds()/(60*60*24)))
            return ntz_text
    return None


def lastTZChange(time_now, tz):
    tzchanges = findTZChanges(time_now, tz)
    tzchanges_past = [t for t in tzchanges
                        if t["fromNow"].total_seconds() <= 0]
    if len(tzchanges_past) < 3:
        return None
    return (tzchanges_past[-1]["fromNow"], tzchanges_past[-1]["start"],
            tzchanges_past[-2]["tzName"], tzchanges_past[-1]["tzName"])


def textLastOffset(time_now, tz_options):
    shuffle(tz_options)
    tries = 200
    tz_list_subset = tz_options[:tries]
    for tz_name in tz_list_subset:
        tz_obj = pytz.timezone(tz_name)
        ntz = lastTZChange(time_now, tz_obj)
        if ntz is not None:
            dago = -ntz[0].total_seconds()/(60*60*24)
            if dago < 500:
                ago_text = "{} days".format(round(dago))
            elif dago < 3000:
                ago_text = "{} years".format(round(dago/365.25, 1))
            else:
                ago_text = "{} years".format(round(dago/365.25))
            ntz_text = ("The last time zone change for {} was from {} to "
                        "{} about {} ago").format(
                            tz_name, ntz[2], ntz[3],
                            ago_text)
            return ntz_text
    return None


def formerOffset(time_now, tz, tolerance_days = 366):
    time_now_utc = time_now.astimezone(pytz.utc)
    local_time = time_now.astimezone(tz)
    tzchanges = findTZChanges(time_now, tz)
    diffTolerance = dt.timedelta(days = tolerance_days)
    tzchanges_past = [t for t in tzchanges
                        if t["fromNow"] < -difft]
    if len(tzchanges_past) < 2:
        return []
    tzchanges_past = tzchanges_past[1:]
    offsets_close = [t["utcOffset"].total_seconds() for t in tzchanges if
                     t["fromNow"] <= difft and t["fromNow"] >= -difft] + [local_time.utcoffset().total_seconds()]
    tzchanges_diff = [t for t in tzchanges_past if
                      t["utcOffset"].total_seconds() not in offsets_close]
    shuffle(tzchanges_diff)
    valid_dates = []
    for tchange in tzchanges_diff:
        try:
            poss_dates = [pytz.utc.localize(dt.datetime(year, time_now_utc.month, time_now_utc.day,
                                      time_now_utc.hour, time_now_utc.minute,
                                      time_now_utc.second)).astimezone(tz) for
                          year in range(tchange["start"].year,
                                        tchange["end"].year + 1)]
            valid_dates = valid_dates + [d for d in poss_dates if d >= tchange["start"] and d
                           < tchange["end"]]
        except Exception as e:
            print(e)
            pass
    valid_dates.sort()
    return valid_dates


def textFormerOffset(time_now, tz_options):
    tnow_year = time_now.year
    shuffle(tz_options)
    tries = 200
    tz_list_subset = tz_options[:tries]
    for tz_name in tz_list_subset:
        tz_obj = pytz.timezone(tz_name)
        f_offsets = formerOffset(time_now, tz_obj)
        if len(f_offsets) > 0:
            chosen_time = max(f_offsets)
            tnow_local = time_now.astimezone(tz_obj)
            now_offset = tnow_local.utcoffset()
            then_offset = chosen_time.utcoffset()
            mins_later = round((now_offset - then_offset).total_seconds() / 60)
            if mins_later > 0:
                mins_text = "{} minutes later".format(mins_later)
            else:
                mins_text = "{} minutes earlier".format(-mins_later)
            ct_utc_year = chosen_time.astimezone(pytz.utc).year
            ct_text = ("Exactly {} years ago in {} it was {}, but "
                       "right now it is {} in {}").format(
                tnow_year - ct_utc_year,
                tz_name,
                chosen_time.strftime("%H:%M %Z"),
                mins_text,
                tnow_local.tzname()
            )
            return ct_text
    return None


def textRandomTimezone(time_now, tz_options):
    tz_name = choice(tz_options)
    tz_obj = pytz.timezone(tz_name)
    time_local = time_now.astimezone(tz_obj)
    rtz_text = ("It is {} in {}").format(
        time_local.strftime("%H:%M %Z on %A %-d %B %Y"),
        tz_name
    )
    return rtz_text


def randomTimeText(time_now, tz_options):
    r = randint(0, 999)
    if r < 25:
        t_text = textIFC(time_now, tz_options)
    elif r < 50:
        t_text = textNextOffset(time_now, tz_options)
    elif r < 100:
        t_text = text5OClock(time_now, tz_options)
    elif r < 150:
        t_text = textBeats(time_now)
    elif r < 250:
        t_text = textLastOffset(time_now, tz_options)
    elif r < 400:
        t_text = textFormerOffset(time_now, tz_options)
    elif r < 700:
        t_text = textDecimalTime(time_now, tz_options)
    else:
        t_text = textRandomTimezone(time_now, tz_options)
    if t_text is None:
        t_text = textDecimalTime(time_now, tz_options)
    return t_text


def main(mastodon_connection=None):
    t_now_utc = dt.datetime.now(pytz.utc)
    toot_text = randomTimeText(t_now_utc, pytz.common_timezones)
    if mastodon_connection is None:
        print(t_now_utc.strftime("%c %Z:"))
        print(toot_text)
        print()

