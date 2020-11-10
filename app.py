from flask import Flask, jsonify, request, render_template
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
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#Initialize the database
db = SQLAlchemy(app)
ma = Marshmallow(app)



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
def ratings():
    ratingsList=Rating.query.all()
    result = ratingsSchema.dump(ratingsList)
    return jsonify(result)

@app.route('/newRating', methods=['GET', 'POST'])
def newRating():
    if request.method == 'POST':
        ratingName=request.form['ratingName']
        ratingScore=float(request.form['ratingScore'])


        rating = Rating(ratingname=ratingName,ratingscore=ratingScore)

        db.session.add(rating)
        db.session.commit()
        return ratingName +' '+ ratingScore

    return render_template('newRating.html')


# using string instead of typical python str due to this being a Flask operation
# Here we use variable rule matching instead of request/getting

# @app.route('/url_variables/<string:name>/<int:age>')
# def url_variables(name: str, age: int):
#     if age < 18:
#         return jsonify(message="Sorry " + name + " you are not old enough"), 401
#     else:
#         return jsonify(message="Welcome " + name + " you are old enough")


@app.route('/users')
def users():
    userList=User.query.all()
    result = usersSchema.dump(userList)
    return jsonify(result)

@app.route('/ratings/<string:ratingname>')
def ratingAvgScore(ratingname: str):
    rating=Rating.query.filter_by(ratingname = ratingname).all()
    if rating:
        result = ratingsSchema.dump(rating)
        return jsonify(result)
    else:
        return jsonify(message ="Sorry, no such rating found."), 404






#######
# Models
#######

# Time to make models using ORM(Object-relational mapping)
class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)



class Rating(db.Model):
    __tablename__ = "ratings"
    score_id = Column(Integer, primary_key=True)
    ratingname = Column(String)
    ratingscore = Column(Float)

#This is used for JSON serialization.
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email')



class RatingSchema(ma.Schema):
    class Meta:
        fields = ('score_id', 'ratingname', 'ratingscore')


userSchema = UserSchema
usersSchema = UserSchema(many=True)

ratingSchema = RatingSchema
ratingsSchema = RatingSchema(many=True)

# Entry point for running the script.
if __name__ == '__main__':
    app.run()

# The terminal here features the default shell for your system. On windows this is powershell.
# Activated debug mode to use automatic server reloading on-change.
