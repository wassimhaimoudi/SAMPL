document.addEventListener("DOMContentLoaded", function() {
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target); // Stop observing once the animation is triggered
            }
        });
    });

    document.querySelectorAll('.animate-slide-left, .animate-slide-right').forEach(element => {
        observer.observe(element);
    });
});
