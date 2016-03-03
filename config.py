# -*- coding:UTF-8 -*-
import uuid
SECRET_KEY = str(uuid.uuid4())
DEBUG = False
PORT = 8080
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://username:password@ip:port/dbname"
SQLALCHEMY_TRACK_MODIFICATIONS = False