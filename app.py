from flask import Flask, jsonify, request
# Here to handle my database.
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Float
# Here to handle object serialization.
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

# database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'personal.db')

db = SQLAlchemy(app)
ma = Marshmallow(app)


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped')


@app.cli.command('db_seed')
def db_seed():
    mercury = Planet(planetName='Mercury',
                     planetType='Class D',
                     homeStar='Sol',
                     mass=3.258e23)
    earth = Planet(planetName='Earth',
                   planetType='Class M',
                   homeStar='Sol',
                   mass=5.972e24)
    db.session.add(mercury)
    db.session.add(earth)

    test_user = User(firstName='William',
                     lastName='Herschel',
                     email='test@test.com',
                     password='P@ssw0rd')
    db.session.add(test_user)
    db.session.commit()
    print('Database seeded')


####
# API
####

# the @ symbol is a known as a decorator
# In this case it is defining the route to our 'end-point' or url
# This app will not server load any templates it is an API that is there to provide JSONS.
@app.route('/')
def hello_world():
    return 'Hello World Garry Here!'


@app.route('/parameters')
def parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    if age < 18:
        return jsonify(message="Sorry " + name + " you are not old enough"), 401
    else:
        return jsonify(message="Welcome " + name + " you are old enough")


# using string instead of typical python str due to this being a Flask operation
# Here we use variable rule matching instead of request/getting
@app.route('/url_variables/<string:name>/<int:age>')
def url_variables(name: str, age: int):
    if age < 18:
        return jsonify(message="Sorry " + name + " you are not old enough"), 401
    else:
        return jsonify(message="Welcome " + name + " you are old enough")


@app.route('/planets')
def planets():
    planets_list = Planet.query.all()
    result = planetsSchema.dump(planets_list)
    return jsonify(result)
    # Serializing is the process of converting an object into text


######
# Models
#######

# Time to make models using ORM(Object-relational mapping)
class User(db.Model):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    firstName = Column(String)
    lastName = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


class Planet(db.Model):
    __tablename__ = "planets"
    planet_id = Column(Integer, primary_key=True)
    planetName = Column(String)
    planetType = Column(String)
    homeStar = Column(String)
    mass = Column(Float)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'firstName', 'lastName', 'email', 'password')


#This is used for JSON serialization.
class PlanetSchema(ma.Schema):
    class Meta:
        fields = ('planet_id', 'planetName', 'planetType', 'homeStar', 'mass')


userSchema = UserSchema
usersSchema = UserSchema(many=True)

planetSchema = PlanetSchema
planetsSchema = PlanetSchema(many=True)

# Entry point for running the script.
if __name__ == '__main__':
    app.run(debug=True)

# The terminal here features the default shell for your system. On windows this is powershell.
# Activated debug mode to use automatic server reloading on-change.
