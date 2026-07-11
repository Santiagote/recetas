import os
from flask import Flask
from flask_cors import CORS
from api.rutas_compilacion import bp_compilacion

app = Flask(__name__)
CORS(app)
app.register_blueprint(bp_compilacion)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))