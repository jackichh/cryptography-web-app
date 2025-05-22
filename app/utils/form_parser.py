import urllib.parse

def parse_form(environ):
    """Parse form data (urlencoded or multipart) from WSGI environ."""
    form = {}
    input_ = environ['wsgi.input']
    content_type = environ.get('CONTENT_TYPE', '')
    content_length = int(environ.get('CONTENT_LENGTH', '0') or 0)

    if environ['REQUEST_METHOD'] == 'GET':
        qs = environ.get('QUERY_STRING', '')
        form = urllib.parse.parse_qs(qs)
        return {k: v[0] if v else '' for k, v in form.items()}

    if content_type.startswith('application/x-www-form-urlencoded'):
        body = input_.read(content_length).decode('utf-8')
        form = urllib.parse.parse_qs(body)
        return {k: v[0] if v else '' for k, v in form.items()}

    elif content_type.startswith('multipart/form-data'):
        # Minimal manual multipart parsing
        boundary = content_type.split("boundary=")[-1]
        boundary = boundary.encode("utf-8")
        data = input_.read(content_length)
        parts = data.split(b"--" + boundary)
        for part in parts:
            if not part or part == b'--\r\n':
                continue
            headers, _, value = part.lstrip(b"\r\n").partition(b"\r\n\r\n")
            if not headers or not value:
                continue
            header_lines = headers.decode("utf-8").split("\r\n")
            disposition = [l for l in header_lines if l.lower().startswith("content-disposition:")]
            if not disposition:
                continue
            disp = disposition[0]
            name = ''
            filename = None
            for item in disp.split(";"):
                item = item.strip()
                if item.startswith("name="):
                    name = item.split("=")[1].strip('"')
                if item.startswith("filename="):
                    filename = item.split("=")[1].strip('"')
            if filename:
                # Handle uploaded file data
                # Store file metadata and content in dictionary
                # Strip trailing multipart form boundary markers
                form[name] = {"filename": filename, "content": value.rstrip(b"\r\n--")}
            else:
                form[name] = value.decode("utf-8").rstrip("\r\n")
        return form
    else:
        return {}