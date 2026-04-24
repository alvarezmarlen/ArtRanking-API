/**
 * Alerts Handler
 * Handles auto-hiding of flash messages after a specified duration.
 */
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        // Wait 5 seconds before starting the hide animation
        setTimeout(() => {
            alert.classList.add('hide');
            
            // Wait for CSS transition (300ms) before removing from DOM
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 4000);
    });
});
