import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgresql://{}/{}".format('postgres:Henry!3%@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        print(f"Done testing function {self._testMethodName}")

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_categories_path(self):
        """ Test the information received by /category path """
        result = self.client().get('/categories')

        self.assertEqual(result.status_code, 200)

    def test_questions_path(self):
        """ Test the information received by /questions path"""
        result = self.client().get('/questions')

        self.assertEqual(result.status_code, 200)
    
    def test_unavailable_category(self):
        """ Test what happen when the client asks for unavailable category"""
        result = self.client().get('/categories/100/questions')

        self.assertEqual(result.status_code, 404)
    
    def test_unavailable_questions_page(self):
        """ Test the information received when passing page arquement to /questions path with unavaiable page number """
        result = self.client().get('/questions?page=10')

        self.assertEqual(result.status_code, 404)


    def test_adding_new_question(self):
        """ Test that POSTs data to the server to add new question to the database """
        result = self.client().post('/questions',json=dict(question='how are you', answer='fine', category='Art', difficulty='1'))
        self.assertEqual(result.status_code, 200)
    
    def test_failed_attempt_adding_new_question(self):
        """ Test that POSTs wrong data keys to the server, it should receives 500 as status code """
        result = self.client().post('/questions',json=dict(questions='how are you', answers='fine', categories='Art', difficulty='1'))
        self.assertEqual(result.status_code, 500)


    def test_delete_quesion(self):
        """ Test DELETE requst """
        questions = Question.query.all()
        import random
        question_id = random.choice(questions)
        question_id = question_id.format()['id']

        result = self.client().delete(f'/questions/{question_id}')
        self.assertEqual(result.status_code, 200)

    def test_failed_delete_quesion(self):
        """ Test failed DELETE requst """
        result = self.client().delete('/questions/200')
        self.assertEqual(result.status_code, 404)
    

    def test_searching(self):
        """ Test searching for questions when given a phrase"""
        result = self.client().post('/search_questions',json=dict(searchTerm='movie'))
        self.assertEqual(result.status_code, 200)

    def test_failed_searching(self):
        """ Test what happens when user submits wrong key name to the server when searching for a phrase """
        result = self.client().post('/search_questions',json=dict(searching='movie'))
        self.assertEqual(result.status_code, 422)


    def test_method_not_allowed(self):
        """ Test the result user recieves when attempting to request for method that is not allowed in the path  """
        result = self.client().delete('/categories/100/questions')

        self.assertEqual(result.status_code, 405)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()