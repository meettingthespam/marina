import os

class Config:
    SECRET_KEY =  os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    # you can set key as config
    GOOGLEMAPS_KEY = "AIzaSyDMzt-VGwRLmSEQgsfYtgUa4QkhWzWOhRU"
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'cycleincooperation@gmail.com'
    MAIL_PASSWORD = 'ThisFeelsReallyGood9'
