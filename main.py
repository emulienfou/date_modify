import unittest
import datetime
from date_modify import DateModify


class TestDateModify(unittest.TestCase):
    def setUp(self):
        super(TestDateModify, self).setUp()
        d = datetime.datetime(year=2020, month=1, day=1)
        self.dm = DateModify(d)

    def test_yesterday(self):
        self.assertEqual(self.dm.modify("yesterday").isoformat(), '2019-12-31T00:00:00')

    def test_yesterday_noon(self):
        self.assertEqual(self.dm.modify("yesterday noon").isoformat(), '2019-12-31T12:00:00')

    def test_yesterday_time(self):
        self.assertEqual(self.dm.modify("yesterday 14:00").isoformat(), '2019-12-31T14:00:00')

    def test_midnight(self):
        self.assertEqual(self.dm.modify("midnight").isoformat(), '2020-01-01T00:00:00')

    def test_today(self):
        self.assertEqual(self.dm.modify("today").isoformat(), '2020-01-01T00:00:00')

    def test_noon(self):
        self.assertEqual(self.dm.modify("noon").isoformat(), '2020-01-01T12:00:00')

    def test_tomorrow(self):
        self.assertEqual(self.dm.modify("tomorrow").isoformat(), '2020-01-02T00:00:00')

    def test_next_dayname(self):
        self.assertEqual(self.dm.modify("next thursday").isoformat(), '2020-01-02T00:00:00')

    def test_next_dayname_more(self):
        self.assertEqual(self.dm.modify("next thursday +15 hours").isoformat(), '2020-01-02T15:00:00')

    def test_last_dayname(self):
        self.assertEqual(self.dm.modify("last friday").isoformat(), '2019-12-27T00:00:00')

    def test_weekday(self):
        self.assertEqual(self.dm.modify("Monday").isoformat(), '2020-01-06T00:00:00')


if __name__ == '__main__':
    unittest.main()
