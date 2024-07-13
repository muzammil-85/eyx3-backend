from django.contrib import admin
from .models import Detection, Doctor, User

# Register your models here.
admin.site.register(Detection)
admin.site.register(Doctor)
admin.site.register(User)