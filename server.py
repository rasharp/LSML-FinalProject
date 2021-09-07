
# 1. Load models
import models as M

# 2. Celery part: handlers
from celery import Celery
from celery.result import AsyncResult

celery_app = Celery("server", broker='redis://redis:6379/0', backend='redis://redis:6379/0')

# celery task handlers
@celery_app.task
def LDA_handler(text):
    return M.json_text_topics(text)

@celery_app.task
def sentiment_handler(text):
    return M.predict_sentiment(text)


# 3. Flask web-server
from flask import Flask, request
import json

app = Flask(__name__)

# 3.1 root entrypoint
@app.route("/")
def flask_root():
    return "Server is up. Please, use API."

# 3.2 sentiment (synchronous)
@app.route("/sentiment", methods=['GET', 'POST'])
def flask_sentiment_post():
    if request.method == 'POST':
        data = request.get_json(force=True)
        text = data['text']
#         task = sentiment_handler.delay(text)  # for asynchronous
#         res = {'task_id': task.id}
#         return json.dumps(res)
        
        res = sentiment_handler(text)
        return str(res)
        response = {
            "status": "DONE",
            "result": res
            }
        return json.dumps(response, skipkeys=True)
          
    else:
        return "Use POST request!"

@app.route('/sentiment/<task_id>')
def flask_sentiment(task_id):
    task = AsyncResult(task_id, app=celery_app)
    if task.ready():
        response = {
            "status": "DONE",
            "result": task.result
        }
    else:
        response = {
            "status": "IN_PROGRESS"
        }
    return json.dumps(response, skipkeys=True)

# 3.3 topics (asynchronous)
@app.route("/topics", methods=['GET', 'POST'])
def flask_topics_post():
    if request.method == 'POST':
        data = request.get_json(force=True)
        text = data['text']
        task = LDA_handler.delay(text)
        res = {'task_id': task.id}
        return json.dumps(res)
    else:
        return "Use POST request!"

@app.route('/topics/<task_id>')
def flask_topic(task_id):
    task = AsyncResult(task_id, app=celery_app)
    if task.ready():
        response = {
            "status": "DONE",
            "result": task.result
        }
    else:
        response = {
            "status": "IN_PROGRESS"
        }
    return json.dumps(response, skipkeys=True)


# 4. Run the server
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        IP = sys.argv[1]
        PORT = int(sys.argv[2])
    else:
        IP = "0.0.0.0"
        PORT = 9001
    app.run(IP, PORT)
