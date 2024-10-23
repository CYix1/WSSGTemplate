import inspect
import sys

from django.contrib import admin

from WSSGTemplate.Core.models import *

# List comprehension to get all classes which are definied in WSSGTemplate.Core.models
# more fail proof than adding the classes manually!
# if migrations fails, it could be from caching issues. Use "./manage.py makemigrations --empty WSSGTemplate"
model_classes = [member for name, member in
                 inspect.getmembers(sys.modules['WSSGTemplate.Core.models'], inspect.isclass)]
print(model_classes)
for model_class in model_classes:
    # User is also defined. so a little filtering is being done.
    if model_class is not User:
        print(f"added {model_class}")
        admin.site.register(model_class)
