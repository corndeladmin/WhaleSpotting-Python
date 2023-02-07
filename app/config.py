import os

class Config(object):
    SECRET_KEY = 'secret-key'

    # SQL Alchemy
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}/{database}'.format(
        user = os.getenv('POSTGRES_USER'), 
        password = os.getenv('POSTGRES_PASSWORD'), 
        host = os.getenv('POSTGRES_HOST'), 
        database = os.getenv('POSTGRES_DATABASE'), 
    )
    
    # Flask-User
    USER_APP_NAME = os.getenv('USER_APP_NAME')
    USER_ENABLE_EMAIL = False
    USER_ENABLE_USERNAME = True
    USER_REQUIRE_RETYPE_PASSWORD = False
