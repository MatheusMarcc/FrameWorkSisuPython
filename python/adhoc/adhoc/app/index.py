import importlib
from wsgiref import simple_server
from urllib.parse import parse_qs
from orator import DatabaseManager, Model
import os
from session import get_session

def app(environ, start_response):
    path = environ['PATH_INFO']

    # Parseia query string e deixa somente o primeiro valor de cada parâmetro
    raw_params = parse_qs(environ['QUERY_STRING'])
    params = {k: v[0] for k, v in raw_params.items()}
    environ['params'] = params

    # Carrega sessão normalmente
    session_id, session = get_session(environ)
    environ['session'] = session

    # Descobre controller e ação
    path_array = path.split('/')
    classname = path_array[2].capitalize() + 'Controller'
    module = importlib.import_module("controllers." + classname)
    instance = getattr(module, classname)(environ)

    try:
        # Chama o método sem passar args posicionais
        action = path_array[3] or 'index'
        getattr(instance, action)()
    except Exception:
        import traceback
        trace = traceback.format_exc()
        print(trace)
        instance.data = "<h1>Erro Interno</h1><pre>" + trace + "</pre>"
        instance.status = "500 Internal Server Error"

    start_response(instance.status, [
        ("Content-Type", "text/html"),
        ("Location", instance.redirect_url),
        ("Set-Cookie", f"session_id={session_id}; Path=/"),
        ("Content-Length", str(len(instance.data)))
    ])
    return [instance.data.encode()]


if __name__ == '__main__':
    config = {
        'pgsql': {
            'driver': 'pgsql',
            'host': 'db',
            'database': os.environ['DB_DATABASE'],
            'user': os.environ['DB_USER'],
            'password': os.environ['DB_PASSWORD'],
            'prefix': ''
        }
    }

    db = DatabaseManager(config)
    Model.set_connection_resolver(db)
    w_s = simple_server.make_server(
        host="",
        port=8000,
        app=app
    )
    w_s.serve_forever()