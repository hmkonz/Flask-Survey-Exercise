from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def show_survey_page():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    questions = satisfaction_survey.questions
    
    return render_template('survey.html', title = title, instructions = instructions, questions = questions)


@app.route('/questions/<int:index>')
def show_questions(index):

    if index > len(satisfaction_survey.questions):
        
        return redirect(f'/questions/{0}')

    if len(responses) != index:

        flash("Tried to Access Invalid Question! Returning to Previous Question.")

        return redirect((f'/questions/{len(responses)}'))

    elif len(responses) == len(satisfaction_survey.questions):
        
        return redirect('/thanks')

    

    return render_template('questions.html', index = index, questions= satisfaction_survey.questions)


@app.route('/answers', methods = ["POST"])
def handle_answers():
    """'choices' equals the answer selected from the radio button"""
    choices = request.form['choices']
    """add the choices selected from the radio buttons to the list 'responses'"""
    responses.append(choices)
    print(responses)
    """ if the number of answers 'choices' appended to the list 'responses' does not equal the number of questions in the satisfaction_survey, redirect to the questions/{len(responses)} page. """
    """Once the length of responses is equal to the length of the list 'questions' in satisfaction_survey, redirect to the '/thanks' page"""
    if len(responses) != len(satisfaction_survey.questions):
        return redirect(f'/questions/{len(responses)}')  
    else:
        return redirect('/thanks')


@app.route('/thanks')
def thanks():
    return '<h1>Thank You!!</h1>'
    
    


    

    
    

