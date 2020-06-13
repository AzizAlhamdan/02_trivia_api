# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET '/questions'
GET '/categories/<int:id>/questions'
POST '/questions'
POST '/search_questions'
POST '/quizzes'
DELETE '/questions/<int:id>'


GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: A list with a  {id:,type:} contains all available categories in the database with their corresponding id number
[
    {'id':'1', 'type':"Science"},
    {'id':'2', 'type':"Art"},
    {'id':'3' , 'type':"Geography"},
    {'id':'4' , 'type':"History"},
    {'id':'5' , 'type':"Entertainment"},
    {'id':'6' , 'type':"Sports"}
]

>>>>>>>>>>>>>>> TODO: completing API documentation <<<<<<<<<<<<<<<

GET '/questions'
- Fetches a jsonified dictionry that contains list of questions, categories and page information, all submitted arquments are optional
- Request Arguments: page:<number>,category:<number>
- Returns: An object with a multiple (key,value) pairs contains one or more questions and other information, as the following example:
{'questions' : [
        {'id':1,
        'question': 'where Effel tower is located ?',
        'difficulty': 2,
        'category':4,
        'answer':'Paris'},
    ],
'pages' : [1],
'total_questions' : 1,
'current_category' : 4,
'categories' : [
        {'id':'1', 'type':"Science"},
        {'id':'2', 'type':"Art"},
        {'id':'3' , 'type':"Geography"},
        {'id':'4' , 'type':"History"},
        {'id':'5' , 'type':"Entertainment"},
        {'id':'6' , 'type':"Sports"}
    ]
}


DELETE '/questions/<int:id>'
- send a delete request to the server to delete a question
- Request Arguments: id:<number>
- Returns: 
    1. If the request was successfully processed, the following json data would be received:
        {
            success:true,
            status:200
        }

    2. If the server failed to delete the requested question:
        {
            success:false,
            status:404,
            msg:'Request is Not Found'
        },404


POST '/questions/'
- Receive a question information submitted by the client to add these information to the database
- Request Arguments: question:<string>, answer:<string>, category:<string>, difficulty:<number>
- Returns: 
    1. If the request was successfully processed, the following json data would be received:
        {
            success:true,
            status:200
        }

    2. If the server failed to add the received question:
        {
            success:false,
            status:500,
            msg:'Server encounterd an error while processing the request'
        },500


POST '/search_qeustions'
- Fetches a jsonified dictionry that contains list of questions that matchs the specified phrase
- Request Arguments: searchTerm:<string>
- Returns: a list contains one or more questions dictionry and number of total questions, 
Example: curl -X POST http://localhost:5000/search_questions --data {'searchTerm': 'tower'} -H 'Content-Type: application/json'
>> {'questions' : [
        {'id':1,
        'question': 'where Effel tower is located ?',
        'difficulty': 2,
        'category':4,
        'answer':'Paris'},
        ],
    'total_qeustions':1
}   

GET '/categories/<int:id>/questions'
- same as GET '/questions' endpoint except that category argument is mandetory otherwise an 404 error will be recieved
- Request Arguments: optional > page:<number>
- Returns: An object with a multiple (key,value) pairs contains one or more questions and other information, as the following example:
{'questions' : [
        {'id':1,
        'question': 'where Effel tower is located ?',
        'difficulty': 2,
        'category':4,
        'answer':'Paris'},
        {'id':5,
        'question': 'when was the great wall of china build ?',
        'difficulty': 4,
        'category':4,
        'answer':'700 BC'},
    ],
'total_questions' : 2,
'current_category' : 4,
}


POST '/quizzes'
- Endpoint gets called after the client picks a category, returns questions one by one untill all questions of that category are answered
- Request Arguments: previous_questions:array of <number>, quiz_category:{id:<number>,type:<string>}
- Returns: jsonfied dictionary with one question and an array of all IDs of answerd questions. 
Example:
{
    'question': 
        {'id':5,
        'question': 'when was the great wall of china build ?',
        'difficulty': 4,
        'category':4,
        'answer':'700 BC'}
    'previousQuestions':[3,7,1]
}
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```