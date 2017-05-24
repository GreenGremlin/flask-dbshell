from urllib.parse import urlsplit

from flask import current_app
from flask_script import Command

from .backends import load_backend
from .compatibility import iteritems


class DbShell(Command):

    def __init__(self, url_config_key='DATABASE_URI', **kwargs):
        self._options = kwargs
        self._url_config_key = url_config_key
        self._url = DbUrl(**kwargs) if 'url' in kwargs else None

    def __call__(self, app=None, *args, **kwargs):
        return self.run_shell(app)

    def run_shell(self, app):
        if self._url is None:
            self._options['url'] = app.config[self._url_config_key]
            self._url = DbUrl(**self._options)

        backend = load_backend(self._url)
        backend.run_shell()


class DbUrl(object):

    """Db url parser

    URL can be specified as a single string,
    like mysql://user:password@host:port/dbname?arg=100
    or explicitly, like DbUrl(host='localhost', port=3456, database='mydb')

    These modes are compatible, so that use can pass both url
    and override some of its parts with explicit arguments.
    I.e, DbUrl(url='mysql://user@host:port/dbname?arg=100', password='123')
    """

    _KNOWN_PARTS = ('backend', 'host', 'port',
                    'database', 'user', 'password')

    def __init__(self, url=None, **kwargs):
        parts = dict()
        if url is not None:
            self.url = url
            o = urlsplit(url, allow_fragments=False)
            parts.update(backend=o.scheme or None,
                         database=o.path.lstrip('/') or None,
                         port=o.port,
                         host=o.hostname,
                         password=o.password,
                         user=o.username)
        parts.update(**kwargs)
        # Cleaning dialect specification like
        # mysql+mysqldb://scott:tiger@localhost/foo
        # postgresql+psycopg2://scott:tiger@localhost/mydatabase
        # that is intrinsic to SQLAlchemy db urls
        backend = parts.get('backend', None)
        if (backend is not None
                and '+' in backend):
            parts.update(backend=backend.split('+')[0])
        self._set_parts(**parts)

    def _set_parts(self, **kwargs):
        for key, val in iteritems(kwargs):
            if key not in self._KNOWN_PARTS:
                raise AttributeError('Unknown argument: "%s"' % key)
            setattr(self, key, val)
        for key in set(self._KNOWN_PARTS) - set(kwargs.keys()):
            setattr(self, key, None)

    def get_connection_string(self):
        if not all([hasattr(self, key) for key in ['backend', 'user', 'host', 'database']]):
            return None

        password = ':{}'.format(self.password) if getattr(self, 'password', None) else ''
        port = ':{}'.format(self.port) if getattr(self, 'port', None) else ''
        return '{backend}://{user}{password}@{host}{port}/{database}'.format(
            backend=self.backend,
            user=self.user,
            password=password,
            host=self.host,
            port=port,
            database=self.database,
        )
