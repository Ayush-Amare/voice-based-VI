from django.db import models
from django.contrib.auth.models import User

class InterviewSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="interview_sessions")
    job_profile = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=50, default="Easy")
    created_at = models.DateTimeField(auto_now_add=True)
    evaluated = models.BooleanField(default=False)
    evaluation_feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Interview for {self.user.username} ({self.job_profile}) on {self.created_at.strftime('%Y-%m-%d')}"

class InterviewResponse(models.Model):
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, related_name="responses")
    question_number = models.IntegerField()
    question_text = models.TextField()
    answer_text = models.TextField(blank=True, null=True)
    audio_response = models.FileField(upload_to="audio_responses/", blank=True, null=True)

    def __str__(self):
        return f"Q{self.question_number} - {self.session.user.username}"