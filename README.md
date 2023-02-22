# Stock Trading Web App
A stock trading web app built on Flask with an aim to learn about backends. 

- Buy, sell, check price of stocks in realtime
- View portfolio of your stocks
- View history of purchase and sale of stocks

## Quick Development Setup

Fork. Clone. Make sure you `cd` to `stock-trading-app` directory. Set upstream and origin.

Install or update to the latest version of `Python` if you haven't already.

Time to get started. Feel free to create an issue if you get stuck or if you need help :)

```
# Note: execute the below commands in `Bash` with administrative privileges

# Installs pipenv globally
pip install pipenv

# The below command installs dependencies in the pipenv's virtualenv
pipenv install --dev

# Activates virtualenv subshell
pipenv shell

# Copies `sample.env` to `.env`
# You can paste your API credentials in `.env`
cp sample.env .env

# Runs the app, served at http://127.0.0.1:5000 by default
flask run
```
