class App:
    def __init__(self):
        self.routes = {"GET": {}, "POST": {}}

    def route(self, path, methods=["GET"]):
        def decorator(func):
            for method in methods:
                self.routes[method.upper()][path] = func
            return func
        return decorator

    def __call__(self, environ, start_response):
        method = environ["REQUEST_METHOD"]
        path = environ["PATH_INFO"]

        handler = self.routes.get(method, {}).get(path)
        if handler:
            from .request import parse_request, build_response
            try:
                request_data, fmt = parse_request(environ)
                response_data = handler(request_data)
                body, headers = build_response(response_data, fmt)
                start_response("200 OK", headers)
                return [body]
            except Exception as e:
                start_response("400 Bad Request", [("Content-Type", "application/json")])
                return [f'{{"error": "{str(e)}"}}'.encode()]
        else:
            start_response("404 Not Found", [("Content-Type", "text/plain")])
            return [b"Not Found"]
