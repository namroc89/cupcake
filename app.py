from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcake_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'plasticbeach1235'
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)

connect_db(app)


def serialize_cupcake(cupcake):
    """ creates a serialized version of cupcake"""

    return {
        "id": cupcake.id,
        'flavor': cupcake.flavor,
        'size': cupcake.size,
        'rating': cupcake.rating,
        "image": cupcake.image
    }


@app.route("/api/cupcakes")
def get_cupcakes():
    """return JSON {cupcakes: [{id, flavor, size, rating, image}, ...]}, for all cupcakes"""

    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcake(c) for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.route("/api/cupcakes/<int:id>")
def get_a_cupcake(id):
    """return JSON {cupcake: {id, flavor, size, rating, image}}, for a specific cupcake"""

    cupcake = Cupcake.query.get_or_404(id)
    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized)


@app.route("/api/cupcakes", methods=['POST'])
def create_cupcake():
    """ Creates a cupcake and return it.
    return JSON {cupcake: {id, flavor, size, rating, image}}"""
    data = request.json

    new_cupcake = Cupcake(flavor=data['flavor'],
                          size=data['size'],
                          rating=data['rating'],
                          image=data['image'] or None)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize_cupcake(new_cupcake)

    return (jsonify(cupcake=serialized), 201)


@app.route("/api/cupcakes/<int:id>", methods=['PATCH'])
def edit_cupcake(id):
    """edit cupcake. Return JSON"""
    cupcake = Cupcake.query.get_or_404(id)
    data = request.json
    cupcake.flavor = data.get('flavor', cupcake.flavor)
    cupcake.size = data.get('size', cupcake.size)
    cupcake.rating = data.get('rating', cupcake.rating)
    cupcake.image = data.get('image', cupcake.image)

    db.session.commit()
    return jsonify(cupcake=serialize_cupcake(cupcake))


@app.route("/api/cupcakes/<int:id>", methods=['DELETE'])
def delete_cupcake(id):
    """Delete Cupcake. Respond with Delete message"""

    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")


@app.route("/")
def home_page():

    return render_template("home.html")
