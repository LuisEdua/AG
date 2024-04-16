from flask import Flask
from routes import Data
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.register_blueprint(Data.DataRoutes, url_prefix='/api/data')
    CORS(app)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
