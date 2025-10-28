import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'replace_this_securely'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    REMEMBER_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = 1800  # 30 min
    WTF_CSRF_TIME_LIMIT = None