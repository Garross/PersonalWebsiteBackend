from flask import Flask, jsonify, request
# Here to handle my database.
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Float
# Here to handle object serialization.
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
#Connect to Heroku Postgres Database
app.config['Secret_Key'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get("DATABASE_URL")

#Initialize the database
db = SQLAlchemy(app)
# ma = Marshmallow(app)

db.init_app(app)

# @app.cli.command('db_create')
# def db_create():
#     db.create_all()
#     print('Database created')
#
#
# @app.cli.command('db_drop')
# def db_drop():
#     db.drop_all()
#     print('Database dropped')
#
#
# @app.cli.command('db_seed')
# def db_seed():
#
#     test_user = User(firstName='William',
#                      lastName='Herschel',
#                      email='test@test.com',
#                      password='P@ssw0rd')
#     db.session.add(test_user)
#     db.session.commit()
#     print('Database seeded')


####
# API
####

# the @ symbol is a known as a decorator
# In this case it is defining the route to our 'end-point' or url
# This app will not server load any templates it is an API that is there to provide JSONS.
@app.route('/')
def hello_world():
    return 'Hello World Garry Here!'

@app.route('/super_simple')
def super_simple():
    return 'Super Simple!'

# @app.route('/parameters')
# def parameters():
#     name = request.args.get('name')
#     age = int(request.args.get('age'))
#     if age < 18:
#         return jsonify(message="Sorry " + name + " you are not old enough"), 401
#     else:
#         return jsonify(message="Welcome " + name + " you are old enough")


# using string instead of typical python str due to this being a Flask operation
# Here we use variable rule matching instead of request/getting

@app.route('/url_variables/<string:name>/<int:age>')
def url_variables(name: str, age: int):
    if age < 18:
        return jsonify(message="Sorry " + name + " you are not old enough"), 401
    else:
        return jsonify(message="Welcome " + name + " you are old enough")


# @app.route('/ratings', method=['get','post'] )
# def ratings():
#     if request.method == 'Post':
#         name = request.form['name']
#         score = request.form['score']
#
#         rating = Rating(name=name, score = score)
#
#         db.session.add(rating)
#         db.session.commit
#     elif request.method == 'Get':
#         ratingList=Rating.query.all()
#         # Serializing is the process of converting an object into text
#         result = ratingsSchema.dump(ratingList)
#         return jsonify(result)




#######
# Models
#######

# Time to make models using ORM(Object-relational mapping)
# class User(db.Model):
#     __tablename__ = "users"
#     user_id = Column(Integer, primary_key=True)
#     name = Column(String)
#     email = Column(String, unique=True)



# class Rating(db.Model):
#     __tablename__ = "ratings"
#     score_id = Column(Integer, primary_key=True)
#     ratingName = Column(String)
#     ratingScore = Column(Float)

#This is used for JSON serialization.
# class UserSchema(ma.Schema):
#     class Meta:
#         fields = ('user_id', 'name', 'email')



# class RatingSchema(ma.Schema):
#     class Meta:
#         fields = ('score_id', 'ratingName', 'ratingScore')


# userSchema = UserSchema
# usersSchema = UserSchema(many=True)

# ratingSchema = RatingSchema
# ratingsSchema = RatingSchema(many=True)

# Entry point for running the script.
if __name__ == '__main__':
    app.run()

# The terminal here features the default shell for your system. On windows this is powershell.
# Activated debug mode to use automatic server reloading on-change.
