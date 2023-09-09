from flaskapp import app

from flask import render_template, make_response, request, Response, jsonify, json, session, redirect, url_for, \
    send_file
import functools
from werkzeug.utils import secure_filename
from util import solution, get_color
import json


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/api/text', methods=['POST'])
def post_text():
    if not request.json or 'text' not in request.json:
        return bad_request()
    else:
        text = request.json['text']
        response, weights_dict = solution(text)

        colors = []
        for word in text.split():
            colors.append(get_color(word, weights_dict))

        return json_response(response)


@app.route('/api/file', methods=['POST'])
def post_file():
    file = request.files["file"]

    return send_file(file, download_name="table.xlsx")


def json_response(data, code=200):
    return Response(status=code, mimetype="application/json", response=json.dumps(data))


def bad_request():
    return make_response(jsonify({'error': 'Bad request'}), 400)
