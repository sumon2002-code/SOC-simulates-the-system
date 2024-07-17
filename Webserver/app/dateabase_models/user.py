try:
    from ._models import User, NotUserAuthenticated
except ImportError :
    from _models import User, NotUserAuthenticated