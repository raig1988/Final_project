from flask import redirect, render_template, request, session, flash, url_for
from budgetapp import app, db, bcrypt, mail
from budgetapp.models import User, Transactions
from budgetapp.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm, TransactionForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


# ROUTES

@app.route("/register", methods=["GET", "POST"])
def register():
    # register user via form
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created successfully for {form.username.data}", category='success')
        return redirect(url_for('index'))
    return render_template("/register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.hash, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        else:
            flash("Login unsuccessful. Please check email and password",'danger')
    return render_template("/login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/")
@login_required
def index():
    return render_template("/index.html")

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("/account.html", form=form)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request", sender="noreply@aprendofinanzas.com", recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link:
{url_for('reset_token', token=token, _external = True)}
'''
    mail.send(msg)

@app.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password", "info")
        return redirect(url_for("login"))
    return render_template("reset_request.html", form=form)


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token.", "warning")
        return redirect(url_for("reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.hash = hashed_password
        db.session.commit()
        flash(f"Password has changed for {user.email}", category='success')
        return redirect(url_for('index'))
    return render_template("reset_token.html", form=form)

@app.route("/transaction", methods=["GET", "POST"])
@login_required
def transaction():
    id = current_user.id
    form = TransactionForm()
    if form.validate_on_submit():
        transaction = Transactions(user_id=id, day=form.day.data, month=form.month.data, year=form.year.data, type=form.type.data, expense=form.expense.data, amount=form.amount.data)
        db.session.add(transaction)
        db.session.commit()
        flash(f" Transaction registered correctly on {transaction.day}/{transaction.month}/{transaction.year} of {transaction.expense}", 'success')
        return redirect(url_for("transaction"))
    return render_template("transaction.html", form=form)

@app.route("/results", methods=["GET", "POST"])
@login_required
def results():
    if request.method == "POST":
        month = request.form.get("month")
        if not month:
            flash("You need to enter the month", "warning")
        year  = request.form.get("year")
        if not year:
            flash("You need to enter the year", "warning")
        transactions = Transactions.query.filter(month==month, year==year)
        return render_template("results.html", transactions=transactions)
    return render_template("results.html")
