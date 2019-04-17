import psycopg2 as pg
import collections
import flask
import json
import os

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = int(os.environ.get("DB_PORT"))
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

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

        template = 'select {} from Summary {} order by random() limit 1;'

        if req.method == 'POST':
            data = json.loads(str(req.data, 'ascii'))
            condition = 'where Date = "{}"'.format(data['date'])

        with pg.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, port=DB_PORT, password=DB_PASS) as db:
            query = template.format(columns, condition)

            with db.cursor() as cur:
                cur.execute(query)

                res['results'] = [Summary(*result)._asdict() for result in cur.fetchall()]
                res['successful'] = True

    except Exception as err:
        print(err)
        pass

    return flask.jsonify(res)
