document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.delete-button').forEach(button => {
      button.addEventListener('click', function () {
        const drinkId = this.dataset.drinkId;
        const entry = this.closest('.drink-entry');
        const mgSpan = entry.querySelector('.drink-mg');
  
        const mgValue = parseInt(mgSpan.textContent);
        const fill = document.getElementById('caffeine-fill');
        const goalText = document.querySelector('.goal-text');
  
        fetch(`/delete_drink/${drinkId}`, {
          method: 'POST',
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          }
        })
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            entry.remove();
  
    
            const currentIntake = parseInt(fill.dataset.intake);
            const newIntake = currentIntake - mgValue;
            const goal = parseInt(fill.dataset.goal);
            const percent = Math.min((newIntake / goal) * 100, 100);
  
            fill.dataset.intake = newIntake;
            fill.style.height = percent + '%';
            goalText.innerHTML = `${newIntake}/${goal}<br>MG`;
          } else {
            alert('Failed to delete drink.');
          }
        })
        .catch(err => {
          console.error(err);
          alert('Server error.');
        });
      });
    });
  });
  