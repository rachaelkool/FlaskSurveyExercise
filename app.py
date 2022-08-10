from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

response_key = 'responses'

@app.route('/')
def begin_survey():
    return render_template('begin_survey.html', survey=survey)


@app.route('/begin', methods=["GET", "POST"])
def start():
    if request.method == 'POST':
        session[response_key] = [] 
        return redirect('/questions/0')
    else: 
        return


@app.route("/questions/<int:qid>", methods=["GET"])
def show_question(qid):
    responses = session.get(response_key)
    if (responses is None):
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")

    if (len(responses) != qid):
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")
            
    question = survey.questions[qid]
    return render_template("question.html", question_num=qid, question=question)


@app.route("/answer", methods=["POST"])
def handle_question():
    
    answer = request.form.get('answer')

    if not answer: 
        flash(f"No answer selected.")
        return redirect(f"/questions/{len(response_key)}")
    
    else: 
        choice = request.form['answer']
    
        responses = session.get(response_key)
        responses.append(choice)
        session[response_key]= responses

        if (len(responses) == len(survey.questions)):
            return redirect("/complete")
        else:
            return redirect(f"/questions/{len(responses)}")
    

# @app.route("/answer", methods=["POST", "GET"])
# def handle_question():

    # if request.method == 'POST':
        # if (request.form['answer'] is None): 
        #     return redirect("/")

#         choice = request.form['answer']
        
#         responses.append(choice)

#         if (len(responses) == len(survey.questions)):
#             return redirect("/complete")
#         else:
#             return redirect(f"/questions/{len(responses)}")
#     else: 
#         return 
  


@app.route("/complete")
def complete():

    return render_template("complete.html")

    