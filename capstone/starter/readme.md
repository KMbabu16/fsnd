# The Great casting Agency of Udacity

This project is a casting agency , which is responsible for creating movies and managing and assigning actors for the movies. You are acting as managing director and designing the application.n As part of Nano degree it serves as a final project where students will be designing models, developing API's and designing security. By completing this project, students learn and apply their skills structuring and implementing well formatted API endpoints that leverage knowledge of HTTP and API development best practices.
 
## Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip and node installed on their local machines.

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file. 

To run the application run the following commands: 
```
set FLASK_APP=app
set FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `app.py file. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 


### Tests
In order to run tests navigate to the backend folder and run the following commands: 

```
python test_app.py
```
All tests are kept in that file and should be maintained as updates are made to app functionality. 

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application require authentication. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 

### Endpoints 
#### GET /Actors
- General:
    - Returns a list of actors objects, and total number of Actors 
- Sample: `curl http://127.0.0.1:5000/actors`

``` {
    "actors": [
        {
            "id": 1,
            "name": "Leonardo DiCaprio",
            "age"=48, 
            "gender"="Male"
        },
        {
            "id": 2,
            "name": "Scarlett Johansson",
            "age"=39, 
            "gender"="Female"
        }
    ],
    "total_actors": 2
}
```

#### GET /movies
- General:
    - Gets all movies from the DB , it shows id ,name and total number of movies 
- 'curl http://127.0.0.1:5000/movies -X GET -H "Content-Type: application/json"'
```
{
  "movies": [
        {"id": 1, "title": "Inception","release_date":"2010-07-16","actor_id"=1, "genres"="Sci-Fi"
        },
        {"id": 2, "title": "Lucy","release_date":"2014-07-25"","actor_id"=2, "genres"="Action"
        }
    ], "total_movies": 2
}
```
#### DELETE /actors/{actor_id}
- General:
    - Deletes the actor of the given ID if it exists. Returns the status of deletion, success value"
- 'curl -X DELETE http://127.0.0.1:5000/actors/1'
```
{
  'success': True
  }
```
#### DELETE /movies/{movie_id}
- General:
    - Deletes the movie of the given ID if it exists. Returns the status of deletion, success value"
- 'curl -X DELETE http://127.0.0.1:5000/movies/1'
```
{
  'success': True
  }
```
#### PATCH /actors/{actor_id}
- General:
    - If provided, updates the age,name and gender of the specified actor. Returns the success value. 
- `curl http://127.0.0.1:5000/actors/1 -X PATCH -H "Content-Type: application/json" -d '{"name": "Mohan", "age": 30, "gender": "Male"}'`
```
{
  "success": true
}
```
#### PATCH /movies/{movie_id}
- General:
    - If provided, updates the age,name and gender of the specified actor. Returns the success value. 
- `curl http://127.0.0.1:5000/movies/1 -X PATCH -H "Content-Type: application/json" -d '{"name": "Mohan", "age": 30, "gender": "Male"}'`
```
{
  "success": true
}
```

#### POST /actors
- General:
    - If provided, updates the age,name and gender of the specified actor. Returns the success value. 
- `curl http://127.0.0.1:5000/actors -X POST -H "Content-Type: application/json" -d '{"name": "Mohan", "age": 30, "gender": "Male"}'`
```
{
  "success": true
}
```
#### POST /movies
- General:
    - If provided, updates the age,name and gender of the specified actor. Returns the success value. 
- `curl http://127.0.0.1:5000/movies -X POST -H "Content-Type: application/json" -d '{"name": "Mohan", "age": 30, "gender": "Male"}'`
```
{
  "success": true
}
```


## Deployment N/A

## Authors
Yours truly, Mohan Babu K

## Acknowledgements 
The awesome team at Udacity and all of the students, soon to be full stack extraordinaires! 

