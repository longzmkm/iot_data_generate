# -*- coding: utf-8 -*-
# © 2016 QYT Technology
# Authored by: Liu tianlong (tlzmkm@gmail.com)
import datetime
import unittest
import settings
from factory import fuzzy
from factory.alchemy import SQLAlchemyModelFactory

from data_factory.common import session
from data_factory.models import Temperature

start_date = datetime.datetime.now()
end_date = datetime.datetime.now() + datetime.timedelta(hours=1)


class TemperatureFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Temperature
        sqlalchemy_session = session

    device_tag = fuzzy.FuzzyText(prefix='nl_temperature')
    value = fuzzy.FuzzyFloat(low=12, high=42)
    date = fuzzy.BaseFuzzyDateTime(start_dt=start_date, end_dt=end_date)


# class MyTestCase(unittest.TestCase):
#
#     def setUp(self):
#         self.session = session
#
#     def test_temperature(self):
#         for i in range(100):
#             temp = TemperatureFactory()
#
#         session.commit()


if __name__ == '__main__':
    import sqlite3
    conn = sqlite3.connect(settings.IOT_DB_PATH)
    c = conn.cursor()
    cursor = c.execute("SELECT *  from temperature")
    for row in cursor:
        print row
