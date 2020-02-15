import flask
import flask_session

from werkzeug import security, exceptions

from finance import app, db
from . import helpers
from .models import User, Transaction
from sqlalchemy.sql import func

# Jinja2 custom filters
app.jinja_env.filters["usd"] = helpers.usd # noqa
app.jinja_env.filters["lookup"] = helpers.lookup # noqa

# Apply flask_session to app
flask_session.Session(app)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
@helpers.login_required
def index():
    """Show portfolio of stocks"""

    user = User.query.get(flask.session.get("user_id"))
    trans_data = db.session.query(Transaction.company_name, Transaction.company_symbol, func.sum(Transaction.shares).label("shares")).filter_by(user_id=user.id).group_by(Transaction.company_symbol)
    return flask.render_template("index.html", transactions=trans_data, cash=user.cash)


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

        # Validation passed. Now query db for username
        user_check = User.query.filter_by(username=flask.request.form.get("username")).first()

        # If username doesn't exists then insert form data to db
        if user_check is None:
            user = User(username=flask.request.form.get("username"), hash=security.generate_password_hash(flask.request.form.get("password")))
            db.session.add(user)
            db.session.commit()

            # User registered
            # Now store user.id in session
            flask.session["user_id"] = user.id
            
            # Flash success register message
            flask.flash("Wow, we got a new user. You have successfully registered 😀", "success")

            # Redirect to index page
            return flask.redirect(flask.url_for("index"))
        
        # username already exists, throw error
        else:
            return helpers.apology("username already taken", 401)
    
    # If user is already logged in then redirect to index
    elif flask.request.method == "GET" and flask.session.get("user_id") is not None:
        flask.flash("Ummm, you have already registered 😉", "info")
        return flask.redirect(flask.url_for("index"))

    # Render register page as user reached via GET
    else:
        return flask.render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # User reached route via POST (as by submitting a form via POST)
    if flask.request.method == "POST":

        # Ensure username was submitted
        if not flask.request.form.get("username"):
            return helpers.apology("must provide username", 401)

        # Ensure password was submitted
        elif not flask.request.form.get("password"):
            return helpers.apology("must provide password", 401)

        # Query database for username
        user = User.query.filter_by(username=flask.request.form.get("username")).first()
        
        # Ensure username exists and password is correct
        if user is None: 
            return helpers.apology("no account found for entered username", 401)
        
        elif not security.check_password_hash(user.hash, flask.request.form.get("password")):
            return helpers.apology("invalid password", 401)

        # Remember which user has logged in
        flask.session["user_id"] = user.id

        # Flash success log in message
        flask.flash("Welcome again! You have successfully logged in 😀", "success")

        # Redirect user to home page
        return flask.redirect(flask.url_for("index"))
        
    # If user is already logged in then redirect to index
    elif flask.request.method == "GET" and flask.session.get("user_id") is not None:
        flask.flash("Don't be greedy, you are already logged in 😉", "info")
        return flask.redirect(flask.url_for("index"))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return flask.render_template("login.html")


@app.route("/logout", methods=["GET"])
def logout():
    """
    Log user out
    Forget any user_id and redirect user to index
    """
    flask.session.clear()

    # Flash success log out message
    flask.flash("You have successfully logged out. It's bad to see you go. We'll miss you 😔", "success")
    return flask.redirect(flask.url_for("index"))


@app.route("/quote", methods=["GET", "POST"])
@helpers.login_required
def quote():
    """Get stock quote (via helpers.lookup)."""

    # Initialize quote as None
    quote = None
    
    # If user submits symbol via POST
    if flask.request.method == "POST":
        # Render apology if symbol input is blank
        if not flask.request.form.get("symbol"):
            return helpers.apology("must provide symbol", 400)

        # Fetch symbol's stock details from helpers.lookup
        quote = helpers.lookup(flask.request.form.get("symbol"))

        if quote is None:
            flask.flash(f"Couldn't get quote for \"{flask.request.form.get('symbol')}\". Please re-check spelling and try again.", "danger")

    return flask.render_template("quote.html", quote=quote)


@app.route("/buy", methods=["GET", "POST"])
@helpers.login_required
def buy():
    """Buy shares of stock"""
    # If request method is POST as via form
    if flask.request.method == "POST":

        # If symbol is blank return apology
        if not flask.request.form.get("symbol"):
            return helpers.apology("must provide symbol", 400)

        # If no. of shares is blank return apology
        if not flask.request.form.get("shares"):
            return helpers.apology("must provide shares", 400)

        # Call API to get symbol's current price
        quote = helpers.lookup(flask.request.form.get("symbol"))

        # If symbol is invalid then flash error message
        if quote is None:
            flask.flash(f"Symbol \"{flask.request.form.get('symbol')}\" is invalid. Please re-check spelling and try again.", "danger")
        # Else calculate required cash for successful purchase
        else:
            cost = int(flask.request.form.get("shares")) * float(quote["price"])

            # Extract logged in user data from session
            user_data = User.query.get(flask.session.get("user_id"))
            
            # If user has enough cash then subtract cost from cash
            # Add transaction info to db and flash success message
            if user_data.cash >= cost:
                user_data.cash = user_data.cash - cost
                transaction = Transaction(user_id=flask.session.get("user_id"), company_name=quote["name"], company_symbol=quote["symbol"], shares=flask.request.form.get("shares"), price=quote["price"], trans_type="purchase")
                db.session.add(transaction)
                db.session.commit()
                flask.flash(f"Purchase successful 🤑", "info")
            # Else flash message to inform user for insufficient funds
            else:
                flask.flash(f"You don't have enough cash. Total cost of purchase is {helpers.usd(cost)}, you have {helpers.usd(user_data.cash)} 😥", "info")

    # Render template
    return flask.render_template("buy.html")


@app.route("/sell", methods=["GET", "POST"])
@helpers.login_required
def sell():
    """Sell shares of stock"""
    return helpers.apology("TODO", 500)


@app.route("/history", methods=["GET"])
@helpers.login_required
def history():
    """Show history of transactions"""
    return helpers.apology("TODO", 500)


@app.route("/api/check/<string:username>", methods=["GET"])
def check(username):
    """Return true if username available, else false, in JSON format"""
    result = User.query.filter_by(username=username).first()
    
    if result is None:
        return flask.jsonify(is_username_available=True)
    return flask.jsonify(is_username_available=False)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, exceptions.HTTPException):
        e = exceptions.InternalServerError()
    return helpers.apology(e.name, e.code)


# Listen for errors
for code in exceptions.default_exceptions:
    app.errorhandler(code)(errorhandler)
