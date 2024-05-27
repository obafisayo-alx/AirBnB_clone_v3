#!/usr/bin/python3
"""check the status of your API"""

from os import getenv
from flask import Flask
from models import storage



app = Flask(__name__)
def create_app():
    """Create flask application."""

    with app.app_context():
        from api.v1.views import app_views
        app.register_blueprint(app_views)
        return app


@app.teardown_appcontext
def close_storage(exception):
    """close db connection when app context is torn down"""
    storage.close()

if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    app = create_app()
    if host and port:
        app.run(host=host, port=port, threaded=True, debug=True)
    else:
        app.run(host="0.0.0.0", port=5000, threaded=True, debug=True)