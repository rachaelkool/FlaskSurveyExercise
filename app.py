from flask import Flask, render_template, redirect, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def begin_survey():
    return render_template('begin_survey.html', survey=survey)

@app.route("/questions/<int:qid>", methods=["POST", "GET"])
def show_question(qid):
    if (responses is None):
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")

    if (len(responses) != qid):
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")
        
    if request.method == 'GET':    
        question = survey.questions[qid]
        return render_template("question.html", question_num=qid, question=question)
    else: 
        return

@app.route("/answer", methods=["POST", "GET"])
def handle_question():

    if request.method == 'POST':
        choice = request.form['answer']
        
        responses.append(choice)

        if (len(responses) == len(survey.questions)):
            return redirect("/complete")
        else:
            return redirect(f"/questions/{len(responses)}")
    else: 
        return 

@app.route("/complete")
def complete():

    return render_template("complete.html")

    