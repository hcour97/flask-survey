from flask import Flask, request, render_template,  redirect, flash,  jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# store user answers:
# should look like this at end of survey: 
# ['Yes', 'No', 'Less than $10,000', 'Yes']
RESPONSES_KEY = "responses"

@app.route('/')
def homepage():
    """Start a survey"""
    return render_template('start.html', survey=survey)

@app.route('/begin', methods=["POST"])
def begin_survey():
    """Clear session of responses"""

    # clears the response list:
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")

@app.route('/answer', methods=["POST"])
def handle_question():
    """Append response to list and send user to next question"""

    # get the user's response from the form:
    choice = request.form['answer']

    # add it to the responses list:
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    # redirect to next question or to the complete page:
    if (len(responses) == len(survey.questions)):
        return redirect('/complete')
    
    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/questions/<int:question_id>")
def show_question(question_id):
    """Display the current question"""
    responses = session.get(RESPONSES_KEY)

    # attempting to access question page early:
    if (responses is None):
        return redirect('/')

    # all questions have been answered: 
    if (len(responses) == len(survey.questions)):
        return redirect('/complete')
    
    # asking questions out of order:
    if len(responses) != question_id:
        flash(f"Invalid Question id: {question_id}.")
        return redirect(f"/questions/{len(responses)}")
    
    question =survey.questions[question_id]
    return render_template("question.html", question_num=question_id, question=question)

@app.route("/complete")
def complete():
    """User finished survey, display complete page."""

    return render_template('complete.html')