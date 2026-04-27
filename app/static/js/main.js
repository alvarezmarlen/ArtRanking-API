/**
 * ArtRanking Main JavaScript
 * Handles common UI interactions like modals and dynamic alerts.
 */

/**
 * Open a modal by ID
 * @param {string} modalId 
 */
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden'; // Prevent scrolling
    }
}

/**
 * Close a modal by ID
 * @param {string} modalId 
 */
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = ''; // Restore scrolling
    }
}

/**
 * Dynamically create and show an alert message
 * @param {string} message 
 * @param {string} type - 'success', 'error', 'info'
 */
function showAlert(message, type = 'info') {
    const container = document.querySelector('.alerts-container');
    if (!container) return;

    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    
    // Choose icon based on type
    let icon = 'ℹ️';
    if (type === 'success') icon = '✅';
    if (type === 'error') icon = '❌';

    alert.innerHTML = `
        <span class="alert-icon">${icon}</span>
        <span class="alert-message">${message}</span>
    `;

    container.appendChild(alert);

    // Auto-hide after 5 seconds
    setTimeout(() => {
        alert.classList.add('hide');
        setTimeout(() => alert.remove(), 300);
    }, 5000);
}

// Close modals when clicking outside the content
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        closeModal(event.target.id);
    }
};
