import os
import resend
from rest_framework.response import Response
from dotenv import load_dotenv

load_dotenv()


def send_email(
    subject: str,
    recipient_list: list,
    cc_list: list,
    from_email: str,
    message: str,
    attachments: list,
):

    if not all([subject, recipient_list, from_email, message]):
        return {"code": -1, "message": "Missing required fields"}

    resend.api_key = os.getenv("RESEND_API_KEY")
    sender = from_email.split("@")[0].title()

    if isinstance(recipient_list, str):
        recipient_list = [recipient_list]

    if isinstance(cc_list, str):
        cc_list = [cc_list]

    params: resend.Emails.SendParams = {
        "from": "{} <{}>".format(sender, from_email),  # "<info@dategroupafrica.com>",
        "to": recipient_list,
        "subject": subject,
        "": attachments or [],
        # "html": "<strong>it works!</strong>",
        "html": """
            <div class="email-body" style="font-family: sans-serif;">
                <p style="padding: 20px;"> Follow the link below to reset your password </p>
                <a href="{}" style="text-decoration: none; font-size: large; padding: 0 20px;">
                    <strong style="color: #00a6b9;">Reset Your Password</strong>
                </a>
            </div>
        """.format(
            message
        ),
    }

    email = resend.Emails.send(params)
    return {"code": 0, "status": "ok", "message": email}
