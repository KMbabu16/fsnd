from flask_sqlalchemy import SQLAlchemy
from settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST
from datetime import datetime

# Construct the database URI
database_path = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    """
    setup_db(app)
    Binds a Flask application and a SQLAlchemy service.
    """
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

def db_drop_and_create_all():
    """
    Drop all tables and recreate them.
    WARNING: This will delete all data.
    """
    with db.engine.connect() as connection:
        transaction = connection.begin()
        try:
            db.drop_all()  # Drop all tables
            db.create_all()  # Recreate tables
            insert_sample_data()  # Insert sample data
            transaction.commit()
        except Exception as e:
            transaction.rollback()
            print(f"Error resetting database: {e}")

def delete_all_tables():
    """
    Deletes all tables from the PostgreSQL database.
    """
    with db.engine.connect() as connection:
        transaction = connection.begin()
        try:
            connection.execute("DROP SCHEMA public CASCADE;")
            connection.execute("CREATE SCHEMA public;")
            transaction.commit()
            print("✅ All tables deleted successfully.")
        except Exception as e:
            transaction.rollback()
            print(f"Error deleting tables: {e}")

#----------------------------------------------------------------------------#
# Models
#----------------------------------------------------------------------------#

class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.Date, nullable=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'), nullable=True)
    genres = db.Column(db.String(120))

    # Define relationship to Actor
    actor = db.relationship('Actor', back_populates='movies')


class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(10), nullable=True)

    # Define relationship to Movie
    movies = db.relationship('Movie', back_populates='actor')

#----------------------------------------------------------------------------#
# Sample Data
#----------------------------------------------------------------------------#

def insert_sample_data():
    """
    Insert sample actors and movies into the database.
    """
    with db.session.begin():  # Ensures transaction safety
        # Clear existing data
        db.session.query(Movie).delete()
        db.session.query(Actor).delete()

        # Create actors
        actor1 = Actor(name="Leonardo DiCaprio", age=48, gender="Male")
        actor2 = Actor(name="Scarlett Johansson", age=39, gender="Female")

        db.session.add_all([actor1, actor2])
        db.session.flush()  # Get IDs before inserting movies

        # Create movies
        movie1 = Movie(title="Inception", release_date=datetime.strptime("2010-07-16", "%Y-%m-%d").date(), actor_id=actor1.id, genres="Sci-Fi")
        movie2 = Movie(title="Lucy", release_date=datetime.strptime("2014-07-25", "%Y-%m-%d").date(), actor_id=actor2.id, genres="Action")

        db.session.add_all([movie1, movie2])
        db.session.commit()

    print("✅ Sample data inserted successfully.")

# Usage:
# from your_module_name import setup_db, delete_all_tables, insert_sample_data
#setup_db(app)
# delete_all_tables()
#insert_sample_data()