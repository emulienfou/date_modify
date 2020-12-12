from datetime import datetime
from date_modify import DateModify


def tests():
    dm = DateModify(datetime.now())

    print("yesterday: " + dm.modify("yesterday").isoformat())
    print("yesterday 14:00: " + dm.modify("yesterday 14:00").isoformat())
    print("yesterday noon: " + dm.modify("yesterday noon").isoformat())
    print("midnight: " + dm.modify("midnight").isoformat())
    print("today: " + dm.modify("today").isoformat())
    print("noon: " + dm.modify("noon").isoformat())
    print("tomorrow: " + dm.modify("tomorrow").isoformat())
    print("next thursday: " + dm.modify("next thursday").isoformat())
    print("last friday: " + dm.modify("last friday").isoformat())
    print("Monday: " + dm.modify("Monday").isoformat())
    print("next thursday +15 hours: " + dm.modify("next thursday +15 hours").isoformat())


if __name__ == '__main__':
    tests()
