# 🎯 Interactive Professional Quiz Application

A Flask-based web application for conducting professional certification quizzes with automatic certificate generation.

## Features

- ✅ Interactive multiple-choice quiz interface
- ✅ Auto-generated PDF certificates
- ✅ Score calculation and performance evaluation
- ✅ Answer review after completion
- ✅ CSV storage for results tracking
- ✅ Responsive design for mobile and desktop
- ✅ Random question ordering

## Installation & Setup

### 1. Clone the repository

git clone https://github.com/Harvad-stack/quiz-certification-app.git

cd quiz-certification-app


### 2. Create virtual environment

python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate


### 3. Install dependencies

pip install -r requirements.txt

### 4. Run the application

python app.py



The app will be available at `http://localhost:5000`

## Usage

1. Enter your name, email (optional), and department
2. Click "Start Quiz" to begin
3. Answer all 10 multiple-choice questions
4. View your results and download certificate
5. Review your answers

## Quiz Details

- **Total Questions**: 10
- **Passing Score**: 50%
- **Time Limit**: None (can be added as extension)
- **Topics**: Python, Programming, Data Structures

## Performance Criteria

- **80%+ (Excellent)**: Full certification with honors
- **50-79% (Good)**: Certification approved
- **Below 50%**: Reattempt recommended

## Deployment Options

### Option 1: Deploy to Render (Recommended)

1. Push code to GitHub
2. Sign up at [render.com](https://render.com)
3. Create new Web Service
4. Connect your GitHub repository
5. Deploy automatically

### Option 2: Deploy to PythonAnywhere

1. Upload files to PythonAnywhere
2. Configure web app in Web tab
3. Set up WSGI configuration
4. Reload and test

### Option 3: Deploy to Heroku

1. Install Heroku CLI
2. Create `Procfile`: `web: gunicorn app:app`
3. Deploy: `git push heroku main`

## Customization

### Adding Questions

Edit `data/questions.json`:



### Changing Theme Colors

Edit `static/css/style.css` - modify gradient colors in the `body` selector.

## Extension Tasks Completed

- ✅ Random question shuffling
- ✅ PDF certificate generation
- ✅ CSV results storage
- ⏱️ Timer (code provided in script.js, commented)

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Certificate**: ReportLab
- **Data Storage**: JSON, CSV


