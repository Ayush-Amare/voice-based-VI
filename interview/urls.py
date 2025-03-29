from django.urls import path,include
from .views import process_audio, start_interview, question_page, evaluate_interview

urlpatterns = [
    path('', start_interview, name='start_interview'), 
    path('interview/', start_interview, name='start_interview'), 
    path('question/<int:question_number>/', question_page, name='question_page'),
    path('evaluate/<int:session_id>/', evaluate_interview, name='evaluate_interview'),
    path("process_audio/", process_audio, name="process_audio"),
]