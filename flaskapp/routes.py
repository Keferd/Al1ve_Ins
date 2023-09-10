import os

from flaskapp import app
import pandas as pd
from flask import render_template, make_response, request, Response, jsonify, json, session, redirect, url_for, \
    send_file
import functools
from util import solution, get_class, get_categories
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
        model_c = request.json['model']
        response = {}
        predicted_class, weights_dict = solution(text)
        response["class"] = predicted_class
        response["categories"] = get_categories(predicted_class)
        response["weights"] = weights_dict


        return json_response(response)


@app.route('/api/file', methods=['POST'])
def post_file():
    file = request.files["file"]

    if file and file.filename.endswith('.xlsx'):
        try:
            df = pd.read_excel(file)
            if 'pr_txt' in df.columns:
                df['Уровень рейтинга'] = df['pr_txt'].apply(get_class)
                df['Категория'] = df['Уровень рейтинга'].apply(get_categories)
                new_filename = 'result.xlsx'
                save_path = os.path.join(os.path.dirname(__file__), new_filename)
                df[['pr_txt', 'Категория', 'Уровень рейтинга']].to_excel(save_path, index=False)
                return send_file(save_path, download_name=new_filename)
            else:
                return "Файл не содержит столбец 'pr_txt'", 400
        except Exception as e:
            print(e)
            return str(e), 500
    else:
        return "Файл должен быть формата .xlsx", 400


def json_response(data, code=200):
    return Response(status=code, mimetype="application/json", response=json.dumps(data))


def bad_request():
    return make_response(jsonify({'error': 'Bad request'}), 400)
