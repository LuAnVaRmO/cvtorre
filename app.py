#!/usr/bin/python3
from api.v1.views import app_views
from flask import Flask, render_template, make_response
from flask_cors import CORS
from config import DevelopmentConfig

# Initializations
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(render_template('error.html', error=error))


if __name__ == "__main__":
    app.run()
