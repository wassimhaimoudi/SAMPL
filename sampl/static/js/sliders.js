document.getElementById('frequency-slider').addEventListener('input', function() {
        document.getElementById('frequency-value').textContent = this.value;
    });

document.getElementById('amplitude-slider').addEventListener('input', function() {
        document.getElementById('amplitude-value').textContent = this.value;
    });
