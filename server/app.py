#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):
    pass

class Index(Resource):
    def get(self):
        response_dict = {
            "index":"Welcome to the Newsletter RESTful api"
        }
        
        response = make_response(
            jsonify(response_dict),
            200
        )
        
        return response
    
class Newsletters(Resource):
    def get(self):
        newsletters = Newsletter.query.all()
        
        return make_response(
            [newsletter.to_dict() for newsletter in newsletters],
            200
        )
        
    def post(self):
        new_newsletter = Newsletter(
            title=request.form['title'],
            body=request.form['body']
        )
        
        db.session.add(new_newsletter)
        db.session.commit()
        
        return make_response(
            new_newsletter.to_dict(),
            201
        )
    
class NewsletterById(Resource):
    def get(self, id):
        newsletter = Newsletter.query.filter(Newsletter.id == id).first()
        
        if not newsletter:
            return make_response(
                "Newsletter not found",
                404
            ) 
            
        return make_response(
            newsletter.to_dict(),
            200
        )
    
api.add_resource(Index,'/')
api.add_resource(Newsletters, '/newsletters')
api.add_resource(NewsletterById, '/newsletters/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
