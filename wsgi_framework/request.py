from urllib.parse import parse_qs

class Request:
    def __init__(self, environ):
        self.method = environ['REQUEST_METHOD']
        self.path = environ['PATH_INFO']
        self.query = parse_qs(environ.get('QUERY_STRING', ''))
        self.headers = {k[5:].replace('_', '-').title(): v for k, v in environ.items() if k.startswith('HTTP_')}
        self.environ = environ
        self._body = None

    @property
    def body(self):
        if self._body is None:
            try:
                length = int(self.environ.get('CONTENT_LENGTH', 0))
            except (ValueError, TypeError):
                length = 0
            self._body = self.environ['wsgi.input'].read(length) if length > 0 else b''
        return self._body

    def form(self):
        if self.method == 'POST':
            return parse_qs(self.body.decode())
        return {}