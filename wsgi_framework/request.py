import json
import xml.etree.ElementTree as et

def parse_request(environ):
    content_type = environ.get('CONTENT_TYPE', '')
    length = int(environ.get('CONTENT_LENGTH', 0))
    raw_data = environ['wsgi.input'].read(length).decode('utf-8')

    if 'application/json' in content_type:
        return json.loads(raw_data), 'json'
    elif 'application/xml' in content_type:
        root = et.fromstring(raw_data)
        return {child.tag: child.text for child in root}, 'xml'
    else:
        raise ValueError('Unsupported Content-Type')

def build_response(data, fmt):
    if fmt == 'json':
        return json.dumps(data).encode(), [("Content-Type", "application/json")]
    elif fmt == 'xml':
        xml = "<response>" + "".join(f"<{k}>{v}</{k}>" for k, v in data.items()) + "</response>"
        return xml.encode(), [("Content-Type", "application/xml")]
    return None
