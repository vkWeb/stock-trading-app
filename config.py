import os
import tempfile

class Config(object):
  """ All the configurations required to run the web application """

  # Configure session to use filesystem (instead of signed cookies)
  SESSION_FILE_DIR = tempfile.mkdtemp()
  SESSION_PERMANENT = False
  SESSION_TYPE = "filesystem"

  # API Config
  API_KEY = os.environ.get("API_KEY") or "pk_7819282ea61a4fdd897c9cb12a242d7b"
