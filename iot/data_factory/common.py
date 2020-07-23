# -*- coding: utf-8 -*-
# © 2016 QYT Technology
# Authored by: Liu tianlong (tlzmkm@gmail.com)

import settings
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float


Model = declarative_base()

engine = create_engine(settings.IOT_DB_URL, echo=False)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()
