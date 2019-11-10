import os

SECRET_KEY = '12345678'
PWD = os.path.abspath(os.curdir)

POSTGRES_URL="ec2-23-21-91-183.compute-1.amazonaws.com:5432"
POSTGRES_USER="jyoaemdhbzzmmo"
POSTGRES_PW="b7dfc5cb281e23651d3ce373469a74dd82a7ec880831d3d2b2fbeebdbbf16aca"
POSTGRES_DB="d99im3kf48j37"
 
dbdir = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)

DEBUG = True
SQLALCHEMY_DATABASE_URI = dbdir
SQLALCHEMY_TRACK_MODIFICATIONS = False