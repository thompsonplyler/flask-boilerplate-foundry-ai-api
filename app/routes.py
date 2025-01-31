# Standard Library imports

# Core Flask imports
from flask import Blueprint

# Third-party imports

# App imports
from app import db_manager
from app import login_manager
from .views import (
    error_views,
    account_management_views,
    static_views,
    ai_views
)
from .models import User
from flask_cors import CORS

bp = Blueprint('routes', __name__)

CORS(bp,origins=[
"http://localhost:5173", 
"https://dynamic-griffin-6352b5.netlify.app/",
"https://dynamic-griffin-6352b5.netlify.app",
"dynamic-griffin-6352b5.netlify.app",
"34.234.106.80:443"
])

# alias
db = db_manager.session

# Request management
@bp.before_app_request
def before_request():
    db()

@bp.teardown_app_request
def shutdown_session(response_or_exc):
    db.remove()

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    if user_id and user_id != "None":
        return User.query.filter_by(user_id=user_id).first()

# Error views
bp.register_error_handler(404, error_views.not_found_error)

bp.register_error_handler(500, error_views.internal_error)

# Public views
bp.add_url_rule("/", view_func=static_views.index)
bp.add_url_rule("/index", view_func=static_views.index)

bp.add_url_rule("/register", view_func=static_views.register)

bp.add_url_rule("/login", view_func=static_views.login)

# Login required views
bp.add_url_rule("/settings", view_func=static_views.settings)

# Public API
bp.add_url_rule(
   "/api/login", view_func=account_management_views.login_account, methods=["POST"]
)

bp.add_url_rule("/logout", view_func=account_management_views.logout_account)

bp.add_url_rule(
   "/api/register",
   view_func=account_management_views.register_account,
   methods=["POST"],
)

# Login Required API
bp.add_url_rule("/api/user", view_func=account_management_views.user)

bp.add_url_rule(
   "/api/email", view_func=account_management_views.email, methods=["POST"]
)

# Admin required
bp.add_url_rule("/admin", view_func=static_views.admin)

# Test connection
bp.add_url_rule("/test", view_func=static_views.test_connection)

# AI Query
bp.add_url_rule("/api/prompt_openai", view_func=ai_views.prompt_openai, methods=["POST", "GET"])
