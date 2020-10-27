from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["SECRET_KEY"] = "secret_key"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.route('/')
def go_to_register():
    """Redirect to register page."""

    return redirect('/register')
    
    
@app.route('/register', methods=['GET', 'POST'])
def register_form():
    """Show register form on GET, handle form submit on POST."""

    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)

        db.session.add(user)
        db.session.commit()

        session['username'] = user.username

        flash('User registered', 'success')
        return redirect(f'/users/{user.username}')

    return render_template('register.html', form=form)
    
    
@app.route('/login', methods=['GET', 'POST'])
def login_form():
    """Show login form on GET, handle form submit on POST."""

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)

        if user:
            session['username'] = user.username
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(f'/users/{user.username}')
        else:
            flash('Invalid username/password', 'error')
            return redirect('/login')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Logout user."""

    session.pop('username')

    flash('Logged out', 'success')
    return redirect('/')


@app.route('/users/<username>')
def show_user_details(username):

    if username != session['username']:
        flash('Please log in first!', 'error')
        return redirect('/login')

    user = User.query.get_or_404(username)

    return render_template('user_details.html', user=user)


@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """Remove user and associated feedback from database and redirect to home."""

    if username != session['username']:
        flash('Please log in first!', 'error')
        return redirect('/login')

    user = User.query.get_or_404(username)

    db.session.delete(user)
    db.session.commit()
    session.pop('username')

    flash('User deleted', 'success')
    return redirect('/')


@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def handle_feedback(username):
    """Show form to add feedback on GET, handle form submit on POST"""

    if username != session['username']:
        flash('Please log in first!', 'error')
        return redirect('/login')

    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title=title, content=content, username=username)

        db.session.add(feedback)
        db.session.commit()

        flash('Feedback added!', 'success')
        return redirect(f'/users/{username}')

    return render_template('add_feedback.html', form=form)


@app.route('/feedback/<feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    """Show form to update feedback on GET, handle form submit on POST."""
    
    feedback = Feedback.query.get_or_404(feedback_id)
    form = FeedbackForm(obj=feedback)

    if feedback.username != session['username']:
        flash('Please log in first!', 'error')
        return redirect('/login')

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        flash('Feedback updated!', 'success')
        return redirect(f'/users/{feedback.username}')

    return render_template('edit_feedback.html', form=form)


@app.route('/feedback/<feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    """Delete feedback and redirect to user details."""

    feedback = Feedback.query.get_or_404(feedback_id)

    if feedback.username != session['username']:
        flash('Please log in first!', 'error')
        return redirect('/login')

    db.session.delete(feedback)
    db.session.commit()

    return redirect(f'/users/{feedback.username}')


