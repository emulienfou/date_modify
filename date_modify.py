"""
PHP date_modify() equivalent
See https://www.php.net/manual/en/function.date-modify.php

Usage:
>>> import datetime
>>> d = datetime.datetime.now()
>>> dm = DateModify(d)
>>> dm.modify("next tuesday +15 hours")
"""
from datetime import datetime, timedelta
from dateutil.relativedelta import *
import re

YESTERDAY_REGEX = r'yesterday (([0-9]|0[0-9]|1[0-9]|2[0-3]):([0-5][0-9])|noon)'
DAYS_REGEX = r'(?i)sunday|monday|tuesday|wednesday|thursday|friday|saturday|sun|mon|tue|wed|thu|fri|sat'
RELTEXT_SPACE_WEEK_REGEX = r'(?i)(sunday|monday|tuesday|wednesday|thursday|friday|saturday|sun|mon|tue|wed|thu|fri|sat) (last|this|next) week'
NEXT_WEEK_REGEX = r'(?i)^next (\w+)$'
NEXT_WEEK_MORE_REGEX = r'(?i)^next (\w+) (\+|-)([0-9]+) (\w+)$'


class DateModify:
    def __init__(self, obj):
        if obj is None:
            self.datetime = datetime.utcnow()
        else:
            self.datetime = obj

    def modify(self, modifier):
        # Midnight of yesterday
        if re.match(r'^yesterday$', modifier):
            return self.set_to_today(self.datetime) - timedelta(days=1)
        # Yesterday at a specific time (24 hour format)
        # Yesterday at noon
        elif re.match(YESTERDAY_REGEX, modifier):
            regex = re.match(YESTERDAY_REGEX, modifier)
            if regex.group(1) == "noon":
                return self.set_to_noon(self.datetime) - timedelta(days=1)
            else:
                return self.datetime.replace(minute=int(regex.group(3)), hour=int(regex.group(2)), second=0,
                                             microsecond=0) - timedelta(days=1)
        # The time is set to 00:00:00
        if re.match(r'^midnight|today$', modifier):
            return self.set_to_today(self.datetime)
        # The time is set to 12:00:00
        elif re.match(r'^noon$', modifier):
            return self.set_to_noon(self.datetime)
        # Midnight of tomorrow
        elif re.match(r'^tomorrow$', modifier):
            return self.set_to_today(self.datetime) + timedelta(days=1)
        # Next `dayname`
        elif re.match(NEXT_WEEK_REGEX, modifier):
            the_day = re.match(NEXT_WEEK_REGEX, modifier).group(1)
            return self.get_next_dayname(the_day)
        elif re.match(NEXT_WEEK_MORE_REGEX, modifier):
            regex = re.match(NEXT_WEEK_MORE_REGEX, modifier)
            next_day = self.get_next_dayname(regex.group(1))
            return self.increase_decrease_unit(datetime=next_day, operator=regex.group(2), value=regex.group(3),
                                               unit=regex.group(4))
        elif re.match(r'^last (\w+)$', modifier):
            the_day = re.match(r'(?i)^last (.*)$', modifier).group(1)
            this_day = self.datetime - timedelta(days=1)
            while not re.match(r"(?i)^" + this_day.strftime("%A") + "$", the_day):
                this_day -= timedelta(days=1)
            return this_day
        # Handles the special format "weekday + last/this/next week".
        elif re.match(RELTEXT_SPACE_WEEK_REGEX, modifier):
            regex = re.match(r'(?i)^(\w+) (last|this|next) week$', modifier)
            print(regex.group(1))
            print(regex.group(2))
            return ""
        # Moves to the next day of this name.
        elif re.match(DAYS_REGEX, modifier):
            this_day = self.datetime + timedelta(days=1)
            while not re.match(r"(?i)^" + this_day.strftime("%A") + "$", modifier):
                this_day += timedelta(days=1)
            return this_day
        #
        elif re.match(r'^ago$', modifier):
            return ""

    # Set time to 12:00:00
    @staticmethod
    def set_to_noon(datetime):
        return datetime.replace(minute=0, hour=12, second=0, microsecond=0)

    # Set time to 00:00:00
    @staticmethod
    def set_to_today(datetime):
        return datetime.replace(minute=0, hour=0, second=0, microsecond=0)

    # Return next `dayname` from reltext
    def get_next_dayname(self, the_day):
        this_day = self.datetime + timedelta(days=1)
        while not re.match(r"(?i)^" + this_day.strftime("%A") + "$", the_day):
            this_day += timedelta(days=1)
        return this_day

    @staticmethod
    def increase_decrease_unit(datetime, operator, value, unit):
        if re.match(r'^((sec|second|min|minute|hour|day|fortnight|forthnight|month|year)s?)|weeks$', unit) is None:
            raise Exception("Not supported unit")

        if re.match(r'^(sec|second)s?$', unit):
            delta = timedelta(seconds=int(value))
        elif re.match(r'^(min|minute)s?$', unit):
            delta = timedelta(minutes=int(value))
        elif re.match(r'^(hour)s?$', unit):
            delta = timedelta(hours=int(value))
        elif re.match(r'^(day)s?$', unit):
            delta = timedelta(days=int(value))
        elif unit == "weeks":
            delta = timedelta(weeks=int(value))
        elif re.match(r'^(month)s?$', unit):
            delta = relativedelta(months=int(value))
        elif re.match(r'^(year)s?$', unit):
            delta = relativedelta(years=int(value))

        if operator == "+":
            return datetime + delta
        elif operator == "-":
            return datetime - delta
        else:
            return datetime
