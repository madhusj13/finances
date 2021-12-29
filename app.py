import os
import json
from flask import Flask, flash, request, redirect, url_for, session, render_template, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import logging
import datetime
import random
import re
import csv
import database_schema
import mongoengine
from database_schema import *
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('HELLO WORLD')


UPLOAD_FOLDER = '/mnt/c/Users/msharma/Documents/finances'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
CORS(app)


@app.route('/hello')
def hello():
    return 'Hello World'


@app.route('/upload', methods=['POST'])
def fileUpload():
    target = os.path.join(UPLOAD_FOLDER, 'test_docs')
    if not os.path.isdir(target):
        os.mkdir(target)
    logger.info("welcome to upload`")
    file = request.files['file']
    filename = secure_filename(file.filename)
    destination = "/".join([target, filename])
    file.save(destination)
    logger.info('THe destination is :: %s' % (destination))
    session['uploadFilePath'] = destination
    response = "Whatever you wish too return"
    return response


@app.route('/data_query', methods=['POST', 'GET'])
def data_query():
    month = request.json
    print(month['month'])
    mongoDb = 'mongodb://localhost:27017/expense_report'
    client = database_schema.connect(db='expense_report', host=mongoDb)
    logger.info('Logging inside query method')
    expense_list = []
    # create a format to serialize with flask_restful later
    expense_fields = {
        'source': '',
        'transaction_amount': '',
        'transaction_date': '',
        'transaction_store': '',
        'classification': '',
    }
    mon = Month.objects.filter(month=month['month']).first()
    if mon:
        print(mon.expenses.count())
        for obj in mon.expenses:
            expense_list.append(
                {
                    'source': 'Capital One',
                    'transaction_amount': obj.transaction_amount,
                    'transaction_date': re.sub('\"', '', str(obj.transaction_date).split(' ')[0]),
                    'transaction_store': obj.transaction_store,
                    'classification': obj.classification,
                }
            )
        print(expense_list)
        return json.dumps(sorted(expense_list, key=lambda i: i['transaction_amount'], reverse=True))
        # return json.dumps(expense_list)
    else:
        return ''


@app.route('/month_query', methods=['POST', 'GET'])
def month_query():
    month_list = []

    mongoDb = 'mongodb://localhost:27017/expense_report'
    client = database_schema.connect(db='expense_report', host=mongoDb)
    logger.info('Logging inside month query method')
    for item in Month.objects:
        month_list.append(
            item.month
        )
    return render_template(
        "expense_table.jinja2",
        input=month_list,
    )


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True, host="0.0.0.0", port='50000', use_reloader=True)
