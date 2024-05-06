from flask import (
    Blueprint,
    jsonify,
    request
)

from booking_management.tasks.email_task import send_tickets_email

email_bp = Blueprint("email", __name__)


@email_bp.route("/send-email/", methods=["POST"])
def send_email():
    data = request.json

    if (html_content := data.get("html_content")) is None:
        return jsonify({"message": "No html content provided"}, status=400)

    if (user_email := data.get("user_email")) is None:
        return jsonify({"message": "No html content provided"}, status=400)

    send_tickets_email.delay(html_content, user_email)

    return jsonify(
        {"message": "Email task triggered successfully"}, status=202
    )
