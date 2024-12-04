from datetime import datetime, timedelta
from app import create_app
from flask import current_app
from app.models import db, ActiveSession

# Load the Flask app context
app = create_app()


def clean_up_sessions():
    
    with app.app_context():
       
        # This function cleans up expired sessions based on a cutoff time
        expiration_time = current_app.config['PERMANENT_SESSION_LIFETIME']
        cutoff_time = datetime.utcnow() - timedelta(seconds=expiration_time)
        
        expired_sessions = ActiveSession.query.filter(ActiveSession.login_time < cutoff_time).all()
        for session in expired_sessions:
            db.session.delete(session)
        
        db.session.commit()

clean_up_sessions()