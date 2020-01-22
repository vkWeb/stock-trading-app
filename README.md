# Stock Trading Web App
A stock trading web app built on Flask with an aim to learn about backends. 

- Buy, sell, check price of stocks in realtime
- View portfolio of your stocks
- View history of purchase and sale of stocks

### My Learning Objectives:

- [x] caching in detail
- [x] databases, ORMs
- [ ] deployment to cloud
- [ ] cookies, session management
- [ ] authentication, authorization
- [ ] WSGI servers and werkzeug (flask is based on werkzeug)
- [ ] web security - eliminate OWASP top ten security risks from the app 
- [ ] REST APIs in detail - Read Roy Fielding's paper
- [ ] client side validation via JavaScript, AJAX
- [ ] scalability, testing, CI & CD
- [ ] QA

### Quick Development Setup

Fork. Clone. Make sure you `cd` to `stock-trading-app` directory. Set upstream and origin.

Install or update to the latest version of `Python` if you haven't already.

Time to get started. Feel free to create an issue if you get stuck or if you need help :)

```
# Install pipenv
pip install pipenv

# Install dependencies in a virtualenv
pipenv install

# Activate virtualenv subshell
pipenv shell

# Setup flask in development mode
export FLASK_APP="application.py"
export FLASK_ENV="development"

# Run app, served at http://127.0.0.1:5000 by default
flask run
```
