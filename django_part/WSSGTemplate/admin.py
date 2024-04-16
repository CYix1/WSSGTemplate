import inspect
import sys

from django.contrib import admin

from WSSGTemplate.models import *

# List comprehension to get all classes which are definied in WSSGTemplate.models
# more fail proof than adding the classes manually!
model_classes = [member for name, member in inspect.getmembers(sys.modules['WSSGTemplate.models'], inspect.isclass)]

for model_class in model_classes:
    # User is also defined. so a little filtering is being done.
    if model_class is not User:
        admin.site.register(model_class)
