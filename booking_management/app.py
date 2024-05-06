from flask import Flask

from booking_management.core import settings
from booking_management.routers import email_bp

app = Flask(__name__)

app.register_blueprint(email_bp)

if __name__ == "__main__":
    app.run(
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        debug=settings.APP_DEBUG,
    )
