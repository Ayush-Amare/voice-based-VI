
from django.contrib import admin
from .models import InterviewSession, InterviewResponse  # ✅ Import models

admin.site.register(InterviewSession)
admin.site.register(InterviewResponse)
# Register your models here.
