from unittest import result
from urllib import response
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@127.0.0.1/project"
app.secret_key = "super-secret-key"
db = SQLAlchemy(app)

#Database
class Questions(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column('Question', db.String(500), nullable=True)
    option1 = db.Column('option1', db.String(100), nullable=True)
    option2 = db.Column('option2', db.String(100), nullable=True)
    option3 = db.Column('option3', db.String(100), nullable=True)
    option4 = db.Column('option4', db.String(100), nullable=True)
    is_delete = db.Column('is_delete', db.Boolean, default=0)

#setting Error Message
def errorMessage(errMsg):
    result = {"error": errMsg, "status": False}
    response = jsonify(result)
    response.status_code = 200
    return response

#api functions
class printHello(Resource):
    def get(self):
        return "Hello world"

#for adding questions
class addQuestion(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return errorMessage("Invalid Request")
        if "question" in data.keys():
            question = data['question']
        else:
            return errorMessage("Question is required")
        if "option1" in data.keys():
            option1 = data['option1']
        else:
            return errorMessage("Minimum 2 options required")
        if "option2" in data.keys():
            option2 = data['option2']
        else:
            return errorMessage("Minimum 2 options required")
        if "option3" in data.keys():
            option3 = data['option3']
        else:
            option3 = None
        if "option4" in data.keys():
            option4 = data['option4']
        else:
            option4 = None
        check = Questions.query.filter_by(question=question, is_delete=0).first()
        if not check:
            mcq = Questions(question=question, option1=option1, option2=option2, option3=option3, option4=option4)
            db.session.add(mcq)
            db.session.commit()
            mcq_id = Questions.query.filter_by(question=question).first().id
            result = {
                "id": mcq_id,
                "error": "",
                "status": True
            }
            response = jsonify(result)
            return response
        else:
            return errorMessage("This question already exists")

#showing all the questions
class allQuestions(Resource):
    def get(self):
        allquestions = Questions.query.filter_by(is_delete=0).all()
        list = []
        for question in allquestions:
            question_det = {}
            question_det["id"] = question.id
            question_det["question"] = question.question
            question_det["option1"] = question.option1
            question_det["option2"] = question.option2
            question_det["option3"] = question.option3
            question_det["option4"] = question.option4
            list.append(question_det)
        result = {
            "questions_lists": list
        }
        response = jsonify(result)
        return response

#updating a particular question
class updateQuestion(Resource):
    def post(self, index):
        get_ques = Questions.query.filter_by(id=index, is_delete=0).first()
        if not get_ques:
            return errorMessage("Question id not found")
        data = request.get_json()
        if not data:
            return errorMessage("Invalid Request")
        if "question" in data.keys():
            question = data['question']
        else:
            question = None
        if "option1" in data.keys():
            option1 = data['option1']
        else:
            option1 = None
        if "option2" in data.keys():
            option2 = data['option2']
        else:
            option2 = None
        if "option3" in data.keys():
            option3 = data['option3']
        else:
            option3 = None
        if "option4" in data.keys():
            option4 = data['option4']
        else:
            option4 = None
        if question is not None:
            get_ques.question = question
        if option1 is not None:
            get_ques.option1 = option1
        if option2 is not None:
            get_ques.option2 = option2
        if option3 is not None:
            get_ques.option3 = option3
        if option4 is not None:
            get_ques.option4 = option4
        
        db.session.add(get_ques)
        db.session.commit()
        result = {
            "error": "",
            "status": True
        }
        response = jsonify(result)
        return response

#deleting a question
class deleteQuestion(Resource):
    def get(self, index):
        index = int(index)
        get_ques = Questions.query.filter_by(id=index, is_delete=0).first()
        if get_ques:
            get_ques.is_delete = 1
            db.session.add(get_ques)
            db.session.commit()
            result = {
                "error": "",
                "status": True
            }
            response = jsonify(result)
            return response
        else:
            return errorMessage("Question doesn't exist")

#list of apis
api.add_resource(printHello, '/v1/api/hello')
api.add_resource(addQuestion, '/v1/api/addquestion')
api.add_resource(updateQuestion, '/v1/api/updatequestions/<index>')
api.add_resource(allQuestions, '/v1/api/allquestions')
api.add_resource(deleteQuestion, '/v1/api/deletequestion/<index>')

app.run(debug=True)