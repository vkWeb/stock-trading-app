# Stock Trading Web App
An app built with Flask to "buy" and "sell" stocks. Buy, sell, check price of stocks in realtime.

### My Learning Objectives:

- [x] caching in detail
- [ ] cookies, session management
- [ ] authentication, authorization
- [ ] web security - eliminate OWASP top ten security risks from the app 
- [ ] databases, ORMs
- [ ] REST APIs in detail - Read Roy Fielding's paper
- [ ] client side validation via JavaScript, AJAX
- [ ] deployment to cloud, basic scalability
- [ ] testing and QA

### Quick Development Setup

Fork. Clone. Make sure to `cd` to `stock-trading-app` directory. Set upstream and origin.

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
