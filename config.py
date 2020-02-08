import os
import tempfile

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
  """All the configurations required to run the web application"""

  # Configure session to use filesystem (instead of signed cookies)
  SESSION_FILE_DIR = tempfile.mkdtemp()
  SESSION_PERMANENT = False
  SESSION_TYPE = "filesystem"

  # Database configuration
  SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or ("sqlite:///" + os.path.join(basedir, "finance.db"))
  SQLALCHEMY_TRACK_MODIFICATIONS = False
