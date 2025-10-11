function updateStatus(id, newStatus) {
    fetch('/update_status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: id, status: newStatus })
    })
    .then(response => response.json())
    .then(data => {
        if(data.success){
            // Update the status text in the table
            document.getElementById(`status-${id}`).innerText = newStatus;

            // Optionally, disable the button after marking collected
            const btn = document.querySelector(`button[onclick="updateStatus(${id}, '${newStatus}')"]`);
            if(btn){
                btn.innerText = 'Collected';
                btn.className = 'btn btn-sm btn-secondary';
                btn.disabled = true;
            }
        } else {
            alert('Failed to update status: ' + data.msg);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while updating status.');
    });
}

  // Wait for the page to load
document.addEventListener("DOMContentLoaded", function() {
    // Select all flash alert divs
    const alerts = document.querySelectorAll('#flash-messages .alert');
    alerts.forEach(alert => {
        // Set timeout to remove each alert after 2 seconds (2000ms)
        setTimeout(() => {
            alert.classList.remove('show');
            alert.classList.add('hide');
            // Optional: remove from DOM completely after fade
            setTimeout(() => alert.remove(), 500);
        }, 2000);
    });
});
