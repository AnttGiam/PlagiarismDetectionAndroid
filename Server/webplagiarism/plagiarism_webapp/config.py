import os


class Config:
    #file_path = os.path.abspath(os.getcwd()) + "/site.db"
    SECRET_KEY = "b003e4cc7f1b28185e695b436d842ae4"
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + file_path
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'  # SETTIAMO LA MAIL
    MAIL_PORT = '587'
    MAIL_USE_TLS = True
    #MAIL_USERNAME = os.environ.get('EMAIL_USER')  # environment variable da system ( in windows control panel)
    #MAIL_PASSWORD = os.environ.get('EMAIL_PASS')  # https://www.youtube.com/watch?v=IolxqkL7cD8
    MAIL_USERNAME = "python.project.uni@gmail.com"
    MAIL_PASSWORD = "passwordtestprogettotesi"