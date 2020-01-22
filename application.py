import os
import cs50
import flask
import flask_session
import tempfile
import werkzeug
import helpers

# Configure application
app = flask.Flask(__name__)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache"
    return response


# Jinja2 custom filter
app.jinja_env.filters["usd"] = helpers.usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = tempfile.mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
flask_session.Session(app)

# Configure CS50 Library to use SQLite database
db = cs50.SQL("sqlite:///finance.db")

# Make sure API key is set
"""
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")
"""


@app.route("/")
@helpers.login_required
def index():
    """Show portfolio of stocks"""
    return helpers.apology("TODO", 500)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if flask.request.method == "POST":

        # Ensure username was submitted
        if not flask.request.form.get("username"):
            return helpers.apology("must provide username", 401)

        # Ensure password was submitted
        elif not flask.request.form.get("password"):
            return helpers.apology("must provide password", 401)

        # Ensure confirmation password was submitted
        elif not flask.request.form.get("confirmation"):
            return helpers.apology("must provide confirmation password", 401)

        # Ensure password and confirmation password are same
        elif flask.request.form.get("password") != flask.request.form.get("confirmation"):
            return helpers.apology("password and confirmation password must be same", 401)
    
    else:
        # Render register page
        return flask.render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    flask.session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if flask.request.method == "POST":

        # Ensure username was submitted
        if not flask.request.form.get("username"):
            return helpers.apology("must provide username", 401)

        # Ensure password was submitted
        elif not flask.request.form.get("password"):
            return helpers.apology("must provide password", 401)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=flask.request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not werkzeug.security.check_password_hash(rows[0]["hash"], flask.request.form.get("password")):
            return helpers.apology("invalid username and/or password", 401)

        # Remember which user has logged in
        flask.session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return flask.redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return flask.render_template("login.html")


@app.route("/logout")
def logout():
    """
    Log user out
    Forget any user_id and redirect user to login form
    """
    flask.session.clear()
    return flask.redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@helpers.login_required
def quote():
    """Get stock quote."""
    return helpers.apology("TODO", 500)


@app.route("/buy", methods=["GET", "POST"])
@helpers.login_required
def buy():
    """Buy shares of stock"""
    return helpers.apology("TODO", 500)


@app.route("/sell", methods=["GET", "POST"])
@helpers.login_required
def sell():
    """Sell shares of stock"""
    return helpers.apology("TODO", 500)


@app.route("/history")
@helpers.login_required
def history():
    """Show history of transactions"""
    return helpers.apology("TODO", 500)


@app.route("/api/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    return flask.jsonify("TODO", 500)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, werkzeug.exceptions.HTTPException):
        e = werkzeug.exceptions.InternalServerError()
    return helpers.apology(e.name, e.code)


# Listen for errors
for code in werkzeug.exceptions.default_exceptions:
    app.errorhandler(code)(errorhandler)
