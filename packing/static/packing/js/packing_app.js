document.addEventListener('DOMContentLoaded', function() {
    // Lazy load images
    const lazyImages = document.querySelectorAll('img.lazy');
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const image = entry.target;
                    image.src = image.dataset.src;
                    image.classList.remove('lazy');
                    imageObserver.unobserve(image);
                }
            });
        });
        
        lazyImages.forEach(image => {
            imageObserver.observe(image);
        });
    } else {
        // Fallback for browsers without IntersectionObserver
        lazyImages.forEach(image => {
            image.src = image.dataset.src;
            image.classList.remove('lazy');
        });
    }
    
    // Form validation optimization
    const packingForm = document.getElementById('packing-form');
    if (packingForm) {
        // Client-side form validation to avoid server roundtrips
        packingForm.addEventListener('submit', function(e) {
            const startDate = new Date(document.getElementById('id_start_date').value);
            const endDate = new Date(document.getElementById('id_end_date').value);
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            
            let hasErrors = false;
            
            // Clear previous error messages
            const errorMessages = document.querySelectorAll('.error-message');
            errorMessages.forEach(message => message.remove());
            
            // Check if destination is empty
            const destination = document.getElementById('id_destination').value;
            if (!destination) {
                addErrorMessage('id_destination', 'Please enter a destination');
                hasErrors = true;
            }
            
            // Check if end date is after start date
            if (endDate < startDate) {
                addErrorMessage('id_end_date', 'End date must be after start date');
                hasErrors = true;
            }
            
            // Check if start date is not in the past
            if (startDate < today) {
                addErrorMessage('id_start_date', 'Start date cannot be in the past');
                hasErrors = true;
            }
            
            // Check if trip is not too long
            const tripDays = (endDate - startDate) / (1000 * 60 * 60 * 24) + 1;
            if (tripDays > 14) {
                addErrorMessage('id_end_date', 'Trip duration should be 14 days or less for accurate weather forecasting');
                hasErrors = true;
            }
            
            if (hasErrors) {
                e.preventDefault();
            } else {
                // Show loading indication immediately
                const submitBtn = packingForm.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Creating...';
                    submitBtn.disabled = true;
                }
            }
        });
    }
    
    // Helper function to add error messages
    function addErrorMessage(fieldId, message) {
        const field = document.getElementById(fieldId);
        const errorSpan = document.createElement('span');
        errorSpan.className = 'error-message text-danger';
        errorSpan.innerText = message;
        field.parentNode.appendChild(errorSpan);
        field.classList.add('is-invalid');
    }
    
    // Optimize itinerary display with accordion collapse
    const dayHeaders = document.querySelectorAll('.day-header');
    if (dayHeaders.length > 0) {
        // Only show first day by default
        const dayContents = document.querySelectorAll('.day-content');
        for (let i = 1; i < dayContents.length; i++) {
            dayContents[i].style.display = 'none';
        }
        
        // Add click event to day headers
        dayHeaders.forEach((header, index) => {
            header.addEventListener('click', function() {
                const content = this.nextElementSibling;
                if (content.style.display === 'none') {
                    content.style.display = 'block';
                } else {
                    content.style.display = 'none';
                }
            });
        });
    }
    
    // Add print functionality
    const printButton = document.getElementById('print-button');
    if (printButton) {
        printButton.addEventListener('click', function() {
            window.print();
        });
    }
    
    // Optimize category display with tabs
    const categoryTabs = document.querySelectorAll('.category-tab');
    if (categoryTabs.length > 0) {
        // Show only first category by default
        const categoryContents = document.querySelectorAll('.category-content');
        for (let i = 1; i < categoryContents.length; i++) {
            categoryContents[i].style.display = 'none';
        }
        
        // Add active class to first tab
        categoryTabs[0].classList.add('active');
        
        // Add click event to tabs
        categoryTabs.forEach((tab, index) => {
            tab.addEventListener('click', function() {
                // Hide all contents
                categoryContents.forEach(content => {
                    content.style.display = 'none';
                });
                
                // Remove active class from all tabs
                categoryTabs.forEach(tab => {
                    tab.classList.remove('active');
                });
                
                // Show selected content and add active class to tab
                categoryContents[index].style.display = 'block';
                this.classList.add('active');
            });
        });
    }
});