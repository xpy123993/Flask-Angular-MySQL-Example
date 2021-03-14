import flask
import logging
from common import storage
import json
import os
import time

app = flask.Flask(__name__)
personHub = storage.InMemoryStorage()


def initializeHub():
    app.logger.info('initializing storage adapter')
    inmemory_flag = os.getenv('USE_IN_MEMORY_STORAGE')
    if inmemory_flag is None or inmemory_flag == '1':
        app.logger.info('use inmemory storage adapter')
        return storage.InMemoryStorage()
    while True:
        time.sleep(2)
        app.logger.info('initializing mysql adapter')
        host = os.getenv('MYSQL_HOST')
        username = os.getenv('MYSQL_USER')
        password = os.getenv('MYSQL_PASSWORD')
        database = os.getenv('MYSQL_DATABASE')
        app.logger.info('accessing %s' % database)
        try:
            return storage.MySQLStorage(
                host=host,
                database=database,
                username=username,
                password=password)
        except Exception:
            app.logger.info('failed to initialize, retry in 2 seconds')


@app.route('/')
def index():
    return flask.redirect('/index.html')


@app.route('/<path:path>')
def serve_static(path):
    return flask.send_from_directory('static', path)


@app.route('/api/fetch')
def fetchResources():
    return app.response_class(
        response=storage.SerializeHub(personHub.Load()),
        status=200,
        mimetype='application/json'
    )


@app.route('/api/upload', methods=['POST'])
def uploadResources():
    if len(flask.request.form['data']) > 0:
        personHub.Save(storage.DeserializeHub(flask.request.form['data']))
    return app.response_class(
        response=json.dumps({'status': 'ok'}),
        status=200,
        mimetype='application/json'
    )


if __name__ == '__main__':
    app.logger.setLevel(logging.INFO)
    personHub = initializeHub()
    app.run(host='0.0.0.0')
