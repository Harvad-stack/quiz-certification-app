// Form validation
document.addEventListener('DOMContentLoaded', function() {
    const startForm = document.getElementById('startForm');
    if (startForm) {
        startForm.addEventListener('submit', function(e) {
            const name = document.getElementById('name').value.trim();
            const department = document.getElementById('department').value.trim();
            
            if (!name || !department) {
                e.preventDefault();
                alert('Please fill in all required fields!');
                return false;
            }
        });
    }
    
    // Quiz form handling
    const quizForm = document.getElementById('quizForm');
    if (quizForm) {
        quizForm.addEventListener('submit', function(e) {
            const selectedAnswer = document.querySelector('input[name="answer"]:checked');
            if (!selectedAnswer) {
                e.preventDefault();
                alert('Please select an answer!');
                return false;
            }
        });
    }
    
    // Add animation to options
    const options = document.querySelectorAll('.option-label');
    options.forEach(option => {
        option.addEventListener('click', function() {
            options.forEach(opt => opt.style.transform = 'scale(1)');
            this.style.transform = 'scale(1.02)';
        });
    });
});

// Optional: Timer functionality (extension task)
function startTimer(duration, display) {
    let timer = duration, minutes, seconds;
    const interval = setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);
        
        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;
        
        display.textContent = minutes + ":" + seconds;
        
        if (--timer < 0) {
            clearInterval(interval);
            alert("Time's up!");
            document.getElementById('quizForm').submit();
        }
    }, 1000);
}
