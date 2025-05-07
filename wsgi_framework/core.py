from wsgi_framework.request import Request

class WSGIApp:
    def __init__(self):
        self.routes = {}

    def route(self, path, methods=['GET']):
        def decorator(func):
            for method in methods:
                self.routes[(path, method)] = func
            return func
        return decorator

    def __call__(self, environ, start_response):
        request = Request(environ)
        handler = self.routes.get((request.path, request.method))
        if handler:
            response = handler(request)
            status = response.get('status', '200 OK')
            headers = response.get('headers', [('Content-type', 'text/html; charset=utf-8')])
            start_response(status, headers)
            return [response.get('body', b'')]
        else:
            start_response('404 Not Found', [('Content-type', 'text/plain')])
            return [b'Not found']