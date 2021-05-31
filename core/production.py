from core.settings import *
import mimetypes



# This will overwrite anything in settings.py
mimetypes.add_type("text/css", ".css", True)
DEBUG = False
