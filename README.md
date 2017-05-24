Flask DbShell
===================

The extension provides facilites for implementing Django-like ```./manage.py dbshell``` command

Installation
------------

Install the extension with one of the following commands:


```bash
$ easy_install flask-dbshell
```

or alternatively if you have pip installed:

```bash
$ pip install flask-dbshell
```

How to use
----------

Example of a simple script that runs mysql's shell

```python
from flask_dbshell import DbShell


def main():
    dbshell = DbShell('mysql://scott:tiger@server/dbname')
    dbshell.run_shell()


if __name__ == '__main__':
    main()
```

Example of use with Flask-Script:

```python
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
```


Python versions supported
-------------------------

Tested with 2.6.x, 2.7.x, and 3.6.x
