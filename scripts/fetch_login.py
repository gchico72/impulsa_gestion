import urllib.request, urllib.error
try:
    r = urllib.request.urlopen('http://127.0.0.1:8000/login/')
    print('OK', r.status)
    print(r.read(4000).decode('utf-8','replace'))
except urllib.error.HTTPError as e:
    print('HTTPERR', e.code)
    try:
        print(e.read(4000).decode('utf-8','replace'))
    except Exception as ex:
        print('no body', ex)
except Exception as e:
    print('ERR', e)
