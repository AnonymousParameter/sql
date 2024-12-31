class BaseConfig(object):

    # 数据库的配置
    DIALCT = "postgresql"
    HOST = 'localhost'
    PORT = "5432"
    USERNAME = "postgres"
    PASSWORD = "0625" # 你自己电脑数据库的密码
    DBNAME = 'course_selection_system'


    SQLALCHEMY_DATABASE_URI = f"{DIALCT}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"
    SQLALCHEMY_ECHO = True

# # 密钥，可随意修改
# SECRET_KEY = '你猜'