import os
import requests
import operator
import re
import nltk
import json
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from stop_words import stops
from collections import Counter
from bs4 import BeautifulSoup
from rq import Queue
from rq.job import Job

from worker import conn


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
q = Queue(connection=conn)

from models import *


def count_and_save_words(url):
    errors = []
    try:
        r = requests.get(url)
    except:
        errors.append("Unable to get URL")
        return {"error": errors}
        
    raw = BeautifulSoup(r.text, 'html.parser').get_text()
    # http://stackoverflow.com/a/10852888
    nltk.data.path.append('./nltk_data/')
    tokens = nltk.word_tokenize(raw)
    text = nltk.Text(tokens)
    nonPunct = re.compile('.*[A-Za-z].*')
    raw_words = [w for w in text if nonPunct.match(w)]
    raw_words_count = Counter(raw_words)
    no_stop_words = [w for w in raw_words if w.lower() not in stops]
    no_stop_words_count = Counter(no_stop_words)
    
    try:
        result = Result(
            url=url,
            result_all=raw_words_count,
            result_no_stop_words=no_stop_words_count
        )
        db.session.add(result)
        db.session.commit()
        return result.id
    except:
        errors.append("Unable to add item to db")
        return {"error": errors}
        
@app.route('/', methods=['GET', 'POST'])
def hello():
    return render_template('index.html')
    
    
@app.route('/start', methods=['POST'])
def get_counts():
    data = json.loads(request.data.decode())
    url = data["url"]
    if "http://" not in url[:7]:
        url = "http://" + url
    job = q.enqueue_call(
        func=count_and_save_words, args=(url,), result_ttl=5000
    )
    return job.get_id()


@app.route('/results/<job_key>', methods=['GET'])
def get_results(job_key):
    job = Job.fetch(job_key, connection=conn)
    if job.is_finished:
        result = Result.query.filter_by(id=job.result).first()
        results = sorted(
            result.result_no_stop_words.items(),
            key=operator.itemgetter(1),
            reverse=True
        )[:10]
        return jsonify(results)
    else:
        return ":(", 202


# @app.route('/<name>')
# def hello_name(name):
#     return "Hello {}!".format(name)


if __name__ == '__main__':
    app.run()