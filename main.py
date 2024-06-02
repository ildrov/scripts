from datetime import datetime
from wsgiref.simple_server import make_server
import json
import pytz

def application(environ, start_response):
    path = environ.get('PATH_INFO')
    if path.startswith('/'):
        path = path[1:]
    method = environ.get('REQUEST_METHOD')

    if method == 'GET':
        tzname = path if path else 'GMT'
        try:
            tz = pytz.timezone(tzname)
            dt = datetime.now(tz)
            response_body = f"""
            <html>
                <head>
                    <title>Current Time</title>
                </head>
                <body>
                    <h1>Current Time in {tzname}</h1>
                    <p>{dt.strftime('%Y-%m-%d %H:%M:%S %Z%z')}</p>
                </body>
            </html>
            """
            start_response('200 OK', [('Content-Type', 'text/html')])
        except pytz.UnknownTimeZoneError:
            response_body = """
            <html>
                <head>
                    <title>Error</title>
                </head>
                <body>
                    <h1>Unknown timezone</h1>
                </body>
            </html>
            """
            start_response('400 Bad Request', [('Content-Type', 'text/html')])
    elif method == 'POST':
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except ValueError:
            request_body_size = 0
        request_body = environ['wsgi.input'].read(request_body_size)
        data = json.loads(request_body)

        if path == 'api/v1/convert':
            dt = datetime.strptime(data['date'], '%m.%d.%Y %H:%M:%S')
            tz = pytz.timezone(data['tz'])
            dt = tz.localize(dt)
            target_tz = pytz.timezone(data['target_tz'])
            dt = dt.astimezone(target_tz)
            response_body = dt.strftime('%Y-%m-%d %H:%M:%S %Z%z')
            start_response('200 OK', [('Content-Type', 'application/json')])
        elif path == 'api/v1/datediff':
            dt1 = datetime.strptime(data['first_date'], '%m.%d.%Y %H:%M:%S')
            tz1 = pytz.timezone(data['first_tz'])
            dt1 = tz1.localize(dt1)

            dt2 = datetime.strptime(data['second_date'], '%m.%d.%Y %H:%M:%S')
            tz2 = pytz.timezone(data['second_tz'])
            dt2 = tz2.localize(dt2)

            diff = abs((dt2 - dt1).total_seconds())
            response_body = str(diff)
            start_response('200 OK', [('Content-Type', 'application/json')])
        else:
            response_body = 'Bad Request'
            start_response('400 Bad Request', [('Content-Type', 'text/html')])
    else:
        response_body = 'Method Not Allowed'
        start_response('405 Method Not Allowed', [('Content-Type', 'text/html')])

    return [response_body.encode('utf-8')]

with make_server('', 8000, application) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()