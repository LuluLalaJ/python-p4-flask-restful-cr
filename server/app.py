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
        message_dict = {
            'Message': 'WELCOME'
        }

        response = make_response(
            message_dict,
            200
        )

        return response

api.add_resource(Home, '/')


class Newsletters(Resource):

    def get(self):
        newsletters = Newsletter.query.all()
        newsletters_serialized = [
            nl.to_dict() for nl in newsletters
        ]

        response = make_response(
            newsletters_serialized,
            200
        )

        return response

    def post(self):

        new_record = Newsletter(
            title=request.form['title'],
            body=request.form['body'],
        )

        db.session.add(new_record)
        db.session.commit()

        response_dict = new_record.to_dict()

        response = make_response(
            response_dict,
            201,
        )

        return response

api.add_resource(Newsletters, '/newsletters')

class NewslettersById(Resource):

    def get(self, id):
        response_dict = Newsletter.query.filter_by(id=id).first().to_dict()

        response = make_response(
            response_dict,
            200
        )

        return response

    def patch(self, id):
        pass

    def delete(self, id):
        pass


api.add_resource(NewslettersById, '/newsletters/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
