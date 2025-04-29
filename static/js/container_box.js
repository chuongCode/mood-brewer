document.addEventListener('DOMContentLoaded', function() {
    const loginContainer = document.querySelector('.login-container');
    if (!loginContainer) return;

    // Create a new image object to preload the background
    const bgImage = new Image();
    bgImage.src = '/static/images/coffeebackground.png';
    
    // Show the container once the image is loaded
    bgImage.onload = function() {
        requestAnimationFrame(() => {
            loginContainer.classList.add('loaded');
        });
    };
    
    // Fallback in case the image fails to load
    bgImage.onerror = function() {
        requestAnimationFrame(() => {
            loginContainer.classList.add('loaded');
        });
    };
}); 