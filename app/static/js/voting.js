
/**
 * ArtRanking Voting System
 * Handles artwork voting via AJAX
 */

document.addEventListener('DOMContentLoaded', () => {
    const voteButtons = document.querySelectorAll('.btn-vote');

    voteButtons.forEach(button => {
        button.addEventListener('click', async (e) => {
            e.preventDefault();
            const submissionId = button.getAttribute('data-id');
            
            // Check if user is logged in (heuristic: check for logout link)
            const isGuest = !document.querySelector('a[href="/auth/logout"]');
            
            if (isGuest) {
                showAlert('Debes iniciar sesión para votar', 'error');
                setTimeout(() => {
                    window.location.href = '/auth/login';
                }, 1500);
                return;
            }

            try {
                // Disable button to prevent double clicks
                button.disabled = true;
                button.textContent = '...';

                const response = await fetch('/votos/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({ submission_id: submissionId })
                });

                const result = await response.json();

                if (response.ok) {
                    // Update vote counter in UI
                    const voteCounter = document.getElementById(`votes-${submissionId}`);
                    if (voteCounter) {
                        const currentVotes = parseInt(voteCounter.textContent.replace(/[^0-9]/g, '')) || 0;
                        voteCounter.textContent = `⭐ ${currentVotes + 1} votos`;
                    }
                    
                    showAlert('¡Voto registrado con éxito!', 'success');
                    
                    button.textContent = 'Votado';
                    button.disabled = true;
                    button.classList.remove('btn-primary');
                    button.classList.add('btn-secondary');
                } else {
                    showAlert(result.error || 'Error al votar', 'error');
                    button.disabled = false;
                    button.textContent = 'Votar';
                }
            } catch (error) {
                console.error('Error in voting:', error);
                showAlert('Error de conexión', 'error');
                button.disabled = false;
                button.textContent = 'Votar';
            }
        });
    });
});
