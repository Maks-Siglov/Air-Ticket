from flask import Flask

from booking_management.core.settings import (
    APP_DEBUG,
    APP_HOST,
    APP_PORT
)
from booking_management.routers import email_bp

app = Flask(__name__)

app.register_blueprint(email_bp)

if __name__ == "__main__":
    app.run(host=APP_HOST, port=APP_PORT, debug=APP_DEBUG)
