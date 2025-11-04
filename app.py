from flask import Flask, render_template, request, session, send_file, redirect, url_for
import json
import random
from datetime import datetime
import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import csv

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Load questions from JSON file
def load_questions():
    with open('data/questions.json', 'r') as f:
        return json.load(f)

# Generate certificate
def generate_certificate(name, department, score, total, percentage):
    filename = f"certificates/{name.replace(' ', '_')}_certificate.pdf"
    
    # Ensure certificates directory exists
    os.makedirs('certificates', exist_ok=True)
    
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    
    # Certificate design
    c.setFillColorRGB(0.2, 0.3, 0.5)
    c.rect(30, 30, width - 60, height - 60, stroke=1, fill=0)
    
    c.setFont("Helvetica-Bold", 36)
    c.setFillColorRGB(0.1, 0.2, 0.4)
    c.drawCentredString(width/2, height - 100, "CERTIFICATE")
    
    c.setFont("Helvetica", 18)
    c.drawCentredString(width/2, height - 140, "of Achievement")
    
    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2, height - 200, "This is to certify that")
    
    c.setFont("Helvetica-Bold", 24)
    c.setFillColorRGB(0.0, 0.0, 0.0)
    c.drawCentredString(width/2, height - 240, name)
    
    c.setFont("Helvetica", 14)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    c.drawCentredString(width/2, height - 280, f"from {department}")
    
    c.drawCentredString(width/2, height - 320, "has successfully completed the")
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height - 350, "Professional Certification Quiz")
    
    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2, height - 390, f"with a score of {score}/{total} ({percentage:.2f}%)")
    
    # Performance status
    if percentage >= 80:
        status = "Excellent Performance"
    elif percentage >= 50:
        status = "Good Attempt"
    else:
        status = "Needs Improvement"
    
    c.setFont("Helvetica-Bold", 14)
    c.setFillColorRGB(0.0, 0.5, 0.0)
    c.drawCentredString(width/2, height - 420, status)
    
    # Date
    c.setFont("Helvetica", 12)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    date_str = datetime.now().strftime("%B %d, %Y")
    c.drawCentredString(width/2, 100, f"Date: {date_str}")
    
    c.save()
    return filename

# Save results to CSV
def save_to_csv(name, email, department, score, total, percentage):
    filename = 'certificates/quiz_results.csv'
    file_exists = os.path.isfile(filename)
    
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['Name', 'Email', 'Department', 'Score', 'Total', 'Percentage', 'Date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({
            'Name': name,
            'Email': email,
            'Department': department,
            'Score': score,
            'Total': total,
            'Percentage': f"{percentage:.2f}",
            'Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-quiz', methods=['POST'])
def start_quiz():
    session['name'] = request.form.get('name')
    session['email'] = request.form.get('email', '')
    session['department'] = request.form.get('department')
    
    questions = load_questions()
    
    # Shuffle questions for randomness
    random.shuffle(questions)
    
    session['questions'] = questions
    session['current_question'] = 0
    session['score'] = 0
    session['answers'] = []
    
    return redirect(url_for('quiz'))

@app.route('/quiz')
def quiz():
    if 'questions' not in session:
        return redirect(url_for('index'))
    
    current_idx = session['current_question']
    questions = session['questions']
    
    if current_idx >= len(questions):
        return redirect(url_for('result'))
    
    question = questions[current_idx]
    total_questions = len(questions)
    
    return render_template('quiz.html', 
                         question=question, 
                         current=current_idx + 1, 
                         total=total_questions)

@app.route('/submit-answer', methods=['POST'])
def submit_answer():
    if 'questions' not in session:
        return redirect(url_for('index'))
    
    selected_answer = request.form.get('answer')
    current_idx = session['current_question']
    questions = session['questions']
    
    correct_answer = questions[current_idx]['correct']
    is_correct = (selected_answer == correct_answer)
    
    if is_correct:
        session['score'] = session.get('score', 0) + 1
    
    # Store answer history
    answers = session.get('answers', [])
    answers.append({
        'question': questions[current_idx]['question'],
        'selected': selected_answer,
        'correct': correct_answer,
        'is_correct': is_correct
    })
    session['answers'] = answers
    
    session['current_question'] = current_idx + 1
    
    return redirect(url_for('quiz'))

@app.route('/result')
def result():
    if 'score' not in session:
        return redirect(url_for('index'))
    
    name = session['name']
    email = session.get('email', '')
    department = session['department']
    score = session['score']
    total = len(session['questions'])
    percentage = (score / total) * 100
    
    # Generate certificate
    cert_filename = generate_certificate(name, department, score, total, percentage)
    
    # Save to CSV
    save_to_csv(name, email, department, score, total, percentage)
    
    # Determine performance level
    if percentage >= 80:
        performance = "Excellent - You are Certified!"
        performance_class = "excellent"
    elif percentage >= 50:
        performance = "Good Attempt - Certification Approved"
        performance_class = "good"
    else:
        performance = "Needs Improvement - Reattempt Required"
        performance_class = "poor"
    
    return render_template('result.html',
                         name=name,
                         score=score,
                         total=total,
                         percentage=percentage,
                         performance=performance,
                         performance_class=performance_class,
                         cert_filename=os.path.basename(cert_filename),
                         answers=session['answers'])

@app.route('/download-certificate/<filename>')
def download_certificate(filename):
    return send_file(f'certificates/{filename}', as_attachment=True)

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
