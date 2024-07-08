from main import app
from flask_cors import CORS

CORS(app)
app.run("0.0.0.0", 80, debug=True)
