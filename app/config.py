import os
import sys

class Config:
    SECRET_KEY = os.environ.get("APP_SECRET_KEY")
    if not SECRET_KEY:
        sys.exit("Error: APP_SECRET_KEY is not set!")

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    if not SQLALCHEMY_DATABASE_URI:
        sys.exit("Error: DATABASE_URL is not set!")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAILERSEND_API_KEY = os.environ.get("MAILERSEND_API_KEY")
    if not MAILERSEND_API_KEY:
        sys.exit("Error: MAILERSEND_API_KEY is not set!")

    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")
    if not SECURITY_PASSWORD_SALT:
        sys.exit("Error: SECURITY_PASSWORD_SALT is not set!")

    # Session management configurations
    SESSION_COOKIE_SECURE = True  # Use secure cookies
    SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript from accessing the cookie
    PERMANENT_SESSION_LIFETIME = 3600  # Set session lifetime to 1 hour
