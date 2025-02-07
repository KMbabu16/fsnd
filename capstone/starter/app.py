import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from models import setup_db, db, db_drop_and_create_all, Actor, Movie
from auth.auth import AuthError, requires_auth

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path)

    CORS(app)
    
    # Uncomment this in development to drop and create all tables
    with app.app_context():
        db_drop_and_create_all()

    # GET implementation
    @app.route('/actors', methods=['GET'])
    def get_actors():
        actors = Actor.query.order_by(Actor.id).all()  
        actors_json = [{'id': actor.id, 'name': actor.name,'age':actor.age,'gender':actor.gender} for actor in actors]
        return jsonify({'actors': actors_json, 'total_actors': len(actors_json)})


    @app.route('/movies', methods=['GET'])
    @requires_auth(permission=["get:movies"])  
    def get_movies():
        movies = Movie.query.order_by(Movie.id).all()
        movies_json = [{'id': movie.id, 'title': movie.title,'release_date':movie.release_date,'genres':movie.genres} for movie in movies]
        return jsonify({'movies': movies_json, 'total_movies': len(movies_json)})
    # DELETE implementation
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth(permission=["delete:actors"]) 
    def delete_actor(actor_id):
        actor = db.session.get(Actor, actor_id)
        if not actor:
            abort(404, description=f"Actor with id {actor_id} not available")
        
        db.session.delete(actor)
        db.session.commit()
        return jsonify({"success": True}), 200

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth(permission=["delete:movies"]) 
    def delete_movie(movie_id):
        movie = db.session.get(Movie, movie_id)
        if not movie:
            abort(404, description=f"Movie with id {movie_id} not available")
        
        db.session.delete(movie)
        db.session.commit()
        return jsonify({"success": True}), 200

    # PATCH implementation
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth(permission=["patch:actors"]) 
    def patch_actor(actor_id):
        actor = db.session.get(Actor, actor_id)
        if not actor:
            abort(404, description="Actor not found")
        
        body = request.get_json()
        if not body:
            abort(400, description="No data provided")

        actor.name = body.get('name', actor.name)
        actor.age = body.get('age', actor.age)
        actor.gender = body.get('gender', actor.gender)
        
        db.session.commit()
        return jsonify({"success": True}), 200

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth(permission=["patch:movies"])  
    def patch_movie(movie_id):
        movie = db.session.get(Movie, movie_id)
        if not movie:
            abort(404, description="Movie not found")
        
        body = request.get_json()
        if not body:
            abort(400, description="No data provided")

        movie.title = body.get('title', movie.title)
        
        if 'release_date' in body:
            try:
                movie.release_date = datetime.strptime(body['release_date'], "%Y-%m-%d")
            except ValueError:
                abort(400, description="Invalid date format. Use YYYY-MM-DD")

        movie.genres = body.get('genres', movie.genres)

        db.session.commit()
        return jsonify({"success": True}), 200

    # POST implementation
    @app.route('/actors', methods=['POST'])
    @requires_auth(permission=["post:actors"]) 
    def post_actor():
        body = request.get_json()
        if not body:
            abort(400, description="No data provided")

        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')

        if not name:
            abort(400, description="Actor name is required")

        actor_exists = Actor.query.filter_by(name=name, age=age, gender=gender).first()
        if actor_exists:
            abort(400, description=f"Actor {name} already exists")

        new_actor = Actor(name=name, age=age, gender=gender)
        db.session.add(new_actor)
        db.session.commit()

        return jsonify({"success": True}), 201

    @app.route('/movies', methods=['POST'])
    @requires_auth(permission=["post:movies"]) 
    def post_movie():
        body = request.get_json()
        if not body:
            abort(400, description="No data provided")

        title = body.get('title')
        release_date = body.get('release_date')
        genres = body.get('genres')

        if not title:
            abort(400, description="Movie title is required")

        if release_date:
            try:
                release_date = datetime.strptime(release_date, "%Y-%m-%d")
            except ValueError:
                abort(400, description="Invalid date format. Use YYYY-MM-DD")

        movie_exists = Movie.query.filter_by(title=title, release_date=release_date, genres=genres).first()
        if movie_exists:
            abort(400, description=f"Movie {title} already exists")

        new_movie = Movie(title=title, release_date=release_date, genres=genres)
        db.session.add(new_movie)
        db.session.commit()

        return jsonify({"success": True}), 201

    # Error Handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "error": 404, "message": "resource not found"}), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({"success": False, "error": 422, "message": "unprocessable"}), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"success": False, "error": 405, "message": "method not allowed"}), 405

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
