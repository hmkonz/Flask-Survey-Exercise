from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False

debug = DebugToolbarExtension(app)

RESPONSES_KEY = 'responses'

@app.route('/')
def show_survey_start():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    questions = satisfaction_survey.questions
    
    return render_template('survey_start.html', title = title, instructions = instructions, questions = questions)

@app.route('/start', methods = ["POST"]) 
def empty_responses():
    """Clear the session of responses and redirect to first question in survey"""
    session[RESPONSES_KEY] = []

    return redirect ('/questions/0')


@app.route('/questions/<int:index>')
def show_questions(index):
    """Display current question."""
    #'responses' is the list in memory (session.get(RESPONSES_KEY) that includes all the answers to the survey questions
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(responses) != index):
        # Trying to access questions out of order.
        flash(f"Tried to Access Invalid Question ID: #{index}! Returning to Previous Question.")
        return redirect((f'/questions/{len(responses)}'))

    elif len(responses) == len(satisfaction_survey.questions):
        # User answered all the questions! Thank them.
        return redirect('/thanks')

    return render_template('questions.html', index = index, questions= satisfaction_survey.questions)


@app.route('/answers', methods = ["POST"])
def handle_question():
    """Save response (choices) to RESPONSE_KEY list in session and redirect to next question."""

    #'choices' equals the answer selected from the radio button
    choices = request.form['choices']
    #set 'responses' equal to the list in session RESPONSES_KEY
    responses = session[RESPONSES_KEY]
  #add the answer to the questions 'choices' to the list 'responses'
    responses.append(choices)
    #set the contents of RESPONSES_KEY in session to the updated list 'responses' 
    session[RESPONSES_KEY] = responses
    #if the number of answers 'choices' appended to the list 'responses' does not equal the number of questions in the satisfaction_survey, redirect to the questions/{len(responses)} page. 
    #Once the length of responses is equal to the length of the list 'questions' in satisfaction_survey, redirect to the '/thanks' page"""
    if len(responses) != len(satisfaction_survey.questions):
        return redirect(f'/questions/{len(responses)}')  
    else:
        # User answered all the questions! Thank them.
        return redirect('/thanks')


@app.route('/thanks')
def thanks():
    """Survey is done. Show thank you page."""
    return render_template('thanks.html')
    



    

    
    

