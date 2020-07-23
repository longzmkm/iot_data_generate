# -*- coding: utf-8 -*-
# © 2016 QYT Technology
# Authored by: Liu tianlong (tlzmkm@gmail.com)
from sqlalchemy import Column, Integer, String, DateTime, Float, Text

from data_factory.common import Model


class Temperature(Model):
    __tablename__ = 'temperature'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    device_tag = Column(Text)
    value = Column(Float(64))


