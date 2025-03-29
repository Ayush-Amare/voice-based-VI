# Voice-Based AI Interview System

## Project Overview
This project is a **Voice-Based AI Interview System** that dynamically conducts interviews based on the selected job profile. The AI:
- Asks **spoken questions** dynamically.
- Captures **vocal responses** from the candidate.
- Evaluates responses using AI and provides feedback.

## Key Features
- **Multi-Step Interview Process:** The interview is split across **7 different pages**, each containing a question and recording the response.
- **Speech Recognition:** Converts spoken responses into text.
- **AI Evaluation:** Analyzes responses and provides an assessment.
- **Flask Backend:** Manages API requests and handles interview logic.
- **Django Integration:** Stores responses and results in a database.

## Tech Stack
- **Backend:** Flask (for AI-driven question generation), Django (for database management)
- **Frontend:** HTML, CSS, JavaScript (for user interaction)
- **Speech Processing:** Google Speech-to-Text API, DeepSpeech, or Whisper
- **Database:** PostgreSQL / MySQL
- **Deployment:** Docker, AWS/GCP/Azure

## Installation & Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-repo/voice-based-VI.git
   cd voice-interview-system
   ```
2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run Flask Backend:**
   ```bash
   cd backend
   flask run
   ```
5. **Run Django Server:**
   ```bash
   cd django_app
   python manage.py runserver
   ```

## Usage
1. Open the web application and select a **job profile**.
2. The AI will **ask spoken questions** one by one.
3. Users respond via **voice input**, which is transcribed and stored.
4. After all responses are collected, the AI **evaluates answers** and provides feedback.
5. Results are **stored in the database** for future reference.

## Future Enhancements
- **Multilingual Support** for interviews.
- **Real-Time Sentiment Analysis** of responses.
- **Enhanced AI feedback** with deep learning models.
- **Integration with HR systems** for applicant tracking.

## Contributing
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch`.
3. Commit your changes: `git commit -m "Added new feature"`.
4. Push to the branch: `git push origin feature-branch`.
5. Submit a pull request.


