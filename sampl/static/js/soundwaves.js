const oscillator = new Tone.Oscillator().toDestination();

document.getElementById('play-sound').addEventListener('click', () => {
    oscillator.start();
});

document.getElementById('frequency-slider').addEventListener('input', (e) => {
    oscillator.frequency.value = e.target.value;
    document.getElementById('frequency-value').textContent = e.target.value;
});

// Add similar listeners for waveform selection and amplitude
