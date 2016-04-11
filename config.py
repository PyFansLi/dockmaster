# -*- coding:UTF-8 -*-
import uuid, os
DBUSER = os.getenv("DBUSER")
DBPASS = os.getenv("DBPASS")
DBHOST = os.getenv("DBHOST")
DBPORT = os.getenv("DBPORT")
DBNAME = os.getenv("DBNAME")
SECRET_KEY = str(uuid.uuid4())
DEBUG = True
PORT = 8080
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://%s:%s@%s:%s/%s" % (DBUSER, DBPASS, DBHOST, DBPORT, DBNAME)
SQLALCHEMY_TRACK_MODIFICATIONS = False