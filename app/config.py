from secrets import token_hex
# Teníamos un problema de seguridad, el SECRET_KEY era público y 
class Config:
    SECRET_KEY = token_hex(16)
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    WTF_CSRF_ENABLED = True