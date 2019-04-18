import pymysql as sql
import collections
import json
import os

DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

fields = ["date", "commentary"]
columns = ', '.join(fields)
Summary = collections.namedtuple("Summary", fields)

def handler(event, context):
    res = { 'successful': False, 'results': [] }

    try:
        condition = ''

        template = 'select {} from Summary {} order by rand() limit 1;'

        if event['httpMethod'] == 'POST':
            data = json.loads(event['body'])
            condition = 'where Date = "{}"'.format(data['date'])

        with sql.connect(host=DB_HOST, db=DB_NAME, user=DB_USER, password=DB_PASS) as db:
            query = template.format(columns, condition)
            db.execute(query)

            res['results'] = [Summary(*result)._asdict() for result in db.fetchall()]
            res['successful'] = True

    except Exception as err:
        print(err)
        pass

    return {
        'statusCode': 200,
        'body': json.dumps(res)
    } 
