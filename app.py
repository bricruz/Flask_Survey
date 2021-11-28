from flask import Flask, request, render_template, jsonify, flash, session
from werkzeug.utils import redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)

responses = []
survey_length = len(satisfaction_survey.questions)

@app.route('/')
def home_page():
    surveyname = satisfaction_survey.title
    num = 0
    return render_template("home.html", surveyname = surveyname, num = num, survey_length=survey_length)
    
@app.route('/start', methods=['POST'])
def start_survey():
    session['responses'] = []
    return redirect('/questions/0')

@app.route('/questions/<int:q_num>')
def question_one(q_num):
    responses = session['responses']
    if len(responses) >= 4:
        flash('You have completed the survey', "success")
        return redirect('/thankyou')

    if q_num > len(responses):
        flash('Invalid URL request', "error")
        q_num = len(responses)
        return redirect('/questions/' + str(q_num))

    

    num = q_num + 1
    if num <= survey_length:
        question = satisfaction_survey.questions[q_num].question
        choice1 = satisfaction_survey.questions[q_num].choices[0]
        choice2 = satisfaction_survey.questions[q_num].choices[1]
    else:
        return redirect('/thankyou')
    
    return render_template("questions.html", question = question, num=num, choice1 = choice1, choice2 = choice2, survey_length=survey_length)

@app.route('/answers', methods=['POST'])
def post_answers():
    ans = request.form['question']
    responses = session['responses']
    print(len(responses))
    
    responses.append(ans)
    session['responses'] = responses
    print(responses)
    num = len(responses)

    return redirect('/questions/' + str(num))



@app.route('/thankyou')
def thankyou():
    
    return render_template("thanks.html")

