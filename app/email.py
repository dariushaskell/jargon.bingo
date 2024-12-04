import os
from mailersend import emails
from itsdangerous import URLSafeTimedSerializer
from flask import url_for, current_app
import traceback

def send_email_with_token(user, token_type, email_subject, email_template, inviter=''):
    if token_type == "verification":
        token = user.email_verification_token
        url = url_for("verify_email", token=token, _external=True)
    elif token_type == "reset":
        token = user.password_reset_token
        url = url_for("reset_password", token=token, _external=True)
    elif token_type == "invite":
        token = user.email_verification_token
        inviter = inviter
        print(f"Inviter: {inviter}, token: {token}")
        url = url_for("complete_registration", token=token, _external=True)
    else:
        raise ValueError("Invalid token type")

    html = email_template.format(url=url, inviter=inviter)
    send_email(user.email, email_subject, html)

def send_verification_email(user):
    email_template = '<p>Hi, please verify your email by clicking <a href="{url}">here</a>.</p>'
    send_email_with_token(user, "verification", "Verify Your Email", email_template)

def send_password_reset_email(user):
    email_template = '<p>To reset your password, click <a href="{url}">here</a>.</p>'
    send_email_with_token(user, "reset", "Reset Your Password", email_template)

def send_invite_email(user, inviter):
    email_template = '<p>You have been invited to join Jargon Bingo by {inviter}. Click <a href="{url}">here</a> to register.</p>'
    print(f"Sending invite email to {user.email} from {inviter}")
    send_email_with_token(user, "invite", "You've been invited to Jargon Bingo", email_template, inviter)

def send_email(to, subject, html):
    api_key = os.environ.get("MAILERSEND_API_KEY")
    if not api_key:
        raise ValueError("MAILERSEND_API_KEY not set in environment variables.")

    mailer = emails.NewEmail(api_key)

    mail_body = {}

    mail_from = {
        "name": "Jargon Bingo Admin",
        "email": os.environ.get("FROM_EMAIL", "admin@jargon.bingo"),
    }

    recipients = [
        {
            "name": "Recipient",
            "email": to,
        }
    ]

    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    mailer.set_subject(subject, mail_body)
    mailer.set_html_content(html, mail_body)

    try:
        response = mailer.send(mail_body)
        print(f"Email sent: {response}")
    except emails.MailSendError as e:
        print("Failed to send email: ", e)
    except Exception as e:
        print("An unexpected error occurred:")
        print(traceback.format_exc())
