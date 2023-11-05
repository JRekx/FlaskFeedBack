from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized
from forms import RegisterF, LoginF, FeedbackF, DeleteF
from models import connect_db, db, Users, Feedback

app = Flask(__name__)

app.config['SECRET_KEY'] = 'turtlejrekx'

# Flask app configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask-feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Debug toolbar setup
toolbar = DebugToolbarExtension(app)

# Database setup
connect_db(app)

# Homepage route, redirects to the registration page
@app.route('/')
def homepage():
    return redirect('/register')

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Redirects to user's page if already logged in
    if 'username' in session:
        return redirect(f"/users/{session['username']}")
    
    form = RegisterF()

    if form.validate_on_submit():
        # Retrieves user data from the form and creates a new user
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        user = Users.register(username, password, first_name, last_name, email)

        # Commits changes to the database and sets session data
        db.session.commit()
        session['username'] = user.username

        # Redirects to user's page after registration
        return redirect(f"/users/{user.username}")
    
    # Renders registration form template
    return render_template("users/register.html", form=form)

# User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Redirects to user's page if already logged in
    if "username" in session:
        return redirect(f"/users/{session['username']}")
    
    form = LoginF()

    if form.validate_on_submit():
        # Retrieves login data from the form and authenticates the user
        username = form.username.data
        password = form.password.data

        user = Users.authenticate(username, password)

        # Sets session data after successful authentication
        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            # Displays error message if authentication fails
            form.username.errors = ["Invalid Username/Password"]
            return render_template("users/login.html", form=form)
    
    # Renders login form template
    return render_template("users/login.html", form=form)

# User logout route
@app.route("/logout")
def logout():
    # Removes user session data and redirects to login page
    session.pop("username")
    return redirect("/login")

# User profile page route
@app.route("/users/<username>")
def show_user(username):
    # Checks user session and authorization before displaying user profile
    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = Users.query.get(username)
    form = DeleteF()

    # Renders user profile template with user data and delete form
    return render_template("users/show.html", user=user, form=form)

# User deletion route
@app.route("/users/<username>/delete", methods=["POST"])
def remove_user(username):
    # Checks user session and authorization before deleting the user
    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = Users.query.get(username)
    db.session.delete(user)
    db.session.commit()

    # Removes user session data and redirects to login page after deletion
    session.pop("username")
    return redirect("/login")

# New feedback submission route
@app.route("/users/<username>/feedback/new", methods=["GET" , "POST"])
def new_feedback(username):
    # Checks user session and authorization before allowing feedback submission
    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = FeedbackF()

    if form.validate_on_submit():
        # Retrieves feedback data from the form and adds it to the database
        title = form.title.data
        content = form.content.data
        feedback = Feedback(
            title=title,
            content=content,
            username=username,
        )

        db.session.add(feedback)
        db.session.commit()

        # Redirects to user's page after feedback submission
        return redirect(f"/users/{feedback.username}")
    else:
        # Renders feedback submission form template
        return render_template('feedback/new.html', form=form)

# Feedback update route
@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)

    # Checks user session and authorization before allowing feedback update
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = FeedbackF(obj=feedback)

    if form.validate_on_submit():
        # Updates feedback data in the database and redirects to user's page
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        return redirect(f'/users/{feedback.username}')

    # Renders feedback update form template
    return render_template("feedback/edit.html", form=form, feedback=feedback)

# Feedback deletion route
@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)

    # Checks user session and authorization before allowing feedback deletion
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = DeleteF()

    if form.validate_on_submit():
        # Deletes feedback from the database and redirects to user's page
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f"/users/{feedback.username}")

if __name__ == '__main__':
    # Runs the Flask app in debug mode
    app.run(debug=True)







