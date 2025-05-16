from app.routes import application

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('localhost', 8000, application)
    print("Server running on http://localhost:8000")
    server.serve_forever()