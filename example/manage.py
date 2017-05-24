# manage.py

from flask import Flask
from flask_script import Manager
from flask_dbshell import DbShell


class DevConfig(object):
    DATABASE_URI = 'sqlite:///demo.sqlite'


app = Flask(__name__)
app.config.from_object(DevConfig)
manager = Manager(app)

manager.add_command('dbshell', DbShell())

# or if your database url string is not at app.config['DATABASE_URI']
manager.add_command('dbshell', DbShell(url_config_key='SQLALCHEMY_DATABASE_URI'))

if __name__ == "__main__":
    manager.run()
