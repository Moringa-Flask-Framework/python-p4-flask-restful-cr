#!/usr/bin/env python3

from flask import Flask, request, make_response
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
    def get(self):
        response_dict= {'message': "Welcome to the newsletter API!"}
        response = make_response(response_dict, 200)
        return response
    
class Newsletters(Resource):
    def get (self):
        # Get all entries in the database and store them as a list of dictionaries
        response_dict = [entry.to_dict for entry in Newsletter.query.all()]
        response = make_response(response_dict, 200)
        return response
    def post(self):
        new_record= Newsletter(
            title= request.form["title"],
            body=request.form["body"]
        )
        db.session.add(new_record)
        db.session.commit()

        response_dict= new_record.to_dict()
        response = make_response(response_dict, 201)
        return response
    
class NewsletterById(Resource):
    def get(self,id):
        record_dict = Newsletter.query.filter_by(id=id).first().to_dict()
        if not record_dict:
            response= make_response(404,"No such id exists.")
            return response
        else:
            response= make_response(record_dict, 200)
            return


api.add_resource(Home, '/')
api.add_resource(Newsletters, '/newsletters')
api.add_resource(NewsletterById, '/newsletters/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
