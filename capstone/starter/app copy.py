import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db,Actor,Movie

def create_app(test_config=None):
    # create and configure the app
    app = Flask(app)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)
    CORS(app)

    #Get implementation
    @app.route('/actors')
    def get_actors():
        Actors= Actor.query.order_by(Actor.id).all()
        return jsonify(
            {
                'Actors': {str(actor.id): actor.name for actor in Actors}
            }
        )
    
    @app.route('/movies')
    def get_movie():
        Movies=Movie.query.order_by(Movie.id).all()
        return jsonify(
            {
                'Movies': {str(movie.id): movie.name for movie in Movies}
            }
        )
    #Delete Implementation
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    def delete_actors():
        search_result=Actor.query.get(Actor.id == actor_id).first()
        if search_result is none:
            print(f"Actor with id {actor_id} not avaialble")
        else:
            abort(402)
        db.session.delete(search_result)
        db.session.commit()
        return jsonify({
                "success": True
            }),200
    
    @app.route('/movies/<int:movie_id>',methods=['DELETE'])
    def delete_movie():
        search_result=Movie.query.get(Movie.id == movie_id).first()
        if search_result is none:
            print(f"movie with id {movie_id} not avaialble")
        else:
            abort(402)
        db.session.delete(search_result)
        db.session.commit()
        return jsonify({
                "success": True
            }),200
    #Patch Implementation
    @app.route('/actors/<int:actor_id>',methods=['PATCH'])
    def patch_actors():
        search_actor=Actor.query.get(Actor.id==actor_id).first()
        body=request.get_json()
        name=body.get('name',None)
        age=body.get("age",None)
        gender=body.get("gender",None)
        if search_actor:
            actor=update(Actor).where(Actor.id==actor_id).values(age=age,name=name,gender=gender)
        else:
            abort(404)
        update_status=db.session.execute(actor)
        print(update_status)
        db.session.commit()
        return jsonify({
                "success": True
            }),200
    
    @app.route('/movies/<int:movie_id>',methods=['PATCH'])
    def patch_movie():
        search_actor=Movie.query.get(Movie.id==movie_id).first()
        body=request.get_json()
        id=body.get("id,None")
        name=body.get('name',None)
        age=body.get("age",None)
        gender=body.get("gender",None)
        if search_actor:
            movie_update=update(Movie).where(Movie.id==movie_id).values(age=age,name=name,gender=gender)
        else:
            abort(404)
        db.session.execute(movie_update)
        db.session.commit()
        return jsonify({
                "success": True
            }),200
    #POSt Implementation
    @app.route('/actors',methods=['POST'])
    def post_actors():
        body=request.get_json()
        name=body.get('name',None)
        age=body.get("age",None)
        gender=body.get("gender",None)
        search_actor=Actor.query.get(Actor.name==name && Actor.age=age && Actor.gender=gender ).first()
        if search_actor:
            print(f"Actor {name} already exist,no action taken") 
            abort(404)
        else:
            new_actor=(name=name,age=age,gender=gender)
            db.session.add(new_actor)
            db.session.commit()
        return jsonify({
                "success": True
            }),200
    
    @app.route('/movies',methods=['POST'])
    def post_movie():
        
        body=request.get_json()
        title=body.get('title',None)
        release_date=body.get("release_date",None)
        genres=body.get("genres",None)
        search_movie=Movie.query.get(Movie.title==title && Movie.release_date=release_date && Movie.genres=genres ).first()
        if search_actor:
            print(f"movie {title} already exist,no action taken") 
            abort(404)
        else:
            new_movie=(title=title,release_date=release_date,genres=genres)
            db.session.add(new_movie)
            db.session.commit()
        return jsonify({
                "success": True
            }),200
    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)