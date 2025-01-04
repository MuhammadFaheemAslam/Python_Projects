// static/js/messages.js
document.addEventListener('DOMContentLoaded', function () {
    // Check if the modal exists
    const messageModal = document.getElementById('messageModal');
    if (messageModal) {
        // Show the modal
        const modal = new bootstrap.Modal(messageModal);
        modal.show();

        // Automatically close after 10 seconds
        setTimeout(() => {
            modal.hide();
        }, 10000); // 10 seconds
    }
});
