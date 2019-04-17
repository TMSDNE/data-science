import collections
import pymysql
import flask
import json
import os

HOST = os.environ.get("DB_HOST")
PORT = int(os.environ.get("DB_PORT"))
NAME = os.environ.get("DB_NAME")
USER = os.environ.get("DB_USER")
PASS = os.environ.get("DB_PASS")

app = flask.Flask(__name__)

fields = ["date", "commentary"]
columns = ', '.join(fields)
Summary = collections.namedtuple("Summary", fields)

@app.route('/', methods=['GET', 'POST'])
def index():
    res = { 'successful': False, 'results': [] }

    try:
        req = flask.request
        condition = ''

        template = '''
            select {}
            from Summary
            {}
            order by rand()
            limit 1;
        '''

        if req.method == 'POST':
            data = json.loads(str(req.data, 'ascii'))
            condition = 'where Date = "{}"'.format(data['date'])

        with pymysql.connect(HOST, user=USER, port=PORT, passwd=PASS, db=NAME) as db:
            query = template.format(columns, condition)
            db.execute(query)

            res['results'] = [Summary(*result)._asdict() for result in list(db.fetchall())]
            res['successful'] = True

    except Exception as err:
        print(err)
        pass

    return flask.jsonify(res)
