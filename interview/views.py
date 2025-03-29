from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from .models import InterviewSession, InterviewResponse
import speech_recognition as sr
import google.generativeai as genai
from gtts import gTTS
import os
import re
import json

# Generate and Configure your Gemini API 
genai.configure(api_key="YOUR_GEMINI_API_KEY")

def generate_tts_audio(text):
    """Generate TTS audio and return the relative media URL."""
    media_path = os.path.join(settings.BASE_DIR, 'media')
    os.makedirs(media_path, exist_ok=True)
    file_path = os.path.join(media_path, "tts_audio.mp3")
    tts = gTTS(text=text, lang="en")
    tts.save(file_path)
    
    return settings.MEDIA_URL + "tts_audio.mp3"

@login_required
def start_interview(request):
    """Start a new interview session and store questions."""
    if request.method == "POST":
        job = request.POST.get("job", "Software Analyst")
        difficulty = request.POST.get("difficulty", "Easy")

        # Generate interview questions
        model = genai.GenerativeModel("gemini-1.5-pro")
        convo = model.start_chat(history=[])
        convo.send_message(f"Generate 7 {difficulty} interview questions for {job} (no dots, no numbering)")
        questions = [q.strip() for q in convo.last.text.splitlines() if q.strip()]

        if len(questions) < 7:
            return render(request, "error.html", {"message": "AI did not generate enough questions."})

        # Create an interview session
        session_obj = InterviewSession.objects.create(user=request.user, job_profile=job, difficulty=difficulty)

        # Store questions in the database
        for i, question in enumerate(questions, start=1):
            InterviewResponse.objects.create(session=session_obj, question_number=i, question_text=question)

        request.session['interview_session_id'] = session_obj.id
        return redirect("question_page", question_number=1)

    return render(request, "start_interview.html")

@login_required
def question_page(request, question_number):
    """Display each interview question."""
    session_id = request.session.get("interview_session_id")
    if not session_id:
        return redirect("start_interview")

    session_obj = get_object_or_404(InterviewSession, pk=session_id)

    try:
        response_obj = session_obj.responses.get(question_number=question_number)
    except InterviewResponse.DoesNotExist:
        return redirect("evaluate_interview")

    tts_audio_url = generate_tts_audio(response_obj.question_text)

    if request.method == "POST":
        answer_text = request.POST.get("answer_text", "").strip()

        if answer_text:
            response_obj.answer_text = answer_text
            response_obj.save()

        next_q = question_number + 1
        return redirect("question_page", question_number=next_q) if next_q <= 7 else redirect("evaluate_interview")

    context = {
        "question": response_obj.question_text,
        "question_number": question_number,
        "total_questions": 7,
        "tts_audio_url": tts_audio_url,
        "answer_text": response_obj.answer_text,
    }
    return render(request, "question_page.html", context)

@login_required
def evaluate_interview(request, session_id):
    """Evaluate a completed interview session."""
    session_obj = get_object_or_404(InterviewSession, pk=session_id)
    responses = session_obj.responses.order_by("question_number")

    if not session_obj.evaluated:
        # Compile answers for AI evaluation
        answers_text = "\n".join(f"Q{r.question_number}: {r.question_text}\nA: {r.answer_text}" for r in responses)

        # AI Feedback
        model = genai.GenerativeModel("gemini-1.5-pro")
        convo = model.start_chat(history=[])
        convo.send_message(f"Evaluate the following interview responses:\n{answers_text}")
        feedback = convo.last.text.strip()
        cleaned_feedback = re.sub(r"\*\*(.*?)\*\*", r"\1", feedback)

        # Store evaluation feedback
        session_obj.evaluation_feedback = cleaned_feedback
        session_obj.evaluated = True
        session_obj.save()

    context = {
        "feedback": session_obj.evaluation_feedback,
        "responses": responses,
    }
    return render(request, "evaluation.html", context)


@login_required
def process_audio(request):
    """Process and store user responses."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            session_id = data.get("session_id")
            question_number = data.get("question_number")
            answer_text = data.get("answer_text")

            if not session_id or not question_number or not answer_text:
                return JsonResponse({"error": "Missing data"}, status=400)

            response_obj = InterviewResponse.objects.get(session_id=session_id, question_number=question_number)
            response_obj.answer_text = answer_text.strip()
            response_obj.save()

            return JsonResponse({"message": "Response saved successfully"})

        except InterviewResponse.DoesNotExist:
            return JsonResponse({"error": "Question not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
