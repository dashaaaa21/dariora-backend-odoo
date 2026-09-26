from . import models
from . import controllers

# Monkey patch Odoo's security check to handle None session_token
import odoo.service.security as security_module

_original_check_session = security_module.check_session

def patched_check_session(session, env, httprequest):
    """Patched version that handles None session_token"""
    if not session.uid:
        return False
    
    try:
        return _original_check_session(session, env, httprequest)
    except TypeError:
        # Handle the case where session_token is None
        return False

security_module.check_session = patched_check_session
