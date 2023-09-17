#!/usr/bin/env python3
import json
from flask import Flask, make_response, jsonify, session, request
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = Article.query.all()

    articles_dict =  [article.to_dict() for article in articles]

    response = make_response(articles_dict, 200)

    return response

@app.route('/articles/<int:id>', methods=['GET'])
def show_article(id):
    session.setdefault('page_views', 0)
    session['page_views'] += 1
    session.modified = True

    if session['page_views'] > 3:
        response = make_response({'message' : 'Maximum pageview limit reached'}, 401)
        return response
    else:
        article = Article.query.filter(Article.id == id).first()
        article_dict = article.to_dict()
        # print(session) --> <SecureCookieSession {'page_views': 1}>
        
        # response_data = {
        #     'session': {
        #         # 'session_id': id,
        #         'session_value': session['page_views'],  # Corrected this line
        #         'session_accessed': session.accessed,
        #     },
        #     'cookies': [{cookie: request.cookies[cookie]} for cookie in request.cookies],
        # }

        # response_data.update(article_dict)

        response = article_dict, 200

        return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
