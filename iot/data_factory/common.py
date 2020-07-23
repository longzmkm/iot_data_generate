# -*- coding: utf-8 -*-
# © 2016 QYT Technology
# Authored by: Liu tianlong (tlzmkm@gmail.com)

from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float


Model = declarative_base()

engine = create_engine('sqlite:///E:/code/iot_data_generate/test.sqlite', echo=False)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()
