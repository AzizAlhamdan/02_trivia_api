import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods','POST, GET, DELETE, PUT, OPTIONS')
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def categories():
    categories = Category.query.all()
    return jsonify(categories = [c.format() for c in categories])

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions', methods=['GET'])
  def questions():
    category = Category.query.all()
    for i in range(len(category)):
      category[i] = category[i].format()
    
    page = request.args.get('page',1,type=int)

    questions = Question.query.order_by(Question.category).paginate(page,QUESTIONS_PER_PAGE) # questions is now an object of type Pagination of SQLALCHEMY. https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.Pagination
    if request.args.get('category',type=int):
      questions = Question.query.filter(Question.category == request.args.get('category',type=int)).order_by(Question.category).paginate(page,QUESTIONS_PER_PAGE)

    formated_list = dict(questions=[q.format() for q in questions.items], 
                          pages = [i+1 for i in range(questions.pages)], 
                          total_questions=questions.total,
                          current_category = ['All'],
                          categories = category)

    return jsonify(formated_list)

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
    question = Question.query.get(id)
    if not question:
      abort(404)
    
    question.delete()
    return jsonify(dict(success=True,status=200))

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route('/questions', methods=['POST'])
  def add_new_question():
    data = request.get_json()
    if not data:
      data = request.get_data().decode()
  
    try:
      category = Category.query.with_entities(Category.id).filter(Category.type == data['category']).first()
      new_questions = Question(question=data['question'], answer=data['answer'], category=category[0], difficulty=data['difficulty'])
      new_questions.insert()
    except Exception as e:
      print(e)
      abort(500)
    return jsonify(dict(success=True,status=200))

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/search_questions', methods=['POST'])
  def search():
    term = request.get_json()
    if 'searchTerm' not in term.keys():
      abort(422)

    questions = Question.query.order_by(Question.category).filter(Question.question.ilike(f"%{term['searchTerm']}%")).all()
    
    return jsonify(dict(questions = [q.format() for q in questions],
                    total_questions = len(questions)))

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def category_based_quesions(id):
    page = request.args.get('page',1,type=int)
    if id > 0:
      questions = Question.query.filter(Question.category == id).order_by(Question.id).paginate(page,QUESTIONS_PER_PAGE)
      current_cateqory = Category.query.get(id)

      if not questions or not current_cateqory: # if Either no questions were found or no category with the given ID
        abort(404)

      return jsonify(questions=[q.format() for q in questions.items],
                      total_questions = questions.total,
                      current_category=current_cateqory.format()['type'])
    else:
      questions = Question.query.order_by(Question.category).paginate(page,QUESTIONS_PER_PAGE)
      return jsonify(questions=[q.format() for q in questions.items],
                      total_questions = questions.total,
                      current_category=['All'])
  

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    import random
    question = None
    data = request.get_json()
    previous = data['previous_questions']
    id = data['quiz_category']['id']
    quiz_type = data['quiz_category']['type']

    if quiz_type == 'click': # which refers to as "ALL" in client side
      questions_ids = Question.query.all() # get all questions
      questions_ids = [q.format()['id'] for q in questions_ids] # extract the IDs only
      next_question = [q for q in questions_ids if q not in previous] # create a list of Ids that are not in prevous list

      if not next_question: # if the list is empty then it must means all questions are answerd.
        return jsonify(dict(question=None,previousQuestions=previous))

      print('\t',next_question, ' --> ', previous)
      next_question = random.choice(next_question) # randomly pick a number form that list
      question = Question.query.get(next_question).format() # fetch that number from the database


    else: # any other category type selected
      # this does same as the if statment except now it fliters quesions IDs by selected category 
      questions_ids = Question.query.filter(Question.category == id).all()
      questions_ids = [q.format()['id'] for q in questions_ids]
      next_question = [q for q in questions_ids if q not in previous]

      if not next_question:
        return jsonify(dict(question=None,previousQuestions=previous))
      
      print('\t',next_question, ' --> ', previous)
      next_question = random.choice(next_question)
      question = Question.query.get(next_question).format()
    

    return jsonify(dict(question=question,previousQuestions=previous))

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify(dict(success=False,status=400,msg='Server can not accepts Bad Request!!')), 400
  
  @app.errorhandler(404)
  def not_found(error):
    return jsonify(dict(success=False,status=404,msg='Request is Not Found')), 404
  
  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify(dict(success=False,status=405,msg='Requested method is not allowed')), 405
  
  @app.errorhandler(422)
  def method_not_allowed(error):
    return jsonify(dict(success=False,status=422,msg='Server was unable to process an unprocessable entity')), 422

  @app.errorhandler(500)
  def Internal_error(error):
    return jsonify(dict(success=False,status=500,msg='Server encounterd an error while processing the request')), 500

  return app

    