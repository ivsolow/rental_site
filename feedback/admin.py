from django.contrib import admin
from feedback.models import Feedback, FeedbackPhoto

admin.site.register(Feedback)

# class FeedbackPhoto(admin.TabularInline):
#     model = FeedbackPhoto
#     extra = 10
