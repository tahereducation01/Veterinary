// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let valid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    valid = false;
                    field.style.borderColor = 'red';
                } else {
                    field.style.borderColor = '';
                }
            });

            if (!valid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });

    // Date validation for appointments
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        const today = new Date().toISOString().split('T')[0];
        input.min = today;
    });

    // Service cards animation
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    document.querySelectorAll('.card, .doctor-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
});

// Pet form management
function showAddPetForm() {
    document.getElementById('addPetForm').style.display = 'block';
}

function hideAddPetForm() {
    document.getElementById('addPetForm').style.display = 'none';
}

// Appointment booking helpers
function calculateServiceDuration(serviceId) {
    // This would typically fetch from the server
    const durations = {
        1: 30, 2: 20, 3: 60, 4: 45, 5: 90, 6: 60
    };
    return durations[serviceId] || 30;
}

function updateAvailableTimes(doctorId, date) {
    // This would typically fetch available times from the server
    console.log(`Fetching available times for doctor ₹{doctorId} on ₹{date}`);
} 
