from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from database.db import get_db, get_user_by_email, get_user_by_id, init_db, seed_db, create_user

app = Flask(__name__)
app.secret_key = "dev-secret-change-me"

with app.app_context():
    init_db()
    seed_db()


@app.context_processor
def inject_current_user():
    user_id = session.get('user_id')
    return {"current_user": get_user_by_id(user_id) if user_id else None}


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get('user_id'):
        return redirect(url_for("landing"))
    if request.method == "GET":
        return render_template("register.html")

    name             = request.form.get("name", "").strip()
    email            = request.form.get("email", "").strip()
    password         = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not all([name, email, password, confirm_password]):
        flash("All fields are required.")
        return render_template("register.html")

    if get_user_by_email(email):
        flash("An account with that email already exists.")
        return render_template("register.html")

    if password != confirm_password:
        flash("Passwords do not match.")
        return render_template("register.html")

    if len(password) < 8:
        flash("Password must be at least 8 characters.")
        return render_template("register.html")

    create_user(name, email, generate_password_hash(password))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get('user_id'):
        return redirect(url_for("landing"))
    if request.method == "GET":
        return render_template("login.html")

    email    = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email or not password:
        flash("All fields are required.")
        return render_template("login.html")

    user = get_user_by_email(email)
    if not user or not check_password_hash(user["password_hash"], password):
        flash("Invalid email or password.")
        return render_template("login.html")

    session["user_id"] = user["id"]
    return redirect(url_for("landing"))


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    return "Profile page — coming in Step 4"


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
