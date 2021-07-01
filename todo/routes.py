from flask import redirect, url_for, render_template, request, redirect, flash
from flask_login import logout_user, login_required, current_user, login_user
from todo import app, db
from todo.models import ToDO, User
from todo.forms import LoginForm, SignupForm, ToDoForm



@app.route("/", methods=["POST", "GET"])
@login_required
def index():

    tasks = ToDO.query.order_by(ToDO.completed).all()    #returns all tasks, completed at the bottom 
    form = ToDoForm()
    if request.method == "POST":
        if form.validate_on_submit():
            new_task = ToDO(content=form.task.data, due_date=form.due_date.data)

            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for("index"))

        if form.errors != {}:  
        #Form should return empty dic if there's no errors
            for error_msg in form.errors.values():
                flash(f'There is an Error creating your task {error_msg}', category="danger")
    return render_template("index.html", tasks=tasks, form=form) 
    

@app.route("/delete/<int:id>" )
def delete(id):
    todo_task_delete = ToDO.query.get_or_404(id)

    try:
        db.session.delete(todo_task_delete)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return "Sorry there was an issue deleting your Task"


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    task = ToDO.query.get_or_404(id)
    form=ToDoForm()

    if request.method == "POST":
        if form.validate_on_submit():
            updated_task_due = ToDO(content=form.task.data, due_date=form.due_date.data)

            db.session.add(updated_task_due)
            db.session.commit()
            return redirect(url_for("index"))

        if form.errors != {}:  
        #Form should return empty dic if there's no errors
            for error_msg in form.errors.values():
                flash(f'There is an Error creating your task {error_msg}', category="danger")
        return render_template("update.html", task=task, form=form) 

        # return redirect(url_for("/update/<int:id>"))
    else:
        return render_template("update.html", task=task, form=form)


@app.route("/completed/<int:id>", methods=["POST", "GET"])
def complete(id):
    comp_task = ToDO.query.get_or_404(id)
    if comp_task.completed == False:
        comp_task.completed = True
    elif comp_task.completed == True:
        comp_task.completed = False
    
    try:
        db.session.add(comp_task)
        db.session.commit()
    except:
        return "Sorry we couldn't complete your task."

    return redirect("/")


@app.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_to_login = User.query.filter_by(username=form.username.data).first()
        if user_to_login and user_to_login.check_password(password_attempt=form.password.data):     #User_to_login should not return None if in db
            login_user(user_to_login)
            flash(f"You have succesfully logged in as {user_to_login.username}")
            return redirect(url_for("index"))

        else:
            flash("That Username and Password does not exist. Please try again", category="danger")




    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash(f'You are now logged out!', category="info")
    return redirect(url_for("signup"))


@app.route("/signup", methods = ["GET", "POST"])
def signup():
    form = SignupForm()
    if request.method == "POST":
        if form.validate_on_submit():
            new_user = User(username=form.username.data,
                            email_address=form.email_address.data,  
                            password=form.password1.data)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash(f'Your account has been created! You are now logged in as {new_user.username}', category="success")
            return redirect(url_for("index"))
    if form.errors != {}:
        for error_msg in form.errors.values():
            flash(f'There was an error creating your account: {error_msg}', category="danger")

    return render_template("signup.html", form=form)
    
