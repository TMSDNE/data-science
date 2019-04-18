import pymysql as sql
import collections
import flask
import json
import os

DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

fields = ["date", "commentary"]
columns = ', '.join(fields)
Summary = collections.namedtuple("Summary", fields)

app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    res = { 'successful': False, 'results': [] }

    try:
        req = flask.request
        condition = ''

        template = 'select {} from Summary {} order by rand() limit 1;'

        if req.method == 'POST':
            data = json.loads(str(req.data, 'ascii'))
            condition = 'where Date = "{}"'.format(data['date'])

        with sql.connect(host=DB_HOST, db=DB_NAME, user=DB_USER, password=DB_PASS) as db:
            query = template.format(columns, condition)
            db.execute(query)

            res['results'] = [Summary(*result)._asdict() for result in db.fetchall()]
            res['successful'] = True

    except Exception as err:
        print(err)
        pass

    return flask.jsonify(res)
