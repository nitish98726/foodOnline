from django.core.exceptions import ValidationError
import os

def allow_only_images(value):
    ext = os.path.splitext(value.name)[1]
    print(ext)
    valid_extensions = ['.png' , '.jpg' , '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported File Extension" +str(valid_extensions))