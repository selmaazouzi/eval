import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'hard to guess string')
    SPRING_URL = os.getenv('SPRING_URL', 'http://localhost:8081')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'postgresql://sys-coding-user:sys-coding-pass@localhost/sys-coding-db'

    @staticmethod
    def get_config():
        env = os.getenv('FLASK_CONFIG', 'development').lower()
        if env == 'staging':
            Config.SPRING_URL = 'https://api-syscodinghub.int.norsys-afrique.dev'
            Config.SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URL') or 'postgresql://sys-coding-user:sys-coding-pass@db-sys-coding-hub/sys-coding-db'
        if env == 'recette':
            Config.SPRING_URL = 'https://eval-api.recette.norsys-afrique.dev'
            Config.SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URL') or 'postgresql://eval-user:QeQ6gpAtOptIj65@eval-db/eval-db'
        return Config
